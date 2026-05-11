from __future__ import annotations

import csv
import json
import statistics
import time
from dataclasses import asdict, dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any

from .backtest import BacktestEngine
from .data import DataStore
from .features import assert_no_lookahead, build_feature_rows, build_label_rows, chronological_split
from .indicators import INDICATOR_PROFILES, indicator_snapshot
from .redaction import redact_payload
from .risk import RiskEngine, RiskLimits
from .signal_model import TinyNeuralSignalModel
from .types import Candle


@dataclass(frozen=True)
class StrategyDataset:
    dataset_id: str
    symbol: str
    interval: str
    candles: int
    features: int
    labels: int
    train: int
    validation: int
    test: int
    feature_path: str
    label_path: str
    leakage_guard: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CalibrationResult:
    status: str
    datasets: list[StrategyDataset]
    symbol_rankings: list[dict[str, Any]]
    indicator_rankings: list[dict[str, Any]]
    confidence_thresholds: list[dict[str, Any]]
    promotion_gate: dict[str, Any]
    report_paths: dict[str, str] = field(default_factory=dict)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(
            {
                "status": self.status,
                "datasets": [dataset.to_dict() for dataset in self.datasets],
                "symbol_rankings": self.symbol_rankings,
                "indicator_rankings": self.indicator_rankings,
                "confidence_thresholds": self.confidence_thresholds,
                "promotion_gate": self.promotion_gate,
                "report_paths": self.report_paths,
                "live_trading_enabled": False,
            }
        )


def build_strategy_dataset(
    store: DataStore,
    symbol: str,
    interval: str,
    candles: list[Candle] | None = None,
    *,
    window: int = 20,
    horizon_bars: int = 3,
) -> StrategyDataset:
    symbol = symbol.upper()
    candles = candles if candles is not None else store.load_candles_csv(symbol, interval)
    features = build_feature_rows(symbol, candles, window=window)
    labels = build_label_rows(candles, window=window, horizon_bars=horizon_bars)
    assert_no_lookahead(features, labels)
    train, validation, test = chronological_split(features)
    dataset_id = f"{symbol}_{interval}_strategy_calibration"
    feature_path = store.save_feature_rows(dataset_id, features)
    label_path = store.save_label_rows(dataset_id, labels)
    return StrategyDataset(
        dataset_id=dataset_id,
        symbol=symbol,
        interval=interval,
        candles=len(candles),
        features=len(features),
        labels=len(labels),
        train=len(train),
        validation=len(validation),
        test=len(test),
        feature_path=str(feature_path),
        label_path=str(label_path),
        leakage_guard="pass",
    )


def calibrate_confidence(candles_by_symbol: dict[str, list[Candle]], *, interval: str = "1m") -> list[dict[str, Any]]:
    rows = []
    for symbol, candles in sorted(candles_by_symbol.items()):
        closes = [float(candle.close) for candle in candles]
        if len(closes) < 30:
            rows.append({"symbol": symbol.upper(), "interval": interval, "status": "blocked", "reason": "insufficient_candles"})
            continue
        returns = [(closes[index] / closes[index - 1]) - 1 for index in range(1, len(closes)) if closes[index - 1]]
        volatility = statistics.pstdev(returns) if len(returns) > 1 else 0.0
        trend = (closes[-1] / closes[0]) - 1 if closes[0] else 0.0
        hit_proxy = sum(1 for item in returns if item > 0) / len(returns) if returns else 0.0
        threshold = max(0.52, min(0.85, 0.55 + volatility * 10 - abs(trend) * 0.2))
        rows.append(
            {
                "symbol": symbol.upper(),
                "interval": interval,
                "status": "ready",
                "trend": round(trend, 6),
                "volatility": round(volatility, 6),
                "hit_rate_proxy": round(hit_proxy, 4),
                "recommended_min_confidence": round(threshold, 4),
            }
        )
    return rows


def rank_symbols(candles_by_symbol: dict[str, list[Candle]]) -> list[dict[str, Any]]:
    rows = []
    for symbol, candles in sorted(candles_by_symbol.items()):
        if len(candles) < 30:
            rows.append({"symbol": symbol.upper(), "score": 0, "status": "blocked", "reason": "insufficient_candles"})
            continue
        closes = [float(candle.close) for candle in candles]
        volumes = [float(candle.quote_volume or candle.volume) for candle in candles]
        trend = abs((closes[-1] / closes[0]) - 1) if closes[0] else 0.0
        returns = [(closes[index] / closes[index - 1]) - 1 for index in range(1, len(closes)) if closes[index - 1]]
        volatility = statistics.pstdev(returns) if len(returns) > 1 else 0.0
        volume_score = min(1.0, statistics.mean(volumes[-20:]) / 100_000) if volumes else 0.0
        score = max(0.0, min(1.0, trend * 4 + volume_score - volatility * 15))
        rows.append({"symbol": symbol.upper(), "score": round(score, 4), "status": "ready", "trend": round(trend, 6), "volatility": round(volatility, 6)})
    return sorted(rows, key=lambda row: row["score"], reverse=True)


