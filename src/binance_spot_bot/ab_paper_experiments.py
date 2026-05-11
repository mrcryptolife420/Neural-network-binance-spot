from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .paper_experiment_split import split_assignment
from .paper_policy_rollout import RolloutPlan
from .redaction import redact_payload


def run_ab_paper_experiment(plan: RolloutPlan, observations: list[dict[str, Any]], *, seed: int = 7) -> dict[str, Any]:
    rows = []
    for row in observations:
        variant = row.get("variant") or split_assignment(str(row.get("symbol", "")), plan.allocation_split, seed=seed)
        rows.append({**row, "variant": variant})
    metrics = {}
    for variant in {"champion", "challenger"}:
        selected = [row for row in rows if row["variant"] == variant]
        pnl = sum(float(row.get("pnl", 0.0)) for row in selected)
        drawdown = max([float(row.get("drawdown", 0.0)) for row in selected] or [0.0])
        metrics[variant] = {
            "observations": len(selected),
            "pnl": round(pnl, 6),
            "drawdown": round(drawdown, 6),
            "risk_adjusted_return": round(pnl / (1.0 + drawdown), 6),
            "trade_count": sum(int(row.get("trades", 1)) for row in selected),
            "policy_violations": sum(int(bool(row.get("policy_violation", False))) for row in selected),
        }
    decision = "challenger_leads" if metrics["challenger"]["risk_adjusted_return"] > metrics["champion"]["risk_adjusted_return"] else "champion_leads"
    return {"status": "evaluated", "rollout_id": plan.rollout_id, "metrics": metrics, "decision": decision, "live_trading_enabled": False}


def write_ab_experiment_report(root: Path, report: dict[str, Any]) -> Path:
    out = root / "policy-governance" / "ab-experiments"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{report['rollout_id']}.json"
    path.write_text(json.dumps(redact_payload(report), indent=2, default=str), encoding="utf-8")
    return path
