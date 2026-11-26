"""Convert CUAD v1 master-clauses CSV rows to LEXSHIFT annotation records.

The converter preserves CUAD's evidence passages and source answers. It does
not infer missing labels, normalize legal meaning, or create character offsets.
"""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

CATEGORY_MAP = {
    "Governing Law": "governing_law",
    "Non-Compete": "non_compete",
    "Anti-Assignment": "anti_assignment",
    "Termination For Convenience": "termination_for_convenience",
    "Cap On Liability": "cap_on_liability",
}
OUTPUT_COLUMNS = [
    "contract_id", "source_domain", "source_reference", "document_date",
    "industry", "clause_category", "presence", "passage_id", "passage_text",
    "start_char", "end_char", "annotator_id", "confidence", "needs_review",
    "adjudication_status", "annotation_version", "source_answer", "notes",
]


def parse_passages(value: Any) -> list[str]:
    """Parse a CUAD evidence cell containing a serialized list of passages."""
    if value is None or (not isinstance(value, (list, tuple)) and pd.isna(value)):
        return []
    if isinstance(value, (list, tuple)):
        parsed = list(value)
    else:
        raw = str(value).strip()
        if not raw or raw in {"[]", "nan", "None"}:
            return []
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            try:
                parsed = ast.literal_eval(raw)
            except (ValueError, SyntaxError) as exc:
                raise ValueError(f"Could not parse CUAD passage cell: {raw[:120]!r}") from exc
    if not isinstance(parsed, (list, tuple)):
        raise ValueError("CUAD passage cell must decode to a list of evidence passages.")
    return [str(item).strip() for item in parsed if str(item).strip()]


def _safe_id(filename: str) -> str:
    """Use the source filename as a stable, collision-resistant contract key."""
    return filename.strip()


def convert_cuad_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Convert a CUAD master frame into one row per evidence passage or negative."""
    if "Filename" not in frame.columns:
        raise ValueError("CUAD input is missing required 'Filename' column.")
    missing = [
        col for category in CATEGORY_MAP
        for col in (category, f"{category}-Answer")
        if col not in frame.columns
    ]
    if missing:
        raise ValueError("CUAD input is missing required columns: " + ", ".join(missing))
    if frame["Filename"].isna().any() or frame["Filename"].astype(str).str.strip().eq("").any():
        raise ValueError("CUAD Filename values must be present.")
    if frame["Filename"].duplicated().any():
        raise ValueError("CUAD Filename values must be unique before conversion.")

    records: list[dict[str, Any]] = []
    for _, source in frame.iterrows():
        filename = str(source["Filename"]).strip()
        for source_category, category in CATEGORY_MAP.items():
            passages = parse_passages(source[source_category])
            answer_value = source[f"{source_category}-Answer"]
            answer = None if pd.isna(answer_value) else str(answer_value).strip()
            if source_category != "Governing Law":
                if answer not in {"Yes", "No"}:
                    raise ValueError(
                        f"{filename}: unexpected {source_category}-Answer value {answer!r}"
                    )
                if (answer == "Yes") != bool(passages):
                    raise ValueError(
                        f"{filename}: {source_category} answer disagrees with evidence passages"
                    )
            elif answer in {"", "[]", "nan"}:
                answer = None

            base = {
                "contract_id": _safe_id(filename),
                "source_domain": "cuad",
                "source_reference": filename,
                "document_date": None,
                "industry": None,
                "clause_category": category,
                "annotator_id": "cuad_v1",
                "confidence": "source_annotated",
                "needs_review": False,
                "adjudication_status": "not_adjudicated",
                "annotation_version": "cuad_v1_import_1",
                "source_answer": answer,
                "notes": (
                    "Imported CUAD expert evidence. Governing Law jurisdiction answer "
                    "is preserved verbatim; presence is based on evidence passage availability."
                    if source_category == "Governing Law"
                    else "Imported CUAD expert evidence; no legal reinterpretation performed."
                ),
            }
            if passages:
                for index, passage in enumerate(passages, start=1):
                    records.append({
                        **base,
                        "presence": True,
                        "passage_id": f"cuad:{category}:{index:03d}",
                        "passage_text": passage,
                        "start_char": None,
                        "end_char": None,
                    })
            else:
                records.append({
                    **base,
                    "presence": False,
                    "passage_id": None,
                    "passage_text": None,
                    "start_char": None,
                    "end_char": None,
                })
    return pd.DataFrame.from_records(records, columns=OUTPUT_COLUMNS)


def convert_cuad_csv(input_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    """Convert a local CUAD CSV and write a standardized annotation CSV."""
    source = Path(input_path)
    if not source.is_file():
        raise FileNotFoundError(f"CUAD CSV not found: {source}")
    frame = pd.read_csv(source)
    converted = convert_cuad_frame(frame)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    converted.to_csv(destination, index=False)
    return {
        "source_rows": int(len(frame)),
        "annotation_rows": int(len(converted)),
        "contracts": int(converted["contract_id"].nunique()),
        "categories": int(converted["clause_category"].nunique()),
        "positive_rows": int(converted["presence"].sum()),
        "negative_rows": int((~converted["presence"]).sum()),
        "output_path": str(destination),
        "category_summary": {
            key: {
                "positive_passages": int(group.loc[group["presence"], "passage_id"].count()),
                "negative_contracts": int((~group["presence"]).sum()),
                "contracts": int(group["contract_id"].nunique()),
            }
            for key, group in converted.groupby("clause_category", sort=True)
        },
    }


def main() -> None:
    import argparse
    print("LEXSHIFT CUAD converter")
    parser = argparse.ArgumentParser(description="Convert CUAD master CSV to LEXSHIFT annotations.")
    parser.add_argument("input_csv")
    parser.add_argument("output_csv")
    args = parser.parse_args()
    print(json.dumps(convert_cuad_csv(args.input_csv, args.output_csv), indent=2))


if __name__ == "__main__":
    main()
