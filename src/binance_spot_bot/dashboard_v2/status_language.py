from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement


STATUS_LANGUAGE = {
    "waiting_for_data": "Wachten op genoeg candle data",
    "blocked": "Geblokkeerd door safety/risk check",
    "testnet-readiness": "Readiness-check, geen orders",
    "demo_armed": "Demo-acties toegestaan na guardrails",
    "kill_switch": "Trading-acties geblokkeerd/veilig",
}


def dashboard_v2_status_language_report() -> dict[str, Any]:
    forbidden_phrases = ["approve live", "enable live", "real order now"]
    joined = " ".join(STATUS_LANGUAGE.values()).lower()
    found = [phrase for phrase in forbidden_phrases if phrase in joined]
    return {
        "status": "blocked" if found else "ok",
        "labels": STATUS_LANGUAGE,
        "forbidden_phrases": found,
        "glossary_consistent": True,
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }
