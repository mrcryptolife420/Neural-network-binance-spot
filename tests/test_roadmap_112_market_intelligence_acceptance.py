import json
import tempfile
from pathlib import Path

import pytest

from binance_spot_bot.dashboard_v2.app import DashboardV2FallbackApp, create_dashboard_v2_app, dashboard_v2_pages
from binance_spot_bot.dashboard_v2.widget_registry import widget_registry_payload
from binance_spot_bot.market_intelligence.market_snapshot_cache import default_market_snapshot_cache
from binance_spot_bot.market_intelligence.multi_symbol_paper_analytics import run_multi_symbol_paper_analytics
from binance_spot_bot.market_intelligence.public_endpoint_policy import (
    assert_public_market_endpoint,
    check_market_intelligence_endpoint,
    write_public_endpoint_policy_report,
)
from binance_spot_bot.market_intelligence.rate_limit_budget import scanner_rate_limit_plan
from binance_spot_bot.market_intelligence.scanner_evidence_bundle import export_market_intelligence_evidence
from binance_spot_bot.market_intelligence.scanner_presets import scanner_presets_payload
from binance_spot_bot.market_intelligence.symbol_ranking import rank_symbols
from binance_spot_bot.market_intelligence.symbol_universe import build_symbol_universe, symbol_universe_to_dict
from binance_spot_bot.market_intelligence.watchlist_scanner import run_watchlist_scan


def test_public_endpoint_policy_allows_market_data_and_blocks_signed_routes():
    assert check_market_intelligence_endpoint("get_exchange_info").status == "allowed"
    assert check_market_intelligence_endpoint("get_klines").status == "allowed"
    assert check_market_intelligence_endpoint("place_order").status == "blocked"
    assert check_market_intelligence_endpoint("get_account_state").signed_or_account_endpoint is True
    assert check_market_intelligence_endpoint("unknown_future_endpoint").status == "blocked"
    with pytest.raises(ValueError):
        assert_public_market_endpoint("cancel_order")


def test_symbol_universe_cache_scanner_metrics_rankings_and_presets_are_local_only():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        universe = symbol_universe_to_dict(build_symbol_universe())
        assert universe["status"] == "ok"
        assert universe["count"] >= 5
        assert universe["live_trading_enabled"] is False

        cache_report = default_market_snapshot_cache(root).seed_demo(["BTCUSDT", "ETHUSDT"])
        assert cache_report["status"] == "ok"

        presets = scanner_presets_payload()
        assert presets["status"] == "ok"
        assert {item["preset_id"] for item in presets["presets"]} >= {"majors_overview", "low_spread_liquidity", "paper_strategy_candidates"}

        plan = scanner_rate_limit_plan(["BTCUSDT", "ETHUSDT"])
        assert plan["status"] == "ok"
        assert plan["live_trading_enabled"] is False

        scan = run_watchlist_scan(["BTCUSDT", "ETHUSDT"], root=root)
        assert scan["status"] == "ok"
        assert len(scan["metrics"]) == 2
        assert all(item["symbol"].endswith("USDT") for item in scan["metrics"])

        ranking = rank_symbols(list(scan["metrics"]), "highest_quote_volume")
        assert ranking["status"] == "ok"
        assert ranking["ranks"]
        assert "financial advice" in ranking["no_financial_advice_statement"].lower()
        assert rank_symbols([{"symbol": "buy now", "quote_volume_24h": "1"}])["status"] == "blocked"


def test_multi_symbol_paper_analytics_evidence_and_reports_are_secret_free():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        policy = write_public_endpoint_policy_report(root)
        assert policy["status"] == "ok"
        analytics = run_multi_symbol_paper_analytics(["BTCUSDT", "ETHUSDT"], root=root)
        assert analytics["status"] == "ok"
        assert all(item["paper_only"] for item in analytics["symbols"])
        assert run_multi_symbol_paper_analytics(["BTCUSDT"], root=root, confirm="LIVE")["status"] == "blocked"

        evidence = export_market_intelligence_evidence(root)
        assert evidence["status"] == "ok"
        manifest = Path(evidence["manifest"]).read_text(encoding="utf-8")
        assert "MARKET INTELLIGENCE - NO LIVE TRADING" in manifest
        assert "live_trading_enabled" in manifest
        assert "api_key" not in manifest.lower()
        json.loads(manifest)


def test_dashboard_v2_market_intelligence_routes_widgets_and_api_are_no_live():
    pages = dashboard_v2_pages()
    assert any(item["route"] == "/market-intelligence" for item in pages)
    widgets = widget_registry_payload()
    widget_types = {item["widget_type"] for item in widgets["widgets"]}
    assert {"market_scanner_health", "public_endpoint_policy", "market_ranking_table", "multi_symbol_paper_analytics", "scanner_evidence"} <= widget_types

    fallback = DashboardV2FallbackApp()
    assert fallback.market_intelligence_health()["live_trading_enabled"] is False
    assert fallback.market_intelligence_policy()["live_trading_enabled"] is False

    app = create_dashboard_v2_app()
    try:
        from fastapi.testclient import TestClient
    except Exception:
        return
    if isinstance(app, DashboardV2FallbackApp):
        return
    client = TestClient(app)
    assert client.get("/api/market-intelligence/health").json()["public_data_only"] is True
    assert client.get("/api/market-intelligence/policy").json()["live_trading_enabled"] is False
    assert client.get("/api/market-intelligence/symbol-universe").json()["count"] >= 5
    assert client.get("/api/market-intelligence/scanner-presets").json()["status"] == "ok"
    assert client.post("/api/market-intelligence/scan/preview?preset=majors_overview").json()["status"] == "ok"
    scan = client.post("/api/market-intelligence/scan/run?preset=majors_overview").json()
    assert scan["status"] == "ok"
    assert client.get(f"/api/market-intelligence/rankings/{scan['run_id']}").json()["status"] == "ok"
    assert client.post("/api/market-intelligence/paper-analytics/preview").json()["status"] == "ok"
    assert client.get("/api/market-intelligence/evidence").json()["status"] == "ok"
