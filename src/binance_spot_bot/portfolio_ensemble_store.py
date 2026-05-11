from pathlib import Path
from .dev_quality_facade import write_dev_report
def write_portfolio_ensemble_store(root: Path, payload: dict): return write_dev_report(root, "portfolio-ensemble-store", payload)
