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
        "/api/market-intelligence/policy",
        "/api/market-intelligence/symbol-universe",
        "/api/market-intelligence/scanner-presets",
        "/api/market-intelligence/scan/preview",
        "/api/market-intelligence/scan/run",
        "/api/market-intelligence/rankings/{run_id}",
        "/api/market-intelligence/paper-analytics/preview",
        "/api/market-intelligence/paper-analytics/run",
        "/api/market-intelligence/evidence",
        "/api/strategy-lab/health",
        "/api/strategy-lab/candidates",
        "/api/strategy-lab/queue/preview",
        "/api/strategy-lab/queue/create",
        "/api/strategy-lab/queues",
        "/api/strategy-lab/results",
        "/api/strategy-lab/comparison",
        "/api/strategy-lab/scorecards",
        "/api/strategy-lab/portfolio-research",
        "/api/strategy-lab/evidence-export",
        "/api/portfolio-lab/health",
        "/api/portfolio-lab/baskets/build",
        "/api/portfolio-lab/baskets",
        "/api/portfolio-lab/allocations/propose",
        "/api/portfolio-lab/allocations/validate",
        "/api/portfolio-lab/simulations/preview",
        "/api/portfolio-lab/simulations/run",
        "/api/portfolio-lab/stress-tests/run",
        "/api/portfolio-lab/scorecards",
        "/api/portfolio-lab/research-guards",
        "/api/portfolio-lab/evidence-export",
        "/api/portfolio-lab/correlation-proxy",
        "/api/portfolio-lab/robustness/health",
        "/api/portfolio-lab/walk-forward/splits/preview",
        "/api/portfolio-lab/walk-forward/splits/create",
        "/api/portfolio-lab/dataset-coverage/audit",
        "/api/portfolio-lab/rebalancing/schedules",
        "/api/portfolio-lab/rebalancing/events/simulate",
        "/api/portfolio-lab/rolling-simulation/preview",
        "/api/portfolio-lab/rolling-simulation/run",
        "/api/portfolio-lab/decay/analyze",
        "/api/portfolio-lab/replacements/simulate",
        "/api/portfolio-lab/walk-forward/performance",
        "/api/portfolio-lab/robustness/scorecards",
        "/api/portfolio-lab/robustness/governance-gate",
        "/api/portfolio-lab/walk-forward/evidence-export",
        "/api/app-control/health",
        "/api/app-control/profiles",
        "/api/app-control/profile-templates",
        "/api/app-control/config-wizard/profile",
        "/api/app-control/secret-ref-status",
        "/api/app-control/launcher/generate",
        "/api/app-control/supervisor/plan",
        "/api/app-control/data-bootstrap",
        "/api/app-control/runtime/start",
        "/api/app-control/runtime/status",
        "/api/app-control/live-readiness",
        "/api/app-control/evidence-export",
        "/api/app-control/profile-matrix",
        "/api/live-training/demo-record",
        "/api/live-training/quality",
        "/api/live-training/dataset-build",
        "/api/live-training/model-validation-gate",
        "/api/live-training/evidence-export",
        "/api/live-training/health",
        "/api/live-training/demo-targets",
        "/api/live-training/demo-targets/progress",
        "/api/live-training/testnet-rehearsal/run",
        "/api/live-training/demo-to-live/run",
        "/api/live/status",
        "/api/live/evidence-prerequisites",
        "/api/live/account/verify",
        "/api/live/endpoint-policy/check",
        "/api/live/dry-run/start",
        "/api/live/order-preview",
        "/api/live/sizing-guard/check",
        "/api/live/safety-drills/kill-switch",
        "/api/live/safety-drills/cancel",
        "/api/live/arm-token/create",
        "/api/live/first-order/execute",
        "/api/live/emergency-stop",
        "/api/live/audit",
        "/api/live/evidence/export",
        "/api/live-session/status",
        "/api/live-session/plan/validate",
        "/api/live-session/create",
        "/api/live-session/arm",
        "/api/live-session/disarm",
        "/api/live-session/emergency-stop",
        "/api/live-session/budget",
        "/api/live-session/scaling",
        "/api/live-session/orders/execute",
        "/api/live-session/orders/reconcile",
        "/api/live-session/heartbeat",
        "/api/live-session/evidence",
        "/api/live-governance/status",
        "/api/live-governance/review/run",
        "/api/live-governance/scorecards/generate",
        "/api/live-governance/risk-calibration/run",
        "/api/live-governance/scaling-decision",
        "/api/live-governance/approval/decide",
        "/api/live-governance/evidence/export",
        "/api/live-ops/status",
        "/api/live-ops/incidents/detect",
        "/api/live-ops/incidents",
        "/api/live-ops/incidents/classify",
        "/api/live-ops/runbooks",
        "/api/live-ops/runbooks/plan",
        "/api/live-ops/command-center/update",
        "/api/live-ops/rollback-drills/run",
        "/api/live-ops/forensics/build-timeline",
        "/api/live-ops/root-cause/analyze",
        "/api/live-ops/prevention-backlog/generate",
        "/api/live-ops/recovery/check",
        "/api/live-ops/evidence/export",
        "/api/package/status",
        "/api/package/profiles",
        "/api/package/backup/create",
        "/api/package/update/plan",
        "/api/package/rollback/preview",
        "/api/package/recovery-kit/build",
        "/api/package/evidence/export",
        "/api/ai-doctor/status",
        "/api/ai-doctor/runs/start",
        "/api/ai-doctor/runs/{run_id}/event",
        "/api/ai-doctor/runs/{run_id}/finish",
        "/api/ai-doctor/runs/{run_id}/collect",
        "/api/ai-doctor/runs/{run_id}/match-issues",
        "/api/ai-doctor/runs/{run_id}/summary",
        "/api/ai-doctor/runs/{run_id}/codex-prompt",
        "/api/ai-doctor/runs/{run_id}/export",
        "/api/ai-doctor/runs/{run_id}/evidence",
        "/ws/events",
    ]
    safe_live_gate_routes = ("no-live", "live-training", "live-readiness", "/api/live/", "/api/live-session/", "/api/live-governance/", "/api/live-ops/")
    live_routes = [route for route in routes if "live" in route and not any(safe in route for safe in safe_live_gate_routes)]
    return {"status": "ok", "routes": routes, "live_routes": live_routes, "live_trading_enabled": False}


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
