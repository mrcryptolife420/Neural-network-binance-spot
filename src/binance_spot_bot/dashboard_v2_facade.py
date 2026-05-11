from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .local_paper_os_facade import safe_record, write_json_report


def dashboard_v2_contract() -> dict[str, Any]:
    return safe_record(
        "dashboard_v2_contract",
        {
            "backend": "fastapi-compatible-local-api",
            "frontend": "react-compatible-operator-ui",
            "transport": ["snapshot", "websocket_event"],
            "full_page_refresh_required": False,
        },
    )


def websocket_event(topic: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return safe_record("dashboard_v2_websocket_event", {"topic": topic, "payload": payload or {}, "ts_ms": int(time.time() * 1000)})


def dashboard_v2_state(snapshot: dict[str, Any]) -> dict[str, Any]:
    return safe_record("dashboard_v2_state", {"snapshot": snapshot, "managed_by_backend": True})


def parity_matrix(legacy_pages: list[str], v2_pages: list[str]) -> dict[str, Any]:
    missing = sorted(set(legacy_pages) - set(v2_pages))
    return safe_record("dashboard_v2_parity", {"missing": missing, "parity": not missing})


def packaging_plan(kind: str = "windows") -> dict[str, Any]:
    return safe_record("dashboard_v2_packaging", {"kind": kind, "one_click": True, "rollback_supported": True})


def operator_workflow(groups: list[str] | None = None) -> dict[str, Any]:
    return safe_record("dashboard_v2_operator_workflow", {"groups": groups or ["Start", "Observe", "Review", "Recover"]})


def streamlit_deprecation_plan(parity_ok: bool, tests_ok: bool) -> dict[str, Any]:
    return safe_record("streamlit_deprecation_plan", {"eligible": parity_ok and tests_ok, "legacy_kept_until_cutover": True})


def advanced_layout(panels: list[str]) -> dict[str, Any]:
    return safe_record("dashboard_v2_layout", {"panels": panels, "customizable": True, "multi_panel": len(panels) > 1})


def extension_pack(name: str, presets: list[str]) -> dict[str, Any]:
    return safe_record("dashboard_v2_extension_pack", {"name": name, "presets": presets, "pluginless": True})


def market_workbench(symbols: list[str]) -> dict[str, Any]:
    return safe_record("market_intelligence_workbench", {"symbols": [s.upper() for s in symbols], "paper_analytics_only": True})


def write_dashboard_v2_report(root: Path, name: str, payload: dict[str, Any]) -> dict[str, str]:
    return write_json_report(root, "dashboard-v2", name, payload)


def dashboard_v2_smoke_payload() -> dict[str, Any]:
    payload = {
        "contract": dashboard_v2_contract(),
        "state": dashboard_v2_state({"status": "ready"}),
        "event": websocket_event("runtime.snapshot", {"status": "ready"}),
        "live_trading_enabled": False,
    }
    json.dumps(payload, default=str)
    return payload
