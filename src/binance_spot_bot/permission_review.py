from __future__ import annotations

import time
from typing import Any

from .permission_drift import permission_drift
from .permission_profiles import permission_matrix
from .redaction import redact_payload


def permission_review(expected: dict[str, Any] | None = None, actual: dict[str, Any] | None = None) -> dict[str, Any]:
    matrix = permission_matrix()
    drift = permission_drift(expected or {"manifest_hash": matrix["manifest_hash"]}, actual or {"manifest_hash": matrix["manifest_hash"]})
    stale = drift["status"] != "ok"
    return redact_payload(
        {
            "status": "review_required" if stale else "ok",
            "reviewed_profiles": list(matrix["profiles"].keys()),
            "stale_profiles": list(matrix["profiles"].keys()) if stale else [],
            "overprivileged_operators": [],
            "unused_permissions": [],
            "forbidden_attempts": [],
            "recommendations": ["review permission drift"] if stale else [],
            "created_at_ms": int(time.time() * 1000),
            "live_trading_enabled": False,
        }
    )
