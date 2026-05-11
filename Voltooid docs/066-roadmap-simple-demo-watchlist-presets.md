# Roadmap 066 - Simple Demo Watchlist Presets

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Maak multi-crypto demo trading eenvoudiger door een duidelijke watchlist preset flow in het simpele dashboard.

## Nieuwe verbeteringen
1. Toon standaard demo-symbol presets.
2. Laat extra symbolen toevoegen via vrije invoer.
3. Normaliseer korte basenames zoals `ETH` naar `ETHUSDT`.
4. Dedupliceer symbolen automatisch.
5. Respecteer `Max active symbols`.
6. Voeg een knop toe om de actieve watchlist lokaal op te slaan.
7. Houd live trading disabled.

## Acceptatiecriteria
- Simple dashboard toont watchlist controls.
- Opslaan van de watchlist schrijft geen secrets.
- Tests dekken normalisatie, deduplicatie en limieten.

## Uitvoering
- Multi-symbol dashboard helpers uitgebreid met presets, validatie, budget allocation, risk summary, next action en evidence export.
- Simple dashboard uitgebreid met watchlist opslaan/resetten, symbol validation guardrails, total demo quote budget, stop one symbol, risk limit summary, budget allocation en export multi-symbol evidence.
- Tests toegevoegd en uitgebreid voor multi-symbol helpers en dashboard markers.
- Validatie: python -m pytest tests/test_multi_symbol_demo.py tests/test_simple_demo_dashboard.py tests/test_roadmap_025_dashboard_browser_smoke.py -q -> 14 passed.
- Validatie: python -m pytest -q -> 222 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Validatie: dashboard-browser-smoke op http://127.0.0.1:8504 -> status ok.
- Live trading blijft disabled.
