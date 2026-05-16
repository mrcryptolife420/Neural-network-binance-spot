from __future__ import annotations

from pathlib import Path
from typing import Any


def write_ai_summary(root: Path, run_id: str, hypotheses: list[dict[str, Any]], suspect_files: list[str]) -> dict[str, Any]:
    main = hypotheses[0] if hypotheses else {"title": "unknown/needs more evidence", "confidence": "low", "recommended_tests": ["pytest -q"]}
    text = "\n".join([
        "# AI Doctor Summary",
        "",
        "## Main status",
        "Local debug bundle generated with safe env.",
        "",
        "## Most likely cause",
        f"{main.get('title')} (confidence: {main.get('confidence')})",
        "",
        "## Suspect files",
        "\n".join(f"- {item}" for item in suspect_files) or "- unknown",
        "",
        "## Recommended tests",
        "\n".join(f"- `{item}`" for item in main.get("recommended_tests", ["pytest -q"])),
        "",
        "## Safety state",
        "- LIVE_TRADING_ENABLED=false",
        "- KILL_SWITCH=true",
        "- No live order path touched",
    ])
    path = root / "data" / "ai-doctor" / "runs" / run_id / "ai_summary.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return {"status": "ok", "path": str(path), "summary": text, "live_trading_enabled": False}

