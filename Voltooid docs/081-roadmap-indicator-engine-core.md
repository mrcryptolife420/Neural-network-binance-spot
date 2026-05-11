# Roadmap 081 - Indicator Engine Core

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Voeg een lokale indicator-engine toe voor demo trading zonder live-order permissies.

## Nieuwe verbeteringen
1. EMA indicator.
2. RSI indicator.
3. ATR indicator.
4. MACD indicator.
5. Bollinger bands.
6. Indicator snapshot per symbool.
7. Tests voor berekeningen en no-live safety.

## Acceptatiecriteria
- Indicator engine werkt op bestaande `Candle` data.
- Geen API calls of live trading.

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
