from pptlint.rules.font import FontRule

from tests.fakes import (
    FakeFont,
    FakeParagraph,
    FakePresentation,
    FakeRun,
    FakeShape,
    FakeSlide,
    FakeTextFrame,
)


def test_run_reports_multiple_fonts_on_slide():
    rule = FontRule()

    tf = FakeTextFrame(
        paragraphs=[
            FakeParagraph(text="a", font=FakeFont(name="Arial")),
            FakeParagraph(text="b", runs=[FakeRun(FakeFont(name="Times New Roman"))]),
        ]
    )
    slide = FakeSlide([FakeShape(text_frame=tf)])
    pres = FakePresentation([slide])

    issues = rule.run(pres)

    assert any("разные шрифты" in it.message for it in issues)
    assert any(it.slide == 1 for it in issues)


def test_run_reports_title_font_mismatch():
    rule = FontRule()

    title1 = FakeShape(text_frame=FakeTextFrame(paragraphs=[FakeParagraph(text="t", font=FakeFont(name="Arial"))]))
    title2 = FakeShape(text_frame=FakeTextFrame(paragraphs=[FakeParagraph(text="t", font=FakeFont(name="Times"))]))

    slide1 = FakeSlide([title1], title=title1)
    slide2 = FakeSlide([title2], title=title2)

    pres = FakePresentation([slide1, slide2])

    issues = rule.run(pres)

    assert any("заголовок не совпадает" in it.message for it in issues)


def test_run_reports_too_many_fonts_across_presentation():
    rule = FontRule(max_fonts=2)

    slide1 = FakeSlide(
        [
            FakeShape(
                text_frame=FakeTextFrame(
                    paragraphs=[
                        FakeParagraph(text="a", font=FakeFont(name="A")),
                        FakeParagraph(text="b", font=FakeFont(name="B")),
                    ]
                )
            )
        ]
    )
    slide2 = FakeSlide(
        [
            FakeShape(
                text_frame=FakeTextFrame(
                    paragraphs=[FakeParagraph(text="c", font=FakeFont(name="C"))]
                )
            )
        ]
    )

    pres = FakePresentation([slide1, slide2])

    issues = rule.run(pres)

    assert any("слишком много" in it.message for it in issues)
    assert any(it.slide is None for it in issues)