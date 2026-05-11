from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .metrics_warehouse import aggregate_metrics


def aggregate_daily_metrics(rows: list[dict[str, Any]], out: Path | None = None) -> dict[str, Any]:
    summary = aggregate_metrics(rows)
    payload = {"period": "daily", **summary}
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        payload["path"] = str(out)
    return payload


def aggregate_weekly_metrics(rows: list[dict[str, Any]], out: Path | None = None) -> dict[str, Any]:
    summary = aggregate_metrics(rows)
    payload = {"period": "weekly", **summary}
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        payload["path"] = str(out)
    return payload
