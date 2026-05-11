from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def write_weekly_governance_report(root: Path, payload: dict[str, Any]) -> dict[str, str]:
    stamp = datetime.now(timezone.utc).strftime("%Y-W%V")
    out = root / "policy-governance" / "weekly" / stamp
    out.mkdir(parents=True, exist_ok=True)
    safe = redact_payload({**payload, "live_trading_enabled": False})
    json_path = out / "weekly_governance_report.json"
    md_path = out / "weekly_governance_report.md"
    policy_csv = out / "policy_status.csv"
    experiment_csv = out / "experiment_results.csv"
    decisions_jsonl = out / "governance_decisions.jsonl"
    manifest_path = out / "evidence_manifest.json"
    json_path.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
    md_path.write_text(_markdown_summary(safe), encoding="utf-8")
    _write_csv(policy_csv, safe.get("policies", [{"policy_id": safe.get("current_champion", "none"), "status": "champion"}]))
    _write_csv(experiment_csv, safe.get("experiments", [_flatten_experiment(safe.get("experiment", {}))]))
    decisions = safe.get("decisions", [safe.get("decision", {})])
    decisions_jsonl.write_text("\n".join(json.dumps(row, default=str) for row in decisions if row) + "\n", encoding="utf-8")
    manifest = {
        "files": [
            {"name": path.name, "relative_path": path.name, "bytes": path.stat().st_size}
            for path in (json_path, md_path, policy_csv, experiment_csv, decisions_jsonl)
        ],
        "live_trading_enabled": False,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {
        "json": str(json_path),
        "markdown": str(md_path),
        "policy_status_csv": str(policy_csv),
        "experiment_results_csv": str(experiment_csv),
        "decisions_jsonl": str(decisions_jsonl),
        "evidence_manifest": str(manifest_path),
    }


def _markdown_summary(payload: dict[str, Any]) -> str:
    decision = payload.get("decision", {})
    return "\n".join(
        [
            "# Weekly Paper Policy Governance Report",
            "",
            f"Current champion: {payload.get('current_champion', payload.get('cur_champion', 'none'))}",
            f"Decision: {decision.get('decision', 'none') if isinstance(decision, dict) else decision}",
            "Modes: paper-only",
            "Live trading: disabled",
            "",
        ]
    )


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    normalized = [row for row in rows if isinstance(row, dict)] or [{"status": "empty"}]
    fields = sorted({field for row in normalized for field in row.keys()})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(normalized)


def _flatten_experiment(experiment: dict[str, Any]) -> dict[str, Any]:
    if not experiment:
        return {"status": "missing"}
    challenger = experiment.get("metrics", {}).get("challenger", {})
    champion = experiment.get("metrics", {}).get("champion", {})
    return {
        "experiment_id": experiment.get("experiment_id", ""),
        "decision": experiment.get("decision", ""),
        "champion_rar": champion.get("risk_adjusted_ret", 0),
        "challenger_rar": challenger.get("risk_adjusted_ret", 0),
        "challenger_drawdown": challenger.get("drawdown", 0),
        "challenger_policy_violations": challenger.get("policy_violations", 0),
    }
