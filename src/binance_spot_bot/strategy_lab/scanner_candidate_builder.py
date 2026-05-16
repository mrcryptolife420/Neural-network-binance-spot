from __future__ import annotations

import hashlib
import time
from dataclasses import asdict, dataclass, field
from decimal import Decimal
from typing import Any

from binance_spot_bot.redaction import redact_payload
from binance_spot_bot.market_intelligence.scanner_presets import get_scanner_preset
from binance_spot_bot.market_intelligence.symbol_ranking import rank_symbols
from binance_spot_bot.market_intelligence.watchlist_scanner import run_watchlist_scan
from . import NO_ADVICE_STATEMENT, NO_LIVE_STATEMENT


def _dec(value: Any) -> Decimal:
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


def _id(*parts: object) -> str:
    return hashlib.sha256("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class ScannerCandidateFilter:
    max_candidates: int = 5
    min_quote_volume: str = "0"
    max_spread_bps: str = "100"
    min_data_quality_score: int = 50
    quote_asset: str = "USDT"
    include_symbols: tuple[str, ...] = ()
    exclude_symbols: tuple[str, ...] = ()
    require_cached_klines: bool = False


@dataclass(frozen=True)
class ScannerCandidateSource:
    scanner_run_id: str
    preset_id: str
    ranking_dimension: str
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))


@dataclass(frozen=True)
class ScannerExperimentCandidate:
    candidate_id: str
    symbol: str
    source_run_id: str
    source_preset: str
    ranking_reasons: tuple[str, ...]
    metrics_snapshot: dict[str, Any]
    data_quality_status: str
    available_intervals: tuple[str, ...] = ("1m", "5m")
    recommended_intervals: tuple[str, ...] = ("1m",)
    warnings: tuple[str, ...] = ()
    not_financial_advice_statement: str = NO_ADVICE_STATEMENT
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class ScannerCandidateBuildReport:
    status: str
    source: ScannerCandidateSource
    candidates: tuple[ScannerExperimentCandidate, ...]
    warnings: tuple[str, ...]
    no_live_statement: str = NO_LIVE_STATEMENT
    no_advice_statement: str = NO_ADVICE_STATEMENT
    live_trading_enabled: bool = False


def build_scanner_candidates(
    scan_report: dict[str, Any] | None = None,
    *,
    preset_id: str = "majors_overview",
    filters: ScannerCandidateFilter | None = None,
) -> dict[str, Any]:
    filters = filters or ScannerCandidateFilter()
    preset = get_scanner_preset(preset_id)
    scan_report = scan_report or run_watchlist_scan(preset.symbols, preset=preset_id)
    metrics = list(scan_report.get("metrics", []))
    ranking = rank_symbols(metrics, preset.ranking_dimension, limit=filters.max_candidates)
    rank_by_symbol = {str(row["symbol"]): row for row in ranking.get("ranks", [])}
    warnings: list[str] = []
    if not metrics:
        warnings.append("missing scanner metrics")
    candidates: list[ScannerExperimentCandidate] = []
    for row in metrics:
        symbol = str(row.get("symbol", "")).upper()
        if filters.quote_asset and not symbol.endswith(filters.quote_asset):
            continue
        if filters.include_symbols and symbol not in filters.include_symbols:
            continue
        if symbol in filters.exclude_symbols:
            continue
        if _dec(row.get("quote_volume_24h")) < _dec(filters.min_quote_volume):
            continue
        if _dec(row.get("spread_bps")) > _dec(filters.max_spread_bps):
            continue
        if int(row.get("data_quality_score", 0)) < filters.min_data_quality_score:
            continue
        reasons = ["scanner_metric_rank"]
        if symbol in rank_by_symbol:
            reasons.append(f"rank_{rank_by_symbol[symbol]['rank']}")
        row_warnings = tuple(str(item) for item in row.get("warnings", []))
        candidates.append(
            ScannerExperimentCandidate(
                candidate_id=_id(scan_report.get("run_id", "fixture"), symbol, preset_id),
                symbol=symbol,
                source_run_id=str(scan_report.get("run_id", "fixture")),
                source_preset=preset_id,
                ranking_reasons=tuple(reasons),
                metrics_snapshot=row,
                data_quality_status="ok" if int(row.get("data_quality_score", 0)) >= 75 else "warn",
                warnings=row_warnings,
            )
        )
        if len(candidates) >= filters.max_candidates:
            break
    source = ScannerCandidateSource(str(scan_report.get("run_id", "fixture")), preset_id, preset.ranking_dimension)
    report = ScannerCandidateBuildReport("ok", source, tuple(candidates), tuple(warnings))
    return redact_payload(asdict(report))
