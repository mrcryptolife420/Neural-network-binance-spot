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
from binance_spot_bot.chaos import simulate_failure
from binance_spot_bot.copilot_permissions import check_copilot_action
from binance_spot_bot.cache_manager import cache_manifest
from binance_spot_bot.dashboard_state import DashboardProcessStatus, DashboardRuntimeState, bot_status_from_runtime
from binance_spot_bot.diagnostics import collect_diagnostics
from binance_spot_bot.evidence import EvidenceVault
from binance_spot_bot.evaluation import evaluate_rule_baseline, report_to_dict
from binance_spot_bot.experiment_db import ExperimentDB
from binance_spot_bot.exchange_profiles import available_profiles, selectable_profile_names
from binance_spot_bot.html_reports import export_html_report
from binance_spot_bot.manual_demo_trading import ManualDemoTradeRequest, execute_manual_demo_trade
from binance_spot_bot.notebook_export import export_notebook
from binance_spot_bot.portfolio import Portfolio, Position
from binance_spot_bot.preflight import run_preflight
from binance_spot_bot.readiness import score_readiness
from binance_spot_bot.replay_sandbox import ReplaySandbox
from binance_spot_bot.risk_debugger import explain_decision, timeline_from_events
from binance_spot_bot.scanner_history import ScannerHistory, ScannerRow, rank_watchlist
from binance_spot_bot.session_compare import compare_sessions
from binance_spot_bot.signal_explainer import explain_signal
from binance_spot_bot.settings_store import DashboardSettingsStore, RISK_PRESETS
from binance_spot_bot.session_store import SessionStore
from binance_spot_bot.spot_preview import SpotPreview, load_spot_symbol_preview
from binance_spot_bot.strategy_templates import list_strategy_templates
from binance_spot_bot.testnet_endurance import TestnetEnduranceGuard
from binance_spot_bot.types import FeatureRow, OrderSide
from binance_spot_bot.ui.charts import candlestick_figure, equity_figure
from binance_spot_bot.ui.components import render_alert_list, render_badges, render_debug, render_table
from binance_spot_bot.ui.demo_trading import demo_trading_badge
from binance_spot_bot.ui.state import SELECTABLE_DATA_SOURCES, SELECTABLE_MODES, create_runtime
from binance_spot_bot.ui.wizard import wizard_options
from binance_spot_bot.workspaces import WorkspaceProfile, WorkspaceStore


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
    if "manual_demo_fills" not in st.session_state:
        st.session_state.manual_demo_fills = []

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
            "Demo Spot Trading",
            "Credentials & Profile",
            "Bot Controls",
            "Risk Controls",
            "Strategy & Model",
            "Market Data",
            "Orders & Account",
            "Sessions",
            "Evaluation",
            "Strategy Lab",
            "Research",
            "Portfolio",
            "Readiness",
            "Logs & Security",
        ]
    )

    with tabs[4]:
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
    _render_status_header(snapshot, profile, runtime_settings, saved)

    with tabs[0]:
        _render_overview(snapshot, profile, runtime_settings)
    with tabs[1]:
        _render_demo_spot_trading(runtime_settings, snapshot, symbol, interval)
    with tabs[2]:
        _render_credentials(st.session_state.credential_manager, runtime_settings, selected_profile, symbol)
    with tabs[3]:
        _render_bot_controls(snapshot, st.session_state.running, runtime_key)
    with tabs[5]:
        _render_strategy(snapshot, runtime_settings)
    with tabs[6]:
        _render_market(snapshot)
    with tabs[7]:
        _render_orders(snapshot)
    with tabs[8]:
        _render_sessions(snapshot)
    with tabs[9]:
        _render_evaluation(snapshot, runtime_settings, symbol, interval)
    with tabs[10]:
        _render_strategy_lab(snapshot)
    with tabs[11]:
        _render_research(snapshot, runtime_settings)
    with tabs[12]:
        _render_portfolio(snapshot)
    with tabs[13]:
        _render_readiness(snapshot)
    with tabs[14]:
        _render_logs_security(snapshot, runtime_settings)

    if st.session_state.running and snapshot.status not in {"completed", "stopped"}:
        time.sleep(0.7)
        st.rerun()


