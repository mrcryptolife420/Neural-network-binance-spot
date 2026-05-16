from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .common import json_write, path_in, stable_hash


class PortfolioExperimentStore:
    def __init__(self, root: Path) -> None:
        self.root = path_in(root, "data", "portfolio-lab")
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, kind: str, item_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        path = path_in(self.root, kind, item_id, f"{kind[:-1] if kind.endswith('s') else kind}.json")
        return json_write(path, payload)

    def list(self, kind: str) -> dict[str, Any]:
        folder = path_in(self.root, kind)
        rows: list[dict[str, Any]] = []
        if folder.exists():
            for path in sorted(folder.glob("*/*.json")):
                payload = json.loads(path.read_text(encoding="utf-8"))
                rows.append({"path": str(path), "sha256": stable_hash(payload), "payload": payload})
        return {"status": "ok", kind: rows, "live_trading_enabled": False}

    def load(self, kind: str, item_id: str) -> dict[str, Any]:
        folder = path_in(self.root, kind, item_id)
        files = sorted(folder.glob("*.json"))
        if not files:
            raise FileNotFoundError(item_id)
        return json.loads(files[0].read_text(encoding="utf-8"))

    def manifest(self) -> dict[str, Any]:
        kinds = ["baskets", "allocations", "runs", "simulations", "stress-tests", "scorecards", "reports", "evidence"]
        return {"status": "ok", "kinds": {kind: len(self.list(kind).get(kind, [])) for kind in kinds}, "live_trading_enabled": False}


def default_portfolio_store(root: Path) -> PortfolioExperimentStore:
    return PortfolioExperimentStore(root)

