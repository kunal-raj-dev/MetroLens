"""
Internal batch image screening helper; no HTTP endpoint mounts this module.

ZIP members are bounded and inspected sequentially by the real pipeline. Results
preserve uncertain and exempt states and do not calculate enforcement penalties.
"""

from __future__ import annotations

import datetime
import io
import os
import zipfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Dict, List, Optional, Tuple

from apps.api.middleware.security import ImageSecurityValidator, MAX_UPLOAD_SIZE_BYTES
from apps.api.services.pipeline_orchestrator import pipeline_orchestrator
from apps.api.services.task_queue import (
    PrioritizedInspectionQueue,
)


@dataclass
class SingleInspectionSummary:
    """Brief summary of a single inspected packaging in a batch raid."""

    filename: str
    inspection_id: str
    overall_verdict: str
    commodity_category: str
    declared_net_quantity: Optional[str] = None
    declared_mrp: Optional[str] = None
    violations_count: int = 0
    violated_rules: List[str] = field(default_factory=list)
    processing_time_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "inspection_id": self.inspection_id,
            "overall_verdict": self.overall_verdict,
            "commodity_category": self.commodity_category,
            "declared_net_quantity": self.declared_net_quantity,
            "declared_mrp": self.declared_mrp,
            "violations_count": self.violations_count,
            "violated_rules": self.violated_rules,
            "processing_time_ms": round(self.processing_time_ms, 2),
        }


@dataclass
class RaidBatchReport:
    """Screening counts; failed rule groups are not adjudicated violations."""

    batch_id: str
    timestamp_utc: str
    establishment_name: str
    district: str
    state: str
    total_images_processed: int
    compliant_count: int
    non_compliant_count: int
    compliance_rate_percent: float
    total_potential_compounding_inr: int
    violations_by_rule: Dict[str, int] = field(default_factory=dict)
    itemized_results: List[SingleInspectionSummary] = field(default_factory=list)
    rejected_files: List[Dict[str, str]] = field(default_factory=list)
    review_required_count: int = 0
    exempted_count: int = 0
    potential_non_compliance_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "batch_id": self.batch_id,
            "timestamp_utc": self.timestamp_utc,
            "establishment_name": self.establishment_name,
            "district": self.district,
            "state": self.state,
            "total_images_processed": self.total_images_processed,
            "compliant_count": self.compliant_count,
            "non_compliant_count": self.non_compliant_count,
            "review_required_count": self.review_required_count,
            "exempted_count": self.exempted_count,
            "potential_non_compliance_count": self.potential_non_compliance_count,
            "compliance_rate_percent": round(self.compliance_rate_percent, 2),
            "total_potential_compounding_inr": self.total_potential_compounding_inr,
            "compounding_estimate_available": False,
            "violations_by_rule": self.violations_by_rule,
            "itemized_results": [r.to_dict() for r in self.itemized_results],
            "rejected_files": self.rejected_files,
        }


