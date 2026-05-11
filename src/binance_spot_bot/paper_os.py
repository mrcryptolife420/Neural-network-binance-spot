from __future__ import annotations

import json
import statistics
import time
from dataclasses import asdict, dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any

from .backup_restore import create_backup
from .config import BotSettings
from .indicators import indicator_snapshot
from .redaction import redact_payload
from .types import Candle


ROADMAP_GROUPS: list[tuple[range, str, int]] = [
    (range(76, 78), "data_strategy_foundation", 10),
    (range(78, 83), "paper_deployment_portfolio_governance", 20),
    (range(83, 90), "local_ops_security_recovery_release", 30),
    (range(90, 97), "developer_runtime_data_quality", 40),
    (range(97, 100), "model_monitoring_ensemble_governance", 50),
    (range(100, 103), "paper_os_audit_stabilization_operator_training", 60),
]
NO_LIVE_CONTRACT = {
    "live_trading": "disabled",
    "signed_order_endpoints": "blocked",
    "withdrawals": "blocked",
    "allowed_modes": ["demo", "paper", "testnet-readiness"],
}


@dataclass(frozen=True)
class RoadmapPriority:
    number: int
    path: str
    group: str
    priority: int
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RuntimeEvent:
    event_type: str
    symbol: str
    payload: dict[str, Any]
    timestamp_ms: int = field(default_factory=lambda: int(time.time() * 1000))

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


class RuntimeEventBus:
    def __init__(self, max_events: int = 500):
        self.max_events = max_events
        self._events: list[RuntimeEvent] = []

    def publish(self, event_type: str, symbol: str, payload: dict[str, Any]) -> RuntimeEvent:
        event = RuntimeEvent(event_type, symbol.upper(), _compact_payload(payload))
        self._events.append(event)
        self._events = self._events[-self.max_events :]
        return event

    def drain(self, event_type: str | None = None) -> list[dict[str, Any]]:
        rows = [event.to_dict() for event in self._events if event_type is None or event.event_type == event_type]
        if event_type is not None:
            self._events = [event for event in self._events if event.event_type != event_type]
        return rows


def prioritize_roadmaps(roadmap_dir: Path) -> list[dict[str, Any]]:
    priorities: list[RoadmapPriority] = []
    for path in sorted(roadmap_dir.glob("*.md")):
        number = _roadmap_number(path)
        if number is None:
            continue
        group, base_priority = _roadmap_group(number)
        priorities.append(
            RoadmapPriority(
                number=number,
                path=str(path),
                group=group,
                priority=base_priority + number,
                reason=_priority_reason(group),
            )
        )
    return [item.to_dict() for item in sorted(priorities, key=lambda item: item.priority)]


def build_public_data_warmup_plan(
    symbols: list[str],
    intervals: tuple[str, ...] = ("1m", "5m", "15m", "1h"),
    min_candles: int = 120,
    cache_ttl_seconds: int = 300,
) -> dict[str, Any]:
    rows = []
    for symbol in _unique_symbols(symbols):
        for interval in intervals:
            rows.append(
                {
                    "symbol": symbol,
                    "interval": interval,
                    "endpoint": "/api/v3/klines",
                    "limit": max(30, min(min_candles, 1000)),
                    "read_only": True,
                    "cache_ttl_seconds": cache_ttl_seconds,
                }
            )
    return {
        "status": "ready" if rows else "blocked",
        "rows": rows,
        "checks": {
            "public_only": True,
            "signed_endpoints": False,
            "min_candles": min_candles,
            "cache_enabled": True,
        },
        "next_action": "warm public candles before indicator calculation" if rows else "select symbols",
    }


def indicator_readiness(candles_by_symbol: dict[str, list[Candle]], min_candles: int = 30) -> dict[str, Any]:
    rows = []
    for symbol, candles in sorted(candles_by_symbol.items()):
        snapshot = indicator_snapshot(symbol.upper(), candles)
        regime = snapshot.get("regime") or {}
        if not isinstance(regime, dict):
            regime = {"regime": str(regime), "reason": snapshot.get("regime_reason", "")}
        rows.append(
            {
                "symbol": symbol.upper(),
                "candles": len(candles),
                "ready": len(candles) >= min_candles,
                "profile": snapshot.get("profile", "auto"),
                "regime": regime.get("regime", "unknown"),
                "reason": regime.get("reason", ""),
            }
        )
    blockers = [row for row in rows if not row["ready"]]
    return {
        "status": "ready" if not blockers and rows else "blocked",
        "rows": rows,
        "blockers": blockers,
        "next_action": "collect more public candles" if blockers else "build calibration dataset",
    }


