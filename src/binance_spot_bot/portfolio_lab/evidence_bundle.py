from __future__ import annotations

from pathlib import Path
from typing import Any

from . import NO_ADVICE_STATEMENT, NO_LIVE_STATEMENT, PAPER_ONLY_RESEARCH_STATEMENT
from .common import json_write, stable_hash
from .portfolio_experiment_store import default_portfolio_store


def export_portfolio_lab_evidence(root: Path, run: dict[str, Any] | None = None) -> dict[str, Any]:
    run = run or {"run_id": "latest", "status": "ok", "live_trading_enabled": False}
    run_id = str(run.get("run_id", "latest"))
    evidence_root = root / "data" / "portfolio-lab" / "evidence" / run_id
    files: list[dict[str, Any]] = []
    files.append(json_write(evidence_root / "files" / "portfolio_run.json", run))
    manifest = {
        "status": "ok",
        "run_id": run_id,
        "safety_contract": "docs/portfolio-lab/paper-portfolio-research-safety-contract.md",
        "no_live_statement": NO_LIVE_STATEMENT,
        "no_financial_advice_statement": NO_ADVICE_STATEMENT,
        "paper_only_research_statement": PAPER_ONLY_RESEARCH_STATEMENT,
        "no_real_allocation_proof": True,
        "redaction_proof": True,
        "store_manifest": default_portfolio_store(root).manifest(),
        "files": files,
        "hashes": [item["sha256"] for item in files],
        "live_trading_enabled": False,
    }
    manifest["manifest_hash"] = stable_hash(manifest)
    saved_manifest = json_write(evidence_root / "portfolio_lab_evidence_manifest.json", manifest)
    summary = "\n".join(
        [
            "# Portfolio Lab Evidence",
            "",
            NO_LIVE_STATEMENT,
            NO_ADVICE_STATEMENT,
            PAPER_ONLY_RESEARCH_STATEMENT,
            "",
            f"Run: {run_id}",
            f"Manifest hash: {manifest['manifest_hash']}",
        ]
    )
    summary_path = evidence_root / "portfolio_lab_evidence_summary.md"
    summary_path.write_text(summary, encoding="utf-8")
    return {"status": "ok", "manifest": manifest, "saved_manifest": saved_manifest, "summary_path": str(summary_path), "live_trading_enabled": False}

