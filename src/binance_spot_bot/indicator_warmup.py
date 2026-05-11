from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .binance_data_ingestion import BinanceDataIngestionService, IngestionRequest
from .config import BotSettings
from .indicators import indicator_snapshot
from .public_data_quality import candle_quality
from .redaction import redact_payload


@dataclass(frozen=True)
class WarmupPolicy:
    minimum_candles: int = 30
    recommended_candles: int = 120
    strong_candles: int = 500
    intervals: tuple[str, ...] = ("1m", "5m", "15m", "1h")


def warmup_indicators(
    settings: BotSettings,
    symbols: list[str],
    *,
    candle_limit: int = 120,
    service: BinanceDataIngestionService | None = None,
    policy: WarmupPolicy = WarmupPolicy(),
) -> dict[str, Any]:
    service = service or BinanceDataIngestionService(settings)
    result = service.ingest(
        IngestionRequest(
            symbols=symbols,
            intervals=list(policy.intervals),
            candle_limit=candle_limit,
            include_order_book=True,
            include_24h_ticker=True,
            include_rolling_ticker=True,
            include_trades=True,
        )
    )
    rows = []
    for bundle in result.bundles:
        primary = bundle.candles.get("1m") or next(iter(bundle.candles.values()), [])
        quality = candle_quality(primary, min_candles=policy.minimum_candles)
        status = _warmup_status(len(primary), policy)
        confidence_penalty = 0.0 if len(primary) >= policy.recommended_candles else 0.10 if len(primary) >= policy.minimum_candles else 0.35
        rows.append(
            {
                "symbol": bundle.symbol,
                "status": status,
                "source": bundle.source,
                "candles_loaded": len(primary),
                "required_candles": policy.minimum_candles,
                "recommended_candles": policy.recommended_candles,
                "strong_candles": policy.strong_candles,
                "freshness_score": bundle.freshness_score,
                "quality_status": quality["status"],
                "confidence_penalty": confidence_penalty,
                "indicator": indicator_snapshot(bundle.symbol, primary),
                "next_action": "fetch more public candles" if len(primary) < policy.minimum_candles else "ready",
            }
        )
    payload = {
        "status": "ready" if rows and all(row["candles_loaded"] >= policy.minimum_candles for row in rows) else "blocked",
        "rows": rows,
        "manifests": result.manifests,
        "warnings": result.warnings,
        "live_trading_enabled": False,
    }
    write_indicator_warmup_report(settings.data_dir, payload)
    return redact_payload(payload)


def multi_timeframe_indicator_context(bundle: Any) -> dict[str, Any]:
    candles_by_interval = bundle.candles if hasattr(bundle, "candles") else bundle.get("candles", {})
    rows = {}
    regimes = []
    confidences = []
    for interval, candles in candles_by_interval.items():
        symbol = bundle.symbol if hasattr(bundle, "symbol") else bundle.get("symbol", "")
        snap = indicator_snapshot(symbol, candles)
        rows[interval] = snap
        regimes.append(str(snap.get("regime", "unknown")))
        confidences.append(float(snap.get("confidence", 0.0) or 0.0))
    known = [item for item in regimes if item not in {"unknown", "insufficient_data"}]
    agreement = (max(known.count(item) for item in set(known)) / len(known)) if known else 0.0
    return {
        "timeframes": rows,
        "timeframe_agreement_score": round(agreement, 4),
        "trend_alignment": "aligned" if agreement >= 0.75 else "mixed",
        "volatility_alignment": "unknown" if not known else "ok",
        "confidence_adjustment": round((agreement - 0.5) * 0.2, 4),
    }


def write_indicator_warmup_report(data_dir: Path, payload: dict[str, Any]) -> dict[str, str]:
    out = data_dir / "public_binance" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "indicator_warmup_report.json"
    md_path = out / "indicator_warmup_report.md"
    json_path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    lines = ["# Indicator Warmup Report", "", f"Status: {payload.get('status', 'unknown')}", ""]
    for row in payload.get("rows", []):
        lines.append(f"- {row['symbol']}: {row['candles_loaded']} candles, {row['quality_status']}, source={row['source']}")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def _warmup_status(count: int, policy: WarmupPolicy) -> str:
    if count < policy.minimum_candles:
        return "blocked"
    if count < policy.recommended_candles:
        return "warning"
    if count >= policy.strong_candles:
        return "strong"
    return "ready"
