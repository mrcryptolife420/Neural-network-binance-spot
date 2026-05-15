from __future__ import annotations

from typing import Any

SAFE_OPERATOR_COMMANDS = [
    "validate-config",
    "preflight",
    "check-all",
    "dashboard-smoke",
    "operator-quality-gate",
    "support-bundle",
    "support-bundle-verify",
    "evidence-manifest",
    "no-live-proof-pack",
    "stabilization-gate",
]


def build_operator_cli_cookbook() -> dict[str, Any]:
    commands = [
        {
            "command": command,
            "purpose": command.replace("-", " "),
            "when_to_use": "local paper/demo operations",
            "safe_mode": "paper_only",
            "example": f"python -m binance_spot_bot.cli {command} --json",
            "forbidden_variants": ["live", "signed order", "account endpoint"],
            "live_trading_enabled": False,
        }
        for command in SAFE_OPERATOR_COMMANDS
    ]
    return {"status": "ok", "commands": commands, "live_trading_enabled": False}


def operator_cli_cookbook() -> dict[str, Any]:
    return build_operator_cli_cookbook()
