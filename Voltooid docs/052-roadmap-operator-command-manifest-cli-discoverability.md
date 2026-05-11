# Roadmap 052 - Operator Command Manifest CLI Discoverability

Status: Voltooid
Project: Neural network Binance spot
Datum: 2026-05-10

## Doel

Maak een command manifest voor veilige operatorcommands zodat de gebruiker weet welke CLI-acties beschikbaar zijn.

## Scope

- Manifest met diagnostics/report/support/rehearsal commands.
- CLI `operator-command-manifest --json`.
- Dashboard kan manifest tonen.

## Acceptatiecriteria

- Manifest bevat geen live trading command.
- Manifest bevat `demo-acceptance-rehearsal`.
- Tests dekken command safety.

## Definition of Done

- Code, tests en docs zijn toegevoegd.
- Volledige validatie slaagt.
- Roadmap wordt naar `Voltooid docs/` verplaatst.

Validatie uitgevoerd: `python -m pytest`, `check-all`, local-ops CLI, rehearsal en security-scan.
