from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def append_test_runtime_history(root: Path | str, record: dict[str, Any]) -> dict[str, Any]:
    root_path = Path(root)
    out = root_path / "data" / "test-runs"
    out.mkdir(parents=True, exist_ok=True)
    payload = redact_payload({**record, "timestamp_ms": int(time.time() * 1000), "live_trading_enabled": False})
    with (out / "history.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, default=str) + "\n")
    (out / "latest.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return {"status": "ready", "path": str(out / "history.jsonl"), "record": payload, "live_trading_enabled": False}


def summarize_test_runtime_history(root: Path | str) -> dict[str, Any]:
    path = Path(root) / "data" / "test-runs" / "history.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()] if path.exists() else []
    by_command: dict[str, list[int]] = {}
    for row in rows:
        by_command.setdefault(row.get("command", "unknown"), []).append(int(row.get("duration_ms", 0)))
    avg = {cmd: sum(values) / max(len(values), 1) for cmd, values in by_command.items()}
    return {"status": "ready", "count": len(rows), "average_duration_ms": avg, "latest_status": rows[-1].get("status") if rows else "missing", "live_trading_enabled": False}


def test_runtime_history(rows: list[dict]) -> dict[str, Any]:
    return {"status": "ready", "count": len(rows), "live_trading_enabled": False}
