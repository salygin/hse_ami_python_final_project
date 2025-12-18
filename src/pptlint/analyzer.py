from typing import List

from .rules.base import Rule, Issue
from .rules.list import ListRule
from .rules.font import FontRule
from .rules.slide_number import SlideNumberRule
from .rules.text_density import TextDensityRule
from .rules.title_style import TitleStyleRule


class PresentationAnalyzer:
    def __init__(self) -> None:
        self.rules: List[Rule] = [
            ListRule(),
            FontRule(),
            SlideNumberRule(),
            TextDensityRule(),
            TitleStyleRule(),
        ]

    def analyze(self, pres) -> List[Issue]:
        issues: List[Issue] = []

        for rule in self.rules:
            issues.append(rule.run(pres))

        issues.sort(
            key=lambda x: (
                x.get("category", ""),
                x.get("slide", 10**9),
                x.get("message", ""),
            )
        )
        return issues
