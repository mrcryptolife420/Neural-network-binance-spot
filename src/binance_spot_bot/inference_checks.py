from __future__ import annotations

import time
from typing import Any

from .feature_store_contracts import FeatureStoreContract
from .signal_model import TinyNeuralSignalModel
from .types import FeatureRow


def inference_compatibility_check(model: TinyNeuralSignalModel, contract: FeatureStoreContract) -> dict[str, Any]:
    expected = set(contract.feature_names)
    actual = set(model.feature_names)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    return {
        "status": "ok" if not missing else "blocked",
        "missing_features": missing,
        "extra_features": extra,
        "feature_schema_hash": contract.schema_hash,
        "live_trading_enabled": False,
    }


def inference_latency_budget(model: TinyNeuralSignalModel, row: FeatureRow, *, budget_ms: float = 25.0, iterations: int = 5) -> dict[str, Any]:
    started = time.perf_counter()
    for _ in range(max(1, iterations)):
        model.predict(row)
    elapsed_ms = ((time.perf_counter() - started) * 1000) / max(1, iterations)
    return {
        "status": "ok" if elapsed_ms <= budget_ms else "warn",
        "latency_ms": elapsed_ms,
        "budget_ms": budget_ms,
        "iterations": iterations,
        "live_trading_enabled": False,
    }
