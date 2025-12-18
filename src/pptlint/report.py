from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
import sys
from .rules.base import Issue


_CATEGORY_ORDER: List[str] = [
    "Списки",
    "Шрифты",
    "Нумерация слайдов",
    "Перегруженность текстом",
    "Стиль заголовков",
]


def print_report(issues: List[Issue]) -> None:

    out = sys.stdout

    if not issues:
        out.write("Проблем не найдено.\n")
        return

    grouped = _group_and_sort(issues)

    for category in _sorted_categories(grouped.keys()):
        items = grouped.get(category, [])
        if not items:
            continue

        out.write(f"\n[{category}]\n")
        for it in items:
            out.write(f"- {_format_issue_console(it)}\n")

    out.write("\n")


def write_markdown_report(issues: List[Issue], path: str | Path) -> None:
    md = _render_markdown(issues)

    p = Path(path)
    if p.parent and not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(md, encoding="utf-8")


def _group_and_sort(issues: Sequence[Issue]) -> Dict[str, List[Issue]]:
    grouped: Dict[str, List[Issue]] = {}
    for it in issues:
        cat = it.category
        grouped.setdefault(cat, []).append(it)

    for cat, items in grouped.items():
        items.sort(key=lambda x: (_slide_sort_key(x.slide), x.message.lower()))
    return grouped


def _sorted_categories(categories: Iterable[str]) -> List[str]:
    cats = list(categories)
    order_index = {c: i for i, c in enumerate(_CATEGORY_ORDER)}
    return sorted(
        cats,
        key=lambda c: (order_index.get(c), c.lower()),
    )


def _slide_sort_key(slide: Optional[int]) -> Tuple[int, int]:
    if slide is None:
        return (1, 0)
    return (0, slide)


def _format_issue_console(issue: Issue) -> str:
    if issue.slide is None:
        return issue.message
    return f"Слайд {issue.slide}: {issue.message}"


def _render_markdown(issues: Sequence[Issue]) -> str:
    if not issues:
        return "# Отчёт PowerPoint Lint\n\nПроблем не найдено.\n"

    grouped = _group_and_sort(issues)

    lines: List[str] = []
    lines.append("# Отчёт PowerPoint Lint\n")

    for category in _sorted_categories(grouped.keys()):
        items = grouped.get(category, [])
        if not items:
            continue

        lines.append(f"## {category}\n")
        for it in items:
            if it.slide is None:
                lines.append(f"- {it.message}")
            else:
                lines.append(f"- **Слайд {it.slide}:** {it.message}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
