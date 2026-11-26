import pandas as pd
import pytest

from lexshift.cuad_convert import convert_cuad_frame, parse_passages


def _row(filename="contract.pdf"):
    row = {"Filename": filename}
    for category in (
        "Governing Law", "Non-Compete", "Anti-Assignment",
        "Termination For Convenience", "Cap On Liability",
    ):
        row[category] = "[]"
        row[f"{category}-Answer"] = "No"
    row["Governing Law"] = "['Governed by New York law.']"
    row["Governing Law-Answer"] = "New York"
    row["Anti-Assignment"] = "['No assignment without consent.', 'A permitted transfer is allowed.']"
    row["Anti-Assignment-Answer"] = "Yes"
    return row


def test_parse_passages_handles_json_and_python_list():
    assert parse_passages('["one", "two"]') == ["one", "two"]
    assert parse_passages("['one', 'two']") == ["one", "two"]
    assert parse_passages("[]") == []


def test_converter_preserves_positive_passages_and_negative_labels():
    converted = convert_cuad_frame(pd.DataFrame([_row()]))
    anti = converted[converted["clause_category"] == "anti_assignment"]
    assert len(anti) == 2
    assert anti["presence"].all()
    assert anti["passage_text"].tolist() == [
        "No assignment without consent.", "A permitted transfer is allowed."
    ]
    negative = converted[converted["clause_category"] == "non_compete"].iloc[0]
    assert not negative["presence"]
    assert pd.isna(negative["passage_id"])
    assert pd.isna(negative["passage_text"])


def test_governing_law_answer_is_preserved_verbatim():
    converted = convert_cuad_frame(pd.DataFrame([_row()]))
    governing = converted[converted["clause_category"] == "governing_law"].iloc[0]
    assert governing["presence"]
    assert governing["source_answer"] == "New York"


def test_missing_governing_law_answer_does_not_erase_evidence():
    row = _row()
    row["Governing Law-Answer"] = None
    converted = convert_cuad_frame(pd.DataFrame([row]))
    governing = converted[converted["clause_category"] == "governing_law"].iloc[0]
    assert governing["presence"]
    assert pd.isna(governing["source_answer"])


def test_converter_rejects_yes_no_evidence_mismatch():
    row = _row()
    row["Non-Compete-Answer"] = "Yes"
    with pytest.raises(ValueError, match="disagrees with evidence"):
        convert_cuad_frame(pd.DataFrame([row]))


def test_converter_rejects_duplicate_filenames():
    with pytest.raises(ValueError, match="must be unique"):
        convert_cuad_frame(pd.DataFrame([_row(), _row()]))
