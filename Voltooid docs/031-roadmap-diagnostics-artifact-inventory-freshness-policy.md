# Roadmap 031 - Diagnostics Artifact Inventory & Freshness Policy

Status: Voltooid
Project: Neural network Binance spot
Datum: 2026-05-10

Volgt op:

- `Roadmap docs/030-roadmap-operator-recovery-diagnostics-support-bundle-state-hygiene.md`

## Doel

Breid de diagnostics-laag uit met een centrale artifact inventory die laat zien welke evidence bestaat, hoe oud die is, of JSON geldig is en of het item kritisch is voor demo-acceptatie.

## Scope

- Artifact inventory voor `check-all`, launch evidence, browser smoke, operator evidence, demo execution, pilot start idempotency, scorecard en rehearsal.
- Freshness policy met `fresh`, `stale`, `missing`, `invalid_json`.
- Geen nieuwe scorecard of rehearsal dupliceren.

## Acceptatiecriteria

- Diagnostics output bevat `artifact_inventory`.
- Lege data-map geeft warnings, geen crash.
- Corrupte JSON geeft `invalid_json`.
- Tests dekken missing/fresh/stale/invalid artifacts.

## Definition of Done

- Code, tests en docs zijn toegevoegd.
- `python -m pytest` slaagt.
- Roadmap wordt na validatie naar `Voltooid docs/` verplaatst.

Validatie uitgevoerd: `python -m pytest`, `check-all`, diagnostics, rehearsal en security-scan.
