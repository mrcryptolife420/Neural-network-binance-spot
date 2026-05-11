# Roadmap 089 - Indicator Evidence Export

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Exporteer indicatoradvies voor latere analyse.

## Nieuwe verbeteringen
1. JSON export onder `data/evidence/indicators`.
2. Rows per symbool.
3. Profielinstelling.
4. Auto-profile status.
5. Redacted payload.
6. Timestamp.
7. Live trading disabled.

## Acceptatiecriteria
- Export schrijft bestand zonder secrets.

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
