from __future__ import annotations

from typing import Any

from .launcher import dashboard_v2_launcher_report


def dashboard_v2_launch_plan(host: str = "127.0.0.1", port: int = 8800, *, no_browser: bool = False) -> dict[str, Any]:
    return dashboard_v2_launcher_report(".", host=host, port=port, no_browser=no_browser)
