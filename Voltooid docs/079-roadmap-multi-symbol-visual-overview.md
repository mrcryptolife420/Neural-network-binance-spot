# Roadmap 079 - Multi Symbol Visual Overview

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

Voeg naast candles een eenvoudige multi-symbol overzichtsgrafiek toe.

## Nieuwe verbeteringen
1. Visualiseer fills per symbool.
2. Visualiseer open orders per symbool.
3. Visualiseer equity per symbool.
4. Gebruik compacte bar chart.
5. Toon deze boven de candle chart.
6. Maak helper testbaar.
7. Geen externe data nodig.

## Acceptatiecriteria
- Dashboard toont multi-symbol visual overview.
- Chart helper importeert zonder Streamlit.

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
