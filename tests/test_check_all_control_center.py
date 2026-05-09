import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.check_all import CheckResult, payload_for
from binance_spot_bot.cli import main as cli_main
from binance_spot_bot.control_center import build_launch_plan, safe_environment, start_control_center


class CheckAllControlCenterTests(unittest.TestCase):
    def test_check_all_payload_fails_on_failed_check(self):
        payload = payload_for(
            [
                CheckResult("ok", "ok", 0),
                CheckResult("bad", "failed", 1, stderr_tail="boom"),
            ]
        )
        self.assertEqual(payload["status"], "failed")

    def test_control_center_plan_forces_safe_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = build_launch_plan(root, start_port=8800)
            env = safe_environment(root)
        self.assertFalse(plan.live_trading_enabled)
        self.assertTrue(plan.kill_switch)
        self.assertEqual(env["LIVE_TRADING_ENABLED"], "false")
        self.assertEqual(env["KILL_SWITCH"], "true")
        self.assertIn("streamlit", plan.command)

    def test_control_center_dry_run_cli_outputs_safe_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {
                "DATA_DIR": str(Path(tmp) / "data"),
                "AUDIT_LOG_PATH": str(Path(tmp) / "data" / "audit" / "events.jsonl"),
            }
            argv = ["spot-bot", "control-center", "--dry-run", "--no-browser", "--start-port", "8810"]
            buf = io.StringIO()
            with patch.dict(os.environ, env, clear=True), patch("sys.argv", argv), redirect_stdout(buf):
                cli_main()
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["status"], "planned")
        self.assertFalse(payload["live_trading_enabled"])
        self.assertTrue(payload["kill_switch"])

    def test_start_control_center_dry_run_does_not_spawn(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = start_control_center(Path(tmp), start_port=8820, open_browser=False, dry_run=True)
        self.assertEqual(result.status, "planned")
        self.assertIsNone(result.pid)


if __name__ == "__main__":
    unittest.main()
