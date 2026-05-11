# Roadmap 073 - Simple Dashboard Next Action Guidance

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Maak het dashboard minder verwarrend met duidelijke operator guidance per toestand.

## Nieuwe verbeteringen
1. Next action voor ontbrekende keys.
2. Next action voor connection test.
3. Next action voor connect demo trading.
4. Next action voor symbol validation blockers.
5. Next action voor start selected symbols.
6. Next action voor running bots.
7. Korte helptekst in expander.

## Acceptatiecriteria
- Helper geeft voorspelbare next action.
- Dashboard toont eenvoudige help.

## Uitvoering
- Multi-symbol dashboard helpers uitgebreid met presets, validatie, budget allocation, risk summary, next action en evidence export.
- Simple dashboard uitgebreid met watchlist opslaan/resetten, symbol validation guardrails, total demo quote budget, stop one symbol, risk limit summary, budget allocation en export multi-symbol evidence.
- Tests toegevoegd en uitgebreid voor multi-symbol helpers en dashboard markers.
- Validatie: python -m pytest tests/test_multi_symbol_demo.py tests/test_simple_demo_dashboard.py tests/test_roadmap_025_dashboard_browser_smoke.py -q -> 14 passed.
- Validatie: python -m pytest -q -> 222 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Validatie: dashboard-browser-smoke op http://127.0.0.1:8504 -> status ok.
- Live trading blijft disabled.
