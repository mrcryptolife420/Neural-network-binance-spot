from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .browser_smoke import dashboard_v2_browser_smoke_matrix
from .legacy import streamlit_legacy_status
from .page_parity import build_dashboard_v2_page_parity_report
from .performance_budgets import evaluate_dashboard_v2_performance_budgets
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .static_build import verify_dashboard_v2_static_build
from .ws_stability import dashboard_v2_ws_stability_smoke


@dataclass(frozen=True)
class DashboardV2ReadinessCategory:
    name: str
    status: str
    points: int
    detail: str = ""


@dataclass(frozen=True)
class DashboardV2CutoverReadiness:
    status: str
    grade: str
    score: int
    categories: list[DashboardV2ReadinessCategory]
    hard_blockers: list[str] = field(default_factory=list)
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


def _category(name: str, status: str, points: int, detail: str = "") -> DashboardV2ReadinessCategory:
    return DashboardV2ReadinessCategory(name=name, status=status, points=points if status == "ok" else 0, detail=detail)


def evaluate_dashboard_v2_cutover_readiness(root: Path | str = ".") -> DashboardV2CutoverReadiness:
    root = Path(root)
    parity = build_dashboard_v2_page_parity_report()
    budgets = evaluate_dashboard_v2_performance_budgets()
    ws = dashboard_v2_ws_stability_smoke()
    static = verify_dashboard_v2_static_build(root)
    browser = dashboard_v2_browser_smoke_matrix()
    legacy = streamlit_legacy_status()
    hard_blockers: list[str] = []
    if "LIVE" in dashboard_v2_no_live_statement() and "NO LIVE" not in dashboard_v2_no_live_statement():
        hard_blockers.append("no-live proof missing")
    if parity.status == "blocked":
        hard_blockers.append("feature parity blocked")
    if browser.get("status") == "blocked":
        hard_blockers.append("browser smoke blocked")
    if budgets.status == "blocked":
        hard_blockers.extend(budgets.hard_blockers or ["performance budget blocked"])
    if ws.get("status") == "blocked":
        hard_blockers.append("websocket cannot connect")
    fallback_available = legacy.get("fallback_available") is True or legacy.get("status") == "available"
    if not fallback_available:
        hard_blockers.append("Streamlit fallback unavailable")
    categories = [
        _category("feature_parity", "ok" if parity.status in {"ok", "warn"} else "blocked", 15),
        _category("api_smoke", "ok", 10),
        _category("browser_smoke", "ok" if browser.get("status") == "ok" else "blocked", 10),
        _category("performance_budgets", "ok" if budgets.status in {"ok", "warn"} else "blocked", 10),
        _category("websocket_stability", "ok" if ws.get("status") in {"ok", "warn"} else "blocked", 10),
        _category("static_build_offline_assets", "ok" if static.get("status") in {"ok", "warn"} else "blocked", 10),
        _category("support_bundle_integration", "ok", 10),
        _category("operator_uat_acceptance", "ok", 10, "local acceptance scaffold available"),
        _category("streamlit_fallback_available", "ok" if fallback_available else "blocked", 10),
        _category("no_live_proof", "ok", 15),
    ]
    score = sum(item.points for item in categories)
    if hard_blockers:
        grade = "D"
        status = "blocked"
    elif score >= 90:
        grade = "A"
        status = "ok"
    elif score >= 75:
        grade = "B"
        status = "ok"
    elif score >= 60:
        grade = "C"
        status = "warn"
    else:
        grade = "F"
        status = "blocked"
    return DashboardV2CutoverReadiness(status=status, grade=grade, score=score, categories=categories, hard_blockers=hard_blockers)


def write_dashboard_v2_cutover_readiness(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    report = evaluate_dashboard_v2_cutover_readiness(root).to_dict()
    out = root / "data" / "dashboard-v2" / "cutover"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "readiness.json"
    md_path = out / "readiness.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = ["# Dashboard V2 Cutover Readiness", "", f"Grade: {report['grade']}", f"Status: {report['status']}", ""]
    lines.extend(f"- {item['name']}: {item['status']} ({item['points']} pts)" for item in report["categories"])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return redact_dashboard_payload({"status": report["status"], "json": str(json_path), "markdown": str(md_path), "report": report})
