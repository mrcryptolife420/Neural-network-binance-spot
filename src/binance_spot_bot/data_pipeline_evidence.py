from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .data_quality_v2 import data_quality_v2
from .redaction import redact_payload


def data_pipeline_lineage(dataset_id: str, artifacts: dict[str, str]) -> dict[str, Any]:
    ordered = ["raw", "candles", "features", "labels", "manifest", "evaluation", "model"]
    return {
        "status": "ready",
        "dataset_id": dataset_id,
        "lineage": [{"stage": key, "path": artifacts.get(key, "")} for key in ordered if key in artifacts],
        "live_trading_enabled": False,
    }


def write_data_pipeline_evidence(path: Path | str, dataset_id: str, rows: list[dict[str, Any]], artifacts: dict[str, str]) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "dataset_id": dataset_id,
        "quality": data_quality_v2(rows),
        "redaction_sample": redact_payload(rows[:1]),
        "lineage": data_pipeline_lineage(dataset_id, artifacts),
        "live_trading_enabled": False,
    }
    target.write_text(json.dumps(redact_payload(payload), indent=2, sort_keys=True), encoding="utf-8")
    return target
