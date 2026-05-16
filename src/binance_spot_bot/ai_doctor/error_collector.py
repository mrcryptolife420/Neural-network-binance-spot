from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, now_ms, redact_value, stable_hash


def collect_errors(root: Path, run_id: str, text: str = "") -> dict[str, Any]:
    text = text or "Traceback\nModuleNotFoundError: No module named 'fastapi'\n"
    safe_text = str(redact_value(text))
    error_type_match = re.search(r"([A-Za-z_]+Error|StreamlitDuplicateElementId)", safe_text)
    error_type = error_type_match.group(1) if error_type_match else "UnknownError"
    file_match = re.search(r'File "([^"]+)", line (\d+)', safe_text)
    error = {
        "error_id": "err-" + stable_hash(safe_text)[:12],
        "error_type": error_type,
        "message": safe_text.splitlines()[-1] if safe_text.splitlines() else safe_text,
        "file": file_match.group(1) if file_match else "",
        "line": int(file_match.group(2)) if file_match else None,
        "traceback_hash": stable_hash(safe_text),
        "first_seen_ms": now_ms(),
        "last_seen_ms": now_ms(),
        "count": 1,
        "severity_guess": "P2",
    }
    run_root = root / "data" / "ai-doctor" / "runs" / run_id
    run_root.mkdir(parents=True, exist_ok=True)
    (run_root / "errors.txt").write_text(safe_text, encoding="utf-8")
    (run_root / "stacktraces.txt").write_text(safe_text, encoding="utf-8")
    saved = json_write(run_root / "error_summary.json", {"errors": [error]})
    return {"status": "ok", "errors": [error], "saved": saved, "live_order_submitted": False}

