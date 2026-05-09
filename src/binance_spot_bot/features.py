from __future__ import annotations

from statistics import mean, pstdev

from .types import Candle, FeatureRow, LabelRow


def build_feature_rows(symbol: str, candles: list[Candle], window: int = 20) -> list[FeatureRow]:
    if window < 2:
        raise ValueError("window must be at least 2")
    closes = [float(c.close) for c in candles]
    volumes = [float(c.volume) for c in candles]
    rows: list[FeatureRow] = []
    for i in range(window, len(candles)):
        close = closes[i]
        prev_close = closes[i - 1]
        close_window = closes[i - window : i]
        volume_window = volumes[i - window : i]
        returns = [(close_window[j] / close_window[j - 1]) - 1 for j in range(1, len(close_window))]
        volatility = pstdev(returns) if len(returns) > 1 else 0.0
        avg_volume = mean(volume_window)
        vol_std = pstdev(volume_window) or 1.0
        candle = candles[i]
        high_low_range = float(candle.high - candle.low) or 1.0
        values = {
            "ret_1": (close / prev_close) - 1,
            "ret_window": (close / close_window[0]) - 1,
            "rolling_volatility": volatility,
            "volume_zscore": (volumes[i] - avg_volume) / vol_std,
            "body_ratio": abs(float(candle.close - candle.open)) / high_low_range,
            "upper_wick_ratio": float(candle.high - max(candle.open, candle.close)) / high_low_range,
            "lower_wick_ratio": float(min(candle.open, candle.close) - candle.low) / high_low_range,
        }
        rows.append(
            FeatureRow(
                symbol=symbol,
                timestamp_ms=candle.close_time_ms,
                values=values,
                close=candle.close,
            )
        )
    return rows


def build_label_rows(candles: list[Candle], window: int = 20, horizon_bars: int = 3) -> list[LabelRow]:
    if horizon_bars < 1:
        raise ValueError("horizon_bars must be positive")
    rows: list[LabelRow] = []
    for i in range(window, len(candles) - horizon_bars):
        close_now = float(candles[i].close)
        close_future = float(candles[i + horizon_bars].close)
        future_return = (close_future / close_now) - 1
        label = 1 if future_return > 0 else 0
        rows.append(
            LabelRow(
                timestamp_ms=candles[i].close_time_ms,
                horizon_bars=horizon_bars,
                future_return=future_return,
                label=label,
            )
        )
    return rows


def chronological_split[T](rows: list[T], train_ratio: float = 0.6, validation_ratio: float = 0.2) -> tuple[list[T], list[T], list[T]]:
    if not 0 < train_ratio < 1:
        raise ValueError("train_ratio must be between 0 and 1")
    if not 0 <= validation_ratio < 1:
        raise ValueError("validation_ratio must be between 0 and 1")
    train_end = int(len(rows) * train_ratio)
    validation_end = train_end + int(len(rows) * validation_ratio)
    return rows[:train_end], rows[train_end:validation_end], rows[validation_end:]


def assert_no_lookahead(features: list[FeatureRow], labels: list[LabelRow]) -> None:
    label_by_ts = {label.timestamp_ms: label for label in labels}
    for row in features:
        if row.timestamp_ms in label_by_ts and label_by_ts[row.timestamp_ms].timestamp_ms != row.timestamp_ms:
            raise ValueError("Feature/label timestamp mismatch")
    timestamps = [row.timestamp_ms for row in features]
    if timestamps != sorted(timestamps):
        raise ValueError("Feature rows must be chronological")

