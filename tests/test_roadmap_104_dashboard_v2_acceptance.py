from __future__ import annotations

import asyncio
import json
from decimal import Decimal

from binance_spot_bot.dashboard_v2.action_policy import evaluate_dashboard_v2_action
from binance_spot_bot.dashboard_v2.app import DashboardV2FallbackApp, create_dashboard_v2_app, dashboard_v2_pages
from binance_spot_bot.dashboard_v2.event_bus import DashboardV2EventBus
from binance_spot_bot.dashboard_v2.runtime_bridge import DashboardRuntimeBridge, DashboardRuntimeConfig
from binance_spot_bot.dashboard_v2.schemas import (
    DashboardV2ActionRequest,
    DashboardV2Config,
    DashboardV2Health,
    DashboardV2RuntimeSnapshot,
    dashboard_v2_no_live_statement,
    redact_dashboard_payload,
)
from binance_spot_bot.dashboard_v2.server import dashboard_v2_launch_plan
from binance_spot_bot.dashboard_v2.smoke import dashboard_v2_page_parity, dashboard_v2_route_list, dashboard_v2_smoke
from binance_spot_bot.dashboard_v2.state import DashboardV2Loop


def test_dashboard_v2_health_config_pages_and_no_live_contract() -> None:
    health = DashboardV2Health().to_dict()
    config = DashboardV2Config().to_dict()
    pages = dashboard_v2_pages()

    assert health["live_trading_enabled"] is False
    assert "live" not in config["supported_modes"]
    assert pages
    assert all(page["live_trading_enabled"] is False for page in pages)
    assert dashboard_v2_no_live_statement() == "LOCAL REALTIME DASHBOARD - NO LIVE TRADING"


def test_dashboard_v2_payload_redaction_decimal_and_limits() -> None:
    payload = redact_dashboard_payload({"api_key": "x" * 32, "value": Decimal("1.23")})
    snapshot = DashboardV2RuntimeSnapshot("running", "demo", "BTCUSDT", candles=[{"i": i} for i in range(300)]).to_dict(limit=10)

    assert payload["api_key"] == "[REDACTED]"
    assert payload["value"] == "1.23"
    assert len(snapshot["candles"]) == 10
    json.dumps(snapshot)


def test_dashboard_v2_runtime_bridge_blocks_live_and_produces_snapshot() -> None:
    bridge = DashboardRuntimeBridge()
    blocked = bridge.configure(DashboardRuntimeConfig(mode="live"))
    configured = bridge.configure(DashboardRuntimeConfig(mode="paper", symbol="ETHUSDT"))
    started = bridge.start()
    stepped = bridge.step()
    snapshot = bridge.snapshot()

    assert blocked["status"] == "blocked"
    assert configured["status"] == "ok"
    assert started["runtime_status"] == "running"
    assert stepped["steps"] == 1
    assert snapshot["symbol"] == "ETHUSDT"
    assert snapshot["live_trading_enabled"] is False


def test_dashboard_v2_action_policy_blocks_live_and_guards_demo_place() -> None:
    live = evaluate_dashboard_v2_action(DashboardV2ActionRequest("live.order.place", mode="live"))
    preview = evaluate_dashboard_v2_action(DashboardV2ActionRequest("demo.order.preview", mode="demo"))
    blocked_place = evaluate_dashboard_v2_action(DashboardV2ActionRequest("demo.order.place", mode="demo"), demo_armed=False)
    place = evaluate_dashboard_v2_action(DashboardV2ActionRequest("demo.order.place", mode="demo", confirm="CONFIRM_DEMO_ORDER"), demo_armed=True)

    assert live.status == "blocked"
    assert preview.status == "ok"
    assert blocked_place.status == "blocked"
    assert place.status == "ok"


def test_dashboard_v2_event_bus_subscription_redaction_and_loop() -> None:
    async def scenario() -> None:
        bus = DashboardV2EventBus(max_payload_items=3)
        queue = bus.subscribe()
        event = bus.publish("runtime.snapshot", {"api_secret": "s" * 32, "candles": list(range(10))})
        queued = await queue.get()
        bus.unsubscribe(queue)

        assert event["payload"]["api_secret"] == "[REDACTED]"
        assert event["payload"]["candles"] == [7, 8, 9]
        assert queued["topic"] == "runtime.snapshot"
        assert not bus.clients

    asyncio.run(scenario())

    bridge = DashboardRuntimeBridge()
    bus = DashboardV2EventBus()
    loop = DashboardV2Loop(bridge, bus, tick_seconds=0.01)
    assert loop.start()["status"] == "ok"
    assert loop.stop()["status"] == "ok"


def test_dashboard_v2_app_smoke_routes_parity_and_launch_plan() -> None:
    app = create_dashboard_v2_app()
    fallback = DashboardV2FallbackApp()
    smoke = dashboard_v2_smoke()
    routes = dashboard_v2_route_list()
    parity = dashboard_v2_page_parity()
    launch = dashboard_v2_launch_plan()

    assert app is not None
    assert fallback.health()["status"] == "ok"
    assert smoke["status"] == "ok"
    assert routes["live_routes"] == []
    assert parity["pages"]
    assert launch["host"] == "127.0.0.1"
    assert launch["safe_env"]["LIVE_TRADING_ENABLED"] == "false"
