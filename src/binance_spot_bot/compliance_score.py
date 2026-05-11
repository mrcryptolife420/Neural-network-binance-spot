from __future__ import annotations

from typing import Any

from .redaction import redact_payload


def compliance_score(checks: list[dict[str, Any]]) -> dict[str, Any]:
    blockers = [check for check in checks if check.get("required") and not check.get("allowed", check.get("status") == "ok")]
    hard = [check for check in checks if check.get("hard_blocker") or check.get("reason") in {"live_enabled", "forbidden_scope_allowed", "secret_scan_finding", "unapproved_execution"}]
    score = max(0, 100 - len(blockers) * 15 - len(hard) * 50)
    grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D" if score >= 40 else "F"
    status = "blocked" if hard else ("warn" if blockers else "ok")
    return redact_payload({"status": status, "score": score, "grade": grade, "blockers": blockers, "hard_blockers": hard, "no_live_proof": True, "live_trading_enabled": False})
