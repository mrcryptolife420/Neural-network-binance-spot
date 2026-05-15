from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def export_model_evidence_bundle(path: Path | str, payload: dict[str, Any]) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    safe = redact_payload({**payload, "live_trading_enabled": False})
    target.write_text(json.dumps(safe, indent=2, sort_keys=True, default=str), encoding="utf-8")
    return target
