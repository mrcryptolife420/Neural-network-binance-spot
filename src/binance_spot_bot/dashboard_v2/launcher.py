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
    session_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": "ready",
        "url": f"http://{host}:{selected_port}",
        "host": host,
        "port": selected_port,
        "no_browser": no_browser,
        "safe_env": {"LIVE_TRADING_ENABLED": "false", "KILL_SWITCH": "true"},
        "static_build": verify_dashboard_v2_static_build(root),
        "startup_health_wait": True,
        "session_file": str(session_dir / "last-launch.json"),
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
        "created_at_ms": int(time.time() * 1000),
    }
    safe_payload = redact_dashboard_payload(payload)
    (session_dir / "last-launch.json").write_text(json.dumps(safe_payload, indent=2), encoding="utf-8")
    return safe_payload
