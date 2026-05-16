from __future__ import annotations

from pathlib import Path
from typing import Any

from . import NO_ADVICE_STATEMENT, NO_LIVE_STATEMENT, PAPER_ONLY_RESEARCH_STATEMENT
from .common import json_write, stable_hash


def export_walk_forward_evidence(root: Path, rolling_report: dict[str, Any], performance: dict[str, Any], scorecards: dict[str, Any], gate: dict[str, Any]) -> dict[str, Any]:
    run_id = str(rolling_report.get("run_id", "latest"))
    evidence_root = root / "data" / "portfolio-lab" / "walk-forward" / "evidence" / run_id
    files = [
        json_write(evidence_root / "files" / "rolling_report.json", rolling_report),
        json_write(evidence_root / "files" / "performance.json", performance),
        json_write(evidence_root / "files" / "robustness_scorecards.json", scorecards),
        json_write(evidence_root / "files" / "governance_gate.json", gate),
    ]
    manifest = {
        "status": "ok",
        "run_id": run_id,
        "safety_contract": "docs/portfolio-lab/walk-forward-robustness-safety-contract.md",
        "no_live_statement": NO_LIVE_STATEMENT,
        "no_financial_advice_statement": NO_ADVICE_STATEMENT,
        "paper_only_research_statement": PAPER_ONLY_RESEARCH_STATEMENT,
        "split_evidence_present": bool(rolling_report.get("split", {}).get("split", {}).get("windows")),
        "redaction_proof": True,
        "files": files,
        "hashes": [item["sha256"] for item in files],
        "live_trading_enabled": False,
    }
    manifest["manifest_hash"] = stable_hash(manifest)
    saved = json_write(evidence_root / "walk_forward_evidence_manifest.json", manifest)
    summary_path = evidence_root / "walk_forward_evidence_summary.md"
    summary_path.write_text(f"# Walk-Forward Evidence\n\n{NO_LIVE_STATEMENT}\n\nRun: {run_id}\n", encoding="utf-8")
    return {"status": "ok", "manifest": manifest, "saved_manifest": saved, "summary_path": str(summary_path), "live_trading_enabled": False}

