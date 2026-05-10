from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from binance_spot_bot.pilot_orchestrator import now_ms
from binance_spot_bot.pilot_runner import (
    PilotCommandQueue,
    PilotHeartbeatStore,
    PilotRunnerLock,
    PilotTelemetryStore,
    command_summary,
    runner_health_payload,
    stale_recovery_payload,
    telemetry_summary,
)
from binance_spot_bot.ui.charts import (
    command_status_figure,
    runner_counters_figure,
    runner_equity_pnl_figure,
    runner_heartbeat_figure,
)


def runner_lock(root: Path, status: str = "running", updated_at_ms: int | None = None) -> PilotRunnerLock:
    return PilotRunnerLock(
        runner_id="runner-1",
        run_id="run-1",
        pid=1234,
        status=status,
        started_at_ms=now_ms(),
        updated_at_ms=updated_at_ms or now_ms(),
        command_dir=str(root / "run-1" / "commands"),
        telemetry_jsonl=str(root / "run-1" / "telemetry.jsonl"),
        latest_telemetry_json=str(root / "run-1" / "latest-telemetry.json"),
    )


class Roadmap022RunnerDashboardTelemetryTests(unittest.TestCase):
    def test_telemetry_store_ignores_corrupt_lines_and_summarizes(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = PilotTelemetryStore(Path(tmp) / "run-1")
            store.append(
                {
                    "runner_status": "running",
                    "runtime_status": "running",
                    "heartbeat_age_ms": 12,
                    "equity": "1000",
                    "pnl": "0",
                    "orders": 1,
                    "rejects": 0,
                    "api_errors": 0,
                    "alerts_count": 0,
                    "reconciliation": {"status": "ok"},
                }
            )
            with store.telemetry_jsonl.open("a", encoding="utf-8") as handle:
                handle.write("{broken-json\n")
            store.append(
                {
                    "runner_status": "running",
                    "runtime_status": "running",
                    "heartbeat_age_ms": 20,
                    "equity": "1005",
                    "pnl": "5",
                    "orders": 2,
                    "rejects": 1,
                    "api_errors": 0,
                    "alerts_count": 1,
                    "reconciliation": {"status": "needs_operator_action"},
                }
            )
            rows = store.rows()
            summary = store.summary()

        self.assertEqual(len(rows), 2)
        self.assertEqual(summary["row_count"], 2)
        self.assertEqual(summary["latest_equity"], "1005")
        self.assertEqual(summary["reconciliation_status_counts"]["ok"], 1)
        self.assertEqual(summary["reconciliation_status_counts"]["needs_operator_action"], 1)

    def test_empty_telemetry_summary_is_safe(self):
        summary = telemetry_summary([])
        self.assertEqual(summary["row_count"], 0)
        self.assertEqual(summary["latest_runner_status"], "not_running")

    def test_command_summary_and_health_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = PilotCommandQueue(Path(tmp) / "run-1")
            pending = queue.create("stop")
            processed = queue.create("reconcile")
            queue.mark(processed, "processed", {"ok": True})
            failed = queue.create("cancel_open_orders")
            queue.mark(failed, "failed", {"error": "boom"})
            commands = queue.all()
            stats = command_summary(commands)
            health = runner_health_payload(
                {"state": "running", "alive": True, "stale": False, "heartbeat_age_ms": 4, "run_id": "run-1"},
                [{"timestamp_ms": now_ms(), "equity": "100", "pnl": "1", "runner_status": "running"}],
                commands,
                {"report_paths": {"pilot_acceptance_json": "report.json"}},
            )

        self.assertEqual(stats["pending"], 1)
        self.assertEqual(stats["processed"], 1)
        self.assertEqual(stats["failed"], 1)
        self.assertEqual(health["failed_commands"], 1)
        self.assertEqual(health["report_paths"], 1)
        self.assertEqual(pending["status"], "pending")

    def test_stale_recovery_payload_and_clear_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            heartbeat = PilotHeartbeatStore(Path(tmp), stale_ms=10)
            heartbeat.write(runner_lock(Path(tmp), updated_at_ms=now_ms() - 1_000))
            status = heartbeat.status_payload()
            recovery = stale_recovery_payload(status)

        self.assertTrue(status["stale"])
        self.assertTrue(recovery["stale"])
        self.assertEqual(recovery["steps"][0]["status"], "required")
        self.assertEqual(recovery["steps"][4]["status"], "available")

    def test_runner_charts_accept_empty_and_populated_data(self):
        self.assertEqual(len(runner_heartbeat_figure([]).data), 0)
        self.assertEqual(len(runner_equity_pnl_figure([]).data), 0)
        self.assertEqual(len(runner_counters_figure([]).data), 0)
        self.assertEqual(len(command_status_figure([]).data), 0)

        rows = [
            {
                "timestamp_ms": now_ms(),
                "heartbeat_age_ms": 10,
                "equity": "1000",
                "pnl": "1",
                "orders": 2,
                "rejects": 0,
                "api_errors": 0,
            }
        ]
        commands = [{"status": "processed"}, {"status": "failed"}]
        self.assertEqual(len(runner_heartbeat_figure(rows).data), 1)
        self.assertEqual(len(runner_equity_pnl_figure(rows).data), 2)
        self.assertEqual(len(runner_counters_figure(rows).data), 3)
        self.assertEqual(len(command_status_figure(commands).data), 1)

    def test_dashboard_module_imports(self):
        import binance_spot_bot.ui.streamlit_app as streamlit_app

        self.assertTrue(callable(streamlit_app.main))


if __name__ == "__main__":
    unittest.main()
