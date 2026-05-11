# Roadmap 076 - Multi Demo Runner Does Not Stop On Replay End

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Voorkom dat de multi-symbol demo bot vanzelf stopt wanneer de lokale demo replay-candles op zijn.

## Nieuwe verbeteringen
1. Detecteer `completed` runtimes in multi-symbol demo mode.
2. Herstart alleen completed demo-runtimes automatisch.
3. Stop niet automatisch bij normale replay-end zolang de operator `multi_demo_running` actief laat.
4. Houd echte `stopped` states zichtbaar voor operatoractie.
5. Toon restart/cycle count per symbool.
6. Houd alle acties demo-only.
7. Voeg tests toe voor anti-stop markers.

## Acceptatiecriteria
- Multi demo running blijft actief na replay-end.
- Completed runtimes worden vervangen door een nieuwe demo-runtime.
- Live trading blijft disabled.

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
