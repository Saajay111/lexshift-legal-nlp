"""Prepare CUAD contract-level labels and leakage-safe split manifests.

This module deliberately does not create passage-level negative examples:
the CUAD master-clauses export supplies absence labels at contract/category
level, not text passages known to be negative.
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

import pandas as pd

from lexshift.schema import require_valid_annotations
from lexshift.splits import assert_contract_level_splits

CATEGORY_ORDER = [
    "governing_law",
    "non_compete",
    "anti_assignment",
    "termination_for_convenience",
    "cap_on_liability",
]


def build_contract_labels(annotations: pd.DataFrame) -> pd.DataFrame:
    """Aggregate passage rows into exactly one binary label per contract/category."""
    require_valid_annotations(annotations)
    missing = {"passage_text", "source_answer"} - set(annotations.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    rows: list[dict[str, Any]] = []
    for (contract_id, category), group in annotations.groupby(
        ["contract_id", "clause_category"], sort=True
    ):
        if category not in CATEGORY_ORDER:
            raise ValueError(f"Unexpected category: {category}")
        positive = group["presence"].astype(bool)
        if positive.any() and (~positive).any():
            raise ValueError(
                f"Mixed positive and negative rows for {contract_id}/{category}"
            )
        answers = group["source_answer"].dropna().astype(str).unique()
        if len(answers) > 1:
            raise ValueError(
                f"Inconsistent source_answer for {contract_id}/{category}: {answers.tolist()}"
            )
        rows.append({
            "contract_id": contract_id,
            "clause_category": category,
            "presence": bool(positive.any()),
            "source_answer": answers[0] if len(answers) else None,
            "positive_passage_count": int(positive.sum()),
        })

    long = pd.DataFrame(rows)
    expected = annotations["contract_id"].nunique() * len(CATEGORY_ORDER)
    if len(long) != expected:
        raise ValueError(
            f"Expected {expected} contract/category labels, found {len(long)}. "
            "Check that every contract has all five categories."
        )

    labels = long.pivot(
        index="contract_id", columns="clause_category", values="presence"
    ).reset_index()
    labels.columns.name = None
    for category in CATEGORY_ORDER:
        if category not in labels:
            raise ValueError(f"Missing category after aggregation: {category}")
    counts = long.groupby("contract_id")["clause_category"].nunique()
    if not counts.eq(len(CATEGORY_ORDER)).all():
        raise ValueError("Every contract must have exactly one label per category.")
    return labels[["contract_id", *CATEGORY_ORDER]].sort_values(
        "contract_id"
    ).reset_index(drop=True)


def make_contract_splits(
    labels: pd.DataFrame,
    *,
    seed: int = 42,
    train_fraction: float = 0.70,
    validation_fraction: float = 0.15,
) -> pd.DataFrame:
    """Assign contracts, not passages, to train/validation/test using a seeded shuffle."""
    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be between 0 and 1.")
    if not 0 < validation_fraction < 1:
        raise ValueError("validation_fraction must be between 0 and 1.")
    if train_fraction + validation_fraction >= 1:
        raise ValueError("Train plus validation fractions must be below 1.")
    if labels["contract_id"].duplicated().any():
        raise ValueError("Contract label table must contain one row per contract.")

    ids = labels["contract_id"].astype(str).tolist()
    random.Random(seed).shuffle(ids)
    n = len(ids)
    train_end = int(n * train_fraction)
    validation_end = train_end + int(n * validation_fraction)
    assignment = {
        contract_id: (
            "train" if index < train_end
            else "validation" if index < validation_end
            else "test"
        )
        for index, contract_id in enumerate(ids)
    }
    splits = pd.DataFrame({
        "contract_id": labels["contract_id"].astype(str),
        "split": labels["contract_id"].astype(str).map(assignment),
    })
    assert_contract_level_splits(splits)
    return splits.sort_values(["split", "contract_id"]).reset_index(drop=True)


def build_preparation_report(
    labels: pd.DataFrame, splits: pd.DataFrame
) -> dict[str, Any]:
    """Summarize class support by split without claiming model performance."""
    merged = labels.merge(splits, on="contract_id", validate="one_to_one")
    report: dict[str, Any] = {
        "contracts": int(len(labels)),
        "split_contracts": {
            key: int(value)
            for key, value in splits["split"].value_counts().sort_index().items()
        },
        "categories": {},
        "warning": (
            "These are contract-level labels. They are not passage-level training "
            "examples; negative text passages must be sampled from full contract "
            "text and independently checked before passage classification."
        ),
    }
    for category in CATEGORY_ORDER:
        report["categories"][category] = {}
        for split_name, group in merged.groupby("split", sort=True):
            positives = int(group[category].sum())
            report["categories"][category][split_name] = {
                "contracts": int(len(group)),
                "positive_contracts": positives,
                "negative_contracts": int(len(group) - positives),
                "positive_rate": round(positives / len(group), 4) if len(group) else None,
            }
    return report


def prepare_cuad(
    input_csv: str | Path,
    output_dir: str | Path,
    *,
    seed: int = 42,
) -> dict[str, Any]:
    """Create contract labels, split manifest, and a machine-readable audit report."""
    input_path = Path(input_csv)
    if not input_path.is_file():
        raise FileNotFoundError(f"Annotation CSV not found: {input_path}")
    annotations = pd.read_csv(input_path)
    labels = build_contract_labels(annotations)
    splits = make_contract_splits(labels, seed=seed)
    report = build_preparation_report(labels, splits)

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    labels.to_csv(destination / "cuad_contract_labels.csv", index=False)
    splits.to_csv(destination / "cuad_contract_splits.csv", index=False)
    (destination / "cuad_preparation_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    report["output_dir"] = str(destination)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare contract-level CUAD labels and leakage-safe splits."
    )
    parser.add_argument("input_csv")
    parser.add_argument("output_dir")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    print(json.dumps(prepare_cuad(args.input_csv, args.output_dir, seed=args.seed), indent=2))


if __name__ == "__main__":
    main()
