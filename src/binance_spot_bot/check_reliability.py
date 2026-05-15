from __future__ import annotations

import hashlib
import json
import statistics
import time
from pathlib import Path
from typing import Any

from .redaction import redact_payload, redact_text


def record_check_history(path: Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    safe = redact_payload(result | {"live_trading_enabled": False, "recorded_at_ms": int(time.time() * 1000)})
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(safe, default=str) + "\n")


def summarize_check_reliability(history: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(history)
    passes = sum(1 for row in history if row.get("status") == "ok" or row.get("returncode") == 0)
    failures = total - passes
    durations = [float(row.get("duration_ms", 0)) for row in history]
    signatures = [
        hashlib.sha256(redact_text(str(row.get("stderr_tail") or row.get("stdout_tail") or row.get("status"))).encode()).hexdigest()[:12]
        for row in history
        if row.get("status") != "ok" and row.get("returncode", 0) != 0
    ]
    flaky = total >= 2 and passes > 0 and failures > 0
    return {
        "status": "warn" if failures or flaky else "ok",
        "runs": total,
        "pass_rate": round(passes / total, 4) if total else 1.0,
        "fail_rate": round(failures / total, 4) if total else 0.0,
        "flaky_score": 1.0 if flaky else 0.0,
        "average_duration_ms": round(statistics.mean(durations), 2) if durations else 0.0,
        "p95_duration_ms": round(sorted(durations)[int(0.95 * (len(durations) - 1))], 2) if durations else 0.0,
        "failure_signatures": sorted(set(signatures)),
        "live_trading_enabled": False,
    }


def check_reliability(history: list[dict[str, Any]]) -> dict[str, Any]:
    return summarize_check_reliability(history)
