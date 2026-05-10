from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any

from .backtest import BacktestEngine
from .dataset_governance import (
    DatasetManifest,
    build_dataset_manifest,
    leakage_guard,
)
from .features import build_feature_rows, build_label_rows
from .risk import RiskEngine, RiskLimits
from .signal_model import RuleBasedSignalModel, TinyNeuralSignalModel
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
    mode: str = "rule_baseline"
    costs: dict[str, str] | None = None
    manifest: dict[str, Any] | None = None
    leakage: dict[str, Any] | None = None
    baseline_summary: dict[str, Any] | None = None
    candidate_summary: dict[str, Any] | None = None
    shuffled: bool = False


@dataclass(frozen=True)
class WalkForwardConfig:
    window: int = 5
    horizon_bars: int = 2
    n_splits: int = 3
    validation_size: int | None = None
    test_size: int | None = None
    gap: int = 2
    expanding: bool = True
    fee_bps: Decimal = Decimal("10")
    slippage_bps: Decimal = Decimal("5")
    spread_bps: Decimal = Decimal("0")
    starting_quote: Decimal = Decimal("1000")


@dataclass(frozen=True)
class WalkForwardFold:
    train_start: int
    train_end: int
    validation_start: int
    validation_end: int
    test_start: int
    test_end: int


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


