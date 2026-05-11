# Roadmap 047 - Operator Report Index Compare History

Status: Voltooid
Project: Neural network Binance spot
Datum: 2026-05-10

## Doel

Maak lokale operatorrapporten vindbaar en vergelijkbaar via een report index.

## Scope

- Index van Markdown/HTML operator reports.
- Laatste rapport vergelijken met vorige.
- CLI `report-index --json`.

## Acceptatiecriteria

- Werkt zonder rapporten.
- Rapportindex bevat grootte en leeftijd.
- Geen secrets in output.

## Definition of Done

- Code, tests en docs zijn toegevoegd.
- Volledige validatie slaagt.
- Roadmap wordt naar `Voltooid docs/` verplaatst.

Validatie uitgevoerd: `python -m pytest`, `check-all`, local-ops CLI, rehearsal en security-scan.
