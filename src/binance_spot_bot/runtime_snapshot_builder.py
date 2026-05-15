from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

from .redaction import redact_payload
from .runtime_snapshot_limits import enforce_snapshot_limits

SNAPSHOT_PROFILES = {
    "compact": {"max_items": 25, "include": {"identity", "lifecycle", "model", "safety"}},
    "dashboard": {"max_items": 100, "include": {"identity", "lifecycle", "market", "paper", "model", "demo", "reports", "safety"}},
    "full": {"max_items": 500, "include": None},
    "evidence": {"max_items": 150, "include": {"identity", "lifecycle", "model", "demo", "reports", "safety"}},
}


def _to_plain(parts: Any) -> dict[str, Any]:
    if is_dataclass(parts):
        return asdict(parts)
    if hasattr(parts, "to_dict") and callable(parts.to_dict):
        return dict(parts.to_dict())
    return dict(parts)


def build_runtime_snapshot(parts: dict[str, Any] | Any, profile: str = "dashboard") -> dict[str, Any]:
    config = SNAPSHOT_PROFILES.get(profile, SNAPSHOT_PROFILES["dashboard"])
    payload = _to_plain(parts)
    include = config["include"]
    if include is not None:
        payload = {key: value for key, value in payload.items() if key in include}
    limited = enforce_snapshot_limits(redact_payload(payload), max_items=int(config["max_items"]))
    return {
        "kind": "runtime_snapshot",
        "profile": profile,
        "payload": limited["limited"],
        "limits": {"max_items": config["max_items"]},
        "live_trading_enabled": False,
    }
