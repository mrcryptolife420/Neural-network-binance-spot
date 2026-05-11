from __future__ import annotations

from dataclasses import replace
from decimal import Decimal
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.demo_execution_sandbox import DemoExecutionSandbox, default_filters, intent_from_values
from binance_spot_bot.exchange_profiles import BINANCE_DEMO_SPOT_PROFILE
from binance_spot_bot.types import TradingMode


class FakeAdapter:
    def __init__(self) -> None:
        self.test_order_calls = 0
        self.place_order_calls = 0

    def test_order(self, order):
        self.test_order_calls += 1
        return {"status": "TEST_OK", "clientOrderId": order.client_order_id}

    def place_order(self, order):
        self.place_order_calls += 1
        return {
            "status": "NEW",
            "symbol": order.symbol,
            "side": order.side.value,
            "clientOrderId": order.client_order_id,
            "orderId": 123,
            "executedQty": "0",
            "price": "0",
        }


def demo_settings(tmp_path: Path, *, kill_switch: bool = True) -> BotSettings:
    return replace(
        BotSettings.from_env(),
        data_dir=tmp_path / "data",
        audit_log_path=tmp_path / "data" / "audit" / "events.jsonl",
        trading_mode=TradingMode.TESTNET,
        exchange_profile=BINANCE_DEMO_SPOT_PROFILE,
        binance_demo_base_url="https://demo-api.binance.com",
        binance_api_key="demo-key",
        binance_api_secret="demo-secret",
        live_trading_enabled=False,
        kill_switch=kill_switch,
    )


def test_preview_quantizes_order_and_writes_evidence(tmp_path: Path) -> None:
    sandbox = DemoExecutionSandbox(demo_settings(tmp_path))
    result = sandbox.preview(intent_from_values("BTCUSDT", "BUY", "10", "100"))
    assert result.status == "PREVIEW_READY"
    assert result.preview is not None
    assert Decimal(result.preview["order"]["quantity"]) == Decimal("0.1")
    assert Path(result.evidence_path).exists()
    assert result.live_trading_enabled is False


def test_preview_blocks_min_notional(tmp_path: Path) -> None:
    filters = default_filters("BTCUSDT")
    sandbox = DemoExecutionSandbox(demo_settings(tmp_path))
    result = sandbox.preview(intent_from_values("BTCUSDT", "BUY", "1", "100"), filters)
    assert result.status == "BLOCKED"
    assert "minNotional" in result.reason


def test_test_order_only_does_not_place_order(tmp_path: Path) -> None:
    adapter = FakeAdapter()
    sandbox = DemoExecutionSandbox(demo_settings(tmp_path), adapter=adapter)
    result = sandbox.test_order_only(intent_from_values("BTCUSDT", "BUY", "10", "100"))
    assert result.status == "TEST_ORDER_ACCEPTED"
    assert adapter.test_order_calls == 1
    assert adapter.place_order_calls == 0


def test_place_order_requires_confirmation(tmp_path: Path) -> None:
    adapter = FakeAdapter()
    sandbox = DemoExecutionSandbox(demo_settings(tmp_path, kill_switch=False), adapter=adapter)
    result = sandbox.place_demo_order(
        intent_from_values("BTCUSDT", "BUY", "10", "100"),
        confirm_demo_order=False,
        armed=True,
    )
    assert result.status == "BLOCKED"
    assert adapter.place_order_calls == 0


def test_place_order_gated_and_records_lifecycle(tmp_path: Path) -> None:
    adapter = FakeAdapter()
    sandbox = DemoExecutionSandbox(demo_settings(tmp_path, kill_switch=False), adapter=adapter)
    result = sandbox.place_demo_order(
        intent_from_values("BTCUSDT", "BUY", "10", "100"),
        confirm_demo_order=True,
        armed=True,
    )
    assert result.status == "NEW"
    assert adapter.test_order_calls == 1
    assert adapter.place_order_calls == 1
    assert result.lifecycle


def test_live_settings_are_blocked(tmp_path: Path) -> None:
    settings = replace(demo_settings(tmp_path), trading_mode=TradingMode.LIVE, live_trading_enabled=True)
    sandbox = DemoExecutionSandbox(settings, adapter=FakeAdapter())
    result = sandbox.test_order_only(intent_from_values("BTCUSDT", "BUY", "10", "100"))
    assert result.status == "BLOCKED"
    assert "live trading blocked" in result.reason
