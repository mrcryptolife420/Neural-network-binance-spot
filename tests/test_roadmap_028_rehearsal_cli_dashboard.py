from __future__ import annotations

import io
import json
import os
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import pytest

from binance_spot_bot.cli import main as cli_main


ROOT = Path(__file__).resolve().parents[1]


def test_rehearsal_cli_writes_latest_json(tmp_path: Path) -> None:
    env = {"DATA_DIR": str(tmp_path / "data"), "AUDIT_LOG_PATH": str(tmp_path / "data" / "audit" / "events.jsonl")}
    buf = io.StringIO()
    with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["spot-bot", "demo-acceptance-rehearsal", "--json"]), redirect_stdout(buf):
        cli_main()
    payload = json.loads(buf.getvalue())
    assert payload["live_trading_enabled"] is False
    assert payload["status"] in {"warn", "pass"}
    assert (tmp_path / "data" / "evidence" / "rehearsals" / "latest.json").exists()


def test_rehearsal_cli_strict_fails_on_warning(tmp_path: Path) -> None:
    env = {"DATA_DIR": str(tmp_path / "data"), "AUDIT_LOG_PATH": str(tmp_path / "data" / "audit" / "events.jsonl")}
    with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["spot-bot", "demo-acceptance-rehearsal", "--strict"]):
        with pytest.raises(SystemExit):
            cli_main()


def test_dashboard_contains_rehearsal_markers() -> None:
    text = (ROOT / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py").read_text(encoding="utf-8")
    assert "Demo Acceptance Rehearsal" in text
    assert "Run rehearsal" in text
    assert "Rehearsal trend" in text


def test_rehearsal_docs_exist() -> None:
    assert (ROOT / "docs" / "demo-acceptance-rehearsal.md").exists()
