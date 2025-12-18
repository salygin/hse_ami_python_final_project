from pathlib import Path
from pptx import Presentation

class PresentationLoadError(Exception):
    pass

def load_presentation(p: Path) -> Presentation:
    pass