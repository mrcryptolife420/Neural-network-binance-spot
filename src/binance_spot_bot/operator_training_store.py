from pathlib import Path
from .model_ops_facade import write_model_ops_report
def write_operator_training_store(root: Path, payload: dict): return write_model_ops_report(root, "operator-training-store", payload)
