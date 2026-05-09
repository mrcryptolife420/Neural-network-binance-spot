from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from .session_store import SessionStore


@dataclass(frozen=True)
class SessionComparisonRow:
    session_id: str
    pnl: Decimal
    max_drawdown: Decimal
    trades: int
    blocks: int
    alerts: int
    data_quality: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        return {key: str(value) if isinstance(value, Decimal) else value for key, value in payload.items()}


def compare_sessions(store: SessionStore, session_ids: list[str]) -> list[SessionComparisonRow]:
    if not 2 <= len(session_ids) <= 10:
        raise ValueError("compare 2-10 sessions")
    rows = []
    for session_id in session_ids:
        summary = store.load_summary(session_id)
        snapshots = store.load_events(session_id, "snapshots.jsonl")
        alerts = store.load_events(session_id, "alerts.jsonl")
        data_quality = snapshots[-1].get("data_quality", {}).get("status", "unknown") if snapshots else "unknown"
        rows.append(SessionComparisonRow(session_id, summary.pnl, summary.max_drawdown, summary.trades, summary.blocks, len(alerts), data_quality))
    return rows


def export_comparison(rows: list[SessionComparisonRow], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join([",".join(str(value) for value in row.to_dict().values()) for row in rows]), encoding="utf-8")
    return path
