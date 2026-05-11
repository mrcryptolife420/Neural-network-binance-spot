# Roadmap 063 - Data Growth Budget Forecast

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

## Doel

Maak lokale datagroei zichtbaar zodat support bundles, reports en evidence niet onbeheersbaar groeien.

## Nieuwe verbeteringen

1. Data growth summary per root.
2. Budget thresholds.
3. Forecast op basis van huidige grootte.
4. Largest files overzicht.
5. CLI `data-growth-budget --json`.
6. Dashboard tabel.
7. Tests met tijdelijke bestanden.

## Acceptatiecriteria

- Output bevat `total_size_bytes`.
- Geen delete-acties.
- Roadmap wordt naar `Voltooid docs/` verplaatst.
## Uitvoering
- Geimplementeerd in operator local-ops backend, CLI en dashboard waar relevant.
- Nieuwe tests toegevoegd voor roadmap 055 t/m 064.
- Validatie: python -m pytest tests/test_roadmaps_055_064_operator_local_ops.py -q -> 10 passed.
- Validatie: python -m pytest -q -> 212 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Live trading blijft disabled; restore previews zijn non-destructief.

