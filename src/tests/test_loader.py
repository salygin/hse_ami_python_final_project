from pathlib import Path

import pytest
from pptx.exc import PackageNotFoundError

from pptlint import loader


def test_load_presentation_empty_path():
    with pytest.raises(loader.PresentationLoadError, match="Путь к файлу пустой"):
        loader.load_presentation(Path(" "))


def test_load_presentation_missing_file(tmp_path: Path):
    missing = tmp_path / "missing.pptx"
    with pytest.raises(FileNotFoundError):
        loader.load_presentation(missing)


def test_load_presentation_not_file(tmp_path: Path):
    p = tmp_path / "dir"
    p.mkdir()
    with pytest.raises(loader.PresentationLoadError, match="не является файлом"):
        loader.load_presentation(p)


def test_load_presentation_wrong_suffix(tmp_path: Path):
    p = tmp_path / "file.txt"
    p.write_text("x")
    with pytest.raises(loader.PresentationLoadError, match="Ожидался файл .pptx"):
        loader.load_presentation(p)


def test_load_presentation_invalid_pptx(tmp_path: Path, monkeypatch):
    p = tmp_path / "file.pptx"
    p.write_text("not a pptx")

    def _boom(_):
        raise PackageNotFoundError("bad")

    monkeypatch.setattr(loader, "Presentation", _boom)

    with pytest.raises(loader.PresentationLoadError, match="не является валидной"):
        loader.load_presentation(p)
