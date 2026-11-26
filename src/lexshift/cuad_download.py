"""Download the official CUAD v1 full-contract TXT files reproducibly."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

CUAD_REPO_ID = "theatticusproject/cuad"
CUAD_REVISION = "a3c393f5d103fd0c516374e4fdff676c8176dcb1"
EXPECTED_CONTRACTS = 510
TEXT_FOLDER_NAME = "full_contract_txt"
PDF_FOLDER_NAME = "full_contract_pdf"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_cuad_text(output_dir: str | Path) -> dict[str, Any]:
    """Download and verify the pinned official CUAD v1 TXT collection."""
    try:
        from huggingface_hub import snapshot_download
    except ImportError as exc:
        raise RuntimeError(
            "Install the optional data dependencies with "
            "pip install -e '.[data]'."
        ) from exc

    destination = Path(output_dir).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    snapshot_path = Path(snapshot_download(
        repo_id=CUAD_REPO_ID,
        repo_type="dataset",
        revision=CUAD_REVISION,
        allow_patterns=[
            f"CUAD_v1/{TEXT_FOLDER_NAME}/**",
            f"CUAD_v1/{PDF_FOLDER_NAME}/**",
        ],
        local_dir=str(destination),
    ))

    # Hugging Face local_dir may also create cache/metadata directories that
    # contain a second path with the same folder name. Prefer the documented
    # dataset path and ignore internal cache paths when using the fallback.
    expected_text_dir = snapshot_path / "CUAD_v1" / TEXT_FOLDER_NAME
    if expected_text_dir.is_dir():
        text_dir = expected_text_dir
    else:
        candidates = [
            path
            for path in snapshot_path.rglob(TEXT_FOLDER_NAME)
            if path.is_dir() and ".cache" not in path.parts
        ]
        if len(candidates) != 1:
            raise ValueError(
                f"Expected one non-cache {TEXT_FOLDER_NAME} directory, "
                f"found {len(candidates)}."
            )
        text_dir = candidates[0]
    files = sorted(text_dir.rglob("*.txt"))
    existing_names = {path.name.casefold() for path in files}
    pdf_dir = snapshot_path / "CUAD_v1" / PDF_FOLDER_NAME
    pdf_files = sorted(pdf_dir.rglob("*.pdf")) if pdf_dir.is_dir() else []
    if len(pdf_files) != EXPECTED_CONTRACTS:
        raise ValueError(
            f"Expected {EXPECTED_CONTRACTS} CUAD PDF files for recovery, "
            f"found {len(pdf_files)}. Existing TXT count: {len(files)}."
        )

    missing_pdfs = [
        path for path in pdf_files if path.stem.casefold() not in existing_names
    ]
    if missing_pdfs:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError(
                "The Hugging Face TXT mirror contains only a subset of the "
                "510 contracts. Install PDF recovery support with "
                "pip install -e '.[data]' (pypdf is included in the data extra)."
            ) from exc

        for pdf_path in missing_pdfs:
            relative_path = pdf_path.relative_to(pdf_dir).with_suffix(".txt")
            output_path = text_dir / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            reader = PdfReader(str(pdf_path))
            extracted = "\n\n".join(
                page.extract_text() or "" for page in reader.pages
            ).strip()
            if not extracted:
                raise ValueError(
                    f"PDF text extraction returned no text for {pdf_path.name}. "
                    "Do not proceed with incomplete source text."
                )
            output_path.write_text(extracted, encoding="utf-8")
            files.append(output_path)

    files = sorted(files)
    if len(files) != EXPECTED_CONTRACTS:
        raise ValueError(
            f"Expected {EXPECTED_CONTRACTS} CUAD text files after PDF recovery, "
            f"found {len(files)}. Do not proceed to alignment."
        )
    names = [path.name.casefold() for path in files]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate TXT basenames found.")

    manifest = {
        "dataset": "Contract Understanding Atticus Dataset (CUAD) v1",
        "repository": CUAD_REPO_ID,
        "revision": CUAD_REVISION,
        "text_directory": str(text_dir),
        "expected_contracts": EXPECTED_CONTRACTS,
        "downloaded_contracts": len(files),
        "original_txt_files": len(existing_names),
        "recovered_from_pdf": len(missing_pdfs),
        "files": [
            {
                "filename": path.name,
                "bytes": path.stat().st_size,
                "sha256": _sha256_file(path),
            }
            for path in files
        ],
        "raw_contract_text_committed_to_repository": False,
    }
    manifest_path = destination / "cuad_text_download_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {
        "contracts": len(files),
        "text_directory": str(text_dir),
        "manifest": str(manifest_path),
        "revision": CUAD_REVISION,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download the pinned official CUAD v1 full-contract TXT files."
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="data/raw/cuad_release",
        help="Local destination; never commit this directory.",
    )
    args = parser.parse_args()
    print(json.dumps(download_cuad_text(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
