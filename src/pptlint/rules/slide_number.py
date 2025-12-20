from typing import Any, Optional, List, Tuple

from .base import Rule, Issue
from ..utils import iter_text_shapes


class SlideNumberRule(Rule):
    category = "Нумерация слайдов"

    def run(self, pres: Any) -> List[Issue]:
        total_slides = len(getattr(pres, "slides", []))
        issues: List[Issue] = []
        slide_num: dict[int, Optional[int]] = {}

        for idx, slide in enumerate(pres.slides, start=1):
            candidates: List[Tuple[int, int]] = []
            for shape in iter_text_shapes(slide):
                num = self._extract_number(shape, total_slides=total_slides)
                if num is None:
                    continue

                dist = abs(num - idx)
                candidates.append((dist, num))

            if not candidates:
                slide_num[idx] = None
                continue

            candidates.sort()
            slide_num[idx] = candidates[0][1]

        for idx in range(1, total_slides + 1):
            if slide_num.get(idx) is None:
                issues.append(self._issue(idx, "Нет номера слайда."))

        first_numbered = next(((i, n) for i, n in slide_num.items() if n is not None), None)
        if first_numbered is not None:
            i0, n0 = first_numbered
            if n0 != 1:
                issues.append(
                    self._issue(
                        i0,
                        f"Нумерация начинается не с 1 (первый найденный номер: {n0}).",
                    )
                )

        gap_slides: set[int] = set()
        prev_n: Optional[int] = None
        for i in range(1, total_slides + 1):
            n = slide_num.get(i)
            if n is None:
                continue
            if prev_n is not None and n != prev_n + 1:
                gap_slides.add(i)
                issues.append(self._issue(i, f"Разрыв нумерации: после {prev_n} идёт {n}."))
            prev_n = n

        for i in range(1, total_slides + 1):
            n = slide_num.get(i)
            if n is None or i in gap_slides:
                continue
            if n != i:
                issues.append(
                    self._issue(i, f"Номер на слайде не соответствует позиции: найден {n}, ожидался {i}.")
                )

        return issues
    
    def _extract_number(self, shape: Any, total_slides: Optional[int] = None) -> Optional[int]:
        pass