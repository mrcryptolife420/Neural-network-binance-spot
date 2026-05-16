from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import has_advice_wording, json_write, now_ms, redact_value, stable_hash, status_from_blockers

from . import NO_UNATTENDED_LIVE_STATEMENT, NOT_FINANCIAL_ADVICE_STATEMENT


@dataclass(frozen=True)
class LiveSessionEvidenceRefs:
    roadmap_117_evidence: str = "demo-to-live-evidence-fixture"
    roadmap_118_evidence: str = "live-execution-evidence-fixture"


@dataclass(frozen=True)
class LiveSessionBudget:
    max_session_orders: int = 2
    max_session_quote_exposure: float = 15.0
    max_single_order_quote: float = 5.0
    max_session_loss_quote: float = 2.0
    max_daily_loss_quote: float = 5.0
    max_session_duration_minutes: int = 15


@dataclass(frozen=True)
class LiveSessionSymbolScope:
    symbol: str = "BTCUSDT"
    allowed_sides: list[str] = field(default_factory=lambda: ["BUY", "SELL"])
    allowed_order_types: list[str] = field(default_factory=lambda: ["MARKET", "LIMIT"])


@dataclass(frozen=True)
class LiveSessionRiskScope:
    max_spread_bps: float = 25.0
    max_data_age_ms: int = 30_000
    max_open_orders: int = 1
    require_preview_hash: bool = True
    require_arm_token: bool = True
    require_reconciliation_after_each_order: bool = True
    require_kill_switch_drill: bool = True
    require_cancel_drill: bool = True


@dataclass(frozen=True)
class LiveSessionPlan:
    session_plan_id: str = "controlled-live-session-fixture"
    profile_id: str = "live-locked-training-required-template"
    symbol_scope: LiveSessionSymbolScope = field(default_factory=LiveSessionSymbolScope)
    budget: LiveSessionBudget = field(default_factory=LiveSessionBudget)
    risk: LiveSessionRiskScope = field(default_factory=LiveSessionRiskScope)
    evidence_refs: LiveSessionEvidenceRefs = field(default_factory=LiveSessionEvidenceRefs)
    no_unattended_live_statement: str = NO_UNATTENDED_LIVE_STATEMENT
    not_financial_advice_statement: str = NOT_FINANCIAL_ADVICE_STATEMENT
    created_at_ms: int = field(default_factory=now_ms)
    expires_at_ms: int = field(default_factory=lambda: now_ms() + 900_000)


def validate_live_session_plan(plan: LiveSessionPlan | dict[str, Any]) -> dict[str, Any]:
    payload = asdict(plan) if isinstance(plan, LiveSessionPlan) else dict(plan)
    payload = redact_value(payload)
    blockers: list[str] = []
    warnings: list[str] = []
    refs = payload.get("evidence_refs", {})
    budget = payload.get("budget", {})
    risk = payload.get("risk", {})
    symbol_scope = payload.get("symbol_scope", {})
    if not refs.get("roadmap_117_evidence"):
        blockers.append("missing Roadmap 117 evidence ref")
    if not refs.get("roadmap_118_evidence"):
        blockers.append("missing Roadmap 118 evidence ref")
    for key in ["max_session_orders", "max_session_quote_exposure", "max_single_order_quote", "max_session_loss_quote", "max_session_duration_minutes"]:
        if float(budget.get(key, 0)) <= 0:
            blockers.append(f"invalid budget: {key}")
    if not risk.get("require_preview_hash"):
        blockers.append("preview hash requirement missing")
    if not risk.get("require_arm_token"):
        blockers.append("arm token requirement missing")
    if not risk.get("require_reconciliation_after_each_order"):
        blockers.append("reconciliation requirement missing")
    if not symbol_scope.get("symbol"):
        blockers.append("symbol required")
    unsafe_types = [item for item in symbol_scope.get("allowed_order_types", []) if item not in {"MARKET", "LIMIT"}]
    if unsafe_types:
        blockers.append("unsafe order type")
    advice_payload = dict(payload)
    advice_payload.pop("symbol_scope", None)
    advice_payload.pop("no_unattended_live_statement", None)
    advice_payload.pop("not_financial_advice_statement", None)
    if has_advice_wording(advice_payload):
        blockers.append("advice/profit wording blocked")
    return {"status": status_from_blockers(blockers, warnings), "plan": payload, "plan_hash": stable_hash(payload), "blockers": blockers, "warnings": warnings, "live_trading_enabled": False}


def write_live_session_plan_report(root: Path, report: dict[str, Any]) -> dict[str, Any]:
    return json_write(root / "data" / "live-trading" / "sessions" / "plans" / "live_session_plan_report.json", report)
