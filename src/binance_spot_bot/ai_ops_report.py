from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def write_ai_ops_report(root: Path, payload: dict[str, Any]) -> Path:
    out = Path(root) / "ai-ops" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    safe = redact_payload({**payload, "live_trading_enabled": False})
    path = out / "assistant-report.json"
    path.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
    md = out / "assistant-report.md"
    md.write_text(
        "\n".join(
            [
                "# AI Ops Assistant Report",
                "",
                f"Status: {safe.get('status', 'ok')}",
                f"Questions: {safe.get('questions', 0)}",
                f"Forbidden blocked: {safe.get('forbidden_blocked', 0)}",
                "Live trading: disabled",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return path
