from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def governance_reminders(open_items: list[str] | None = None, *, root: Path | None = None) -> dict[str, Any]:
    items = [{"id": item, "severity": "info", "reason": item} for item in (open_items or [])]
    if root is not None:
        items.extend(_filesystem_reminders(root))
    payload = {"status": "ready", "count": len(items), "reminders": items, "generated_at_ms": int(time.time() * 1000), "live_trading_enabled": False}
    return redact_payload(payload)


def write_governance_reminders(root: Path, payload: dict[str, Any]) -> Path:
    out = root / "local-ops" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "governance_reminders.json"
    path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    return path


def _filesystem_reminders(root: Path) -> list[dict[str, Any]]:
    reminders: list[dict[str, Any]] = []
    if not (root / "policy-governance" / "weekly").exists():
        reminders.append({"id": "weekly_governance_report_due", "severity": "warning", "reason": "weekly governance report missing"})
    if not (root / "checks" / "dashboard" / "browser-smoke.json").exists():
        reminders.append({"id": "browser_smoke_stale", "severity": "warning", "reason": "browser smoke evidence missing"})
    if not (root / "evidence").exists():
        reminders.append({"id": "evidence_manifest_due", "severity": "info", "reason": "evidence directory missing"})
    return reminders
