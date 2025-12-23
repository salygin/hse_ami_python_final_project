from pptlint.rules.title_style import TitleStyleRule

from tests.fakes import (
    FakeFont,
    FakeParagraph,
    FakePresentation,
    FakeRun,
    FakeShape,
    FakeSlide,
    FakeSize,
    FakeTextFrame
)


def _title_shape(font_name: str, size_pt: float, bold: bool, text: str = "Title"):
    run = FakeRun(FakeFont(name=font_name, size=FakeSize(size_pt), bold=bold))
    tf = FakeTextFrame(paragraphs=[FakeParagraph(text=text, runs=[run])])
    return FakeShape(text_frame=tf)


def test_missing_title_reports_issue():
    rule = TitleStyleRule(ignore_first_slide=True)

    slide1 = FakeSlide([], title=None)
    slide2 = FakeSlide([], title=None)
    pres = FakePresentation([slide1, slide2])

    issues = rule.run(pres)

    assert any(it.slide == 2 and "нет заголовка" in it.message for it in issues)


def test_title_style_mismatch_reports_issue():
    rule = TitleStyleRule(ignore_first_slide=True)

    title_a = _title_shape("Arial", 24, True)
    title_b = _title_shape("Times", 24, True)

    slide1 = FakeSlide([title_a], title=title_a)
    slide2 = FakeSlide([title_a], title=title_a)
    slide3 = FakeSlide([title_b], title=title_b)

    pres = FakePresentation([slide1, slide2, slide3])

    issues = rule.run(pres)

    assert any(it.slide == 3 and "отличается по стилю" in it.message for it in issues)