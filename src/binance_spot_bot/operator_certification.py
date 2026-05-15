from __future__ import annotations

import time
from typing import Any


def certification_draft(level: str = "paper-operator") -> dict[str, Any]:
    checklist = [
        "validate-config",
        "preflight",
        "check-all",
        "dashboard-smoke",
        "support-bundle-verify",
        "no-live-proof-review",
        "forbidden-live-actions-understood",
    ]
    return {"status": "draft", "level": level, "checklist": checklist, "approval_scope": "paper_only", "live_trading_enabled": False}


def complete_certification(level: str, confirm: str, *, score: int = 100) -> dict[str, Any]:
    if confirm != "PAPER_ONLY_CERTIFICATION":
        return {"status": "blocked", "reason": "paper-only certification confirm required", "live_trading_enabled": False}
    if score < 80:
        return {"status": "failed", "score": score, "live_trading_enabled": False}
    return {
        "status": "passed",
        "level": level,
        "score": score,
        "expires_at_ms": int(time.time() * 1000) + 90 * 86_400_000,
        "approval_scope": "paper_only",
        "live_trading_enabled": False,
    }


def operator_certification(score: int) -> dict[str, Any]:
    return {"status": "passed" if score >= 80 else "failed", "score": score, "live_trading_enabled": False}
