from pptlint.rules.list import ListRule

from tests.fakes import FakeParagraph, FakeShape, FakeSlide, FakeTextFrame


def test_paragraph_type_detects_bullets():
    rule = ListRule()

    assert rule._paragraph_type(FakeParagraph(text="a", bullet_type="auto")) is "auto"
    assert rule._paragraph_type(FakeParagraph(text="a", bullet_type="char")) is "char"
    assert rule._paragraph_type(FakeParagraph(text="a", bullet_type="blip")) is "blip"
    assert rule._paragraph_type(FakeParagraph(text="a", bullet_type="font")) is "font"
    assert rule._paragraph_type(FakeParagraph(text="a", bullet_type="none")) is "none"
    assert rule._paragraph_type(FakeParagraph(text="a", bullet_type=None)) is "none"


def test_count_items_counts_only_list_items():
    rule = ListRule()

    tf = FakeTextFrame(
        paragraphs=[
            FakeParagraph(text="one", bullet_type="auto"),
            FakeParagraph(text="two", bullet_type="none"),
            FakeParagraph(text="", bullet_type="auto"),
        ]
    )

    assert rule._count_items(tf) == 1


def test_has_mixed_bullets():
    rule = ListRule()

    tf = FakeTextFrame(
        paragraphs=[
            FakeParagraph(text="one", bullet_type="auto"),
            FakeParagraph(text="two", bullet_type="none"),
            FakeParagraph(text="three", bullet_type="auto"),
        ]
    )

    assert rule._has_mixed_bullets(tf) is True


def test_run_reports_single_item_and_mixed_list():
    rule = ListRule()

    shape_one = FakeShape(
        text_frame=FakeTextFrame(paragraphs=[FakeParagraph(text="one", bullet_type="auto")])
    )
    shape_mixed = FakeShape(
        text_frame=FakeTextFrame(
            paragraphs=[
                FakeParagraph(text="one", bullet_type="auto"),
                FakeParagraph(text="two", bullet_type="none"),
                FakeParagraph(text="three", bullet_type="auto"),
            ]
        )
    )
    slide = FakeSlide([shape_one, shape_mixed])

    issues = rule.run(type("Pres", (), {"slides": [slide]})())
    messages = [it.message for it in issues]

    assert any("на слайде 2 списка" in msg for msg in messages)
    assert any("список с перемешанными маркерами" in msg for msg in messages)
