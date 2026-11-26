"""Validation helpers for LEXSHIFT annotation and prediction tables."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

REQUIRED_ANNOTATION_COLUMNS = {
    "contract_id",
    "source_domain",
    "clause_category",
    "presence",
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
    """Return structural annotation errors without mutating the input.

    Absence labels do not require a passage ID. Positive labels must identify
    at least one evidence passage. Each distinct passage is stored as a row.
    """
    errors: list[str] = []
    missing = sorted(REQUIRED_ANNOTATION_COLUMNS - set(frame.columns))
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
        return errors

    if frame.empty:
        errors.append("Annotation table is empty.")
        return errors

    for column in ("contract_id", "source_domain", "clause_category", "annotator_id"):
        if frame[column].isna().any():
            errors.append(f"Column '{column}' contains missing values.")

    categories = set(frame["clause_category"].dropna().astype(str))
    unexpected = sorted(categories - set(allowed_categories))
    if unexpected:
        errors.append(f"Unexpected clause categories: {', '.join(unexpected)}")

    if frame["presence"].isna().any():
        errors.append("Column 'presence' contains missing values.")
    elif not frame["presence"].isin([True, False, 0, 1]).all():
        errors.append("Column 'presence' must contain boolean values.")

    if "passage_id" in frame.columns:
        positive_without_passage = frame["presence"].astype(bool) & frame["passage_id"].isna()
        if positive_without_passage.any():
            errors.append("Positive annotations must include a passage_id.")

        negative_with_passage = (~frame["presence"].astype(bool)) & frame["passage_id"].notna()
        if negative_with_passage.any():
            errors.append("Negative annotations must not include a passage_id.")

    if {"start_char", "end_char"}.issubset(frame.columns):
        spans = frame[["start_char", "end_char"]].dropna()
        invalid = spans[
            (spans["start_char"] < 0) | (spans["end_char"] <= spans["start_char"])
        ]
        if not invalid.empty:
            errors.append("Character spans must satisfy 0 <= start_char < end_char.")

        if "presence" in frame.columns:
            missing_positive_spans = (
                frame["presence"].astype(bool)
                & (frame["start_char"].isna() | frame["end_char"].isna())
            )
            if missing_positive_spans.any():
                errors.append("Positive annotations with span columns need both offsets.")

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
