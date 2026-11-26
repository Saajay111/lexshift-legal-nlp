from pathlib import Path

import pandas as pd

from lexshift import cuad_align
from lexshift.cuad_align import align_cuad_annotations, align_passage


def test_unique_match_recovers_offsets_across_whitespace():
    text = "Intro\n\nThis   Agreement\tshall be governed by law.\nEnd"
    passage = "This Agreement shall be governed by law."
    result = align_passage(text, passage)
    assert result["status"] == "unique_whitespace_normalized_match"
    assert text[result["start_char"]:result["end_char"]] == (
        "This   Agreement\tshall be governed by law."
    )


def test_unique_match_is_case_insensitive_and_preserves_source_offsets():
    text = "Intro\\nIN NO EVENT shall COMPANY be liable.\\nEnd"
    passage = "in no event SHALL company be liable."
    result = align_passage(text, passage)
    assert result["status"] == "unique_casefolded_whitespace_match"
    assert text[result["start_char"]:result["end_char"]] == (
        "IN NO EVENT shall COMPANY be liable."
    )


def test_casefold_expansion_maps_offsets_to_original_character():
    text = "Intro STRASSE clause. End"
    passage = "Straße clause."
    result = align_passage(text, passage)
    assert result["status"] == "unique_casefolded_whitespace_match"
    assert text[result["start_char"]:result["end_char"]] == "STRASSE clause."

def test_exact_unique_match_takes_priority_over_casefold_duplicates():
    text = "First clause. SECOND clause. second clause."
    passage = "SECOND clause."
    result = align_passage(text, passage)
    assert result["status"] == "unique_whitespace_normalized_match"
    assert text[result["start_char"]:result["end_char"]] == "SECOND clause."
    assert result["occurrences"] == 1


def test_casefold_fallback_recovers_capitalization_difference():
    text = "Intro\\nIN NO EVENT shall COMPANY be liable.\\nEnd"
    passage = "in no event SHALL company be liable."
    result = align_passage(text, passage)
    assert result["status"] == "unique_casefolded_whitespace_match"
    assert text[result["start_char"]:result["end_char"]] == (
        "IN NO EVENT shall COMPANY be liable."
    )
    assert result["occurrences"] == 1

def test_repeated_passage_is_flagged_ambiguous():
    result = align_passage("Clause A. Clause A.", "Clause A.")
    assert result["status"] == "ambiguous_multiple_matches"
    assert result["start_char"] is None


def test_unmatched_passage_is_not_fabricated():
    result = align_passage("Entirely different text.", "Missing clause.")
    assert result["status"] == "not_found"
    assert result["end_char"] is None


def test_negative_rows_are_not_passage_examples(tmp_path: Path):
    txt_dir = tmp_path / "txt"
    txt_dir.mkdir()
    (txt_dir / "ContractA.txt").write_text(
        "The agreement is governed by Delaware law.", encoding="utf-8"
    )
    annotations = pd.DataFrame([
        {
            "contract_id": "ContractA.pdf",
            "source_reference": "ContractA.pdf",
            "clause_category": "governing_law",
            "presence": True,
            "passage_id": "p1",
            "passage_text": "The agreement is governed by Delaware law.",
        },
        {
            "contract_id": "ContractA.pdf",
            "source_reference": "ContractA.pdf",
            "clause_category": "non_compete",
            "presence": False,
            "passage_id": None,
            "passage_text": None,
        },
    ])
    csv_path = tmp_path / "annotations.csv"
    annotations.to_csv(csv_path, index=False)
    report = align_cuad_annotations(csv_path, txt_dir, tmp_path / "out")
    aligned = pd.read_csv(tmp_path / "out" / "cuad_passage_alignment.csv")
    assert report["contracts_with_full_text"] == 1
    assert aligned.iloc[0]["alignment_status"] == "unique_whitespace_normalized_match"
    assert aligned.iloc[1]["alignment_status"] == (
        "not_applicable_contract_level_negative"
    )
    assert not (tmp_path / "out" / "raw_contract_text.txt").exists()


def test_alignment_ignores_flat_mirror_when_canonical_collection_is_complete(
    monkeypatch, tmp_path: Path
):
    text_root = tmp_path / "txt"
    mirror_dir = text_root / "Part_I"
    canonical_dir = text_root / "Part_III" / "Service"
    mirror_dir.mkdir(parents=True)
    canonical_dir.mkdir(parents=True)
    (mirror_dir / "ContractA.txt").write_text(
        "Incorrect mirror copy.", encoding="utf-8"
    )
    (canonical_dir / "ContractA.txt").write_text(
        "Canonical contract text contains the clause.", encoding="utf-8"
    )
    monkeypatch.setattr(cuad_align, "CANONICAL_CONTRACT_COUNT", 1)

    annotations = pd.DataFrame([{
        "contract_id": "ContractA.pdf",
        "source_reference": "ContractA.pdf",
        "clause_category": "governing_law",
        "presence": True,
        "passage_id": "p1",
        "passage_text": "Canonical contract text contains the clause.",
    }])
    csv_path = tmp_path / "annotations.csv"
    annotations.to_csv(csv_path, index=False)

    report = align_cuad_annotations(csv_path, text_root, tmp_path / "out")
    manifest = pd.read_csv(tmp_path / "out" / "cuad_fulltext_manifest.csv")
    assert report["contracts_with_full_text"] == 1
    assert report["full_text_files_considered"] == 1
    assert report["full_text_selection_strategy"] == (
        "complete_category_organized_collection"
    )
    assert manifest.iloc[0]["status"] == "matched_full_text"
