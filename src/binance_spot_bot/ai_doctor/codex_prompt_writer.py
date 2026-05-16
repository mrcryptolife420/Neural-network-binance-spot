from __future__ import annotations

from pathlib import Path
from typing import Any


def write_codex_fix_prompt(root: Path, run_id: str, matches: list[dict[str, Any]], suspect_files: list[str]) -> dict[str, Any]:
    tests = matches[0].get("recommended_tests", ["pytest -q"]) if matches else ["pytest -q"]
    prompt = "\n".join([
        "# Codex Fix Prompt",
        "",
        "Read the AI Doctor bundle first, then inspect the suspect files.",
        "",
        "Safety constraints:",
        "- do not start live trading.",
        "- Do not place or cancel orders.",
        "- Do not expose secrets.",
        "- Keep LIVE_TRADING_ENABLED=false and KILL_SWITCH=true in tests.",
        "",
        "Suspect files:",
        "\n".join(f"- {item}" for item in suspect_files) or "- unknown",
        "",
        "Acceptance tests:",
        "\n".join(f"- `{item}`" for item in tests),
    ])
    path = root / "data" / "ai-doctor" / "runs" / run_id / "codex_fix_prompt.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(prompt, encoding="utf-8")
    return {"status": "ok", "path": str(path), "prompt": prompt, "live_order_submitted": False}
