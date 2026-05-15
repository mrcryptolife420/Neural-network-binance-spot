from __future__ import annotations

import json
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .schemas import redact_dashboard_payload

SYMBOL_RE = re.compile(r"^[A-Z0-9]{3,20}$")


@dataclass(frozen=True)
class DashboardV2Watchlist:
    watchlist_id: str
    name: str
    symbols: tuple[str, ...]
    default_interval: str = "1m"
    source_preference: str = "demo"
    notes: str = ""
    tags: tuple[str, ...] = ()
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    updated_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


def validate_symbols(symbols: list[str] | tuple[str, ...]) -> list[str]:
    return [symbol for symbol in symbols if not SYMBOL_RE.match(symbol)]


class DashboardV2WatchlistStore:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def create(self, name: str, symbols: list[str] | tuple[str, ...]) -> dict[str, Any]:
        clean = tuple(symbol.strip().upper() for symbol in symbols if symbol.strip())
        invalid = validate_symbols(clean)
        if invalid:
            return {"status": "blocked", "blockers": [f"invalid symbols: {', '.join(invalid)}"], "live_trading_enabled": False}
        watchlist_id = re.sub(r"[^a-z0-9_-]+", "-", name.lower()).strip("-") or "watchlist"
        item = DashboardV2Watchlist(watchlist_id=watchlist_id, name=name, symbols=clean)
        path = self.root / f"{watchlist_id}.json"
        path.write_text(json.dumps(item.to_dict(), indent=2), encoding="utf-8")
        return {"status": "ok", "watchlist": item.to_dict(), "path": str(path), "live_trading_enabled": False}

    def list(self) -> dict[str, Any]:
        rows = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(self.root.glob("*.json"))]
        return {"status": "ok", "watchlists": rows, "count": len(rows), "live_trading_enabled": False}

    def delete(self, watchlist_id: str, *, confirm: str = "") -> dict[str, Any]:
        if confirm != watchlist_id:
            return {"status": "blocked", "blockers": ["delete requires confirm matching watchlist id"], "live_trading_enabled": False}
        path = self.root / f"{watchlist_id}.json"
        if path.exists():
            path.unlink()
        return {"status": "ok", "deleted": watchlist_id, "live_trading_enabled": False}


def default_watchlist_store(root: Path | str = ".") -> DashboardV2WatchlistStore:
    return DashboardV2WatchlistStore(Path(root) / "data" / "dashboard-v2" / "watchlists")
