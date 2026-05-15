from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from binance_spot_bot.redaction import redact_payload

from .schemas import dashboard_v2_no_live_statement

CRITICAL_PAGES = {
    "overview",
    "demo_spot_trading",
    "bot_controls",
    "risk_controls",
    "market_data",
    "orders_account",
    "sessions",
    "readiness",
    "logs_security",
    "demo_pilot",
}
MIGRATED_PAGES = {
    "overview",
    "demo_spot_trading",
    "demo_pilot",
    "sessions",
    "readiness",
    "logs_security",
    "paper_os_audit",
    "stabilization",
    "operator_training",
}


@dataclass(frozen=True)
class DashboardV2RouteRef:
    path: str
    component: str
    exists: bool = True


@dataclass(frozen=True)
class DashboardV2MigrationStatus:
    status: str
    recommended_next_step: str


@dataclass(frozen=True)
class DashboardV2PageParityItem:
    page_key: str
    title: str
    streamlit_available: bool
    v2_route: DashboardV2RouteRef
    migration_status: str
    required_api_endpoints: list[str]
    required_ws_topics: list[str]
    tests: list[str]
    browser_smoke_required: bool
    no_live_statement: str
    notes: str
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class DashboardV2PageParityReport:
    status: str
    items: list[DashboardV2PageParityItem]
    warnings: list[str]
    blockers: list[str]
    parity_percent: int
    no_live_statement: str
    live_trading_enabled: bool = False


def _route_for(page_key: str) -> DashboardV2RouteRef:
    path = "/" if page_key == "overview" else f"/{page_key.replace('_', '-')}"
    return DashboardV2RouteRef(path, f"{''.join(part.title() for part in page_key.split('_'))}Page")


def _status_for(page_key: str) -> str:
    if page_key in MIGRATED_PAGES:
        return "migrated"
    if page_key in CRITICAL_PAGES:
        return "partial"
    return "legacy_placeholder"


def build_dashboard_v2_page_parity_report(pages: list[Any] | None = None) -> DashboardV2PageParityReport:
    if pages is None:
        from binance_spot_bot.ui.page_registry import PAGES

        pages = list(PAGES)
    keys = [page.key for page in pages]
    blockers: list[str] = []
    warnings: list[str] = []
    if len(keys) != len(set(keys)):
        blockers.append("duplicate page keys")
    items: list[DashboardV2PageParityItem] = []
    for page in pages:
        if getattr(page, "live_trading_enabled", False):
            blockers.append(f"live page is not allowed: {page.key}")
        status = _status_for(page.key)
        if page.key in CRITICAL_PAGES and status not in {"migrated", "partial", "legacy_placeholder"}:
            warnings.append(f"critical page needs migration status: {page.key}")
        route = _route_for(page.key)
        if not route.path:
            warnings.append(f"missing route: {page.key}")
        items.append(
            DashboardV2PageParityItem(
                page_key=page.key,
                title=page.title,
                streamlit_available=True,
                v2_route=route,
                migration_status=status,
                required_api_endpoints=["/api/runtime/snapshot"] if page.key in CRITICAL_PAGES else ["/api/pages"],
                required_ws_topics=["runtime.snapshot"] if page.key in CRITICAL_PAGES else ["system.health"],
                tests=["tests/test_roadmap_105_dashboard_v2_parity_acceptance.py"],
                browser_smoke_required=page.key in CRITICAL_PAGES,
                no_live_statement=dashboard_v2_no_live_statement(),
                notes="route available as migrated page" if status == "migrated" else "legacy placeholder keeps Streamlit fallback available",
            )
        )
    parity_percent = int(round(100 * sum(1 for item in items if item.migration_status in {"migrated", "partial"}) / max(1, len(items))))
    status = "blocked" if blockers else "warn" if warnings else "ok"
    return DashboardV2PageParityReport(status, items, warnings, blockers, parity_percent, dashboard_v2_no_live_statement())


def dashboard_v2_page_parity_to_dict(report: DashboardV2PageParityReport) -> dict[str, Any]:
    return redact_payload(asdict(report))


def write_dashboard_v2_page_parity_report(root: Path | str = ".") -> dict[str, str]:
    root = Path(root)
    payload = dashboard_v2_page_parity_to_dict(build_dashboard_v2_page_parity_report())
    out = root / "data" / "dashboard-v2" / "parity"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "dashboard_v2_page_parity.json"
    md_path = out / "dashboard_v2_page_parity.md"
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        f"# Dashboard V2 Page Parity\n\nStatus: {payload['status']}\nParity: {payload['parity_percent']}%\nLive trading: disabled\n",
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}
