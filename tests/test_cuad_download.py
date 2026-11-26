from pathlib import Path
import sys
import types

import pytest

from lexshift.cuad_download import download_cuad_text


def _mock_snapshot(monkeypatch, snapshot_path: Path):
    from lexshift import cuad_download

    def fake_snapshot_download(**kwargs):
        return str(snapshot_path)

    fake_hub = types.ModuleType("huggingface_hub")
    fake_hub.snapshot_download = fake_snapshot_download
    monkeypatch.setitem(sys.modules, "huggingface_hub", fake_hub)
    return cuad_download


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


def test_download_rejects_incomplete_collection(monkeypatch, tmp_path: Path):
    from lexshift import cuad_download

    text_dir = tmp_path / "snapshot" / "CUAD_v1" / "full_contract_txt"
    text_dir.mkdir(parents=True)
    (text_dir / "Part_I").mkdir()
    (text_dir / "Part_I" / "one.txt").write_text("sample", encoding="utf-8")

    _mock_snapshot(monkeypatch, tmp_path / "snapshot")
    monkeypatch.setattr(cuad_download, "EXPECTED_CONTRACTS", 510)

    with pytest.raises(ValueError, match="Expected 510 CUAD text files"):
        download_cuad_text(tmp_path / "download")


def test_download_prefers_complete_organized_collection(
    monkeypatch, tmp_path: Path
):
    snapshot = tmp_path / "snapshot"
    text_dir = snapshot / "CUAD_v1" / "full_contract_txt"
    organized_dir = text_dir / "Part_III" / "Service"
    organized_dir.mkdir(parents=True)

    # Simulate the 200-file flat mirror plus the canonical 510-file collection.
    (text_dir / "Part_I").mkdir()
    (text_dir / "Part_II").mkdir()
    for index in range(100):
        (text_dir / "Part_I" / f"mirror_i_{index}.txt").write_text(
            "mirror", encoding="utf-8"
        )
        (text_dir / "Part_II" / f"mirror_ii_{index}.txt").write_text(
            "mirror", encoding="utf-8"
        )
    for index in range(510):
        (organized_dir / f"contract_{index}.txt").write_text(
            f"contract {index}", encoding="utf-8"
        )

    cuad_download = _mock_snapshot(monkeypatch, snapshot)
    monkeypatch.setattr(cuad_download, "EXPECTED_CONTRACTS", 510)

    report = download_cuad_text(tmp_path / "download")
    assert report["contracts"] == 510

    import json

    manifest = json.loads(Path(report["manifest"]).read_text(encoding="utf-8"))
    assert manifest["discovered_txt_files"] == 710
    assert manifest["original_txt_files_selected"] == 510
    assert manifest["recovered_from_pdf"] == 0
    assert manifest["selection_strategy"] == "complete_category_organized_collection"


def test_extract_pdf_text_uses_pymupdf(monkeypatch, tmp_path: Path):
    from lexshift import cuad_download

    class FakePage:
        def get_text(self, mode, sort=False):
            assert mode == "text"
            assert sort is True
            return "contract text"

    class FakeDocument:
        def __enter__(self):
            return [FakePage(), FakePage()]

        def __exit__(self, *args):
            return False

    fake_pymupdf = types.ModuleType("pymupdf")
    fake_pymupdf.open = lambda path: FakeDocument()
    monkeypatch.setitem(sys.modules, "pymupdf", fake_pymupdf)

    assert cuad_download._extract_pdf_text(tmp_path / "sample.pdf") == (
        "contract text\n\ncontract text"
    )
