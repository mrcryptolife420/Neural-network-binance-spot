from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import NO_ADVICE_STATEMENT, NO_LIVE_STATEMENT, PAPER_ONLY_RESEARCH_STATEMENT
from .common import has_advice_wording, json_write, now_ms, stable_hash, status_from_blockers, to_plain


@dataclass(frozen=True)
class WalkForwardWindow:
    window_id: str
    train_start_ms: int
    train_end_ms: int
    validation_start_ms: int
    validation_end_ms: int
    symbols: list[str]
    source_dataset_ids: list[str]
    min_candles_required: int = 10
    test_start_ms: int | None = None
    test_end_ms: int | None = None
    no_live_statement: str = NO_LIVE_STATEMENT
    paper_only_research_statement: str = PAPER_ONLY_RESEARCH_STATEMENT
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class WalkForwardSplitConfig:
    mode: str = "rolling_window"
    window_count: int = 3
    train_steps: int = 100
    validation_steps: int = 40
    test_steps: int = 20
    step_ms: int = 60_000


@dataclass(frozen=True)
class WalkForwardSplit:
    split_id: str
    mode: str
    windows: list[WalkForwardWindow]
    symbols: list[str]
    created_at_ms: int = field(default_factory=now_ms)
    no_live_statement: str = NO_LIVE_STATEMENT
    no_financial_advice_statement: str = NO_ADVICE_STATEMENT
    paper_only_research_statement: str = PAPER_ONLY_RESEARCH_STATEMENT
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class WalkForwardSplitValidationResult:
    status: str
    blockers: list[str]
    warnings: list[str]
    live_trading_enabled: bool = False


def walk_forward_split_to_dict(split: WalkForwardSplit) -> dict[str, Any]:
    return to_plain(split)


def validate_walk_forward_split(split: WalkForwardSplit) -> WalkForwardSplitValidationResult:
    blockers: list[str] = []
    warnings: list[str] = []
    if split.live_trading_enabled:
        blockers.append("split live_trading_enabled must be false")
    if not split.no_live_statement:
        blockers.append("missing no_live_statement")
    if not split.no_financial_advice_statement:
        blockers.append("missing no_financial_advice_statement")
    if not split.paper_only_research_statement:
        blockers.append("missing paper_only_research_statement")
    if not split.windows:
        blockers.append("empty windows")
    seen: set[str] = set()
    for window in split.windows:
        if window.window_id in seen:
            blockers.append(f"duplicate window_id: {window.window_id}")
        seen.add(window.window_id)
        if window.live_trading_enabled:
            blockers.append(f"window live_trading_enabled must be false: {window.window_id}")
        if not window.symbols:
            blockers.append(f"empty symbols: {window.window_id}")
        if window.min_candles_required <= 0:
            blockers.append(f"invalid min_candles_required: {window.window_id}")
        if window.train_end_ms <= window.train_start_ms or window.validation_end_ms <= window.validation_start_ms:
            blockers.append(f"invalid window boundaries: {window.window_id}")
        if window.train_end_ms > window.validation_start_ms:
            blockers.append(f"train overlaps validation: {window.window_id}")
        if window.test_start_ms is not None:
            if window.validation_end_ms > window.test_start_ms:
                blockers.append(f"validation overlaps test: {window.window_id}")
            if window.test_end_ms is None or window.test_end_ms <= window.test_start_ms:
                blockers.append(f"invalid test boundaries: {window.window_id}")
    if has_advice_wording(split):
        blockers.append("advice wording blocked")
    return WalkForwardSplitValidationResult(status_from_blockers(blockers, warnings), blockers, warnings)


def build_walk_forward_split(config: WalkForwardSplitConfig | None = None, symbols: list[str] | None = None) -> dict[str, Any]:
    config = config or WalkForwardSplitConfig()
    symbols = symbols or ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    start = 1_700_000_000_000
    windows: list[WalkForwardWindow] = []
    span = (config.train_steps + config.validation_steps + config.test_steps) * config.step_ms
    for index in range(config.window_count):
        base = start + index * (span // 2 if config.mode == "rolling_window" else span)
        train_end = base + config.train_steps * config.step_ms
        validation_start = train_end
        validation_end = validation_start + config.validation_steps * config.step_ms
        test_start = validation_end
        test_end = test_start + config.test_steps * config.step_ms
        windows.append(
            WalkForwardWindow(
                window_id=f"wf-window-{index + 1}",
                train_start_ms=base,
                train_end_ms=train_end,
                validation_start_ms=validation_start,
                validation_end_ms=validation_end,
                test_start_ms=test_start,
                test_end_ms=test_end,
                symbols=symbols,
                source_dataset_ids=[f"fixture-{symbol.lower()}-1m" for symbol in symbols],
            )
        )
    split = WalkForwardSplit(f"wf-split-{stable_hash({'mode': config.mode, 'symbols': symbols, 'windows': len(windows)})[:12]}", config.mode, windows, symbols)
    validation = validate_walk_forward_split(split)
    return {"status": validation.status, "split": walk_forward_split_to_dict(split), "validation": to_plain(validation), "live_trading_enabled": False}


def write_walk_forward_split_report(root: Path, split: WalkForwardSplit) -> dict[str, Any]:
    payload = {"status": validate_walk_forward_split(split).status, "split": walk_forward_split_to_dict(split), "validation": to_plain(validate_walk_forward_split(split)), "live_trading_enabled": False}
    return json_write(root / "data" / "portfolio-lab" / "walk-forward" / "splits" / f"{split.split_id}.json", payload)

