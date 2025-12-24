import argparse
import sys
from pathlib import Path


def _bootstrap_import_path() -> None:
    if __package__:
        return

    this_file = Path(__file__).resolve()
    pkg_dir = this_file.parent
    project_root = pkg_dir.parent

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


_bootstrap_import_path()

from pptlint.loader import load_presentation
from pptlint.analyzer import PresentationAnalyzer
from pptlint.report import print_report, write_markdown_report

def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="pptlint",
        description="PowerPoint Lint: проверка .pptx на типовые ошибки оформления",
    )
    p.add_argument("pptx", help="Путь к .pptx презентации")
    p.add_argument(
        "--report",
        metavar="PATH",
        help="Сохранить отчёт в Markdown по указанному пути (например, report.md)",
    )
    return p.parse_args(argv)

def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    pptx_path = Path(args.pptx)
    report_path = str(Path(args.report)) if args.report else None

    try:
        pres = load_presentation(pptx_path)
        analyzer = PresentationAnalyzer()
        issues = analyzer.analyze(pres)

        print(f"Файл: {pptx_path}\n")
        print_report(issues)

        if report_path:
            write_markdown_report(issues, report_path)
            print(f"\nMarkdown-отчёт сохранён: {report_path}")

        return 0
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
