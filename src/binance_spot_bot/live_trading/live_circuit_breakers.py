from __future__ import annotations


def evaluate_live_circuit_breakers(findings: list[str]) -> dict[str, object]:
    action = "ok"
    if any(item in findings for item in {"unknown_order", "reconciliation", "loss", "stale_data", "connectivity"}):
        action = "disarm"
    elif findings:
        action = "warn"
    return {"status": action, "action": action, "findings": findings, "live_trading_enabled": False}