class RetailRaidBatchProcessor:
    """
    Safely unpacks ZIP archives and orchestrates batch packaging audits.
    """

    MAX_ZIP_ENTRIES = 200
    MAX_TOTAL_UNCOMPRESSED_BYTES = 250 * 1024 * 1024  # 250 MB max
    MAX_ARCHIVE_BYTES = 250 * 1024 * 1024
    MAX_ENTRY_UNCOMPRESSED_BYTES = MAX_UPLOAD_SIZE_BYTES
    MAX_COMPRESSION_RATIO = 50.0  # Max 50:1 ratio (Zip Bomb Defense)

    def __init__(
        self,
        security_validator: Optional[ImageSecurityValidator] = None,
        task_queue: Optional[PrioritizedInspectionQueue] = None,
    ) -> None:
        self.validator = security_validator or ImageSecurityValidator()
        # Reserved constructor compatibility: this helper currently runs sequentially.
        self.task_queue = task_queue

    def process_zip_archive(
        self,
        zip_bytes: bytes,
        establishment_name: str,
        district: str,
        state: str,
        batch_id: Optional[str] = None,
    ) -> RaidBatchReport:
        """
        Unpack ZIP archive with zip-bomb defenses and inspect images.

        Args:
            zip_bytes: Raw binary bytes of uploaded ZIP archive.
            establishment_name: Supermarket / warehouse name under inspection.
            district: District jurisdiction name.
            state: State jurisdiction name.
            batch_id: Optional identifier string.
        """
        bid = batch_id or f"RAID-{datetime.datetime.now().strftime('%Y%m%d')}-{os.urandom(4).hex().upper()}"
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

        valid_images: List[Tuple[str, bytes]] = []
        rejected: List[Dict[str, str]] = []

        # 1. Inspect and extract ZIP entries safely
        try:
            if len(zip_bytes) > self.MAX_ARCHIVE_BYTES:
                raise ValueError("Compressed archive size exceeds the allowed limit.")
            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
                infolist = zf.infolist()
                if len(infolist) > self.MAX_ZIP_ENTRIES:
                    raise ValueError(
                        f"ZIP archive contains {len(infolist)} files; exceeds maximum limit of {self.MAX_ZIP_ENTRIES}."
                    )

                total_uncompressed = 0
                seen_filenames = set()
                for info in infolist:
                    # Skip directories
                    if info.is_dir():
                        continue

                    # Defense against Directory Traversal (Zip Slip)
                    member_path = PurePosixPath(info.filename.replace("\\", "/"))
                    filename = member_path.name
                    if (not filename or ".." in member_path.parts or member_path.is_absolute()
                            or PureWindowsPath(info.filename).drive or ":" in info.filename):
                        rejected.append({"filename": info.filename, "reason": "Suspicious directory traversal path"})
                        continue
                    if filename.casefold() in seen_filenames:
                        rejected.append({"filename": filename, "reason": "Duplicate image filename"})
                        continue
                    seen_filenames.add(filename.casefold())
                    if info.file_size > self.MAX_ENTRY_UNCOMPRESSED_BYTES:
                        rejected.append({"filename": filename, "reason": "Image member size exceeds the allowed limit"})
                        continue

                    # Defense against Zip Bomb
                    if info.compress_size > 0:
                        ratio = info.file_size / float(info.compress_size)
                        if ratio > self.MAX_COMPRESSION_RATIO:
                            rejected.append(
                                {
                                    "filename": filename,
                                    "reason": f"Suspicious compression ratio ({ratio:.1f}:1 exceeds {self.MAX_COMPRESSION_RATIO}:1)",
                                }
                            )
                            continue

                    remaining = self.MAX_TOTAL_UNCOMPRESSED_BYTES - total_uncompressed
                    if info.file_size > remaining:
                        raise ValueError(
                            f"Uncompressed ZIP payload exceeds {self.MAX_TOTAL_UNCOMPRESSED_BYTES // (1024*1024)} MB limit."
                        )

                    # Open the checked member, not a filename lookup that can select
                    # another duplicate entry. Bound actual output as well as metadata.
                    read_limit = min(self.MAX_ENTRY_UNCOMPRESSED_BYTES, remaining)
                    with zf.open(info) as member:
                        data = member.read(read_limit + 1)
                    if len(data) > read_limit or len(data) != info.file_size:
                        raise ValueError("ZIP member decompressed size exceeds or disagrees with its declared size.")
                    total_uncompressed += len(data)

                    # Verify image magic bytes
                    if not self._is_valid_image_extension_and_bytes(filename, data):
                        rejected.append({"filename": filename, "reason": "Unsupported image format or magic bytes"})
                        continue

                    valid_images.append((filename, data))

        except Exception as exc:
            return RaidBatchReport(
                batch_id=bid,
                timestamp_utc=now_iso,
                establishment_name=establishment_name,
                district=district,
                state=state,
                total_images_processed=0,
                compliant_count=0,
                non_compliant_count=0,
                compliance_rate_percent=0.0,
                total_potential_compounding_inr=0,
                rejected_files=[{"filename": "ARCHIVE", "reason": f"Corrupt or unsafe ZIP archive: {str(exc)}"}],
            )

        # 2. Execute inspections on valid extracted images
        itemized: List[SingleInspectionSummary] = []
        violations_by_rule: Dict[str, int] = {}
        comp_count = 0
        non_comp_count = 0
        review_count = 0
        exempt_count = 0
        potential_count = 0

        for fname, img_data in valid_images:
            start_t = datetime.datetime.now()
            try:
                # Orchestrate inspection
                resp = pipeline_orchestrator.orchestrate_inspection(
                    image_bytes=img_data,
                    filename=fname,
                )
                dur_ms = (datetime.datetime.now() - start_t).total_seconds() * 1000.0

                groups = resp.rule_evaluations
                failed_rules = [
                    rule for rule, status in (
                        ("Rule 6(1)", groups.rule6_mandatory_status.overall_status),
                        ("Rule 6(11)", groups.usp_audit.status),
                        ("Rule 7", groups.font_height_audit.status),
                    ) if status == "FAIL"
                ]
                net_qty_str = (
                    f"{resp.declarations.net_quantity_value} {resp.declarations.net_quantity_unit}"
                    if resp.declarations.net_quantity_value is not None
                    else None
                )
                mrp_str = (
                    f"Rs. {resp.declarations.mrp_inr}"
                    if resp.declarations.mrp_inr is not None
                    else None
                )
                itemized.append(
                    SingleInspectionSummary(
                        filename=fname,
                        inspection_id=resp.inspection_id,
                        overall_verdict=resp.state,
                        commodity_category=resp.declarations.commodity_name or "Unknown",
                        declared_net_quantity=net_qty_str,
                        declared_mrp=mrp_str,
                        violations_count=len(failed_rules),
                        violated_rules=failed_rules,
                        processing_time_ms=dur_ms,
                    )
                )
                # Count only complete, successfully summarized responses.
                if resp.state == "COMPLIANT":
                    comp_count += 1
                elif resp.state == "NON_COMPLIANT":
                    non_comp_count += 1
                elif resp.state == "EXEMPTED":
                    exempt_count += 1
                elif resp.state == "POTENTIAL_NON_COMPLIANCE":
                    potential_count += 1
                else:
                    review_count += 1
                for rule in failed_rules:
                    violations_by_rule[rule] = violations_by_rule.get(rule, 0) + 1
            except Exception as e:
                rejected.append({"filename": fname, "reason": f"Inspection pipeline execution error: {str(e)}"})

        total_processed = len(itemized)
        comp_rate = (comp_count / total_processed * 100.0) if total_processed > 0 else 0.0
        # A preliminary image assessment supplies no authority or verified basis
        # for calculating a compounding amount. Retain the legacy numeric field only.

        return RaidBatchReport(
            batch_id=bid,
            timestamp_utc=now_iso,
            establishment_name=establishment_name,
            district=district,
            state=state,
            total_images_processed=total_processed,
            compliant_count=comp_count,
            non_compliant_count=non_comp_count,
            compliance_rate_percent=comp_rate,
            total_potential_compounding_inr=0,
            violations_by_rule=violations_by_rule,
            itemized_results=itemized,
            rejected_files=rejected,
            review_required_count=review_count,
            exempted_count=exempt_count,
            potential_non_compliance_count=potential_count,
        )

    def _is_valid_image_extension_and_bytes(self, filename: str, data: bytes) -> bool:
        ext = Path(filename).suffix.lower()
        if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
            return False
        if data.startswith(b"\xFF\xD8\xFF") or data.startswith(b"\x89PNG\r\n\x1a\n") or (data.startswith(b"RIFF") and data[8:12] == b"WEBP"):
            return True
        return False
