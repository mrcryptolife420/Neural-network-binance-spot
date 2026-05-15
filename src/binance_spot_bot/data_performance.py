from __future__ import annotations

from pathlib import Path
from typing import Any


def analyze_data_performance(root: Path | str = ".") -> dict[str, Any]:
    root_path = Path(root)
    watched = ["data/public_binance", "data/metrics", "data/repository-knowledge", "data/roadmaps", "data/releases", "data/backups"]
    operations = []
    for rel in watched:
        path = root_path / rel
        files = list(path.rglob("*")) if path.exists() else []
        file_count = sum(item.is_file() for item in files)
        size_bytes = sum(item.stat().st_size for item in files if item.is_file())
        status = "warn" if size_bytes > 50_000_000 or file_count > 10_000 else "ok"
        operations.append({"path": rel, "file_count": file_count, "size_bytes": size_bytes, "status": status})
    return {"status": "ready", "operations": operations, "recommendations": ["compact old reports"] if any(item["status"] == "warn" for item in operations) else [], "live_trading_enabled": False}


def data_performance(rows: int, elapsed_ms: float) -> dict[str, Any]:
    per_row = elapsed_ms / max(rows, 1)
    return {"status": "ok" if per_row <= 10 else "warn", "payload": {"rows": rows, "elapsed_ms": elapsed_ms, "ms_per_row": per_row}, "live_trading_enabled": False}
