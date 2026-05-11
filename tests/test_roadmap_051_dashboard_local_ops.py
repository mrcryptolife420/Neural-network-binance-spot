from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_contains_local_ops_single_pane_markers() -> None:
    text = (ROOT / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py").read_text(encoding="utf-8")

    assert "Local artifact catalog" in text
    assert "Diagnostics baseline drift" in text
    assert "Support bundle verification matrix" in text
    assert "Operator command manifest" in text
