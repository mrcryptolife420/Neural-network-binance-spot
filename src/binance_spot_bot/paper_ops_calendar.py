from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def paper_ops_calendar(jobs: list[dict[str, Any]]) -> dict[str, Any]:
    items = []
    for job in jobs:
        schedule = job.get("schedule", {})
        items.append(
            {
                "id": job.get("job_id", job.get("id", "unknown")),
                "title": job.get("name", job.get("job_id", "Local ops job")),
                "type": schedule.get("schedule_type", job.get("cadence", "manual")),
                "config": schedule.get("config", {}),
                "enabled": job.get("enabled", True),
            }
        )
    return {"status": "ready", "items": items, "live_trading_enabled": False}


def export_paper_ops_calendar(root: Path, calendar: dict[str, Any]) -> dict[str, str]:
    out = root / "local-ops" / "calendars"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "paper_ops_calendar.json"
    md_path = out / "paper_ops_calendar.md"
    ics_path = out / "paper_ops_calendar.ics"
    safe = redact_payload(calendar)
    json_path.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
    md_path.write_text(_markdown(safe), encoding="utf-8")
    ics_path.write_text(_ics(safe), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path), "ics": str(ics_path)}


def _markdown(calendar: dict[str, Any]) -> str:
    lines = ["# Paper Ops Calendar", "", "Live trading: disabled", ""]
    for item in calendar.get("items", []):
        lines.append(f"- {item['id']}: {item['type']} ({'enabled' if item.get('enabled') else 'disabled'})")
    return "\n".join(lines) + "\n"


def _ics(calendar: dict[str, Any]) -> str:
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//SpotBot//Local Paper Ops//EN"]
    for item in calendar.get("items", []):
        lines.extend(["BEGIN:VEVENT", f"UID:{item['id']}@spotbot.local", f"SUMMARY:{item['title']}", "END:VEVENT"])
    lines.append("END:VCALENDAR")
    return "\n".join(lines) + "\n"
