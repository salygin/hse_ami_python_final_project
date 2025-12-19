from typing import List

from pptx.oxml.ns import qn

from .base import Rule, Issue
from ..utils import iter_text_shapes


class ListRule(Rule):
    CATEGORY = "Списки"

    def run(self, pres) -> List[Issue]:
        issues: List[Issue] = []

        for slide_idx, slide in enumerate(getattr(pres, "slides", []), start=1):
            list_frames = 0
            one_item_frames = 0
            mixed_frames = 0

            for shape in iter_text_shapes(slide):
                tf = shape.text_frame
                items = self._count_items(tf)
                if items <= 0:
                    continue

                list_frames += 1
                if items == 1:
                    one_item_frames += 1
                if self._has_mixed_bullets(tf):
                    mixed_frames += 1

            if one_item_frames > 0:
                if list_frames >= 2 and one_item_frames == 1:
                    msg = f"Слайд {slide_idx}: на слайде {list_frames} списка, один из них из 1 пункта."
                elif list_frames == 1 and one_item_frames == 1:
                    msg = f"Слайд {slide_idx}: список из 1 пункта."
                else:
                    msg = f"Слайд {slide_idx}: {one_item_frames} списка из 1 пункта."
                issues.append(self._issue(slide_idx, msg))

            if mixed_frames > 0:
                if mixed_frames == 1:
                    msg = (
                        f"Слайд {slide_idx}: список с перемешанными маркерами."
                    )
                else:
                    msg = (
                        f"Слайд {slide_idx}: {mixed_frames} списка с перемешанными маркерами."
                    )
                issues.append(self._issue(slide_idx, msg))

        return issues

    @staticmethod
    def _count_items(self, text_frame) -> int:
        pass

    @staticmethod
    def _has_mixed_bullets(self, text_frame) -> bool:
        pass