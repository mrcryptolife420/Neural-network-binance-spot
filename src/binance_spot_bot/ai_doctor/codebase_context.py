from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write


def collect_codebase_context(root: Path, run_id: str, errors: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    suspect = sorted({error.get("file", "") for error in (errors or []) if error.get("file")})
    if not suspect:
        suspect = ["src/binance_spot_bot/cli.py", "src/binance_spot_bot/dashboard_v2/app.py"]
    context = {"git_ref": "local", "changed_files": [], "suspect_files": suspect, "recommended_tests": ["pytest -q tests/test_roadmap_123_ai_doctor_acceptance.py"], "live_trading_enabled": False}
    saved = json_write(root / "data" / "ai-doctor" / "runs" / run_id / "codebase_context" / "suspect_files.json", context)
    return {"status": "ok", "context": context, "saved": saved}

