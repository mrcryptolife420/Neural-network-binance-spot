from __future__ import annotations

from pathlib import Path
from typing import Any


def generate_pr_template(roadmap: int | str = "090", phase: str = "foundation", kind: str = "feature", out: Path | str | None = None) -> dict[str, Any]:
    number = f"{int(str(roadmap).lstrip('0') or '0'):03d}" if str(roadmap).isdigit() else str(roadmap)
    text = "\n".join(
        [
            f"# Roadmap {number} {kind.title()} PR",
            "",
            f"Phase: {phase}",
            "",
            "## Summary",
            "- ",
            "",
            "## Changed Files",
            "- ",
            "",
            "## Safety Constraints",
            "- Local-only",
            "- No live trading",
            "- No signed Binance endpoints",
            "- No order/account endpoints",
            "- No secrets in artifacts",
            "",
            "## Tests Run",
            "- [ ] `python -m pytest -q`",
            "- [ ] `python -m binance_spot_bot.cli check-all --skip-tests --json`",
            "- [ ] Dashboard/browser smoke if dashboard changed",
            "",
            "## Evidence",
            "- [ ] Evidence manifest generated",
            "- [ ] No-live proof present",
            "",
            "## Rollback Notes",
            "- Revert scoped files only.",
            "",
            "Live trading enabled: false",
            "",
        ]
    )
    path = None
    if out:
        out_path = Path(out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        path = str(out_path)
    return {"status": "ready", "roadmap": number, "phase": phase, "kind": kind, "markdown": text, "path": path, "live_trading_enabled": False}


def pr_template(title: str) -> dict[str, Any]:
    return generate_pr_template(roadmap="000", phase=title, kind="feature")
