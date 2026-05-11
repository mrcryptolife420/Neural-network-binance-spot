# Roadmap 086 - Indicator Chart Context

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Maak de candle chart begrijpelijker met indicatorcontext.

## Nieuwe verbeteringen
1. Chart focus symbol gebruikt indicator snapshot.
2. Toon chart context naast grafiek.
3. Toon focused RSI.
4. Toon focused regime.
5. Toon focused bias.
6. Toon focused reason.
7. Houd grafiek compact.

## Acceptatiecriteria
- Chart focus toont indicatorcontext.

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
