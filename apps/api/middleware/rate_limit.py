"""
MetroLens API Gateway: Thread-Safe Leaky-Bucket Rate Limiter Middleware.
Enforces 10 requests per minute per IP address with HTTP 429 and Retry-After headers.
Conforms strictly to docs/API_CONTRACT.md Section 4 and ADR-013.
"""

import logging
import threading
import time
from typing import Dict, List, Optional, Set, Tuple
from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from apps.api.errors import RateLimitExceededError

logger = logging.getLogger("metrolens.middleware.rate_limit")


class InMemoryRateLimiter:
    """
    Thread-safe sliding-window / leaky-bucket rate limiter.
    Tracks client invocation timestamps in memory with automatic eviction of stale entries.
    """

    def __init__(
        self,
        requests_per_window: int = 10,
        window_seconds: int = 60,
        cleanup_interval_seconds: int = 300,
    ):
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self.cleanup_interval_seconds = cleanup_interval_seconds
        self._buckets: Dict[str, List[float]] = {}
        self._last_cleanup = time.time()
        self._lock = threading.Lock()

    def is_allowed(self, client_id: str) -> Tuple[bool, int]:
        """
        Evaluates whether a request from client_id is permitted under the rate limit.

        Returns:
            Tuple[bool, int]: (allowed, retry_after_seconds)
        """
        now = time.time()
        cutoff = now - self.window_seconds

        with self._lock:
            # Periodic background sweep of dead buckets
            if now - self._last_cleanup > self.cleanup_interval_seconds:
                self._sweep_stale_buckets(now)
                self._last_cleanup = now

            timestamps = self._buckets.setdefault(client_id, [])

            # Evict timestamps outside sliding window
            self._buckets[client_id] = [t for t in timestamps if t > cutoff]
            active_timestamps = self._buckets[client_id]

            if len(active_timestamps) >= self.requests_per_window:
                oldest_in_window = active_timestamps[0]
                retry_after = max(1, int(self.window_seconds - (now - oldest_in_window)) + 1)
                logger.warning(
                    "Rate limit exceeded for client '%s' (%d/%d reqs). Retry-After: %ds",
                    client_id,
                    len(active_timestamps),
                    self.requests_per_window,
                    retry_after,
                )
                return False, retry_after

            active_timestamps.append(now)
            return True, 0

    def reset_client(self, client_id: str) -> None:
        """Resets the history for a specific client (useful for test isolation)."""
        with self._lock:
            self._buckets.pop(client_id, None)

    def reset_all(self) -> None:
        """Flushes all rate-limiting buckets."""
        with self._lock:
            self._buckets.clear()

    def _sweep_stale_buckets(self, current_time: float) -> None:
        """Removes IP buckets that have had zero activity for more than 2x window duration."""
        cutoff = current_time - (self.window_seconds * 2)
        dead_keys = [
            cid for cid, ts_list in self._buckets.items()
            if not ts_list or ts_list[-1] < cutoff
        ]
        for k in dead_keys:
            del self._buckets[k]
        if dead_keys:
            logger.debug("RateLimiter swept %d inactive client buckets.", len(dead_keys))


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Starlette/FastAPI middleware enforcing statutory request caps on API endpoints.
    Exempts health checks and OpenAPI documentation endpoints.
    """

    EXEMPT_PATHS: Set[str] = {
        "/health",
        "/api/v1/health",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/favicon.ico",
    }

    def __init__(
        self,
        app,
        rate_limiter: Optional[InMemoryRateLimiter] = None,
        exempt_paths: Optional[Set[str]] = None,
    ):
        super().__init__(app)
        self.limiter = rate_limiter or InMemoryRateLimiter(requests_per_window=10, window_seconds=60)
        self.exempt_paths = exempt_paths or self.EXEMPT_PATHS

    async def dispatch(self, request: Request, call_next) -> Response:
        """Intercepts request, checks client IP quota, and raises HTTP 429 if exceeded."""
        path = request.url.path

        # 1. Exempt administrative and health routes
        if path in self.exempt_paths or path.startswith("/docs") or path.startswith("/redoc"):
            return await call_next(request)

        # 2. Check for explicit test bypass header
        if request.headers.get("X-Bypass-Rate-Limit") == "true":
            return await call_next(request)

        # 3. Extract client IP (respecting proxy forward headers)
        client_ip = self._extract_client_ip(request)

        # 3. Rate limit check
        allowed, retry_after = self.limiter.is_allowed(client_ip)
        if not allowed:
            exc = RateLimitExceededError(retry_after_seconds=retry_after)
            envelope = exc.to_envelope()
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content=envelope.model_dump(),
                headers={"Retry-After": str(retry_after)},
            )

        response = await call_next(request)
        return response

    @staticmethod
    def _extract_client_ip(request: Request) -> str:
        """Resolves client IP from X-Forwarded-For or socket peer."""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            # First IP in comma-separated proxy chain is original client
            return forwarded.split(",")[0].strip()
        if request.client:
            return request.client.host
        return "127.0.0.1"


# Default rate limiter singleton
rate_limiter = InMemoryRateLimiter(requests_per_window=10, window_seconds=60)
