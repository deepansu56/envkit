"""TTL 缓存。"""

from __future__ import annotations

import pytest

from envkit import TTLCache


class FakeClock:
    """可手动推进的假时钟，用来稳定复现过期行为。"""

    def __init__(self, start: float = 0.0) -> None:
        self.now = start

    def __call__(self) -> float:
        return self.now

    def tick(self, seconds: float) -> None:
        self.now += seconds


def test_set_and_get():
    cache = TTLCache(ttl=60)
    cache.set("a", 1)
    assert cache.get("a") == 1


def test_get_missing_returns_default():
    cache = TTLCache(ttl=60)
    assert cache.get("nope") is None
    assert cache.get("nope", default="fallback") == "fallback"


def test_get_before_expiry():
    clock = FakeClock()
    cache = TTLCache(ttl=10, clock=clock)
    cache.set("a", "v")
    clock.tick(9.5)
    assert cache.get("a") == "v"


def test_contains_respects_expiry():
    clock = FakeClock()
    cache = TTLCache(ttl=10, clock=clock)
    cache.set("a", 1)
    assert "a" in cache
    clock.tick(10)
    assert "a" not in cache


def test_overwrite_resets_expiry():
    clock = FakeClock()
    cache = TTLCache(ttl=10, clock=clock)
    cache.set("a", 1)
    clock.tick(9)
    cache.set("a", 2)
    clock.tick(9)
    assert cache.get("a") == 2


def test_purge_removes_only_expired():
    clock = FakeClock()
    cache = TTLCache(ttl=10, clock=clock)
    cache.set("old", 1)
    clock.tick(11)
    cache.set("fresh", 2)
    assert cache.purge() == 1
    assert cache.get("fresh") == 2


def test_stats_shape():
    cache = TTLCache(ttl=60)
    cache.set("a", 1)
    cache.get("a")
    cache.get("nope")
    stats = cache.stats()
    assert stats["size"] == 1
    assert set(stats) == {"hits", "misses", "size"}


def test_rejects_non_positive_ttl():
    with pytest.raises(ValueError):
        TTLCache(ttl=0)
    with pytest.raises(ValueError):
        TTLCache(ttl=-5)
