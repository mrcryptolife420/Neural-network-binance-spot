from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def write_rotation_evidence(path: Path | str, payload: dict[str, Any]) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(redact_payload({**payload, "live_trading_enabled": False}), indent=2, sort_keys=True, default=str), encoding="utf-8")
    return target
