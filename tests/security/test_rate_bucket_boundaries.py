import pytest

from apps.api.middleware.rate_limit import InMemoryRateLimiter


def test_peer_capacity_is_bounded_without_resetting_existing_quota(monkeypatch):
    clock = [1000.0]
    monkeypatch.setattr('apps.api.middleware.rate_limit.time.time', lambda: clock[0])
    limiter = InMemoryRateLimiter(requests_per_window=1, max_clients=2)
    assert limiter.is_allowed('a')[0]
    assert limiter.is_allowed('b')[0]
    assert not limiter.is_allowed('c')[0]
    assert not limiter.is_allowed('a')[0]
    assert len(limiter._buckets) == 2
    clock[0] += 121
    assert limiter.is_allowed('c')[0]
    assert len(limiter._buckets) == 1


def test_peer_capacity_must_be_positive():
    with pytest.raises(ValueError):
        InMemoryRateLimiter(max_clients=0)
