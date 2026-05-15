from __future__ import annotations

from typing import Any


def build_dashboard_walkthroughs(page_keys: list[str] | None = None) -> dict[str, Any]:
    if page_keys is None:
        try:
            from .ui.page_registry import PAGES

            page_keys = [page.key for page in PAGES]
        except Exception:
            page_keys = []
    walkthroughs = [
        {
            "page": key,
            "purpose": key.replace("_", " "),
            "safe_actions": ["inspect status", "export local evidence"],
            "confirm_required": [],
            "never_live": True,
            "related_cli_commands": ["dashboard-smoke"],
            "live_trading_enabled": False,
        }
        for key in page_keys
    ]
    missing = [key for key in page_keys if not key]
    return {"status": "ok" if not missing else "warn", "walkthroughs": walkthroughs, "missing": missing, "live_trading_enabled": False}


def dashboard_walkthroughs() -> dict[str, Any]:
    return build_dashboard_walkthroughs()
