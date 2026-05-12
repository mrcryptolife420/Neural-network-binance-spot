from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .redaction import redact_payload


SCHEMA_DOMAINS = ["config", "data_store", "public_binance_cache", "metrics", "action_center", "permission", "compliance", "backup", "deployment", "portfolio_policy", "ai_ops_context", "release_manifest"]


@dataclass(frozen=True)
class SchemaVersion:
    domain: str
    version: str = "1"
    status: str = "compatible"

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def schema_registry(names: list[str] | None = None) -> dict[str, Any]:
    domains = names or SCHEMA_DOMAINS
    schemas = [SchemaVersion(name).to_dict() for name in domains]
    return {"status": "ok", "schemas": schemas, "live_trading_enabled": False}


def validate_schema_registry(current: dict[str, str] | None = None) -> dict[str, Any]:
    current = current or {name: "1" for name in SCHEMA_DOMAINS}
    unknown = [key for key in current if key not in SCHEMA_DOMAINS]
    return {"status": "warn" if unknown else "ok", "unknown": unknown, "live_trading_enabled": False}
