from __future__ import annotations

from typing import Any


def stabilize_dashboard_smoke(pages: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    pages = pages or []
    duplicate_keys = [page["key"] for page in pages if page.get("duplicate_key")]
    live_pages = [page["key"] for page in pages if page.get("live_trading_enabled")]
    heavy_pages = [page["key"] for page in pages if float(page.get("payload_rows", 0)) > 250]
    findings = []
    findings.extend({"page": key, "severity": "P1", "reason": "duplicate widget/chart key"} for key in duplicate_keys)
    findings.extend({"page": key, "severity": "P0", "reason": "live trading control is not allowed"} for key in live_pages)
    findings.extend({"page": key, "severity": "P2", "reason": "payload exceeds smoke budget"} for key in heavy_pages)
    return {
        "status": "blocked" if live_pages else "warn" if findings else "ok",
        "findings": findings,
        "critical_pages": [page.get("key") for page in pages if page.get("critical")],
        "no_live_badge_required": True,
        "live_trading_enabled": False,
    }


def dashboard_smoke_stabilizer() -> dict[str, Any]:
    return stabilize_dashboard_smoke([])
