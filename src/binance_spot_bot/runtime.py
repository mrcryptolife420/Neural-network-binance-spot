from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, replace
from decimal import Decimal
from typing import Any

from .alerts import AlertManager, AlertSeverity, WatchdogAction
from .audit import AuditLog
from .config import BotSettings
from .data import DataStore
from .data_quality import DataQualityReport, check_candles
from .execution import ExecutionEngine
from .exchange_profiles import profile_for
from .features import build_feature_rows
from .market_data_source import (
    DemoMarketReplaySource,
    MarketDataSource,
    RestPollingMarketDataSource,
    StaticMarketDataSource,
    WebSocketMarketDataSource,
)
from .model_registry import ModelMetadata, ModelRegistry
from .monitoring import RuntimeMetrics
from .orderbook import TopOfBook
from .order_lifecycle import OrderLifecycleStore
from .paper import PaperTrader
from .paper_accounting import PaperAccount
from .risk import RiskEngine, RiskLimits
from .session_report import export_session_report
from .session_store import SessionStore, SessionSummary
from .signal_model import RuleBasedSignalModel, TinyNeuralSignalModel
from .types import (
    AccountState,
    Candle,
    ExecutionResult,
    FeatureRow,
    MarketState,
    RiskDecision,
    Signal,
    SymbolFilters,
    TradingMode,
)
from .user_data_stream import UserDataStreamAdapter


UI_MODES = ("demo", "paper", "testnet-readiness")
DATA_SOURCES = ("auto", "demo", "rest", "websocket")


@dataclass(frozen=True)
class RuntimeOptions:
    mode: str = "demo"
    symbol: str = "BTCUSDT"
    interval: str = "1m"
    scenario: str = "sideways"
    seed: int = 7
    window: int = 5
    source: str = "auto"
    model_alias: str = ""
    starting_quote: Decimal = Decimal("1000")
    max_daily_loss_quote: Decimal = Decimal("50")
    max_position_quote: Decimal = Decimal("25")
    max_trades_per_day: int = 25
    min_signal_confidence: float = 0.15
    max_spread_bps: Decimal = Decimal("30")
    max_data_age_ms: int = 120_000
    default_quote_size: Decimal = Decimal("10")
    fetch_limit: int = 120


@dataclass
class RuntimeSnapshot:
    mode: str
    symbol: str
    interval: str
    status: str
    message: str
    current_candle: Candle | None
    latest_signal: Signal | None
    latest_risk_decision: RiskDecision | None
    latest_execution_result: ExecutionResult | None
    equity: Decimal
    paper_quote: Decimal
    paper_position: Decimal
    metrics: RuntimeMetrics
    audit_tail: list[dict[str, Any]]
    candles: list[Candle] = field(default_factory=list)
    signals: list[dict[str, Any]] = field(default_factory=list)
    fills: list[dict[str, Any]] = field(default_factory=list)
    equity_points: list[dict[str, Any]] = field(default_factory=list)
    testnet_prechecks: dict[str, bool] = field(default_factory=dict)
    market_data: dict[str, Any] = field(default_factory=dict)
    top_of_book: dict[str, Any] = field(default_factory=dict)
    data_quality: dict[str, Any] = field(default_factory=dict)
    session_id: str = ""
    session_summary: dict[str, Any] = field(default_factory=dict)
    recent_sessions: list[dict[str, Any]] = field(default_factory=list)
    active_model: dict[str, Any] = field(default_factory=dict)
    exchange_profile: dict[str, Any] = field(default_factory=dict)
    credential_status: dict[str, Any] = field(default_factory=dict)
    user_data_stream: dict[str, Any] = field(default_factory=dict)
    order_lifecycle: list[dict[str, Any]] = field(default_factory=list)
    alerts: list[dict[str, Any]] = field(default_factory=list)
    paper_account: dict[str, Any] = field(default_factory=dict)
    report_paths: dict[str, str] = field(default_factory=dict)
    readiness: dict[str, Any] = field(default_factory=dict)


