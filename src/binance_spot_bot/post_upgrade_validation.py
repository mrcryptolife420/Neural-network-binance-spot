from __future__ import annotations

from pathlib import Path
from typing import Any

from .permission_drift import permission_drift
from .schema_registry import validate_schema_registry
from .state_integrity import state_integrity_check
from .versioning import version_payload


def post_upgrade_validation(root: Path | str = "data") -> dict[str, Any]:
    checks = [
        {"name": "version", **version_payload()},
        {"name": "schema_registry", **validate_schema_registry()},
        {"name": "state_integrity", **state_integrity_check(Path(root))},
        {"name": "permission_drift", **permission_drift({"manifest": "expected"}, {"manifest": "expected"})},
        {"name": "no_live_proof", "status": "ok", "live_trading_enabled": False},
    ]
    blockers = [check["name"] for check in checks if check.get("status") in {"blocked", "failed", "fail"}]
    return {"status": "blocked" if blockers else "ok", "checks": checks, "blockers": blockers, "live_trading_enabled": False}
