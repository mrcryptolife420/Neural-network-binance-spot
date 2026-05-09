from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any

from .backtest import BacktestEngine
from .features import build_feature_rows
from .risk import RiskEngine, RiskLimits
from .signal_model import RuleBasedSignalModel
from .types import Candle


@dataclass(frozen=True)
class FoldRange:
    train_start: int
    train_end: int
    test_start: int
    test_end: int


@dataclass(frozen=True)
class EvaluationReport:
    symbol: str
    interval: str
    folds: list[dict[str, Any]]
    gap: int
    shuffled: bool = False


def time_series_folds(length: int, n_splits: int = 3, test_size: int | None = None, gap: int = 0) -> list[FoldRange]:
    if length <= 0:
        return []
    if n_splits < 1:
        raise ValueError("n_splits must be at least 1")
    if gap < 0:
        raise ValueError("gap must not be negative")
    test_size = test_size or max(1, length // (n_splits + 1))
    folds: list[FoldRange] = []
    for fold in range(n_splits):
        test_start = length - (n_splits - fold) * test_size
        test_end = min(length, test_start + test_size)
        train_end = max(0, test_start - gap)
        if test_start <= 0 or train_end <= 0 or test_start >= test_end:
            continue
        folds.append(FoldRange(0, train_end, test_start, test_end))
    return folds


def evaluate_rule_baseline(
    symbol: str,
    interval: str,
    candles: list[Candle],
    *,
    window: int = 5,
    gap: int = 2,
    n_splits: int = 3,
) -> EvaluationReport:
    features = build_feature_rows(symbol, candles, window=window)
    folds = []
    for fold_no, fold in enumerate(time_series_folds(len(features), n_splits=n_splits, gap=gap), start=1):
        train_rows = features[fold.train_start : fold.train_end]
        test_rows = features[fold.test_start : fold.test_end]
        model = RuleBasedSignalModel()
        limits = RiskLimits(
            max_daily_loss_quote=Decimal("50"),
            max_position_quote=Decimal("25"),
            max_trades_per_day=10_000,
            min_signal_confidence=0.1,
            max_spread_bps=Decimal("100"),
        )
        result = BacktestEngine(RiskEngine(limits, kill_switch=False)).run(test_rows, model)
        distribution: dict[str, int] = {"BUY": 0, "SELL": 0, "HOLD": 0}
        for row in test_rows:
            signal = model.predict(row).signal.value
            distribution[signal] = distribution.get(signal, 0) + 1
        folds.append(
            {
                "fold": fold_no,
                "train_range": _range_payload(train_rows),
                "test_range": _range_payload(test_rows),
                "gap": gap,
                "signal_distribution": distribution,
                "pnl": str(result.pnl),
                "max_drawdown": str(result.max_drawdown),
                "turnover": result.trades,
                "block_reasons": {"blocked": result.blocked},
            }
        )
    return EvaluationReport(symbol=symbol, interval=interval, folds=folds, gap=gap)


def report_to_dict(report: EvaluationReport) -> dict[str, Any]:
    return asdict(report)


def _range_payload(rows: list[Any]) -> dict[str, int | None]:
    if not rows:
        return {"start": None, "end": None, "count": 0}
    return {"start": rows[0].timestamp_ms, "end": rows[-1].timestamp_ms, "count": len(rows)}
