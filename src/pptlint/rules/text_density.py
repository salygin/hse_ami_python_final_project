from typing import List, Optional

from .base import Rule, Issue
from ..utils import iter_text_shapes

class TextDensityRule(Rule):
    category = "Перегруженность текстом"

    def __init__(self, max_lines: int = 8, min_font_pt: int = 16) -> None:
        self.max_lines = max_lines
        self.min_font_pt = min_font_pt

    def run(self, pres) -> List[Issue]:
        issues: List[Issue] = []

        for slide_idx, slide in enumerate(pres.slides, start=1):
            for shape in iter_text_shapes(slide):
                tf = shape.text_frame
                if tf is None:
                    continue
                line_count = self._count_lines(tf)
                if line_count > self.max_lines:
                    issues.append(
                        self._issue(
                            f"Слайд {slide_idx}: более {self.max_lines} строк текста в одном текстовом блоке "
                            f"(≈ {line_count}).",
                            slide=slide_idx,
                        )
                    )
                min_size = self._min_font_size(tf)
                if min_size is not None and min_size < self.min_font_pt:
                    issues.append(
                        self._issue(
                            f"Слайд {slide_idx}: слишком маленький размер шрифта ({min_size} pt).",
                            slide=slide_idx,
                        )
                    )
        return issues

    def _count_lines(self, text_frame) -> int:
        lines = 0
        for p in getattr(text_frame, "paragraphs", []):
            text = (getattr(p, "text", "") or "").strip()
            if not text:
                continue
            lines += 1 + text.count("\n")
        return lines

    def _min_font_size(self, text_frame) -> Optional[int]:
        min_pt: Optional[int] = None
        for p in getattr(text_frame, "paragraphs", []):
            p_size = self._size_to_pt(getattr(getattr(p, "font", None), "size", None))
            runs = getattr(p, "runs", []) or []
            if runs:
                for r in runs:
                    r_size = self._size_to_pt(getattr(getattr(r, "font", None), "size", None))
                    size = r_size if r_size is not None else p_size
                    if size is None:
                        continue
                    min_pt = size if min_pt is None else min(min_pt, size)
            else:
                if p_size is not None:
                    min_pt = p_size if min_pt is None else min(min_pt, p_size)
        return min_pt

    @staticmethod
    def _size_to_pt(size) -> Optional[int]:
        if size is None:
            return None
        try:
            return int(round(float(size.pt)))
        except Exception:
            return None
