from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


REMOTE_URL_RE = re.compile(r"//cdn\.|https?://cdn\.|fonts\.(?:googleapis|gstatic)\.com", re.IGNORECASE)


def verify_dashboard_v2_static_build(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    candidates = [
        root / "src" / "binance_spot_bot" / "dashboard_v2" / "static",
        root / "dashboard-v2" / "dist",
    ]
    build_dir = next((path for path in candidates if (path / "index.html").exists()), candidates[0])
    files = [path for path in build_dir.rglob("*") if path.is_file()] if build_dir.exists() else []
    warnings: list[str] = []
    hard_blockers: list[str] = []
    if not (build_dir / "index.html").exists():
        warnings.append("static build missing; Vite dev server or fallback can still be used")
    remote_refs: list[str] = []
    for path in files:
        if path.suffix.lower() not in {".html", ".js", ".css", ".json"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if REMOTE_URL_RE.search(text):
            remote_refs.append(str(path.relative_to(root)))
    if remote_refs:
        hard_blockers.append("external URL/CDN reference found")
    manifest = build_dir / "manifest.json"
    if not manifest.exists():
        manifest = build_dir / ".vite" / "manifest.json"
    payload = {
        "status": "blocked" if hard_blockers else "warn" if warnings else "ok",
        "build_dir": str(build_dir),
        "index_exists": (build_dir / "index.html").exists(),
        "manifest_exists": manifest.exists(),
        "asset_count": len(files),
        "external_refs": remote_refs,
        "warnings": warnings,
        "hard_blockers": hard_blockers,
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }
    if manifest.exists():
        payload["manifest"] = json.loads(manifest.read_text(encoding="utf-8"))
    return redact_dashboard_payload(payload)
