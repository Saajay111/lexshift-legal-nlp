"""Validation helpers for LEXSHIFT annotation and prediction tables."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

REQUIRED_ANNOTATION_COLUMNS = {
    "contract_id",
    "source_domain",
    "clause_category",
    "presence",
    "passage_id",
    "annotator_id",
}
ALLOWED_CATEGORIES = {
    "governing_law",
    "non_compete",
    "anti_assignment",
    "termination_for_convenience",
    "cap_on_liability",
}


def validate_annotation_frame(
    frame: pd.DataFrame,
    *,
    allowed_categories: Iterable[str] = ALLOWED_CATEGORIES,
) -> list[str]:
    """Return validation errors without mutating the input frame.

    The function intentionally checks structural integrity only. It does not
    decide whether a legal annotation is substantively correct.
    """
    errors: list[str] = []
    missing = sorted(REQUIRED_ANNOTATION_COLUMNS - set(frame.columns))
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
        return errors

    if frame.empty:
        errors.append("Annotation table is empty.")

    for column in ("contract_id", "source_domain", "clause_category", "passage_id"):
        if frame[column].isna().any():
            errors.append(f"Column '{column}' contains missing values.")

    categories = set(frame["clause_category"].dropna().astype(str))
    unexpected = sorted(categories - set(allowed_categories))
    if unexpected:
        errors.append(f"Unexpected clause categories: {', '.join(unexpected)}")

    if not frame.empty and frame["presence"].isna().any():
        errors.append("Column 'presence' contains missing values.")

    if {"start_char", "end_char"}.issubset(frame.columns):
        spans = frame[["start_char", "end_char"]].dropna()
        invalid = spans[
            (spans["start_char"] < 0) | (spans["end_char"] <= spans["start_char"])
        ]
        if not invalid.empty:
            errors.append("Character spans must satisfy 0 <= start_char < end_char.")

    duplicate_keys = ["contract_id", "clause_category", "passage_id", "annotator_id"]
    if set(duplicate_keys).issubset(frame.columns):
        if frame.duplicated(duplicate_keys).any():
            errors.append("Duplicate annotation keys detected.")

    return errors


def require_valid_annotations(frame: pd.DataFrame) -> None:
    """Raise ValueError when the annotation frame fails structural validation."""
    errors = validate_annotation_frame(frame)
    if errors:
        raise ValueError("Invalid annotation data:\n- " + "\n- ".join(errors))
