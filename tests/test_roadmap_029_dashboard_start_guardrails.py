from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_contains_pilot_start_guardrail_markers() -> None:
    text = (ROOT / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py").read_text(encoding="utf-8")

    assert "Pilot run" in text
    assert "Start action" in text
    assert "Recovery action" in text
    assert "Pilot is already running" in text
    assert "disabled=start_disabled" in text


def test_pilot_recovery_docs_exist() -> None:
    assert (ROOT / "docs" / "demo-pilot-state-recovery.md").exists()
