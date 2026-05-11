# Roadmap 035 - Rehearsal Scorecard Diagnostics Gate Integration

Status: Voltooid
Project: Neural network Binance spot
Datum: 2026-05-10

Volgt op:

- `Roadmap docs/028-roadmap-one-click-demo-acceptance-rehearsal-evidence-trends.md`
- `Roadmap docs/030-roadmap-operator-recovery-diagnostics-support-bundle-state-hygiene.md`

## Doel

Maak diagnostics onderdeel van de Demo Acceptance Rehearsal en Evidence Scorecard, zodat operator-state problemen automatisch zichtbaar zijn in acceptatie-evidence.

## Scope

- Rehearsal step `operator-diagnostics`.
- Diagnostics artifact `data/evidence/diagnostics/latest-diagnostics.json`.
- Scorecard waarschuwing/blokkade op basis van diagnostics status.

## Acceptatiecriteria

- Rehearsal schrijft diagnostics artifact.
- Scorecard leest diagnostics artifact.
- Diagnostics mag geen circular crash veroorzaken als scorecard ontbreekt.
- Tests dekken integratie.

## Definition of Done

- Code, tests en docs zijn toegevoegd.
- `python -m pytest` slaagt.
- Roadmap wordt na validatie naar `Voltooid docs/` verplaatst.

Validatie uitgevoerd: `python -m pytest`, `check-all`, diagnostics, rehearsal en security-scan.
