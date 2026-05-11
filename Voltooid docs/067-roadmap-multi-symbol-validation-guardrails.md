# Roadmap 067 - Multi Symbol Validation Guardrails

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Voeg duidelijke validatie toe voordat meerdere demo-symbolen gestart worden.

## Nieuwe verbeteringen
1. Valideer lege symbolen.
2. Valideer te veel symbolen.
3. Valideer alleen alfanumerieke symbolen.
4. Waarschuw voor niet-`USDT` quote pairs.
5. Toon blockers/warnings in dashboard.
6. Blokkeer start bij ongeldige selectie.
7. Houd validatie lokaal en zonder live order calls.

## Acceptatiecriteria
- Validatie geeft `status`, `blockers`, `warnings` en `valid_symbols`.
- Dashboard toont validation guardrails.
- Tests dekken validatie.

## Uitvoering
- Multi-symbol dashboard helpers uitgebreid met presets, validatie, budget allocation, risk summary, next action en evidence export.
- Simple dashboard uitgebreid met watchlist opslaan/resetten, symbol validation guardrails, total demo quote budget, stop one symbol, risk limit summary, budget allocation en export multi-symbol evidence.
- Tests toegevoegd en uitgebreid voor multi-symbol helpers en dashboard markers.
- Validatie: python -m pytest tests/test_multi_symbol_demo.py tests/test_simple_demo_dashboard.py tests/test_roadmap_025_dashboard_browser_smoke.py -q -> 14 passed.
- Validatie: python -m pytest -q -> 222 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Validatie: dashboard-browser-smoke op http://127.0.0.1:8504 -> status ok.
- Live trading blijft disabled.
