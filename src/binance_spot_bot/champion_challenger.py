from __future__ import annotations


def champion_challenger(champion: float, challenger: float, *, min_delta: float = 0.0) -> dict[str, object]:
    decision = "promote_challenger" if challenger > champion + min_delta else "keep_champion"
    return {"decision": decision, "champion": champion, "challenger": challenger, "scope": "paper_shadow_demo_only", "live_trading_enabled": False}
