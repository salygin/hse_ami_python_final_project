import re

from .base import Rule, Issue
from ..utils import iter_text_shapes


class SlideNumberRule(Rule):
    category = "Нумерация слайдов"

    def run(self, pres: object) -> list[Issue]:
        total_slides = len(getattr(pres, "slides", []))
        issues: list[Issue] = []
        slide_num: dict[int, int | None] = {}

        for idx, slide in enumerate(pres.slides, start=1):
            candidates: list[tuple[int, int]] = []
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
                issues.append(self._issue("Нет номера слайда.", slide=idx))

        first_numbered = next(((i, n) for i, n in slide_num.items() if n is not None), None)
        if first_numbered is not None:
            i0, n0 = first_numbered
            if n0 != 1:
                issues.append(
                    self._issue(
                        f"Нумерация начинается не с 1 (первый найденный номер: {n0}).",
                        slide=i0,
                    )
                )

        gap_slides: set[int] = set()
        prev_n: int | None = None
        for i in range(1, total_slides + 1):
            n = slide_num.get(i)
            if n is None:
                continue
            if prev_n is not None and n != prev_n + 1:
                gap_slides.add(i)
                issues.append(self._issue(f"Разрыв нумерации: после {prev_n} идёт {n}.", slide=i))
            prev_n = n

        for i in range(1, total_slides + 1):
            n = slide_num.get(i)
            if n is None or i in gap_slides:
                continue
            if n != i:
                issues.append(
                    self._issue(
                        f"Номер на слайде не соответствует позиции: найден {n}, ожидался {i}.",
                        slide=i,
                    )
                )

        return issues
    
    def _extract_number(self, shape: object, total_slides: int | None = None) -> int | None:
        if not getattr(shape, "has_text_frame", False):
            return None

        text_frame = getattr(shape, "text_frame", None)
        if text_frame is None:
            return None

        raw = (getattr(text_frame, "text", "")).strip()
        if not raw:
            return None

        # слишком длинные или многострочные тексты почти наверняка не номер слайда
        if "\n" in raw or len(raw) > 20:
            return None

        s = raw.strip()
        if not s:
            return False
        
        # убираем типичные обертки номера слайда
        s = re.sub(r"^\s*(?:slide\s*)?", "", s, flags=re.IGNORECASE)
        s = re.sub(r"^\s*(?:слайд\s*)?", "", s, flags=re.IGNORECASE)
        s = re.sub(r"^\s*[#№]+\s*", "", s)
        s = re.sub(r"^[\-\–\—\(\[\{]\s*", "", s)
        s = re.sub(r"\s*[\-\–\—\)\]\}]\s*$", "", s)
        s = s.strip()

        # "3/10"
        m = re.fullmatch(r"(\d+)\s*/\s*(\d+)", s)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if a <= 0:
                return None
            if total_slides is not None and (b <= 0 or b < total_slides - 2 or b > total_slides):
                return None
            if b > 1000:
                return None
            if a > b:
                return None
            return a

        # "3"
        if re.fullmatch(r"\d+", s):
            n = int(s)
            if n <= 0:
                return None
            if n > total_slides:
                return None
            if n > 1000:
                return None
            return n

        return None
