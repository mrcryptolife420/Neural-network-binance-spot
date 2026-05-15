from __future__ import annotations

from typing import Any

from .guided_actions import dashboard_v2_guided_actions
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


def dashboard_v2_command_palette_smoke(query: str = "") -> dict[str, Any]:
    actions = dashboard_v2_guided_actions()["actions"]
    entries = [
        {"kind": "action", "label": action["title"], "command": action["related_cli"], "safety": action["safety_label"]}
        for action in actions
    ]
    if query:
        entries = [entry for entry in entries if query.lower() in entry["label"].lower()]
    forbidden = [entry for entry in entries if " live" in entry["label"].lower()]
    return redact_dashboard_payload(
        {
            "status": "blocked" if forbidden else "ok",
            "entries": entries,
            "forbidden_actions": forbidden,
            "copy_command_supported": True,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )
