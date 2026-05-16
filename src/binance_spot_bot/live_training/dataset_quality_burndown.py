from __future__ import annotations

from typing import Any


def build_dataset_quality_burndown(vault_report: dict[str, Any], target_report: dict[str, Any]) -> dict[str, Any]:
    issues = []
    for item in target_report.get("missing_targets", []):
        issues.append({"issue_id": f"dq-{item}", "category": item, "priority": "DQ-P1", "status": "open"})
    for blocker in vault_report.get("manifest", {}).get("blockers", []):
        issues.append({"issue_id": f"dq-p0-{len(issues)}", "category": blocker, "priority": "DQ-P0", "status": "open"})
    if target_report.get("missing_market_regimes"):
        issues.append({"issue_id": "dq-market-regimes", "category": "too few market regimes", "priority": "DQ-P2", "status": "open"})
    return {"status": "blocked" if any(item["priority"] == "DQ-P0" for item in issues) else ("warn" if issues else "ok"), "issues": issues, "live_trading_enabled": False}

