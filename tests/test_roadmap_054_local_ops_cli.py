from __future__ import annotations

import io
import json
import os
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.cli import main as cli_main


def test_local_ops_cli_commands_return_json(tmp_path: Path) -> None:
    env = {"DATA_DIR": str(tmp_path / "data"), "AUDIT_LOG_PATH": str(tmp_path / "data" / "audit" / "events.jsonl")}
    commands = ["artifact-catalog", "diagnostics-baseline", "report-index", "support-bundles-verify", "redaction-self-test", "local-ops-snapshot", "operator-command-manifest", "evidence-manifest"]
    for command in commands:
        buf = io.StringIO()
        with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["spot-bot", command, "--json"]), redirect_stdout(buf):
            cli_main()
        payload = json.loads(buf.getvalue())
        assert payload["live_trading_enabled"] is False