def calibrate_strategy_confidence(candles_by_symbol: dict[str, list[Candle]]) -> dict[str, Any]:
    rows = []
    for symbol, candles in sorted(candles_by_symbol.items()):
        closes = [float(candle.close) for candle in candles]
        if len(closes) < 30:
            rows.append({"symbol": symbol.upper(), "status": "blocked", "reason": "insufficient candles"})
            continue
        returns = [(closes[index] - closes[index - 1]) / closes[index - 1] for index in range(1, len(closes)) if closes[index - 1]]
        volatility = statistics.pstdev(returns) if len(returns) > 1 else 0.0
        trend = (closes[-1] - closes[0]) / closes[0] if closes[0] else 0.0
        confidence = max(0.05, min(0.95, 0.50 + abs(trend) * 3 - volatility * 12))
        rows.append(
            {
                "symbol": symbol.upper(),
                "status": "ready",
                "candles": len(candles),
                "trend": round(trend, 6),
                "volatility": round(volatility, 6),
                "confidence": round(confidence, 4),
                "recommended_threshold": round(max(0.55, min(0.85, confidence + volatility * 4)), 4),
            }
        )
    ready_rows = [row for row in rows if row["status"] == "ready"]
    avg_confidence = statistics.mean(row["confidence"] for row in ready_rows) if ready_rows else 0.0
    return {
        "status": "ready" if ready_rows else "blocked",
        "rows": rows,
        "avg_confidence": round(avg_confidence, 4),
        "promotion_gate": "paper_only" if avg_confidence >= 0.55 else "needs_more_evidence",
        "no_live_contract": NO_LIVE_CONTRACT,
    }


def paper_deployment_control(strategy_id: str, calibration: dict[str, Any]) -> dict[str, Any]:
    approved = calibration.get("promotion_gate") == "paper_only"
    return {
        "strategy_id": strategy_id,
        "status": "approved" if approved else "blocked",
        "mode": "paper",
        "version_lock": f"{strategy_id}:paper-only",
        "rollback_preset": "conservative",
        "watchdog_checks": ["max_drawdown", "confidence_decay", "drift", "stale_data"],
        "auto_rollback": approved,
        "next_action": "start controlled paper deployment" if approved else "collect calibration evidence",
        "no_live_contract": NO_LIVE_CONTRACT,
    }


def portfolio_allocation_policy(symbol_scores: dict[str, float], total_quote_budget: Decimal) -> dict[str, Any]:
    cleaned = {symbol.upper(): max(0.0, float(score)) for symbol, score in symbol_scores.items()}
    total_score = sum(cleaned.values()) or 1.0
    max_symbol_quote = total_quote_budget * Decimal("0.35")
    rows = []
    for symbol, score in sorted(cleaned.items(), key=lambda item: item[1], reverse=True):
        raw = total_quote_budget * Decimal(str(score / total_score))
        allocation = min(raw, max_symbol_quote)
        rows.append(
            {
                "symbol": symbol,
                "score": round(score, 4),
                "quote_allocation": str(allocation.quantize(Decimal("0.01"))),
                "max_open_orders": 2,
                "rotation": "eligible" if score >= 0.55 else "watch",
            }
        )
    return {
        "status": "ready" if rows else "blocked",
        "total_quote_budget": str(total_quote_budget),
        "max_symbol_quote": str(max_symbol_quote.quantize(Decimal("0.01"))),
        "rows": rows,
        "conflict_policy": "highest_score_symbol_strategy_wins_same_symbol_conflicts",
    }


def stress_test_policy(policy: dict[str, Any], shock_bps: int = 250) -> dict[str, Any]:
    rows = []
    for row in policy.get("rows", []):
        allocation = Decimal(str(row.get("quote_allocation", "0")))
        stressed_loss = allocation * Decimal(shock_bps) / Decimal("10000")
        rows.append(
            {
                "symbol": row.get("symbol", ""),
                "shock_bps": shock_bps,
                "stressed_loss_quote": str(stressed_loss.quantize(Decimal("0.01"))),
                "status": "pass" if stressed_loss <= allocation * Decimal("0.05") else "review",
            }
        )
    return {
        "status": "pass" if all(row["status"] == "pass" for row in rows) else "review",
        "scenario": "spread_liquidity_downside",
        "rows": rows,
        "replay_reproducible": True,
    }


