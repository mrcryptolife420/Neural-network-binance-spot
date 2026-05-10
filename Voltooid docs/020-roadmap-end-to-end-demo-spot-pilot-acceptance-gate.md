# Roadmap 020: End-to-End Demo Spot Pilot Acceptance Gate

## Status

Voltooid.

Deze roadmap bouwt direct voort op roadmaps 001 t/m 019. De bot heeft nu een lokale Windows one-click start, Binance Demo Spot connect/arm flow, deterministic risk engine, order lifecycle tracking, reconciliation, clean-start checks, account sync, demo pilot presets, operator dashboard, chart markers en redacted pilot reports.

De volgende beste stap is niet een nieuwe strategie of extra tradinglogica, maar een harde end-to-end acceptatielaag:

**Kan de operator lokaal veilig een Binance Demo Spot pilot starten, volgen, stoppen, herstellen en bewijzen dat alles correct werkte?**

Live trading blijft buiten scope en disabled.

## Waarom deze roadmap nu nodig is

Roadmap 019 maakte de operatorervaring begrijpelijker. De resterende zwakte is dat de pilot nog te veel bestaat uit losse runtime-acties:

- credentials laden;
- connectie testen;
- clean-start checken;
- arm/disarm;
- runtime starten;
- handmatig reconciliëren;
- stop/cancel/export;
- rapport controleren.

Voor echte demo-pilot betrouwbaarheid moet dit één gecontroleerde flow worden met duidelijke states, automatische preflight, periodieke reconciliation, crash/resume herkenning en een acceptatierapport dat bewijst wat er gebeurd is.

## Doel

Maak een centrale Demo Spot Pilot Acceptance Gate die:

1. Preflight uitvoert.
2. Alleen start als alle blockers opgelost zijn.
3. De pilot als state machine beheert.
4. Periodiek account sync en reconciliation uitvoert.
5. Stop/cancel/reconcile/export als één veilige stop-flow uitvoert.
6. Pilot-run checkpoints bewaart.
7. Na crash/sluiten herstelbaar en verklaarbaar is.
8. Een acceptatiebundel exporteert.

## In Scope

- End-to-end Demo Spot pilot orchestration.
- Pilot state machine.
- Pilot-run persistence.
- Start/stop acceptance gates.
- Periodieke reconciliation/account sync.
- Crash/resume detection.
- Dashboard pilot wizard bovenop bestaande Demo Pilot tab.
- Acceptance report bundle.
- Tests voor start, block, stop, resume en report.
- `check-all` integratie.

## Niet In Scope

- Binance live trading.
- Futures/margin.
- Nieuwe exchange-integraties.
- Nieuwe ML-strategie.
- RL.
- Autonome LLM-orders.
- Secrets opslaan in repo/logs/reports.
- Risk engine omzeilen.

## Niet Opnieuw Bouwen

Gebruik en breid bestaande infrastructuur uit:

- `demo_pilot.py`
- `demo_spot.py`
- `runtime.py`
- `order_lifecycle.py`
- `session_report.py`
- `ui/streamlit_app.py`
- `ui/components.py`
- `ui/charts.py`
- `control_center.py`
- `connectivity.py`
- `readiness.py`
- `check_all.py`

Nieuwe code moet klein en gericht zijn. Als orchestration apart nodig is, maak een dunne laag bovenop bestaande componenten, geen tweede runtime.

## Architectuurkeuze

Voeg een centrale orchestrator toe:

- `DemoPilotOrchestrator`
  - berekent start readiness;
  - beheert pilot state transitions;
  - roept bestaande runtime/reconciliation/account sync aan;
  - voert veilige stop-flow uit;
  - produceert operator actions en blockers.

Voeg persistente run-state toe:

- `PilotRunStore`
  - schrijft naar `data/pilot-runs/`;
  - bewaart run id, status, timestamps, profile, symbol, preset, blockers, checkpoints;
  - bevat geen secrets;
  - ondersteunt resume detection.

Voeg acceptatie-output toe:

- `PilotAcceptanceReport`
  - vat preflight, orders, reconciliation, account before/after, alerts, stop-flow en acceptance criteria samen;
  - blijft redacted;
  - wordt gekoppeld aan bestaande session reports.

## Pilot State Machine

Minimale states:

- `idle`
- `checking`
- `blocked`
- `ready`
- `running`
- `paused`
- `stopping`
- `completed`
- `failed`
- `resume_required`

Regels:

- `running` mag alleen na `ready`.
- `ready` mag alleen als start gate groen is.
- `resume_required` blokkeert nieuwe start tot reconcile/cancel is uitgevoerd.
- `stopping` voert altijd stop-flow uit.
- `completed` vereist finale reconciliation en report export.
- Unknown/orphan orders blijven hard blockers.

## Start Acceptance Gate

Start mag alleen als:

- Exchange profile is `binance-demo-spot`.
- Base URL is Demo Spot.
- Live trading disabled is.
- Credentials zijn geladen voor huidige sessie.
- Signed account check werkt.
- Account `canTrade` is waar.
- Symbol filters zijn geladen.
- Risk limits zijn gezet.
- Pilot preset is gekozen.
- Runtime is niet al bezig met een andere pilot.
- Clean start is ok.
- Geen orphan/unknown open orders.
- Kill switch policy is correct voor demo armed mode.

Dashboard moet per blocker tonen:

- checknaam;
- status;
- exacte reden;
- volgende operatoractie.

## Stop Acceptance Gate

Stop-flow moet één veilige actie zijn:

1. Stop runtime loop.
2. Disarm demo trading.
3. Cancel open demo orders als policy dit vereist.
4. Query alle bekende niet-terminale orders.
5. Detecteer orphan/unknown orders.
6. Sync account.
7. Exporteer acceptatierapport.
8. Zet state naar `completed` of `resume_required`.

Acceptatie:

- Geen open demo orders na stop, tenzij Binance API een verklaarde fout teruggeeft.
- Als cancel/query faalt, status wordt `resume_required`.
- Report bevat cancel/reconciliation events.

## Periodieke Reconciliation

Voeg runtime-orchestrator scheduling toe zonder aparte zware scheduler:

- reconciliation interval uit pilot preset gebruiken;
- account sync interval uit pilot preset gebruiken;
- laatste sync/reconcile timestamps tonen in dashboard;
- failures tellen mee in pilot counters;
- overschrijding van max reconciliation failures pauzeert/stopt pilot volgens policy.

Acceptatie:

- Tijdens running pilot wordt reconciliation automatisch aangeroepen.
- Dashboard toont laatste reconciliation status en leeftijd.
- Reconciliation failures zijn zichtbaar als blocker.

## Crash en Resume

Bij dashboard/runtime start:

- check `data/pilot-runs/` op laatste niet-terminale run;
- check open demo orders;
- check order lifecycle;
- zet dashboard in `resume_required` als er onzekerheid is.

Operator kan dan:

- `Reconcile now`;
- `Cancel open demo orders`;
- `Mark resolved` alleen als checks groen zijn;
- nieuw pilot starten pas na clean state.

Acceptatie:

- Een onafgemaakte pilot wordt gedetecteerd.
- Nieuwe start wordt geblokkeerd bij open/orphan/unknown orders.
- Resolve-flow schrijft een audit/checkpoint event.

## Dashboard UX

Breid de bestaande Demo Pilot tab uit met een `Pilot Run` paneel:

- grote state badge;
- start gate checklist;
- startknop alleen logisch beschikbaar als `ready`;
- veilige stopknop tijdens `running`;
- resume-required panel;
- next safe action;
- run id en elapsed time;
- reconciliation/account sync age;
- acceptance criteria status.

Raw JSON blijft alleen in expanders/debug.

Geen live trading UI toevoegen.

## Report Bundle

Breid pilot reports uit met:

- `pilot-acceptance.json`;
- `pilot-acceptance.md`;
- run id;
- state transitions;
- preflight/start gate;
- stop gate;
- account before/after;
- order lifecycle summary;
- reconciliation summary;
- open/orphan/unknown order checks;
- alerts/errors;
- operator actions;
- final acceptance result: `accepted`, `blocked`, `resume_required`, `failed`.

Geen secrets in report.

## CLI en Check-All

Voeg waar nuttig CLI/read-only helpers toe:

- `pilot-status`
- `pilot-report`
- optioneel `pilot-preflight --json`

Breid `check-all` uit met:

- pilot orchestrator import;
- pilot store write/read test;
- no-secret report scan;
- dashboard import blijft groen.

## Testplan

Unit tests:

- start gate groen bij geldige Demo Spot payload;
- start gate blocked bij verkeerde profile/base URL;
- start gate blocked bij ontbrekende credentials;
- start gate blocked bij orphan orders;
- state transitions zijn geldig;
- invalid transitions worden geweigerd;
- stop-flow zet `resume_required` bij cancel/query failure;
- pilot store schrijft/leest zonder secrets;
- acceptance report bevat checklist/pipeline/reconciliation;
- report redaction werkt.

Dashboard/import tests:

- dashboard import blijft groen;
- Demo Pilot tab helper kan payload zonder actieve order renderen;
- resume-required payload toont blockers.

Integratietests met fake adapter:

- clean start -> ready -> running -> completed;
- open order bij start -> blocked;
- reconciliation failure -> resume_required;
- stop-flow cancelt fake open order en exporteert report.

Validatie:

- `python -m unittest discover -s tests`
- `python -m binance_spot_bot.cli check-all --json`
- secret scan groen;
- live trading disabled.

## Acceptatiecriteria

Roadmap 020 is volledig afgewerkt wanneer:

- Er een centrale Demo Spot pilot start/stop acceptance gate bestaat.
- Pilot states persistent worden bijgehouden.
- Start geblokkeerd wordt bij concrete blockers.
- Stop-flow cancel/reconcile/report als één veilige flow uitvoert.
- Periodieke reconciliation/account sync tijdens running pilot werkt.
- Crash/resume-required situatie wordt gedetecteerd en visueel uitgelegd.
- Dashboard toont next safe action.
- Acceptance report is leesbaar en redacted.
- Tests en `check-all` groen zijn.
- Roadmapbestand na implementatie wordt verplaatst naar `Voltooid docs/`.

## Veiligheidsregels

- Geen secrets in repo, logs, reports of pilot-run store.
- Live trading blijft disabled.
- Demo orders blijven achter explicit arm/start gate.
- Risk engine blijft verplicht.
- Orphan/unknown orders blokkeren start.
- LLM mag geen orders plaatsen of autoriseren.
- Operator moet altijd handmatig kunnen stoppen/disarmen/cancel uitvoeren.

## Aanbevolen Implementatievolgorde

1. `PilotRunStore` toevoegen.
2. `DemoPilotOrchestrator` met start gate en state transitions.
3. Stop-flow implementeren bovenop bestaande runtime methods.
4. Periodieke reconciliation/account sync integreren.
5. Dashboard `Pilot Run` paneel toevoegen.
6. Acceptance report uitbreiden.
7. Tests toevoegen.
8. `check-all` draaien.
9. Roadmap naar `Voltooid docs/` verplaatsen na volledige validatie.

## Uitvoering

Afgewerkt op 2026-05-10.

- `PilotRunStore` toegevoegd voor persistente pilot-run state, transitions, checkpoints, report paths en redacted opslag in `data/pilot-runs/`.
- `DemoPilotOrchestrator` toegevoegd als centrale start/stop acceptance gate bovenop bestaande runtime, reconciliation, account sync en operator payloads.
- Runtime gekoppeld aan pilot start gate, pilot-run metadata, veilige stop-flow, periodieke reconciliation en account sync.
- Dashboard uitgebreid met `Pilot Run` paneel, state badge, run id, start gate, resume status, next safe action en acceptance criteria.
- Session reports uitgebreid met `pilot-acceptance.json` en `pilot-acceptance.md`.
- CLI uitgebreid met `pilot-status`, `pilot-preflight` en `pilot-report`.
- `check-all` uitgebreid met pilot orchestrator import en pilot store smoke test.
- Tests toegevoegd voor start blockers, valid transitions, invalid transitions, store redaction, runtime stop-flow, cancel failure, periodic sync en acceptance report redaction.

## Validatie

- `python -m unittest tests.test_roadmap_020_pilot_acceptance_gate` groen: 8 tests.
- `python -m unittest discover -s tests` groen: 106 tests.
- `python -m binance_spot_bot.cli check-all --json` groen.
- Secret scan groen: geen secret artifacts.
- `git diff --check` zonder whitespace errors; alleen bestaande Windows line-ending waarschuwingen.
