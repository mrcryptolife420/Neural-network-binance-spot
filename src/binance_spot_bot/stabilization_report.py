from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def build_stabilization_report(
    ingest: dict[str, Any],
    backlog: dict[str, Any],
    gate: dict[str, Any],
    *,
    reliability: dict[str, Any] | None = None,
    gaps: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return redact_payload(
        {
            "status": "ok" if gate.get("status") == "pass" else "blocked",
            "executive_summary": "Paper OS stabilization report generated with live trading disabled.",
            "roadmap100_input_status": ingest.get("status"),
            "backlog_summary": {"status": backlog.get("status"), "items": len(backlog.get("items", []))},
            "gate": gate,
            "check_reliability": reliability or {},
            "evidence_gaps": gaps or {},
            "readiness_score_delta": 0,
            "recommended_next_fixes": [item.get("title") for item in backlog.get("items", [])[:5]],
            "no_live_proof": "required",
            "live_trading_enabled": False,
        }
    )


def write_stabilization_report(root: Path, payload: dict) -> dict[str, str]:
    out = root / "data" / "stabilization" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    safe = redact_payload(payload)
    json_path = out / "stabilization_report.json"
    md_path = out / "stabilization_report.md"
    json_path.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        f"# Stabilization Report\n\nStatus: {safe['status']}\nBacklog items: {safe['backlog_summary']['items']}\nLive trading: disabled\n",
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}
