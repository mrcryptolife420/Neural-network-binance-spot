from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.config import BotSettings

from .action_policy import evaluate_dashboard_v2_action
from .event_bus import DashboardV2EventBus
from .payload_profiles import apply_payload_profile
from .runtime_bridge import DashboardRuntimeBridge
from .schemas import (
    DashboardV2ActionRequest,
    DashboardV2Config,
    DashboardV2Health,
    DashboardV2Page,
    SUPPORTED_MODES,
    dashboard_v2_no_live_statement,
)
from .analytics_query import analytics_query
from .analytics_preset_packs import analytics_presets_payload
from .extension_pack_evidence import export_extension_pack_evidence
from .extension_pack_registry import default_extension_pack_registry
from .pack_recommendations import recommend_extension_packs
from .operator_preferences import operator_preferences_payload
from .watchlists import default_watchlist_store
from .watchlist_packs import watchlist_packs_payload
from .widget_registry import widget_registry_payload
from .workflow_packs import workflow_packs_payload
from .workspace_performance import evaluate_workspace_performance
from .workspace_presets import build_workspace_preset, workspace_presets_payload
from .workspace_schema import dashboard_workspace_from_dict, dashboard_workspace_to_dict
from .workspace_store import default_workspace_store
from binance_spot_bot.market_intelligence.multi_symbol_paper_analytics import run_multi_symbol_paper_analytics
from binance_spot_bot.market_intelligence.public_endpoint_policy import write_public_endpoint_policy_report
from binance_spot_bot.market_intelligence.scanner_evidence_bundle import export_market_intelligence_evidence
from binance_spot_bot.market_intelligence.scanner_presets import get_scanner_preset, scanner_presets_payload
from binance_spot_bot.market_intelligence.symbol_ranking import rank_symbols
from binance_spot_bot.market_intelligence.symbol_universe import build_symbol_universe, symbol_universe_to_dict
from binance_spot_bot.market_intelligence.watchlist_scanner import run_watchlist_scan
from binance_spot_bot.strategy_lab import PAPER_ONLY_CONFIRM, strategy_lab_health
from binance_spot_bot.strategy_lab.candidate_scorecards import build_candidate_scorecards
from binance_spot_bot.strategy_lab.experiment_evidence_bundle import export_strategy_lab_evidence
from binance_spot_bot.strategy_lab.experiment_matrix import expand_experiment_matrix
from binance_spot_bot.strategy_lab.experiment_queue import build_queue_from_candidates
from binance_spot_bot.strategy_lab.experiment_queue_store import default_strategy_queue_store
from binance_spot_bot.strategy_lab.experiment_result_store import default_result_store
from binance_spot_bot.strategy_lab.paper_experiment_runner import run_paper_experiment_queue
from binance_spot_bot.strategy_lab.portfolio_candidate_research import build_portfolio_candidate_research
from binance_spot_bot.strategy_lab.research_guards import evaluate_research_guards
from binance_spot_bot.strategy_lab.scanner_candidate_builder import build_scanner_candidates
from binance_spot_bot.strategy_lab.strategy_comparison import compare_strategy_results
from binance_spot_bot.portfolio_lab import PAPER_PORTFOLIO_CONFIRM, WALK_FORWARD_CONFIRM, portfolio_lab_health
from binance_spot_bot.portfolio_lab.allocation_constraints import validate_allocation
from binance_spot_bot.portfolio_lab.allocation_proposals import propose_allocation
from binance_spot_bot.portfolio_lab.basket_builder import build_candidate_basket
from binance_spot_bot.portfolio_lab.candidate_basket import fixture_basket
from binance_spot_bot.portfolio_lab.correlation_proxy import portfolio_correlation_proxy
from binance_spot_bot.portfolio_lab.evidence_bundle import export_portfolio_lab_evidence
from binance_spot_bot.portfolio_lab.portfolio_experiment_orchestrator import preview_portfolio_simulation, run_portfolio_experiment
from binance_spot_bot.portfolio_lab.portfolio_experiment_store import default_portfolio_store
from binance_spot_bot.portfolio_lab.portfolio_research_guards import evaluate_portfolio_research_guards
from binance_spot_bot.portfolio_lab.stress_tests import run_portfolio_stress_tests
from binance_spot_bot.portfolio_lab.allocation_scorecards import build_allocation_scorecards
from binance_spot_bot.portfolio_lab.allocation_decay import analyze_allocation_decay
from binance_spot_bot.portfolio_lab.allocation_robustness_scorecards import build_robustness_scorecards
from binance_spot_bot.portfolio_lab.candidate_replacement import simulate_candidate_replacements
from binance_spot_bot.portfolio_lab.dataset_coverage_audit import audit_dataset_coverage
from binance_spot_bot.portfolio_lab.rebalance_event_simulator import simulate_rebalance_events
from binance_spot_bot.portfolio_lab.rebalancing_schedules import default_rebalancing_schedules, validate_rebalancing_schedule
from binance_spot_bot.portfolio_lab.robustness_governance_gate import evaluate_robustness_governance_gate
from binance_spot_bot.portfolio_lab.rolling_portfolio_orchestrator import preview_rolling_portfolio_simulation, run_rolling_portfolio_simulation
from binance_spot_bot.portfolio_lab.walk_forward_evidence_bundle import export_walk_forward_evidence
from binance_spot_bot.portfolio_lab.walk_forward_performance import analyze_walk_forward_performance
from binance_spot_bot.portfolio_lab.walk_forward_splits import build_walk_forward_split
from binance_spot_bot.app_control.app_evidence import export_app_control_evidence
from binance_spot_bot.app_control.app_supervisor import app_supervisor_plan
from binance_spot_bot.app_control.bot_profile import BotProfileMode, built_in_profiles
from binance_spot_bot.app_control.config_wizard import create_profile_from_wizard
from binance_spot_bot.app_control.data_bootstrap import data_bootstrap_report
from binance_spot_bot.app_control.one_click_launcher import generate_one_click_launcher
from binance_spot_bot.app_control.profile_matrix import profile_matrix_report
from binance_spot_bot.app_control.profile_store import default_profile_store
from binance_spot_bot.app_control.runtime_orchestrator import runtime_orchestrator_status, start_profile
from binance_spot_bot.app_control.secret_refs import secret_ref_status
from binance_spot_bot.app_control.startup_health import startup_health_report
from binance_spot_bot.live_training.demo_dataset_quality import evaluate_demo_dataset_quality
from binance_spot_bot.live_training.demo_spot_data_recorder import record_demo_spot_events
from binance_spot_bot.live_training.live_readiness_gate import evaluate_live_readiness_gate
from binance_spot_bot.live_training.live_training_evidence import export_live_training_evidence
from binance_spot_bot.live_training.model_validation_gate import evaluate_model_validation_gate
from binance_spot_bot.live_training.training_dataset_builder import build_training_dataset
from binance_spot_bot.live_training.demo_to_live_pipeline import run_demo_to_live_pipeline
from binance_spot_bot.live_training.demo_session_targets import calculate_demo_session_target_progress, default_demo_session_target, fixture_complete_sessions
from binance_spot_bot.live_training.testnet_rehearsal_runner import TESTNET_REHEARSAL_CONFIRM, run_testnet_rehearsal


