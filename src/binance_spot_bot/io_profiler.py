from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .profiling_core import ProfileRun, profile_block, summarize_profile_run


def profile_json_write(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    run = ProfileRun("io-profile", "io")
    with profile_block("json_write", "io", {"path": str(path), "bytes": len(json.dumps(payload, default=str))}, run):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({**payload, "live_trading_enabled": False}, indent=2, default=str), encoding="utf-8")
    return {"status": "ready", "run": run.to_dict(), "summary": summarize_profile_run(run), "live_trading_enabled": False}


def io_profile(reads: int, writes: int) -> dict[str, Any]:
    warnings = []
    if writes > 100:
        warnings.append("many_small_writes")
    return {"status": "ready", "payload": {"reads": reads, "writes": writes, "warnings": warnings}, "live_trading_enabled": False}
