from __future__ import annotations

from typing import Any


def render_page(*_args: Any, **_kwargs: Any) -> dict[str, object]:
    return {"status": "registered", "live_trading_enabled": False}