def _render_status_header(snapshot, profile, settings: BotSettings, saved) -> None:
    render_badges(
        {
            "Live": "disabled" if not settings.live_trading_enabled else "blocked",
            "Mode": snapshot.mode,
            "Workspace": "default",
            "Profile": profile.mode_badge,
            "Kill switch": "on" if settings.kill_switch else "paper override",
            "Session": snapshot.status,
            "Readiness": snapshot.readiness.get("level", "R0"),
        }
    )
    if snapshot.readiness.get("blockers"):
        st.warning("Readiness blockers: " + ", ".join(snapshot.readiness["blockers"]))


def _render_overview(snapshot, profile, settings: BotSettings) -> None:
    st.subheader("Operational overview")
    state = DashboardRuntimeState(
        DashboardProcessStatus.RUNNING,
        bot_status_from_runtime(snapshot.status),
        snapshot.mode,
        snapshot.market_data.get("source", "unknown"),
        profile.name,
        live_disabled=not settings.live_trading_enabled,
    )
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
        render_debug("Health details", snapshot.metrics.health())
        render_debug("Credential status", snapshot.credential_status)
        st.subheader("Start wizard")
        render_debug("Wizard options", {"state": state.to_dict(), "options": wizard_options()})
        st.subheader("Workspace")
        workspace_store = WorkspaceStore(settings.data_dir / "workspaces")
        if st.button("Save current workspace"):
            workspace_store.save(WorkspaceProfile("default", str(settings.data_dir), profile.name, [snapshot.symbol], language="nl"))
        render_table("Saved workspaces", [workspace.to_dict() for workspace in workspace_store.list()])


def _render_demo_spot_trading(settings: BotSettings, snapshot, symbol: str, interval: str) -> None:
    st.subheader("Demo Spot Trading")
    st.caption(f"{demo_trading_badge()} - Manual demo fills are local paper events only; no signed Binance order endpoint is called.")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Mode", snapshot.mode)
    col_b.metric("Live", "disabled")
    col_c.metric("Manual fills", len(st.session_state.manual_demo_fills))
    if st.button("Refresh public Spot preview"):
        st.session_state.spot_preview = load_spot_symbol_preview(settings, symbol, interval, limit=60)
    preview: SpotPreview | None = st.session_state.get("spot_preview")
    if preview is None:
        st.info("Refresh the Spot preview before placing a local demo fill.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Source", preview.source)
        c2.metric("Last", f"{preview.last_price}")
        c3.metric("Spread bps", f"{preview.spread_bps}" if preview.spread_bps is not None else "-")
        c4.metric("Filter", preview.filters.status)
        render_debug(
            "Preview details",
            {
                "symbol": preview.symbol,
                "message": preview.message,
                "filters": {
                    "tick_size": str(preview.filters.tick_size),
                    "step_size": str(preview.filters.step_size),
                    "min_qty": str(preview.filters.min_qty),
                    "min_notional": str(preview.filters.min_notional),
                },
            }
        )
        with st.form("manual_demo_trade_form"):
            side = st.selectbox("Side", [OrderSide.BUY.value, OrderSide.SELL.value])
            quote_size = Decimal(str(st.number_input("Quote size", value=25.0, min_value=0.0, step=5.0)))
            quote_balance = Decimal(str(st.number_input("Paper quote balance", value=1000.0, min_value=0.0, step=50.0)))
            base_balance = Decimal(str(st.number_input("Paper base balance", value=0.0, min_value=0.0, step=0.001, format="%.6f")))
            confirmed = st.checkbox("I understand this is a local paper demo fill")
            submitted = st.form_submit_button("Create local demo fill")
        if submitted:
            request = ManualDemoTradeRequest(
                symbol=preview.symbol,
                side=OrderSide(side),
                quote_size=quote_size,
                price=preview.last_price,
                quote_balance=quote_balance,
                base_balance=base_balance,
                confirmed_demo_only=confirmed,
            )
            result = execute_manual_demo_trade(request, preview.filters)
            if result.fill:
                st.session_state.manual_demo_fills.append(result.fill)
                if snapshot.session_id:
                    SessionStore(settings.data_dir / "sessions").record_fill(snapshot.session_id, result.fill)
            render_debug("Trade result", {"status": result.status, "preview": result.preview.to_dict(), "fill": result.fill})
    if st.session_state.manual_demo_fills:
        render_table("Local demo fill history", st.session_state.manual_demo_fills[-10:])


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
    render_debug("Credential status", manager.status().to_dict())
    if st.session_state.connectivity_report:
        st.subheader("Connectivity report")
        render_debug("Connectivity report", st.session_state.connectivity_report)


