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
            result = rule.run(pres)
            if not result:
                continue
            for item in result:
                if isinstance(item, Issue):
                    issues.append(item)
                elif isinstance(item, dict):
                    issues.append(
                        Issue(
                            category=item.get("category", rule.category),
                            message=item.get("message", ""),
                            slide=item.get("slide"),
                            rule=item.get("rule", rule.__class__.__name__),
                        )
                    )
                else:
                    issues.append(
                        Issue(
                            category=rule.category,
                            message=str(item),
                            slide=None,
                            rule=rule.__class__.__name__,
                        )
                    )

        issues.sort(
            key=lambda x: (
                x.category,
                x.slide if x.slide is not None else 10**9,
                x.message,
            )
        )
        return issues
