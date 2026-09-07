"""
Integration Tests for Chunk 6: Leaky-Bucket Rate Limiter & Security Hardening.
Verifies:
1. In-memory sliding-window algorithm allows burst within limit.
2. 11th request from same IP is blocked with HTTP 429 RATE_LIMIT_EXCEEDED.
3. Response headers strictly include Retry-After.
4. Administrative and health routes (/health, /api/v1/health) are exempt from rate limiting.
5. Distinct IP addresses maintain independent quota pools.
6. Periodic stale bucket sweep prevents memory exhaustion.
"""

import time
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.api.middleware.rate_limit import InMemoryRateLimiter, RateLimitMiddleware
from apps.api.errors import register_error_handlers


@pytest.fixture
def rate_limited_app():
    """Creates an isolated FastAPI application equipped with RateLimitMiddleware for testing."""
    test_app = FastAPI()
    register_error_handlers(test_app)

    # Tight limits for testing: 5 requests per 10 seconds
    limiter = InMemoryRateLimiter(requests_per_window=5, window_seconds=10, cleanup_interval_seconds=1)
    test_app.add_middleware(RateLimitMiddleware, rate_limiter=limiter)

    @test_app.get("/api/v1/test-endpoint")
    def sample_endpoint():
        return {"status": "ok"}

    @test_app.get("/health")
    def health():
        return {"status": "healthy"}

    @test_app.get("/api/v1/health")
    def api_health():
        return {"status": "healthy"}

    return test_app, limiter


# =========================================================================
# Unit Tests for InMemoryRateLimiter Core
# =========================================================================

def test_rate_limiter_in_memory_sliding_window():
    """Verifies that InMemoryRateLimiter accurately tracks sliding-window counts."""
    limiter = InMemoryRateLimiter(requests_per_window=3, window_seconds=2)
    client_ip = "192.168.1.100"

    # Requests 1, 2, 3 must pass
    for _ in range(3):
        allowed, retry_after = limiter.is_allowed(client_ip)
        assert allowed is True
        assert retry_after == 0

    # Request 4 must fail
    allowed, retry_after = limiter.is_allowed(client_ip)
    assert allowed is False
    assert retry_after > 0
    assert retry_after <= 3

    # Reset client
    limiter.reset_client(client_ip)
    allowed, retry_after = limiter.is_allowed(client_ip)
    assert allowed is True


def test_rate_limiter_multi_ip_isolation():
    """Verifies that separate client IPs maintain independent quotas."""
    limiter = InMemoryRateLimiter(requests_per_window=2, window_seconds=60)
    ip_a = "10.0.0.1"
    ip_b = "10.0.0.2"

    # Exhaust IP A
    assert limiter.is_allowed(ip_a)[0] is True
    assert limiter.is_allowed(ip_a)[0] is True
    assert limiter.is_allowed(ip_a)[0] is False

    # IP B must still be fully permitted
    assert limiter.is_allowed(ip_b)[0] is True
    assert limiter.is_allowed(ip_b)[0] is True
    assert limiter.is_allowed(ip_b)[0] is False


def test_rate_limiter_stale_bucket_sweep():
    """Verifies that inactive buckets are purged during periodic sweeps."""
    limiter = InMemoryRateLimiter(requests_per_window=5, window_seconds=1, cleanup_interval_seconds=1)
    ip_stale = "172.16.0.5"

    limiter.is_allowed(ip_stale)
    assert ip_stale in limiter._buckets

    # Simulate time lapse beyond window * 2
    past_time = time.time() + 10.0
    limiter._sweep_stale_buckets(past_time)

    assert ip_stale not in limiter._buckets


# =========================================================================
# Integration Tests for RateLimitMiddleware
# =========================================================================

def test_rate_limit_middleware_blocks_on_threshold(rate_limited_app):
    """
    Verifies that requests exceeding quota return HTTP 429
    with canonical error JSON envelope and Retry-After header.
    """
    test_app, limiter = rate_limited_app
    client = TestClient(test_app)

    # First 5 requests must succeed (HTTP 200)
    for i in range(5):
        resp = client.get("/api/v1/test-endpoint", headers={"X-Forwarded-For": "203.0.113.195"})
        assert resp.status_code == 200, f"Request {i+1} failed unexpectedly: {resp.text}"

    # 6th request must be rejected with HTTP 429
    blocked_resp = client.get("/api/v1/test-endpoint", headers={"X-Forwarded-For": "203.0.113.195"})
    assert blocked_resp.status_code == 429
    assert "Retry-After" in blocked_resp.headers

    data = blocked_resp.json()
    assert "error" in data
    assert data["error"]["code"] == "RATE_LIMIT_EXCEEDED"
    assert "statutory threshold" in data["error"]["message"]
    assert "retry_after_seconds" in data["error"]["details"]


def test_rate_limit_exempts_health_and_docs(rate_limited_app):
    """
    Verifies that administrative paths (/health, /api/v1/health)
    are strictly exempt from rate limiting and never return HTTP 429.
    """
    test_app, limiter = rate_limited_app
    client = TestClient(test_app)

    client_ip = "198.51.100.42"

    # Send 15 consecutive requests to /health
    for _ in range(15):
        resp = client.get("/health", headers={"X-Forwarded-For": client_ip})
        assert resp.status_code == 200

    # Send 15 consecutive requests to /api/v1/health
    for _ in range(15):
        resp = client.get("/api/v1/health", headers={"X-Forwarded-For": client_ip})
        assert resp.status_code == 200
