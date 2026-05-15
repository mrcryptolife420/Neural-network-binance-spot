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
            "/api/market-intelligence/scanner-presets",
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


def create_dashboard_v2_app(settings: BotSettings | None = None) -> Any:
    if "live" in SUPPORTED_MODES:
        raise ValueError("Dashboard V2 supported modes must not include live")
    try:
        from fastapi import FastAPI, WebSocket
        from fastapi.middleware.cors import CORSMiddleware
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

    @app.websocket("/ws/events")
    async def ws_events(websocket: WebSocket) -> None:
        await websocket.accept()
        await websocket.send_json(bus.heartbeat())
        await websocket.close()

    return app
