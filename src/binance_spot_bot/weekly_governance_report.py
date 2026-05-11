from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def write_weekly_governance_report(root: Path, payload: dict[str, Any]) -> dict[str, str]:
    stamp = datetime.now(timezone.utc).strftime("%Y-W%V")
    out = root / "policy-governance" / "weekly" / stamp
    out.mkdir(parents=True, exist_ok=True)
    safe = redact_payload({**payload, "live_trading_enabled": False})
    json_path = out / "weekly_governance_report.json"
    md_path = out / "weekly_governance_report.md"
    json_path.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# Weekly Paper Policy Governance Report",
                "",
                f"Current champion: {safe.get('current_champion', 'none')}",
                f"Decision: {safe.get('decision', {}).get('decision', 'none')}",
                "Live trading: disabled",
            ]
        ),
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}
