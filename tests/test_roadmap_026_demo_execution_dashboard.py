from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_contains_demo_execution_drill_panel() -> None:
    text = (ROOT / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py").read_text(encoding="utf-8")
    assert "Demo Execution Drill" in text
    assert "Test order only" in text
    assert "Confirm demo order" in text
    assert "Cancel order" in text


def test_operator_evidence_includes_demo_execution_drill() -> None:
    text = (ROOT / "src" / "binance_spot_bot" / "dashboard_evidence.py").read_text(encoding="utf-8")
    assert "demo_execution_drill" in text
    assert "demo_execution_drill.json" in text


def test_demo_execution_docs_exist() -> None:
    assert (ROOT / "docs" / "demo-execution-sandbox.md").exists()
    assert (ROOT / "docs" / "demo-order-lifecycle-drill.md").exists()
