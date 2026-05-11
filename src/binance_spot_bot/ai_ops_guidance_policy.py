from __future__ import annotations

from typing import Any

ALLOWED = {"run diagnostics", "run check-all", "create support bundle", "verify support bundle", "open runbook", "export report", "inspect evidence", "run dashboard smoke", "run redaction self-test", "run metrics ingest", "review governance reminder", "explain", "summarize", "propose_command"}
CONFIRM = {"clear cache", "compact metrics", "archive old state", "install scheduler task", "stop local paper job", "pause paper strategy", "rollback paper policy"}
FORBIDDEN = {"enable live", "place order", "cancel real order", "query real account", "bypass risk", "reveal secret", "upload support bundle", "run arbitrary shell"}


def guidance_policy(action: str) -> dict[str, Any]:
    normalized = action.lower()
    if any(term in normalized for term in FORBIDDEN):
        klass = "forbidden"
    elif any(term in normalized for term in CONFIRM):
        klass = "confirm_required"
    elif any(term in normalized for term in ALLOWED):
        klass = "allowed"
    else:
        klass = "review_required"
    return {
        "status": "blocked" if klass == "forbidden" else "ready",
        "action": action,
        "safety_class": klass,
        "confirm_phrase": "CONFIRM_SAFE_LOCAL_ACTION" if klass == "confirm_required" else "",
        "live_trading_enabled": False,
    }
