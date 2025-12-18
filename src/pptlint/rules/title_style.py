from .base import Rule, Issue

class TitleStyleRule(Rule):
    CATEGORY = "Стиль заголовков"

    def __init__(self, *, ignore_first_slide: bool = True) -> None:
        pass

    def run(self, pres) -> List[Issue]:
        pass