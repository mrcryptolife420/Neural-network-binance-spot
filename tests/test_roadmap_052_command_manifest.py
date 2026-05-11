from __future__ import annotations

from binance_spot_bot.operator_ops import operator_command_manifest


def test_operator_command_manifest_is_demo_safe() -> None:
    payload = operator_command_manifest()
    commands = {row["command"] for row in payload["commands"]}

    assert "demo-acceptance-rehearsal" in commands
    assert "enable-live" not in commands
    assert all(row["live_trading"] is False for row in payload["commands"])
