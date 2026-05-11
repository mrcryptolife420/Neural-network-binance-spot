from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_contains_trend_retention_timeline_report_markers() -> None:
    text = (ROOT / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py").read_text(encoding="utf-8")

    assert "Diagnostics retention preview" in text
    assert "Operator incident timeline" in text
    assert "Export operator report" in text
    assert "Operator report" in text
