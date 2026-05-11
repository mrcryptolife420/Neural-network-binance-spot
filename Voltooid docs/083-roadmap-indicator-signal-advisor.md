# Roadmap 083 - Indicator Signal Advisor

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Voeg een indicator advisor toe die BUY/SELL/HOLD bias geeft naast het NN-signaal.

## Nieuwe verbeteringen
1. Indicator bias.
2. Confidence score.
3. Human-readable reason.
4. RSI overbought/oversold checks.
5. EMA trend checks.
6. MACD confirmation.
7. Houd risk engine leidend.

## Acceptatiecriteria
- Advisor beÃ¯nvloedt geen live orders.
- Dashboard toont advies per symbool.

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