def optimize_risk_budget(policy: dict[str, Any], stress_report: dict[str, Any]) -> dict[str, Any]:
    review_symbols = {row["symbol"] for row in stress_report.get("rows", []) if row.get("status") != "pass"}
    rows = []
    for row in policy.get("rows", []):
        symbol = row.get("symbol", "")
        cap = Decimal("0.25") if symbol in review_symbols else Decimal("0.35")
        rows.append({"symbol": symbol, "risk_budget_cap": str(cap), "reason": "stress_review" if symbol in review_symbols else "stable"})
    return {
        "status": "ready",
        "selection": "conservative_robust_allocation",
        "rows": rows,
        "optimizer_guardrail": "do_not_select_highest_pnl_without_stress_pass",
    }


def champion_challenger_governance(champion: str, challenger_scores: dict[str, float]) -> dict[str, Any]:
    ranked = sorted(challenger_scores.items(), key=lambda item: item[1], reverse=True)
    best = ranked[0] if ranked else (champion, 0.0)
    promote = best[0] != champion and best[1] >= max(challenger_scores.get(champion, 0.0), 0.60) + 0.05
    return {
        "champion": champion,
        "challengers": [{"strategy": name, "score": round(score, 4)} for name, score in ranked],
        "decision": "promote_challenger_paper_only" if promote else "keep_champion",
        "requires_operator_approval": promote,
        "ab_experiment_mode": "paper_only",
    }


def local_ops_job_plan() -> dict[str, Any]:
    return {
        "status": "ready",
        "jobs": [
            {"name": "daily_paper_report", "cadence": "daily", "safe": True},
            {"name": "evidence_scorecard", "cadence": "daily", "safe": True},
            {"name": "support_bundle_preview", "cadence": "weekly", "safe": True},
            {"name": "roadmap_completion_gate", "cadence": "on_change", "safe": True},
        ],
        "execution": "local_only",
    }


def metrics_warehouse_snapshot(metrics: list[dict[str, Any]]) -> dict[str, Any]:
    pnl_values = [float(item.get("pnl", 0.0)) for item in metrics]
    latency_values = [float(item.get("latency_ms", 0.0)) for item in metrics]
    return {
        "status": "ready",
        "rows": len(metrics),
        "pnl_sum": round(sum(pnl_values), 6),
        "latency_p95_ms": round(_percentile(latency_values, 0.95), 3),
        "anomaly": bool(latency_values and _percentile(latency_values, 0.95) > 2000),
    }


def safe_ops_assistant_answer(question: str, context: dict[str, Any]) -> dict[str, Any]:
    lowered = question.lower()
    if any(term in lowered for term in ["live", "withdraw", "real order", "echte order"]):
        return {"answer": "Niet toegestaan: live trading en withdrawals blijven geblokkeerd.", "allowed": False}
    return {
        "answer": f"Lokale status: {context.get('status', 'unknown')}. Volgende veilige actie: {context.get('next_action', 'review evidence')}.",
        "allowed": True,
        "sources": ["local_redacted_artifacts"],
    }


def action_center_proposal(action: str, safety_class: str = "safe_local") -> dict[str, Any]:
    allowed = safety_class in {"safe_local", "read_only", "paper_only"}
    return {
        "action": action,
        "safety_class": safety_class,
        "status": "pending_approval" if allowed else "blocked",
        "confirmation_phrase": f"CONFIRM {action.upper().replace(' ', '_')}" if allowed else "",
        "decision_journal_required": allowed,
    }


def permission_profile(role: str) -> dict[str, Any]:
    profiles = {
        "viewer": ["read_dashboard", "read_reports"],
        "operator": ["read_dashboard", "read_reports", "approve_safe_local", "approve_paper_only"],
        "admin": ["read_dashboard", "read_reports", "approve_safe_local", "approve_paper_only", "manage_local_settings"],
    }
    permissions = profiles.get(role, profiles["viewer"])
    return {
        "role": role if role in profiles else "viewer",
        "permissions": permissions,
        "live_trading_permission": False,
        "separation_of_duties": role == "admin",
    }


def disaster_recovery_plan(settings: BotSettings, output_zip: Path | None = None) -> dict[str, Any]:
    artifacts = [settings.data_dir] if settings.data_dir.exists() else []
    payload: dict[str, Any] = {
        "status": "ready" if artifacts else "no_data_dir",
        "artifacts": [str(path) for path in artifacts],
        "restore_preview": True,
        "integrity_checks": ["zip_manifest", "redaction", "path_traversal_guard"],
    }
    if output_zip and artifacts:
        payload["backup"] = create_backup(artifacts, output_zip).to_dict()
    return payload


