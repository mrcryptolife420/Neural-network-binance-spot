from __future__ import annotations

import os
import time
import tracemalloc
from pathlib import Path
from typing import Any


def resource_snapshot(root: Path | str = ".", *, tracemalloc_enabled: bool = False, cpu_pct: float = 0, memory_mb: float = 0) -> dict[str, Any]:
    current = peak = 0
    if tracemalloc_enabled:
        if not tracemalloc.is_tracing():
            tracemalloc.start()
        current, peak = tracemalloc.get_traced_memory()
    data_dir = Path(root) / "data"
    data_bytes = sum(path.stat().st_size for path in data_dir.rglob("*") if path.is_file()) if data_dir.exists() else 0
    return {
        "status": "ready",
        "timestamp_ms": int(time.time() * 1000),
        "pid": os.getpid(),
        "cpu_pct": cpu_pct,
        "memory_mb": memory_mb,
        "peak_traced_mb": round(peak / 1024 / 1024, 3),
        "current_traced_mb": round(current / 1024 / 1024, 3),
        "data_dir_size_bytes": data_bytes,
        "live_trading_enabled": False,
    }
