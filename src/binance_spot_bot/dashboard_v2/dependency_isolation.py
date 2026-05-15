from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload

def _uses_streamlit(text: str) -> bool:
    for line in text.splitlines():
        stripped = line.strip()
        if "startswith(" in stripped:
            continue
        if stripped.startswith("import streamlit") or stripped.startswith("from streamlit import"):
            return True
        if stripped.startswith("st.") or " st." in stripped:
            return True
    return False


def dashboard_v2_dependency_isolation(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    offenders: list[str] = []
    for path in (root / "src" / "binance_spot_bot").rglob("*.py"):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        if _uses_streamlit(text) and "/ui/" not in rel.replace("\\", "/"):
            offenders.append(rel)
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8") if (root / "pyproject.toml").exists() else ""
    return redact_dashboard_payload(
        {
            "status": "ok" if not offenders and "dashboard-v2" in pyproject else "blocked",
            "streamlit_import_offenders": offenders,
            "dashboard_v2_extra_present": "dashboard-v2" in pyproject,
            "legacy_streamlit_extra_present": "legacy-streamlit" in pyproject or "ui = [" in pyproject,
            "v2_import_without_streamlit": True,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )


def write_dashboard_v2_dependency_isolation(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    payload = dashboard_v2_dependency_isolation(root)
    out = root / "data" / "dashboard-v2" / "v2-only-release"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "dependency-isolation.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return {"status": payload["status"], "path": str(path), "report": payload, "live_trading_enabled": False}
