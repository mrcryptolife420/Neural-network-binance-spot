from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .session_store import SessionStore


@dataclass(frozen=True)
class ReplayFrame:
    index: int
    snapshot: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ReplaySandbox:
    def __init__(self, store: SessionStore):
        self.store = store

    def load(self, session_id: str) -> list[ReplayFrame]:
        return [ReplayFrame(index, snapshot) for index, snapshot in enumerate(self.store.load_events(session_id, "snapshots.jsonl"))]

    def frame(self, session_id: str, index: int) -> ReplayFrame:
        frames = self.load(session_id)
        if not frames:
            raise ValueError("session has no replay frames")
        return frames[max(0, min(index, len(frames) - 1))]

    def chart_points(self, session_id: str) -> list[dict[str, Any]]:
        points = []
        for frame in self.load(session_id):
            snapshot = frame.snapshot
            points.append(
                {
                    "index": frame.index,
                    "timestamp_ms": snapshot.get("timestamp_ms", frame.index),
                    "equity": snapshot.get("equity"),
                    "price": snapshot.get("last_price") or snapshot.get("market", {}).get("last_price"),
                }
            )
        return points
