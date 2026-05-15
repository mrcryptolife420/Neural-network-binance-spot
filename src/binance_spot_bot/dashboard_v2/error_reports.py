from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


def create_dashboard_v2_error_report(
    root: Path | str = ".",
    *,
    message: str = "dashboard-v2 error",
    route: str = "/",
    context: dict[str, Any] | None = None,
    write_file: bool = True,
) -> dict[str, Any]:
    root = Path(root)
    out = root / "data" / "dashboard-v2" / "errors"
    out.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": "captured",
        "message": message,
        "route": route,
        "context": context or {},
        "playbook": "docs/dashboard-v2/troubleshooting-v2.md",
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
        "created_at_ms": int(time.time() * 1000),
    }
    safe_payload = redact_dashboard_payload(payload)
    path = out / f"dashboard-v2-error-{safe_payload['created_at_ms']}.json"
    if write_file:
        path.write_text(json.dumps(safe_payload, indent=2, default=str), encoding="utf-8")
    safe_payload["path"] = str(path)
    return safe_payload


def recent_dashboard_v2_error_reports(root: Path | str = ".", *, limit: int = 10) -> dict[str, Any]:
    root = Path(root)
    out = root / "data" / "dashboard-v2" / "errors"
    files = sorted(out.glob("dashboard-v2-error-*.json"))[-limit:] if out.exists() else []
    return redact_dashboard_payload({"status": "ok", "reports": [str(path) for path in files], "live_trading_enabled": False})
