from pptlint.rules.text_density import TextDensityRule

from tests.fakes import FakeFont, FakeParagraph, FakePresentation, FakeRun, FakeShape, FakeSlide, FakeSize, FakeTextFrame


def test_count_lines_counts_newlines_and_paragraphs():
    rule = TextDensityRule()
    tf = FakeTextFrame(
        paragraphs=[
            FakeParagraph(text="one"),
            FakeParagraph(text="two\nthree"),
            FakeParagraph(text=""),
        ]
    )

    assert rule._count_lines(tf) == 3


def test_min_font_size_uses_runs_and_paragraph_fallbacks():
    rule = TextDensityRule()
    tf = FakeTextFrame(
        paragraphs=[
            FakeParagraph(
                text="a",
                font=FakeFont(size=FakeSize(20)),
                runs=[
                    FakeRun(FakeFont(size=FakeSize(18))),
                    FakeRun(FakeFont(size=FakeSize(12))),
                ],
            ),
            FakeParagraph(text="b", font=FakeFont(size=FakeSize(16))),
        ]
    )

    assert rule._min_font_size(tf) == 12


def test_run_reports_too_many_lines_and_small_font():
    rule = TextDensityRule(max_lines=2, min_font_pt=16)

    tf = FakeTextFrame(
        paragraphs=[
            FakeParagraph(text="one"),
            FakeParagraph(text="two"),
            FakeParagraph(text="three"),
            FakeParagraph(text="", runs=[FakeRun(FakeFont(size=FakeSize(12)))]),
        ]
    )
    shape = FakeShape(text_frame=tf)
    slide = FakeSlide([shape])
    pres = FakePresentation([slide])

    issues = rule.run(pres)
    messages = [it.message for it in issues]

    assert any("более 2 строк" in msg for msg in messages)
    assert any("слишком маленький размер шрифта" in msg for msg in messages)