def walk_forward_folds(length: int, config: WalkForwardConfig) -> list[WalkForwardFold]:
    if length <= 0:
        return []
    if config.n_splits < 1:
        raise ValueError("n_splits must be at least 1")
    if config.gap < 0:
        raise ValueError("gap must not be negative")
    test_size = config.test_size or max(1, length // (config.n_splits + 3))
    validation_size = config.validation_size or test_size
    folds: list[WalkForwardFold] = []
    for fold in range(config.n_splits):
        test_start = length - (config.n_splits - fold) * test_size
        test_end = min(length, test_start + test_size)
        validation_end = test_start - config.gap
        validation_start = validation_end - validation_size
        train_end = validation_start - config.gap
        train_start = 0 if config.expanding else max(0, train_end - max(validation_size * 2, test_size * 2))
        if min(train_end, validation_start, validation_end, test_start) <= 0:
            continue
        if train_start < train_end < validation_start < validation_end < test_start < test_end:
            folds.append(WalkForwardFold(train_start, train_end, validation_start, validation_end, test_start, test_end))
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


def evaluate_walk_forward(
    symbol: str,
    interval: str,
    candles: list[Candle],
    *,
    dataset_id: str = "walkforward-demo",
    source: str = "demo",
    config: WalkForwardConfig | None = None,
) -> EvaluationReport:
    config = config or WalkForwardConfig()
    features = build_feature_rows(symbol, candles, window=config.window)
    labels = build_label_rows(candles, window=config.window, horizon_bars=config.horizon_bars)
    folds = walk_forward_folds(len(features), config)
    if not folds:
        raise ValueError("not enough chronological rows for walk-forward evaluation")
    fold_payloads: list[dict[str, Any]] = []
    baseline_pnl = Decimal("0")
    candidate_pnl = Decimal("0")
    first_fold = folds[0]
    manifest: DatasetManifest | None = None
    overall_leakage = None
    for fold_no, fold in enumerate(folds, start=1):
        train_rows = features[fold.train_start : fold.train_end]
        validation_rows = features[fold.validation_start : fold.validation_end]
        test_rows = features[fold.test_start : fold.test_end]
        leakage = leakage_guard(
            features,
            labels,
            train_rows=train_rows,
            validation_rows=validation_rows,
            test_rows=test_rows,
            label_horizon=config.horizon_bars,
            embargo=config.gap,
        )
        if not leakage.passed:
            raise ValueError("walk-forward leakage guard failed: " + ", ".join(issue.code for issue in leakage.issues))
        baseline_model = RuleBasedSignalModel()
        candidate_model = TinyNeuralSignalModel()
        candidate_model.fit(train_rows, labels, epochs=8)
        engine = BacktestEngine(
            RiskEngine(_evaluation_limits(), kill_switch=False),
            fee_bps=config.fee_bps,
            slippage_bps=config.slippage_bps + (config.spread_bps / Decimal("2")),
        )
        baseline_result = engine.run(test_rows, baseline_model, starting_quote=config.starting_quote)
        candidate_result = engine.run(test_rows, candidate_model, starting_quote=config.starting_quote)
        baseline_pnl += baseline_result.pnl
        candidate_pnl += candidate_result.pnl
        fold_payloads.append(
            {
                "fold": fold_no,
                "train_range": _range_payload(train_rows),
                "validation_range": _range_payload(validation_rows),
                "test_range": _range_payload(test_rows),
                "gap": config.gap,
                "leakage": leakage.to_dict(),
                "baseline": _result_metrics(baseline_result, config.starting_quote),
                "candidate": _result_metrics(candidate_result, config.starting_quote),
                "confidence_buckets": _confidence_buckets(candidate_model, test_rows),
            }
        )
        if fold_no == 1:
            manifest = build_dataset_manifest(
                dataset_id=dataset_id,
                source=source,
                symbol=symbol,
                interval=interval,
                candles=candles,
                features=features,
                labels=labels,
                train_rows=features[first_fold.train_start : first_fold.train_end],
                validation_rows=features[first_fold.validation_start : first_fold.validation_end],
                test_rows=features[first_fold.test_start : folds[-1].test_end],
                lookback_window=config.window,
                label_horizon=config.horizon_bars,
                fee_bps=config.fee_bps,
                slippage_bps=config.slippage_bps,
                spread_bps=config.spread_bps,
            )
            overall_leakage = leakage
    return EvaluationReport(
        symbol=symbol,
        interval=interval,
        folds=fold_payloads,
        gap=config.gap,
        mode="walk_forward",
        costs={
            "fee_bps": str(config.fee_bps),
            "slippage_bps": str(config.slippage_bps),
            "spread_bps": str(config.spread_bps),
        },
        manifest=manifest.to_dict() if manifest else None,
        leakage=overall_leakage.to_dict() if overall_leakage else None,
        baseline_summary={"folds": len(folds), "pnl": str(baseline_pnl)},
        candidate_summary={
            "folds": len(folds),
            "pnl": str(candidate_pnl),
            "beats_baseline": candidate_pnl > baseline_pnl,
        },
    )


def report_to_dict(report: EvaluationReport) -> dict[str, Any]:
    return asdict(report)


def _range_payload(rows: list[Any]) -> dict[str, int | None]:
    if not rows:
        return {"start": None, "end": None, "count": 0}
    return {"start": rows[0].timestamp_ms, "end": rows[-1].timestamp_ms, "count": len(rows)}


def _evaluation_limits() -> RiskLimits:
    return RiskLimits(
        max_daily_loss_quote=Decimal("500"),
        max_position_quote=Decimal("25"),
        max_trades_per_day=10_000,
        min_signal_confidence=0.1,
        max_spread_bps=Decimal("100"),
    )


def _result_metrics(result: Any, starting_quote: Decimal) -> dict[str, Any]:
    net_return = (result.pnl / starting_quote) if starting_quote else Decimal("0")
    return {
        "trades": result.trades,
        "blocked": result.blocked,
        "final_equity": str(result.final_equity),
        "pnl": str(result.pnl),
        "net_return": str(net_return),
        "max_drawdown": str(result.max_drawdown),
        "turnover": result.trades,
    }


def _confidence_buckets(model: TinyNeuralSignalModel, rows: list[Any]) -> dict[str, int]:
    buckets = {"0.00-0.25": 0, "0.25-0.50": 0, "0.50-0.75": 0, "0.75-1.00": 0}
    for row in rows:
        confidence = model.predict(row).confidence
        if confidence < 0.25:
            buckets["0.00-0.25"] += 1
        elif confidence < 0.50:
            buckets["0.25-0.50"] += 1
        elif confidence < 0.75:
            buckets["0.50-0.75"] += 1
        else:
            buckets["0.75-1.00"] += 1
    return buckets