def _render_bot_controls(snapshot, running: bool, runtime_key: tuple) -> None:
    st.subheader("Bot Controls")
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Running", "yes" if running else "no")
    b2.metric("Session", snapshot.session_id[-8:] if snapshot.session_id else "-")
    b3.metric("Fills", len(snapshot.fills))
    b4.metric("Blocks", sum(snapshot.metrics.block_reasons.values()))
    st.caption("Start, pause, step and emergency stop are in the sidebar.")
    render_debug("Active runtime key", {"active_runtime_key": [str(item) for item in runtime_key]})


def _render_strategy(snapshot, settings: BotSettings) -> None:
    st.subheader("Strategy & Model")
    render_debug("Active model", snapshot.active_model)
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
    render_debug("Market data details", snapshot.market_data)
    st.subheader("Data quality")
    render_debug("Data quality details", snapshot.data_quality)


def _render_orders(snapshot) -> None:
    st.subheader("Orders & Account")
    render_debug("User data stream", snapshot.user_data_stream)
    render_table("Order lifecycle", snapshot.order_lifecycle)
    st.subheader("Testnet readiness")
    render_debug("Testnet readiness", snapshot.testnet_prechecks)


def _render_sessions(snapshot) -> None:
    st.subheader("Sessions")
    st.write(f"Current session: `{snapshot.session_id}`")
    render_table("Recent sessions", snapshot.recent_sessions)
    store = SessionStore(BotSettings.from_env().data_dir / "sessions")
    session_ids = [item.get("session_id", "") for item in snapshot.recent_sessions if item.get("session_id")]
    if session_ids:
        selected = st.selectbox("Replay session", session_ids)
        frames = ReplaySandbox(store).chart_points(selected)
        render_table("Replay timeline", frames[:100])
        compare_ids = st.multiselect("Compare sessions", session_ids, default=session_ids[:2] if len(session_ids) >= 2 else [])
        if len(compare_ids) >= 2:
            render_table("Session comparison", [row.to_dict() for row in compare_sessions(store, compare_ids[:10])])
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


def _render_strategy_lab(snapshot) -> None:
    st.subheader("Strategy Lab")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("Risk decision debugger")
        if snapshot.latest_risk_decision:
            render_table("Latest risk decision", [explain_decision(snapshot.latest_risk_decision).to_dict()])
        else:
            st.caption("No risk decision yet.")
        render_table("Risk timeline", [event.to_dict() for event in timeline_from_events(snapshot.audit_tail)])
    with col_b:
        st.write("Signal explanation")
        if snapshot.latest_signal and snapshot.current_candle:
            row = FeatureRow(
                snapshot.symbol,
                snapshot.current_candle.close_time_ms,
                {"close": float(snapshot.current_candle.close), "confidence": float(snapshot.latest_signal.confidence)},
                snapshot.current_candle.close,
            )
            explanation = explain_signal(snapshot.latest_signal, row).to_dict()
            render_badges(
                {
                    "Signal": explanation["signal"],
                    "Confidence": round(explanation["confidence"], 4),
                    "Horizon": explanation["horizon"],
                    "Model": explanation["model_version"],
                }
            )
            render_table("Top features", [{"feature": key, "value": value} for key, value in explanation["top_features"]])
        else:
            st.caption("Run or step the bot to inspect a signal.")
        st.write("Strategy templates")
        render_table("Templates", list_strategy_templates())


