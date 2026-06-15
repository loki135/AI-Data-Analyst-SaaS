"""Correlation-analysis helpers."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class CorrelationResult:
    """Pairwise correlation between two columns."""

    col_a: str
    col_b: str
    pearson: float
    spearman: float


def compute_correlation_matrix(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    """Return the correlation matrix for all numeric columns.

    *method* can be ``'pearson'``, ``'spearman'``, or ``'kendall'``.
    Raises ``ValueError`` on unknown method or when no numeric columns exist.
    """
    valid_methods = {"pearson", "spearman", "kendall"}
    if method not in valid_methods:
        raise ValueError(f"Unknown method {method!r}; choose from {valid_methods}")
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        raise ValueError("No numeric columns available for correlation")
    return numeric.corr(method=method)


def find_top_correlations(
    df: pd.DataFrame, n: int = 10, threshold: float = 0.0
) -> list[CorrelationResult]:
    """Return the *n* strongest absolute correlations above *threshold*.

    Self-correlations (col vs itself) are excluded.
    """
    pearson = compute_correlation_matrix(df, method="pearson")
    spearman = compute_correlation_matrix(df, method="spearman")

    pairs: list[CorrelationResult] = []
    cols = pearson.columns.tolist()
    seen: set[tuple[str, str]] = set()

    for i, ca in enumerate(cols):
        for j, cb in enumerate(cols):
            if i >= j:
                continue
            key = (ca, cb)
            if key in seen:
                continue
            seen.add(key)
            p_val = float(pearson.loc[ca, cb])
            s_val = float(spearman.loc[ca, cb])
            if abs(p_val) >= threshold:
                pairs.append(CorrelationResult(col_a=ca, col_b=cb, pearson=p_val, spearman=s_val))

    pairs.sort(key=lambda r: abs(r.pearson), reverse=True)
    return pairs[:n]
