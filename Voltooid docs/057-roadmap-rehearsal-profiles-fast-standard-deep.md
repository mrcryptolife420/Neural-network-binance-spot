# Roadmap 057 - Rehearsal Profiles Fast Standard Deep

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

## Doel

Maak lokale rehearsal runs profileerbaar zodat operators sneller kunnen kiezen tussen snelle checks en diepe acceptatie.

## Nieuwe verbeteringen

1. Profile manifest voor `fast`, `standard`, `deep`.
2. CLI `rehearsal-profiles --json`.
3. Profile recommended duration en use case.
4. Profile step list uit bestaande rehearsal stappen.
5. Dashboard command manifest neemt profiles op.
6. Docs voor wanneer welk profiel te gebruiken.
7. Tests voor profile schema.

## Acceptatiecriteria

- Geen nieuwe rehearsal-engine dupliceren.
- Profiles zijn metadata bovenop bestaande rehearsal.
- Roadmap wordt na validatie naar `Voltooid docs/` verplaatst.
## Uitvoering
- Geimplementeerd in operator local-ops backend, CLI en dashboard waar relevant.
- Nieuwe tests toegevoegd voor roadmap 055 t/m 064.
- Validatie: python -m pytest tests/test_roadmaps_055_064_operator_local_ops.py -q -> 10 passed.
- Validatie: python -m pytest -q -> 212 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Live trading blijft disabled; restore previews zijn non-destructief.

