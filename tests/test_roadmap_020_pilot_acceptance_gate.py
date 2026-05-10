from __future__ import annotations

import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.binance import BinanceAPIError
from binance_spot_bot.config import BotSettings
from binance_spot_bot.exchange_profiles import BINANCE_DEMO_SPOT_PROFILE
from binance_spot_bot.pilot_orchestrator import (
    DemoPilotOrchestrator,
    PilotRunRecord,
    PilotRunStore,
    pilot_acceptance_payload,
    transition_record,
)
from binance_spot_bot.runtime import BotRuntime, RuntimeOptions
from binance_spot_bot.session_report import export_session_report
from binance_spot_bot.session_store import SessionStore
from binance_spot_bot.types import TradingMode


class FakePilotAdapter:
    def __init__(self, open_orders=None, fail_cancel: bool = False):
        self.open = list(open_orders or [])
        self.fail_cancel = fail_cancel
        self.cancelled: list[int] = []
        self.reconcile_calls = 0
        self.account_calls = 0

    def open_orders(self, symbol):
        return list(self.open)

    def query_order(self, symbol, order_id=None, client_order_id=None):
        self.reconcile_calls += 1
        return {"symbol": symbol, "status": "FILLED", "orderId": order_id or 1, "clientOrderId": client_order_id or "known"}

    def cancel_order(self, symbol, order_id):
        if self.fail_cancel:
            raise BinanceAPIError("cancel failed", status=500, payload={"msg": "cancel failed"})
        self.cancelled.append(order_id)
        self.open = [item for item in self.open if item.get("orderId") != order_id]
        return {"symbol": symbol, "orderId": order_id, "status": "CANCELED"}

    def get_account_state(self):
        self.account_calls += 1
        return {"canTrade": True, "accountType": "SPOT", "balances": [{"asset": "USDT", "free": "100", "locked": "0"}]}

    def test_order(self, order):
        return {}

    def place_order(self, order):
        return {"symbol": order.symbol, "status": "NEW", "orderId": 10, "clientOrderId": order.client_order_id}


def demo_settings(tmp: str) -> BotSettings:
    return BotSettings(
        app_env="local",
        trading_mode=TradingMode.TESTNET,
        binance_base_url="https://api.binance.com",
        binance_testnet_base_url="https://demo-api.binance.com",
        binance_api_key="demo-key",
        binance_api_secret="demo-secret",
        live_trading_enabled=False,
        kill_switch=False,
        manual_live_approval="",
        max_daily_loss_quote=Decimal("50"),
        max_position_quote=Decimal("25"),
        max_trades_per_day=5,
        min_signal_confidence=0.1,
        max_spread_bps=Decimal("50"),
        data_dir=Path(tmp) / "data",
        audit_log_path=Path(tmp) / "data" / "audit" / "events.jsonl",
        exchange_profile=BINANCE_DEMO_SPOT_PROFILE,
        binance_demo_base_url="https://demo-api.binance.com",
    )


def valid_payload() -> dict[str, object]:
    return {
        "status": "created",
        "symbol": "BTCUSDT",
        "exchange_profile": {"name": "binance-demo-spot"},
        "credential_status": {"has_api_key": True, "has_api_secret": True, "capability": "loaded"},
        "demo_connection": {
            "profile": "binance-demo-spot",
            "base_url": "https://demo-api.binance.com",
            "armed": True,
            "connected": True,
            "authenticated": True,
            "gate": {"checks": {"filters_loaded": True, "demo_base_url": True}, "reason": "allowed"},
        },
        "demo_account": {"status": "ok", "can_trade": True},
        "demo_open_orders": [],
        "reconciliation": {"status": "ok", "orphan_orders": 0, "failures": 0, "needs_operator_action": False},
        "testnet_prechecks": {"risk_limits_set": True},
        "demo_pilot": {"config": {"pilot_name": "smoke"}, "counters": {}},
        "resume_required": False,
    }


