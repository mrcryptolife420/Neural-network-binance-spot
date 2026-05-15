from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def log_shadow_prediction(path: Path | str, *, model_alias: str, symbol: str, prediction: dict[str, Any], features: dict[str, Any] | None = None) -> dict[str, Any]:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "timestamp_ms": int(time.time() * 1000),
        "model_alias": model_alias,
        "symbol": symbol,
        "prediction": prediction,
        "features": features or {},
        "live_trading_enabled": False,
    }
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(redact_payload(row), sort_keys=True, default=str) + "\n")
    return {"status": "ok", "path": str(target), "live_trading_enabled": False}
