from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .redaction import redact_payload
from .stabilization_classifier import classify_stabilization_finding


@dataclass(frozen=True)
class StabilizationItem:
    item_id: str
    title: str
    priority: str
    status: str
    domain: str
    source: str = ""
    acceptance_gate: str = "standard_milestone"
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class StabilizationBacklog:
    status: str
    items: list[StabilizationItem]
    live_trading_enabled: bool = False


def build_stabilization_backlog(findings: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, StabilizationItem] = {}
    for index, finding in enumerate(findings):
        classified = classify_stabilization_finding(finding)
        title = finding.get("title", f"Finding {index}")
        key = f"{classified['priority']}:{classified['domain']}:{title}"
        grouped[key] = StabilizationItem(
            item_id=f"STAB-{len(grouped) + 1:03d}",
            title=title,
            priority=classified["priority"],
            status="new",
            domain=classified["domain"],
            source=finding.get("evidence_path", ""),
            acceptance_gate=classified["recommended_gate"],
        )
    priorities = {item.priority for item in grouped.values()}
    status = "blocked" if "P0" in priorities else "review" if grouped else "clean"
    return redact_payload(asdict(StabilizationBacklog(status, list(grouped.values()))))


def stabilization_backlog(items: list[str] | dict[str, Any]) -> dict[str, Any]:
    if isinstance(items, dict):
        findings = items.get("findings", [])
    else:
        findings = [{"title": item, "category": "manual"} for item in items]
    return build_stabilization_backlog(findings)


def write_stabilization_backlog(root: Path | str, backlog: dict[str, Any]) -> dict[str, str]:
    root = Path(root)
    out = root / "data" / "stabilization" / "backlog"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "stabilization_backlog.json"
    md_path = out / "stabilization_backlog.md"
    json_path.write_text(json.dumps(redact_payload(backlog), indent=2, default=str), encoding="utf-8")
    lines = ["# Stabilization Backlog", "", f"Status: {backlog['status']}", "Live trading: disabled", ""]
    for item in backlog["items"]:
        lines.append(f"- {item['item_id']} {item['priority']} {item['title']}")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}
