from __future__ import annotations

from typing import Any


def page_key() -> str:
    return "demo_pilot"


def render_page(*_args: Any, **_kwargs: Any) -> dict[str, object]:
    return {"page": "demo_pilot", "status": "delegated_to_streamlit_app", "live_trading_enabled": False}
