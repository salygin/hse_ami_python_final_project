
from .base import Rule, Issue

class TextDensityRule(Rule):
    category = "Перегруженность текстом"

    def __init__(self, max_lines: int = 8, min_font_pt: int = 16) -> None:
        pass

    def run(self, pres) -> List[Issue]:
        pass