def dashboard_v2_pages() -> list[dict[str, Any]]:
    from binance_spot_bot.ui.page_registry import PAGES

    pages = []
    for page in PAGES:
        if page.live_trading_enabled:
            raise ValueError(f"Dashboard V2 refuses live page: {page.key}")
        pages.append(DashboardV2Page(page.key, page.title, "/" if page.key == "overview" else f"/{page.key.replace('_', '-')}").to_dict())
    pages.extend(
        [
            DashboardV2Page("workspaces", "Workspaces", "/workspaces").to_dict(),
            DashboardV2Page("watchlists", "Watchlists", "/watchlists").to_dict(),
            DashboardV2Page("preferences", "Preferences", "/preferences").to_dict(),
            DashboardV2Page("analytics", "Analytics", "/analytics").to_dict(),
            DashboardV2Page("extension_packs", "Extension Packs", "/extension-packs").to_dict(),
            DashboardV2Page("templates", "Templates", "/templates").to_dict(),
            DashboardV2Page("analytics_presets", "Analytics Presets", "/analytics-presets").to_dict(),
            DashboardV2Page("workflow_packs", "Workflow Packs", "/workflow-packs").to_dict(),
            DashboardV2Page("market_intelligence", "Market Intelligence", "/market-intelligence").to_dict(),
            DashboardV2Page("market_intelligence_scanner", "Market Scanner", "/market-intelligence/scanner").to_dict(),
            DashboardV2Page("market_intelligence_rankings", "Market Rankings", "/market-intelligence/rankings").to_dict(),
            DashboardV2Page("market_intelligence_symbols", "Symbol Universe", "/market-intelligence/symbols").to_dict(),
            DashboardV2Page("market_intelligence_paper_analytics", "Paper Analytics", "/market-intelligence/paper-analytics").to_dict(),
            DashboardV2Page("strategy_lab", "Strategy Lab", "/strategy-lab").to_dict(),
            DashboardV2Page("portfolio_lab", "Portfolio Lab", "/portfolio-lab").to_dict(),
            DashboardV2Page("portfolio_lab_baskets", "Portfolio Baskets", "/portfolio-lab/baskets").to_dict(),
            DashboardV2Page("portfolio_lab_allocations", "Portfolio Allocations", "/portfolio-lab/allocations").to_dict(),
            DashboardV2Page("portfolio_lab_simulations", "Portfolio Simulations", "/portfolio-lab/simulations").to_dict(),
            DashboardV2Page("portfolio_robustness", "Portfolio Robustness", "/portfolio-lab/robustness").to_dict(),
            DashboardV2Page("control_center", "Control Center", "/control-center").to_dict(),
            DashboardV2Page("live_training", "Live Training", "/live-training").to_dict(),
            DashboardV2Page("live_safety", "Live Safety", "/live").to_dict(),
            DashboardV2Page("live_session", "Live Session", "/live/session").to_dict(),
            DashboardV2Page("live_governance", "Live Governance", "/live/governance").to_dict(),
            DashboardV2Page("live_ops", "Live Ops", "/live-ops").to_dict(),
            DashboardV2Page("package_center", "Package Center", "/package").to_dict(),
            DashboardV2Page("ai_doctor", "AI Doctor", "/ai-doctor").to_dict(),
        ]
    )
    return pages


class DashboardV2FallbackApp:
    def __init__(self) -> None:
        self.routes = [
            "/api/health",
            "/api/config",
            "/api/pages",
            "/api/runtime/snapshot",
            "/api/workspaces",
            "/api/workspace-presets",
            "/api/widgets",
            "/api/analytics/query",
            "/api/watchlists",
            "/api/preferences",
            "/api/extension-packs",
            "/api/extension-packs/catalog",
            "/api/extension-packs/installed",
            "/api/extension-packs/recommendations",
            "/api/market-intelligence/health",
            "/api/market-intelligence/policy",
            "/api/market-intelligence/symbol-universe",
            "/api/market-intelligence/scanner-presets",
            "/api/market-intelligence/scan/preview",
            "/api/market-intelligence/paper-analytics/preview",
            "/api/market-intelligence/evidence",
            "/api/strategy-lab/health",
            "/api/strategy-lab/candidates",
            "/api/strategy-lab/queue/preview",
            "/api/portfolio-lab/health",
            "/api/portfolio-lab/baskets/build",
            "/api/portfolio-lab/allocations/propose",
            "/api/portfolio-lab/simulations/preview",
            "/api/portfolio-lab/simulations/run",
            "/api/portfolio-lab/robustness/health",
            "/api/portfolio-lab/walk-forward/splits/preview",
            "/api/portfolio-lab/rolling-simulation/preview",
            "/api/app-control/health",
            "/api/app-control/profiles",
            "/api/app-control/config-wizard/profile",
            "/ws/events",
        ]
        self.bridge = DashboardRuntimeBridge()
        self.bus = DashboardV2EventBus()

    def health(self) -> dict[str, Any]:
        return DashboardV2Health().to_dict()

    def config(self) -> dict[str, Any]:
        return DashboardV2Config().to_dict()

    def pages(self) -> dict[str, Any]:
        return {"status": "ok", "pages": dashboard_v2_pages(), "live_trading_enabled": False}

    def snapshot(self, profile: str = "overview") -> dict[str, Any]:
        return apply_payload_profile(self.bridge.snapshot(), profile)

    def action(self, request: DashboardV2ActionRequest) -> dict[str, Any]:
        return evaluate_dashboard_v2_action(request).to_dict()

    def workspaces(self) -> dict[str, Any]:
        return default_workspace_store(Path.cwd()).list()

    def workspace_presets(self) -> dict[str, Any]:
        return workspace_presets_payload()

    def widgets(self) -> dict[str, Any]:
        return widget_registry_payload()

    def analytics_query(self, scope: str = "runtime_snapshot", tail: int = 250) -> dict[str, Any]:
        return analytics_query(self.bridge.snapshot(), scope=scope, tail=tail)

    def watchlists(self) -> dict[str, Any]:
        return default_watchlist_store(Path.cwd()).list()

    def preferences(self) -> dict[str, Any]:
        return operator_preferences_payload(Path.cwd())

    def extension_packs(self) -> dict[str, Any]:
        return default_extension_pack_registry(Path.cwd()).available()

    def market_intelligence_health(self) -> dict[str, Any]:
        return {"status": "ok", "public_data_only": True, "live_trading_enabled": False}

    def market_intelligence_policy(self) -> dict[str, Any]:
        return write_public_endpoint_policy_report(Path.cwd())

    def market_intelligence_presets(self) -> dict[str, Any]:
        return scanner_presets_payload()

    def strategy_lab_health(self) -> dict[str, Any]:
        return strategy_lab_health()


