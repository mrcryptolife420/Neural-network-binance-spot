from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import replace
from decimal import Decimal

import streamlit as st

from binance_spot_bot.config import BotSettings
from binance_spot_bot.connectivity import connectivity_report
from binance_spot_bot.credentials import CredentialManager, WindowsSecretStoreAdapter
from binance_spot_bot.evaluation import evaluate_rule_baseline, report_to_dict
from binance_spot_bot.exchange_profiles import available_profiles, selectable_profile_names
from binance_spot_bot.settings_store import DashboardSettingsStore, RISK_PRESETS
from binance_spot_bot.ui.charts import candlestick_figure, equity_figure
from binance_spot_bot.ui.state import SELECTABLE_DATA_SOURCES, SELECTABLE_MODES, create_runtime


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--mode", choices=SELECTABLE_MODES, default="demo")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--interval", default="1m")
    parser.add_argument("--scenario", default="sideways")
    parser.add_argument("--source", choices=SELECTABLE_DATA_SOURCES, default="auto")
    args, _ = parser.parse_known_args(sys.argv[1:])
    return args


def main() -> None:
    args = parse_args()
    st.set_page_config(page_title="Spot Bot Control Center", layout="wide")
    st.title("Neural Network Binance Spot Bot")
    st.caption("LIVE TRADING DISABLED")

    base_settings = BotSettings.from_env()
    store = DashboardSettingsStore(base_settings.data_dir / "settings")
    if "dashboard_settings" not in st.session_state:
        st.session_state.dashboard_settings = store.load()
    if "credential_manager" not in st.session_state:
        st.session_state.credential_manager = CredentialManager()
    if "connectivity_report" not in st.session_state:
        st.session_state.connectivity_report = {}
    if "evaluation_report" not in st.session_state:
        st.session_state.evaluation_report = {}

    saved = st.session_state.dashboard_settings
    profiles = available_profiles()

    with st.sidebar:
        st.header("Control")
        selected_profile = st.selectbox(
            "Exchange profile",
            selectable_profile_names(),
            index=selectable_profile_names().index(saved.selected_profile)
            if saved.selected_profile in selectable_profile_names()
            else 0,
            format_func=lambda value: profiles[value].label,
        )
        mode = st.selectbox("Runtime mode", SELECTABLE_MODES, index=SELECTABLE_MODES.index(args.mode))
        source = st.selectbox(
            "Market data source",
            SELECTABLE_DATA_SOURCES,
            index=SELECTABLE_DATA_SOURCES.index(saved.source if saved.source in SELECTABLE_DATA_SOURCES else args.source),
        )
        symbol = st.text_input("Symbol", value=saved.symbol or args.symbol).upper()
        intervals = ["1m", "5m", "15m", "1h"]
        interval = st.selectbox(
            "Interval",
            intervals,
            index=intervals.index(saved.interval if saved.interval in intervals else args.interval),
        )
        scenario = st.selectbox("Demo scenario", ["sideways", "uptrend", "downtrend", "volatile"], index=0)
        model_alias = st.text_input("Model alias", value=saved.model_alias)
        speed = st.selectbox("Replay speed", [1, 5, 10], index=0)
        st.header("Run")
        reset_runtime = st.button("Reset runtime", use_container_width=True)
        start = st.button("Start / run", use_container_width=True)
        pause = st.button("Pause", use_container_width=True)
        step_once = st.button("Single step", use_container_width=True)
        emergency_stop = st.button("Emergency stop", use_container_width=True)

    profile = profiles[selected_profile]
    st.session_state.credential_manager.set_session_credentials(
        selected_profile,
        st.session_state.credential_manager._api_key,
        st.session_state.credential_manager._api_secret,
    )
    runtime_settings = st.session_state.credential_manager.apply_to_settings(base_settings, selected_profile)

    current_preset = RISK_PRESETS.get(saved.risk_preset, RISK_PRESETS["balanced"])
    tabs = st.tabs(
        [
            "Overview",
            "Credentials & Profile",
            "Bot Controls",
            "Risk Controls",
            "Strategy & Model",
            "Market Data",
            "Orders & Account",
            "Sessions",
            "Evaluation",
            "Logs & Security",
        ]
    )

    with tabs[3]:
        st.subheader("Risk controls")
        with st.form("risk_controls"):
            risk_preset = st.selectbox("Risk preset", list(RISK_PRESETS.keys()), index=list(RISK_PRESETS.keys()).index(saved.risk_preset if saved.risk_preset in RISK_PRESETS else "balanced"))
            preset = RISK_PRESETS[risk_preset]
            max_daily_loss = Decimal(str(st.number_input("Max daily loss quote", value=float(preset["max_daily_loss_quote"]), min_value=0.0)))
            max_position = Decimal(str(st.number_input("Max position quote", value=float(preset["max_position_quote"]), min_value=0.0)))
            max_trades = st.number_input("Max trades per day", value=int(preset["max_trades_per_day"]), min_value=0, step=1)
            min_conf = st.slider("Min signal confidence", 0.0, 1.0, float(preset["min_signal_confidence"]), 0.01)
            max_spread = Decimal(str(st.number_input("Max spread bps", value=float(preset["max_spread_bps"]), min_value=0.0)))
            max_data_age_ms = st.number_input("Max data age ms", value=int(preset["max_data_age_ms"]), min_value=1_000, step=1_000)
            default_quote_size = Decimal(str(st.number_input("Default quote size", value=float(preset["default_quote_size"]), min_value=0.0)))
            apply_risk = st.form_submit_button("Apply risk settings")
        if apply_risk:
            saved.risk_preset = risk_preset
            store.save(saved)
            st.success("Risk settings applied to next runtime reset.")
    if "max_daily_loss" not in locals():
        max_daily_loss = Decimal(str(current_preset["max_daily_loss_quote"]))
        max_position = Decimal(str(current_preset["max_position_quote"]))
        max_trades = int(current_preset["max_trades_per_day"])
        min_conf = float(current_preset["min_signal_confidence"])
        max_spread = Decimal(str(current_preset["max_spread_bps"]))
        max_data_age_ms = int(current_preset["max_data_age_ms"])
        default_quote_size = Decimal(str(current_preset["default_quote_size"]))

    runtime_key = (
        selected_profile,
        mode,
        source,
        symbol,
        interval,
        scenario,
        model_alias,
        str(max_daily_loss),
        str(max_position),
        int(max_trades),
        float(min_conf),
        str(max_spread),
        int(max_data_age_ms),
        str(default_quote_size),
        st.session_state.credential_manager.status().api_key_fingerprint,
    )
    if reset_runtime or st.session_state.get("runtime_key") != runtime_key:
        st.session_state.runtime = create_runtime(
            runtime_settings,
            mode,
            symbol,
            interval,
            scenario,
            7,
            max_daily_loss,
            max_position,
            int(max_trades),
            float(min_conf),
            max_spread,
            source,
            model_alias,
            int(max_data_age_ms),
            default_quote_size,
        )
        st.session_state.runtime_key = runtime_key
        st.session_state.running = False
        saved.selected_profile = selected_profile
        saved.symbol = symbol
        saved.interval = interval
        saved.scenario = scenario
        saved.source = source
        saved.model_alias = model_alias
        store.save(saved)
    if "runtime" not in st.session_state:
        st.session_state.runtime = create_runtime(
            runtime_settings,
            mode,
            symbol,
            interval,
            scenario,
            7,
            max_daily_loss,
            max_position,
            int(max_trades),
            float(min_conf),
            max_spread,
            source,
            model_alias,
            int(max_data_age_ms),
            default_quote_size,
        )
        st.session_state.runtime_key = runtime_key
        st.session_state.running = False
    if start:
        st.session_state.running = True
    if pause:
        st.session_state.running = False
    if emergency_stop:
        st.session_state.running = False
        st.session_state.runtime.stop()
    if step_once:
        st.session_state.runtime.step()
    if st.session_state.running:
        st.session_state.runtime.run_steps(int(speed))
    snapshot = st.session_state.runtime.snapshot()

    with tabs[0]:
        _render_overview(snapshot, profile, runtime_settings)
    with tabs[1]:
        _render_credentials(st.session_state.credential_manager, runtime_settings, selected_profile, symbol)
    with tabs[2]:
        _render_bot_controls(snapshot, st.session_state.running, runtime_key)
    with tabs[4]:
        _render_strategy(snapshot, runtime_settings)
    with tabs[5]:
        _render_market(snapshot)
    with tabs[6]:
        _render_orders(snapshot)
    with tabs[7]:
        _render_sessions(snapshot)
    with tabs[8]:
        _render_evaluation(snapshot, runtime_settings, symbol, interval)
    with tabs[9]:
        _render_logs_security(snapshot, runtime_settings)

    if st.session_state.running and snapshot.status not in {"completed", "stopped"}:
        time.sleep(0.7)
        st.rerun()