def release_upgrade_plan(current_version: str, target_version: str) -> dict[str, Any]:
    return {
        "status": "ready" if current_version != target_version else "noop",
        "current_version": current_version,
        "target_version": target_version,
        "steps": ["pre_upgrade_backup", "compatibility_check", "migration_manifest", "smoke_tests", "rollback_evidence"],
        "downgrade_safe": True,
    }


def roadmap_execution_status(roadmap_dir: Path) -> dict[str, Any]:
    priorities = prioritize_roadmaps(roadmap_dir)
    return {
        "status": "ready" if priorities else "empty",
        "open_roadmaps": len(priorities),
        "priorities": priorities,
        "completion_gate": ["tests_pass", "evidence_written", "moved_to_voltooid_docs"],
    }


def repository_knowledge_graph(root: Path) -> dict[str, Any]:
    src_files = sorted((root / "src" / "binance_spot_bot").glob("*.py"))
    test_files = sorted((root / "tests").glob("test*.py"))
    doc_files = sorted((root / "docs").glob("*.md")) if (root / "docs").exists() else []
    return {
        "status": "ready",
        "nodes": {"src": len(src_files), "tests": len(test_files), "docs": len(doc_files)},
        "hotspots": [path.name for path in src_files if path.name in {"runtime.py", "streamlit_app.py", "paper_os.py"}],
        "duplicate_work_guard": "reuse_existing_modules_before_new_files",
    }


def select_tests_for_changes(changed_paths: list[str]) -> dict[str, Any]:
    selected = {"tests/test_roadmaps_076_102_paper_os.py"}
    for path in changed_paths:
        normalized = path.replace("\\", "/")
        if "runtime.py" in normalized or "pilot_orchestrator.py" in normalized:
            selected.add("tests/test_roadmap_029_pilot_state_machine.py")
        if "streamlit_app.py" in normalized or "/ui/" in normalized:
            selected.add("tests/test_simple_demo_dashboard.py")
        if "model" in normalized or "evaluation.py" in normalized:
            selected.add("tests/test_features_model_backtest.py")
    profile = "deep" if len(selected) > 3 else "standard"
    return {"profile": profile, "tests": sorted(selected), "regression_risk": "medium" if profile == "standard" else "high"}


def performance_budget_report(samples: list[dict[str, Any]]) -> dict[str, Any]:
    durations = [float(item.get("duration_ms", 0.0)) for item in samples]
    p95 = _percentile(durations, 0.95)
    return {
        "status": "pass" if p95 <= 1500 else "review",
        "samples": len(samples),
        "p95_ms": round(p95, 3),
        "budget_ms": 1500,
    }


def dashboard_payload_budget(snapshot: dict[str, Any], max_rows: int = 200) -> dict[str, Any]:
    tables = {}
    for key, value in snapshot.items():
        if isinstance(value, list):
            tables[key] = {"rows": len(value), "over_budget": len(value) > max_rows}
    return {
        "status": "pass" if not any(item["over_budget"] for item in tables.values()) else "review",
        "max_rows": max_rows,
        "tables": tables,
        "lazy_loading": True,
    }


def feature_contract_report(feature_rows: list[dict[str, Any]], required_features: set[str]) -> dict[str, Any]:
    missing: dict[str, list[str]] = {}
    for index, row in enumerate(feature_rows):
        values = row.get("values", row)
        absent = sorted(required_features - set(values.keys()))
        if absent:
            missing[str(index)] = absent
    return {
        "status": "pass" if not missing else "blocked",
        "required_features": sorted(required_features),
        "rows": len(feature_rows),
        "missing": missing,
    }


def model_experiment_card(alias: str, metrics: dict[str, Any], feature_contract: dict[str, Any]) -> dict[str, Any]:
    promoted = feature_contract.get("status") == "pass" and float(metrics.get("walkforward_score", 0.0)) >= 0.55
    return {
        "alias": alias,
        "status": "paper_promotable" if promoted else "candidate",
        "metrics": redact_payload(metrics),
        "feature_contract": feature_contract.get("status"),
        "latency_budget_ms": 250,
        "promotion_scope": "paper_shadow_demo_only",
    }


def shadow_drift_report(reference: list[float], current: list[float], threshold: float = 0.10) -> dict[str, Any]:
    ref_mean = statistics.mean(reference) if reference else 0.0
    cur_mean = statistics.mean(current) if current else 0.0
    drift = abs(cur_mean - ref_mean)
    return {
        "status": "review" if drift > threshold else "pass",
        "reference_mean": round(ref_mean, 6),
        "current_mean": round(cur_mean, 6),
        "drift": round(drift, 6),
        "threshold": threshold,
        "downgrade": drift > threshold,
    }


