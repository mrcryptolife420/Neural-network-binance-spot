from pathlib import Path
from .dev_quality_facade import evidence_bundle
def export_portfolio_ensemble_evidence(files: list[Path], out: Path): return evidence_bundle(files, out)
