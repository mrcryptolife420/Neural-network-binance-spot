from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .action_policy import dashboard_v2_action_matrix
from .app import create_dashboard_v2_app, dashboard_v2_pages
from .event_bus import DashboardV2EventBus
from .schemas import DashboardV2Config, DashboardV2Health, dashboard_v2_no_live_statement
from .static import dashboard_v2_static_status
from .page_parity import build_dashboard_v2_page_parity_report, dashboard_v2_page_parity_to_dict


def dashboard_v2_route_list() -> dict[str, Any]:
    routes = [
        "/api/health",
        "/api/config",
        "/api/pages",
        "/api/runtime/snapshot",
        "/api/no-live-proof",
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
        "/api/templates",
        "/api/analytics-presets",
        "/api/workflow-packs",
        "/api/market-intelligence/health",
        "/api/market-intelligence/symbol-universe",
        "/api/market-intelligence/scanner-presets",
        "/api/market-intelligence/scan/preview",
        "/api/market-intelligence/paper-analytics/preview",
        "/ws/events",
    ]
    return {"status": "ok", "routes": routes, "live_routes": [route for route in routes if "live" in route and "no-live" not in route], "live_trading_enabled": False}


def dashboard_v2_page_parity() -> dict[str, Any]:
    payload = dashboard_v2_page_parity_to_dict(build_dashboard_v2_page_parity_report())
    payload["pages"] = [
        {"key": item["page_key"], "title": item["title"], "route": item["v2_route"]["path"], "live_trading_enabled": False}
        for item in payload["items"]
    ]
    return payload


def dashboard_v2_smoke(root: Path | str = ".") -> dict[str, Any]:
    app = create_dashboard_v2_app()
    health = DashboardV2Health().to_dict()
    config = DashboardV2Config().to_dict()
    routes = dashboard_v2_route_list()
    event = DashboardV2EventBus().heartbeat()
    blockers = []
    if "live" in config["supported_modes"]:
        blockers.append("live mode exposed")
    if routes["live_routes"]:
        blockers.append("live route exposed")
    if event["live_trading_enabled"]:
        blockers.append("event enabled live trading")
    payload = {
        "status": "ok" if not blockers else "blocked",
        "app_imported": app is not None,
        "health": health,
        "config": config,
        "routes": routes,
        "pages": dashboard_v2_page_parity(),
        "action_policy": dashboard_v2_action_matrix(),
        "websocket_heartbeat": event,
        "static": dashboard_v2_static_status(root),
        "no_live_statement": dashboard_v2_no_live_statement(),
        "blockers": blockers,
        "live_trading_enabled": False,
    }
    json.dumps(payload, default=str)
    return payload
