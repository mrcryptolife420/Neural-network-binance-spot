# Roadmap 049 - Redaction Self-Test Security Evidence

Status: Voltooid
Project: Neural network Binance spot
Datum: 2026-05-10

## Doel

Voeg een lokale redaction self-test toe die bewijst dat bekende secret-vormen uit support/report output worden verwijderd.

## Scope

- Redaction self-test met Binance/OpenAI/token-like voorbeelden.
- CLI `redaction-self-test --json`.
- Evidence in operator local ops snapshot.

## Acceptatiecriteria

- Self-test status is `ok`.
- Ruwe secrets komen niet terug in output.
- Security scan blijft groen.

## Definition of Done

- Code, tests en docs zijn toegevoegd.
- Volledige validatie slaagt.
- Roadmap wordt naar `Voltooid docs/` verplaatst.

Validatie uitgevoerd: `python -m pytest`, `check-all`, local-ops CLI, rehearsal en security-scan.
