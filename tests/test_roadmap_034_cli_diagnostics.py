from __future__ import annotations

import io
import json
import os
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import pytest

from binance_spot_bot.cli import main as cli_main


def test_diagnostics_cli_json_and_strict(tmp_path: Path) -> None:
    env = {"DATA_DIR": str(tmp_path / "data"), "AUDIT_LOG_PATH": str(tmp_path / "data" / "audit" / "events.jsonl")}
    buf = io.StringIO()
    with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["spot-bot", "diagnostics", "--json"]), redirect_stdout(buf):
        cli_main()

    payload = json.loads(buf.getvalue())
    assert payload["live_trading_enabled"] is False
    assert payload["status"] in {"ok", "warn", "fail"}

    with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["spot-bot", "diagnostics", "--strict"]):
        with pytest.raises(SystemExit):
            cli_main()


def test_support_bundle_cli_json(tmp_path: Path) -> None:
    env = {"DATA_DIR": str(tmp_path / "data"), "AUDIT_LOG_PATH": str(tmp_path / "data" / "audit" / "events.jsonl")}
    output = tmp_path / "bundle.zip"
    buf = io.StringIO()
    with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["spot-bot", "support-bundle", "--output", str(output), "--json"]), redirect_stdout(buf):
        cli_main()

    payload = json.loads(buf.getvalue())
    assert Path(payload["bundle"]).exists()
    assert payload["live_trading_enabled"] is False
