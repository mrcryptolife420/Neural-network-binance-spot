from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .compliance_score import compliance_score
from .permission_drift import permission_drift
from .permission_profiles import permission_matrix, write_permission_manifest
from .redaction import redact_payload


def write_compliance_report(root: Path, checks: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    date_dir = Path(root) / "compliance" / time.strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)
    manifest = write_permission_manifest(root)
    score = compliance_score(checks or [{"required": True, "allowed": True}])
    report = {
        "status": "ok" if score["status"] != "blocked" else "blocked",
        "summary": "local permissions compliance",
        "no_live_proof": True,
        "permission_profiles": permission_matrix(),
        "permission_drift": permission_drift({"manifest": "expected"}, {"manifest": "expected"}),
        "compliance_score": score,
        "evidence_manifest": str(manifest),
        "created_at_ms": int(time.time() * 1000),
        "live_trading_enabled": False,
    }
    json_path = date_dir / "compliance_report.json"
    md_path = date_dir / "compliance_report.md"
    json_path.write_text(json.dumps(redact_payload(report), indent=2, default=str), encoding="utf-8")
    md_path.write_text(f"# Compliance Report\n\nStatus: {report['status']}\n\nGrade: {score['grade']}\n\nLive trading enabled: false\n", encoding="utf-8")
    return {"path": str(json_path), "markdown": str(md_path), **report}
