from pathlib import Path
from .dev_quality_facade import evidence_bundle
def export_stabilization_evidence_bundle(files: list[Path], out: Path): return evidence_bundle(files, out)
