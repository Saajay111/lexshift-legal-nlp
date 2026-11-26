"""Schema audit helpers for the CUAD v1 master-clauses CSV."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd

EXPECTED_CATEGORIES = (
    "Governing Law",
    "Non-Compete",
    "Anti-Assignment",
    "Termination for Convenience",
    "Cap on Liability",
)


def _normalise(value: str) -> str:
    """Normalize labels for robust matching without changing source labels."""
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def audit_cuad_frame(frame: pd.DataFrame) -> dict[str, Any]:
    """Summarize the supplied CUAD master CSV frame without mutating it.

    This is a discovery audit, not a semantic validation of annotation content.
    It reports which expected category names occur in source column names and
    preserves the exact source column strings for manual inspection.
    """
    normalized_columns = {
        column: _normalise(str(column)) for column in frame.columns
    }
    category_columns: dict[str, list[str]] = {}
    missing_categories: list[str] = []

    for category in EXPECTED_CATEGORIES:
        needle = _normalise(category)
        matches = [
            str(column)
            for column, normalized in normalized_columns.items()
            if needle in normalized
        ]
        category_columns[category] = matches
        if not matches:
            missing_categories.append(category)

    first_column = str(frame.columns[0]) if len(frame.columns) else None
    unique_first_column_values = (
        int(frame[first_column].nunique(dropna=True))
        if first_column is not None
        else 0
    )

    return {
        "row_count": int(len(frame)),
        "column_count": int(len(frame.columns)),
        "columns": [str(column) for column in frame.columns],
        "first_column": first_column,
        "unique_first_column_values": unique_first_column_values,
        "category_columns": category_columns,
        "missing_expected_categories": missing_categories,
    }


def audit_cuad_csv(path: str | Path) -> dict[str, Any]:
    """Read a CUAD master-clauses CSV and return a schema audit."""
    csv_path = Path(path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"CUAD CSV not found: {csv_path}")
    frame = pd.read_csv(csv_path)
    return audit_cuad_frame(frame)
