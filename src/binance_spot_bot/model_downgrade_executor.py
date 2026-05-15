from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .model_monitoring_config import ALLOWED_DOWNGRADE_ALIASES, FORBIDDEN_DOWNGRADE_ALIASES
from .redaction import redact_payload


def model_downgrade_executor(
    action: str,
    confirm: str,
    *,
    alias: str = "candidate",
    fallback_alias: str = "baseline",
    root: Path | str | None = None,
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blockers: list[str] = []
    if action != "downgrade_candidate":
        blockers.append("no_downgrade_action")
    if confirm != "DOWNGRADE_PAPER_MODEL":
        blockers.append("confirmation_required")
    if alias in FORBIDDEN_DOWNGRADE_ALIASES or alias not in ALLOWED_DOWNGRADE_ALIASES:
        blockers.append("alias_not_allowed_for_downgrade")
    if not evidence and root is not None:
        blockers.append("evidence_required")
    status = "applied" if not blockers else "blocked"
    payload = {
        "status": status,
        "action": action,
        "alias": alias,
        "fallback_alias": fallback_alias,
        "blockers": blockers,
        "scope": "paper_shadow_demo_only",
        "live_trading_enabled": False,
    }
    if root is not None:
        path = Path(root) / "model-monitoring" / "alias-history.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        row = {**payload, "evidence": evidence or {}, "timestamp_ms": int(time.time() * 1000)}
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(redact_payload(row), sort_keys=True, default=str) + "\n")
        payload["history_path"] = str(path)
    return payload
