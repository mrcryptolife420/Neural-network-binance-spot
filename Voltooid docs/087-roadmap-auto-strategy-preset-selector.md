# Roadmap 087 - Auto Strategy Preset Selector

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Laat dashboard per marktregime een indicatorprofiel voorstellen.

## Nieuwe verbeteringen
1. Trend regime kiest trend profiel.
2. High volatility kiest volatility profiel.
3. Range kiest range profiel.
4. Momentum kiest momentum profiel.
5. Auto profile blijft explainable.
6. Tabel toont chosen profile.
7. Tests voor profielkeuze.

## Acceptatiecriteria
- Auto selector is deterministic.

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
