from typing import List
from .rules.base import Issue
from pathlib import Path

def print_report(issues: List[Issue]) -> None:
    pass

def write_markdown_report(issues: List[Issue], path: str | Path) -> None:
    pass
