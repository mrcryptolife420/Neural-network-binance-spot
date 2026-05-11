from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_contains_recovery_diagnostics_markers() -> None:
    text = (ROOT / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py").read_text(encoding="utf-8")

    assert "Recovery & Diagnostics" in text
    assert "Refresh diagnostics" in text
    assert "Export support bundle" in text
    assert "Artifact inventory" in text
