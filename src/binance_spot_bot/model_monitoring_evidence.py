from pathlib import Path
from .model_ops_facade import export_model_ops_evidence
def export_model_monitoring_evidence(files: list[Path], out: Path): return export_model_ops_evidence(files, out)
