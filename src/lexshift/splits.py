"""Contract-level split integrity checks."""

from __future__ import annotations

import pandas as pd


def find_contract_split_leakage(
    frame: pd.DataFrame,
    *,
    contract_column: str = "contract_id",
    split_column: str = "split",
) -> dict[str, list[str]]:
    """Return contract IDs assigned to more than one split."""
    required = {contract_column, split_column}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    counts = frame.groupby(contract_column, dropna=False)[split_column].nunique()
    leaking_ids = counts[counts > 1].index
    leakage: dict[str, list[str]] = {}
    for contract_id in leaking_ids:
        splits = (
            frame.loc[frame[contract_column] == contract_id, split_column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
        leakage[str(contract_id)] = sorted(splits)
    return leakage


def assert_contract_level_splits(frame: pd.DataFrame) -> None:
    """Raise ValueError if any contract occurs in multiple splits."""
    leakage = find_contract_split_leakage(frame)
    if leakage:
        examples = list(leakage.items())[:5]
        raise ValueError(f"Contract leakage detected (sample): {examples}")
