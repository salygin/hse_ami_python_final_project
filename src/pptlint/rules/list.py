from typing import List

from .base import Rule, Issue


class ListRule(Rule):
    CATEGORY = "Списки"

    def run(self, pres) -> List[Issue]:
        pass