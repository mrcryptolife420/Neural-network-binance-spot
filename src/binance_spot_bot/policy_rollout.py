from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .config import BotSettings
from .redaction import redact_payload


@dataclass(frozen=True)
class PaperPolicyVariant:
    policy_id: str
    model_alias: str
    risk_preset: str
    max_symbols: int
    allocation_cap_pct: float


@dataclass(frozen=True)
class PaperPolicyExperiment:
    experiment_id: str
    champion: PaperPolicyVariant
    challenger: PaperPolicyVariant
    symbols: list[str]
    traffic_split_pct: int = 20
    min_observations: int = 30
    max_drawdown_quote: float = 25.0
    status: str = "paper_running"
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def assign_ab_bucket(symbol: str, experiment_id: str, split_pct: int) -> str:
    bucket = sum(ord(char) for char in f"{experiment_id}:{symbol.upper()}") % 100
    return "challenger" if bucket < max(0, min(100, split_pct)) else "champion"


def create_policy_experiment(
    champion: PaperPolicyVariant,
    challenger: PaperPolicyVariant,
    symbols: list[str],
    *,
    traffic_split_pct: int = 20,
    min_observations: int = 30,
) -> PaperPolicyExperiment:
    normalized = sorted({symbol.strip().upper() for symbol in symbols if symbol.strip()})
    return PaperPolicyExperiment(
        experiment_id=f"paper-policy-{int(time.time() * 1000)}",
        champion=champion,
        challenger=challenger,
        symbols=normalized,
        traffic_split_pct=traffic_split_pct,
        min_observations=min_observations,
    )


def evaluate_champion_challenger(experiment: PaperPolicyExperiment, observations: list[dict[str, Any]]) -> dict[str, Any]:
    grouped = {"champion": [], "challenger": []}
    for row in observations:
        variant = str(row.get("variant") or assign_ab_bucket(str(row.get("symbol", "")), experiment.experiment_id, experiment.traffic_split_pct))
        if variant in grouped:
            grouped[variant].append(row)
    metrics = {name: _variant_metrics(rows) for name, rows in grouped.items()}
    blockers = []
    for name, row in metrics.items():
        if row["drawdown_quote"] > experiment.max_drawdown_quote:
            blockers.append(f"{name}_drawdown_limit")
    challenger_ready = metrics["challenger"]["observations"] >= experiment.min_observations and not blockers
    challenger_better = metrics["challenger"]["score"] > metrics["champion"]["score"]
    decision = "promote_challenger" if challenger_ready and challenger_better else "keep_champion"
    if blockers:
        decision = "rollback_challenger"
    return {
        "status": "blocked" if blockers else "evaluated",
        "experiment_id": experiment.experiment_id,
        "metrics": metrics,
        "decision": decision,
        "blockers": blockers,
        "live_trading_enabled": False,
    }


def policy_rollout_report(settings: BotSettings, experiment: PaperPolicyExperiment, evaluation: dict[str, Any]) -> dict[str, Any]:
    out = settings.data_dir / "paper-policy-rollouts"
    out.mkdir(parents=True, exist_ok=True)
    assignments = [
        {"symbol": symbol, "variant": assign_ab_bucket(symbol, experiment.experiment_id, experiment.traffic_split_pct)}
        for symbol in experiment.symbols
    ]
    payload = {"experiment": experiment.to_dict(), "assignments": assignments, "evaluation": evaluation}
    json_path = out / f"{experiment.experiment_id}.json"
    md_path = out / f"{experiment.experiment_id}.md"
    latest = out / "latest-policy-rollout.json"
    safe_payload = redact_payload(payload)
    json_path.write_text(json.dumps(safe_payload, indent=2, default=str), encoding="utf-8")
    latest.write_text(json.dumps(safe_payload, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# Paper Policy Rollout",
                "",
                f"Experiment: {experiment.experiment_id}",
                f"Status: {evaluation['status']}",
                f"Decision: {evaluation['decision']}",
                f"Traffic split: {experiment.traffic_split_pct}%",
                "Live trading: disabled",
            ]
        ),
        encoding="utf-8",
    )
    return {"path": str(json_path), "latest": str(latest), "markdown": str(md_path), **safe_payload}


def run_policy_rollout(settings: BotSettings, symbols: list[str]) -> dict[str, Any]:
    experiment = create_policy_experiment(
        PaperPolicyVariant("champion-balanced", "champion", "balanced", 3, 0.35),
        PaperPolicyVariant("challenger-conservative", "candidate", "conservative", 4, 0.25),
        symbols,
        min_observations=3,
    )
    observations = [
        {"symbol": symbol, "variant": assign_ab_bucket(symbol, experiment.experiment_id, experiment.traffic_split_pct), "pnl": "0.7", "drawdown": "0.2"}
        for symbol in experiment.symbols
    ]
    evaluation = evaluate_champion_challenger(experiment, observations)
    return policy_rollout_report(settings, experiment, evaluation)


def _variant_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    pnl = sum(float(row.get("pnl", 0.0)) for row in rows)
    drawdown = max([float(row.get("drawdown", 0.0)) for row in rows] or [0.0])
    trades = sum(int(row.get("trades", 1)) for row in rows)
    return {
        "observations": len(rows),
        "pnl_quote": round(pnl, 6),
        "drawdown_quote": round(drawdown, 6),
        "trades": trades,
        "score": round(pnl - drawdown * 0.5, 6),
    }
