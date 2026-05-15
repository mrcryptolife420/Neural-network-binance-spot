from __future__ import annotations

import json

from binance_spot_bot.runtime_demo_pilot_service import RuntimeDemoPilotService
from binance_spot_bot.runtime_event_bus import RuntimeEvent, RuntimeEventBus
from binance_spot_bot.runtime_session_batch import RuntimeSessionBatchWriter
from binance_spot_bot.runtime_snapshot_builder import build_runtime_snapshot
from binance_spot_bot.runtime_snapshot_limits import enforce_snapshot_limits
from binance_spot_bot.runtime_state import RuntimeIdentity, RuntimeSafetyState, RuntimeState
from binance_spot_bot.runtime_step_pipeline import RuntimeStepPipeline


def test_runtime_state_snapshot_profiles_are_limited_and_redacted() -> None:
    state = RuntimeState(identity=RuntimeIdentity(symbol="ETHUSDT"), safety=RuntimeSafetyState(credential_fingerprint="abc"))
    payload = state.to_dict()
    payload["api_secret"] = "abcdefghijklmnopqrstuvwxyz"

    compact = build_runtime_snapshot(payload, profile="compact")
    limited = enforce_snapshot_limits({"items": list(range(20)), "nested": {"a": 1, "b": 2}}, max_items=3)

    assert compact["kind"] == "runtime_snapshot"
    assert compact["profile"] == "compact"
    assert "market" not in compact["payload"]
    assert "[REDACTED]" in json.dumps(build_runtime_snapshot(payload, profile="full"))
    assert limited["limited"]["items"] == [0, 1, 2]
    assert compact["live_trading_enabled"] is False


def test_runtime_event_bus_typed_and_legacy_events_have_no_execution_side_effects() -> None:
    observed: list[str] = []
    bus = RuntimeEventBus()
    bus.subscribe(lambda event: observed.append(event.event_type))

    typed = bus.publish(RuntimeEvent("runtime.started", {"secret": "abcdefghijklmnopqrstuvwxyz"}))
    legacy = bus.publish({"type": "tick", "price": 1})
    drained = bus.drain()

    assert typed["status"] == "published"
    assert legacy["status"] == "published"
    assert observed == ["runtime.started", "tick"]
    assert len(drained) == 2
    assert typed["live_trading_enabled"] is False


def test_runtime_step_pipeline_emits_stage_events_and_stops_on_failure() -> None:
    bus = RuntimeEventBus()
    pipeline = RuntimeStepPipeline(
        [
            ("market", lambda ctx: {"price": 1}),
            ("risk", lambda ctx: {"risk": "ok"}),
            ("boom", lambda ctx: (_ for _ in ()).throw(ValueError("blocked"))),
            ("after", lambda ctx: {"after": True}),
        ],
        bus,
    )

    result = pipeline.run({})
    events = bus.drain_dicts()

    assert result["status"] == "failed"
    assert [stage["name"] for stage in result["stages"]] == ["market", "risk", "boom"]
    assert [event["payload"]["stage"] for event in events] == ["market", "risk", "boom"]
    assert result["live_trading_enabled"] is False


def test_runtime_session_batch_writer_and_demo_pilot_service_are_local_only(tmp_path) -> None:
    writer = RuntimeSessionBatchWriter(tmp_path / "events.jsonl", batch_size=2)
    service = RuntimeDemoPilotService()

    writer.append(RuntimeEvent("runtime.signal", {"api_key": "abcdefghijklmnopqrstuvwxyz"}))
    result = writer.append({"type": "runtime.risk", "decision": "blocked"})
    service.record_start()
    service.record_reconciliation()

    rows = (tmp_path / "events.jsonl").read_text(encoding="utf-8").splitlines()
    assert result["status"] == "queued"
    assert len(rows) == 2
    assert "[REDACTED]" in rows[0]
    assert service.status()["counters"]["reconciliations"] == 1
    assert service.status()["live_trading_enabled"] is False
