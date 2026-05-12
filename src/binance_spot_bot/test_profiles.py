from __future__ import annotations

from typing import Any


PROFILE_COMMANDS = {
    "fast": ["python -m pytest {targeted} -q", "python -m binance_spot_bot.cli validate-config"],
    "standard": ["python -m pytest {targeted} -q", "python -m binance_spot_bot.cli check-all --skip-tests --json"],
    "deep": ["python -m pytest -q", "python -m binance_spot_bot.cli check-all --json", "python -m binance_spot_bot.cli redaction-self-test --json"],
    "dashboard": ["python -m binance_spot_bot.cli dashboard-smoke --seconds 1", "python -m binance_spot_bot.cli dashboard-browser-smoke --url http://127.0.0.1:8506/ --seconds 10"],
    "security": ["python -m binance_spot_bot.cli security-scan", "python -m binance_spot_bot.cli redaction-self-test --json"],
    "release_migration": ["python -m binance_spot_bot.cli migration-dry-run --name demo --json", "python -m binance_spot_bot.cli release-quality-gate --json"],
}


def test_profiles() -> dict[str, Any]:
    return {"status": "ready", "payload": {"profiles": [{"name": key, "commands": value, "live_trading_enabled": False} for key, value in PROFILE_COMMANDS.items()]}, "live_trading_enabled": False}


def validate_profile_for_risk(profile: str, risk_level: str) -> dict[str, Any]:
    blocked = risk_level in {"critical", "high"} and profile == "fast"
    return {"status": "blocked" if blocked else "ok", "profile": profile, "risk_level": risk_level, "live_trading_enabled": False}
