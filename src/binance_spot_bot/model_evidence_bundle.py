from pathlib import Path
from .model_ops_facade import export_model_ops_evidence
def export_model_evidence_bundle(files: list[Path], out: Path): return export_model_ops_evidence(files, out)
