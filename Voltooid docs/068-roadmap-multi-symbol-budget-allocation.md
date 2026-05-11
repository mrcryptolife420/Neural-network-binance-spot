# Roadmap 068 - Multi Symbol Budget Allocation

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Maak zichtbaar hoeveel demo quote budget per crypto gebruikt mag worden.

## Nieuwe verbeteringen
1. Voeg totaal demo quote budget input toe.
2. Bereken budget per actief symbool.
3. Toon default quote size per order.
4. Toon max positie per symbool.
5. Waarschuw wanneer default order size boven symbol budget ligt.
6. Toon budgettabel in simple dashboard.
7. Houd het paper/demo-only.

## Acceptatiecriteria
- Budgetplan werkt voor 1 of meerdere symbolen.
- Dashboard toont budget allocation.
- Tests dekken budgetverdeling.

## Uitvoering
- Multi-symbol dashboard helpers uitgebreid met presets, validatie, budget allocation, risk summary, next action en evidence export.
- Simple dashboard uitgebreid met watchlist opslaan/resetten, symbol validation guardrails, total demo quote budget, stop one symbol, risk limit summary, budget allocation en export multi-symbol evidence.
- Tests toegevoegd en uitgebreid voor multi-symbol helpers en dashboard markers.
- Validatie: python -m pytest tests/test_multi_symbol_demo.py tests/test_simple_demo_dashboard.py tests/test_roadmap_025_dashboard_browser_smoke.py -q -> 14 passed.
- Validatie: python -m pytest -q -> 222 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Validatie: dashboard-browser-smoke op http://127.0.0.1:8504 -> status ok.
- Live trading blijft disabled.
