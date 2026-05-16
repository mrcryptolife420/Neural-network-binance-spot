from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


@dataclass(frozen=True)
class DashboardV2WidgetDefinition:
    widget_type: str
    title: str
    category: str
    data_sources: tuple[str, ...]
    default_size: tuple[int, int] = (4, 3)
    min_size: tuple[int, int] = (2, 2)
    max_instances: int = 8
    locked: bool = False
    can_export: bool = True
    action_policy: str = "read_only"
    safe_modes: tuple[str, ...] = ("demo", "paper", "testnet-readiness")
    required_permissions: tuple[str, ...] = ("local_dashboard",)
    secret_safe: bool = True

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


def _widget(widget_type: str, title: str, category: str, data_sources: tuple[str, ...], **kwargs: Any) -> DashboardV2WidgetDefinition:
    return DashboardV2WidgetDefinition(widget_type=widget_type, title=title, category=category, data_sources=data_sources, **kwargs)


CORE_WIDGETS: tuple[DashboardV2WidgetDefinition, ...] = (
    _widget("no_live_banner", "No Live Banner", "safety", ("no_live_proof",), locked=True, max_instances=1, can_export=False),
    _widget("stop_button", "Stop Button", "safety", ("runtime_controls",), locked=True, max_instances=1, action_policy="safe_local_stop"),
    _widget("runtime_status", "Runtime Status", "runtime", ("runtime_snapshot",)),
    _widget("mode_source_symbol", "Mode Source Symbol", "runtime", ("runtime_snapshot",)),
    _widget("websocket_status", "WebSocket Status", "runtime", ("websocket",)),
    _widget("candle_chart", "Candle Chart", "chart", ("candles",), default_size=(6, 4), max_instances=6),
    _widget("equity_chart", "Equity Curve", "chart", ("equity_points",), default_size=(6, 3), max_instances=4),
    _widget("signal_markers", "Signal Markers", "market", ("signals",)),
    _widget("fill_markers", "Fill Markers", "paper", ("fills",)),
    _widget("paper_account", "Paper Account", "paper", ("paper_account",)),
    _widget("risk_decision", "Risk Decision", "risk", ("risk_blocks",)),
    _widget("risk_block_summary", "Risk Block Summary", "risk", ("risk_blocks",)),
    _widget("alerts_inbox", "Alerts Inbox", "operator", ("alerts",)),
    _widget("demo_connection", "Demo Connection", "demo", ("demo_connection",)),
    _widget("demo_order_status", "Demo Order Status", "demo", ("open_demo_orders",)),
    _widget("reconciliation", "Reconciliation", "demo", ("reconciliation",)),
    _widget("session_summary", "Session Summary", "operator", ("sessions",)),
    _widget("active_model", "Active Model", "model", ("model_status",)),
    _widget("model_health", "Model Health", "model", ("model_status",)),
    _widget("prediction_drift", "Prediction Drift", "model", ("model_status",)),
    _widget("portfolio_allocation", "Portfolio Allocation", "portfolio", ("portfolio_status",)),
    _widget("risk_budget", "Risk Budget", "portfolio", ("portfolio_status",)),
    _widget("attribution", "Attribution", "portfolio", ("portfolio_status",)),
    _widget("rotation_status", "Rotation Status", "portfolio", ("portfolio_status",)),
    _widget("top_of_book", "Top Of Book", "market", ("runtime_snapshot",)),
    _widget("spread", "Spread", "market", ("runtime_snapshot",)),
    _widget("volume", "Volume", "market", ("candles",)),
    _widget("data_quality", "Data Quality", "market", ("runtime_snapshot",)),
    _widget("watchlist", "Watchlist", "operator", ("watchlists",)),
    _widget("session_report", "Session Report", "evidence", ("operator_evidence",)),
    _widget("evidence_manifest", "Evidence Manifest", "evidence", ("operator_evidence",)),
    _widget("support_bundle_status", "Support Bundle", "support", ("support_status",)),
    _widget("local_ops_snapshot", "Local Ops Snapshot", "support", ("operator_evidence",)),
    _widget("operator_quality_gate", "Operator Quality Gate", "operator", ("operator_evidence",)),
    _widget("performance_budget_status", "Performance Budget", "performance", ("performance_metrics",)),
    _widget("monitoring_alerts", "Monitoring Alerts", "logs", ("alerts",)),
    _widget("signal_confidence", "Signal Confidence", "advanced", ("signals",)),
    _widget("market_scanner_health", "Market Scanner Health", "market_intelligence", ("market_intelligence_health",)),
    _widget("public_endpoint_policy", "Public Endpoint Policy", "market_intelligence", ("market_intelligence_policy",), locked=True, can_export=False),
    _widget("rate_limit_budget", "Rate Limit Budget", "market_intelligence", ("scanner_rate_limit_plan",)),
    _widget("symbol_universe", "Symbol Universe", "market_intelligence", ("symbol_universe",)),
    _widget("watchlist_snapshot", "Watchlist Snapshot", "market_intelligence", ("watchlist_scan",)),
    _widget("market_ranking_table", "Market Ranking Table", "market_intelligence", ("symbol_rankings",)),
    _widget("spread_volume_matrix", "Spread Volume Matrix", "market_intelligence", ("market_metrics",)),
    _widget("volatility_momentum", "Volatility Momentum", "market_intelligence", ("market_metrics",)),
    _widget("data_freshness", "Data Freshness", "market_intelligence", ("data_quality",)),
    _widget("market_data_quality", "Market Data Quality", "market_intelligence", ("data_quality",)),
    _widget("symbol_detail", "Symbol Detail", "market_intelligence", ("symbol_universe", "watchlist_scan")),
    _widget("multi_symbol_paper_analytics", "Multi-Symbol Paper Analytics", "market_intelligence", ("paper_analytics",)),
    _widget("scanner_evidence", "Scanner Evidence", "market_intelligence", ("scanner_evidence",)),
    _widget("scanner_candidate_table", "Scanner Candidate Table", "strategy_lab", ("strategy_lab_candidates",)),
    _widget("experiment_queue", "Experiment Queue", "strategy_lab", ("strategy_lab_queue",)),
    _widget("experiment_matrix", "Experiment Matrix", "strategy_lab", ("strategy_lab_matrix",)),
    _widget("experiment_run_status", "Experiment Run Status", "strategy_lab", ("strategy_lab_results",)),
    _widget("strategy_comparison", "Strategy Comparison", "strategy_lab", ("strategy_lab_comparison",)),
    _widget("candidate_scorecard", "Candidate Scorecard", "strategy_lab", ("strategy_lab_scorecards",)),
    _widget("research_guard", "Research Guard", "strategy_lab", ("strategy_lab_guards",)),
    _widget("portfolio_candidate", "Portfolio Candidate", "strategy_lab", ("strategy_lab_portfolio",)),
    _widget("experiment_evidence", "Experiment Evidence", "strategy_lab", ("strategy_lab_evidence",)),
    _widget("portfolio_basket_builder", "Portfolio Basket Builder", "portfolio_lab", ("portfolio_lab_basket",)),
    _widget("candidate_basket_table", "Candidate Basket Table", "portfolio_lab", ("portfolio_lab_basket",)),
    _widget("allocation_proposal", "Allocation Proposal", "portfolio_lab", ("portfolio_lab_allocation",)),
    _widget("allocation_constraint", "Allocation Constraint", "portfolio_lab", ("portfolio_lab_constraints",)),
    _widget("portfolio_simulation_status", "Portfolio Simulation Status", "portfolio_lab", ("portfolio_lab_simulation",)),
    _widget("portfolio_equity_curve", "Portfolio Equity Curve", "portfolio_lab", ("portfolio_lab_simulation",), default_size=(6, 3)),
    _widget("portfolio_drawdown", "Portfolio Drawdown", "portfolio_lab", ("portfolio_lab_risk",)),
    _widget("portfolio_risk_analytics", "Portfolio Risk Analytics", "portfolio_lab", ("portfolio_lab_risk",)),
    _widget("correlation_proxy", "Correlation Proxy", "portfolio_lab", ("portfolio_lab_correlation",)),
    _widget("stress_test", "Stress Test", "portfolio_lab", ("portfolio_lab_stress",)),
    _widget("allocation_scorecard", "Allocation Scorecard", "portfolio_lab", ("portfolio_lab_scorecards",)),
    _widget("portfolio_research_guard", "Portfolio Research Guard", "portfolio_lab", ("portfolio_lab_guards",)),
    _widget("portfolio_evidence", "Portfolio Evidence", "portfolio_lab", ("portfolio_lab_evidence",)),
    _widget("walk_forward_split", "Walk-Forward Split", "portfolio_lab", ("walk_forward_split",)),
    _widget("dataset_coverage", "Dataset Coverage", "portfolio_lab", ("dataset_coverage",)),
    _widget("rebalancing_schedule", "Rebalancing Schedule", "portfolio_lab", ("rebalancing_schedules",)),
    _widget("rebalance_event_timeline", "Rebalance Event Timeline", "portfolio_lab", ("rebalance_events",)),
    _widget("rolling_portfolio_status", "Rolling Portfolio Status", "portfolio_lab", ("rolling_portfolio",)),
    _widget("walk_forward_performance", "Walk-Forward Performance", "portfolio_lab", ("walk_forward_performance",)),
    _widget("allocation_decay", "Allocation Decay", "portfolio_lab", ("allocation_decay",)),
    _widget("candidate_replacement", "Candidate Replacement", "portfolio_lab", ("candidate_replacement",)),
    _widget("robustness_scorecard", "Robustness Scorecard", "portfolio_lab", ("robustness_scorecards",)),
    _widget("robustness_governance_gate", "Robustness Governance Gate", "portfolio_lab", ("robustness_gate",)),
    _widget("walk_forward_evidence", "Walk-Forward Evidence", "portfolio_lab", ("walk_forward_evidence",)),
)


