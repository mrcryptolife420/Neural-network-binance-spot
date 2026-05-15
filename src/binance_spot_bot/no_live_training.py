from __future__ import annotations

from typing import Any


def no_live_training_lesson(failure_example: bool = False) -> dict[str, Any]:
    steps = [
        "verify runtime modes are demo, paper, testnet-readiness",
        "run no-live-proof-pack",
        "check dashboard no-live banner",
        "stop immediately if live mode appears",
    ]
    status = "blocked" if failure_example else "ok"
    return {
        "status": status,
        "title": "Guided no-live verification",
        "steps": steps,
        "report_includes_no_live_proof": True,
        "live_trading_enabled": False,
    }


def no_live_training_statement() -> dict[str, Any]:
    return {"status": "ok", "text": "Training and support never enable live trading.", "live_trading_enabled": False}
