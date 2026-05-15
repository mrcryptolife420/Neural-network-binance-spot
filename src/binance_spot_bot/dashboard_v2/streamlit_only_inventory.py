from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


RENDER_RE = re.compile(r"def (_render_[a-zA-Z0-9_]+)\(")


def dashboard_v2_streamlit_only_inventory(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    path = root / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    renders = sorted(set(RENDER_RE.findall(text)))
    return redact_dashboard_payload(
        {
            "status": "ok",
            "render_functions": [{"name": name, "critical": any(key in name for key in ("demo", "paper", "support", "evidence"))} for name in renders],
            "streamlit_only_pages": [],
            "streamlit_only_actions": [],
            "report_path": str(path),
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )


def write_dashboard_v2_streamlit_only_inventory(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    payload = dashboard_v2_streamlit_only_inventory(root)
    out = root / "data" / "dashboard-v2" / "deprecation"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "streamlit-only-inventory.json"
    md_path = out / "streamlit-only-inventory.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(f"# Streamlit Only Inventory\n\nRender functions: {len(payload['render_functions'])}\n", encoding="utf-8")
    return {"status": "ok", "json": str(json_path), "markdown": str(md_path), "report": payload, "live_trading_enabled": False}
