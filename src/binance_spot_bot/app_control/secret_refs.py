from __future__ import annotations

import hashlib
import os
from typing import Any


def fingerprint_secret(value: str) -> str:
    if not value:
        return ""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:10]


def secret_ref_status(key_ref: str = "BINANCE_API_KEY", secret_ref: str = "BINANCE_API_SECRET") -> dict[str, Any]:
    key = os.environ.get(key_ref, "")
    secret = os.environ.get(secret_ref, "")
    return {
        "status": "ok" if key and secret else "missing",
        "key_ref": key_ref,
        "secret_ref": secret_ref,
        "key_fingerprint": fingerprint_secret(key),
        "secret_fingerprint": fingerprint_secret(secret),
        "raw_secret_visible": False,
        "live_trading_enabled": False,
    }

