# Roadmap 071 - Per Symbol Demo Control Actions

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Maak het mogelijk om niet alleen alles te stoppen, maar ook een specifiek symbool uit de demo run te halen.

## Nieuwe verbeteringen
1. Toon actieve runtime-symbolen.
2. Voeg `Stop one symbol` invoer toe.
3. Stop en verwijder alleen de gekozen runtime.
4. Houd overige symbolen actief.
5. Toon status daarna in dezelfde tabel.
6. Voorkom errors bij onbekend symbool.
7. Houd alle acties demo-only.

## Acceptatiecriteria
- Dashboard bevat per-symbol stop controls.
- Helper blijft tolerant bij lege/unknown symbolen.

## Uitvoering
- Multi-symbol dashboard helpers uitgebreid met presets, validatie, budget allocation, risk summary, next action en evidence export.
- Simple dashboard uitgebreid met watchlist opslaan/resetten, symbol validation guardrails, total demo quote budget, stop one symbol, risk limit summary, budget allocation en export multi-symbol evidence.
- Tests toegevoegd en uitgebreid voor multi-symbol helpers en dashboard markers.
- Validatie: python -m pytest tests/test_multi_symbol_demo.py tests/test_simple_demo_dashboard.py tests/test_roadmap_025_dashboard_browser_smoke.py -q -> 14 passed.
- Validatie: python -m pytest -q -> 222 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Validatie: dashboard-browser-smoke op http://127.0.0.1:8504 -> status ok.
- Live trading blijft disabled.
