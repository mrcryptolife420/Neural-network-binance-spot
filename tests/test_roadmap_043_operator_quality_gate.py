from __future__ import annotations

import io
import json
import os
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import pytest

from binance_spot_bot.cli import main as cli_main


def test_operator_quality_gate_cli_json_and_strict(tmp_path: Path) -> None:
    env = {"DATA_DIR": str(tmp_path / "data"), "AUDIT_LOG_PATH": str(tmp_path / "data" / "audit" / "events.jsonl")}
    buf = io.StringIO()
    with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["spot-bot", "operator-quality-gate", "--json"]), redirect_stdout(buf):
        cli_main()

    payload = json.loads(buf.getvalue())
    assert payload["live_trading_enabled"] is False
    assert payload["support_bundle_verify"]["status"] == "ok"

    with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["spot-bot", "operator-quality-gate", "--strict"]):
        with pytest.raises(SystemExit):
            cli_main()
