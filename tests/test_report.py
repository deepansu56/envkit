"""事件聚合与报表。"""

from __future__ import annotations

import pytest

from envkit import aggregate
from envkit.report import top_categories


def test_aggregate_counts_and_totals():
    report = aggregate(
        [
            {"category": "a", "value": 1},
            {"category": "a", "value": 2},
            {"category": "b", "value": 5},
        ]
    )
    assert report == {"a": {"count": 2, "total": 3}, "b": {"count": 1, "total": 5}}


def test_aggregate_empty():
    assert aggregate([]) == {}


def test_aggregate_value_defaults_to_zero():
    assert aggregate([{"category": "x"}]) == {"x": {"count": 1, "total": 0}}


def test_aggregate_requires_category():
    with pytest.raises(KeyError):
        aggregate([{"value": 1}])


def test_aggregate_keeps_negative_values():
    report = aggregate([{"category": "a", "value": -3}])
    assert report["a"]["total"] == -3


def test_top_categories_orders_by_count():
    report = aggregate(
        [
            {"category": "a", "value": 1},
            {"category": "a", "value": 1},
            {"category": "b", "value": 1},
            {"category": "c", "value": 1},
            {"category": "c", "value": 1},
            {"category": "c", "value": 1},
        ]
    )
    assert top_categories(report, n=2) == [("c", 3), ("a", 2)]


def test_top_categories_limits_n():
    report = {"a": {"count": 1}, "b": {"count": 2}}
    assert len(top_categories(report, n=1)) == 1


def test_top_categories_rejects_non_positive_n():
    with pytest.raises(ValueError):
        top_categories({}, n=0)
