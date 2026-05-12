from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from .code_ownership import owner_for_file
from .safety_surface_map import safety_surface_map


def detect_changed_files(root: Path | str = ".", changed: list[str] | None = None) -> dict[str, Any]:
    root_path = Path(root)
    warnings = []
    files = changed or []
    if not files:
        try:
            result = subprocess.run(["git", "diff", "--name-only"], cwd=root_path, text=True, capture_output=True, timeout=5, check=False)
            files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        except Exception as exc:  # pragma: no cover - git may be unavailable
            warnings.append(f"git_unavailable:{exc.__class__.__name__}")
    items = []
    surfaces = safety_surface_map(files)["surfaces"]
    for path in files:
        items.append({"path": path, "status": "modified" if (root_path / path).exists() else "unknown", "owner": owner_for_file(path), "safety_surface": [item["surface"] for item in surfaces if item["file"] == path]})
    return {"status": "ready", "payload": {"files": items, "warnings": warnings}, "live_trading_enabled": False}
