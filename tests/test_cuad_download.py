import json
import sys
import types
from pathlib import Path

import pytest

from lexshift.cuad_download import download_cuad_text


def _mock_snapshot(monkeypatch, snapshot_path: Path):
    def fake_snapshot_download(**kwargs):
        assert kwargs["revision"] == "a3c393f5d103fd0c516374e4fdff676c8176dcb1"
        return str(snapshot_path)

    fake_hub = types.ModuleType("huggingface_hub")
    fake_hub.snapshot_download = fake_snapshot_download
    monkeypatch.setitem(sys.modules, "huggingface_hub", fake_hub)


def test_download_requires_optional_dependency(monkeypatch, tmp_path: Path):
    import builtins

    real_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name == "huggingface_hub":
            raise ImportError("not installed")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", guarded_import)
    with pytest.raises(RuntimeError, match="optional data dependencies"):
        download_cuad_text(tmp_path / "download")


def test_reconstructs_510_category_mapped_texts_from_196_mirrors_and_314_pdfs(
    monkeypatch, tmp_path: Path
):
    snapshot = tmp_path / "snapshot"
    text_dir = snapshot / "CUAD_v1" / "full_contract_txt"
    pdf_dir = snapshot / "CUAD_v1" / "full_contract_pdf"

    # Build 510 unique canonical PDFs across category directories.
    for index in range(510):
        category = "Service" if index % 2 == 0 else "Maintenance"
        part = "Part_I" if index < 170 else ("Part_II" if index < 340 else "Part_III")
        pdf_path = pdf_dir / part / category / f"contract_{index:03}.pdf"
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_path.write_bytes(b"%PDF-test")

    # The pinned release has 100 flat TXT mirrors in each of Part_I/Part_II;
    # 196 of their basenames correspond to official PDFs.
    for index in range(196):
        part = "Part_I" if index < 100 else "Part_II"
        mirror = text_dir / part / f"contract_{index:03}.txt"
        mirror.parent.mkdir(parents=True, exist_ok=True)
        mirror.write_text(f"official mirror {index}", encoding="utf-8")

    _mock_snapshot(monkeypatch, snapshot)

    from lexshift import cuad_download

    calls = []

    def fake_extract(path):
        calls.append(path.name)
        return f"extracted {path.stem}"

    monkeypatch.setattr(cuad_download, "_extract_pdf_text", fake_extract)

    report = download_cuad_text(tmp_path / "download")

    assert report["contracts"] == 510
    assert report["copied_from_txt"] == 196
    assert report["recovered_from_pdf"] == 314
    assert len(calls) == 314

    manifest = json.loads(Path(report["manifest"]).read_text(encoding="utf-8"))
    assert manifest["official_pdf_files"] == 510
    assert manifest["flat_txt_mirrors_matched_to_pdfs"] == 196
    assert manifest["recovered_from_pdf"] == 314
    assert manifest["selection_strategy"] == (
        "canonical_pdf_paths_with_flat_txt_mirror_reuse"
    )

    # Every output mirrors the canonical PDF's category-relative path.
    for index in range(510):
        category = "Service" if index % 2 == 0 else "Maintenance"
        part = "Part_I" if index < 170 else ("Part_II" if index < 340 else "Part_III")
        output = text_dir / part / category / f"contract_{index:03}.txt"
        assert output.is_file()
        if index < 196:
            assert output.read_text(encoding="utf-8") == f"official mirror {index}"
        else:
            assert output.read_text(encoding="utf-8") == f"extracted contract_{index:03}"


def test_rejects_duplicate_pdf_basenames(monkeypatch, tmp_path: Path):
    snapshot = tmp_path / "snapshot"
    text_dir = snapshot / "CUAD_v1" / "full_contract_txt"
    pdf_dir = snapshot / "CUAD_v1" / "full_contract_pdf"
    for folder in ("A", "B"):
        path = pdf_dir / folder / "same.pdf"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"%PDF-test")
    text_dir.mkdir(parents=True)

    _mock_snapshot(monkeypatch, snapshot)

    from lexshift import cuad_download

    monkeypatch.setattr(cuad_download, "EXPECTED_CONTRACTS", 2)
    with pytest.raises(ValueError, match="Duplicate PDF basenames"):
        download_cuad_text(tmp_path / "download")
