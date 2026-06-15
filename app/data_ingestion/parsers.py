"""File parsers for supported data formats."""

from __future__ import annotations

import csv
import io
import json
from typing import Any

import pandas as pd


def parse_csv(raw: str | bytes, delimiter: str = ",") -> pd.DataFrame:
    """Parse CSV content into a DataFrame.

    Raises ``ValueError`` when the content is empty or unparseable.
    """
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    raw = raw.strip()
    if not raw:
        raise ValueError("CSV content is empty")
    try:
        sniffer = csv.Sniffer()
        if sniffer.has_header(raw[:2048]):
            return pd.read_csv(io.StringIO(raw), delimiter=delimiter)
        return pd.read_csv(io.StringIO(raw), delimiter=delimiter, header=None)
    except Exception as exc:
        raise ValueError(f"Failed to parse CSV: {exc}") from exc


def parse_json(raw: str | bytes) -> pd.DataFrame:
    """Parse JSON content into a DataFrame.

    Accepts JSON arrays of objects or a single object (→ one-row frame).
    Raises ``ValueError`` on bad JSON or unsupported structure.
    """
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    raw = raw.strip()
    if not raw:
        raise ValueError("JSON content is empty")
    try:
        data: Any = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc

    if isinstance(data, list):
        if not data:
            raise ValueError("JSON array is empty")
        return pd.DataFrame(data)
    if isinstance(data, dict):
        return pd.DataFrame([data])
    raise ValueError(f"Unsupported JSON root type: {type(data).__name__}")


def parse_excel(raw: bytes) -> pd.DataFrame:
    """Parse Excel (.xlsx / .xls) bytes into a DataFrame.

    Raises ``ValueError`` on failure.
    """
    if not raw:
        raise ValueError("Excel content is empty")
    try:
        return pd.read_excel(io.BytesIO(raw), engine="openpyxl")
    except Exception as exc:
        raise ValueError(f"Failed to parse Excel file: {exc}") from exc
