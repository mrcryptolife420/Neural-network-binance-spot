from __future__ import annotations

import json
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


PROFILE_LIMITS: dict[str, dict[str, int]] = {
    "header": {"candles": 0, "signals": 0, "fills": 0, "equity": 1},
    "overview": {"candles": 50, "signals": 20, "fills": 20, "equity": 50},
    "chart": {"candles": 500, "signals": 200, "fills": 200, "equity": 500},
    "orders": {"candles": 0, "signals": 0, "fills": 250, "equity": 0},
    "sessions": {"candles": 0, "signals": 0, "fills": 25, "equity": 25},
    "evidence": {"candles": 10, "signals": 10, "fills": 10, "equity": 10},
    "debug": {"candles": 1000, "signals": 1000, "fills": 1000, "equity": 1000},
    "full": {"candles": 10_000, "signals": 10_000, "fills": 10_000, "equity": 10_000},
}


def _tail(value: Any, limit: int) -> tuple[list[Any], int]:
    if not isinstance(value, list):
        return [], 0
    if limit <= 0:
        return [], len(value)
    return value[-limit:], max(0, len(value) - limit)


def apply_payload_profile(snapshot: dict[str, Any], profile: str = "overview") -> dict[str, Any]:
    if profile not in PROFILE_LIMITS:
        profile = "overview"
    limits = PROFILE_LIMITS[profile]
    payload = dict(snapshot)
    trimmed: dict[str, int] = {}
    for key, limit in limits.items():
        payload[key], trimmed[key] = _tail(payload.get(key, []), limit)
    if profile not in {"debug", "full"}:
        payload.pop("debug", None)
        payload.pop("raw", None)
    payload["no_live_statement"] = dashboard_v2_no_live_statement()
    payload["live_trading_enabled"] = False
    body = redact_dashboard_payload(payload)
    bytes_len = len(json.dumps(body, default=str).encode("utf-8"))
    return {
        "status": "ok",
        "profile": profile,
        "payload": body,
        "meta": {"payload_bytes": bytes_len, "trimmed_counts": trimmed, "live_trading_enabled": False},
        "live_trading_enabled": False,
    }


def dashboard_v2_payload_profile_report(snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    snapshot = snapshot or {
        "candles": [{"i": i, "api_key": "redacted"} for i in range(120)],
        "signals": [{"i": i} for i in range(60)],
        "fills": [{"i": i} for i in range(40)],
        "equity": [{"i": i} for i in range(80)],
    }
    profiles = {profile: apply_payload_profile(snapshot, profile)["meta"] for profile in PROFILE_LIMITS}
    overview_bytes = profiles["overview"]["payload_bytes"]
    full_bytes = profiles["full"]["payload_bytes"]
    return redact_dashboard_payload(
        {
            "status": "ok",
            "profiles": profiles,
            "overview_smaller_than_full": overview_bytes < full_bytes,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )
