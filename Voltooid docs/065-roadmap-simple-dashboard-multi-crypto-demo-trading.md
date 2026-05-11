# Roadmap 065 - Simple Dashboard Multi Crypto Demo Trading

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Breid de simpele dashboardmodus uit zodat demo trading niet beperkt blijft tot `BTCUSDT`, maar meerdere gekozen crypto-symbolen veilig naast elkaar kan draaien op Binance Demo Spot.

## Nieuwe verbeteringen
1. Multi-symbol watchlist in simple dashboard met presets en vrije invoer.
2. Limiet `x aantal symbols traden` zodat de operator bewust 1-10 markten kiest.
3. Per symbool een bestaande `BotRuntime`, zodat data, risk checks, orders en sessies gescheiden blijven.
4. Gezamenlijke start/stop voor geselecteerde demo-symbolen.
5. Overzichtstabel met status, signaal, risk decision, fills, open demo orders en equity per symbool.
6. Totale multi-symbol samenvatting met aantal actieve bots, fills en open orders.
7. Safety guardrails: alleen Binance Demo Spot, demo keys vereist, live trading disabled, max open orders per symbool zichtbaar.

## Acceptatiecriteria
- De simpele dashboardmodus bevat multi-crypto controls.
- De gebruiker kan symbolen kiezen of invoeren en een maximum aantal actieve symbolen instellen.
- Er kunnen meerdere demo-runtimes naast elkaar worden gestart zonder de single-symbol advanced tools te dupliceren.
- Dashboard toont per symbool status en open orders.
- Tests bevestigen parser, selectie, UI-markers en no-live safety.
- `python -m pytest -q` en `check-all` blijven groen.
- Roadmap wordt na validatie naar `Voltooid docs/` verplaatst.

## Uitvoering
- Multi-symbol helper toegevoegd voor normalisatie, deduplicatie en max-active selectie.
- Simple dashboard uitgebreid met multi-crypto watchlist, extra symbols, max active symbols en max open orders per symbol.
- Per gekozen symbool wordt een bestaande demo-runtime gebruikt; geen live trading en geen duplicatie van core execution.
- Dashboard toont multi crypto bot status, total fills, open orders en per-symbol signal/risk/status.
- Tests toegevoegd voor parser en simple dashboard markers.
- Validatie: python -m pytest tests/test_multi_symbol_demo.py tests/test_simple_demo_dashboard.py tests/test_roadmap_025_dashboard_browser_smoke.py -q -> 9 passed.
- Validatie: python -m pytest -q -> 217 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Validatie: dashboard-browser-smoke op http://127.0.0.1:8504 -> status ok.
