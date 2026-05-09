from __future__ import annotations

from .audit import AuditLog
from .execution import ExecutionEngine
from .risk import RiskEngine
from .signal_model import RuleBasedSignalModel, TinyNeuralSignalModel
from .types import AccountState, FeatureRow, MarketState, RiskDecision, Signal, SymbolFilters


class PaperTrader:
    def __init__(
        self,
        model: RuleBasedSignalModel | TinyNeuralSignalModel,
        risk_engine: RiskEngine,
        execution_engine: ExecutionEngine,
        audit_log: AuditLog,
    ):
        self.model = model
        self.risk_engine = risk_engine
        self.execution_engine = execution_engine
        self.audit_log = audit_log
        self.last_signal: Signal | None = None
        self.last_decision: RiskDecision | None = None

    def step(
        self,
        row: FeatureRow,
        account: AccountState,
        market: MarketState,
        filters: SymbolFilters,
    ):
        signal = self.model.predict(row)
        self.last_signal = signal
        self.audit_log.emit("paper", "signal_generated", {"signal": signal})
        decision = self.risk_engine.decide(signal, account, market)
        self.last_decision = decision
        self.audit_log.emit("paper", "risk_decision", {"decision": decision})
        result = self.execution_engine.execute(decision, market, filters)
        if result.status in {"FILLED", "TEST_ORDER_ACCEPTED"}:
            self.risk_engine.record_trade()
        return result
