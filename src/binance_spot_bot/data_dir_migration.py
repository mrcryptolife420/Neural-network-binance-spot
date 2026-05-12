from __future__ import annotations

from pathlib import Path
from typing import Any

from .redaction import redact_payload
from .state_inventory import state_inventory


def data_dir_migration_preview(src: Path, target: Path) -> dict[str, Any]:
    src = Path(src)
    target = Path(target)
    inventory = state_inventory(src)
    conflicts = [item["path"] for item in inventory["items"] if (target / item["path"]).exists()]
    target_valid = not any(part == ".." for part in target.parts)
    return redact_payload(
        {
            "status": "ok" if target_valid else "blocked",
            "source": str(src),
            "target": str(target),
            "items": len(inventory["items"]),
            "conflicts": conflicts,
            "backup_required": True,
            "preview_only": True,
            "rollback_plan": "restore from pre-migration backup",
            "live_trading_enabled": False,
        }
    )
