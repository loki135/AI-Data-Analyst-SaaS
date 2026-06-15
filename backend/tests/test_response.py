"""Tests for shared response utilities."""

from app.core.response import ok, paginated


def test_ok_basic():
    result = ok({"key": "value"})
    assert result == {"success": True, "data": {"key": "value"}}


def test_ok_with_meta():
    result = ok([1, 2, 3], meta={"total": 3})
    assert result["meta"] == {"total": 3}


def test_paginated():
    result = paginated(items=[1, 2], page=1, per_page=10, total=25)
    assert result["success"] is True
    assert result["data"] == [1, 2]
    assert result["pagination"]["total_pages"] == 3
    assert result["pagination"]["page"] == 1
