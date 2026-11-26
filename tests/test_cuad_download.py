from pathlib import Path
import sys
import types

import pytest

from lexshift.cuad_download import download_cuad_text


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
    (text_dir / "one.txt").write_text("sample", encoding="utf-8")

    def fake_snapshot_download(**kwargs):
        return str(tmp_path / "snapshot")

    monkeypatch.setattr(cuad_download, "EXPECTED_CONTRACTS", 510)
    fake_hub = types.ModuleType("huggingface_hub")
    fake_hub.snapshot_download = fake_snapshot_download
    monkeypatch.setitem(sys.modules, "huggingface_hub", fake_hub)

    with pytest.raises(ValueError, match="Expected 510 CUAD TXT files"):
        download_cuad_text(tmp_path / "download")
