from __future__ import annotations

import io
import json
import os
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.cli import main as cli_main
from binance_spot_bot.config import BotSettings
from binance_spot_bot.control_center import start_control_center
from binance_spot_bot.dashboard_evidence import build_operator_evidence, write_operator_evidence


def test_control_center_dry_run_writes_launch_evidence() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        result = start_control_center(Path(tmp), start_port=8840, open_browser=False, dry_run=True)
        evidence_path = Path(result.evidence_path)
        payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    assert result.status == "planned"
    assert evidence_path.name == "launch-evidence.json"
    assert payload["live_trading_enabled"] is False
    assert payload["kill_switch"] is True
    assert payload["preflight_status"] == "not_run"


def test_operator_evidence_contains_dashboard_contract_without_secrets() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        with patch.dict(os.environ, {"DATA_DIR": str(Path(tmp) / "data")}, clear=True):
            settings = BotSettings.from_env()
            payload = build_operator_evidence(
                settings,
                mode="demo",
                profile="binance-demo-spot",
                source="demo",
                connectivity={"api_key": "abcd1234efgh5678ijkl9012mnop3456"},
                runner_status={"runner": {"state": "not_running"}, "runner_health": {}, "telemetry_summary": {}, "commands": []},
            )
            path = write_operator_evidence(settings, payload)
            text = path.read_text(encoding="utf-8")
    assert payload["live_trading_enabled"] is False
    assert payload["kill_switch"] is True
    assert payload["dashboard"]["unique_chart_keys"] is True
    assert "overview" in payload["dashboard"]["pages"]
    assert "abcd1234" not in text
    assert "[REDACTED]" in text


def test_operator_evidence_cli_outputs_path_and_safe_flags() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        argv = [
            "spot-bot",
            "dashboard-operator-evidence",
            "--mode",
            "demo",
            "--profile",
            "local-demo",
            "--source",
            "demo",
        ]
        buf = io.StringIO()
        with patch.dict(os.environ, {"DATA_DIR": str(Path(tmp) / "data")}, clear=True), patch("sys.argv", argv), redirect_stdout(buf):
            cli_main()
        output = json.loads(buf.getvalue())
        assert Path(output["path"]).exists()
        assert output["live_trading_enabled"] is False
        assert output["kill_switch"] is True
