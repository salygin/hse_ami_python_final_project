from typing import List

from .base import Rule, Issue


class FontRule(Rule):
    category = "Шрифты"

    def __init__(self, max_fonts: int = 3):
        pass

    def run(self, pres) -> List[Issue]:
        pass
   