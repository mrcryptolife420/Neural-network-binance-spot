from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def save_training_progress(root: Path | str, operator_id: str, lesson_id: str, status: str) -> dict[str, Any]:
    root = Path(root)
    out = root / "data" / "operator-training" / "progress"
    out.mkdir(parents=True, exist_ok=True)
    payload = {
        "operator_id": operator_id,
        "lesson_id": lesson_id,
        "status": status,
        "updated_at_ms": int(time.time() * 1000),
        "live_trading_enabled": False,
    }
    payload["sha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:32]
    path = out / f"{operator_id}-{lesson_id}.json"
    path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    return payload | {"path": str(path)}


def write_operator_training_store(root: Path, payload: dict) -> dict[str, str]:
    saved = save_training_progress(root, str(payload.get("operator_id", "local")), str(payload.get("lesson_id", "lesson")), str(payload.get("status", "complete")))
    return {"json": saved["path"]}
