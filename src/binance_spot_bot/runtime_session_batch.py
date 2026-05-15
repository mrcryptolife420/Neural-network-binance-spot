from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .redaction import redact_payload
from .runtime_event_bus import RuntimeEvent


class RuntimeSessionBatchWriter:
    def __init__(self, path: Path | str, batch_size: int = 25) -> None:
        self.path = Path(path)
        self.batch_size = batch_size
        self.buffer: list[dict[str, Any]] = []

    def append(self, event: RuntimeEvent | dict[str, Any]) -> dict[str, Any]:
        payload = event.to_dict() if isinstance(event, RuntimeEvent) else redact_payload(event)
        self.buffer.append(payload)
        if len(self.buffer) >= self.batch_size:
            self.flush()
        return {"status": "queued", "queued": len(self.buffer), "live_trading_enabled": False}

    def flush(self) -> dict[str, Any]:
        if not self.buffer:
            return {"status": "ok", "written": 0, "live_trading_enabled": False}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            for row in self.buffer:
                handle.write(json.dumps(redact_payload(row), default=str) + "\n")
        written = len(self.buffer)
        self.buffer.clear()
        return {"status": "ok", "written": written, "path": str(self.path), "live_trading_enabled": False}
