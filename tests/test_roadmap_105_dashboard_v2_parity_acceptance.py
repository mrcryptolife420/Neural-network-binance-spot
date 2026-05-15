from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from binance_spot_bot.dashboard_v2.browser_smoke import dashboard_v2_browser_smoke_matrix
from binance_spot_bot.dashboard_v2.legacy import dashboard_choice, streamlit_legacy_status
from binance_spot_bot.dashboard_v2.page_parity import (
    build_dashboard_v2_page_parity_report,
    dashboard_v2_page_parity_to_dict,
    write_dashboard_v2_page_parity_report,
)
from binance_spot_bot.dashboard_v2.performance import dashboard_v2_performance_report
from binance_spot_bot.dashboard_v2.smoke import dashboard_v2_page_parity


@dataclass(frozen=True)
class FakePage:
    key: str
    title: str
    live_trading_enabled: bool = False


def test_dashboard_v2_page_parity_all_registry_pages_are_mapped() -> None:
    report = build_dashboard_v2_page_parity_report()
    payload = dashboard_v2_page_parity_to_dict(report)

    assert payload["items"]
    assert payload["live_trading_enabled"] is False
    assert all(item["v2_route"]["path"] for item in payload["items"])
    assert all(item["no_live_statement"] for item in payload["items"])
    json.dumps(payload)


def test_dashboard_v2_page_parity_rejects_live_page() -> None:
    report = build_dashboard_v2_page_parity_report([FakePage("overview", "Overview"), FakePage("live", "Live", True)])
    payload = dashboard_v2_page_parity_to_dict(report)

    assert payload["status"] == "blocked"
    assert payload["blockers"]


def test_dashboard_v2_page_parity_warns_and_exports_report(tmp_path: Path) -> None:
    report = build_dashboard_v2_page_parity_report([FakePage("unknown_page", "Unknown")])
    payload = dashboard_v2_page_parity_to_dict(report)
    paths = write_dashboard_v2_page_parity_report(tmp_path)

    assert payload["items"][0]["migration_status"] == "legacy_placeholder"
    assert Path(paths["json"]).exists()
    assert Path(paths["markdown"]).exists()


def test_dashboard_v2_legacy_choice_performance_and_browser_matrix() -> None:
    legacy = streamlit_legacy_status()
    choice = dashboard_choice()
    performance = dashboard_v2_performance_report()
    browser = dashboard_v2_browser_smoke_matrix()
    parity = dashboard_v2_page_parity()

    assert legacy["status"] == "available"
    assert choice["recommended"] == "dashboard-v2"
    assert performance["status"] == "ok"
    assert browser["status"] == "ok"
    assert all(row["no_live_banner_visible"] for row in browser["routes"])
    assert parity["live_trading_enabled"] is False
