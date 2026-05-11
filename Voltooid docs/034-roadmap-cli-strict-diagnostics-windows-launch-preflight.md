# Roadmap 034 - CLI Strict Diagnostics & Windows Launch Preflight

Status: Voltooid
Project: Neural network Binance spot
Datum: 2026-05-10

Volgt op:

- `Roadmap docs/030-roadmap-operator-recovery-diagnostics-support-bundle-state-hygiene.md`

## Doel

Maak diagnostics bruikbaar vanaf CLI en Windows one-click launch, zodat operators geen Python traceback hoeven te lezen.

## Scope

- `spot-bot diagnostics --json --strict`.
- `spot-bot support-bundle --json --output ...`.
- Launch evidence krijgt diagnostics summary.
- Strict mode faalt bij `warn` of `fail`.

## Acceptatiecriteria

- CLI werkt zonder Binance keys.
- Strict mode geeft non-zero bij waarschuwingen.
- Windows launcher blijft werken.
- Tests controleren CLI-output en exit codes.

## Definition of Done

- Code, tests en docs zijn toegevoegd.
- `python -m pytest` slaagt.
- Roadmap wordt na validatie naar `Voltooid docs/` verplaatst.

Validatie uitgevoerd: `python -m pytest`, `check-all`, diagnostics, support-bundle, rehearsal en security-scan.
