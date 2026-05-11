# Roadmap 070 - Multi Symbol Evidence Export

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Voeg een operator evidence export toe voor multi-crypto demo trading.

## Nieuwe verbeteringen
1. Exporteer actieve symbolen.
2. Exporteer validation status.
3. Exporteer budget allocation.
4. Exporteer multi bot status rows.
5. Exporteer aggregated totals.
6. Redacteer payloads.
7. Schrijf onder `data/evidence/multi-symbol/`.

## Acceptatiecriteria
- Evidence export schrijft JSON.
- Payload bevat `live_trading_enabled: false`.
- Tests dekken export.

## Uitvoering
- Multi-symbol dashboard helpers uitgebreid met presets, validatie, budget allocation, risk summary, next action en evidence export.
- Simple dashboard uitgebreid met watchlist opslaan/resetten, symbol validation guardrails, total demo quote budget, stop one symbol, risk limit summary, budget allocation en export multi-symbol evidence.
- Tests toegevoegd en uitgebreid voor multi-symbol helpers en dashboard markers.
- Validatie: python -m pytest tests/test_multi_symbol_demo.py tests/test_simple_demo_dashboard.py tests/test_roadmap_025_dashboard_browser_smoke.py -q -> 14 passed.
- Validatie: python -m pytest -q -> 222 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Validatie: dashboard-browser-smoke op http://127.0.0.1:8504 -> status ok.
- Live trading blijft disabled.
