from __future__ import annotations

from typing import Any


def data_quality_v2(rows: list[dict[str, Any]]) -> dict[str, Any]:
    timestamps = [int(row.get("timestamp_ms", row.get("open_time_ms", i))) for i, row in enumerate(rows)]
    duplicates = len(timestamps) - len(set(timestamps))
    ordered = timestamps == sorted(timestamps)
    gaps = sum(1 for left, right in zip(timestamps, timestamps[1:]) if right <= left)
    status = "ok" if rows and ordered and duplicates == 0 and gaps == 0 else "warn"
    return {
        "status": status,
        "rows": len(rows),
        "ordered": ordered,
        "duplicate_count": duplicates,
        "gap_count": gaps,
        "live_trading_enabled": False,
    }
