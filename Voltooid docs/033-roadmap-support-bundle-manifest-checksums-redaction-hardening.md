# Roadmap 033 - Support Bundle Manifest Checksums & Redaction Hardening

Status: Voltooid
Project: Neural network Binance spot
Datum: 2026-05-10

Volgt op:

- `Roadmap docs/030-roadmap-operator-recovery-diagnostics-support-bundle-state-hygiene.md`

## Doel

Maak support bundles bruikbaar voor debugging en veilig genoeg om lokaal te delen: manifest, checksums, redaction summary en alleen toegestane artifacts.

## Scope

- Support bundle met diagnostics, preflight, scorecard, rehearsal, check-all, launch evidence, browser smoke, pilot idempotency en sanitized settings.
- Manifest met bestandslijst, size bytes, sha256 en redaction status.
- Geen `.env`, geen raw keys, geen secrets.

## Acceptatiecriteria

- Bundle bevat `manifest.json`.
- Bundle bevat checksums.
- Secret scan op bundle output heeft geen findings.
- Tests controleren redactie en manifest.

## Definition of Done

- Code, tests en docs zijn toegevoegd.
- `python -m pytest` slaagt.
- Roadmap wordt na validatie naar `Voltooid docs/` verplaatst.

Validatie uitgevoerd: `python -m pytest`, `check-all`, diagnostics, support-bundle, rehearsal en security-scan.
