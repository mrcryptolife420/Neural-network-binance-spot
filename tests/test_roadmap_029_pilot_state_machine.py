from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.pilot_orchestrator import DemoPilotOrchestrator, PilotRunStore
from binance_spot_bot.runtime import BotRuntime, RuntimeOptions

from tests.test_roadmap_020_pilot_acceptance_gate import FakePilotAdapter, demo_settings, valid_payload


def test_mark_running_is_idempotent_for_existing_running_run() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        orchestrator = DemoPilotOrchestrator(demo_settings(tmp), PilotRunStore(Path(tmp) / "runs"))
        first = orchestrator.mark_running(valid_payload())
        second = orchestrator.mark_running(valid_payload())

    assert first.run_id == second.run_id
    assert second.state == "running"
    assert not any(item["from"] == "running" and item["to"] == "ready" for item in second.transitions)
    assert any(item["event"] == "start_idempotent" for item in second.checkpoints)


def test_runtime_start_is_idempotent_for_running_demo_pilot() -> None:
    adapter = FakePilotAdapter()
    with tempfile.TemporaryDirectory() as tmp, patch("binance_spot_bot.runtime.BinanceSpotAdapter", return_value=adapter):
        runtime = BotRuntime(demo_settings(tmp), RuntimeOptions(mode="demo", demo_trading_armed=True, source="demo"))
        runtime.start()
        first_run_id = runtime.pilot_run_store.latest().run_id
        runtime.start()
        latest = runtime.pilot_run_store.latest()

    assert latest.run_id == first_run_id
    assert latest.state == "running"
    assert runtime.status == "running"
    assert runtime.message == "runtime already running"
    assert not any(item["from"] == "running" and item["to"] == "ready" for item in latest.transitions)


def test_stopping_run_blocks_start_without_invalid_transition() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        orchestrator = DemoPilotOrchestrator(demo_settings(tmp), PilotRunStore(Path(tmp) / "runs"))
        running = orchestrator.mark_running(valid_payload())
        orchestrator.store.transition(running.run_id, "stopping", "safe stop requested")
        blocked = orchestrator.mark_running(valid_payload())

    assert blocked.run_id == running.run_id
    assert blocked.state == "stopping"
    assert blocked.blockers[0]["check"] == "pilot_state"


def test_pilot_checkpoints_compact_large_runtime_snapshots() -> None:
    payload = valid_payload()
    payload["candles"] = [{"open_time_ms": item, "close": "1.0"} for item in range(200)]
    payload["fills"] = [{"orderId": item, "price": "1.0"} for item in range(25)]
    with tempfile.TemporaryDirectory() as tmp:
        store = PilotRunStore(Path(tmp) / "runs")
        orchestrator = DemoPilotOrchestrator(demo_settings(tmp), store)
        first = orchestrator.mark_running(payload)
        second = orchestrator.mark_running(payload)
        loaded = store.load(first.run_id)
        size = store.path_for(first.run_id).stat().st_size

    start_snapshot = next(item for item in loaded.checkpoints if item["event"] == "start_snapshot")
    idempotent = next(item for item in second.checkpoints if item["event"] == "start_idempotent")
    assert start_snapshot["payload"]["candles"]["count"] == 200
    assert start_snapshot["payload"]["fills"]["count"] == 25
    assert idempotent["payload"]["snapshot"]["candles"]["count"] == 200
    assert size < 25_000


def test_pilot_store_trims_existing_large_checkpoint_history() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = PilotRunStore(Path(tmp) / "runs")
        record = store.create_run("binance-demo-spot", "BTCUSDT", "smoke", "ready")
        record.checkpoints = [
            {
                "event": f"snapshot_{item}",
                "timestamp_ms": item,
                "payload": {"snapshot": {"symbol": "BTCUSDT", "candles": [{"close": "1.0"} for _ in range(500)]}},
            }
            for item in range(80)
        ]
        store.save(record)
        loaded = store.load(record.run_id)

    assert len(loaded.checkpoints) == 50
    assert loaded.checkpoints[-1]["payload"]["snapshot"]["candles"]["count"] == 500
