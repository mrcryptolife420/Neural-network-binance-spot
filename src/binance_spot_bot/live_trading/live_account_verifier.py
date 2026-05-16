from __future__ import annotations

from typing import Any

from binance_spot_bot.portfolio_lab.common import redact_value, stable_hash, status_from_blockers


LIVE_SPOT_BASE_URL = "https://api.binance.com/api"


class FakeLiveReadOnlyAdapter:
    def __init__(self, *, account_ok: bool = True, base_url: str = LIVE_SPOT_BASE_URL) -> None:
        self.account_ok = account_ok
        self.base_url = base_url
        self.calls: list[str] = []

    def account_state(self) -> dict[str, Any]:
        self.calls.append("account_state")
        if not self.account_ok:
            return {"status": "blocked", "permissions": []}
        return {"status": "ok", "permissions": ["SPOT"], "balances": [{"asset": "USDT", "free": "100.00"}]}


def verify_live_read_only_account(adapter: FakeLiveReadOnlyAdapter | None = None, *, api_key: str = "fixture-live-key", api_secret_present: bool = True, privacy_mode: bool = True) -> dict[str, Any]:
    adapter = adapter or FakeLiveReadOnlyAdapter()
    blockers: list[str] = []
    warnings: list[str] = []
    if adapter.base_url != LIVE_SPOT_BASE_URL:
        blockers.append("live base URL must be Binance live spot")
    if not api_key or not api_secret_present:
        blockers.append("live credentials missing")
    account = adapter.account_state() if not blockers else {}
    if account.get("status") == "blocked":
        blockers.append("account read-only verification failed")
    balance_summary = {"assets_seen": len(account.get("balances", [])), "privacy_mode": privacy_mode}
    return redact_value(
        {
            "status": status_from_blockers(blockers, warnings),
            "api_key_fingerprint": stable_hash(api_key)[:12] if api_key else "",
            "permissions": account.get("permissions", []),
            "balance_summary": balance_summary,
            "server_time_drift_ms": 0,
            "adapter_calls": adapter.calls,
            "blockers": blockers,
            "warnings": warnings,
            "order_endpoints_called": False,
            "live_execution_enabled": False,
            "live_order_placement_enabled": False,
            "live_trading_enabled": False,
        }
    )
