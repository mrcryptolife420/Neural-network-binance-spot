from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_defaults_to_simple_demo_trading_flow() -> None:
    text = (ROOT / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py").read_text(encoding="utf-8")

    assert '"Simple demo trading", "Advanced tools"' in text
    assert "Start Demo Trading" in text
    assert "Use demo keys for this session" in text
    assert "Test demo connection" in text
    assert "Connect demo trading" in text
    assert "Start selected symbols" in text
    assert "Setup checklist" in text
    assert "Bot activity" in text
    assert "Multi Crypto Demo Trading" in text
    assert "Max active symbols" in text
    assert "Multi crypto bot status" in text
    assert "Symbol validation guardrails" in text
    assert "Budget allocation" in text
    assert "Risk limit summary" in text
    assert "Export multi-symbol evidence" in text
    assert "Stop one symbol" in text
    assert "Save active watchlist" in text
    assert "Live status panel" in text
    assert "@st.fragment(run_every=\"2s\")" in text
    assert "the full dashboard does not rerun" in text
    assert "_restart_completed_multi_runtime" in text
    assert "Chart focus symbol" in text
    assert "Visible candles" in text
    assert "multi_symbol_visual_overview" in text
    assert "max_demo_orders_per_session=max(10, max_trades)" in text
    assert "Adaptive Indicator Advisor" in text
    assert "Auto-select indicator profile" in text
    assert "Adaptive indicator advisor" in text
    assert "Bot trading decision explanation" in text
    assert "Risk adjusted allocation hints" in text
    assert "Export indicator evidence" in text
    assert "Focused regime" in text


def test_simple_dashboard_does_not_use_fast_full_page_rerun_loop() -> None:
    text = (ROOT / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py").read_text(encoding="utf-8")

    assert "time.sleep(0.7)" not in text
    assert "st.session_state.multi_demo_running) and snapshot.status" not in text


def test_simple_dashboard_keeps_advanced_markers_for_smoke_checks() -> None:
    text = (ROOT / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py").read_text(encoding="utf-8")

    assert "Advanced tools blijven beschikbaar" in text
    assert "Advanced tools: Overview, Demo Spot Trading, Demo Pilot." in text
    assert "LIVE TRADING DISABLED" in text
