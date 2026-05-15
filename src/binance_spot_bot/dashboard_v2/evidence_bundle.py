from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

from .cutover_readiness import write_dashboard_v2_cutover_readiness
from .launcher import dashboard_v2_launcher_report
from .payload_profiles import dashboard_v2_payload_profile_report
from .performance_baseline import write_dashboard_v2_performance_report
from .performance_budgets import write_dashboard_v2_budget_report
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .static_build import verify_dashboard_v2_static_build
from .support_diagnostics import dashboard_v2_support_diagnostics
from .ws_stability import dashboard_v2_ws_stability_smoke


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def export_dashboard_v2_evidence_bundle(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    run_id = str(int(time.time() * 1000))
    out = root / "data" / "dashboard-v2" / "evidence" / run_id
    files_dir = out / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "performance_baseline": write_dashboard_v2_performance_report(root),
        "performance_budget": write_dashboard_v2_budget_report(root),
        "payload_profiles": dashboard_v2_payload_profile_report(),
        "ws_stability": dashboard_v2_ws_stability_smoke(),
        "static_build": verify_dashboard_v2_static_build(root),
        "launcher": dashboard_v2_launcher_report(root, no_browser=True),
        "support_diagnostics": dashboard_v2_support_diagnostics(root),
        "cutover_readiness": write_dashboard_v2_cutover_readiness(root),
        "no_live_proof": {"no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False},
    }
    copied: list[dict[str, Any]] = []
    for name, artifact in artifacts.items():
        text = json.dumps(redact_dashboard_payload(artifact), indent=2, default=str)
        path = files_dir / f"{name}.json"
        path.write_text(text, encoding="utf-8")
        copied.append({"name": name, "path": str(path), "sha256_16": _hash_text(text)})
    manifest = {
        "status": "ok",
        "run_id": run_id,
        "files": copied,
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }
    manifest = redact_dashboard_payload(manifest)
    manifest_path = out / "dashboard_v2_evidence_manifest.json"
    summary_path = out / "dashboard_v2_evidence_summary.md"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    summary_path.write_text(
        "# Dashboard V2 Evidence Bundle\n\n"
        f"Status: {manifest['status']}\n"
        f"No-live proof: {manifest['no_live_statement']}\n"
        f"Files: {len(copied)}\n",
        encoding="utf-8",
    )
    return {"status": "ok", "run_id": run_id, "manifest": str(manifest_path), "summary": str(summary_path), "files": copied, "live_trading_enabled": False}
