"""
Two-Tier Perceptual Inspection Cache Engine
===========================================
High-performance concurrent cache providing sub-millisecond retrieval of
canonical OCR declarations and compliance verdicts using perceptual hash
(pHash) visual similarity matching and lock-striped concurrency.

Architecture:
    - Tier 1: In-memory lock-striped LRU cache (16 stripes, zero contention).
    - Tier 2: File-backed persistent disk cache (JSON serialized).
    - Query Strategy:
        1. Exact SHA-256 lookup (O(1)).
        2. Perceptual pHash lookup (Hamming distance <= threshold).
"""

from __future__ import annotations

import collections
import datetime
import hashlib
import json
import os
import threading
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from apps.api.forensics.perceptual_hash import PerceptualHasher, PerceptualHashResult


@dataclass
class CachedInspectionEntry:
    """Cached canonical declaration and inspection outcome."""

    entry_id: str
    sha256_hash: str
    phash_int: int
    phash_hex: str
    commodity_type: str
    canonical_declarations: Dict[str, Any]
    compliance_verdict: str
    created_at_epoch: float
    last_accessed_epoch: float
    access_count: int = 1
    ttl_seconds: int = 86400  # 24 hours default TTL

    @property
    def is_expired(self) -> bool:
        return time.time() > (self.created_at_epoch + self.ttl_seconds)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "sha256_hash": self.sha256_hash,
            "phash_hex": self.phash_hex,
            "commodity_type": self.commodity_type,
            "canonical_declarations": self.canonical_declarations,
            "compliance_verdict": self.compliance_verdict,
            "created_at_epoch": self.created_at_epoch,
            "access_count": self.access_count,
        }


class CacheStripe:
    """Single lock-protected LRU shard in the cache."""

    def __init__(self, max_capacity: int = 256) -> None:
        self.max_capacity = max_capacity
        self._lock = threading.RLock()
        self._sha_map: Dict[str, CachedInspectionEntry] = {}
        # List of (phash_int, entry) for linear perceptual scan
        self._phash_list: List[Tuple[int, CachedInspectionEntry]] = []

    def get_by_sha(self, sha256_hash: str) -> Optional[CachedInspectionEntry]:
        with self._lock:
            entry = self._sha_map.get(sha256_hash)
            if entry:
                if entry.is_expired:
                    self._remove_entry(entry)
                    return None
                entry.last_accessed_epoch = time.time()
                entry.access_count += 1
                return entry
            return None

    def get_by_phash(
        self, phash_int: int, max_hamming_distance: int = 2
    ) -> Optional[CachedInspectionEntry]:
        with self._lock:
            best_entry = None
            best_dist = 65

            for p_int, entry in self._phash_list:
                if entry.is_expired:
                    continue
                dist = (phash_int ^ p_int).bit_count()
                if dist <= max_hamming_distance and dist < best_dist:
                    best_dist = dist
                    best_entry = entry

            if best_entry:
                best_entry.last_accessed_epoch = time.time()
                best_entry.access_count += 1
                return best_entry
            return None

    def put(self, entry: CachedInspectionEntry) -> None:
        with self._lock:
            # Evict LRU if capacity reached
            if len(self._sha_map) >= self.max_capacity:
                lru_key = min(self._sha_map, key=lambda k: self._sha_map[k].last_accessed_epoch)
                self._remove_entry(self._sha_map[lru_key])

            self._sha_map[entry.sha256_hash] = entry
            self._phash_list.append((entry.phash_int, entry))

    def _remove_entry(self, entry: CachedInspectionEntry) -> None:
        self._sha_map.pop(entry.sha256_hash, None)
        self._phash_list = [(p, e) for p, e in self._phash_list if e.entry_id != entry.entry_id]

    def purge_expired(self) -> int:
        with self._lock:
            expired_keys = [k for k, v in self._sha_map.items() if v.is_expired]
            for k in expired_keys:
                self._remove_entry(self._sha_map[k])
            return len(expired_keys)

    def size(self) -> int:
        with self._lock:
            return len(self._sha_map)


