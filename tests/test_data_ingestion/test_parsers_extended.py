"""Extended parser tests – cover JSON edge cases, Excel parser, and headerless CSV."""

import pandas as pd
import pytest

from app.data_ingestion.parsers import parse_csv, parse_excel, parse_json


class TestParseCSVExtended:
    def test_bytes_input(self) -> None:
        df = parse_csv(b"a,b\n1,2\n3,4")
        assert len(df) == 2

    def test_no_header(self) -> None:
        df = parse_csv("1,2,3\n4,5,6")
        assert len(df) == 2
        assert len(df.columns) == 3

    def test_custom_delimiter(self) -> None:
        df = parse_csv("a;b\n1;2", delimiter=";")
        assert list(df.columns) == ["a", "b"]


class TestParseJSONExtended:
    def test_single_object(self) -> None:
        df = parse_json('{"name": "Alice", "age": 30}')
        assert len(df) == 1
        assert "name" in df.columns

    def test_empty_array_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            parse_json("[]")

    def test_invalid_json_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid JSON"):
            parse_json("{bad json}")

    def test_unsupported_root_type(self) -> None:
        with pytest.raises(ValueError, match="Unsupported JSON root type"):
            parse_json('"just a string"')

    def test_bytes_input(self) -> None:
        df = parse_json(b'[{"x": 1}]')
        assert len(df) == 1


class TestParseExcel:
    def test_empty_content_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            parse_excel(b"")

    def test_invalid_content_raises(self) -> None:
        with pytest.raises(ValueError, match="Failed to parse"):
            parse_excel(b"this is not excel data")

    def test_valid_excel(self, tmp_path: pytest.TempPathFactory) -> None:
        path = tmp_path / "test.xlsx"  # type: ignore[operator]
        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        df.to_excel(str(path), index=False)
        result = parse_excel(path.read_bytes())  # type: ignore[union-attr]
        assert len(result) == 2
        assert list(result.columns) == ["col1", "col2"]
