from __future__ import annotations

import json
import statistics
import time
from dataclasses import asdict, dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any

from .config import BotSettings
from .redaction import redact_payload


@dataclass(frozen=True)
class PaperDeploymentPlan:
    deployment_id: str
    strategy_id: str
    model_alias: str
    symbols: list[str]
    risk_preset: str
    version_lock: str
    status: str = "planned"
    rollback_preset: str = "conservative"
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class PaperEvaluation:
    status: str
    deployment_id: str
    pnl: Decimal
    drawdown: Decimal
    trades: int
    drift_score: float
    watchdog_status: str
    rollback_required: bool
    reasons: list[str]
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


class PaperDeploymentStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save_plan(self, plan: PaperDeploymentPlan) -> Path:
        path = self.root / f"{plan.deployment_id}.json"
        path.write_text(json.dumps(plan.to_dict(), indent=2, default=str), encoding="utf-8")
        (self.root / "latest-plan.json").write_text(json.dumps(plan.to_dict(), indent=2, default=str), encoding="utf-8")
        return path

    def load_plan(self, deployment_id: str) -> PaperDeploymentPlan:
        payload = json.loads((self.root / f"{deployment_id}.json").read_text(encoding="utf-8"))
        return PaperDeploymentPlan(**{key: payload[key] for key in PaperDeploymentPlan.__dataclass_fields__ if key in payload})

    def save_evaluation(self, evaluation: PaperEvaluation) -> Path:
        path = self.root / f"{evaluation.deployment_id}-evaluation.json"
        path.write_text(json.dumps(evaluation.to_dict(), indent=2, default=str), encoding="utf-8")
        (self.root / "latest-evaluation.json").write_text(json.dumps(evaluation.to_dict(), indent=2, default=str), encoding="utf-8")
        return path


def create_paper_deployment_plan(
    settings: BotSettings,
    strategy_id: str,
    model_alias: str,
    symbols: list[str],
    *,
    risk_preset: str = "balanced",
    calibration_gate: dict[str, Any] | None = None,
) -> PaperDeploymentPlan:
    gate = calibration_gate or {"status": "paper_approved"}
    status = "planned" if gate.get("status") in {"paper_approved", "approved"} and not settings.live_trading_enabled else "blocked"
    normalized = [symbol.strip().upper() for symbol in symbols if symbol.strip()]
    deployment_id = f"paper-{strategy_id}-{int(time.time() * 1000)}"
    return PaperDeploymentPlan(
        deployment_id=deployment_id,
        strategy_id=strategy_id,
        model_alias=model_alias,
        symbols=normalized,
        risk_preset=risk_preset,
        version_lock=f"{strategy_id}:{model_alias}:{risk_preset}",
        status=status,
        live_trading_enabled=False,
    )


def evaluate_paper_deployment(
    plan: PaperDeploymentPlan,
    observations: list[dict[str, Any]],
    *,
    expected_pnl: Decimal = Decimal("0"),
    max_drawdown: Decimal = Decimal("25"),
    drift_threshold: float = 0.20,
) -> PaperEvaluation:
    pnl = sum(Decimal(str(row.get("pnl", "0"))) for row in observations)
    equity = Decimal("1000")
    peak = equity
    drawdown = Decimal("0")
    confidences = []
    for row in observations:
        equity += Decimal(str(row.get("pnl", "0")))
        peak = max(peak, equity)
        drawdown = max(drawdown, peak - equity)
        if "confidence" in row:
            confidences.append(float(row["confidence"]))
    avg_conf = statistics.mean(confidences) if confidences else 0.5
    drift = abs(avg_conf - 0.5)
    reasons = []
    if pnl < expected_pnl:
        reasons.append("pnl_below_expectation")
    if drawdown > max_drawdown:
        reasons.append("drawdown_limit_breached")
    if drift > drift_threshold:
        reasons.append("confidence_drift")
    rollback = bool(reasons)
    return PaperEvaluation(
        status="rollback" if rollback else "healthy",
        deployment_id=plan.deployment_id,
        pnl=pnl,
        drawdown=drawdown,
        trades=len(observations),
        drift_score=round(drift, 4),
        watchdog_status="triggered" if rollback else "clear",
        rollback_required=rollback,
        reasons=reasons,
    )


def rollback_plan(plan: PaperDeploymentPlan, evaluation: PaperEvaluation) -> dict[str, Any]:
    return {
        "deployment_id": plan.deployment_id,
        "status": "rollback_required" if evaluation.rollback_required else "no_rollback",
        "target_preset": plan.rollback_preset,
        "safe_mode": "paper_only",
        "reasons": evaluation.reasons,
        "live_trading_enabled": False,
    }


def write_daily_strategy_report(settings: BotSettings, plan: PaperDeploymentPlan, evaluation: PaperEvaluation) -> dict[str, str]:
    out = settings.data_dir / "paper-deployments" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    payload = {"plan": plan.to_dict(), "evaluation": evaluation.to_dict(), "rollback": rollback_plan(plan, evaluation)}
    json_path = out / f"{plan.deployment_id}-daily-report.json"
    md_path = out / f"{plan.deployment_id}-daily-report.md"
    json_path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# Paper Strategy Daily Report",
                "",
                f"Deployment: {plan.deployment_id}",
                f"Status: {evaluation.status}",
                f"PnL: {evaluation.pnl}",
                f"Drawdown: {evaluation.drawdown}",
                f"Rollback required: {evaluation.rollback_required}",
                "Live trading: disabled",
            ]
        ),
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}


def run_paper_deployment_cycle(
    settings: BotSettings,
    strategy_id: str,
    model_alias: str,
    symbols: list[str],
    observations: list[dict[str, Any]],
    *,
    calibration_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    store = PaperDeploymentStore(settings.data_dir / "paper-deployments")
    plan = create_paper_deployment_plan(settings, strategy_id, model_alias, symbols, calibration_gate=calibration_gate)
    store.save_plan(plan)
    evaluation = evaluate_paper_deployment(plan, observations)
    store.save_evaluation(evaluation)
    reports = write_daily_strategy_report(settings, plan, evaluation)
    return {"plan": plan.to_dict(), "evaluation": evaluation.to_dict(), "rollback": rollback_plan(plan, evaluation), "reports": reports}
