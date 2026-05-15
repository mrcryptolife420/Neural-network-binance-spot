from __future__ import annotations

from typing import Any

from .redaction import redact_payload


def model_card_v2(model_id: str, metrics: dict[str, Any] | None = None, feature_contract: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = {
        "status": "ok",
        "model_id": model_id,
        "metrics": metrics or {},
        "feature_contract": feature_contract or {},
        "intended_use": "paper/shadow/demo research only",
        "forbidden_use": "live trading",
        "live_trading_enabled": False,
    }
    return redact_payload(payload)
