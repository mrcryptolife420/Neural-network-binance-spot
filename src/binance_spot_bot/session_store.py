from __future__ import annotations

import csv
import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any


def _json_default(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if hasattr(value, "value"):
        return value.value
    if hasattr(value, "__dict__"):
        return asdict(value)
    return str(value)


@dataclass
class SessionSummary:
    session_id: str
    mode: str
    symbol: str
    interval: str
    started_at_ms: int
    ended_at_ms: int | None = None
    pnl: Decimal = Decimal("0")
    max_drawdown: Decimal = Decimal("0")
    trades: int = 0
    blocks: int = 0
    model_version: str = "unknown"
    status: str = "running"
    metadata: dict[str, Any] = field(default_factory=dict)


class SessionStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def start_session(
        self,
        *,
        mode: str,
        symbol: str,
        interval: str,
        model_version: str,
        metadata: dict[str, Any] | None = None,
    ) -> SessionSummary:
        session_id = f"{int(time.time() * 1000)}-{uuid.uuid4().hex[:8]}"
        summary = SessionSummary(
            session_id=session_id,
            mode=mode,
            symbol=symbol,
            interval=interval,
            started_at_ms=int(time.time() * 1000),
            model_version=model_version,
            metadata=metadata or {},
        )
        self._session_dir(session_id).mkdir(parents=True, exist_ok=True)
        self._write_summary(summary)
        return summary

    def record_snapshot(self, session_id: str, payload: dict[str, Any]) -> None:
        self._append_jsonl(session_id, "snapshots.jsonl", payload)

    def record_fill(self, session_id: str, payload: dict[str, Any]) -> None:
        self._append_jsonl(session_id, "fills.jsonl", payload)

    def finish_session(
        self,
        session_id: str,
        *,
        pnl: Decimal,
        max_drawdown: Decimal,
        trades: int,
        blocks: int,
        status: str,
    ) -> SessionSummary:
        summary = self.load_summary(session_id)
        summary.ended_at_ms = int(time.time() * 1000)
        summary.pnl = pnl
        summary.max_drawdown = max_drawdown
        summary.trades = trades
        summary.blocks = blocks
        summary.status = status
        self._write_summary(summary)
        return summary

    def list_sessions(self, limit: int = 5) -> list[SessionSummary]:
        summaries = [
            self.load_summary(path.name)
            for path in self.root.iterdir()
            if path.is_dir() and (path / "summary.json").exists()
        ]
        summaries.sort(key=lambda item: item.started_at_ms, reverse=True)
        return summaries[:limit]

    def load_summary(self, session_id: str) -> SessionSummary:
        payload = json.loads((self._session_dir(session_id) / "summary.json").read_text(encoding="utf-8"))
        payload["pnl"] = Decimal(str(payload.get("pnl", "0")))
        payload["max_drawdown"] = Decimal(str(payload.get("max_drawdown", "0")))
        return SessionSummary(**payload)

    def load_events(self, session_id: str, name: str = "snapshots.jsonl") -> list[dict[str, Any]]:
        path = self._session_dir(session_id) / name
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def export_session_jsonl(self, session_id: str) -> Path:
        return self._session_dir(session_id) / "snapshots.jsonl"

    def export_fills_csv(self, session_id: str) -> Path:
        fills = self.load_events(session_id, "fills.jsonl")
        path = self._session_dir(session_id) / "fills.csv"
        fields = sorted({key for fill in fills for key in fill.keys()})
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            if fields:
                writer.writeheader()
                writer.writerows(fills)
        return path

    def _append_jsonl(self, session_id: str, name: str, payload: dict[str, Any]) -> None:
        path = self._session_dir(session_id) / name
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, default=_json_default, sort_keys=True) + "\n")

    def _write_summary(self, summary: SessionSummary) -> None:
        path = self._session_dir(summary.session_id) / "summary.json"
        path.write_text(json.dumps(asdict(summary), default=_json_default, indent=2), encoding="utf-8")

    def _session_dir(self, session_id: str) -> Path:
        return self.root / session_id
