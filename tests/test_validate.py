"""输入校验与清洗。"""

from __future__ import annotations

import pytest

from envkit import parse_email, parse_port, sanitize_filename


def test_sanitize_replaces_unsafe_chars():
    assert sanitize_filename("report<1>.txt") == "report_1_.txt"
    assert sanitize_filename('a|b?c*d.txt') == "a_b_c_d.txt"


def test_sanitize_replaces_path_separators():
    assert sanitize_filename("dir/file.txt") == "dir_file.txt"
    assert sanitize_filename("dir\\file.txt") == "dir_file.txt"


def test_sanitize_blocks_directory_traversal():
    assert "/" not in sanitize_filename("../../etc/passwd")
    assert ".." not in sanitize_filename("../../etc/passwd")


def test_sanitize_strips_surrounding_dots_and_spaces():
    assert sanitize_filename("  report.txt  ") == "report.txt"


def test_sanitize_rejects_empty_result():
    with pytest.raises(ValueError):
        sanitize_filename("   ")
    with pytest.raises(ValueError):
        sanitize_filename("...")


def test_sanitize_rejects_non_str():
    with pytest.raises(TypeError):
        sanitize_filename(123)  # type: ignore[arg-type]


def test_parse_port_basic():
    assert parse_port("8080") == 8080
    assert parse_port(443) == 443


def test_parse_port_bounds():
    assert parse_port(1) == 1
    assert parse_port(65535) == 65535


def test_parse_port_rejects_out_of_range():
    with pytest.raises(ValueError):
        parse_port(65536)
    with pytest.raises(ValueError):
        parse_port(-1)


def test_parse_port_rejects_zero():
    with pytest.raises(ValueError):
        parse_port(0)


def test_parse_email_normalizes():
    assert parse_email("  User@Example.COM ") == "user@example.com"


def test_parse_email_rejects_invalid():
    for bad in ("no-at-sign", "a@b", "@b.com", "a@.com", "a b@c.com"):
        with pytest.raises(ValueError):
            parse_email(bad)


def test_parse_email_rejects_non_str():
    with pytest.raises(TypeError):
        parse_email(None)  # type: ignore[arg-type]
