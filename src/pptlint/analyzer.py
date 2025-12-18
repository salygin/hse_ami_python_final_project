from typing import Any, Dict, List

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
        pass
