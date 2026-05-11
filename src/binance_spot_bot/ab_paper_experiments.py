from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .paper_experiment_split import split_assignment
from .paper_policy_rollout import RolloutPlan
from .redaction import redact_payload

EXPERIMENT_TYPES = {"champion_challenger", "parameter_sweep", "symbol_basket", "time_slice", "canary"}


def run_ab_paper_experiment(
    plan: RolloutPlan,
    observations: list[dict[str, Any]],
    *,
    seed: int = 7,
    experiment_type: str = "champion_challenger",
) -> dict[str, Any]:
    if experiment_type not in EXPERIMENT_TYPES:
        raise ValueError("invalid experiment_type")
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(observations):
        variant = row.get("variant") or split_assignment(str(row.get("symbol", "")), plan.alloc_split, seed=seed, bucket_key=str(index))
        rows.append({**row, "variant": variant, "signed_endpoint_used": False})
    metrics = {variant: _variant_metrics(rows, variant) for variant in ("champion", "challenger")}
    decision = "challenger_leads" if metrics["challenger"]["risk_adjusted_ret"] > metrics["champion"]["risk_adjusted_ret"] else "champion_leads"
    report = {
        "status": "evaluated",
        "experiment_id": f"ab-{plan.rollout_id}-{seed}",
        "experiment_type": experiment_type,
        "rollout_id": plan.rollout_id,
        "seed": seed,
        "metrics": metrics,
        "decision": decision,
        "rows": rows,
        "guardrails": {
            "paper_only": True,
            "signed_endpoint_used": any(bool(row.get("signed_endpoint_used")) for row in rows),
            "account_endpoint_used": False,
        },
        "live_trading_enabled": False,
    }
    return redact_payload(report)


def write_ab_experiment_report(root: Path, report: dict[str, Any]) -> Path:
    out = root / "policy-governance" / "ab-experiments"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{report['experiment_id']}.json"
    path.write_text(json.dumps(redact_payload(report), indent=2, default=str), encoding="utf-8")
    return path


def _variant_metrics(rows: list[dict[str, Any]], variant: str) -> dict[str, Any]:
    selected = [row for row in rows if row.get("variant") == variant]
    pnl = sum(float(row.get("pnl", 0.0)) for row in selected)
    drawdown = max([float(row.get("drawdown", 0.0)) for row in selected] or [0.0])
    fees = sum(float(row.get("fees", 0.0)) for row in selected)
    slippage = sum(float(row.get("slippage", 0.0)) for row in selected)
    turnover = sum(float(row.get("turnover", 0.0)) for row in selected)
    trades = sum(int(row.get("trades", 1)) for row in selected)
    blocked = sum(int(bool(row.get("blocked", False))) for row in selected)
    conflicts = sum(int(bool(row.get("conflict", False))) for row in selected)
    data_warnings = sum(int(bool(row.get("data_quality_warning", False))) for row in selected)
    liquidity_penalty = sum(float(row.get("liquidity_penalty", 0.0)) for row in selected)
    rotation_churn = sum(float(row.get("rotation_churn", 0.0)) for row in selected)
    watchdog_alerts = sum(int(bool(row.get("watchdog_alert", False))) for row in selected)
    policy_violations = sum(int(bool(row.get("policy_violation", False))) for row in selected)
    net_pnl = pnl - fees - slippage - liquidity_penalty
    return {
        "observations": len(selected),
        "pnl": round(pnl, 6),
        "net_pnl": round(net_pnl, 6),
        "drawdown": round(drawdown, 6),
        "risk_adjusted_ret": round(net_pnl / (1.0 + drawdown), 6),
        "trade_count": trades,
        "blocked_rate": round(blocked / max(1, trades), 6),
        "conflict_rate": round(conflicts / max(1, trades), 6),
        "data_quality_warnings": data_warnings,
        "liquidity_penalty": round(liquidity_penalty, 6),
        "turnover": round(turnover, 6),
        "rotation_churn": round(rotation_churn, 6),
        "watchdog_alerts": watchdog_alerts,
        "policy_violations": policy_violations,
        "last_updated_ms": int(time.time() * 1000),
    }
