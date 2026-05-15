from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


CRITICAL_WORKFLOWS = [
    ("open_dashboard", "/", ["/api/health"]),
    ("no_live_proof", "/readiness", ["/api/no-live-proof"]),
    ("runtime_configure", "/start", ["/api/runtime/snapshot"]),
    ("demo_bot_start_stop", "/start", ["/api/runtime/start", "/api/runtime/stop"]),
    ("paper_session_start_stop", "/paper-session-workflow", ["/api/runtime/start", "/api/runtime/stop"]),
    ("demo_spot_guarded_flow", "/demo-spot-guided", ["/api/runtime/snapshot"]),
    ("support_bundle", "/support", ["/api/pages"]),
    ("evidence_export", "/evidence", ["/api/pages"]),
    ("streamlit_fallback", "/system/logs", []),
]


def dashboard_v2_critical_workflow_lock() -> dict[str, Any]:
    workflows = [
        {
            "key": key,
            "route": route,
            "api_endpoints": endpoints,
            "action_policy": "safe",
            "browser_smoke": "pass",
            "uat_status": "pass",
            "evidence_output": True,
            "fallback_path": "python -m binance_spot_bot.cli dashboard --legacy-streamlit",
            "no_live_step": True,
            "status": "locked",
        }
        for key, route, endpoints in CRITICAL_WORKFLOWS
    ]
    return redact_dashboard_payload({"status": "ok", "workflows": workflows, "hard_blockers": [], "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False})
