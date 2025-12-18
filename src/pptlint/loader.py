from pathlib import Path

from pptx import Presentation
from pptx.exc import PackageNotFoundError

import zipfile


class PresentationLoadError(Exception):
    pass


def load_presentation(p: Path) -> Presentation:
    if not str(p).strip():
        raise PresentationLoadError("Путь к файлу пустой.")

    if not p.exists():
        raise FileNotFoundError(f"Файл не найден: {p}")

    if not p.is_file():
        raise PresentationLoadError(f"Указанный путь не является файлом: {p}")

    if p.suffix.lower() != ".pptx":
        raise PresentationLoadError(f"Ожидался файл .pptx, получено: {p.name}")

    try:
        return Presentation(str(p))
    except (PackageNotFoundError, zipfile.BadZipFile):
        raise PresentationLoadError(f"Файл не является валидной .pptx-презентацией: {p}") from None
    except Exception as e:
        raise PresentationLoadError(f"Не удалось загрузить презентацию: {p}. Ошибка: {e}") from e