# Roadmap 048 - Support Bundle Verification Matrix

Status: Voltooid
Project: Neural network Binance spot
Datum: 2026-05-10

## Doel

Verifieer alle lokale support bundles in één matrix zodat operators zien welke bundles geldig zijn.

## Scope

- Scan `data/support/*.zip`.
- Per bundle: status, errors, file count.
- CLI `support-bundles-verify --json`.

## Acceptatiecriteria

- Werkt zonder bundles.
- Geldige bundle geeft `ok`.
- Foutieve bundle geeft `fail`.

## Definition of Done

- Code, tests en docs zijn toegevoegd.
- Volledige validatie slaagt.
- Roadmap wordt naar `Voltooid docs/` verplaatst.

Validatie uitgevoerd: `python -m pytest`, `check-all`, local-ops CLI, rehearsal en security-scan.
