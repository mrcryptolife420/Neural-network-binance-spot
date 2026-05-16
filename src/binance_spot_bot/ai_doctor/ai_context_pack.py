from __future__ import annotations

from pathlib import Path


def write_ai_context_pack(root: Path, summary: str, prompt: str) -> dict[str, object]:
    out = root / "data" / "ai-context"
    out.mkdir(parents=True, exist_ok=True)
    (out / "latest-ai-doctor-summary.md").write_text(summary, encoding="utf-8")
    (out / "latest-codex-fix-prompt.md").write_text(prompt, encoding="utf-8")
    return {"status": "ok", "summary_path": str(out / "latest-ai-doctor-summary.md"), "prompt_path": str(out / "latest-codex-fix-prompt.md"), "live_trading_enabled": False}

