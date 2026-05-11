# Roadmap 041 - Local Operator Report HTML & Markdown Export

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-10  

## Doel

Maak één lokaal operatorrapport dat diagnostics, artifact inventory, timeline, scorecard en rehearsal samenvat.

## Scope

- Markdown rapport.
- Simpel HTML rapport zonder externe dependencies.
- CLI `operator-report`.
- Dashboard exportknop.

## Acceptatiecriteria

- Rapport schrijft naar `data/reports/operator/`.
- Rapport bevat live disabled status.
- Rapport bevat geen secrets.

## Definition of Done

- Code, tests en docs zijn toegevoegd.
- Volledige validatie slaagt.
- Roadmap wordt naar `Voltooid docs/` verplaatst.

Validatie uitgevoerd: `python -m pytest`, `check-all`, support-bundle verify, operator-report, quality-gate, rehearsal en security-scan.
