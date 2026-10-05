"""事件聚合与报表。"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any


def aggregate(events: Iterable[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    """按 ``category`` 聚合事件。

    :param events: 事件序列，每条至少含 ``category`` 与 ``value``
    :returns: 形如 ``{类别: {"count": n, "total": x}}`` 的字典
    :raises KeyError: 事件缺少 ``category`` 字段

    示例::

        >>> aggregate([{"category": "a", "value": 1},
        ...            {"category": "a", "value": 2},
        ...            {"category": "b", "value": 5}])
        {'a': {'count': 2, 'total': 3}, 'b': {'count': 1, 'total': 5}}
    """
    buckets: dict[str, dict[str, Any]] = {}

    for event in events:
        category = event["category"]
        value = event.get("value", 0)
        bucket = buckets.setdefault(category, {"count": 0, "total": 0})
        bucket["count"] += 1
        bucket["total"] += value

    return buckets


def top_categories(report: Mapping[str, Mapping[str, Any]], n: int = 3) -> list[tuple[str, int]]:
    """取事件数最多的前 ``n`` 个类别。

    :param report: :func:`aggregate` 的返回值
    :param n: 取前几名，必须为正
    :returns: ``[(类别, count), …]``，按 count 从大到小
    :raises ValueError: ``n`` 非正

    示例::

        >>> top_categories({"a": {"count": 3}, "b": {"count": 1}}, n=1)
        [('a', 3)]
    """
    if n <= 0:
        raise ValueError("n 必须为正数")

    ranked = sorted(report.items(), key=lambda kv: kv[1]["count"], reverse=True)
    return [(name, int(entry["count"])) for name, entry in ranked[:n]]
