# Roadmap 056 - Artifact Catalog Filters, Staleness Groups & Type Summary

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  

## Doel

Maak de artifact catalog bruikbaarder met filters, typegroepen en staleness-overzicht.

## Nieuwe verbeteringen

1. Filter op categorie.
2. Filter op suffix/type.
3. `stale` vlag per artifact.
4. Type summary met counts.
5. Category summary met counts en bytes.
6. CLI flags `--category`, `--suffix`, `--stale-days`.
7. Tests voor filters en summaries.

## Acceptatiecriteria

- Catalog output bevat `summaries`.
- Filters werken zonder crash op lege data.
- Roadmap wordt na validatie naar `Voltooid docs/` verplaatst.
## Uitvoering
- Geimplementeerd in operator local-ops backend, CLI en dashboard waar relevant.
- Nieuwe tests toegevoegd voor roadmap 055 t/m 064.
- Validatie: python -m pytest tests/test_roadmaps_055_064_operator_local_ops.py -q -> 10 passed.
- Validatie: python -m pytest -q -> 212 passed, 1 warning.
- Validatie: python -m binance_spot_bot.cli check-all --json -> status ok.
- Live trading blijft disabled; restore previews zijn non-destructief.

