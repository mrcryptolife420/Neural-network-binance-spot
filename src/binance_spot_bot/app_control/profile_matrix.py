from __future__ import annotations

from typing import Any


def profile_matrix_report() -> dict[str, Any]:
    rows = [
        {"profile": "Backtest", "api_keys": "No", "orders": "No", "auto_start": True, "live_training_gate": False, "status": "Safe"},
        {"profile": "Paper", "api_keys": "No", "orders": "Paper only", "auto_start": True, "live_training_gate": False, "status": "Safe"},
        {"profile": "Demo Spot", "api_keys": "Yes", "orders": "Demo/test only", "auto_start": "Guarded", "live_training_gate": "Data source", "status": "Safe with guard"},
        {"profile": "Testnet", "api_keys": "Yes", "orders": "Testnet/test only", "auto_start": "Guarded", "live_training_gate": "Validation source", "status": "Safe with guard"},
        {"profile": "Live Locked", "api_keys": "Yes", "orders": "Blocked", "auto_start": False, "live_training_gate": True, "status": "Locked"},
    ]
    return {"status": "ok", "rows": rows, "live_trading_enabled": False}

