"""Conservatively align CUAD evidence passages to the official full contract text.

Exact whitespace-normalized matches take priority. Case-insensitive matching is a fallback only. Unmatched
or repeated passages are flagged for review; this module never invents spans
or treats contract-level negatives as negative text passages.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

CANONICAL_CONTRACT_COUNT = 510


def _read_text(path: Path) -> str:
    """Read CUAD TXT using UTF-8, with a documented Windows-1252 fallback."""
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("cp1252")


def _normalized_with_offsets(
    text: str, *, casefold: bool = False
) -> tuple[str, list[int]]:
    """Collapse whitespace, optionally casefolding, while preserving source offsets."""
    chars: list[str] = []
    offsets: list[int] = []
    in_whitespace = False
    for index, char in enumerate(text):
        if char.isspace():
            if chars and not in_whitespace:
                chars.append(" ")
                offsets.append(index)
            in_whitespace = True
        else:
            # Map any casefold expansion back to its original source character.
            normalized_chars = char.casefold() if casefold else char
            for normalized_char in normalized_chars:
                chars.append(normalized_char)
                offsets.append(index)
            in_whitespace = False
    if chars and chars[-1] == " ":
        chars.pop()
        offsets.pop()
    return "".join(chars), offsets


def _all_occurrences(haystack: str, needle: str) -> list[int]:
    """Return all possibly overlapping exact occurrences."""
    if not needle:
        return []
    hits: list[int] = []
    cursor = 0
    while True:
        found = haystack.find(needle, cursor)
        if found < 0:
            return hits
        hits.append(found)
        cursor = found + 1


def align_passage(full_text: str, passage_text: str) -> dict[str, Any]:
    """Return a unique source span, or a conservative review status."""
    if not isinstance(passage_text, str) or not passage_text.strip():
        return {"status": "empty_passage", "start_char": None, "end_char": None,
                "occurrences": 0}
    # Prefer an exact case-sensitive match. Casefolding is only a fallback,
    # so it cannot turn an otherwise unique exact match into an ambiguity.
    normalized_full, source_offsets = _normalized_with_offsets(full_text)
    normalized_passage, _ = _normalized_with_offsets(passage_text)
    hits = _all_occurrences(normalized_full, normalized_passage)
    match_status = "unique_whitespace_normalized_match"

    if not hits:
        normalized_full, source_offsets = _normalized_with_offsets(
            full_text, casefold=True
        )
        normalized_passage, _ = _normalized_with_offsets(
            passage_text, casefold=True
        )
        hits = _all_occurrences(normalized_full, normalized_passage)
        match_status = "unique_casefolded_whitespace_match"

    if not hits:
        return {"status": "not_found", "start_char": None, "end_char": None,
                "occurrences": 0}
    if len(hits) > 1:
        return {"status": "ambiguous_multiple_matches", "start_char": None,
                "end_char": None, "occurrences": len(hits)}
    start_norm = hits[0]
    end_norm = start_norm + len(normalized_passage)
    start_char = source_offsets[start_norm]
    end_char = source_offsets[end_norm - 1] + 1
    return {"status": match_status, "start_char": start_char,
            "end_char": end_char, "occurrences": 1}


def _canonical_text_files(text_root: Path) -> tuple[list[Path], str]:
    """Return all TXT candidates so annotation evidence can resolve mirror copies."""
    return sorted(text_root.rglob("*.txt")), "all_available_txt_files_scored_by_annotation_evidence"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def align_cuad_annotations(
    annotations_csv: str | Path,
    contracts_txt_dir: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    """Align positive CUAD passages to full TXT files and write audit artifacts."""
    annotation_path = Path(annotations_csv)
    text_root = Path(contracts_txt_dir)
    if not annotation_path.is_file():
        raise FileNotFoundError(f"Annotations CSV not found: {annotation_path}")
    if not text_root.is_dir():
        raise NotADirectoryError(f"Full-contract TXT directory not found: {text_root}")

    annotations = pd.read_csv(annotation_path)
    required = {"contract_id", "source_reference", "clause_category",
                "presence", "passage_id", "passage_text"}
    missing = required - set(annotations.columns)
    if missing:
        raise ValueError(f"Annotation CSV is missing columns: {', '.join(sorted(missing))}")

    selected_files, selection_strategy = _canonical_text_files(text_root)
    txt_index: dict[str, list[Path]] = {}
    for path in selected_files:
        txt_index.setdefault(path.stem.casefold(), []).append(path)

    contract_rows: list[dict[str, Any]] = []
    text_cache: dict[str, str] = {}
    for contract_id, group in annotations.groupby("contract_id", sort=True):
        refs = group["source_reference"].dropna().astype(str).unique()
        base_manifest = {
            "contract_id": contract_id,
            "source_reference": ";".join(refs),
            "candidate_file_count": 0,
            "selected_text_path": None,
            "candidate_match_scores": None,
        }
        if len(refs) != 1:
            contract_rows.append({
                **base_manifest,
                "status": "missing_or_conflicting_source_reference",
                "full_text_characters": None,
                "full_text_sha256": None,
            })
            continue

        source_reference = refs[0]
        stem = Path(source_reference).stem.casefold()
        candidates = txt_index.get(stem, [])
        if not candidates:
            contract_rows.append({
                **base_manifest,
                "source_reference": source_reference,
                "status": "full_text_not_found",
                "full_text_characters": None,
                "full_text_sha256": None,
            })
            continue

        positive_passages = [
            value for value in group.loc[
                group["presence"].astype(bool), "passage_text"
            ].dropna().astype(str).tolist()
            if value.strip()
        ]
        candidate_results: list[tuple[Path, str, int]] = []
        score_details: dict[str, int] = {}
        for candidate in candidates:
            candidate_text = _read_text(candidate)
            score = sum(
                align_passage(candidate_text, passage)["status"]
                in {
                    "unique_whitespace_normalized_match",
                    "unique_casefolded_whitespace_match",
                }
                for passage in positive_passages
            )
            candidate_results.append((candidate, candidate_text, score))
            score_details[str(candidate.relative_to(text_root))] = int(score)

        selected: tuple[Path, str, int] | None = None
        selection_reason = "single_candidate"
        if len(candidate_results) == 1:
            selected = candidate_results[0]
        else:
            best_score = max(item[2] for item in candidate_results)
            best = [item for item in candidate_results if item[2] == best_score]
            if best_score > 0 and len(best) == 1:
                selected = best[0]
                selection_reason = "unique_highest_annotation_match_count"
            else:
                selection_reason = "unresolved_duplicate_candidates"

        if selected is None:
            contract_rows.append({
                **base_manifest,
                "source_reference": source_reference,
                "candidate_file_count": len(candidates),
                "candidate_match_scores": json.dumps(score_details, sort_keys=True),
                "selection_reason": selection_reason,
                "status": "ambiguous_full_text_filename",
                "full_text_characters": None,
                "full_text_sha256": None,
            })
            continue

        selected_path, full_text, selected_score = selected
        text_cache[str(contract_id)] = full_text
        contract_rows.append({
            **base_manifest,
            "source_reference": source_reference,
            "candidate_file_count": len(candidates),
            "selected_text_path": str(selected_path.relative_to(text_root)),
            "candidate_match_scores": json.dumps(score_details, sort_keys=True),
            "selection_reason": selection_reason,
            "selected_candidate_match_count": int(selected_score),
            "status": "matched_full_text",
            "full_text_characters": len(full_text),
            "full_text_sha256": _sha256(full_text),
        })

    manifest = pd.DataFrame(contract_rows)
    status_by_contract = manifest.set_index("contract_id")["status"].to_dict()
    alignment_rows: list[dict[str, Any]] = []
    for row in annotations.itertuples(index=False):
        is_positive = bool(row.presence)
        base = {
            "contract_id": row.contract_id,
            "clause_category": row.clause_category,
            "passage_id": row.passage_id if pd.notna(row.passage_id) else None,
        }
        if not is_positive:
            alignment_rows.append({
                **base, "alignment_status": "not_applicable_contract_level_negative",
                "start_char": None, "end_char": None, "occurrences": 0,
            })
            continue
        if status_by_contract.get(row.contract_id) != "matched_full_text":
            alignment_rows.append({
                **base, "alignment_status": status_by_contract.get(
                    row.contract_id, "contract_missing_from_manifest"
                ), "start_char": None, "end_char": None, "occurrences": 0,
            })
            continue
        result = align_passage(text_cache[str(row.contract_id)], row.passage_text)
        alignment_rows.append({
            **base, "alignment_status": result["status"],
            "start_char": result["start_char"], "end_char": result["end_char"],
            "occurrences": result["occurrences"],
        })

    alignments = pd.DataFrame(alignment_rows)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(destination / "cuad_fulltext_manifest.csv", index=False)
    alignments.to_csv(destination / "cuad_passage_alignment.csv", index=False)

    report = {
        "contracts_in_annotations": int(annotations["contract_id"].nunique()),
        "contracts_with_full_text": int(
            manifest["status"].eq("matched_full_text").sum()
        ),
        "full_text_contract_status": {
            str(k): int(v) for k, v in manifest["status"].value_counts().items()
        },
        "positive_passages": int(annotations["presence"].astype(bool).sum()),
        "alignment_status": {
            str(k): int(v) for k, v in alignments["alignment_status"].value_counts().items()
        },
        "full_text_files_considered": len(selected_files),
        "full_text_selection_strategy": selection_strategy,
        "negative_rows_are_not_passage_examples": True,
        "raw_contract_text_written_to_output": False,
    }
    (destination / "cuad_alignment_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Align CUAD evidence passages against full contract TXT files."
    )
    parser.add_argument("annotations_csv")
    parser.add_argument("contracts_txt_dir")
    parser.add_argument("output_dir")
    args = parser.parse_args()
    print(json.dumps(
        align_cuad_annotations(
            args.annotations_csv, args.contracts_txt_dir, args.output_dir
        ),
        indent=2,
    ))


if __name__ == "__main__":
    main()
