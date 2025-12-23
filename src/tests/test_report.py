from pptlint.report import (
    _group_and_sort,
    _sorted_categories,
    _render_markdown,
    print_report,
)
from pptlint.rules.base import Issue


def test_group_and_sort_orders_by_slide_then_message():
    issues = [
        Issue(category="Шрифты", message="b", slide=2),
        Issue(category="Шрифты", message="a", slide=2),
        Issue(category="Шрифты", message="c", slide=1),
    ]

    grouped = _group_and_sort(issues)

    msgs = [it.message for it in grouped["Шрифты"]]
    assert msgs == ["c", "a", "b"]


def test_sorted_categories_respects_order():
    categories = ["Стиль заголовков", "Шрифты", "Нумерация слайдов"]

    sorted_cats = _sorted_categories(categories)

    assert sorted_cats == ["Шрифты", "Нумерация слайдов", "Стиль заголовков"]


def test_render_markdown_empty():
    md = _render_markdown([])
    assert "Проблем не найдено" in md


def test_print_report_output(capsys):
    issues = [
        Issue(category="Шрифты", message="разные шрифты", slide=2),
        Issue(category="Списки", message="список из 1 пункта", slide=1),
    ]

    print_report(issues)
    out = capsys.readouterr().out

    assert "[Списки]" in out
    assert "[Шрифты]" in out
    assert "Слайд 1: список из 1 пункта" in out
    assert "Слайд 2: разные шрифты" in out