def widget_registry() -> dict[str, DashboardV2WidgetDefinition]:
    return {item.widget_type: item for item in CORE_WIDGETS}


def widget_registry_payload() -> dict[str, Any]:
    widgets = [item.to_dict() for item in CORE_WIDGETS]
    blockers = validate_widget_registry()["blockers"]
    return {
        "status": "ok" if not blockers else "blocked",
        "widgets": widgets,
        "categories": sorted({item.category for item in CORE_WIDGETS}),
        "blockers": blockers,
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }


def validate_widget_registry() -> dict[str, Any]:
    blockers: list[str] = []
    seen: set[str] = set()
    for item in CORE_WIDGETS:
        if item.widget_type in seen:
            blockers.append(f"duplicate widget type: {item.widget_type}")
        seen.add(item.widget_type)
        if "live" in item.safe_modes or item.widget_type.startswith("live_"):
            blockers.append(f"live widget blocked: {item.widget_type}")
        if item.category == "safety" and not item.locked:
            blockers.append(f"safety widget must be locked: {item.widget_type}")
        if not item.secret_safe:
            blockers.append(f"widget must be secret safe: {item.widget_type}")
    return {"status": "ok" if not blockers else "blocked", "blockers": blockers, "live_trading_enabled": False}


def validate_widget_types(widget_types: list[str] | tuple[str, ...]) -> dict[str, Any]:
    registry = widget_registry()
    unknown = sorted({item for item in widget_types if item not in registry})
    live = sorted({item for item in widget_types if item.startswith("live_") or ".live" in item})
    blockers = [f"unknown widget type: {item}" for item in unknown] + [f"live widget type blocked: {item}" for item in live]
    return {"status": "ok" if not blockers else "blocked", "blockers": blockers, "live_trading_enabled": False}
