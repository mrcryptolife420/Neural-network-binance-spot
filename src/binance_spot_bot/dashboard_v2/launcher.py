from __future__ import annotations

import json
import socket
import time
from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .static_build import verify_dashboard_v2_static_build


def _find_free_port(host: str, start_port: int) -> int:
    for port in range(start_port, start_port + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.05)
            if sock.connect_ex((host, port)) != 0:
                return port
    raise RuntimeError("no free localhost port found")


def dashboard_v2_launcher_report(
    root: Path | str = ".",
    *,
    host: str = "127.0.0.1",
    port: int = 8800,
    no_browser: bool = False,
    find_free_port: bool = False,
) -> dict[str, Any]:
    if host not in {"127.0.0.1", "localhost"}:
        return {
            "status": "blocked",
            "reason": "Dashboard V2 launcher only supports localhost by default",
            "live_trading_enabled": False,
        }
    root = Path(root)
    selected_port = _find_free_port(host, port) if find_free_port else port
    session_dir = root / "data" / "dashboard-v2" / "launcher"
    checks_dir = root / "data" / "checks" / "dashboard-v2"
    logs_dir = root / "data" / "logs"
    session_dir.mkdir(parents=True, exist_ok=True)
    checks_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": "ready",
        "url": f"http://{host}:{selected_port}",
        "host": host,
        "port": selected_port,
        "no_browser": no_browser,
        "safe_env": {"LIVE_TRADING_ENABLED": "false", "KILL_SWITCH": "true"},
        "start_command": f"python -m uvicorn binance_spot_bot.dashboard_v2.app:create_dashboard_v2_app --factory --host {host} --port {selected_port}",
        "static_build": verify_dashboard_v2_static_build(root),
        "startup_health_wait": True,
        "session_file": str(session_dir / "last-launch.json"),
        "stdout_log": str(logs_dir / "dashboard-v2.log"),
        "stderr_log": str(logs_dir / "dashboard-v2.err.log"),
        "launch_evidence": str(checks_dir / "launch-evidence.json"),
        "backend_health_url": f"http://{host}:{selected_port}/api/health",
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
        "created_at_ms": int(time.time() * 1000),
    }
    safe_payload = redact_dashboard_payload(payload)
    (session_dir / "last-launch.json").write_text(json.dumps(safe_payload, indent=2), encoding="utf-8")
    (checks_dir / "launch-evidence.json").write_text(json.dumps(safe_payload, indent=2), encoding="utf-8")
    return safe_payload


def dashboard_v2_launcher_status(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    session_file = root / "data" / "dashboard-v2" / "launcher" / "last-launch.json"
    if not session_file.exists():
        return {"status": "not_started", "live_trading_enabled": False}
    return redact_dashboard_payload(json.loads(session_file.read_text(encoding="utf-8")))


def dashboard_v2_launcher_stop(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    session_dir = root / "data" / "dashboard-v2" / "launcher"
    session_dir.mkdir(parents=True, exist_ok=True)
    payload = {"status": "stop_requested", "session_file": str(session_dir / "last-launch.json"), "live_trading_enabled": False, "live_order_submitted": False}
    (session_dir / "last-stop.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
