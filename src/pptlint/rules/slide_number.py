from typing import Any, List

from .base import Rule, Issue


class SlideNumberRule(Rule):
    category = "Нумерация слайдов"

    def run(self, pres: Any) -> List[Issue]:
        pass