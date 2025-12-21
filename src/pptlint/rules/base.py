from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class Issue:
    category: str
    message: str
    slide: int | None = None
    rule: str = ""


class Rule(ABC):
    category: str = "General"
    name: str = ""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def run(self, pres: object) -> list[Issue]:
        raise NotImplementedError

    def _issue(self, message: str, slide: int | None = None) -> Issue:
        return Issue(
            category=self.category,
            message=message,
            slide=slide,
            rule=self.__class__.__name__,
        )
