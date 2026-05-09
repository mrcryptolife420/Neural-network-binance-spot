from __future__ import annotations

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.alerts import AlertSeverity, WatchdogAction
from binance_spot_bot.cli import main as cli_main
from binance_spot_bot.config import BotSettings
from binance_spot_bot.evidence import EvidenceVault
from binance_spot_bot.experiment_db import ExperimentDB
from binance_spot_bot.html_reports import export_html_report
from binance_spot_bot.notebook_export import export_notebook
from binance_spot_bot.replay_sandbox import ReplaySandbox
from binance_spot_bot.runtime import BotRuntime, RuntimeOptions
from binance_spot_bot.scanner_history import ScannerHistory, ScannerRow
from binance_spot_bot.session_compare import compare_sessions
from binance_spot_bot.session_store import SessionStore
from binance_spot_bot.workspaces import WorkspaceStore


class Roadmap015OpsTests(unittest.TestCase):
    def settings(self, tmp: str) -> BotSettings:
        env = {
            "DATA_DIR": str(Path(tmp) / "data"),
            "AUDIT_LOG_PATH": str(Path(tmp) / "data" / "audit" / "events.jsonl"),
        }
        with patch.dict(os.environ, env, clear=True):
            return BotSettings.from_env()

    def test_runtime_writes_alerts_orders_and_report_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = self.settings(tmp)
            runtime = BotRuntime(settings, RuntimeOptions(mode="demo", source="demo", fetch_limit=120))
            snapshot = runtime.run_steps(80)
            runtime.stop()
            snapshot = runtime.snapshot()
            store = SessionStore(settings.data_dir / "sessions")
            alerts = store.load_events(snapshot.session_id, "alerts.jsonl")
            orders = store.load_events(snapshot.session_id, "orders.jsonl")
            self.assertTrue(alerts)
            self.assertTrue(orders)
            self.assertTrue(Path(snapshot.report_paths["summary_md"]).exists())

    def test_runtime_accounting_is_snapshot_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = BotRuntime(self.settings(tmp), RuntimeOptions(mode="demo", source="demo", fetch_limit=100))
            snapshot = runtime.run_steps(60)
        self.assertEqual(str(snapshot.paper_quote), snapshot.paper_account["quote_balance"])
        self.assertIn("fees_paid", snapshot.paper_account)

    def test_critical_alert_stops_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = BotRuntime(self.settings(tmp), RuntimeOptions(mode="demo", source="demo", fetch_limit=100))
            runtime._emit_alert("forced_stop", AlertSeverity.CRITICAL, "stop", WatchdogAction.STOP_RUNTIME)
            snapshot = runtime.run_steps(10)
        self.assertEqual(snapshot.status, "stopped")

    def test_runtime_uses_paper_mode_without_signed_adapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = BotRuntime(self.settings(tmp), RuntimeOptions(mode="demo", source="demo", fetch_limit=100))
            runtime.run_steps(20)
        self.assertFalse(runtime.execution.settings.live_trading_enabled)
        self.assertIsNone(runtime.execution.adapter)

    def test_workspace_lifecycle_create_rename_duplicate_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = WorkspaceStore(Path(tmp) / "workspaces")
            created = store.create("Demo A", data_dir="data/demo-a")
            renamed = store.rename(created.name, "Demo B")
            duplicate = store.duplicate(renamed.name, "Demo C")
            archived = store.archive(duplicate.name, confirm=True)
        self.assertEqual(renamed.name, "Demo B")
        self.assertTrue(archived.archived)

    def test_workspace_export_import_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = WorkspaceStore(root / "workspaces")
            store.create("Demo", data_dir="data/demo")
            export_path = store.export_workspace("Demo", root / "demo-workspace.json")
            other = WorkspaceStore(root / "other")
            imported = other.import_workspace(export_path)
            with self.assertRaises(FileExistsError):
                other.import_workspace(export_path)
        self.assertEqual(imported.name, "Demo")

    def test_paper_session_cli_outputs_report_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {
                "DATA_DIR": str(Path(tmp) / "data"),
                "AUDIT_LOG_PATH": str(Path(tmp) / "data" / "audit" / "events.jsonl"),
            }
            argv = ["spot-bot", "paper-session", "--minutes", "1", "--max-steps", "20", "--source", "demo"]
            buf = io.StringIO()
            with patch.dict(os.environ, env, clear=True), patch("sys.argv", argv), redirect_stdout(buf):
                cli_main()
            payload = json.loads(buf.getvalue())
        self.assertEqual(payload["mode"], "paper")
        self.assertIn("summary_md", payload["report_paths"])

    def test_scanner_history_indexes_experiment_and_exports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db = ExperimentDB(root / "experiments.json")
            history = ScannerHistory(root / "scanner.jsonl", db)
            run = history.record_run([ScannerRow("BTCUSDT", 1.0, 100.0, "BUY", 0.8)])
            html_path = export_html_report("Scanner", run, root / "scanner.html")
            notebook_path = export_notebook("Scanner", run, root / "scanner.ipynb")
            self.assertFalse(run["orders_allowed"])
            self.assertTrue(html_path.exists())
            self.assertTrue(notebook_path.exists())
            self.assertEqual(db.list()[0].kind, "scanner")

    def test_replay_and_compare_flow_reads_existing_sessions(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SessionStore(Path(tmp) / "sessions")
            first = store.start_session(mode="demo", symbol="BTCUSDT", interval="1m", model_version="m")
            second = store.start_session(mode="demo", symbol="ETHUSDT", interval="1m", model_version="m")
            store.record_snapshot(first.session_id, {"timestamp_ms": 1, "equity": "100"})
            store.record_snapshot(second.session_id, {"timestamp_ms": 1, "equity": "101"})
            replay = ReplaySandbox(store).chart_points(first.session_id)
            rows = compare_sessions(store, [first.session_id, second.session_id])
        self.assertEqual(replay[0]["equity"], "100")
        self.assertEqual(len(rows), 2)

    def test_evidence_records_and_verifies_session_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = EvidenceVault(Path(tmp) / "evidence.jsonl")
            record = vault.add("session-report", {"summary": "ok"})
            exported = vault.export(Path(tmp) / "evidence.json")
            self.assertTrue(vault.verify(record))
            self.assertTrue(exported.exists())

    def test_session_report_contains_runtime_summary_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = BotRuntime(self.settings(tmp), RuntimeOptions(mode="demo", source="demo", fetch_limit=100))
            runtime.run_steps(30)
            runtime.stop()
            summary = json.loads(Path(runtime.report_paths["summary_json"]).read_text(encoding="utf-8"))
        self.assertIn("alerts_count", summary["metadata"])
        self.assertIn("fees_paid", summary["metadata"])

    def test_profile_readiness_keeps_live_disallowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = BotRuntime(self.settings(tmp), RuntimeOptions(mode="testnet-readiness")).snapshot()
        self.assertFalse(snapshot.readiness["live_allowed"])
        self.assertTrue(snapshot.testnet_prechecks["live_disabled"])

    def test_heartbeat_events_are_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = self.settings(tmp)
            runtime = BotRuntime(settings, RuntimeOptions(mode="demo", source="demo"))
            runtime.session_store.record_heartbeat(runtime.session.session_id, {"status": "ok"})
            events = runtime.session_store.load_events(runtime.session.session_id, "heartbeats.jsonl")
        self.assertEqual(events[0]["status"], "ok")


if __name__ == "__main__":
    unittest.main()
