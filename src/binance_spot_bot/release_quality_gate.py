from __future__ import annotations

from typing import Any


def release_quality_gate(results: list[dict]) -> dict[str, Any]:
    hard = [row for row in results if row.get("required", True) and row.get("status") not in {"ok", "pass", "ready", "warning"}]
    warnings = [row for row in results if row.get("status") == "warning"]
    return {"status": "fail" if hard else ("warn" if warnings else "ok"), "hard_blockers": hard, "warnings": warnings, "live_trading_enabled": False}
