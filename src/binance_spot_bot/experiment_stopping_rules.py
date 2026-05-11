from __future__ import annotations

from typing import Any


def evaluate_stopping_rules(report: dict[str, Any], *, max_drawdown: float = 25.0, min_samples: int = 10) -> dict[str, Any]:
    challenger = report.get("metrics", {}).get("challenger", {})
    champion = report.get("metrics", {}).get("champion", {})
    reasons = []
    if float(challenger.get("drawdown", 0.0)) > max_drawdown:
        reasons.append("challenger_max_drawdown")
    if float(challenger.get("risk_adjusted_return", 0.0)) < float(champion.get("risk_adjusted_return", 0.0)) * 0.8:
        reasons.append("challenger_underperforms")
    if int(challenger.get("observations", 0)) < min_samples:
        reasons.append("too_few_samples")
    if int(challenger.get("policy_violations", 0)) > 0:
        reasons.append("policy_violation")
    action = "pause_challenger" if reasons else "continue"
    return {"status": "stop" if reasons else "continue", "action": action, "reasons": reasons, "live_trading_enabled": False}