class TwoTierInspectionCache:
    """
    Two-tier concurrent perceptual cache manager.
    """

    NUM_STRIPES = 16

    def __init__(
        self,
        disk_cache_dir: Optional[Path] = None,
        stripe_capacity: int = 256,
        max_hamming_distance: int = 2,
    ) -> None:
        self.disk_cache_dir = disk_cache_dir or Path(
            os.environ.get("TEMP", "/tmp")
        ) / "metrolens_perceptual_cache"
        self.disk_cache_dir.mkdir(parents=True, exist_ok=True)

        self.max_hamming_distance = max_hamming_distance
        self.hasher = PerceptualHasher()
        self._stripes = [CacheStripe(max_capacity=stripe_capacity) for _ in range(self.NUM_STRIPES)]

        # Telemetry
        self.hits_sha = 0
        self.hits_phash = 0
        self.misses = 0
        self._telemetry_lock = threading.Lock()

    def _get_stripe_index(self, key_str: str) -> int:
        """Hash string to a stripe index 0..NUM_STRIPES-1."""
        h = int(hashlib.md5(key_str.encode("utf-8")).hexdigest(), 16)
        return h % self.NUM_STRIPES

    def lookup(
        self,
        image_bytes: bytes,
        allow_perceptual_match: bool = True,
    ) -> Tuple[Optional[CachedInspectionEntry], str]:
        """
        Lookup cached inspection result by raw bytes.

        Returns:
            Tuple of (Optional[CachedInspectionEntry], hit_type: 'SHA_HIT' | 'PHASH_HIT' | 'MISS')
        """
        sha256_hex = hashlib.sha256(image_bytes).hexdigest()
        stripe_idx = self._get_stripe_index(sha256_hex)
        stripe = self._stripes[stripe_idx]

        # 1. Tier 1: Exact SHA-256 in memory
        entry = stripe.get_by_sha(sha256_hex)
        if entry:
            with self._telemetry_lock:
                self.hits_sha += 1
            return entry, "SHA_HIT"

        # 2. Tier 2: Check disk cache for exact SHA-256
        disk_entry = self._read_from_disk(sha256_hex)
        if disk_entry and not disk_entry.is_expired:
            stripe.put(disk_entry)
            with self._telemetry_lock:
                self.hits_sha += 1
            return disk_entry, "SHA_HIT"

        # 3. Perceptual pHash lookup across stripes
        if allow_perceptual_match:
            try:
                phash_res = self.hasher.compute(image_bytes)
                for s in self._stripes:
                    match = s.get_by_phash(phash_res.phash_int, self.max_hamming_distance)
                    if match:
                        with self._telemetry_lock:
                            self.hits_phash += 1
                        return match, "PHASH_HIT"
            except Exception:
                pass

        with self._telemetry_lock:
            self.misses += 1
        return None, "MISS"

    def put(
        self,
        image_bytes: bytes,
        commodity_type: str,
        canonical_declarations: Dict[str, Any],
        compliance_verdict: str,
        ttl_seconds: int = 86400,
    ) -> CachedInspectionEntry:
        """Store newly evaluated inspection result into both tiers."""
        sha256_hex = hashlib.sha256(image_bytes).hexdigest()
        phash_res = self.hasher.compute(image_bytes)

        now = time.time()
        entry = CachedInspectionEntry(
            entry_id=f"CACHE-{sha256_hex[:12].upper()}",
            sha256_hash=sha256_hex,
            phash_int=phash_res.phash_int,
            phash_hex=phash_res.phash_hex,
            commodity_type=commodity_type,
            canonical_declarations=canonical_declarations,
            compliance_verdict=compliance_verdict,
            created_at_epoch=now,
            last_accessed_epoch=now,
            ttl_seconds=ttl_seconds,
        )

        # Store in-memory
        stripe_idx = self._get_stripe_index(sha256_hex)
        self._stripes[stripe_idx].put(entry)

        # Store to disk
        self._write_to_disk(entry)
        return entry

    def _write_to_disk(self, entry: CachedInspectionEntry) -> None:
        try:
            target_path = self.disk_cache_dir / f"{entry.sha256_hash}.json"
            target_path.write_text(json.dumps(entry.to_dict(), indent=2), encoding="utf-8")
        except Exception:
            pass

    def _read_from_disk(self, sha256_hex: str) -> Optional[CachedInspectionEntry]:
        try:
            target_path = self.disk_cache_dir / f"{sha256_hex}.json"
            if not target_path.is_file():
                return None
            data = json.loads(target_path.read_text(encoding="utf-8"))
            p_int = int(data.get("phash_hex", "0"), 16)
            return CachedInspectionEntry(
                entry_id=data.get("entry_id", ""),
                sha256_hash=data.get("sha256_hash", sha256_hex),
                phash_int=p_int,
                phash_hex=data.get("phash_hex", ""),
                commodity_type=data.get("commodity_type", "FMCG"),
                canonical_declarations=data.get("canonical_declarations", {}),
                compliance_verdict=data.get("compliance_verdict", "COMPLIANT"),
                created_at_epoch=data.get("created_at_epoch", time.time()),
                last_accessed_epoch=time.time(),
                access_count=data.get("access_count", 1),
            )
        except Exception:
            return None

    def get_stats(self) -> Dict[str, Any]:
        """Return cache hit ratio and capacity statistics."""
        with self._telemetry_lock:
            total_queries = self.hits_sha + self.hits_phash + self.misses
            hit_ratio = (
                (self.hits_sha + self.hits_phash) / total_queries if total_queries > 0 else 0.0
            )
            total_entries = sum(s.size() for s in self._stripes)

            return {
                "total_queries": total_queries,
                "hits_sha": self.hits_sha,
                "hits_phash": self.hits_phash,
                "misses": self.misses,
                "hit_ratio": round(hit_ratio, 4),
                "in_memory_entries": total_entries,
                "stripes_count": self.NUM_STRIPES,
            }
