"""Download and reconstruct the official CUAD v1 full-contract text collection."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
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


def _extract_pdf_text(pdf_path: Path) -> str:
    """Extract PDF text with PyMuPDF without the slower layout-sorting pass."""
    try:
        import pymupdf
    except ImportError as exc:
        raise RuntimeError(
            "Install PDF recovery support with pip install -e '.[data]' "
            "(PyMuPDF is included in the data extra)."
        ) from exc

    with pymupdf.open(str(pdf_path)) as document:
        pages = []
        for page in document:
            text = page.get_text("text") or ""
            if text:
                pages.append(text)
    return "\n\n".join(pages).strip()


def _flat_txt_mirrors(text_dir: Path) -> dict[str, Path]:
    """Index only the official flat Part_I/Part_II TXT mirrors by basename."""
    mirrors: dict[str, Path] = {}
    for part in ("Part_I", "Part_II"):
        part_dir = text_dir / part
        if not part_dir.is_dir():
            continue
        for path in sorted(part_dir.glob("*.txt")):
            key = path.stem.casefold()
            if key in mirrors:
                raise ValueError(
                    f"Duplicate flat TXT mirror basename {path.stem!r}: "
                    f"{mirrors[key]} and {path}"
                )
            mirrors[key] = path
    return mirrors


def download_cuad_text(output_dir: str | Path) -> dict[str, Any]:
    """Download the pinned CUAD release and build one TXT per canonical PDF."""
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

    text_dir = snapshot_path / "CUAD_v1" / TEXT_FOLDER_NAME
    pdf_dir = snapshot_path / "CUAD_v1" / PDF_FOLDER_NAME
    if not text_dir.is_dir() or not pdf_dir.is_dir():
        raise ValueError(
            "The pinned CUAD snapshot must contain both full_contract_txt "
            "and full_contract_pdf directories."
        )

    pdf_files = sorted(
        path for path in pdf_dir.rglob("*")
        if path.is_file() and path.suffix.casefold() == ".pdf"
    )
    if len(pdf_files) != EXPECTED_CONTRACTS:
        raise ValueError(
            f"Expected {EXPECTED_CONTRACTS} official CUAD PDFs, found "
            f"{len(pdf_files)}. Do not proceed with an incomplete source set."
        )

    pdf_names = [path.stem.casefold() for path in pdf_files]
    if len(pdf_names) != len(set(pdf_names)):
        raise ValueError(
            "Duplicate PDF basenames found in the pinned CUAD release; "
            "refusing an ambiguous TXT reconstruction."
        )

    mirrors = _flat_txt_mirrors(text_dir)
    matched_mirrors = {
        name: path for name, path in mirrors.items() if name in set(pdf_names)
    }
    if len(matched_mirrors) != 196:
        raise ValueError(
            "Expected 196 basename-matched official TXT mirrors for this "
            f"pinned revision, found {len(matched_mirrors)}. Recheck the "
            "dataset revision and source directory before recovery."
        )

    recovered_from_pdf = 0
    copied_from_txt = 0
    files: list[Path] = []

    for index, pdf_path in enumerate(pdf_files, start=1):
        relative_txt = pdf_path.relative_to(pdf_dir).with_suffix(".txt")
        output_path = text_dir / relative_txt
        output_path.parent.mkdir(parents=True, exist_ok=True)

        mirror = matched_mirrors.get(pdf_path.stem.casefold())
        if mirror is not None:
            # The flat mirrors are the official text source for these
            # contracts; copy them to the corresponding category path.
            if mirror.resolve() != output_path.resolve():
                shutil.copyfile(mirror, output_path)
            copied_from_txt += 1
        elif not output_path.is_file() or output_path.stat().st_size == 0:
            # A nonempty category-path file is retained across interrupted
            # runs, so already completed PDF extraction is not repeated.
            try:
                extracted = _extract_pdf_text(pdf_path)
            except Exception as exc:
                raise RuntimeError(
                    f"PDF text extraction failed for {pdf_path.name} "
                    f"({index}/{len(pdf_files)}). Rerun safely; completed "
                    "nonempty TXT recoveries are preserved."
                ) from exc
            if not extracted:
                raise ValueError(
                    f"PDF text extraction returned no text for "
                    f"{pdf_path.name}. Do not proceed with incomplete text."
                )
            output_path.write_text(extracted, encoding="utf-8")
            recovered_from_pdf += 1

        if not output_path.is_file() or output_path.stat().st_size == 0:
            raise ValueError(f"Missing or empty reconstructed TXT: {output_path}")
        files.append(output_path)

    files = sorted(files)
    relative_names = [path.relative_to(text_dir).as_posix().casefold() for path in files]
    if len(files) != EXPECTED_CONTRACTS or len(relative_names) != len(set(relative_names)):
        raise ValueError(
            f"Expected {EXPECTED_CONTRACTS} unique category-mapped TXT files, "
            f"found {len(files)}."
        )

    manifest = {
        "dataset": "Contract Understanding Atticus Dataset (CUAD) v1",
        "repository": CUAD_REPO_ID,
        "revision": CUAD_REVISION,
        "text_directory": str(text_dir),
        "pdf_directory": str(pdf_dir),
        "expected_contracts": EXPECTED_CONTRACTS,
        "downloaded_contracts": len(files),
        "official_pdf_files": len(pdf_files),
        "flat_txt_mirrors": len(mirrors),
        "flat_txt_mirrors_matched_to_pdfs": copied_from_txt,
        "recovered_from_pdf": recovered_from_pdf,
        "selection_strategy": "canonical_pdf_paths_with_flat_txt_mirror_reuse",
        "files": [
            {
                "relative_path": path.relative_to(text_dir).as_posix(),
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
        "copied_from_txt": copied_from_txt,
        "recovered_from_pdf": recovered_from_pdf,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download and reconstruct pinned official CUAD v1 full text."
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
