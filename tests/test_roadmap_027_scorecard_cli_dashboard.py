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


def test_scorecard_cli_writes_latest(tmp_path: Path) -> None:
    env = {"DATA_DIR": str(tmp_path / "data"), "AUDIT_LOG_PATH": str(tmp_path / "data" / "audit" / "events.jsonl")}
    buf = io.StringIO()
    with patch.dict(os.environ, env, clear=True), patch("sys.argv", ["spot-bot", "evidence-scorecard", "--json"]), redirect_stdout(buf):
        cli_main()
    payload = json.loads(buf.getvalue())
    assert Path(payload["path"]).exists()
    assert payload["status"] == "warn"
    assert payload["live_trading_enabled"] is False


def test_scorecard_strict_fails_on_warning(tmp_path: Path) -> None:
    env = {"DATA_DIR": str(tmp_path / "data"), "AUDIT_LOG_PATH": str(tmp_path / "data" / "audit" / "events.jsonl")}
    with patch.dict(os.environ, env, clear=True), patch("sys.argv", ["spot-bot", "evidence-scorecard", "--strict"]):
        with pytest.raises(SystemExit):
            cli_main()


def test_dashboard_contains_evidence_scorecard_markers() -> None:
    text = (ROOT / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py").read_text(encoding="utf-8")
    assert "Evidence Scorecard" in text
    assert "Generate scorecard" in text
    assert "Evidence scorecard blockers" in text


def test_scorecard_docs_exist() -> None:
    assert (ROOT / "docs" / "evidence-scorecards.md").exists()
