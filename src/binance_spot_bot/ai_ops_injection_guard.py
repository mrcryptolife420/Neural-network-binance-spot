from __future__ import annotations

import re

from .redaction import redact_text

SUSPICIOUS_PATTERNS = [
    re.compile(r"ignore previous", re.I),
    re.compile(r"reveal (the )?(secret|key)", re.I),
    re.compile(r"enable live trading", re.I),
    re.compile(r"execute (this )?command", re.I),
    re.compile(r"upload (this )?(file|bundle)", re.I),
    re.compile(r"(powershell|cmd\.exe|bash|curl)\s+", re.I),
    re.compile(r"system instructions?", re.I),
    re.compile(r"[A-Za-z0-9+/]{48,}={0,2}"),
]


def injection_guard(text: str) -> dict:
    hits = [pattern.pattern for pattern in SUSPICIOUS_PATTERNS if pattern.search(text or "")]
    return {
        "status": "blocked" if hits else "ok",
        "suspicious": bool(hits),
        "patterns": hits,
        "safe_text": redact_text(text or ""),
        "live_trading_enabled": False,
    }
