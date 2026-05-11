# Roadmap 061 - Dashboard Command Palette for Local Ops

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

## Doel

Maak de veilige operatorcommands beter vindbaar in het dashboard.

## Nieuwe verbeteringen

1. Dashboard label `Local Ops Command Palette`.
2. Tabel met veilige commands.
3. Kolom voor live trading `false`.
4. Kolom voor use case.
5. Link naar docs.
6. Geen execute-knoppen voor gevaarlijke acties.
7. Tests voor dashboardmarkers.

## Acceptatiecriteria

- Dashboard bevat command palette markers.
- Geen live command in manifest.
- Roadmap wordt na validatie naar `Voltooid docs/` verplaatst.
## Uitvoering
- Geimplementeerd in operator local-ops backend, CLI en dashboard waar relevant.
- Nieuwe tests toegevoegd voor roadmap 055 t/m 064.
- Validatie: python -m pytest tests/test_roadmaps_055_064_operator_local_ops.py -q -> 10 passed.
- Validatie: python -m pytest -q -> 212 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Live trading blijft disabled; restore previews zijn non-destructief.

