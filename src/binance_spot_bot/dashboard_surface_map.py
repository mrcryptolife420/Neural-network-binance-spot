from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def build_dashboard_surface_map(root: Path | str = ".") -> dict[str, Any]:
    path = Path(root) / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py"
    text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    render_functions = sorted(dict.fromkeys(re.findall(r"def (_render_[a-zA-Z0-9_]+)\(", text)))
    subheaders = sorted(dict.fromkeys(re.findall(r"st\.subheader\(\"([^\"]+)\"", text)))
    chart_keys = sorted(dict.fromkeys(re.findall(r"key=\"([^\"]+)\"", text)))
    buttons = sorted(dict.fromkeys(re.findall(r"st\.button\(\"([^\"]+)\"", text)))
    warnings = []
    if len(chart_keys) != len(set(chart_keys)):
        warnings.append("duplicate_chart_keys")
    return {
        "status": "ready",
        "payload": {
            "render_functions": render_functions,
            "panels": subheaders,
            "chart_keys": chart_keys,
            "buttons": buttons,
            "warnings": warnings,
            "browser_smoke_required": True,
        },
        "live_trading_enabled": False,
    }


def dashboard_surface_map(pages: list[str]) -> dict[str, Any]:
    return {"status": "ready", "payload": {"pages": pages, "browser_smoke_required": True}, "live_trading_enabled": False}
