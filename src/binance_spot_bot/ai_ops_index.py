from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .redaction import redact_text


def build_ai_ops_index(paths: list[Path], out: Path | None = None) -> dict[str, Any]:
    rows = []
    for path in paths:
        path = Path(path)
        if not path.exists() or not path.is_file():
            continue
        text = redact_text(path.read_text(encoding="utf-8", errors="replace"))[:4000]
        rows.append({"path": str(path), "title": path.stem, "terms": sorted(set(text.lower().replace("#", " ").split()))[:200], "snippet": text[:500]})
    payload = {"status": "ready", "items": rows, "live_trading_enabled": False}
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return payload


def search_ai_ops_index(query: str, docs: list[str] | None = None, *, index: dict[str, Any] | None = None) -> dict[str, Any]:
    q = query.lower()
    if index is None:
        matches = [{"path": doc, "snippet": doc} for doc in (docs or []) if q in doc.lower()]
    else:
        matches = [item for item in index.get("items", []) if q in " ".join(item.get("terms", [])) or q in item.get("snippet", "").lower()]
    return {"status": "ready", "matches": matches[:10], "live_trading_enabled": False}
