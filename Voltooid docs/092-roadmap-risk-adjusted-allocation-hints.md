# Roadmap 092 - Risk Adjusted Allocation Hints

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Geef veilige demo allocation hints op basis van indicator confidence.

## Nieuwe verbeteringen
1. Allocation hint per symbool.
2. Confidence weging.
3. HOLD krijgt lage allocation.
4. High volatility reduceert allocation.
5. Totaal budget blijft begrensd.
6. Dashboardtabel.
7. Geen echte order sizing override.

## Acceptatiecriteria
- Allocation hints zijn informatief en demo-only.

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
