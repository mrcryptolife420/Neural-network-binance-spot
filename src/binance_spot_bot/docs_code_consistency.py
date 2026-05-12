from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .cli_surface_map import build_cli_surface_map


def build_docs_code_consistency(root: Path | str = ".") -> dict[str, Any]:
    root_path = Path(root)
    docs_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in (root_path / "docs").rglob("*.md")) if (root_path / "docs").exists() else ""
    commands = build_cli_surface_map(root_path)["payload"]["commands"]
    stale_or_missing = [item["command"] for item in commands if item["command"] not in docs_text and item["command"] in {"check-all", "dashboard-smoke", "roadmap-index", "impact-analysis"}]
    no_live_drift = "live trading enabled: false" not in docs_text.lower()
    payload = {"status": "warning" if stale_or_missing or no_live_drift else "ok", "missing_docs": stale_or_missing, "no_live_doc_drift": no_live_drift, "live_trading_enabled": False}
    out = root_path / "data" / "repository-knowledge" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    (out / "docs_code_consistency_report.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (out / "docs_code_consistency_report.md").write_text(f"# Docs Code Consistency\n\n- Status: {payload['status']}\n- Live trading enabled: false\n", encoding="utf-8")
    return payload


def docs_code_consistency(docs: list[str], modules: list[str]) -> dict[str, Any]:
    missing = [module for module in modules if not any(module in doc for doc in docs)]
    return {"status": "ok" if not missing else "warning", "missing": missing, "live_trading_enabled": False}
