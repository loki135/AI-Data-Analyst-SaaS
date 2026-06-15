"""Shared fixtures for the test suite."""

from __future__ import annotations

import pandas as pd
import pytest


@pytest.fixture()
def sample_csv_bytes() -> bytes:
    return b"name,age,score\nAlice,30,85.5\nBob,25,92.0\nCharlie,35,78.3\n"


@pytest.fixture()
def sample_json_bytes() -> bytes:
    return b'[{"name":"Alice","age":30,"score":85.5},{"name":"Bob","age":25,"score":92.0}]'


@pytest.fixture()
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
            "age": [30, 25, 35, 28, 32],
            "score": [85.5, 92.0, 78.3, 88.1, 95.0],
            "grade": ["A", "A+", "B+", "A", "A+"],
        }
    )


@pytest.fixture()
def numeric_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "y": [2.1, 4.0, 5.9, 8.1, 10.0, 12.1, 13.9, 16.0, 18.1, 20.0],
            "z": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        }
    )