def _render_overview(snapshot, profile, settings: BotSettings) -> None:
    st.subheader("Operational overview")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Profile", profile.mode_badge)
    c2.metric("Runtime", snapshot.mode)
    c3.metric("Status", snapshot.status)
    c4.metric("Equity", f"{snapshot.equity}")
    c5.metric("Position", f"{snapshot.paper_position}")
    c6.metric("Live", "disabled")
    st.info(f"{snapshot.message} | Base URL: {settings.active_base_url} | Live trading is not selectable.")
    chart_col, side_col = st.columns([3, 1])
    with chart_col:
        st.plotly_chart(candlestick_figure(snapshot.candles, snapshot.signals, snapshot.fills), use_container_width=True)
        st.plotly_chart(equity_figure(snapshot.equity_points), use_container_width=True)
    with side_col:
        st.subheader("Health")
        st.json(snapshot.metrics.health())
        st.subheader("Credential status")
        st.json(snapshot.credential_status)


def _render_credentials(manager: CredentialManager, settings: BotSettings, selected_profile: str, symbol: str) -> None:
    st.subheader("Credentials & Profile")
    profile = available_profiles()[selected_profile]
    st.metric("Mode badge", profile.mode_badge)
    st.write(f"REST base URL: `{settings.active_base_url}`")
    st.write(f"WebSocket base URL: `{profile.websocket_base_url}`")
    with st.form("credential_form"):
        api_key = st.text_input("API key", value="", type="password")
        api_secret = st.text_input("API secret", value="", type="password")
        use_session = st.form_submit_button("Use for this session")
    if use_session:
        manager.set_session_credentials(selected_profile, api_key, api_secret)
        st.success("Credentials loaded for this Streamlit session only.")
        st.rerun()
    cols = st.columns(4)
    if cols[0].button("Test connection"):
        checked = manager.apply_to_settings(settings, selected_profile)
        st.session_state.connectivity_report = connectivity_report(checked, symbol)
    if cols[1].button("Clear session credentials"):
        manager.clear()
        st.rerun()
    secret_store = WindowsSecretStoreAdapter()
    if cols[2].button("Save to Windows SecretStore"):
        if secret_store.is_available():
            st.warning("SecretStore is available, but write support is intentionally gated for a later confirmation flow.")
        else:
            st.warning(secret_store.docs_hint())
    st.json(manager.status().to_dict())
    if st.session_state.connectivity_report:
        st.subheader("Connectivity report")
        st.json(st.session_state.connectivity_report)


