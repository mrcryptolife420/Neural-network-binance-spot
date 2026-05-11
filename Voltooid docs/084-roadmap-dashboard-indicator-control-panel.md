# Roadmap 084 - Dashboard Indicator Control Panel

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Maak indicatorinstellingen zichtbaar in de simpele dashboardmodus.

## Nieuwe verbeteringen
1. Indicator profile selectbox.
2. Auto profile toggle.
3. Indicator helptekst.
4. Live status panel integratie.
5. Profiel zichtbaar in badges.
6. Geen advanced tab nodig.
7. Geen secrets in instellingen.

## Acceptatiecriteria
- Simple dashboard bevat indicator controls.

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
