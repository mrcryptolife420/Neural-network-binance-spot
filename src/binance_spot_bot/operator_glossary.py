from __future__ import annotations

from typing import Any


TERMS = {
    "demo": "Binance demo/test environment guarded by local controls",
    "paper": "simulated local trading without real orders",
    "testnet-readiness": "configuration/readiness checks without live trading",
    "live": "disabled",
    "kill switch": "safety control that blocks trading actions",
    "no-live proof": "evidence that live trading and signed real-order paths are not active",
    "P0": "critical safety or secret blocker",
    "waiver": "expiry-bound exception; P0 no-live and secret findings cannot be waived",
}


def explain_operator_term(term: str) -> dict[str, Any]:
    return {"term": term, "meaning": TERMS.get(term.lower(), "Unknown operator term; check the operator manual."), "live_trading_enabled": False}


def operator_glossary() -> dict[str, Any]:
    return {"status": "ok", "terms": TERMS, "live_trading_enabled": False}
