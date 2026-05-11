from pathlib import Path
from binance_spot_bot.dev_quality_facade import evidence_bundle
def live_governance_evidence(files: list[Path], out: Path): return evidence_bundle(files, out)
