"""Tests for app.visualization.service – VisualizationService."""

import pandas as pd
import pytest

from app.visualization.charts import ChartType
from app.visualization.service import VisualizationService


@pytest.fixture()
def svc() -> VisualizationService:
    return VisualizationService()


class TestAutoVisualize:
    def test_generates_charts(self, svc: VisualizationService, sample_df: pd.DataFrame) -> None:
        charts = svc.auto_visualize(sample_df)
        assert len(charts) >= 1
        types = {c.chart_type for c in charts}
        assert ChartType.HISTOGRAM in types

    def test_numeric_only_df(self, svc: VisualizationService, numeric_df: pd.DataFrame) -> None:
        charts = svc.auto_visualize(numeric_df)
        types = {c.chart_type for c in charts}
        assert ChartType.SCATTER in types
        assert ChartType.HEATMAP in types


class TestCreateChart:
    def test_bar(self, svc: VisualizationService, sample_df: pd.DataFrame) -> None:
        spec = svc.create_chart(sample_df, ChartType.BAR, x_col="name", y_col="age")
        assert spec.chart_type == ChartType.BAR

    def test_line(self, svc: VisualizationService, sample_df: pd.DataFrame) -> None:
        spec = svc.create_chart(sample_df, ChartType.LINE, x_col="age", y_col="score")
        assert spec.chart_type == ChartType.LINE

    def test_scatter(self, svc: VisualizationService, sample_df: pd.DataFrame) -> None:
        spec = svc.create_chart(sample_df, ChartType.SCATTER, x_col="age", y_col="score")
        assert spec.chart_type == ChartType.SCATTER

    def test_histogram(self, svc: VisualizationService, sample_df: pd.DataFrame) -> None:
        spec = svc.create_chart(sample_df, ChartType.HISTOGRAM, x_col="age", bins=15)
        assert spec.chart_type == ChartType.HISTOGRAM

    def test_pie(self, svc: VisualizationService, sample_df: pd.DataFrame) -> None:
        spec = svc.create_chart(sample_df, ChartType.PIE, x_col="name", y_col="score")
        assert spec.chart_type == ChartType.PIE

    def test_unsupported_raises(self, svc: VisualizationService, sample_df: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="not supported"):
            svc.create_chart(sample_df, ChartType.HEATMAP, x_col="age", y_col="score")
