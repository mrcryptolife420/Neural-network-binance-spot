# Roadmap 072 - Multi Symbol Aggregate Status

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Verbeter de overzichtelijkheid met Ã©Ã©n aggregate statusblok voor alle gekozen demo-symbolen.

## Nieuwe verbeteringen
1. Tel actieve bots.
2. Tel totale fills.
3. Tel totale open orders.
4. Tel symbolen per runtime status.
5. Toon totaal equity waar beschikbaar.
6. Toon next operator action.
7. Maak summary testbaar als pure helper.

## Acceptatiecriteria
- Summary helper werkt zonder Streamlit.
- Dashboard badges gebruiken summary.

## Uitvoering
- Multi-symbol dashboard helpers uitgebreid met presets, validatie, budget allocation, risk summary, next action en evidence export.
- Simple dashboard uitgebreid met watchlist opslaan/resetten, symbol validation guardrails, total demo quote budget, stop one symbol, risk limit summary, budget allocation en export multi-symbol evidence.
- Tests toegevoegd en uitgebreid voor multi-symbol helpers en dashboard markers.
- Validatie: python -m pytest tests/test_multi_symbol_demo.py tests/test_simple_demo_dashboard.py tests/test_roadmap_025_dashboard_browser_smoke.py -q -> 14 passed.
- Validatie: python -m pytest -q -> 222 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Validatie: dashboard-browser-smoke op http://127.0.0.1:8504 -> status ok.
- Live trading blijft disabled.
