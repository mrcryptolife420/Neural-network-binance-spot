from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


def dashboard_v2_guided_actions() -> dict[str, Any]:
    actions = [
        ("start_demo_bot", "Start demo bot", "/start", "python -m binance_spot_bot.cli dashboard-v2-start-wizard-smoke --json"),
        ("start_paper_session", "Start paper session", "/paper-session-workflow", "python -m binance_spot_bot.cli paper-simulation"),
        ("connect_demo_profile", "Connect demo profile", "/demo-spot-guided", "python -m binance_spot_bot.cli connectivity-check"),
        ("preview_demo_order", "Preview demo order", "/demo-spot-guided", "python -m binance_spot_bot.cli demo-execution-preview"),
        ("export_support", "Export support bundle", "/support", "python -m binance_spot_bot.cli support-bundle --json"),
        ("export_evidence", "Export operator evidence", "/evidence", "python -m binance_spot_bot.cli dashboard-v2-workflow-evidence-export --json"),
        ("run_smoke", "Run dashboard smoke", "/system/logs", "python -m binance_spot_bot.cli dashboard-smoke --seconds 1"),
        ("review_no_live", "Review no-live proof", "/readiness", "python -m binance_spot_bot.cli dashboard-v2-no-live-proof --json"),
    ]
    return redact_dashboard_payload(
        {
            "status": "ok",
            "actions": [
                {
                    "key": key,
                    "title": title,
                    "route": route,
                    "safety_label": "local demo/paper only",
                    "disabled_reason": "",
                    "related_cli": cli,
                    "live_trading_enabled": False,
                }
                for key, title, route, cli in actions
            ],
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )
