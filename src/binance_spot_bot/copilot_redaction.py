from __future__ import annotations

from typing import Any

from .redaction import redact_payload, redact_text


def redact_for_copilot(payload: Any) -> Any:
    return redact_payload(payload)


def redact_copilot_text(text: str) -> str:
    return redact_text(text)
