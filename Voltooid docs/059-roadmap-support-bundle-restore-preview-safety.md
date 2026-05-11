# Roadmap 059 - Support Bundle Restore Preview Safety

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

## Doel

Maak support bundle restore veilig preview-only, zodat een operator kan zien wat in een bundle zit zonder bestanden terug te schrijven.

## Nieuwe verbeteringen

1. Restore preview uit bundle manifest.
2. Geen extract naar workspace.
3. Bestandstype summary.
4. Redaction status summary.
5. CLI `support-bundle-restore-preview --bundle ... --json`.
6. Fail state bij ontbrekende manifest.
7. Tests voor geldige en ontbrekende bundle.

## Acceptatiecriteria

- Preview schrijft niets terug.
- Geen secrets in output.
- Roadmap wordt na validatie naar `Voltooid docs/` verplaatst.
## Uitvoering
- Geimplementeerd in operator local-ops backend, CLI en dashboard waar relevant.
- Nieuwe tests toegevoegd voor roadmap 055 t/m 064.
- Validatie: python -m pytest tests/test_roadmaps_055_064_operator_local_ops.py -q -> 10 passed.
- Validatie: python -m pytest -q -> 212 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Live trading blijft disabled; restore previews zijn non-destructief.

