"""时区偏移与 ISO-8601 解析。"""

from __future__ import annotations

import pytest

from envkit import parse_offset, split_iso


def test_offset_positive():
    assert parse_offset("+08:00") == 480


def test_offset_zero_forms():
    assert parse_offset("Z") == 0
    assert parse_offset("z") == 0
    assert parse_offset("+00:00") == 0


def test_offset_without_sign_treated_as_positive():
    assert parse_offset("03:00") == 180


def test_offset_rejects_bad_format():
    with pytest.raises(ValueError):
        parse_offset("eight")
    with pytest.raises(ValueError):
        parse_offset("+8")


def test_offset_rejects_minutes_out_of_range():
    with pytest.raises(ValueError):
        parse_offset("+08:75")


def test_offset_rejects_non_str():
    with pytest.raises(TypeError):
        parse_offset(480)  # type: ignore[arg-type]


def test_split_iso_basic_fields():
    parts = split_iso("2024-03-05T08:30:00+08:00")
    assert parts["year"] == 2024
    assert parts["month"] == 3
    assert parts["day"] == 5
    assert parts["hour"] == 8
    assert parts["minute"] == 30
    assert parts["second"] == 0
    assert parts["offset"] == 480


def test_split_iso_without_offset():
    assert split_iso("2024-01-01T00:00:00")["offset"] == 0


def test_split_iso_rejects_missing_t():
    with pytest.raises(ValueError):
        split_iso("2024-03-05 08:30:00")


def test_split_iso_rejects_bad_date():
    with pytest.raises(ValueError):
        split_iso("2024-03T08:30:00")
