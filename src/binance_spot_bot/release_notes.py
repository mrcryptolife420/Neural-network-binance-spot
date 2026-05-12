from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def release_notes(version: str, changes: list[str], *, root: Path | str = "data", release_id: str | None = None) -> dict[str, Any]:
    release_id = release_id or f"release-{version}"
    out = Path(root) / "releases" / release_id
    out.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": "ok",
        "release_id": release_id,
        "version": version,
        "summary": f"Local release {version}",
        "new_features": changes,
        "changed_behavior": [],
        "migration_required": False,
        "backup_required": True,
        "validation_checklist": ["check-all --skip-tests", "dashboard-smoke"],
        "rollback_notes": "Use rollback plan and pre-upgrade backup.",
        "no_live_statement": "Live trading remains disabled.",
        "live_trading_enabled": False,
    }
    json_path = out / "release-notes.json"
    md_path = out / "release-notes.md"
    json_path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    md_path.write_text(f"# Release {version}\n\n" + "\n".join(f"- {change}" for change in changes) + "\n\nLive trading enabled: false\n", encoding="utf-8")
    return {"path": str(json_path), "markdown": str(md_path), **redact_payload(payload)}
