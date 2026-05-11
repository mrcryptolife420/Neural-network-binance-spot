# Roadmap 069 - Multi Symbol Risk Limit Summary

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Maak risk limits voor multi-symbol demo trading zichtbaar zonder advanced tabs te openen.

## Nieuwe verbeteringen
1. Toon max trades per symbol.
2. Toon max open orders per symbol.
3. Toon max position quote per symbol.
4. Toon max daily loss quote.
5. Toon max spread bps.
6. Toon min signal confidence.
7. Toon live trading disabled als permanente guardrail.

## Acceptatiecriteria
- Dashboard bevat risk limit summary.
- Tests dekken risk rows helper.

## Uitvoering
- Multi-symbol dashboard helpers uitgebreid met presets, validatie, budget allocation, risk summary, next action en evidence export.
- Simple dashboard uitgebreid met watchlist opslaan/resetten, symbol validation guardrails, total demo quote budget, stop one symbol, risk limit summary, budget allocation en export multi-symbol evidence.
- Tests toegevoegd en uitgebreid voor multi-symbol helpers en dashboard markers.
- Validatie: python -m pytest tests/test_multi_symbol_demo.py tests/test_simple_demo_dashboard.py tests/test_roadmap_025_dashboard_browser_smoke.py -q -> 14 passed.
- Validatie: python -m pytest -q -> 222 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Validatie: dashboard-browser-smoke op http://127.0.0.1:8504 -> status ok.
- Live trading blijft disabled.
