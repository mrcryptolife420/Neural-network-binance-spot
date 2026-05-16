from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from . import NO_ADVICE_STATEMENT, NO_LIVE_STATEMENT, PAPER_ONLY_RESEARCH_STATEMENT

ADVICE_PATTERNS = (
    re.compile(r"\bbuy\b", re.IGNORECASE),
    re.compile(r"\bsell\b", re.IGNORECASE),
    re.compile(r"real[- ]?money", re.IGNORECASE),
    re.compile(r"real allocation", re.IGNORECASE),
    re.compile(r"financial advice", re.IGNORECASE),
)
SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*[A-Za-z0-9_/+=-]{12,}"),
    re.compile(r"[A-Za-z0-9]{48,}"),
)


def now_ms() -> int:
    return int(time.time() * 1000)


def stable_hash(payload: Any) -> str:
    raw = json.dumps(to_plain(payload), sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def to_plain(value: Any) -> Any:
    if is_dataclass(value):
        return {key: to_plain(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): to_plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_plain(item) for item in value]
    return value


def redact_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: redact_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, str):
        redacted = value
        for pattern in SECRET_PATTERNS:
            redacted = pattern.sub("[REDACTED]", redacted)
        return redacted
    return value


def has_advice_wording(payload: Any) -> bool:
    text = json.dumps(to_plain(payload), default=str)
    safe_phrases = (NO_LIVE_STATEMENT, NO_ADVICE_STATEMENT, PAPER_ONLY_RESEARCH_STATEMENT)
    for phrase in safe_phrases:
        text = text.replace(phrase, "")
    return any(pattern.search(text) for pattern in ADVICE_PATTERNS)


def path_in(root: Path, *parts: str) -> Path:
    base = root.resolve()
    path = base.joinpath(*parts).resolve()
    if base != path and base not in path.parents:
        raise ValueError("path traversal blocked")
    return path


def json_write(path: Path, payload: Any) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    safe = redact_value(to_plain(payload))
    path.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
    return {"path": str(path), "sha256": stable_hash(safe)}


def status_from_blockers(blockers: list[str], warnings: list[str] | None = None) -> str:
    if blockers:
        return "blocked"
    if warnings:
        return "warn"
    return "ok"

