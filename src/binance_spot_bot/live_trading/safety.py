from __future__ import annotations

import hashlib
import time
from dataclasses import asdict, dataclass, field
from typing import Any

from binance_spot_bot.redaction import redact_payload


@dataclass(frozen=True)
class LiveSafetyDecision:
    status: str
    action: str
    reasons: list[str]
    requires_approval: bool = True
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_order_submitted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def preview_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(str(sorted(payload.items())).encode("utf-8")).hexdigest()


def block_without_confirmation(confirm: str, phrase: str) -> bool:
    return confirm != phrase


def no_live_order() -> dict[str, Any]:
    return {"live_order_submitted": False, "signed_order_endpoint_called": False, "live_trading_enabled": False}
