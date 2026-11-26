import pandas as pd

from lexshift.schema import validate_annotation_frame


def valid_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "contract_id": ["C001"],
            "source_domain": ["SEC"],
            "clause_category": ["termination"],
            "presence": [True],
            "passage_id": ["P001"],
            "annotator_id": ["A1"],
        }
    )


def test_valid_annotation_frame_has_no_errors() -> None:
    assert validate_annotation_frame(valid_frame()) == []


def test_missing_required_column_is_reported() -> None:
    frame = valid_frame().drop(columns=["passage_id"])
    errors = validate_annotation_frame(frame)
    assert any("passage_id" in error for error in errors)


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
