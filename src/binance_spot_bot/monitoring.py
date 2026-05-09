from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class RuntimeMetrics:
    api_requests: int = 0
    api_errors: int = 0
    rate_limit_events: int = 0
    signals: dict[str, int] = field(default_factory=lambda: {"BUY": 0, "SELL": 0, "HOLD": 0})
    block_reasons: dict[str, int] = field(default_factory=dict)
    paper_pnl: Decimal = Decimal("0")
    exposure_quote: Decimal = Decimal("0")
    reconciliation_failures: int = 0
    data_quality_warnings: int = 0
    stream_status: str = "ok"

    def record_signal(self, signal: str) -> None:
        self.signals[signal] = self.signals.get(signal, 0) + 1

    def record_block(self, reason: str) -> None:
        self.block_reasons[reason] = self.block_reasons.get(reason, 0) + 1

    def health(self) -> dict[str, str | int]:
        status = "ok"
        if self.rate_limit_events or self.reconciliation_failures or self.data_quality_warnings:
            status = "degraded"
        if self.stream_status not in {"ok", "completed"}:
            status = "degraded"
        if self.api_errors > 10:
            status = "unhealthy"
        return {
            "status": status,
            "api_requests": self.api_requests,
            "api_errors": self.api_errors,
            "rate_limit_events": self.rate_limit_events,
            "reconciliation_failures": self.reconciliation_failures,
            "data_quality_warnings": self.data_quality_warnings,
            "stream_status": self.stream_status,
        }
