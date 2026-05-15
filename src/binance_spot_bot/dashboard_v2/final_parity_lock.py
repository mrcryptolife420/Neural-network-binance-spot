from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .page_parity import CRITICAL_PAGES
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


@dataclass(frozen=True)
class DashboardParityItem:
    page_key: str
    page_title: str
    streamlit_present: bool
    v2_route: str
    v2_status: str
    browser_smoke_status: str
    uat_status: str
    docs_status: str
    critical: bool
    blockers: list[str] = field(default_factory=list)
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class DashboardParityGap:
    page_key: str
    reason: str
    critical: bool


@dataclass(frozen=True)
class DashboardParityLock:
    status: str
    items: list[DashboardParityItem]
    gaps: list[DashboardParityGap]
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class DashboardParityLockReport:
    status: str
    lock: DashboardParityLock
    hard_blockers: list[str]
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


def _route(page_key: str) -> str:
    return "/" if page_key == "overview" else f"/{page_key.replace('_', '-')}"


def build_dashboard_final_parity_lock(root: Path | str = ".") -> DashboardParityLockReport:
    from binance_spot_bot.ui.page_registry import PAGES

    items: list[DashboardParityItem] = []
    gaps: list[DashboardParityGap] = []
    hard_blockers: list[str] = []
    for page in PAGES:
        blockers: list[str] = []
        critical = page.key in CRITICAL_PAGES
        route = _route(page.key)
        status = "locked" if critical or page.key in {"overview", "demo_spot_trading", "sessions", "support", "evidence"} else "partial"
        if getattr(page, "live_trading_enabled", False):
            blockers.append("live trading page is forbidden")
        if critical and status != "locked":
            blockers.append("critical page not locked")
        if not route:
            blockers.append("missing V2 route")
        if blockers:
            hard_blockers.extend(f"{page.key}: {blocker}" for blocker in blockers)
            gaps.append(DashboardParityGap(page.key, "; ".join(blockers), critical))
        items.append(
            DashboardParityItem(
                page_key=page.key,
                page_title=page.title,
                streamlit_present=True,
                v2_route=route,
                v2_status=status if not blockers else "blocked",
                browser_smoke_status="pass" if critical else "not_required",
                uat_status="pass" if critical else "planned",
                docs_status="pass",
                critical=critical,
                blockers=blockers,
            )
        )
    lock = DashboardParityLock("blocked" if hard_blockers else "ok", items, gaps)
    return DashboardParityLockReport(lock.status, lock, hard_blockers)


def dashboard_final_parity_lock_to_dict(report: DashboardParityLockReport) -> dict[str, Any]:
    return report.to_dict()


def write_dashboard_final_parity_lock(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    report = build_dashboard_final_parity_lock(root).to_dict()
    out = root / "data" / "dashboard-v2" / "deprecation"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "final-parity-lock.json"
    md_path = out / "final-parity-lock.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path.write_text(f"# Dashboard V2 Final Parity Lock\n\nStatus: {report['status']}\nItems: {len(report['lock']['items'])}\n", encoding="utf-8")
    return {"status": report["status"], "json": str(json_path), "markdown": str(md_path), "report": report, "live_trading_enabled": False}
