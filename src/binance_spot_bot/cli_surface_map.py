from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def _safety_class(command: str) -> str:
    if any(token in command for token in ["cancel", "place", "execution"]):
        return "demo_execution"
    if any(token in command for token in ["migration", "restore", "move", "compact", "clear"]):
        return "destructive_confirm_required"
    if any(token in command for token in ["dashboard", "report", "bundle", "evidence"]):
        return "artifact_generation"
    if any(token in command for token in ["run-local", "paper", "pilot"]):
        return "paper_demo_runtime"
    return "read_only"


def build_cli_surface_map(root: Path | str = ".") -> dict[str, Any]:
    path = Path(root) / "src" / "binance_spot_bot" / "cli.py"
    text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    commands = sorted(dict.fromkeys(re.findall(r"add_parser\(\"([^\"]+)\"", text)))
    items = [
        {
            "command": command,
            "safety_class": _safety_class(command),
            "required_tests": ["python -m pytest -q"] if command in {"check-all", "run-local"} else ["python -m binance_spot_bot.cli check-all --skip-tests --json"],
            "no_live_constraints": True,
        }
        for command in commands
    ]
    return {"status": "ready", "payload": {"commands": items, "count": len(items)}, "live_trading_enabled": False}


def cli_surface_map(commands: list[str]) -> dict[str, Any]:
    return {"status": "ready", "payload": {"commands": [{"command": item, "safety_class": _safety_class(item)} for item in commands]}, "live_trading_enabled": False}
