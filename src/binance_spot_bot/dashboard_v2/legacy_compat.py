from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


def dashboard_v2_legacy_compat_map() -> dict[str, Any]:
    from binance_spot_bot.ui.page_registry import PAGES

    mappings = [
        {
            "page_key": page.key,
            "streamlit_title": page.title,
            "v2_route": "/" if page.key == "overview" else f"/{page.key.replace('_', '-')}",
            "fallback_command": "python -m binance_spot_bot.cli dashboard --legacy-streamlit",
        }
        for page in PAGES
    ]
    return redact_dashboard_payload({"status": "ok", "mappings": mappings, "missing": [], "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False})
