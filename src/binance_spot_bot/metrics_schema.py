from dataclasses import dataclass
@dataclass(frozen=True)
class MetricEvent:
    name: str
    value: float
    ts_ms: int
    live_trading_enabled: bool = False
