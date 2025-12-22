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
                            slide_idx,
                            f"Слайд {slide_idx}: более {self.max_lines} строк текста в одном текстовом блоке "
                            f"(≈ {line_count}).",
                        )
                    )
                min_size = self._min_font_size(tf)
                if min_size is not None and min_size < self.min_font_pt:
                    issues.append(
                        self._issue(
                            slide_idx,
                            f"Слайд {slide_idx}: слишком маленький размер шрифта ({min_size} pt).",
                        )
                    )
        return issues

    def _count_lines(self, text_frame) -> int:
        lines = 0
        for p in text_frame.paragraphs:
            txt = (p.text or "").strip()
            if not txt:
                continue
            lines += 1 + txt.count("\n")
        return lines

    def _min_font_size(self, text_frame) -> Optional[int]:
        min_pt: Optional[int] = None
        for p in text_frame.paragraphs:
            p_size = self._size_to_pt(getattr(p.font, "size", None))
            if p_size:
                min_pt = p_size if min_pt is None else min(min_pt, p_size)
            if getattr(p, "runs", None):
                for r in p.runs:
                    r_size = self._size_to_pt(getattr(r.font, "size", None))
                    if r_size:
                        min_pt = r_size if min_pt is None else min(min_pt, r_size)
        return min_pt
    
    @staticmethod
    def _size_to_pt(size) -> Optional[int]:
        if size is None:
            return None
        try:
            pt_val = float(size.pt)
            return int(round(pt_val))
        except Exception:
            return None