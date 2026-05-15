from __future__ import annotations

from pathlib import Path
from typing import Any

from .redaction import redact_text


def verify_stabilization_secrets(paths: list[Path]) -> dict[str, Any]:
    findings = []
    for path in paths:
        if not path.exists() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if redact_text(text) != text:
            findings.append({"path": str(path), "status": "blocked", "reason": "secret-like content found"})
    return {"status": "ok" if not findings else "blocked", "findings": findings, "live_trading_enabled": False}


def stabilization_secret_verify(findings: list) -> dict[str, Any]:
    return {"status": "ok" if not findings else "blocked", "findings": findings, "live_trading_enabled": False}
