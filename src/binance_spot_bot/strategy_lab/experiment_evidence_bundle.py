from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

from binance_spot_bot.redaction import redact_payload
from . import NO_ADVICE_STATEMENT, NO_LIVE_STATEMENT


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def export_strategy_lab_evidence(root: Path | str, artifacts: dict[str, Any] | None = None) -> dict[str, Any]:
    root = Path(root)
    run_id = str(int(time.time() * 1000))
    out = root / "data" / "strategy-lab" / "evidence" / run_id
    files_dir = out / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    artifacts = artifacts or {}
    artifacts = {
        "safety_contract": {"paper_only": True, "no_live_statement": NO_LIVE_STATEMENT, "no_advice_statement": NO_ADVICE_STATEMENT, "live_trading_enabled": False},
        **artifacts,
    }
    files = []
    for name, payload in artifacts.items():
        text = json.dumps(redact_payload(payload), indent=2, default=str)
        path = files_dir / f"{name}.json"
        path.write_text(text, encoding="utf-8")
        files.append({"name": name, "path": str(path), "sha256": _hash(text)})
    manifest = redact_payload({"status": "ok", "run_id": run_id, "files": files, "no_live_statement": NO_LIVE_STATEMENT, "no_advice_statement": NO_ADVICE_STATEMENT, "live_trading_enabled": False})
    manifest_path = out / "strategy_lab_evidence_manifest.json"
    summary_path = out / "strategy_lab_evidence_summary.md"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    summary_path.write_text(f"# Strategy Lab Evidence\n\nStatus: ok\n\n{NO_ADVICE_STATEMENT}\n", encoding="utf-8")
    return {"status": "ok", "run_id": run_id, "manifest": str(manifest_path), "summary": str(summary_path), "files": files, "live_trading_enabled": False}
