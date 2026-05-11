from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .redaction import redact_payload


@dataclass(frozen=True)
class ComplianceEvidence:
    evidence_type: str
    path: str
    required: bool = True
    status: str = "unknown"
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["evidence_hash"] = hashlib.sha256(json.dumps(redact_payload(payload), sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]
        return redact_payload(payload)


def compliance_evidence_check(items: list[ComplianceEvidence]) -> dict[str, Any]:
    missing = [item.to_dict() for item in items if item.required and item.path and not Path(item.path).exists()]
    failed = [item.to_dict() for item in items if item.status not in {"ok", "pass", "unknown"}]
    return {"status": "blocked" if missing or failed else "ok", "missing": missing, "failed": failed, "items": [item.to_dict() for item in items], "live_trading_enabled": False}