def _render_research(snapshot, settings: BotSettings) -> None:
    st.subheader("Research")
    spread = float(snapshot.top_of_book.get("spread_bps") or 0)
    confidence = float(snapshot.latest_signal.confidence) if snapshot.latest_signal else 0.0
    signal = snapshot.latest_signal.signal.value if snapshot.latest_signal else "HOLD"
    scanner_rows = rank_watchlist([ScannerRow(snapshot.symbol, spread, 0.0, signal, confidence)])
    render_table("Scanner ranking", [row.to_dict() for row in scanner_rows])
    experiments = ExperimentDB(settings.data_dir / "experiments" / "experiments.json")
    history = ScannerHistory(settings.data_dir / "scanner" / "history.jsonl", experiments)
    if st.button("Record scanner run"):
        st.session_state.scanner_run = history.record_run(scanner_rows)
    if st.button("Export scanner reports"):
        payload = {"rows": [row.to_dict() for row in scanner_rows], "orders_allowed": False}
        html_path = export_html_report("Scanner Research", payload, settings.data_dir / "reports" / "scanner.html")
        notebook_path = export_notebook("Scanner Research", payload, settings.data_dir / "reports" / "scanner.ipynb")
        st.session_state.scanner_exports = {"html": str(html_path), "notebook": str(notebook_path)}
    render_table("Scanner history", history.list_runs()[-10:])
    if st.session_state.get("scanner_exports"):
        render_debug("Scanner exports", st.session_state.scanner_exports)
    manifest = cache_manifest(settings.data_dir)
    render_badges({"Cache entries": len(manifest["entries"]), "Manifest time": manifest["created_at_ms"]})


def _render_portfolio(snapshot) -> None:
    st.subheader("Portfolio")
    portfolio = Portfolio()
    portfolio.set_balance("USDT", Decimal(str(snapshot.paper_quote)))
    mark = Decimal(str(snapshot.current_candle.close)) if snapshot.current_candle else Decimal("0")
    if snapshot.paper_position > 0:
        portfolio.positions[snapshot.symbol] = portfolio.positions.get(snapshot.symbol) or Position(snapshot.symbol, snapshot.paper_position, mark)
    render_badges(
        {
            "Quote": portfolio.to_dict()["balances"].get("USDT", "0"),
            "Total equity": str(portfolio.total_equity({snapshot.symbol: mark})),
            "Exposure": str(portfolio.total_exposure({snapshot.symbol: mark})),
            "Fees": snapshot.paper_account.get("fees_paid", "0"),
        }
    )
    render_table("Positions", list(portfolio.to_dict()["positions"].values()))


def _render_readiness(snapshot) -> None:
    st.subheader("Readiness")
    evidence = {"check-all", "secret-scan"}
    if snapshot.session_id:
        evidence.add("paper-report")
    score = score_readiness(evidence)
    render_badges({"Readiness": score.level, "Live allowed": str(score.live_allowed), "Blockers": len(score.blockers)})
    render_table("Readiness blockers", [{"blocker": item} for item in score.blockers])
    st.write("Copilot guard")
    render_table("Copilot permissions", [check_copilot_action(action).to_dict() for action in ["summarize_session", "place_order", "enable_live", "read_api_secret"]])
    st.write("Chaos scenarios")
    render_table("Chaos scenarios", [simulate_failure(key).to_dict() for key in ["429", "418", "5xx", "websocket_disconnect", "stale_data", "write_failure", "unknown_order"]])
    guard = TestnetEnduranceGuard(max_orders=5)
    render_debug("Testnet endurance guard", guard.to_dict())
    profiles = available_profiles()
    render_table(
        "Profile readiness",
        [
            {
                "profile": item.name,
                "mode": item.trading_mode.value,
                "requires_credentials": item.requires_credentials,
                "live_disabled": True,
                "base_url": item.rest_base_url,
            }
            for item in profiles.values()
        ],
    )
    if st.button("Record readiness evidence"):
        vault = EvidenceVault(BotSettings.from_env().data_dir / "evidence" / "evidence.jsonl")
        evidence_record = vault.add("readiness-score", score.to_dict())
        st.session_state.readiness_evidence = evidence_record.to_dict()
    if st.session_state.get("readiness_evidence"):
        render_debug("Readiness evidence", st.session_state.readiness_evidence)
    st.info("Live-readiness remains design-only; live trading is not enabled from this dashboard.")


def _render_logs_security(snapshot, settings: BotSettings) -> None:
    st.subheader("Logs & Security")
    if st.button("Run preflight checks"):
        st.session_state.preflight_report = run_preflight(settings).to_dict()
    if st.session_state.get("preflight_report"):
        st.subheader("Preflight")
        render_debug("Preflight details", st.session_state.preflight_report)
    if st.button("Collect diagnostics"):
        st.session_state.diagnostics_report = collect_diagnostics(settings).to_dict()
    if st.session_state.get("diagnostics_report"):
        st.subheader("Diagnostics")
        render_debug("Diagnostics details", st.session_state.diagnostics_report)
    render_alert_list(snapshot.alerts[-20:])
    render_debug(
        "Security details",
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
