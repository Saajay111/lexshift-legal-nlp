import pandas as pd

from lexshift.cuad_audit import audit_cuad_frame


def test_audit_finds_expected_category_columns() -> None:
    frame = pd.DataFrame(
        {
            "Contract Name": ["A", "B"],
            "Governing Law - Context": ["text", "text"],
            "Governing Law - Answer": ["yes", "no"],
            "Cap on Liability - Context": ["text", "text"],
        }
    )
    result = audit_cuad_frame(frame)
    assert result["row_count"] == 2
    assert result["category_columns"]["Governing Law"]
    assert result["category_columns"]["Cap on Liability"]
    assert "Non-Compete" in result["missing_expected_categories"]


def test_audit_preserves_source_column_names() -> None:
    frame = pd.DataFrame({"Contract": ["A"], "Termination for Convenience (Context)": ["x"]})
    result = audit_cuad_frame(frame)
    assert result["category_columns"]["Termination for Convenience"] == [
        "Termination for Convenience (Context)"
    ]


def test_audit_handles_empty_frame() -> None:
    result = audit_cuad_frame(pd.DataFrame())
    assert result["row_count"] == 0
    assert result["first_column"] is None
