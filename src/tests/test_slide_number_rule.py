from pptlint.rules.slide_number import SlideNumberRule

from tests.fakes import FakePresentation, FakeShape, FakeSlide, FakeTextFrame


def _shape_with_text(text: str, top: int = 900, height: int = 50):
    tf = FakeTextFrame(text=text)
    return FakeShape(text_frame=tf, top=top, height=height)


def test_extract_number_parses_common_formats():
    rule = SlideNumberRule()

    assert rule._extract_number(_shape_with_text("3")) == 3
    assert rule._extract_number(_shape_with_text("Slide 4")) == 4
    assert rule._extract_number(_shape_with_text("№5")) == 5
    assert rule._extract_number(_shape_with_text("3/10")) == 3


def test_extract_number_rejects_invalid():
    rule = SlideNumberRule()

    assert rule._extract_number(_shape_with_text("0")) is None
    assert rule._extract_number(_shape_with_text("1001")) is None
    assert rule._extract_number(_shape_with_text("text")) is None
    assert rule._extract_number(_shape_with_text("11/10")) is None


def test_run_reports_missing_slide_numbers():
    rule = SlideNumberRule()

    slide1 = FakeSlide([_shape_with_text("1")])
    slide2 = FakeSlide([])
    slide3 = FakeSlide([_shape_with_text("3")])

    pres = FakePresentation([slide1, slide2, slide3], slide_height=1000)

    issues = rule.run(pres)

    assert any(it.slide == 2 and "Нет номера" in it.message for it in issues)


def test_run_reports_start_not_one():
    rule = SlideNumberRule()

    slide1 = FakeSlide([_shape_with_text("2")])
    slide2 = FakeSlide([_shape_with_text("3")])

    pres = FakePresentation([slide1, slide2], slide_height=1000)

    issues = rule.run(pres)

    assert any(it.slide == 1 and "не с 1" in it.message for it in issues)
