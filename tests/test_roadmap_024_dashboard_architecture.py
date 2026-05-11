from __future__ import annotations

import importlib
from pathlib import Path

from binance_spot_bot.ui.page_registry import PAGES, page_titles, validate_page_registry


ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_page_registry_is_unique_and_live_disabled() -> None:
    validate_page_registry()
    assert page_titles()[0] == "Overview"
    assert "Demo Spot Trading" in page_titles()
    assert "Demo Pilot" in page_titles()
    assert not any(page.live_trading_enabled for page in PAGES)


def test_dashboard_page_modules_import() -> None:
    for module in (
        "binance_spot_bot.ui.pages.overview",
        "binance_spot_bot.ui.pages.demo_spot_trading",
        "binance_spot_bot.ui.pages.demo_pilot",
    ):
        imported = importlib.import_module(module)
        assert imported.page_key()


def test_ui_pages_do_not_import_direct_order_execution() -> None:
    offenders: list[str] = []
    for path in (ROOT / "src" / "binance_spot_bot" / "ui").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "import place_order" in text or "import create_order" in text:
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == []


def test_dashboard_architecture_docs_exist() -> None:
    required = [
        "dashboard-architecture-contract.md",
        "dashboard-component-architecture.md",
        "dashboard-visual-regression.md",
        "dashboard-smoke-tests.md",
        "dashboard-performance-budgets.md",
        "dashboard-accessibility.md",
        "dashboard-troubleshooting.md",
    ]
    for name in required:
        assert (ROOT / "docs" / name).exists()
