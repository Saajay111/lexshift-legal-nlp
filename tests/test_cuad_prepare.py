import pandas as pd
import pytest

from lexshift.cuad_prepare import (
    build_contract_labels,
    build_preparation_report,
    make_contract_splits,
)


def _annotations():
    rows = []
    categories = [
        "governing_law", "non_compete", "anti_assignment",
        "termination_for_convenience", "cap_on_liability",
    ]
    for index in range(20):
        for category_index, category in enumerate(categories):
            positive = (index + category_index) % 3 != 0
            rows.append({
                "contract_id": f"C{index:02d}",
                "source_domain": "cuad",
                "clause_category": category,
                "presence": positive,
                "passage_id": f"{category}:{index}" if positive else None,
                "passage_text": "evidence passage" if positive else None,
                "annotator_id": "cuad_v1",
                "source_answer": "Yes" if positive else "No",
            })
    return pd.DataFrame(rows)


def test_build_contract_labels_aggregates_passage_rows():
    annotations = _annotations()
    labels = build_contract_labels(annotations)
    assert len(labels) == 20
    assert labels.contract_id.nunique() == 20
    assert len(labels.columns) == 6
    assert labels["governing_law"].dtype == bool


def test_split_manifest_is_deterministic_and_contract_level():
    labels = build_contract_labels(_annotations())
    first = make_contract_splits(labels, seed=17)
    second = make_contract_splits(labels, seed=17)
    pd.testing.assert_frame_equal(first, second)
    assert first.contract_id.nunique() == 20
    assert first.groupby("contract_id").split.nunique().max() == 1
    assert first.split.value_counts().to_dict() == {
        "train": 14, "validation": 3, "test": 3
    }


def test_report_contains_category_support():
    labels = build_contract_labels(_annotations())
    splits = make_contract_splits(labels)
    report = build_preparation_report(labels, splits)
    assert report["contracts"] == 20
    assert "non_compete" in report["categories"]
    assert "negative text passages" in report["warning"]


def test_mixed_positive_and_negative_rows_for_same_contract_category_fail():
    annotations = _annotations()
    duplicate = annotations.iloc[[0]].copy()
    duplicate["presence"] = not bool(duplicate.iloc[0]["presence"])
    duplicate["passage_id"] = None
    duplicate["passage_text"] = None
    duplicate["source_answer"] = "No"
    annotations = pd.concat([annotations, duplicate], ignore_index=True)
    with pytest.raises(ValueError, match="Mixed positive and negative"):
        build_contract_labels(annotations)


def test_missing_contract_category_pair_fails():
    annotations = _annotations().iloc[1:].copy()
    with pytest.raises(ValueError, match="Expected"):
        build_contract_labels(annotations)
