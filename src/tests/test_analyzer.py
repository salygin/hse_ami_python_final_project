from pptlint.analyzer import PresentationAnalyzer
from pptlint.rules.base import Rule


class FakeRule(Rule):
    category = "Z"

    def __init__(self, issues):
        self._issues = issues

    def run(self, pres):
        return self._issues


def test_analyzer_has_default_rules():
    analyzer = PresentationAnalyzer()
    rule_names = [rule.__class__.__name__ for rule in analyzer.rules]

    assert rule_names == [
        "ListRule",
        "FontRule",
        "SlideNumberRule",
        "TextDensityRule",
        "TitleStyleRule",
    ]


def test_analyzer_sorts_issues():
    analyzer = PresentationAnalyzer()
    analyzer.rules = [
        FakeRule([
            {"category": "B", "slide": 2, "message": "b"},
            {"category": "A", "slide": 3, "message": "c"},
        ]),
        FakeRule([
            {"category": "A", "slide": 2, "message": "a"},
        ]),
    ]

    issues = analyzer.analyze(object())

    assert [(i.category, i.slide, i.message) for i in issues] == [
        ("A", 2, "a"),
        ("A", 3, "c"),
        ("B", 2, "b"),
    ]
