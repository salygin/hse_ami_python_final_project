from pptlint.rules.base import Rule


class DummyRule(Rule):
    category = "Cat"

    def run(self, pres):
        return []


def test_issue_includes_rule_and_category():
    rule = DummyRule()
    issue = rule._issue("msg", slide=2)

    assert issue.category == "Cat"
    assert issue.message == "msg"
    assert issue.slide == 2
    assert issue.rule == "DummyRule"
