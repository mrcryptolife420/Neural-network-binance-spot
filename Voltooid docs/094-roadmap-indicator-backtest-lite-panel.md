# Roadmap 094 - Indicator Backtest Lite Panel

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Voeg een lichte indicator sanity check toe zonder zware researchflow.

## Nieuwe verbeteringen
1. Count BUY/SELL/HOLD per actieve symbolen.
2. Gemiddelde confidence.
3. Regime distributie.
4. Warning bij weinig candles.
5. Dashboard summary.
6. Helper tests.
7. Geen performance claims.

## Acceptatiecriteria
- Indicator sanity summary is zichtbaar.

## Uitvoering
- Indicator engine toegevoegd met EMA, RSI, ATR, MACD, Bollinger position, regime detectie en adaptive profiles.
- Indicator advisor toegevoegd met BUY/SELL/HOLD bias, confidence, reason, summary, allocation hints en evidence export.
- Simple dashboard uitgebreid met Adaptive Indicator Advisor, auto profile toggle, per-symbol indicator table, decision explanation en focused chart context.
- Dashboard blijft demo-only; risk engine blijft leidend en live trading blijft disabled.
- Tests toegevoegd voor indicator snapshots, profile keuze, summary, allocation hints, evidence export en dashboard markers.
- Validatie: gerichte indicator/dashboard tests -> 20 passed.
- Validatie: python -m pytest -q -> 228 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Validatie: dashboard-browser-smoke op http://127.0.0.1:8504 -> status ok.
