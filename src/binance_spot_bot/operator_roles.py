from __future__ import annotations

import hashlib
import json
from typing import Any

from .permission_profiles import PROFILES
from .redaction import redact_payload


def default_operator_roles() -> dict[str, Any]:
    roles = {role: profile.to_dict() for role, profile in PROFILES.items() if role in {"viewer", "operator", "maintainer", "governance_reviewer", "admin_local"}}
    payload = {"status": "ready", "roles": roles, "live_trading_enabled": False}
    payload["role_template_hash"] = hashlib.sha256(json.dumps(redact_payload(roles), sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]
    return redact_payload(payload)
