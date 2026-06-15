"""Tests for app.data_ingestion.parsers."""

import pytest

from app.data_ingestion.parsers import parse_csv, parse_json


class TestParseCSV:
    def test_basic_csv(self, sample_csv_bytes: bytes) -> None:
        df = parse_csv(sample_csv_bytes)
        assert list(df.columns) == ["name", "age", "score"]
        assert len(df) == 3

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            parse_csv("")


class TestParseJSON:
    def test_array_of_objects(self, sample_json_bytes: bytes) -> None:
        df = parse_json(sample_json_bytes)
        assert len(df) == 2
        assert "name" in df.columns

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            parse_json("")
