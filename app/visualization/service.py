"""Visualization service – orchestrates chart generation."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from app.analysis.correlations import compute_correlation_matrix
from app.visualization.charts import (
    ChartSpec,
    ChartType,
    build_bar_chart,
    build_correlation_heatmap,
    build_histogram,
    build_line_chart,
    build_pie_chart,
    build_scatter_chart,
    suggest_chart_types,
)


@dataclass
class VisualizationService:
    """Generate chart specs from DataFrames."""

    def auto_visualize(self, df: pd.DataFrame) -> list[ChartSpec]:
        """Automatically generate a set of charts for *df*."""
        charts: list[ChartSpec] = []
        suggestions = suggest_chart_types(df)
        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        if ChartType.HISTOGRAM in suggestions and num_cols:
            charts.append(build_histogram(df, num_cols[0]))

        if ChartType.SCATTER in suggestions and len(num_cols) >= 2:
            charts.append(build_scatter_chart(df, num_cols[0], num_cols[1]))

        if ChartType.BAR in suggestions and cat_cols and num_cols:
            charts.append(build_bar_chart(df, cat_cols[0], num_cols[0]))

        if ChartType.HEATMAP in suggestions and len(num_cols) >= 2:
            corr = compute_correlation_matrix(df)
            charts.append(build_correlation_heatmap(corr))

        return charts

    def create_chart(
        self,
        df: pd.DataFrame,
        chart_type: ChartType,
        x_col: str = "",
        y_col: str = "",
        title: str = "",
        **kwargs: object,
    ) -> ChartSpec:
        """Create a specific chart type."""
        builders = {
            ChartType.BAR: lambda: build_bar_chart(df, x_col, y_col, title),
            ChartType.LINE: lambda: build_line_chart(df, x_col, y_col, title),
            ChartType.SCATTER: lambda: build_scatter_chart(df, x_col, y_col, title),
            ChartType.HISTOGRAM: lambda: build_histogram(
                df, x_col, bins=int(kwargs.get("bins", 20)), title=title
            ),
            ChartType.PIE: lambda: build_pie_chart(df, x_col, y_col, title),
        }
        builder = builders.get(chart_type)
        if builder is None:
            raise ValueError(f"Chart type {chart_type.value!r} not supported via create_chart")
        return builder()
