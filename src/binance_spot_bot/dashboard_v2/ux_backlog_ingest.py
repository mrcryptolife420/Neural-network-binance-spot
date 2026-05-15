from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


@dataclass(frozen=True)
class DashboardV2UxFinding:
    source: str
    title: str
    category: str
    severity: str
    detail: str = ""


@dataclass(frozen=True)
class DashboardV2UxBacklogItem:
    item_id: str
    title: str
    category: str
    priority: str
    sources: list[str]
    count: int = 1
    status: str = "open"


@dataclass(frozen=True)
class DashboardV2UxBacklog:
    status: str
    items: list[DashboardV2UxBacklogItem]
    warnings: list[str] = field(default_factory=list)
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


@dataclass(frozen=True)
class DashboardV2UxIngestReport:
    status: str
    backlog: DashboardV2UxBacklog
    generated_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


INPUT_ARTIFACTS = (
    ("uat", "data/dashboard-v2/uat/feedback.json"),
    ("cutover", "data/dashboard-v2/cutover/readiness.json"),
    ("browser", "data/dashboard-v2/browser-smoke/matrix.json"),
    ("performance", "data/dashboard-v2/performance/budget.json"),
    ("docs", "data/docs/consistency.json"),
)


def _priority_for(finding: DashboardV2UxFinding) -> str:
    text = f"{finding.title} {finding.detail} {finding.category}".lower()
    if "no-live" in text or "live mode" in text or "safety" in text:
        return "UX-P0"
    if finding.severity in {"blocked", "critical"} or "critical workflow" in text:
        return "UX-P1"
    if finding.severity in {"warn", "warning"} or "friction" in text:
        return "UX-P2"
    return "UX-P3"


def _finding_from_payload(source: str, payload: dict[str, Any]) -> list[DashboardV2UxFinding]:
    findings: list[DashboardV2UxFinding] = []
    status = str(payload.get("status", "ok"))
    if status not in {"ok", "pass", "ready", "available"}:
        findings.append(DashboardV2UxFinding(source, f"{source} status {status}", "alerts_blockers", status))
    for blocker in payload.get("hard_blockers", []) or payload.get("blockers", []) or []:
        findings.append(DashboardV2UxFinding(source, str(blocker), "no_live_safety" if "live" in str(blocker).lower() else "alerts_blockers", "blocked"))
    for warning in payload.get("warnings", []) or []:
        findings.append(DashboardV2UxFinding(source, str(warning), "performance" if source == "performance" else "docs_help", "warning"))
    return findings


def ingest_dashboard_v2_ux_backlog(root: Path | str = ".", manual_findings: list[DashboardV2UxFinding] | None = None) -> DashboardV2UxIngestReport:
    root = Path(root)
    warnings: list[str] = []
    findings = list(manual_findings or [])
    for source, rel in INPUT_ARTIFACTS:
        path = root / rel
        if not path.exists():
            warnings.append(f"missing optional artifact: {rel}")
            continue
        try:
            findings.extend(_finding_from_payload(source, json.loads(path.read_text(encoding="utf-8"))))
        except json.JSONDecodeError:
            warnings.append(f"invalid json artifact: {rel}")
    grouped: dict[tuple[str, str], DashboardV2UxBacklogItem] = {}
    for finding in findings:
        key = (finding.category, finding.title.lower())
        priority = _priority_for(finding)
        current = grouped.get(key)
        if current is None:
            item_id = f"ux-{len(grouped) + 1:03d}"
            grouped[key] = DashboardV2UxBacklogItem(item_id, finding.title, finding.category, priority, [finding.source])
            continue
        sources = sorted(set(current.sources + [finding.source]))
        best_priority = min(current.priority, priority)
        grouped[key] = DashboardV2UxBacklogItem(current.item_id, current.title, current.category, best_priority, sources, current.count + 1, current.status)
    backlog = DashboardV2UxBacklog("ok", list(grouped.values()), warnings)
    return DashboardV2UxIngestReport("ok" if not any(item.priority == "UX-P0" for item in backlog.items) else "action_required", backlog)


def dashboard_v2_ux_backlog_to_dict(report: DashboardV2UxIngestReport) -> dict[str, Any]:
    return report.to_dict()


def write_dashboard_v2_ux_backlog(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    report = ingest_dashboard_v2_ux_backlog(root).to_dict()
    out = root / "data" / "dashboard-v2" / "ux"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "ux-backlog.json"
    md_path = out / "ux-backlog.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = ["# Dashboard V2 UX Backlog", "", f"Status: {report['status']}", ""]
    lines.extend(f"- {item['priority']} {item['category']}: {item['title']}" for item in report["backlog"]["items"])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"status": report["status"], "json": str(json_path), "markdown": str(md_path), "report": report, "live_trading_enabled": False}
