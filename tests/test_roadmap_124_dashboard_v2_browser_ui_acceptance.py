from __future__ import annotations

import json
import subprocess
import sys

from binance_spot_bot.dashboard_v2.app import create_dashboard_v2_app
from binance_spot_bot.dashboard_v2.launcher import dashboard_v2_launcher_report, dashboard_v2_launcher_status, dashboard_v2_launcher_stop
from binance_spot_bot.dashboard_v2.static_build import verify_dashboard_v2_static_build
from binance_spot_bot.ai_doctor.known_issue_matcher import match_known_issues
from binance_spot_bot.packaging.exe_builder import package_exe_plan, package_exe_smoke
from binance_spot_bot.packaging.portable_bundle import build_portable_bundle
from binance_spot_bot.security import scan_for_secrets


def test_dashboard_v2_static_browser_ui_is_strict_and_safe():
    payload = verify_dashboard_v2_static_build()
    assert payload["status"] == "ok", payload
    assert payload["index_exists"] is True
    assert payload["app_js_exists"] is True
    assert payload["styles_css_exists"] is True
    assert payload["manifest_exists"] is True
    assert not payload["external_refs"]
    assert not payload["secret_refs"]
    assert not payload["live_order_refs"]
    assert payload["live_trading_enabled"] is False


def test_dashboard_v2_api_contract_and_spa_routes():
    app = create_dashboard_v2_app()
    try:
        from fastapi.testclient import TestClient
    except Exception:
        return
    client = TestClient(app)
    assert client.get("/").status_code == 200
    assert "Neural Binance Spot - Dashboard V2" in client.get("/").text
    assert client.get("/ai-doctor").status_code == 200
    endpoints = [
        "/api/health",
        "/api/config",
        "/api/pages",
        "/api/runtime/snapshot",
        "/api/app-control/health",
        "/api/live-training/health",
        "/api/live/status",
        "/api/live-session/status",
        "/api/live-governance/status",
        "/api/live-ops/status",
        "/api/package/status",
        "/api/ai-doctor/status",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        assert response.headers["content-type"].startswith("application/json")
        assert response.json().get("live_trading_enabled") is False or endpoint in {"/api/pages"}


def test_dashboard_v2_launcher_scripts_and_packaging_are_safe(tmp_path):
    launch = dashboard_v2_launcher_report(tmp_path, find_free_port=True, no_browser=True)
    assert launch["status"] == "ready"
    assert launch["safe_env"]["LIVE_TRADING_ENABLED"] == "false"
    assert "dashboard_v2.app:create_dashboard_v2_app" in launch["start_command"]
    assert (tmp_path / "data" / "checks" / "dashboard-v2" / "launch-evidence.json").exists()
    assert dashboard_v2_launcher_status(tmp_path)["status"] == "ready"
    assert dashboard_v2_launcher_stop(tmp_path)["status"] == "stop_requested"
    bundle = build_portable_bundle(tmp_path)
    script = (tmp_path / "dist" / "portable" / "Neural-Binance-Spot-Bot" / "Start-Neural-Binance-Bot.cmd").read_text(encoding="utf-8")
    assert "dashboard-v2" in script
    assert "LIVE_TRADING_ENABLED=false" in script
    assert bundle["live_order_submitted"] is False
    assert package_exe_plan(tmp_path)["live_trading_enabled"] is False
    assert package_exe_smoke(tmp_path)["status"] == "ok"


def test_security_scan_ignores_venv_but_scans_source(tmp_path):
    (tmp_path / ".venv" / "Lib").mkdir(parents=True)
    (tmp_path / ".venv" / "Lib" / "ignored.py").write_text("api_key='" + "A" * 64 + "'", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "bad.py").write_text("api_key='" + "B" * 64 + "'", encoding="utf-8")
    findings = scan_for_secrets(tmp_path)
    assert len(findings) == 1
    assert findings[0][0].name == "bad.py"


def test_dashboard_v2_124_cli_smokes():
    commands = [
        ["dashboard-v2-static-verify"],
        ["dashboard-v2-launcher-report", "--find-free-port"],
        ["dashboard-v2-status"],
        ["dashboard-v2-stop"],
        ["package-exe-plan"],
        ["package-exe-smoke"],
    ]
    for command in commands:
        completed = subprocess.run([sys.executable, "-m", "binance_spot_bot.cli", *command, "--json"], text=True, capture_output=True, timeout=60)
        assert completed.returncode == 0, completed.stderr
        json.loads(completed.stdout)


def test_ai_doctor_matches_dashboard_v2_blank_ui_issues():
    payload = match_known_issues([], "blank dashboard page missing app.js WebSocket failed")
    issue_ids = {item["issue_id"] for item in payload["matches"]}
    assert "blank_dashboard_v2" in issue_ids
    assert "missing_dashboard_app_js" in issue_ids
    assert "dashboard_websocket_failed" in issue_ids
