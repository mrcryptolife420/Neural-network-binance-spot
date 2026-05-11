# Roadmap 078 - Readable Live Candle Chart

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Maak de live candle chart leesbaar wanneer de bot langer draait.

## Nieuwe verbeteringen
1. Toon standaard minder recente candles.
2. Voeg slider toe voor candle window.
3. Voeg symboolselector toe voor chart-focus.
4. Verhoog chart height.
5. Bereken zichtbare candles uit het gekozen symbool.
6. Houd open orders/signals/fills op hetzelfde symbool.
7. Voeg marker tests toe.

## Acceptatiecriteria
- Dashboard bevat chart focus symbol en candle window.
- Grafiek gebruikt het gekozen symbool en beperkt candles.

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
