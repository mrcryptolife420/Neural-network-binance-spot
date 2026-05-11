from __future__ import annotations

from typing import Any

from .permission_profiles import FORBIDDEN_SCOPES
from .redaction import redact_payload


def permission_drift(expected: dict, actual: dict) -> dict[str, Any]:
    findings = []
    if not expected or not actual:
        findings.append({"severity": "warning", "reason": "missing_permission_manifest"})
    for key, value in actual.items():
        if key not in expected:
            findings.append({"severity": "warning", "reason": "new_permission_entry", "key": key})
        elif expected[key] != value:
            findings.append({"severity": "warning", "reason": "permission_value_changed", "key": key})
    forbidden = sorted(set(_flatten(actual)) & FORBIDDEN_SCOPES)
    if forbidden:
        findings.append({"severity": "critical", "reason": "forbidden_scope_appeared", "scopes": forbidden})
    status = "blocked" if any(item["severity"] == "critical" for item in findings) else ("warning" if findings else "ok")
    return redact_payload({"status": status, "findings": findings, "live_trading_enabled": False})


def _flatten(value: Any) -> list[str]:
    if isinstance(value, dict):
        out: list[str] = []
        for item in value.values():
            out.extend(_flatten(item))
        return out
    if isinstance(value, list):
        out = []
        for item in value:
            out.extend(_flatten(item))
        return out
    return [str(value)]
