from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def write_long_term_analytics_report(root: Path, payload: dict[str, Any], *, period: str = "daily") -> dict[str, str]:
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y-%m-%d" if period == "daily" else "%Y-W%V" if period == "weekly" else "%Y-%m")
    out = root / "metrics" / "reports" / period / stamp
    out.mkdir(parents=True, exist_ok=True)
    safe = redact_payload({**payload, "period": period, "live_trading_enabled": False})
    json_path = out / "analytics-report.json"
    md_path = out / "analytics-report.md"
    json_path.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# Local Observability Analytics Report",
                "",
                "LOCAL OBSERVABILITY ONLY",
                f"Period: {period}",
                f"Status: {safe.get('status', 'ok')}",
                f"Recommended action: {safe.get('recommended_action', 'none')}",
                "Live trading: disabled",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}
