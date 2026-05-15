from __future__ import annotations

from typing import Any


def detect_flaky_checks(history: list[dict[str, Any]]) -> dict[str, Any]:
    by_name: dict[str, set[str]] = {}
    for row in history:
        by_name.setdefault(str(row.get("name", row.get("command", "unknown"))), set()).add("ok" if row.get("status") == "ok" or row.get("returncode") == 0 else "failed")
    flaky = sorted(name for name, statuses in by_name.items() if {"ok", "failed"} <= statuses)
    items = [
        {
            "name": name,
            "class": "intermittent_result",
            "retry_policy": "single retry allowed only after root-cause evidence",
            "quarantine_allowed": False,
        }
        for name in flaky
    ]
    return {"status": "warn" if flaky else "ok", "flaky": flaky, "items": items, "live_trading_enabled": False}


def flaky_check_burndown(flaky: list[str] | list[dict[str, Any]]) -> dict[str, Any]:
    if flaky and isinstance(flaky[0], dict):
        return detect_flaky_checks(flaky)  # type: ignore[arg-type]
    return {"status": "ok" if not flaky else "warn", "flaky": flaky, "live_trading_enabled": False}
