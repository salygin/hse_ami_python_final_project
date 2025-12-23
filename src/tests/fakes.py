from typing import Iterable


class FakeSize:
    def __init__(self, pt: float | None):
        self.pt = pt


class FakeFont:
    def __init__(self, name: str | None = None, size: FakeSize | None = None, bold: bool | None = None):
        self.name = name
        self.size = size
        self.bold = bold


class FakeRun:
    def __init__(self, font: FakeFont | None = None):
        self.font = font or FakeFont()


class FakePPr:
    def __init__(self, bullet_type: str | None = None):
        self.bullet_type = bullet_type

    def find(self, key):
        if self.bullet_type is None:
            return None

        key_str = str(key)
        mapping = {
            "none": "buNone",
            "auto": "buAutoNum",
            "char": "buChar",
            "blip": "buBlip",
            "font": "buFont",
        }
        target = mapping.get(self.bullet_type)
        if target and key_str.endswith(target):
            return object()
        return None


class FakeP:
    def __init__(self, pPr: FakePPr):
        self.pPr = pPr


class FakeParagraph:
    def __init__(
        self,
        text: str = "",
        runs: list[FakeRun] | None = None,
        font: FakeFont | None = None,
        bullet_type: str | None = None,
    ):
        self.text = text
        self.runs = runs or []
        self.font = font or FakeFont()
        self._p = FakeP(FakePPr(bullet_type)) if bullet_type is not None else None


class FakeTextFrame:
    def __init__(self, text: str = "", paragraphs: list[FakeParagraph] | None = None):
        self.text = text
        self.paragraphs = paragraphs or []


class FakeShape:
    def __init__(
        self,
        text_frame: FakeTextFrame | None = None,
        shapes: list["FakeShape"] | None = None,
        shape_type: int | None = None,
        name: str = "",
        is_placeholder: bool = False,
        placeholder_type: int | None = None,
        top: int = 0,
        height: int = 0,
    ):
        self.text_frame = text_frame
        self.has_text_frame = text_frame is not None
        self.shapes = shapes
        self.shape_type = shape_type
        self.name = name
        self.is_placeholder = is_placeholder
        self.placeholder_format = type("Placeholder", (), {"type": placeholder_type})() if placeholder_type else None
        self.top = top
        self.height = height


class FakeShapesCollection:
    def __init__(self, shapes: Iterable[FakeShape], title: FakeShape | None = None):
        self._shapes = list(shapes)
        self.title = title

    def __iter__(self):
        return iter(self._shapes)


class FakeSlide:
    def __init__(self, shapes: Iterable[FakeShape], title: FakeShape | None = None):
        self.shapes = FakeShapesCollection(shapes, title=title)


class FakePresentation:
    def __init__(self, slides: list[FakeSlide], slide_height: int = 0):
        self.slides = slides
        self.slide_height = slide_height
