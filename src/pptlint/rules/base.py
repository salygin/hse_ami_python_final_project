from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass(frozen=True)
class Issue:
    category: str
    message: str
    slide: Optional[int] = None
    rule: str = ""


class Rule(ABC):
    category: str = "General"
    name: str = ""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def run(self, pres: Any) -> List[Issue]:
        raise NotImplementedError

    def _issue(self, message: str, slide: Optional[int] = None) -> Issue:
        return Issue(
            category=self.category,
            message=message,
            slide=slide,
            rule=self.self.__class__.__name__,
        )
