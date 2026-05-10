from __future__ import annotations

import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.config import BotSettings
from binance_spot_bot.exchange_profiles import BINANCE_DEMO_SPOT_PROFILE
from binance_spot_bot.pilot_orchestrator import now_ms
from binance_spot_bot.pilot_runner import (
    PilotCommandQueue,
    PilotHeartbeatStore,
    PilotRunnerLock,
    PilotRunnerService,
    PilotTelemetryStore,
)
from binance_spot_bot.runtime import BotRuntime, RuntimeOptions
from binance_spot_bot.types import TradingMode


class FakePilotAdapter:
    def __init__(self):
        self.cancelled: list[int] = []
        self.queries = 0
        self.accounts = 0

    def open_orders(self, symbol):
        return []

    def query_order(self, symbol, order_id=None, client_order_id=None):
        self.queries += 1
        return {"symbol": symbol, "status": "FILLED", "orderId": order_id or 1, "clientOrderId": client_order_id or "known"}

    def cancel_order(self, symbol, order_id):
        self.cancelled.append(order_id)
        return {"symbol": symbol, "orderId": order_id, "status": "CANCELED"}

    def get_account_state(self):
        self.accounts += 1
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


def lock(run_root: Path, status: str = "running", updated_at_ms: int | None = None) -> PilotRunnerLock:
    command_dir = run_root / "commands"
    telemetry_jsonl = run_root / "telemetry.jsonl"
    latest = run_root / "latest-telemetry.json"
    return PilotRunnerLock(
        runner_id="runner-1",
        run_id=run_root.name,
        pid=123,
        status=status,
        started_at_ms=now_ms(),
        updated_at_ms=updated_at_ms or now_ms(),
        command_dir=str(command_dir),
        telemetry_jsonl=str(telemetry_jsonl),
        latest_telemetry_json=str(latest),
        process_command=["python", "-m", "binance_spot_bot.cli", "pilot-runner-start"],
    )


class Roadmap021PilotRunnerTests(unittest.TestCase):
    def test_heartbeat_lock_active_and_stale_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = PilotHeartbeatStore(Path(tmp), stale_ms=10)
            fresh = store.write(lock(Path(tmp) / "run-1"))
            self.assertEqual(store.read().runner_id, fresh.runner_id)
            self.assertIsNotNone(store.active_lock())
            stale = lock(Path(tmp) / "run-1", updated_at_ms=now_ms() - 1_000)
            store.write(stale)
            self.assertTrue(store.is_stale())
            self.assertEqual(store.status_payload()["state"], "stale")

    def test_active_lock_blocks_duplicate_runner_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = demo_settings(tmp)
            service = PilotRunnerService(settings)
            service.heartbeat.write(lock(settings.data_dir / "pilot-runs" / "run-1"))
            with self.assertRaises(RuntimeError):
                service.run(max_steps=1)

    def test_telemetry_latest_and_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            telemetry = PilotTelemetryStore(Path(tmp) / "run-1")
            telemetry.append({"runner_status": "running", "api_key": "abcde" * 6})
            latest = telemetry.latest()
        self.assertEqual(latest["runner_status"], "running")
        self.assertEqual(latest["api_key"], "[REDACTED]")

    def test_command_queue_create_process_fail_ignore_and_redact(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = PilotCommandQueue(Path(tmp) / "run-1")
            pending = queue.create("reconcile", {"api_secret": "abcde" * 6})
            queue.mark(pending, "processed", {"ok": True})
            ignored = queue.create("unknown")
            queue.mark(ignored, "ignored", {"reason": "unsupported"})
            failed = queue.create("stop")
            queue.mark(failed, "failed", {"error": "boom"})
            rows = queue.all()
        self.assertEqual(rows[0]["payload"]["api_secret"], "[REDACTED]")
        self.assertEqual({row["status"] for row in rows}, {"processed", "ignored", "failed"})

    def test_runner_status_payload_without_active_runner(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = PilotRunnerService(demo_settings(tmp)).status()
        self.assertEqual(payload["runner"]["state"], "not_running")
        self.assertFalse(payload["live_trading_enabled"])

    def test_runner_service_run_writes_lock_heartbeat_telemetry_and_report(self):
        adapter = FakePilotAdapter()
        with tempfile.TemporaryDirectory() as tmp, patch("binance_spot_bot.runtime.BinanceSpotAdapter", return_value=adapter):
            service = PilotRunnerService(demo_settings(tmp))
            payload = service.run(max_steps=1)
            latest_run = service.run_store.latest()
            telemetry = PilotTelemetryStore(service.root / latest_run.run_id).latest()
        self.assertEqual(payload["runner"]["state"], "completed")
        self.assertEqual(latest_run.state, "completed")
        self.assertIn("runner_status", telemetry)
        self.assertIn("pilot_acceptance_json", latest_run.report_paths)

    def test_runner_processes_reconcile_cancel_unknown_and_stop_commands(self):
        adapter = FakePilotAdapter()
        with tempfile.TemporaryDirectory() as tmp, patch("binance_spot_bot.runtime.BinanceSpotAdapter", return_value=adapter):
            settings = demo_settings(tmp)
            service = PilotRunnerService(settings)
            runtime = BotRuntime(settings, RuntimeOptions(mode="demo", source="demo", demo_trading_armed=True))
            runtime.start()
            record = runtime.pilot_run_store.latest()
            run_root = service.root / record.run_id
            telemetry = PilotTelemetryStore(run_root)
            queue = PilotCommandQueue(run_root)
            queue.create("reconcile")
            queue.create("cancel_open_orders")
            queue.create("unknown")
            queue.create("stop")
            active_lock = lock(run_root)
            stop_requested = service._process_commands(runtime, active_lock, telemetry, queue)
            rows = queue.all()
        self.assertTrue(stop_requested)
        self.assertIn("processed", {row["status"] for row in rows})
        self.assertIn("ignored", {row["status"] for row in rows})
        self.assertEqual(runtime.status, "stopped")

    def test_clear_stale_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = PilotHeartbeatStore(Path(tmp), stale_ms=10)
            store.write(lock(Path(tmp) / "run-1", updated_at_ms=now_ms() - 1_000))
            self.assertTrue(store.clear_stale())
            self.assertEqual(store.status_payload()["state"], "not_running")


if __name__ == "__main__":
    unittest.main()
