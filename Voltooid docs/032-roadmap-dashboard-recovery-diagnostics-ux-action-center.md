# Roadmap 032 - Dashboard Recovery Diagnostics UX Action Center

Status: Voltooid
Project: Neural network Binance spot
Datum: 2026-05-10

Volgt op:

- `Roadmap docs/030-roadmap-operator-recovery-diagnostics-support-bundle-state-hygiene.md`
- `Roadmap docs/031-roadmap-diagnostics-artifact-inventory-freshness-policy.md`

## Doel

Maak diagnostics zichtbaar in het lokale dashboard als operator action center, zonder bestaande Demo Pilot, Readiness of Logs/Security functies dubbel te bouwen.

## Scope

- Dashboardsectie `Recovery & Diagnostics`.
- Badges voor overall health, pilot run, runner lock, scorecard, rehearsal en live status.
- Tabellen voor blockers, warnings, recommended actions en artifact inventory.
- Knoppen voor refresh diagnostics, run rehearsal en export support bundle.

## Acceptatiecriteria

- Dashboard bevat `Recovery & Diagnostics`.
- UI crasht niet bij lege/corrupte artifacts.
- Start/stop pilot blijft in de bestaande Demo Pilot sectie.
- Tests controleren dashboardmarkers.

## Definition of Done

- Code, tests en docs zijn toegevoegd.
- `python -m pytest` slaagt.
- Roadmap wordt na validatie naar `Voltooid docs/` verplaatst.

Validatie uitgevoerd: `python -m pytest`, `check-all`, diagnostics, rehearsal en security-scan.
