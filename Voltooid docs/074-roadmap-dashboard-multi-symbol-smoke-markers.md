# Roadmap 074 - Dashboard Multi Symbol Smoke Markers

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Zorg dat browser smoke checks de nieuwe simpele multi-symbol flow kunnen herkennen.

## Nieuwe verbeteringen
1. Stabiele tekstmarker voor `Multi Crypto Demo Trading`.
2. Stabiele tekstmarker voor `Budget allocation`.
3. Stabiele tekstmarker voor `Risk limit summary`.
4. Stabiele tekstmarker voor `Export multi-symbol evidence`.
5. Stabiele tekstmarker voor `Multi crypto bot status`.
6. Behoud oude advanced markers voor bestaande smoke tests.
7. Geen Streamlit duplicate key regressies.

## Acceptatiecriteria
- Browser smoke blijft groen.
- Tests controleren markers.

## Uitvoering
- Multi-symbol dashboard helpers uitgebreid met presets, validatie, budget allocation, risk summary, next action en evidence export.
- Simple dashboard uitgebreid met watchlist opslaan/resetten, symbol validation guardrails, total demo quote budget, stop one symbol, risk limit summary, budget allocation en export multi-symbol evidence.
- Tests toegevoegd en uitgebreid voor multi-symbol helpers en dashboard markers.
- Validatie: python -m pytest tests/test_multi_symbol_demo.py tests/test_simple_demo_dashboard.py tests/test_roadmap_025_dashboard_browser_smoke.py -q -> 14 passed.
- Validatie: python -m pytest -q -> 222 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Validatie: dashboard-browser-smoke op http://127.0.0.1:8504 -> status ok.
- Live trading blijft disabled.
