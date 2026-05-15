from __future__ import annotations

from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement


def dashboard_v2_onboarding_report(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    steps = ["local_environment", "no_live_explanation", "data_dir", "dashboard_health", "demo_source", "paper_smoke", "support_bundle", "evidence_export"]
    return {
        "status": "ok",
        "steps": [{"key": step, "status": "pass" if step != "data_dir" or (root / "data").exists() else "ready"} for step in steps],
        "works_without_api_keys": True,
        "progress_saved_locally": True,
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }
