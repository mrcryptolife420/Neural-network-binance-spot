# Correctie-audit Roadmaps 082-122

Datum: 2026-05-11

## Conclusie

De roadmaps `082-122` zijn opnieuw uit `Voltooid docs/` teruggezet naar `Roadmap docs/`.

Reden: de vorige uitvoering heeft veel lokale modules, façade-functies, safety-surfaces en smoke-tests aangemaakt, maar dat is niet hetzelfde als alle roadmapfeatures volledig bouwen. Veel roadmaps vragen production-grade workflows zoals Dashboard V2, FastAPI/WebSocket/React UI, live-session governance, packaging, rollback, model monitoring, experiment orchestration en operator workflows. Die zijn niet volledig end-to-end geïmplementeerd.

## Wat wel is gebouwd

- Lokale helpermodules en safety facades voor de genoemde domeinen.
- Tests die basisgedrag en no-live invariants controleren.
- Dashboard registry uitbreidingen en smoke-test compatibiliteit.
- Documenten die de bedoelde safety-contracten samenvatten.

## Wat niet voldoende is voor "Voltooid"

- Geen echte Dashboard V2 React/FastAPI/WebSocket applicatie met feature parity.
- Geen volledige production-grade release/installer/cutover flow.
- Geen volledige modelops/training/monitoring pipeline met echte experiment tracking.
- Geen volledige live trading lifecycle; alleen niet-submittende safety stubs.
- Geen volledige evidence/approval/governance workflows per roadmapchecklist.
- Geen volledige UX/browser parity-validatie per nieuwe V2 workflow.

## Nieuwe regel

Een roadmap mag pas terug naar `Voltooid docs/` als:

- de hoofdfeature end-to-end werkt;
- er geen placeholder/facade als primaire implementatie overblijft;
- acceptatiecriteria uit de roadmap aantoonbaar zijn afgedekt;
- gerichte tests plus volledige pytest/check-all groen zijn;
- bij UI-roadmaps een relevante browser/dashboard smoke is uitgevoerd;
- bij live-roadmaps expliciet is bewezen dat geen echte order kan worden geplaatst zonder alle vereiste gates.

## Status

`Roadmap docs/` bevat weer de open roadmaps `082-122`. Deze moeten opnieuw één voor één worden uitgevoerd, in kleinere realistische batches.
