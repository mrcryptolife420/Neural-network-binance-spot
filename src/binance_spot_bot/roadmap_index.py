from pathlib import Path
from .dev_quality_facade import roadmap_index
def build_roadmap_index(root: Path): return roadmap_index(root / "Roadmap docs", root / "Voltooid docs")
