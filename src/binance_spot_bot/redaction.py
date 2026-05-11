from __future__ import annotations

import hashlib
import re
from typing import Any


SECRET_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{24,}"),
    re.compile(r"(?i)(BINANCE_API_KEY|BINANCE_API_SECRET|api[_-]?key|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)\b(signature|listenKey)\s*[:=]\s*[A-Za-z0-9_-]{16,}"),
    re.compile(r"\b[A-Za-z0-9]{56,128}\b"),
]
JSON_SECRET_PATTERN = re.compile(r"(?i)(\"(?:BINANCE_API_KEY|BINANCE_API_SECRET|api[_-]?key|api[_-]?secret|secret)\"\s*:\s*\")[^\"]+(\")")


def fingerprint(value: str) -> str:
    if not value:
        return "not-configured"
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:10]
    if len(value) <= 8:
        return f"sha256:{digest}"
    return f"{value[:4]}...{value[-4:]} sha256:{digest}"


def redact_text(value: str) -> str:
    redacted = JSON_SECRET_PATTERN.sub(r"\1[REDACTED]\2", value)
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def redact_payload(payload: Any) -> Any:
    if isinstance(payload, str):
        return redact_text(payload)
    if isinstance(payload, dict):
        safe: dict[str, Any] = {}
        for key, value in payload.items():
            if key.lower() in {"binance_api_key", "binance_api_secret", "api_key", "api_secret", "signature", "listenkey", "listen_key"}:
                safe[key] = "[REDACTED]"
            else:
                safe[key] = redact_payload(value)
        return safe
    if isinstance(payload, list):
        return [redact_payload(item) for item in payload]
    return payload
