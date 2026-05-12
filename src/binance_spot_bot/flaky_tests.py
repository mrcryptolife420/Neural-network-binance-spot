from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any
import json


def flaky_tests(history: list[dict]) -> dict[str, Any]:
    by_command: dict[str, set[str]] = defaultdict(set)
    for row in history:
        by_command[row.get("command", "unknown")].add(row.get("status", "unknown"))
    candidates = [{"command": command, "reason": "mixed_pass_fail"} for command, statuses in by_command.items() if {"ok", "failed"} <= statuses]
    return {"status": "ready", "candidates": candidates, "live_trading_enabled": False}


def write_flaky_test_report(root: Path | str, history: list[dict]) -> dict[str, Any]:
    payload = flaky_tests(history)
    out = Path(root) / "data" / "test-runs" / "flaky"
    out.mkdir(parents=True, exist_ok=True)
    (out / "flaky-tests.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    (out / "flaky-tests.md").write_text(f"# Flaky Tests\n\n- Candidates: {len(payload['candidates'])}\n- Live trading enabled: false\n", encoding="utf-8")
    payload["paths"] = {"json": str(out / "flaky-tests.json"), "markdown": str(out / "flaky-tests.md")}
    return payload
