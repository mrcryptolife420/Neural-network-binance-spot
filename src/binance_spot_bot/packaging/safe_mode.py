from __future__ import annotations


def package_safe_mode_status() -> dict[str, object]:
    return {"status": "ok", "mode": "safe", "dashboard_read_only": True, "live_profiles_locked": True, "runtime_auto_start": False, "order_endpoints_enabled": False, "tools": ["diagnostics", "restore", "backup", "docs", "evidence"], "live_trading_enabled": False}

