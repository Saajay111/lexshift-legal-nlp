import pandas as pd

from lexshift.schema import validate_annotation_frame


def valid_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "contract_id": ["C001"],
            "source_domain": ["SEC"],
            "clause_category": ["governing_law"],
            "presence": [True],
            "passage_id": ["P001"],
            "annotator_id": ["A1"],
        }
    )


def test_valid_annotation_frame_has_no_errors() -> None:
    assert validate_annotation_frame(valid_frame()) == []


def test_missing_required_column_is_reported() -> None:
    frame = valid_frame().drop(columns=["annotator_id"])
    errors = validate_annotation_frame(frame)
    assert any("annotator_id" in error for error in errors)


def test_absence_label_does_not_require_passage_id() -> None:
    frame = valid_frame()
    frame.loc[0, "presence"] = False
    frame.loc[0, "passage_id"] = None
    assert validate_annotation_frame(frame) == []


def test_positive_label_requires_passage_id() -> None:
    frame = valid_frame()
    frame.loc[0, "passage_id"] = None
    errors = validate_annotation_frame(frame)
    assert any("Positive annotations must include a passage_id" in error for error in errors)


def test_negative_label_cannot_have_passage_id() -> None:
    frame = valid_frame()
    frame.loc[0, "presence"] = False
    errors = validate_annotation_frame(frame)
    assert any("Negative annotations must not include a passage_id" in error for error in errors)


def test_unexpected_category_is_reported() -> None:
    frame = valid_frame()
    frame.loc[0, "clause_category"] = "made_up_category"
    errors = validate_annotation_frame(frame)
    assert any("Unexpected clause categories" in error for error in errors)


def test_invalid_character_span_is_reported() -> None:
    frame = valid_frame()
    frame["start_char"] = [10]
    frame["end_char"] = [5]
    errors = validate_annotation_frame(frame)
    assert any("Character spans" in error for error in errors)