def ensemble_vote(votes: list[dict[str, Any]]) -> dict[str, Any]:
    weighted: dict[str, float] = {}
    for vote in votes:
        signal = str(vote.get("signal", "HOLD")).upper()
        weighted[signal] = weighted.get(signal, 0.0) + float(vote.get("weight", 1.0)) * float(vote.get("confidence", 0.5))
    decision = max(weighted.items(), key=lambda item: item[1])[0] if weighted else "HOLD"
    return {
        "decision": decision,
        "scores": {key: round(value, 4) for key, value in sorted(weighted.items())},
        "governance": "paper_shadow_demo_only",
    }


def paper_os_audit(root: Path, settings: BotSettings, roadmap_dir: Path) -> dict[str, Any]:
    roadmap_status = roadmap_execution_status(roadmap_dir)
    graph = repository_knowledge_graph(root)
    ops = local_ops_job_plan()
    blockers = []
    if settings.live_trading_enabled:
        blockers.append("live_trading_enabled")
    if roadmap_status["open_roadmaps"] == 0:
        blockers.append("no_open_roadmaps_to_audit")
    return {
        "status": "pass" if not blockers else "blocked",
        "blockers": blockers,
        "roadmaps": roadmap_status,
        "knowledge_graph": graph,
        "ops": ops,
        "no_live_contract": NO_LIVE_CONTRACT,
    }


def stabilization_backlog(audit: dict[str, Any]) -> dict[str, Any]:
    blockers = list(audit.get("blockers", []))
    return {
        "status": "ready" if blockers else "clean",
        "items": [{"blocker": item, "priority": "high", "owner": "local_operator"} for item in blockers],
        "reliability_focus": ["flaky_checks", "slow_checks", "evidence_gaps", "dashboard_smoke"],
    }


def operator_manual_payload() -> dict[str, Any]:
    return {
        "status": "ready",
        "chapters": [
            "start_dashboard",
            "connect_demo_spot",
            "start_multi_symbol_demo",
            "read_risk_and_indicator_panels",
            "handle_recovery",
            "export_support_bundle",
            "never_enable_live_trading",
        ],
        "training_mode": True,
        "certification": ["can_start_demo", "can_stop_demo", "can_read_evidence", "can_recover_safely"],
    }


def write_paper_os_evidence(settings: BotSettings, payload: dict[str, Any], name: str = "paper-os-audit") -> Path:
    target_dir = settings.data_dir / "paper-os"
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / f"{name}-{int(time.time() * 1000)}.json"
    path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    return path


def _roadmap_number(path: Path) -> int | None:
    prefix = path.name.split("-", 1)[0]
    return int(prefix) if prefix.isdigit() else None


def _roadmap_group(number: int) -> tuple[str, int]:
    for number_range, group, priority in ROADMAP_GROUPS:
        if number in number_range:
            return group, priority
    return "unclassified", 90


def _priority_reason(group: str) -> str:
    return {
        "data_strategy_foundation": "basis voor alle latere strategy, model en dashboard evidence",
        "paper_deployment_portfolio_governance": "maakt gecontroleerde paper runs en portfolio policies mogelijk",
        "local_ops_security_recovery_release": "maakt lokale bediening, security, recovery en upgrades veilig",
        "developer_runtime_data_quality": "vermindert regressierisico en performanceproblemen in de kern",
        "model_monitoring_ensemble_governance": "bewaakt modellen en strategieen zonder live trading",
        "paper_os_audit_stabilization_operator_training": "sluit af met audit, stabilisatie en operator handleiding",
    }.get(group, "onbekende roadmapgroep")


def _unique_symbols(symbols: list[str]) -> list[str]:
    seen: set[str] = set()
    rows = []
    for symbol in symbols:
        normalized = symbol.strip().upper()
        if normalized and normalized not in seen:
            seen.add(normalized)
            rows.append(normalized)
    return rows


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * percentile)))
    return ordered[index]


def _compact_payload(payload: dict[str, Any]) -> dict[str, Any]:
    compacted: dict[str, Any] = {}
    for key, value in payload.items():
        if isinstance(value, list):
            compacted[key] = {"count": len(value), "latest": value[-1] if value else None}
        elif isinstance(value, dict):
            compacted[key] = {str(item_key): item_value for item_key, item_value in list(value.items())[:25]}
        else:
            compacted[key] = value
    return redact_payload(compacted)
