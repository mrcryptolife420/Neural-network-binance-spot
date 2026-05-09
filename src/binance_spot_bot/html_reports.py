from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def export_html_report(title: str, payload: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    safe_json = json.dumps(redact_payload(payload), indent=2, default=str)
    body = f"<!doctype html><html><head><meta charset=\"utf-8\"><title>{html.escape(title)}</title></head><body><h1>{html.escape(title)}</h1><pre>{html.escape(safe_json)}</pre></body></html>"
    path.write_text(body, encoding="utf-8")
    return path
