import pandas as pd
import pytest

from lexshift.splits import assert_contract_level_splits, find_contract_split_leakage


def test_no_leakage_returns_empty_mapping() -> None:
    frame = pd.DataFrame(
        {"contract_id": ["C1", "C1", "C2"], "split": ["train", "train", "test"]}
    )
    assert find_contract_split_leakage(frame) == {}
    assert_contract_level_splits(frame)


def test_contract_in_multiple_splits_is_detected() -> None:
    frame = pd.DataFrame(
        {"contract_id": ["C1", "C1"], "split": ["train", "test"]}
    )
    assert find_contract_split_leakage(frame) == {"C1": ["test", "train"]}
    with pytest.raises(ValueError, match="Contract leakage detected"):
        assert_contract_level_splits(frame)


def test_missing_columns_raise_error() -> None:
    with pytest.raises(ValueError, match="Missing required columns"):
        find_contract_split_leakage(pd.DataFrame({"contract_id": ["C1"]}))
