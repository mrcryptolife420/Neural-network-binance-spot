from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


@dataclass(frozen=True)
class ChartSyncState:
    workspace_id: str
    time_range_ms: tuple[int, int] = (0, 0)
    crosshair_timestamp_ms: int | None = None
    symbol: str = "BTCUSDT"
    paused: bool = False
    replay_index: int = 0
    overlays: tuple[str, ...] = ("signals", "fills", "risk_blocks")
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


def create_chart_sync_state(workspace_id: str, *, symbol: str = "BTCUSDT", paused: bool = False) -> dict[str, Any]:
    return {
        "status": "ok",
        "sync": ChartSyncState(workspace_id=workspace_id, symbol=symbol.upper(), paused=paused).to_dict(),
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }


def compare_chart_sessions(current: list[dict[str, Any]], previous: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "status": "ok",
        "current_points": len(current),
        "previous_points": len(previous),
        "delta_points": len(current) - len(previous),
        "overlays": ["signals", "fills", "risk_blocks"],
        "live_trading_enabled": False,
    }