def _render_bot_controls(snapshot, running: bool, runtime_key: tuple) -> None:
    st.subheader("Bot Controls")
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Running", "yes" if running else "no")
    b2.metric("Session", snapshot.session_id[-8:] if snapshot.session_id else "-")
    b3.metric("Fills", len(snapshot.fills))
    b4.metric("Blocks", sum(snapshot.metrics.block_reasons.values()))
    st.caption("Start, pause, step and emergency stop are in the sidebar.")
    st.json({"active_runtime_key": [str(item) for item in runtime_key]})


def _render_strategy(snapshot, settings: BotSettings) -> None:
    st.subheader("Strategy & Model")
    st.json(snapshot.active_model)
    st.subheader("Optional AI summary")
    if os.getenv("OPENAI_API_KEY"):
        st.info("AI summaries can be added with Structured Outputs. This panel is read-only and cannot generate orders.")
    else:
        st.warning("AI summaries disabled because OPENAI_API_KEY is not configured.")


def _render_market(snapshot) -> None:
    st.subheader("Market Data")
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Bid", snapshot.top_of_book.get("bid", "-"))
    b2.metric("Ask", snapshot.top_of_book.get("ask", "-"))
    b3.metric("Mid", snapshot.top_of_book.get("mid_price", "-"))
    b4.metric("Spread bps", snapshot.top_of_book.get("spread_bps", "-"))
    st.json(snapshot.market_data)
    st.subheader("Data quality")
    st.json(snapshot.data_quality)


def _render_orders(snapshot) -> None:
    st.subheader("Orders & Account")
    st.json({"user_data_stream": snapshot.user_data_stream, "order_lifecycle": snapshot.order_lifecycle})
    st.subheader("Testnet readiness")
    st.json(snapshot.testnet_prechecks)


def _render_sessions(snapshot) -> None:
    st.subheader("Sessions")
    st.write(f"Current session: `{snapshot.session_id}`")
    st.json(snapshot.recent_sessions)
    st.download_button(
        "Export current session summary",
        data=json.dumps(snapshot.session_summary, default=str, indent=2),
        file_name=f"{snapshot.session_id}-summary.json",
        mime="application/json",
    )


def _render_evaluation(snapshot, settings: BotSettings, symbol: str, interval: str) -> None:
    st.subheader("Evaluation")
    if st.button("Run local evaluation"):
        if len(snapshot.candles) > 20:
            report = evaluate_rule_baseline(symbol, interval, snapshot.candles)
            st.session_state.evaluation_report = report_to_dict(report)
        else:
            st.warning("Run the bot for more candles before evaluation.")
    if st.session_state.evaluation_report:
        st.json(st.session_state.evaluation_report)
    else:
        st.caption("Run after enough candles are available.")


def _render_logs_security(snapshot, settings: BotSettings) -> None:
    st.subheader("Logs & Security")
    st.json(
        {
            "live_trading_enabled": settings.live_trading_enabled,
            "kill_switch": settings.kill_switch,
            "audit_tail": snapshot.audit_tail[-8:],
            "block_reasons": snapshot.metrics.block_reasons,
            "secret_policy": "session-only by default; no plaintext secrets are written to repo, logs, audit or sessions",
        }
    )


if __name__ == "__main__":
    main()
