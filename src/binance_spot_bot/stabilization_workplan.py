from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def build_stabilization_workplans(backlog: dict[str, Any], priority: str | None = None) -> dict[str, Any]:
    items = [item for item in backlog.get("items", []) if priority is None or item.get("priority") == priority]
    workplans = []
    for item in items:
        workplans.append(
            {
                "workplan_id": f"WP-{item['item_id']}",
                "related_backlog_item_ids": [item["item_id"]],
                "subsystem": item.get("domain", "paper_os"),
                "allowed_files": ["src/binance_spot_bot", "tests", "docs"],
                "forbidden_files": ["src/binance_spot_bot/live_trading"],
                "recommended_steps": ["reproduce finding", "apply smallest fix", "run required validation", "export evidence"],
                "required_tests": ["python -m pytest tests/test_roadmap_101_stabilization_acceptance.py -q"],
                "required_evidence": ["stabilization_report", "no_live_proof"],
                "rollback_plan": "revert only files changed for this workplan if validation fails",
                "no_live_constraints": ["no live mode", "no signed order/account endpoints"],
                "expected_validation_command": "python -m binance_spot_bot.cli stabilization-gate --profile standard --json",
                "live_trading_enabled": False,
            }
        )
    return {"status": "ready" if workplans else "clean", "workplans": workplans, "live_trading_enabled": False}


def stabilization_workplan(blockers: list[str]) -> dict[str, Any]:
    backlog = {"items": [{"item_id": f"STAB-{i:03d}", "title": blocker, "priority": "P1", "domain": "manual"} for i, blocker in enumerate(blockers, 1)]}
    return build_stabilization_workplans(backlog)


def write_stabilization_workplans(root: Path | str, payload: dict[str, Any]) -> dict[str, str]:
    root = Path(root)
    out = root / "data" / "stabilization" / "workplans"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "stabilization_workplans.json"
    md_path = out / "stabilization_workplans.md"
    json_path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    md_path.write_text(f"# Stabilization Workplans\n\nStatus: {payload['status']}\nWorkplans: {len(payload['workplans'])}\nLive trading: disabled\n", encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}
