from __future__ import annotations

from binance_spot_bot.operator_ops import redaction_self_test


def test_redaction_self_test_passes_without_leaks() -> None:
    payload = redaction_self_test()

    assert payload["status"] == "ok"
    assert payload["leaked"] == []
    assert payload["live_trading_enabled"] is False