class Roadmap020PilotAcceptanceGateTests(unittest.TestCase):
    def test_start_gate_allows_valid_demo_spot_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator = DemoPilotOrchestrator(demo_settings(tmp), PilotRunStore(Path(tmp) / "runs"))
            gate = orchestrator.evaluate_start_gate(valid_payload())
        self.assertTrue(gate["allowed"])
        self.assertEqual(gate["state"], "ready")

    def test_start_gate_blocks_wrong_profile_missing_credentials_and_orphans(self):
        payload = valid_payload()
        payload["exchange_profile"] = {"name": "local-demo"}
        payload["credential_status"] = {"has_api_key": False, "has_api_secret": False}
        payload["demo_open_orders"] = [{"orderId": 1}]
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator = DemoPilotOrchestrator(demo_settings(tmp), PilotRunStore(Path(tmp) / "runs"))
            gate = orchestrator.evaluate_start_gate(payload)
        blockers = {item["check"] for item in gate["blockers"]}
        self.assertFalse(gate["allowed"])
        self.assertIn("profile", blockers)
        self.assertIn("credentials", blockers)
        self.assertIn("no_open_orders", blockers)

    def test_state_transitions_reject_invalid_transition(self):
        record = PilotRunRecord("run-1", "idle", "binance-demo-spot", "BTCUSDT", "smoke", 1, 1)
        transition_record(record, "ready", "gate ok")
        transition_record(record, "running", "started")
        with self.assertRaises(ValueError):
            transition_record(record, "ready", "cannot go backwards")

    def test_pilot_store_redacts_and_detects_non_terminal(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = PilotRunStore(Path(tmp) / "runs")
            record = store.create_run(
                "binance-demo-spot",
                "BTCUSDT",
                "smoke",
                "blocked",
                [{"check": "credentials", "reason": "api_key=" + ("abcde" * 6)}],
            )
            loaded = store.load(record.run_id)
        self.assertEqual(loaded.blockers[0]["reason"], "[REDACTED]")

    def test_runtime_stop_flow_exports_acceptance_report(self):
        adapter = FakePilotAdapter()
        with tempfile.TemporaryDirectory() as tmp, patch("binance_spot_bot.runtime.BinanceSpotAdapter", return_value=adapter):
            runtime = BotRuntime(demo_settings(tmp), RuntimeOptions(mode="demo", demo_trading_armed=True, source="demo"))
            runtime.start()
            runtime.stop()
            acceptance = json.loads(Path(runtime.report_paths["pilot_acceptance_json"]).read_text(encoding="utf-8"))
            latest_run = runtime.pilot_run_store.latest()
        self.assertIsNotNone(latest_run)
        self.assertEqual(latest_run.state, "completed")
        self.assertIn(acceptance["final_acceptance"], {"accepted", "completed"})
        self.assertIn("start_gate", acceptance)

    def test_stop_flow_sets_resume_required_on_cancel_failure(self):
        adapter = FakePilotAdapter([{"symbol": "BTCUSDT", "side": "BUY", "status": "NEW", "orderId": 99, "clientOrderId": "known"}], fail_cancel=True)
        with tempfile.TemporaryDirectory() as tmp, patch("binance_spot_bot.runtime.BinanceSpotAdapter", return_value=adapter):
            runtime = BotRuntime(demo_settings(tmp), RuntimeOptions(mode="demo", demo_trading_armed=True, source="demo"))
            runtime.demo_pilot_config = runtime.demo_pilot_config.__class__(**{**runtime.demo_pilot_config.to_dict(), "require_clean_start": False})
            runtime.start()
            runtime.stop()
            latest_run = runtime.pilot_run_store.latest()
        self.assertEqual(latest_run.state, "resume_required")

    def test_periodic_reconciliation_and_account_sync(self):
        adapter = FakePilotAdapter()
        with tempfile.TemporaryDirectory() as tmp, patch("binance_spot_bot.runtime.BinanceSpotAdapter", return_value=adapter):
            runtime = BotRuntime(demo_settings(tmp), RuntimeOptions(mode="demo", demo_trading_armed=True, source="demo"))
            runtime._periodic_demo_pilot_maintenance(100_000)
        self.assertGreater(runtime.last_reconciliation_check_ms, 0)
        self.assertEqual(runtime.last_demo_account_sync_ms, 100_000)

    def test_acceptance_payload_and_report_are_redacted(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SessionStore(Path(tmp) / "sessions")
            session = store.start_session(
                mode="demo",
                symbol="BTCUSDT",
                interval="1m",
                model_version="baseline",
                metadata={"pilot_start_gate": {"checks": [{"check": "credentials", "reason": "api_secret=" + ("abcde" * 6)}]}},
            )
            store.record_snapshot(session.session_id, valid_payload())
            paths = export_session_report(store, session.session_id)
            payload = pilot_acceptance_payload(store.load_summary(session.session_id), store.load_events(session.session_id), [], [])
            report_text = Path(paths["pilot_acceptance_json"]).read_text(encoding="utf-8")
        self.assertIn("operator_checklist", payload)
        self.assertIn("pilot_acceptance_md", paths)
        self.assertNotIn("abcde" * 6, report_text)


if __name__ == "__main__":
    unittest.main()
