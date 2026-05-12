from __future__ import annotations

import hashlib
import time
from pathlib import Path
from typing import Any

from .backup_profiles import is_forbidden_backup_path
from .redaction import redact_payload


def state_inventory(root: Path) -> dict[str, Any]:
    root = Path(root)
    items: list[dict[str, Any]] = []
    if not root.exists():
        return {"status": "warning", "items": [], "warnings": ["root_missing"], "live_trading_enabled": False}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            rel = path.name
        forbidden = is_forbidden_backup_path(rel)
        items.append(
            redact_payload(
                {
                    "path": rel,
                    "category": _category(rel),
                    "suffix": path.suffix.lower(),
                    "size_bytes": path.stat().st_size,
                    "modified_at": int(path.stat().st_mtime * 1000),
                    "sha256": _sha256(path) if not forbidden else "",
                    "redacted": True,
                    "required": rel.endswith(("manifest.json", "manifest.jsonl")),
                    "stale": (time.time() - path.stat().st_mtime) > 30 * 86400,
                    "include_eligible": not forbidden,
                    "restore_priority": _restore_priority(rel),
                }
            )
        )
    warnings = ["no_state_files"] if not items else []
    return {"status": "ok" if not warnings else "warning", "items": items, "warnings": warnings, "live_trading_enabled": False}


def write_state_inventory(root: Path, out: Path | None = None) -> dict[str, Any]:
    payload = state_inventory(root)
    target = out or Path(root) / "disaster-recovery" / "inventory_manifest.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    import json

    target.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return {"path": str(target), **payload}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:24]


def _category(rel: str) -> str:
    first = rel.split("/", 1)[0]
    mapping = {
        "checks": "checks",
        "evidence": "evidence",
        "reports": "reports",
        "support": "support_bundles",
        "sessions": "sessions",
        "pilot-runs": "pilot_runs",
        "metrics-warehouse": "metrics",
        "metrics": "metrics",
        "local-ops": "local_jobs",
        "ai-ops": "ai_ops",
        "action-center": "action_center",
        "permissions": "permissions",
        "compliance": "compliance",
        "portfolio-policies": "portfolio_policies",
        "backups": "backups",
    }
    return mapping.get(first, "state")


def _restore_priority(rel: str) -> int:
    if rel.startswith(("permissions/", "compliance/", "action-center/")):
        return 10
    if rel.startswith(("reports/", "evidence/", "checks/")):
        return 20
    return 50
