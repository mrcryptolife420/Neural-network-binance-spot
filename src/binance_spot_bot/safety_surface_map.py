from __future__ import annotations

from typing import Any


SURFACES = {
    "live_trading_gates": ["live", "no_live", "live_trading"],
    "signed_endpoint_gates": ["signed", "recvWindow", "signature"],
    "order_endpoints": ["order", "execution"],
    "credential_handling": ["credential", "secret", "api_key"],
    "redaction": ["redaction", "security"],
    "restore_migration_apply": ["restore", "migration", "rollback", "backup"],
    "permissions_compliance": ["permission", "compliance", "role"],
}


def safety_surface_map(files: list[str]) -> dict[str, Any]:
    impacted = []
    for path in files:
        lower = path.lower()
        for surface, tokens in SURFACES.items():
            if any(token.lower() in lower for token in tokens):
                impacted.append({"file": path, "surface": surface, "impact": "critical" if surface in {"order_endpoints", "credential_handling", "restore_migration_apply"} else "high"})
    return {"status": "ready", "surfaces": impacted, "required_validation": ["security-scan", "redaction-self-test"] if impacted else [], "live_trading_enabled": False}
