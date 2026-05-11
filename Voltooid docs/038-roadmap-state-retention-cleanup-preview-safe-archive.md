# Roadmap 038 - State Retention Cleanup Preview & Safe Archive

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-10  

## Doel

Maak lokale data-hygiëne zichtbaar zonder bewijs te verliezen: preview welke generated artifacts oud zijn en archiveer alleen expliciet.

## Scope

- Retention preview voor checks, evidence, support bundles, sessions en pilot-runs.
- Geen automatische delete.
- Archive manifest met redaction en checksums.

## Acceptatiecriteria

- Preview werkt zonder data-map.
- Archive schrijft manifest.
- Geen secrets in archive.
- Dashboard toont retention preview.

## Definition of Done

- Code, tests en docs zijn toegevoegd.
- Volledige validatie slaagt.
- Roadmap wordt naar `Voltooid docs/` verplaatst.

Validatie uitgevoerd: `python -m pytest`, `check-all`, support-bundle verify, operator-report, quality-gate, rehearsal en security-scan.
