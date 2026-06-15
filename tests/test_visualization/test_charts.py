"""Tests for app.visualization.charts."""

import pandas as pd
import pytest

from app.visualization.charts import (
    ChartType,
    build_bar_chart,
    build_correlation_heatmap,
    build_histogram,
    build_line_chart,
    build_pie_chart,
    build_scatter_chart,
    suggest_chart_types,
)


@pytest.fixture()
def df() -> pd.DataFrame:
    return pd.DataFrame(
        {"cat": ["A", "B", "C"], "x": [10, 20, 30], "y": [1.1, 2.2, 3.3]}
    )


class TestBuildBarChart:
    def test_basic(self, df: pd.DataFrame) -> None:
        spec = build_bar_chart(df, "cat", "x")
        assert spec.chart_type == ChartType.BAR
        assert spec.data["x"] == ["A", "B", "C"]
        assert spec.data["y"] == [10, 20, 30]

    def test_custom_title(self, df: pd.DataFrame) -> None:
        spec = build_bar_chart(df, "cat", "x", title="My Chart")
        assert spec.title == "My Chart"

    def test_missing_column_raises(self, df: pd.DataFrame) -> None:
        with pytest.raises(KeyError, match="not found"):
            build_bar_chart(df, "cat", "nonexistent")


class TestBuildLineChart:
    def test_basic(self, df: pd.DataFrame) -> None:
        spec = build_line_chart(df, "x", "y")
        assert spec.chart_type == ChartType.LINE
        assert len(spec.data["x"]) == 3


class TestBuildScatterChart:
    def test_basic(self, df: pd.DataFrame) -> None:
        spec = build_scatter_chart(df, "x", "y")
        assert spec.chart_type == ChartType.SCATTER

    def test_missing_column(self, df: pd.DataFrame) -> None:
        with pytest.raises(KeyError):
            build_scatter_chart(df, "x", "missing")


class TestBuildHistogram:
    def test_basic(self, df: pd.DataFrame) -> None:
        spec = build_histogram(df, "x", bins=10)
        assert spec.chart_type == ChartType.HISTOGRAM
        assert spec.options["bins"] == 10
        assert len(spec.data["values"]) == 3

    def test_missing_column(self, df: pd.DataFrame) -> None:
        with pytest.raises(KeyError):
            build_histogram(df, "nonexistent")


class TestBuildPieChart:
    def test_basic(self, df: pd.DataFrame) -> None:
        spec = build_pie_chart(df, "cat", "x")
        assert spec.chart_type == ChartType.PIE
        assert spec.data["labels"] == ["A", "B", "C"]


class TestBuildCorrelationHeatmap:
    def test_basic(self, df: pd.DataFrame) -> None:
        corr = df[["x", "y"]].corr()
        spec = build_correlation_heatmap(corr)
        assert spec.chart_type == ChartType.HEATMAP
        assert spec.data["columns"] == ["x", "y"]


class TestChartSpecToDict:
    def test_serializes(self, df: pd.DataFrame) -> None:
        spec = build_bar_chart(df, "cat", "x")
        d = spec.to_dict()
        assert d["chart_type"] == "bar"
        assert "data" in d


class TestSuggestChartTypes:
    def test_numeric_only(self) -> None:
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        suggestions = suggest_chart_types(df)
        assert ChartType.HISTOGRAM in suggestions
        assert ChartType.SCATTER in suggestions

    def test_mixed(self, df: pd.DataFrame) -> None:
        suggestions = suggest_chart_types(df)
        assert ChartType.BAR in suggestions
        assert ChartType.PIE in suggestions

    def test_no_numeric(self) -> None:
        df = pd.DataFrame({"a": ["x", "y"]})
        suggestions = suggest_chart_types(df)
        assert ChartType.HISTOGRAM not in suggestions
