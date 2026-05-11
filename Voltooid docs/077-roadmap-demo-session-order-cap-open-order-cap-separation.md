# Roadmap 077 - Demo Session Order Cap And Open Order Cap Separation

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Scheid het zichtbare open-order limiet van de maximale sessie-orders, zodat de bot niet te vroeg stopt.

## Nieuwe verbeteringen
1. `Max open orders per symbol` blijft dashboardinformatie.
2. Runtime `max_demo_orders_per_session` gebruikt max trades/session.
3. Voorkom dat open-order cap van 1-2 de hele runtime stopt.
4. Toon order cap duidelijker in risk summary.
5. Houd session cap conservatief.
6. Voeg regressietest toe via source markers.
7. Geen live-order enablement.

## Acceptatiecriteria
- Runtime create gebruikt niet meer direct `max_open_orders_per_symbol` als session order cap.
- Risk summary toont beide concepten duidelijk.

## Uitvoering
- Multi demo auto-stop opgelost door completed demo replay runtimes automatisch te vervangen zolang multi_demo_running actief blijft.
- Open-order cap gescheiden van max demo orders per session; session cap gebruikt nu max(10, max_trades).
- Candle chart verbeterd met chart focus symbol, visible candles slider en hogere chart height.
- Multi-symbol visual overview toegevoegd voor fills, open orders en equity per symbool.
- Tests uitgebreid voor anti-stop, chart markers en multi-symbol overview chart.
- Validatie: gerichte dashboard/multi-symbol tests -> 24 passed.
- Validatie: python -m pytest -q -> 224 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Validatie: dashboard-browser-smoke op http://127.0.0.1:8504 -> status ok.
- Live trading blijft disabled.