def rank_indicator_profiles(candles_by_symbol: dict[str, list[Candle]]) -> list[dict[str, Any]]:
    rows = []
    for profile in INDICATOR_PROFILES:
        confidences = []
        ready = 0
        for symbol, candles in candles_by_symbol.items():
            snapshot = indicator_snapshot(symbol.upper(), candles, requested_profile=profile)
            confidence = float(snapshot.get("confidence", 0) or 0)
            if snapshot.get("regime") != "insufficient_data":
                ready += 1
            confidences.append(confidence)
        rows.append(
            {
                "profile": profile,
                "ready_symbols": ready,
                "avg_confidence": round(statistics.mean(confidences), 4) if confidences else 0,
                "score": round((ready / max(1, len(candles_by_symbol))) * (statistics.mean(confidences) if confidences else 0), 4),
            }
        )
    return sorted(rows, key=lambda row: row["score"], reverse=True)


def run_backtest_calibration(candles_by_symbol: dict[str, list[Candle]]) -> list[dict[str, Any]]:
    rows = []
    limits = RiskLimits(max_daily_loss_quote=Decimal("100"), max_position_quote=Decimal("25"), max_trades_per_day=50, min_signal_confidence=0.1, max_spread_bps=Decimal("100"), default_quote_size=Decimal("10"))
    for symbol, candles in sorted(candles_by_symbol.items()):
        if len(candles) < 40:
            rows.append({"symbol": symbol.upper(), "status": "blocked", "reason": "insufficient_candles"})
            continue
        features = build_feature_rows(symbol.upper(), candles, window=20)
        labels = build_label_rows(candles, window=20, horizon_bars=3)
        model = TinyNeuralSignalModel()
        model.fit(features, labels, epochs=3)
        result = BacktestEngine(RiskEngine(limits, kill_switch=False)).run(features, model)
        rows.append({"symbol": symbol.upper(), "status": "ready", "trades": result.trades, "final_equity": str(result.final_equity), "max_drawdown": str(result.max_drawdown)})
    return rows


def paper_promotion_gate(calibration_rows: list[dict[str, Any]], backtest_rows: list[dict[str, Any]]) -> dict[str, Any]:
    ready = [row for row in calibration_rows if row.get("status") == "ready"]
    backtests = [row for row in backtest_rows if row.get("status") == "ready"]
    blockers = []
    if not ready:
        blockers.append("no_ready_calibration_rows")
    if not backtests:
        blockers.append("no_ready_backtests")
    if any(float(row.get("recommended_min_confidence", 1)) > 0.85 for row in ready):
        blockers.append("confidence_threshold_unstable")
    return {
        "status": "paper_approved" if not blockers else "blocked",
        "scope": "paper_only",
        "blockers": blockers,
        "operator_confirmation_required": not blockers,
        "live_trading_enabled": False,
    }


def calibrate_strategy(
    data_dir: Path,
    candles_by_symbol: dict[str, list[Candle]],
    *,
    interval: str = "1m",
) -> CalibrationResult:
    store = DataStore(data_dir)
    datasets = [build_strategy_dataset(store, symbol, interval, candles) for symbol, candles in sorted(candles_by_symbol.items())]
    thresholds = calibrate_confidence(candles_by_symbol, interval=interval)
    symbol_rankings = rank_symbols(candles_by_symbol)
    indicator_rankings = rank_indicator_profiles(candles_by_symbol)
    backtests = run_backtest_calibration(candles_by_symbol)
    gate = paper_promotion_gate(thresholds, backtests)
    result = CalibrationResult(
        status="ready" if gate["status"] == "paper_approved" else "blocked",
        datasets=datasets,
        symbol_rankings=symbol_rankings,
        indicator_rankings=indicator_rankings,
        confidence_thresholds=thresholds,
        promotion_gate={**gate, "backtests": backtests},
    )
    paths = write_strategy_calibration_report(data_dir, result)
    return CalibrationResult(
        status=result.status,
        datasets=result.datasets,
        symbol_rankings=result.symbol_rankings,
        indicator_rankings=result.indicator_rankings,
        confidence_thresholds=result.confidence_thresholds,
        promotion_gate=result.promotion_gate,
        report_paths=paths,
    )


def write_strategy_calibration_report(data_dir: Path, result: CalibrationResult) -> dict[str, str]:
    out = data_dir / "strategy-calibration"
    out.mkdir(parents=True, exist_ok=True)
    stamp = int(time.time() * 1000)
    json_path = out / f"strategy-calibration-{stamp}.json"
    latest_path = out / "latest.json"
    md_path = out / "strategy-calibration-report.md"
    payload = result.to_dict()
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    latest_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    _write_csv(out / "symbol-ranking.csv", result.symbol_rankings)
    _write_csv(out / "indicator-ranking.csv", result.indicator_rankings)
    lines = ["# Strategy Calibration Report", "", f"Status: {result.status}", "", "## Symbol Ranking"]
    lines.extend(f"- {row['symbol']}: {row['score']}" for row in result.symbol_rankings)
    lines.append("")
    lines.append("## Promotion Gate")
    lines.append(json.dumps(result.promotion_gate, default=str))
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return {"json": str(json_path), "latest": str(latest_path), "markdown": str(md_path), "symbol_ranking_csv": str(out / "symbol-ranking.csv"), "indicator_ranking_csv": str(out / "indicator-ranking.csv")}


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=sorted({key for row in rows for key in row.keys()}))
        writer.writeheader()
        writer.writerows(rows)
