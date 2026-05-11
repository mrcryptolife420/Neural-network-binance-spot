from __future__ import annotations

import io
import json
import os
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import pytest

from binance_spot_bot.cli import main as cli_main
from binance_spot_bot.exchange_profiles import BINANCE_DEMO_SPOT_PROFILE


def run_cli(argv: list[str], tmp_path: Path) -> dict:
    env = {
        "DATA_DIR": str(tmp_path / "data"),
        "AUDIT_LOG_PATH": str(tmp_path / "data" / "audit" / "events.jsonl"),
    }
    buf = io.StringIO()
    with patch.dict(os.environ, env, clear=True), patch("sys.argv", argv), redirect_stdout(buf):
        cli_main()
    return json.loads(buf.getvalue())


def test_preview_cli_works_offline(tmp_path: Path) -> None:
    payload = run_cli(["spot-bot", "demo-execution-preview", "--symbol", "BTCUSDT", "--side", "BUY", "--quote-size", "10"], tmp_path)
    assert payload["status"] == "PREVIEW_READY"
    assert payload["live_trading_enabled"] is False
    assert payload["preview"]["order"]["symbol"] == "BTCUSDT"


def test_place_cli_requires_confirmation(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        run_cli(["spot-bot", "demo-execution-place", "--symbol", "BTCUSDT", "--side", "BUY", "--quote-size", "10"], tmp_path)


def test_test_order_cli_blocks_without_credentials(tmp_path: Path) -> None:
    payload = run_cli(["spot-bot", "demo-execution-test-order", "--symbol", "BTCUSDT", "--side", "BUY", "--quote-size", "10"], tmp_path)
    assert payload["status"] == "BLOCKED"
    assert "Demo Spot" in payload["reason"] or "credentials" in payload["reason"]


def test_cancel_cli_requires_confirmation(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        run_cli(["spot-bot", "demo-execution-cancel", "--symbol", "BTCUSDT", "--order-id", "123"], tmp_path)


def test_report_cli_returns_latest_preview(tmp_path: Path) -> None:
    run_cli(["spot-bot", "demo-execution-preview", "--symbol", "BTCUSDT", "--side", "BUY", "--quote-size", "10"], tmp_path)
    payload = run_cli(["spot-bot", "demo-execution-report"], tmp_path)
    assert payload["status"] == "PREVIEW_READY"


def test_demo_profile_env_still_no_live(tmp_path: Path) -> None:
    env = {
        "DATA_DIR": str(tmp_path / "data"),
        "AUDIT_LOG_PATH": str(tmp_path / "data" / "audit" / "events.jsonl"),
        "TRADING_MODE": "testnet",
        "EXCHANGE_PROFILE": BINANCE_DEMO_SPOT_PROFILE,
        "BINANCE_API_BASE_URL": "https://demo-api.binance.com/api",
        "BINANCE_API_KEY": "demo-key",
        "BINANCE_API_SECRET": "demo-secret",
    }
    buf = io.StringIO()
    with patch.dict(os.environ, env, clear=True), patch(
        "sys.argv",
        ["spot-bot", "demo-execution-test-order", "--symbol", "BTCUSDT", "--side", "BUY", "--quote-size", "10"],
    ), redirect_stdout(buf):
        cli_main()
    payload = json.loads(buf.getvalue())
    assert payload["live_trading_enabled"] is False
