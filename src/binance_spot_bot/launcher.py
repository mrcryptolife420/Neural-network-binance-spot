from __future__ import annotations

import socket
import sys
from pathlib import Path


def find_free_port(start: int = 8503, host: str = "127.0.0.1", attempts: int = 50) -> int:
    for port in range(start, start + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            if sock.connect_ex((host, port)) != 0:
                return port
    raise RuntimeError(f"no free port found from {start} to {start + attempts - 1}")


def dashboard_command(project_root: Path, port: int) -> list[str]:
    return [
        sys.executable,
        "-m",
        "uvicorn",
        "binance_spot_bot.dashboard_v2.app:create_dashboard_v2_app",
        "--factory",
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
    ]