def create_dashboard_v2_app(settings: BotSettings | None = None) -> Any:
    if "live" in SUPPORTED_MODES:
        raise ValueError("Dashboard V2 supported modes must not include live")
    try:
        from fastapi import FastAPI, WebSocket
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import FileResponse
        from fastapi.staticfiles import StaticFiles
    except Exception:
        return DashboardV2FallbackApp()

    bridge = DashboardRuntimeBridge()
    bus = DashboardV2EventBus()
    app = FastAPI(title="Dashboard V2", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1", "http://localhost"],
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    static_dir = Path(__file__).resolve().parent / "static"
    if static_dir.exists():
        app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="dashboard_assets") if (static_dir / "assets").exists() else None

        @app.get("/")
        def dashboard_index() -> Any:
            return FileResponse(static_dir / "index.html")

        @app.get("/app.js")
        def dashboard_app_js() -> Any:
            return FileResponse(static_dir / "app.js")

        @app.get("/styles.css")
        def dashboard_styles_css() -> Any:
            return FileResponse(static_dir / "styles.css")

        @app.get("/manifest.json")
        def dashboard_manifest() -> Any:
            return FileResponse(static_dir / "manifest.json")

    @app.get("/api/health")
    def health() -> dict[str, Any]:
        return DashboardV2Health().to_dict()

    @app.get("/api/config")
    def config() -> dict[str, Any]:
        return DashboardV2Config().to_dict()

    @app.get("/api/pages")
    def pages() -> dict[str, Any]:
        return {"status": "ok", "pages": dashboard_v2_pages(), "live_trading_enabled": False}

    @app.get("/api/runtime/snapshot")
    def snapshot(profile: str = "overview") -> dict[str, Any]:
        return apply_payload_profile(bridge.snapshot(), profile)

    @app.get("/api/charts/candles")
    def chart_candles(tail: int = 500) -> dict[str, Any]:
        payload = apply_payload_profile(bridge.snapshot(), "chart")["payload"]
        return {"status": "ok", "candles": payload.get("candles", [])[-min(tail, 500):], "live_trading_enabled": False}

    @app.get("/api/charts/equity")
    def chart_equity(tail: int = 500) -> dict[str, Any]:
        return {"status": "ok", "equity": bridge.snapshot().get("equity", [])[-min(tail, 500):], "live_trading_enabled": False}

    @app.get("/api/charts/signals")
    def chart_signals(tail: int = 200) -> dict[str, Any]:
        return {"status": "ok", "signals": bridge.snapshot().get("signals", [])[-min(tail, 200):], "live_trading_enabled": False}

    @app.get("/api/charts/fills")
    def chart_fills(tail: int = 200) -> dict[str, Any]:
        return {"status": "ok", "fills": bridge.snapshot().get("fills", [])[-min(tail, 200):], "live_trading_enabled": False}

    @app.post("/api/runtime/{action}")
    def runtime_action(action: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        request = DashboardV2ActionRequest(action=f"runtime.{action}", mode=(payload or {}).get("mode", "demo"))
        result = evaluate_dashboard_v2_action(request)
        return result.to_dict()

    @app.get("/api/no-live-proof")
    def no_live_proof() -> dict[str, Any]:
        return {"status": "ok", "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}

    @app.get("/api/workspaces")
    def workspaces() -> dict[str, Any]:
        return default_workspace_store(Path.cwd()).list()

    @app.post("/api/workspaces")
    def create_workspace(preset: str = "operator_overview", name: str = "Operator Workspace") -> dict[str, Any]:
        workspace = build_workspace_preset(preset, name=name)
        return default_workspace_store(Path.cwd()).save(workspace)

    @app.get("/api/workspaces/{workspace_id}")
    def workspace_detail(workspace_id: str) -> dict[str, Any]:
        workspace = default_workspace_store(Path.cwd()).load(workspace_id)
        return {"status": "ok", "workspace": dashboard_workspace_to_dict(workspace), "live_trading_enabled": False}

    @app.post("/api/workspaces/{workspace_id}/clone")
    def workspace_clone(workspace_id: str) -> dict[str, Any]:
        return default_workspace_store(Path.cwd()).clone(workspace_id)

    @app.post("/api/workspaces/{workspace_id}/export")
    def workspace_export(workspace_id: str) -> dict[str, Any]:
        return default_workspace_store(Path.cwd()).export(workspace_id)

    @app.delete("/api/workspaces/{workspace_id}")
    def workspace_delete(workspace_id: str, confirm: str = "") -> dict[str, Any]:
        return default_workspace_store(Path.cwd()).delete(workspace_id, confirm=confirm)

    @app.get("/api/workspace-presets")
    def workspace_presets() -> dict[str, Any]:
        return workspace_presets_payload()

    @app.get("/api/widgets")
    def widgets() -> dict[str, Any]:
        return widget_registry_payload()

    @app.get("/api/analytics/query")
    def analytics(scope: str = "runtime_snapshot", tail: int = 250, symbol: str = "", severity: str = "") -> dict[str, Any]:
        return analytics_query(bridge.snapshot(), scope=scope, tail=tail, symbol=symbol, severity=severity)

    @app.get("/api/analytics/summary")
    def analytics_summary() -> dict[str, Any]:
        return analytics_query(bridge.snapshot(), scope="runtime_snapshot", aggregation="count")

    @app.get("/api/analytics/series/{series_name}")
    def analytics_series(series_name: str, tail: int = 250) -> dict[str, Any]:
        return analytics_query(bridge.snapshot(), scope=series_name, tail=tail)

    @app.get("/api/watchlists")
    def watchlists() -> dict[str, Any]:
        return default_watchlist_store(Path.cwd()).list()

    @app.get("/api/preferences")
    def preferences() -> dict[str, Any]:
        return operator_preferences_payload(Path.cwd())

    @app.get("/api/workspaces/{workspace_id}/performance")
    def workspace_performance(workspace_id: str) -> dict[str, Any]:
        workspace = default_workspace_store(Path.cwd()).load(workspace_id)
        return evaluate_workspace_performance(workspace)

    @app.get("/api/extension-packs")
    def extension_packs() -> dict[str, Any]:
        return default_extension_pack_registry(Path.cwd()).available()

    @app.get("/api/extension-packs/catalog")
    def extension_pack_catalog() -> dict[str, Any]:
        return default_extension_pack_registry(Path.cwd()).available()

    @app.get("/api/extension-packs/installed")
    def extension_pack_installed() -> dict[str, Any]:
        return default_extension_pack_registry(Path.cwd()).installed()

    @app.get("/api/extension-packs/recommendations")
    def extension_pack_recommendations(workflow: str = "paper-session") -> dict[str, Any]:
        return recommend_extension_packs({"workflow": workflow})

    @app.get("/api/extension-packs/{pack_id}")
    def extension_pack_detail(pack_id: str) -> dict[str, Any]:
        registry = default_extension_pack_registry(Path.cwd())
        pack = registry.load_pack(pack_id)
        return {"status": "ok", "pack": pack.manifest.__dict__, "live_trading_enabled": False}

    @app.get("/api/extension-packs/{pack_id}/compatibility")
    def extension_pack_compatibility(pack_id: str) -> dict[str, Any]:
        from .pack_compatibility import evaluate_pack_compatibility

        pack = default_extension_pack_registry(Path.cwd()).load_pack(pack_id)
        return evaluate_pack_compatibility(pack)

    @app.post("/api/extension-packs/{pack_id}/instantiate-workspace")
    def extension_pack_instantiate_workspace(pack_id: str) -> dict[str, Any]:
        registry = default_extension_pack_registry(Path.cwd())
        pack = registry.load_pack(pack_id)
        if not pack.content.workspace_templates:
            return {"status": "blocked", "blockers": ["pack has no workspace templates"], "live_trading_enabled": False}
        workspace = dashboard_workspace_from_dict(pack.content.workspace_templates[0])
        return default_workspace_store(Path.cwd()).save(workspace)

    @app.post("/api/extension-packs/evidence-export")
    def extension_pack_evidence() -> dict[str, Any]:
        return export_extension_pack_evidence(Path.cwd())

    @app.get("/api/templates")
    def templates() -> dict[str, Any]:
        from .workspace_template_packs import template_packs_payload

        return template_packs_payload()

    @app.get("/api/analytics-presets")
    def analytics_presets() -> dict[str, Any]:
        return analytics_presets_payload()

    @app.get("/api/workflow-packs")
    def workflow_packs() -> dict[str, Any]:
        return workflow_packs_payload()

    @app.get("/api/watchlist-packs")
    def watchlist_packs() -> dict[str, Any]:
        return watchlist_packs_payload()

    @app.get("/api/market-intelligence/health")
    def market_intelligence_health() -> dict[str, Any]:
        return {"status": "ok", "public_data_only": True, "no_live_statement": "MARKET INTELLIGENCE - NO LIVE TRADING", "live_trading_enabled": False}

    @app.get("/api/market-intelligence/symbol-universe")
    def market_intelligence_symbol_universe() -> dict[str, Any]:
        return symbol_universe_to_dict(build_symbol_universe())

    @app.post("/api/market-intelligence/symbol-universe/refresh")
    def market_intelligence_symbol_universe_refresh() -> dict[str, Any]:
        from binance_spot_bot.market_intelligence.symbol_universe import write_symbol_universe_report

        return write_symbol_universe_report(Path.cwd())

    @app.get("/api/market-intelligence/scanner-presets")
    def market_intelligence_scanner_presets() -> dict[str, Any]:
        return scanner_presets_payload()

    @app.post("/api/market-intelligence/scan/preview")
    def market_intelligence_scan_preview(preset: str = "majors_overview") -> dict[str, Any]:
        item = get_scanner_preset(preset)
        from binance_spot_bot.market_intelligence.rate_limit_budget import scanner_rate_limit_plan

        return scanner_rate_limit_plan(item.symbols)

    @app.post("/api/market-intelligence/scan/run")
    def market_intelligence_scan_run(preset: str = "majors_overview") -> dict[str, Any]:
        item = get_scanner_preset(preset)
        return run_watchlist_scan(item.symbols, root=Path.cwd(), preset=preset)

    @app.get("/api/market-intelligence/rankings/{run_id}")
    def market_intelligence_rankings(run_id: str) -> dict[str, Any]:
        item = get_scanner_preset("majors_overview")
        scan = run_watchlist_scan(item.symbols, root=Path.cwd(), preset="majors_overview")
        return rank_symbols(list(scan.get("metrics", [])), item.ranking_dimension)

    @app.post("/api/market-intelligence/paper-analytics/preview")
    def market_intelligence_paper_preview() -> dict[str, Any]:
        item = get_scanner_preset("majors_overview")
        return run_multi_symbol_paper_analytics(item.symbols, root=Path.cwd())

    @app.post("/api/market-intelligence/paper-analytics/run")
    def market_intelligence_paper_run(confirm: str = "RUN_PAPER_ANALYTICS_ONLY") -> dict[str, Any]:
        item = get_scanner_preset("majors_overview")
        return run_multi_symbol_paper_analytics(item.symbols, root=Path.cwd(), confirm=confirm)

    @app.get("/api/market-intelligence/evidence")
    def market_intelligence_evidence() -> dict[str, Any]:
        return export_market_intelligence_evidence(Path.cwd())

    @app.get("/api/market-intelligence/policy")
    def market_intelligence_policy() -> dict[str, Any]:
        return write_public_endpoint_policy_report(Path.cwd())

    @app.get("/api/strategy-lab/health")
    def strategy_lab_health_route() -> dict[str, Any]:
        return strategy_lab_health()

    @app.post("/api/strategy-lab/candidates/build")
    def strategy_lab_candidates_build(preset: str = "majors_overview") -> dict[str, Any]:
        return build_scanner_candidates(preset_id=preset)

    @app.get("/api/strategy-lab/candidates")
    def strategy_lab_candidates() -> dict[str, Any]:
        return build_scanner_candidates()

    @app.post("/api/strategy-lab/queue/preview")
    def strategy_lab_queue_preview(preset: str = "small_safe_smoke") -> dict[str, Any]:
        candidates = list(build_scanner_candidates()["candidates"])
        return expand_experiment_matrix(candidates, preset=preset)

    @app.post("/api/strategy-lab/queue/create")
    def strategy_lab_queue_create(preset: str = "small_safe_smoke") -> dict[str, Any]:
        candidates = list(build_scanner_candidates()["candidates"])
        queue = build_queue_from_candidates(candidates, preset=preset)
        return default_strategy_queue_store(Path.cwd()).save(queue)

    @app.get("/api/strategy-lab/queues")
    def strategy_lab_queues() -> dict[str, Any]:
        return default_strategy_queue_store(Path.cwd()).list()

    @app.get("/api/strategy-lab/queues/{queue_id}")
    def strategy_lab_queue_detail(queue_id: str) -> dict[str, Any]:
        return {"status": "ok", "queue": default_strategy_queue_store(Path.cwd()).load(queue_id), "live_trading_enabled": False}

    @app.post("/api/strategy-lab/queues/{queue_id}/run")
    def strategy_lab_queue_run(queue_id: str, confirm: str = "") -> dict[str, Any]:
        if confirm != PAPER_ONLY_CONFIRM:
            return {"status": "blocked", "blockers": [f"queue run requires confirm {PAPER_ONLY_CONFIRM}"], "live_trading_enabled": False}
        queue = default_strategy_queue_store(Path.cwd()).load(queue_id)
        report = run_paper_experiment_queue(queue, confirm=confirm)
        for row in report.get("results", []):
            default_result_store(Path.cwd()).save_job_result(row)
        return report

    @app.post("/api/strategy-lab/queues/{queue_id}/cancel")
    def strategy_lab_queue_cancel(queue_id: str) -> dict[str, Any]:
        return {"status": "ok", "queue_id": queue_id, "cancelled": True, "live_trading_enabled": False}

    @app.get("/api/strategy-lab/results")
    def strategy_lab_results() -> dict[str, Any]:
        return default_result_store(Path.cwd()).list_results()

    @app.get("/api/strategy-lab/results/{run_id}")
    def strategy_lab_result_detail(run_id: str) -> dict[str, Any]:
        return {"status": "ok", "run_id": run_id, "results": default_result_store(Path.cwd()).list_results().get("results", []), "live_trading_enabled": False}

    @app.post("/api/strategy-lab/comparison")
    def strategy_lab_comparison() -> dict[str, Any]:
        return compare_strategy_results(default_result_store(Path.cwd()).list_results().get("results", []))

    @app.post("/api/strategy-lab/scorecards")
    def strategy_lab_scorecards() -> dict[str, Any]:
        return build_candidate_scorecards(default_result_store(Path.cwd()).list_results().get("results", []), list(build_scanner_candidates()["candidates"]))

    @app.post("/api/strategy-lab/portfolio-research")
    def strategy_lab_portfolio_research() -> dict[str, Any]:
        cards = build_candidate_scorecards(default_result_store(Path.cwd()).list_results().get("results", []), list(build_scanner_candidates()["candidates"]))
        return build_portfolio_candidate_research(list(cards.get("scorecards", [])))

    @app.post("/api/strategy-lab/guards")
    def strategy_lab_guards() -> dict[str, Any]:
        return evaluate_research_guards(default_result_store(Path.cwd()).list_results().get("results", []))

    @app.post("/api/strategy-lab/evidence-export")
    def strategy_lab_evidence_export() -> dict[str, Any]:
        results = default_result_store(Path.cwd()).list_results()
        return export_strategy_lab_evidence(Path.cwd(), {"results": results})

    @app.get("/api/portfolio-lab/health")
    def portfolio_lab_health_route() -> dict[str, Any]:
        return portfolio_lab_health()

    @app.post("/api/portfolio-lab/baskets/build")
    def portfolio_lab_baskets_build(mode: str = "top_score", max_items: int = 4) -> dict[str, Any]:
        return build_candidate_basket(mode=mode, max_items=max_items)

    @app.get("/api/portfolio-lab/baskets")
    def portfolio_lab_baskets() -> dict[str, Any]:
        return default_portfolio_store(Path.cwd()).list("baskets")

    @app.get("/api/portfolio-lab/baskets/{basket_id}")
    def portfolio_lab_basket_detail(basket_id: str) -> dict[str, Any]:
        return default_portfolio_store(Path.cwd()).load("baskets", basket_id)

    @app.post("/api/portfolio-lab/allocations/propose")
    def portfolio_lab_allocation_propose(mode: str = "equal_weight") -> dict[str, Any]:
        basket = fixture_basket()
        return propose_allocation(basket, mode=mode)

    @app.post("/api/portfolio-lab/allocations/validate")
    def portfolio_lab_allocation_validate() -> dict[str, Any]:
        basket = fixture_basket()
        proposal = propose_allocation(basket)
        weights = {item["item_id"]: float(item["weight"]) for item in proposal["proposal"]["items"]}
        return validate_allocation(basket, weights)

    @app.get("/api/portfolio-lab/allocations")
    def portfolio_lab_allocations() -> dict[str, Any]:
        return default_portfolio_store(Path.cwd()).list("allocations")

    @app.post("/api/portfolio-lab/simulations/preview")
    def portfolio_lab_simulation_preview() -> dict[str, Any]:
        return preview_portfolio_simulation()

    @app.post("/api/portfolio-lab/simulations/run")
    def portfolio_lab_simulation_run(confirm: str = "") -> dict[str, Any]:
        return run_portfolio_experiment(Path.cwd(), confirm=confirm)

    @app.get("/api/portfolio-lab/simulations")
    def portfolio_lab_simulations() -> dict[str, Any]:
        return default_portfolio_store(Path.cwd()).list("runs")

    @app.get("/api/portfolio-lab/simulations/{run_id}")
    def portfolio_lab_simulation_detail(run_id: str) -> dict[str, Any]:
        return default_portfolio_store(Path.cwd()).load("runs", run_id)

    @app.post("/api/portfolio-lab/stress-tests/run")
    def portfolio_lab_stress_tests_run() -> dict[str, Any]:
        run = run_portfolio_experiment(Path.cwd(), confirm=PAPER_PORTFOLIO_CONFIRM)
        return run_portfolio_stress_tests(run["simulation"])

    @app.post("/api/portfolio-lab/scorecards")
    def portfolio_lab_scorecards() -> dict[str, Any]:
        run = run_portfolio_experiment(Path.cwd(), confirm=PAPER_PORTFOLIO_CONFIRM)
        return build_allocation_scorecards(run["risk"], run["stress"], run["guards"])

    @app.post("/api/portfolio-lab/research-guards")
    def portfolio_lab_research_guards() -> dict[str, Any]:
        basket = fixture_basket()
        proposal = propose_allocation(basket)["proposal"]
        run = run_portfolio_experiment(Path.cwd(), basket=basket, allocation=proposal, confirm=PAPER_PORTFOLIO_CONFIRM)
        return evaluate_portfolio_research_guards(basket, proposal, run["risk"], run["stress"], run["correlation"])

    @app.post("/api/portfolio-lab/evidence-export")
    def portfolio_lab_evidence_export() -> dict[str, Any]:
        run = run_portfolio_experiment(Path.cwd(), confirm=PAPER_PORTFOLIO_CONFIRM)
        return export_portfolio_lab_evidence(Path.cwd(), run)

    @app.get("/api/portfolio-lab/correlation-proxy")
    def portfolio_lab_correlation_proxy_route() -> dict[str, Any]:
        return portfolio_correlation_proxy(fixture_basket())

    @app.get("/api/portfolio-lab/robustness/health")
    def portfolio_robustness_health_route() -> dict[str, Any]:
        payload = portfolio_lab_health()
        payload["robustness_lab"] = True
        payload["requires_confirm"] = WALK_FORWARD_CONFIRM
        return payload

    @app.post("/api/portfolio-lab/walk-forward/splits/preview")
    def portfolio_walk_forward_splits_preview() -> dict[str, Any]:
        return build_walk_forward_split()

    @app.post("/api/portfolio-lab/walk-forward/splits/create")
    def portfolio_walk_forward_splits_create() -> dict[str, Any]:
        return build_walk_forward_split()

    @app.post("/api/portfolio-lab/dataset-coverage/audit")
    def portfolio_dataset_coverage_audit() -> dict[str, Any]:
        return audit_dataset_coverage(build_walk_forward_split())

    @app.get("/api/portfolio-lab/rebalancing/schedules")
    def portfolio_rebalancing_schedules() -> dict[str, Any]:
        return default_rebalancing_schedules()

    @app.post("/api/portfolio-lab/rebalancing/schedules/validate")
    def portfolio_rebalancing_schedules_validate() -> dict[str, Any]:
        return validate_rebalancing_schedule(default_rebalancing_schedules()["schedules"][1])

    @app.post("/api/portfolio-lab/rebalancing/events/simulate")
    def portfolio_rebalancing_events_simulate() -> dict[str, Any]:
        basket = fixture_basket()
        allocation = propose_allocation(basket)["proposal"]
        return simulate_rebalance_events(allocation, default_rebalancing_schedules()["schedules"][1])

    @app.post("/api/portfolio-lab/rolling-simulation/preview")
    def portfolio_rolling_simulation_preview() -> dict[str, Any]:
        return preview_rolling_portfolio_simulation()

    @app.post("/api/portfolio-lab/rolling-simulation/run")
    def portfolio_rolling_simulation_run(confirm: str = "") -> dict[str, Any]:
        return run_rolling_portfolio_simulation(Path.cwd(), confirm=confirm)

    @app.post("/api/portfolio-lab/decay/analyze")
    def portfolio_decay_analyze() -> dict[str, Any]:
        return analyze_allocation_decay(fixture_basket())

    @app.post("/api/portfolio-lab/replacements/simulate")
    def portfolio_replacements_simulate(policy: str = "manual_review_required") -> dict[str, Any]:
        basket = fixture_basket()
        return simulate_candidate_replacements(basket, analyze_allocation_decay(basket), policy=policy)

    @app.post("/api/portfolio-lab/walk-forward/performance")
    def portfolio_walk_forward_performance() -> dict[str, Any]:
        rolling = run_rolling_portfolio_simulation(Path.cwd(), confirm=WALK_FORWARD_CONFIRM)
        return analyze_walk_forward_performance(rolling)

    @app.post("/api/portfolio-lab/robustness/scorecards")
    def portfolio_robustness_scorecards() -> dict[str, Any]:
        rolling = run_rolling_portfolio_simulation(Path.cwd(), confirm=WALK_FORWARD_CONFIRM)
        performance = analyze_walk_forward_performance(rolling)
        return build_robustness_scorecards(performance, rolling.get("decay"))

    @app.post("/api/portfolio-lab/robustness/governance-gate")
    def portfolio_robustness_governance_gate() -> dict[str, Any]:
        rolling = run_rolling_portfolio_simulation(Path.cwd(), confirm=WALK_FORWARD_CONFIRM)
        performance = analyze_walk_forward_performance(rolling)
        scorecards = build_robustness_scorecards(performance, rolling.get("decay"))
        return evaluate_robustness_governance_gate(scorecards, performance, rolling.get("split"))

    @app.post("/api/portfolio-lab/walk-forward/evidence-export")
    def portfolio_walk_forward_evidence_export() -> dict[str, Any]:
        rolling = run_rolling_portfolio_simulation(Path.cwd(), confirm=WALK_FORWARD_CONFIRM)
        performance = analyze_walk_forward_performance(rolling)
        scorecards = build_robustness_scorecards(performance, rolling.get("decay"))
        gate = evaluate_robustness_governance_gate(scorecards, performance, rolling.get("split"))
        return export_walk_forward_evidence(Path.cwd(), rolling, performance, scorecards, gate)

    @app.get("/api/app-control/health")
    def app_control_health_route() -> dict[str, Any]:
        return startup_health_report(Path.cwd())

    @app.get("/api/app-control/profiles")
    def app_control_profiles() -> dict[str, Any]:
        return default_profile_store(Path.cwd()).list()

    @app.get("/api/app-control/profile-templates")
    def app_control_profile_templates() -> dict[str, Any]:
        return default_profile_store(Path.cwd()).templates()

    @app.post("/api/app-control/config-wizard/profile")
    def app_control_config_wizard_profile(profile_type: str = "paper", symbol: str = "BTCUSDT") -> dict[str, Any]:
        return create_profile_from_wizard(profile_type, symbol)

    @app.get("/api/app-control/secret-ref-status")
    def app_control_secret_ref_status() -> dict[str, Any]:
        return secret_ref_status()

    @app.post("/api/app-control/launcher/generate")
    def app_control_launcher_generate() -> dict[str, Any]:
        return generate_one_click_launcher(Path.cwd())

    @app.get("/api/app-control/supervisor/plan")
    def app_control_supervisor_plan() -> dict[str, Any]:
        return app_supervisor_plan(Path.cwd())

    @app.post("/api/app-control/data-bootstrap")
    def app_control_data_bootstrap() -> dict[str, Any]:
        profile = built_in_profiles()[1]
        return data_bootstrap_report(profile)

    @app.post("/api/app-control/runtime/start")
    def app_control_runtime_start(profile_type: str = "paper") -> dict[str, Any]:
        profile = next((item for item in built_in_profiles() if item.mode == profile_type), built_in_profiles()[1])
        return start_profile(profile)

    @app.post("/api/app-control/runtime/status")
    def app_control_runtime_status(profile_type: str = "paper") -> dict[str, Any]:
        profile = next((item for item in built_in_profiles() if item.mode == profile_type), built_in_profiles()[1])
        return runtime_orchestrator_status(profile)

    @app.post("/api/live-training/demo-record")
    def live_training_demo_record() -> dict[str, Any]:
        return record_demo_spot_events(Path.cwd())

    @app.post("/api/live-training/quality")
    def live_training_quality() -> dict[str, Any]:
        recording = record_demo_spot_events(Path.cwd())
        return evaluate_demo_dataset_quality(recording)

    @app.post("/api/live-training/dataset-build")
    def live_training_dataset_build() -> dict[str, Any]:
        recording = record_demo_spot_events(Path.cwd())
        quality = evaluate_demo_dataset_quality(recording)
        return build_training_dataset(Path.cwd(), recording, quality)

    @app.post("/api/live-training/model-validation-gate")
    def live_training_model_validation_gate() -> dict[str, Any]:
        recording = record_demo_spot_events(Path.cwd())
        quality = evaluate_demo_dataset_quality(recording)
        dataset = build_training_dataset(Path.cwd(), recording, quality)
        return evaluate_model_validation_gate(dataset)

    @app.post("/api/live-training/evidence-export")
    def live_training_evidence_export() -> dict[str, Any]:
        recording = record_demo_spot_events(Path.cwd())
        quality = evaluate_demo_dataset_quality(recording)
        dataset = build_training_dataset(Path.cwd(), recording, quality)
        validation = evaluate_model_validation_gate(dataset)
        return export_live_training_evidence(Path.cwd(), recording, quality, dataset, validation)

    @app.post("/api/app-control/live-readiness")
    def app_control_live_readiness() -> dict[str, Any]:
        profile = next(item for item in built_in_profiles() if item.mode == BotProfileMode.LIVE_LOCKED.value)
        recording = record_demo_spot_events(Path.cwd())
        quality = evaluate_demo_dataset_quality(recording)
        dataset = build_training_dataset(Path.cwd(), recording, quality)
        validation = evaluate_model_validation_gate(dataset)
        return evaluate_live_readiness_gate(profile, validation)

    @app.post("/api/app-control/evidence-export")
    def app_control_evidence_export() -> dict[str, Any]:
        payload = {"run_id": "app-control-dashboard", "profiles": default_profile_store(Path.cwd()).validate_all(), "startup": startup_health_report(Path.cwd()), "live_trading_enabled": False}
        return export_app_control_evidence(Path.cwd(), payload)

    @app.get("/api/app-control/profile-matrix")
    def app_control_profile_matrix() -> dict[str, Any]:
        return profile_matrix_report()

    @app.get("/api/live-training/health")
    def live_training_health() -> dict[str, Any]:
        return {"status": "ok", "demo_to_live_training": True, "live_execution_enabled": False, "live_trading_enabled": False}

    @app.get("/api/live-training/demo-targets")
    def live_training_demo_targets() -> dict[str, Any]:
        return {"status": "ok", "target": default_demo_session_target().__dict__, "live_trading_enabled": False}

    @app.get("/api/live-training/demo-targets/progress")
    def live_training_demo_targets_progress() -> dict[str, Any]:
        return calculate_demo_session_target_progress(default_demo_session_target(), fixture_complete_sessions())

    @app.post("/api/live-training/testnet-rehearsal/run")
    def live_training_testnet_rehearsal_run(confirm: str = "") -> dict[str, Any]:
        pipeline = run_demo_to_live_pipeline(Path.cwd(), testnet_confirm=TESTNET_REHEARSAL_CONFIRM)
        return run_testnet_rehearsal(pipeline["testnet_promotion"], confirm=confirm)

    @app.post("/api/live-training/demo-to-live/run")
    def live_training_demo_to_live_run() -> dict[str, Any]:
        return run_demo_to_live_pipeline(Path.cwd())

    @app.get("/api/live/status")
    def live_status() -> dict[str, Any]:
        return {"status": "locked", "live_execution_enabled": False, "live_order_placement_enabled": False, "live_trading_enabled": False}

    @app.get("/api/live/evidence-prerequisites")
    def live_evidence_prerequisites() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_safety_pipeline import run_live_safety_pipeline

        return run_live_safety_pipeline(Path.cwd())["evidence"]

    @app.post("/api/live/account/verify")
    def live_account_verify() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_safety_pipeline import run_live_safety_pipeline

        return run_live_safety_pipeline(Path.cwd())["account"]

    @app.post("/api/live/endpoint-policy/check")
    def live_endpoint_policy_check(phase: str = "dry_run") -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_endpoint_policy import live_endpoint_policy_report

        return live_endpoint_policy_report(phase)

    @app.post("/api/live/dry-run/start")
    def live_dry_run_start() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_safety_pipeline import run_live_safety_pipeline

        return run_live_safety_pipeline(Path.cwd())["dry_run"]

    @app.post("/api/live/order-preview")
    def live_order_preview_route() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_safety_pipeline import run_live_safety_pipeline

        return run_live_safety_pipeline(Path.cwd())["preview"]

    @app.post("/api/live/sizing-guard/check")
    def live_sizing_guard_check() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_safety_pipeline import run_live_safety_pipeline

        return run_live_safety_pipeline(Path.cwd())["sizing"]

    @app.post("/api/live/safety-drills/kill-switch")
    def live_kill_switch_drill() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_safety_pipeline import run_live_safety_pipeline

        return run_live_safety_pipeline(Path.cwd())["kill_switch_drill"]

    @app.post("/api/live/safety-drills/cancel")
    def live_cancel_drill() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_safety_pipeline import run_live_safety_pipeline

        return run_live_safety_pipeline(Path.cwd())["cancel_drill"]

    @app.post("/api/live/arm-token/create")
    def live_arm_token_create(confirm: str = "") -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_safety_pipeline import run_live_safety_pipeline

        return run_live_safety_pipeline(Path.cwd(), arm_confirm=confirm)["arm_token"]

    @app.post("/api/live/first-order/execute")
    def live_first_order_execute(confirm: str = "") -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_safety_pipeline import run_live_safety_pipeline

        return run_live_safety_pipeline(Path.cwd(), order_confirm=confirm, execute_first_order=True)["first_order"]

    @app.post("/api/live/emergency-stop")
    def live_emergency_stop() -> dict[str, Any]:
        return {"status": "ok", "state": "emergency_stopped", "disarmed": True, "live_trading_enabled": False}

    @app.get("/api/live/audit")
    def live_audit() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_safety_pipeline import run_live_safety_pipeline

        return run_live_safety_pipeline(Path.cwd())["audit"]

    @app.post("/api/live/evidence/export")
    def live_evidence_export() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_safety_pipeline import run_live_safety_pipeline

        return run_live_safety_pipeline(Path.cwd())["evidence_bundle"]

    @app.get("/api/live-session/status")
    def live_session_status() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_session_pipeline import run_controlled_live_session_pipeline

        return {"status": "locked", "pipeline": run_controlled_live_session_pipeline(Path.cwd()), "live_trading_enabled": False}

    @app.post("/api/live-session/plan/validate")
    def live_session_plan_validate() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_session_pipeline import run_controlled_live_session_pipeline

        return run_controlled_live_session_pipeline(Path.cwd())["plan"]

    @app.post("/api/live-session/create")
    def live_session_create() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_session_pipeline import run_controlled_live_session_pipeline

        return run_controlled_live_session_pipeline(Path.cwd())["session"]

    @app.post("/api/live-session/arm")
    def live_session_arm(confirm: str = "") -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_session_pipeline import run_controlled_live_session_pipeline

        return run_controlled_live_session_pipeline(Path.cwd(), arm_confirm=confirm)["arm"]

    @app.post("/api/live-session/disarm")
    def live_session_disarm() -> dict[str, Any]:
        return {"status": "ok", "state": "disarmed", "live_trading_enabled": False}

    @app.post("/api/live-session/emergency-stop")
    def live_session_emergency_stop() -> dict[str, Any]:
        return {"status": "ok", "state": "emergency_stopped", "live_trading_enabled": False}

    @app.get("/api/live-session/budget")
    def live_session_budget() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_session_pipeline import run_controlled_live_session_pipeline

        return run_controlled_live_session_pipeline(Path.cwd())["budget"]

    @app.get("/api/live-session/scaling")
    def live_session_scaling() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_session_pipeline import run_controlled_live_session_pipeline

        return run_controlled_live_session_pipeline(Path.cwd())["scaling"]

    @app.post("/api/live-session/orders/execute")
    def live_session_order_execute(confirm: str = "") -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_session_pipeline import run_controlled_live_session_pipeline

        return run_controlled_live_session_pipeline(Path.cwd(), order_confirm=confirm)["executor"]

    @app.post("/api/live-session/orders/reconcile")
    def live_session_reconcile() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_session_pipeline import run_controlled_live_session_pipeline

        return run_controlled_live_session_pipeline(Path.cwd())["reconciliation"]

    @app.get("/api/live-session/heartbeat")
    def live_session_heartbeat() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_session_pipeline import run_controlled_live_session_pipeline

        return run_controlled_live_session_pipeline(Path.cwd())["heartbeat"]

    @app.get("/api/live-session/evidence")
    def live_session_evidence() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_session_pipeline import run_controlled_live_session_pipeline

        return run_controlled_live_session_pipeline(Path.cwd())["evidence"]

    @app.get("/api/live-governance/status")
    def live_governance_status() -> dict[str, Any]:
        return {"status": "ok", "no_auto_scale": True, "live_order_submitted": False, "live_trading_enabled": False}

    @app.post("/api/live-governance/review/run")
    def live_governance_review_run() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_governance_pipeline import run_live_governance_pipeline

        return run_live_governance_pipeline(Path.cwd())["review"]

    @app.post("/api/live-governance/scorecards/generate")
    def live_governance_scorecard() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_governance_pipeline import run_live_governance_pipeline

        return run_live_governance_pipeline(Path.cwd())["scorecard"]

    @app.post("/api/live-governance/risk-calibration/run")
    def live_governance_calibration() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_governance_pipeline import run_live_governance_pipeline

        return run_live_governance_pipeline(Path.cwd())["calibration"]

    @app.post("/api/live-governance/scaling-decision")
    def live_governance_scaling_decision() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_governance_pipeline import run_live_governance_pipeline

        return run_live_governance_pipeline(Path.cwd())["scaling"]

    @app.post("/api/live-governance/approval/decide")
    def live_governance_approval_decide(confirm: str = "", note: str = "") -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_governance_pipeline import run_live_governance_pipeline

        return run_live_governance_pipeline(Path.cwd(), approval_confirm=confirm, approval_note=note)["approval"]

    @app.post("/api/live-governance/evidence/export")
    def live_governance_evidence_export() -> dict[str, Any]:
        from binance_spot_bot.live_trading.live_governance_pipeline import run_live_governance_pipeline

        return run_live_governance_pipeline(Path.cwd())["evidence"]

    @app.get("/api/live-ops/status")
    def live_ops_status() -> dict[str, Any]:
        from binance_spot_bot.live_ops.live_ops_pipeline import run_live_ops_pipeline

        pipeline = run_live_ops_pipeline(Path.cwd())
        return {
            "status": "ok",
            "open_incidents": pipeline["detected"]["count"],
            "live_order_submitted": False,
            "live_rearmed": False,
            "live_trading_enabled": False,
        }

    @app.post("/api/live-ops/incidents/detect")
    def live_ops_incident_detect() -> dict[str, Any]:
        from binance_spot_bot.live_ops.live_ops_pipeline import run_live_ops_pipeline

        return run_live_ops_pipeline(Path.cwd())["detected"]

    @app.get("/api/live-ops/incidents")
    def live_ops_incidents() -> dict[str, Any]:
        from binance_spot_bot.live_ops.live_ops_pipeline import run_live_ops_pipeline

        return run_live_ops_pipeline(Path.cwd())["detected"]

    @app.post("/api/live-ops/incidents/classify")
    def live_ops_incident_classify() -> dict[str, Any]:
        from binance_spot_bot.live_ops.live_ops_pipeline import run_live_ops_pipeline

        return run_live_ops_pipeline(Path.cwd())["classification"]

    @app.get("/api/live-ops/runbooks")
    def live_ops_runbooks() -> dict[str, Any]:
        from binance_spot_bot.live_ops.live_ops_pipeline import run_live_ops_pipeline

        return run_live_ops_pipeline(Path.cwd())["registry"]

    @app.post("/api/live-ops/runbooks/plan")
    def live_ops_runbook_plan() -> dict[str, Any]:
        from binance_spot_bot.live_ops.live_ops_pipeline import run_live_ops_pipeline

        return run_live_ops_pipeline(Path.cwd())["plan"]

    @app.post("/api/live-ops/command-center/update")
    def live_ops_command_center_update() -> dict[str, Any]:
        from binance_spot_bot.live_ops.live_ops_pipeline import run_live_ops_pipeline

        return run_live_ops_pipeline(Path.cwd())["command_center"]

    @app.post("/api/live-ops/rollback-drills/run")
    def live_ops_rollback_drill() -> dict[str, Any]:
        from binance_spot_bot.live_ops.live_ops_pipeline import run_live_ops_pipeline

        return run_live_ops_pipeline(Path.cwd())["rollback"]

    @app.post("/api/live-ops/forensics/build-timeline")
    def live_ops_forensics() -> dict[str, Any]:
        from binance_spot_bot.live_ops.live_ops_pipeline import run_live_ops_pipeline

        return run_live_ops_pipeline(Path.cwd())["timeline"]

    @app.post("/api/live-ops/root-cause/analyze")
    def live_ops_root_cause() -> dict[str, Any]:
        from binance_spot_bot.live_ops.live_ops_pipeline import run_live_ops_pipeline

        return run_live_ops_pipeline(Path.cwd())["root_cause"]

    @app.post("/api/live-ops/prevention-backlog/generate")
    def live_ops_prevention_backlog() -> dict[str, Any]:
        from binance_spot_bot.live_ops.live_ops_pipeline import run_live_ops_pipeline

        return run_live_ops_pipeline(Path.cwd())["backlog"]

    @app.post("/api/live-ops/recovery/check")
    def live_ops_recovery_check() -> dict[str, Any]:
        from binance_spot_bot.live_ops.live_ops_pipeline import run_live_ops_pipeline

        return run_live_ops_pipeline(Path.cwd())["recovery"]

    @app.post("/api/live-ops/evidence/export")
    def live_ops_evidence_export() -> dict[str, Any]:
        from binance_spot_bot.live_ops.live_ops_pipeline import run_live_ops_pipeline

        return run_live_ops_pipeline(Path.cwd())["evidence"]

    @app.get("/api/package/status")
    def package_status() -> dict[str, Any]:
        from binance_spot_bot.packaging.packaging_pipeline import run_packaging_pipeline

        pipeline = run_packaging_pipeline(Path.cwd())
        return {"status": "ok", "profile": pipeline["profiles"], "startup": pipeline["startup"], "live_trading_enabled": False}

    @app.get("/api/package/profiles")
    def package_profiles() -> dict[str, Any]:
        from binance_spot_bot.packaging.packaging_pipeline import run_packaging_pipeline

        return run_packaging_pipeline(Path.cwd())["profiles"]

    @app.post("/api/package/backup/create")
    def package_backup_create() -> dict[str, Any]:
        from binance_spot_bot.packaging.packaging_pipeline import run_packaging_pipeline

        return run_packaging_pipeline(Path.cwd())["backup"]

    @app.post("/api/package/update/plan")
    def package_update_plan() -> dict[str, Any]:
        from binance_spot_bot.packaging.packaging_pipeline import run_packaging_pipeline

        return run_packaging_pipeline(Path.cwd())["update"]

    @app.post("/api/package/rollback/preview")
    def package_rollback_preview() -> dict[str, Any]:
        from binance_spot_bot.packaging.packaging_pipeline import run_packaging_pipeline

        return run_packaging_pipeline(Path.cwd())["rollback"]

    @app.post("/api/package/recovery-kit/build")
    def package_recovery_kit() -> dict[str, Any]:
        from binance_spot_bot.packaging.packaging_pipeline import run_packaging_pipeline

        return run_packaging_pipeline(Path.cwd())["recovery_kit"]

    @app.post("/api/package/evidence/export")
    def package_evidence_export() -> dict[str, Any]:
        from binance_spot_bot.packaging.packaging_pipeline import run_packaging_pipeline

        return run_packaging_pipeline(Path.cwd())["evidence"]

    @app.get("/api/ai-doctor/status")
    def ai_doctor_status() -> dict[str, Any]:
        from binance_spot_bot.ai_doctor.ai_doctor_pipeline import run_ai_doctor_pipeline

        pipeline = run_ai_doctor_pipeline(Path.cwd())
        return {"status": "ok", "run_id": pipeline["run_id"], "issues": pipeline["issues"], "live_trading_enabled": False}

    @app.post("/api/ai-doctor/runs/start")
    def ai_doctor_start() -> dict[str, Any]:
        from binance_spot_bot.ai_doctor.ai_doctor_pipeline import run_ai_doctor_pipeline

        return run_ai_doctor_pipeline(Path.cwd())["start"]

    @app.post("/api/ai-doctor/runs/{run_id}/event")
    def ai_doctor_event(run_id: str) -> dict[str, Any]:
        from binance_spot_bot.ai_doctor.ai_doctor_pipeline import run_ai_doctor_pipeline

        return run_ai_doctor_pipeline(Path.cwd())["event"]

    @app.post("/api/ai-doctor/runs/{run_id}/finish")
    def ai_doctor_finish(run_id: str) -> dict[str, Any]:
        from binance_spot_bot.ai_doctor.ai_doctor_pipeline import run_ai_doctor_pipeline

        return run_ai_doctor_pipeline(Path.cwd())["finish"]

    @app.post("/api/ai-doctor/runs/{run_id}/collect")
    def ai_doctor_collect(run_id: str) -> dict[str, Any]:
        from binance_spot_bot.ai_doctor.ai_doctor_pipeline import run_ai_doctor_pipeline

        pipeline = run_ai_doctor_pipeline(Path.cwd())
        return {"status": "ok", "errors": pipeline["errors"], "logs": pipeline["logs"], "system_state": pipeline["system_state"], "live_trading_enabled": False}

    @app.post("/api/ai-doctor/runs/{run_id}/match-issues")
    def ai_doctor_match_issues(run_id: str) -> dict[str, Any]:
        from binance_spot_bot.ai_doctor.ai_doctor_pipeline import run_ai_doctor_pipeline

        return run_ai_doctor_pipeline(Path.cwd())["issues"]

    @app.post("/api/ai-doctor/runs/{run_id}/summary")
    def ai_doctor_summary(run_id: str) -> dict[str, Any]:
        from binance_spot_bot.ai_doctor.ai_doctor_pipeline import run_ai_doctor_pipeline

        return run_ai_doctor_pipeline(Path.cwd())["summary"]

    @app.post("/api/ai-doctor/runs/{run_id}/codex-prompt")
    def ai_doctor_codex_prompt(run_id: str) -> dict[str, Any]:
        from binance_spot_bot.ai_doctor.ai_doctor_pipeline import run_ai_doctor_pipeline

        return run_ai_doctor_pipeline(Path.cwd())["prompt"]

    @app.post("/api/ai-doctor/runs/{run_id}/export")
    def ai_doctor_export(run_id: str) -> dict[str, Any]:
        from binance_spot_bot.ai_doctor.ai_doctor_pipeline import run_ai_doctor_pipeline

        return run_ai_doctor_pipeline(Path.cwd())["debug_pack"]

    @app.post("/api/ai-doctor/runs/{run_id}/evidence")
    def ai_doctor_evidence(run_id: str) -> dict[str, Any]:
        from binance_spot_bot.ai_doctor.ai_doctor_pipeline import run_ai_doctor_pipeline

        return run_ai_doctor_pipeline(Path.cwd())["evidence"]

    @app.websocket("/ws/events")
    async def ws_events(websocket: WebSocket) -> None:
        await websocket.accept()
        await websocket.send_json(bus.heartbeat())
        await websocket.close()

    if static_dir.exists():
        @app.get("/{route_path:path}")
        def dashboard_spa_fallback(route_path: str) -> Any:
            if route_path.startswith(("api/", "ws/")):
                return {"status": "not_found", "route": route_path, "live_trading_enabled": False}
            return FileResponse(static_dir / "index.html")

    return app
