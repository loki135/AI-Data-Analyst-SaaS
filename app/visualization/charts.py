"""Chart-specification builders.

This module produces *chart specs* — serialisable dicts that describe a chart
without coupling to a specific rendering backend.  A frontend (or a server-side
renderer) can consume these specs to produce actual images/SVGs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import pandas as pd


class ChartType(Enum):
    BAR = "bar"
    LINE = "line"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"
    PIE = "pie"
    HEATMAP = "heatmap"
    BOX = "box"


@dataclass
class ChartSpec:
    """Backend-agnostic chart specification."""

    chart_type: ChartType
    title: str
    x_label: str
    y_label: str
    data: dict[str, Any]
    options: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "chart_type": self.chart_type.value,
            "title": self.title,
            "x_label": self.x_label,
            "y_label": self.y_label,
            "data": self.data,
            "options": self.options,
        }


def build_bar_chart(
    df: pd.DataFrame, x_col: str, y_col: str, title: str = ""
) -> ChartSpec:
    """Build a bar-chart spec from two columns."""
    _assert_column_exists(df, x_col)
    _assert_column_exists(df, y_col)
    return ChartSpec(
        chart_type=ChartType.BAR,
        title=title or f"{y_col} by {x_col}",
        x_label=x_col,
        y_label=y_col,
        data={"x": df[x_col].tolist(), "y": df[y_col].tolist()},
    )


def build_line_chart(
    df: pd.DataFrame, x_col: str, y_col: str, title: str = ""
) -> ChartSpec:
    """Build a line-chart spec."""
    _assert_column_exists(df, x_col)
    _assert_column_exists(df, y_col)
    return ChartSpec(
        chart_type=ChartType.LINE,
        title=title or f"{y_col} over {x_col}",
        x_label=x_col,
        y_label=y_col,
        data={"x": df[x_col].tolist(), "y": df[y_col].tolist()},
    )


def build_scatter_chart(
    df: pd.DataFrame, x_col: str, y_col: str, title: str = ""
) -> ChartSpec:
    """Build a scatter-plot spec."""
    _assert_column_exists(df, x_col)
    _assert_column_exists(df, y_col)
    return ChartSpec(
        chart_type=ChartType.SCATTER,
        title=title or f"{y_col} vs {x_col}",
        x_label=x_col,
        y_label=y_col,
        data={"x": df[x_col].tolist(), "y": df[y_col].tolist()},
    )


def build_histogram(
    df: pd.DataFrame, col: str, bins: int = 20, title: str = ""
) -> ChartSpec:
    """Build a histogram spec."""
    _assert_column_exists(df, col)
    return ChartSpec(
        chart_type=ChartType.HISTOGRAM,
        title=title or f"Distribution of {col}",
        x_label=col,
        y_label="Frequency",
        data={"values": df[col].dropna().tolist()},
        options={"bins": bins},
    )


def build_pie_chart(
    df: pd.DataFrame, label_col: str, value_col: str, title: str = ""
) -> ChartSpec:
    """Build a pie-chart spec."""
    _assert_column_exists(df, label_col)
    _assert_column_exists(df, value_col)
    return ChartSpec(
        chart_type=ChartType.PIE,
        title=title or f"{value_col} distribution",
        x_label=label_col,
        y_label=value_col,
        data={"labels": df[label_col].tolist(), "values": df[value_col].tolist()},
    )


def build_correlation_heatmap(corr_matrix: pd.DataFrame, title: str = "") -> ChartSpec:
    """Build a heatmap spec from a correlation matrix."""
    return ChartSpec(
        chart_type=ChartType.HEATMAP,
        title=title or "Correlation Heatmap",
        x_label="",
        y_label="",
        data={
            "columns": corr_matrix.columns.tolist(),
            "values": corr_matrix.values.tolist(),
        },
    )


def suggest_chart_types(df: pd.DataFrame) -> list[ChartType]:
    """Heuristically suggest suitable chart types for *df*."""
    suggestions: list[ChartType] = []
    num_cols = df.select_dtypes(include="number").columns
    cat_cols = df.select_dtypes(include=["object", "category"]).columns

    if len(num_cols) >= 1:
        suggestions.append(ChartType.HISTOGRAM)
        suggestions.append(ChartType.BOX)
    if len(num_cols) >= 2:
        suggestions.append(ChartType.SCATTER)
        suggestions.append(ChartType.LINE)
        suggestions.append(ChartType.HEATMAP)
    if len(cat_cols) >= 1 and len(num_cols) >= 1:
        suggestions.append(ChartType.BAR)
        suggestions.append(ChartType.PIE)

    return suggestions


def _assert_column_exists(df: pd.DataFrame, col: str) -> None:
    if col not in df.columns:
        raise KeyError(f"Column '{col}' not found in DataFrame")
