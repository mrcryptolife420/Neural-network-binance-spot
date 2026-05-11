from __future__ import annotations

import io
import json
import os
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.cli import main as cli_main
from binance_spot_bot.dashboard_browser_smoke import analyze_dashboard_text, run_dashboard_browser_smoke


def test_dashboard_text_analysis_requires_operator_markers() -> None:
    checks = analyze_dashboard_text(
        "Neural Network Binance Spot Bot LIVE TRADING DISABLED Overview Demo Spot Trading Demo Pilot"
    )
    assert all(check["status"] == "ok" for check in checks)


def test_dashboard_text_analysis_fails_on_duplicate_element_error() -> None:
    checks = analyze_dashboard_text(
        "Neural Network Binance Spot Bot LIVE TRADING DISABLED Overview Demo Spot Trading Demo Pilot "
        "StreamlitDuplicateElementId"
    )
    assert any(check["status"] == "failed" and "StreamlitDuplicateElementId" in check["name"] for check in checks)


def test_browser_smoke_cli_writes_schema_via_service_patch() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        payload = {
            "path": str(Path(tmp) / "browser-smoke.json"),
            "status": "ok",
            "url": "http://127.0.0.1:8503",
            "browser_mode": "playwright",
            "checks": [],
            "screenshots": {"Overview": str(Path(tmp) / "overview.png")},
            "live_trading_enabled": False,
        }
        argv = ["spot-bot", "dashboard-browser-smoke", "--url", "http://127.0.0.1:8503", "--seconds", "1"]
        buf = io.StringIO()
        with patch.dict(os.environ, {"DATA_DIR": str(Path(tmp) / "data")}, clear=True), patch(
            "binance_spot_bot.dashboard_browser_smoke.run_dashboard_browser_smoke",
            return_value=payload,
        ), patch("sys.argv", argv), redirect_stdout(buf):
            cli_main()
    output = json.loads(buf.getvalue())
    assert output["status"] == "ok"
    assert output["live_trading_enabled"] is False


def test_browser_smoke_writes_failed_payload_for_missing_dashboard() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        payload = run_dashboard_browser_smoke("http://127.0.0.1:9", Path(tmp), seconds=1)
        path = Path(payload["path"])
        assert path.exists()
        assert payload["status"] == "failed"
        assert payload["live_trading_enabled"] is False