class BotRuntime:
    def __init__(
        self,
        settings: BotSettings,
        options: RuntimeOptions,
        candles: list[Candle] | None = None,
    ):
        if options.mode not in UI_MODES:
            raise ValueError(f"unsupported runtime mode: {options.mode}")
        if options.source not in DATA_SOURCES:
            raise ValueError(f"unsupported data source: {options.source}")
        self.settings = settings
        self.options = options
        self.datastore = DataStore(settings.data_dir)
        self.audit = AuditLog(settings.audit_log_path)
        self.metrics = RuntimeMetrics()
        self.session_store = SessionStore(settings.data_dir / "sessions")
        self.model_registry = ModelRegistry(self.datastore.models_dir)
        self.status = "created"
        self.message = "ready"
        self.paper_account = PaperAccount(
            options.starting_quote,
            fee_bps=Decimal("10"),
            slippage_bps=self._limits().max_slippage_bps,
        )
        self.latest_signal: Signal | None = None
        self.latest_risk_decision: RiskDecision | None = None
        self.latest_execution_result: ExecutionResult | None = None
        self.signal_points: list[dict[str, Any]] = []
        self.fill_points: list[dict[str, Any]] = []
        self.equity_points: list[dict[str, Any]] = []
        self.candles: list[Candle] = []
        self.top_of_book: TopOfBook | None = None
        self.latest_data_quality = check_candles([])
        self.filters = self._default_filters(options.symbol)
        self.model, self.model_metadata = self._load_model()
        self.data_source = self._create_data_source(candles)
        self.user_data_stream = UserDataStreamAdapter(settings.exchange_profile)
        self.order_lifecycle = OrderLifecycleStore()
        self.alerts = AlertManager()
        self.report_paths: dict[str, str] = {}
        self.paper_settings = replace(
            settings,
            trading_mode=TradingMode.PAPER,
            live_trading_enabled=False,
            kill_switch=False,
        )
        self.risk = RiskEngine(self._limits(), kill_switch=False)
        self.execution = ExecutionEngine(self.paper_settings, self.audit)
        self.paper = PaperTrader(self.model, self.risk, self.execution, self.audit)
        self.session = self.session_store.start_session(
            mode=options.mode,
            symbol=options.symbol,
            interval=options.interval,
            model_version=self._model_version(),
            metadata={"source": self._resolved_source(), "model_alias": options.model_alias},
        )
        self.session_finished = False
        self._emit_alert("runtime_created", AlertSeverity.INFO, "runtime created", WatchdogAction.OBSERVE)

    def start(self) -> None:
        self.status = "running"
        self.message = "runtime started"
        self.audit.emit(
            "runtime",
            "started",
            {"mode": self.options.mode, "symbol": self.options.symbol, "source": self._resolved_source()},
        )
        self._emit_alert("runtime_started", AlertSeverity.INFO, "runtime started", WatchdogAction.OBSERVE)

    def stop(self) -> None:
        self.status = "stopped"
        self.message = "runtime stopped"
        self.data_source.close()
        self._finish_session("stopped")
        self.audit.emit("runtime", "stopped", {"session_id": self.session.session_id})

    def step(self) -> RuntimeSnapshot:
        if self.status == "created":
            self.start()
        if self.options.mode == "testnet-readiness":
            self.status = "ready"
            self.message = "testnet readiness only; no orders are sent"
            return self.snapshot()
        candle = self.data_source.next_event()
        data_snapshot = self.data_source.snapshot()
        self.metrics.stream_status = data_snapshot.status
        self.top_of_book = data_snapshot.top_of_book
        if candle is None:
            self.status = "completed"
            self.message = "replay completed" if data_snapshot.status != "degraded" else data_snapshot.message
            if data_snapshot.status == "degraded":
                self._emit_alert("connectivity_fallback", AlertSeverity.WARNING, data_snapshot.message or "market data degraded")
            self._finish_session("completed")
            return self.snapshot()
        self.candles = data_snapshot.candles or [*self.candles, candle]
        self._update_data_quality(candle)
        if len(self.candles) <= self.options.window:
            self.message = "waiting_for_data"
            self._record_equity(candle)
            self._record_session_snapshot(candle)
            return self.snapshot()
        feature = build_feature_rows(self.options.symbol, self.candles, self.options.window)[-1]
        market = self._market_from_feature(feature, candle, self.top_of_book)
        account = AccountState(
            quote_balance=self.paper_account.quote_balance,
            base_balance=self.paper_account.base_balance,
            equity_quote=self._equity(candle),
            daily_realized_pnl=self.paper_account.realized_pnl,
        )
        result = self.paper.step(feature, account, market, self.filters)
        self.latest_signal = self.paper.last_signal
        self.latest_risk_decision = self.paper.last_decision
        self.latest_execution_result = result
        if self.latest_signal is not None:
            self.metrics.record_signal(self.latest_signal.signal.value)
        if self.latest_risk_decision is not None and self.latest_risk_decision.decision.value == "BLOCK":
            self.metrics.record_block(self.latest_risk_decision.reason)
            self._emit_alert("risk_block", AlertSeverity.WARNING, self.latest_risk_decision.reason, WatchdogAction.OBSERVE)
        self._apply_paper_fill(result, candle)
        self._record_order_event(result, candle)
        self.signal_points.append(
            {
                "timestamp_ms": candle.close_time_ms,
                "price": str(candle.close),
                "side": self.latest_signal.signal.value if self.latest_signal else "HOLD",
                "confidence": self.latest_signal.confidence if self.latest_signal else 0,
                "model_version": self._model_version(),
            }
        )
        self._record_equity(candle)
        self._record_session_snapshot(candle)
        self.message = "tick processed"
        if self.alerts.should_stop_runtime():
            self.status = "stopped"
            self.message = "runtime stopped by critical alert"
            self._finish_session("stopped")
        return self.snapshot()

    def run_steps(self, count: int) -> RuntimeSnapshot:
        for _ in range(count):
            snap = self.step()
            if snap.status == "completed":
                break
        return self.snapshot()

    def snapshot(self) -> RuntimeSnapshot:
        current = self.candles[-1] if self.candles else None
        data_snapshot = self.data_source.snapshot()
        self.metrics.stream_status = data_snapshot.status
        return RuntimeSnapshot(
            mode=self.options.mode,
            symbol=self.options.symbol,
            interval=self.options.interval,
            status=self.status,
            message=self.message,
            current_candle=current,
            latest_signal=self.latest_signal,
            latest_risk_decision=self.latest_risk_decision,
            latest_execution_result=self.latest_execution_result,
            equity=self._equity(current) if current else self.paper_account.quote_balance,
            paper_quote=self.paper_account.quote_balance,
            paper_position=self.paper_account.base_balance,
            metrics=self.metrics,
            audit_tail=self.audit_tail(),
            candles=list(self.candles),
            signals=list(self.signal_points),
            fills=list(self.fill_points),
            equity_points=list(self.equity_points),
            testnet_prechecks=self.testnet_prechecks(),
            market_data={
                "source": data_snapshot.source,
                "status": data_snapshot.status,
                "message": data_snapshot.message,
                "last_event_age_ms": data_snapshot.last_event_age_ms,
                "reconnect_count": data_snapshot.reconnect_count,
                "stream_url": data_snapshot.stream_url,
            },
            top_of_book=self.top_of_book.to_dict(current.close_time_ms) if self.top_of_book and current else {"status": "empty"},
            data_quality=self.latest_data_quality.to_dict(),
            session_id=self.session.session_id,
            session_summary=asdict(self.session),
            recent_sessions=[asdict(item) for item in self.session_store.list_sessions(5)],
            active_model=self._active_model_payload(),
            exchange_profile=profile_for(self.settings.exchange_profile).to_dict(),
            credential_status={
                "profile": self.settings.exchange_profile,
                "has_api_key": bool(self.settings.binance_api_key),
                "has_api_secret": bool(self.settings.binance_api_secret),
                "capability": "Credentials loaded for signed checks"
                if self.settings.binance_api_key and self.settings.binance_api_secret
                else "No signed credentials required"
                if not profile_for(self.settings.exchange_profile).requires_credentials
                else "needs credentials",
            },
            user_data_stream=self.user_data_stream.status(),
            order_lifecycle=self.order_lifecycle.list_recent(),
            alerts=[alert.to_dict() for alert in self.alerts.alerts()],
            paper_account=self.paper_account.to_dict(current.close if current else None),
            report_paths=dict(self.report_paths),
            readiness=self._readiness_payload(),
        )

    def audit_tail(self, limit: int = 20) -> list[dict[str, Any]]:
        path = self.settings.audit_log_path
        if not path.exists():
            return []
        lines = path.read_text(encoding="utf-8").splitlines()[-limit:]
        items: list[dict[str, Any]] = []
        for line in lines:
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return items

    def testnet_prechecks(self) -> dict[str, bool]:
        return {
            "api_key_present": bool(self.settings.binance_api_key),
            "api_secret_present": bool(self.settings.binance_api_secret),
            "mode_is_testnet": self.settings.trading_mode == TradingMode.TESTNET,
            "live_disabled": not self.settings.live_trading_enabled,
            "risk_limits_set": self.options.max_position_quote > 0 and self.options.max_trades_per_day > 0,
        }

    def _create_data_source(self, candles: list[Candle] | None) -> MarketDataSource:
        if candles is not None:
            return StaticMarketDataSource(self.options.symbol, candles)
        source = self._resolved_source()
        if source == "rest":
            return RestPollingMarketDataSource(
                self.settings,
                self.options.symbol,
                self.options.interval,
                self.datastore,
                limit=self.options.fetch_limit,
            )
        if source == "websocket":
            return WebSocketMarketDataSource(
                self.settings,
                self.options.symbol,
                self.options.interval,
                self.datastore,
                limit=self.options.fetch_limit,
            )
        return DemoMarketReplaySource(
            symbol=self.options.symbol,
            interval=self.options.interval,
            scenario=self.options.scenario,
            seed=self.options.seed,
            count=max(self.options.fetch_limit, 80),
        )

    def _resolved_source(self) -> str:
        if self.options.source == "auto":
            return "rest" if self.options.mode == "paper" else "demo"
        return self.options.source

    def _load_model(self) -> tuple[RuleBasedSignalModel | TinyNeuralSignalModel, ModelMetadata | None]:
        if self.options.model_alias:
            loaded = self.model_registry.load_by_alias(self.options.model_alias)
            if loaded is not None:
                return loaded
        return RuleBasedSignalModel(), None

    def _limits(self) -> RiskLimits:
        return RiskLimits(
            max_daily_loss_quote=self.options.max_daily_loss_quote,
            max_position_quote=self.options.max_position_quote,
            max_trades_per_day=self.options.max_trades_per_day,
            min_signal_confidence=self.options.min_signal_confidence,
            max_spread_bps=self.options.max_spread_bps,
            max_data_age_ms=self.options.max_data_age_ms,
            default_quote_size=min(self.options.default_quote_size, self.options.max_position_quote),
        )

    def _market_from_feature(
        self,
        feature: FeatureRow,
        candle: Candle,
        top_of_book: TopOfBook | None,
    ) -> MarketState:
        if top_of_book is not None:
            return MarketState(
                symbol=feature.symbol,
                last_price=feature.close,
                bid=top_of_book.bid,
                ask=top_of_book.ask,
                data_timestamp_ms=top_of_book.event_time_ms or candle.close_time_ms,
                now_ms=candle.close_time_ms,
            )
        return MarketState(
            symbol=feature.symbol,
            last_price=feature.close,
            bid=feature.close * Decimal("0.9999"),
            ask=feature.close * Decimal("1.0001"),
            data_timestamp_ms=feature.timestamp_ms,
            now_ms=feature.timestamp_ms,
        )

    def _apply_paper_fill(self, result: ExecutionResult, candle: Candle) -> None:
        if result.status != "FILLED" or result.order_request is None:
            return
        qty = result.order_request.quantity or Decimal("0")
        price = Decimal(str(result.response.get("price", candle.close)))
        try:
            if result.order_request.side.value == "BUY":
                account_fill = self.paper_account.buy(result.order_request.symbol, qty, price)
            else:
                account_fill = self.paper_account.sell(result.order_request.symbol, qty, price)
        except ValueError as exc:
            self._emit_alert("paper_accounting_block", AlertSeverity.ERROR, str(exc), WatchdogAction.BLOCK_TRADING)
            return
        fill = {
            "timestamp_ms": candle.close_time_ms,
            "price": str(account_fill.price),
            "side": result.order_request.side.value,
            "quantity": str(account_fill.quantity),
            "notional": str(account_fill.notional),
            "fee": str(account_fill.fee),
            "realized_pnl": str(account_fill.realized_pnl),
            "model_version": self._model_version(),
        }
        self.fill_points.append(fill)
        self.session_store.record_fill(self.session.session_id, fill)

    def _record_equity(self, candle: Candle) -> None:
        equity = self._equity(candle)
        self.metrics.paper_pnl = equity - self.options.starting_quote
        self.metrics.exposure_quote = self.paper_account.base_balance * candle.close
        self.equity_points.append({"timestamp_ms": candle.close_time_ms, "equity": str(equity)})

    def _record_session_snapshot(self, candle: Candle) -> None:
        self.session_store.record_snapshot(
            self.session.session_id,
            {
                "timestamp_ms": candle.close_time_ms,
                "status": self.status,
                "message": self.message,
                "equity": str(self._equity(candle)),
                "quote": str(self.paper_account.quote_balance),
                "position": str(self.paper_account.base_balance),
                "blocks": dict(self.metrics.block_reasons),
                "alerts": len(self.alerts.alerts()),
                "critical_alerts": len([alert for alert in self.alerts.alerts() if alert.severity == AlertSeverity.CRITICAL]),
                "fees_paid": str(sum((fill.fee for fill in self.paper_account.fills), Decimal("0"))),
                "realized_pnl": str(self.paper_account.realized_pnl),
                "source": self._resolved_source(),
                "model_version": self._model_version(),
            },
        )

    def _update_data_quality(self, candle: Candle) -> None:
        spread = self.top_of_book.spread_bps if self.top_of_book else None
        report = check_candles(
            self.candles,
            now_ms=candle.close_time_ms,
            spread_bps=spread,
            max_spread_bps=self.options.max_spread_bps,
        )
        self.latest_data_quality = report
        warnings = len(report.issues)
        self.metrics.data_quality_warnings = warnings
        if report.status != "ok":
            self.audit.emit(
                "data_quality",
                "warning",
                {"status": report.status, "issues": [issue.code for issue in report.issues]},
            )
            for issue in report.issues:
                severity = AlertSeverity.ERROR if issue.severity == "error" else AlertSeverity.WARNING
                action = WatchdogAction.STOP_RUNTIME if issue.severity == "error" else WatchdogAction.OBSERVE
                name = "stale_data" if issue.code == "stale_data" else "spread_above_limit" if issue.code == "extreme_spread" else issue.code
                self._emit_alert(name, severity, issue.message, action, issue.details)
        if self.paper_account.realized_pnl <= -self.options.max_daily_loss_quote:
            self._emit_alert("max_loss_reached", AlertSeverity.CRITICAL, "paper account reached max loss", WatchdogAction.STOP_RUNTIME)

    def _finish_session(self, status: str) -> None:
        if self.session_finished:
            return
        summary = self.session_store.finish_session(
            self.session.session_id,
            pnl=self.metrics.paper_pnl,
            max_drawdown=self._max_drawdown(),
            trades=len(self.fill_points),
            blocks=sum(self.metrics.block_reasons.values()),
            status=status,
        )
        summary.metadata.update(
            {
                "alerts_count": len(self.alerts.alerts()),
                "critical_alerts_count": len([alert for alert in self.alerts.alerts() if alert.severity == AlertSeverity.CRITICAL]),
                "realized_pnl": str(self.paper_account.realized_pnl),
                "fees_paid": str(sum((fill.fee for fill in self.paper_account.fills), Decimal("0"))),
                "slippage_bps": str(self.paper_account.slippage_bps),
                "readiness_blockers": self._readiness_payload()["blockers"],
            }
        )
        self.session_store._write_summary(summary)
        self.session = summary
        self.session_finished = True
        self.report_paths = export_session_report(self.session_store, self.session.session_id)

    def _max_drawdown(self) -> Decimal:
        peak = Decimal("0")
        max_dd = Decimal("0")
        for point in self.equity_points:
            equity = Decimal(str(point["equity"]))
            peak = max(peak, equity)
            max_dd = max(max_dd, peak - equity)
        return max_dd

    def _equity(self, candle: Candle | None) -> Decimal:
        if candle is None:
            return self.paper_account.quote_balance
        return self.paper_account.equity(candle.close)

    def _emit_alert(
        self,
        name: str,
        severity: AlertSeverity,
        message: str,
        action: WatchdogAction | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        alert = self.alerts.emit(name, severity, message, action, metadata)
        self.audit.emit("alert", name, alert.to_dict())
        if hasattr(self, "session"):
            self.session_store.record_alert(self.session.session_id, alert.to_dict())

    def _record_order_event(self, result: ExecutionResult, candle: Candle) -> None:
        payload = {
            "timestamp_ms": candle.close_time_ms,
            "status": result.status,
            "mode": result.mode.value,
            "order_request": asdict(result.order_request) if result.order_request else None,
            "response": result.response,
        }
        self.session_store.record_order(self.session.session_id, payload)
        if result.status in {"BLOCKED", "DISABLED"}:
            return
        if result.order_request and result.order_request.client_order_id:
            lifecycle = self.order_lifecycle.record_intent(
                result.order_request.client_order_id,
                result.order_request.symbol,
                result.order_request.side.value,
            )
            lifecycle.status = result.status
            lifecycle.events.append({"type": "PAPER", "status": result.status, "response": result.response})

    def _readiness_payload(self) -> dict[str, Any]:
        blockers = []
        if self.alerts.should_stop_runtime():
            blockers.append("critical alerts present")
        if not self.report_paths and self.status in {"completed", "stopped"}:
            blockers.append("session report missing")
        if self.settings.live_trading_enabled:
            blockers.append("live trading enabled")
        return {
            "level": "R3" if not blockers else "R2",
            "blockers": blockers,
            "live_allowed": False,
        }

    def _model_version(self) -> str:
        return self.model_metadata.model_id if self.model_metadata else self.model.model_version

    def _active_model_payload(self) -> dict[str, Any]:
        if self.model_metadata is None:
            return {
                "alias": "baseline",
                "model_version": self.model.model_version,
                "model_type": "rule-based",
                "metrics": {},
            }
        payload = asdict(self.model_metadata)
        payload["model_version"] = self.model_metadata.model_id
        return payload

    @staticmethod
    def _default_filters(symbol: str) -> SymbolFilters:
        return SymbolFilters(
            symbol=symbol,
            status="TRADING",
            tick_size=Decimal("0.01"),
            step_size=Decimal("0.00001"),
            min_qty=Decimal("0.00001"),
            max_qty=Decimal("100000"),
            min_notional=Decimal("5"),
        )


def snapshot_to_dict(snapshot: RuntimeSnapshot) -> dict[str, Any]:
    return asdict(snapshot)
