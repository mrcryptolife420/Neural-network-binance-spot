from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


REMOTE_URL_RE = re.compile(r"https?://(?!127\.0\.0\.1|localhost)|//cdn\.|fonts\.(?:googleapis|gstatic)\.com", re.IGNORECASE)
SECRET_RE = re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_/+=-]{20,}|[A-Za-z0-9]{64,}")
FORBIDDEN_LIVE_ORDER_RE = re.compile(r"/api/live/(first-order/execute)|/api/live-session/orders/execute", re.IGNORECASE)
REQUIRED_STATIC_FILES = ("index.html", "app.js", "styles.css", "manifest.json")
REQUIRED_APP_SNIPPETS = (
    "/api/health",
    "/api/pages",
    "/api/runtime/snapshot",
    "/api/live/status",
    "/api/ai-doctor/status",
)


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
    missing_required = [name for name in REQUIRED_STATIC_FILES if not (build_dir / name).exists()]
    if not build_dir.exists():
        warnings.append("static build missing; local fallback or dev server can still be used")
    elif missing_required:
        hard_blockers.append(f"missing required static files: {', '.join(missing_required)}")
    remote_refs: list[str] = []
    secret_refs: list[str] = []
    live_order_refs: list[str] = []
    empty_files: list[str] = []
    for path in files:
        if path.suffix.lower() not in {".html", ".js", ".css", ".json"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if not text.strip():
            empty_files.append(str(path.relative_to(root)))
        if REMOTE_URL_RE.search(text):
            remote_refs.append(str(path.relative_to(root)))
        if SECRET_RE.search(text):
            secret_refs.append(str(path.relative_to(root)))
        if FORBIDDEN_LIVE_ORDER_RE.search(text):
            live_order_refs.append(str(path.relative_to(root)))
    if remote_refs:
        hard_blockers.append("external URL/CDN reference found")
    if secret_refs:
        hard_blockers.append("secret-like value found in static build")
    if live_order_refs:
        hard_blockers.append("forbidden live order endpoint found in static build")
    if empty_files:
        hard_blockers.append("empty static file found")
    app_js = build_dir / "app.js"
    app_text = app_js.read_text(encoding="utf-8", errors="ignore") if app_js.exists() else ""
    missing_snippets = [snippet for snippet in REQUIRED_APP_SNIPPETS if snippet not in app_text] if build_dir.exists() else []
    if missing_snippets:
        hard_blockers.append(f"missing required API wiring: {', '.join(missing_snippets)}")
    combined_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in files if path.suffix.lower() in {".html", ".js", ".css", ".json"})
    if build_dir.exists() and ("LIVE_TRADING_ENABLED=false" not in combined_text or "KILL_SWITCH=true" not in combined_text):
        hard_blockers.append("safe env statement missing")
    manifest = build_dir / "manifest.json"
    if not manifest.exists():
        manifest = build_dir / ".vite" / "manifest.json"
    payload = {
        "status": "blocked" if hard_blockers else "warn" if warnings else "ok",
        "build_dir": str(build_dir),
        "index_exists": (build_dir / "index.html").exists(),
        "app_js_exists": (build_dir / "app.js").exists(),
        "styles_css_exists": (build_dir / "styles.css").exists(),
        "manifest_exists": manifest.exists(),
        "asset_count": len(files),
        "external_refs": remote_refs,
        "secret_refs": secret_refs,
        "live_order_refs": live_order_refs,
        "empty_files": empty_files,
        "missing_required": missing_required,
        "missing_api_wiring": missing_snippets,
        "warnings": warnings,
        "hard_blockers": hard_blockers,
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }
    if manifest.exists():
        payload["manifest"] = json.loads(manifest.read_text(encoding="utf-8"))
    return redact_dashboard_payload(payload)
