from __future__ import annotations

import json
import re
import time
import uuid
from dataclasses import asdict, is_dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[-_]?key|secret|signature|authorization|x-mbx-apikey)"),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
]


def _json_default(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, Path):
        return str(value)
    return str(value)


def scrub(value: Any) -> Any:
    if isinstance(value, dict):
        cleaned: dict[str, Any] = {}
        for key, item in value.items():
            if any(pattern.search(str(key)) for pattern in SECRET_PATTERNS):
                cleaned[key] = "***REDACTED***"
            else:
                cleaned[key] = scrub(item)
        return cleaned
    if isinstance(value, list):
        return [scrub(item) for item in value]
    if isinstance(value, str):
        redacted = value
        for pattern in SECRET_PATTERNS[1:]:
            redacted = pattern.sub("***REDACTED***", redacted)
        return redacted
    return value


class AuditLog:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def emit(
        self,
        component: str,
        event: str,
        payload: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> str:
        cid = correlation_id or str(uuid.uuid4())
        record = {
            "timestamp_ms": int(time.time() * 1000),
            "correlation_id": cid,
            "component": component,
            "event": event,
            "payload": scrub(payload or {}),
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, default=_json_default, sort_keys=True) + "\n")
        return cid

