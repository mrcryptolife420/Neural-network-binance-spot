from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def write_disaster_recovery_report(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    out = Path(root) / "disaster-recovery" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    report = {
        "status": payload.get("status", "ok"),
        "created_at_ms": int(time.time() * 1000),
        "backup": payload.get("backup", {}),
        "verify": payload.get("verify", {}),
        "restore_preview": payload.get("restore_preview", {}),
        "restore_drill": payload.get("restore_drill", {}),
        "integrity": payload.get("integrity", {}),
        "permission_restore": payload.get("permission_restore", {}),
        "evidence_continuity": payload.get("evidence_continuity", {}),
        "no_live_proof": True,
        "redaction_proof": True,
        "live_trading_enabled": False,
    }
    json_path = out / "disaster_recovery_report.json"
    md_path = out / "disaster_recovery_report.md"
    json_path.write_text(json.dumps(redact_payload(report), indent=2, default=str), encoding="utf-8")
    md_path.write_text(f"# Disaster Recovery Report\n\nStatus: {report['status']}\n\nLive trading enabled: false\n", encoding="utf-8")
    return {"path": str(json_path), "markdown": str(md_path), **report}
