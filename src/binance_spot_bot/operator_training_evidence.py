from pathlib import Path
from .dev_quality_facade import evidence_bundle
def export_operator_training_evidence(files: list[Path], out: Path): return evidence_bundle(files, out)
