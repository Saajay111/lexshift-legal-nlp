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
        allow_patterns=[f"CUAD_v1/{TEXT_FOLDER_NAME}/**"],
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
    if len(files) != EXPECTED_CONTRACTS:
        raise ValueError(
            f"Expected {EXPECTED_CONTRACTS} CUAD TXT files, found {len(files)}. "
            "Do not proceed to alignment with an incomplete download."
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
