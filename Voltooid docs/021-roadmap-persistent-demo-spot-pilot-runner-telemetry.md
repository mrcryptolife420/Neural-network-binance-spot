# Roadmap 021: Persistent Demo Spot Pilot Runner en Telemetry

## Status

Voltooid.

Deze roadmap bouwt direct voort op roadmaps 001 t/m 020. De bot heeft nu een lokale Windows one-click start, Binance Demo Spot connect/arm flow, deterministic risk engine, order lifecycle tracking, reconciliation, account sync, demo pilot presets, operator dashboard, acceptance gate, pilot-run persistence en acceptance reports.

Roadmap 020 heeft bewezen wanneer een Demo Spot pilot veilig mag starten en hoe start/stop/report acceptance gecontroleerd wordt. De volgende stap is dat de pilot als echte lokale run stabiel kan blijven draaien, los van Streamlit-reruns en handmatige interactie.

**Maak van de Demo Spot pilot een persistente lokale runner met heartbeat, commands, crash-detectie en live telemetry.**

Live trading blijft buiten scope en disabled.

## Waarom deze roadmap nu nodig is

De huidige dashboard/runtime flow is bruikbaar voor gecontroleerde stappen, maar een operationele pilot moet lokaal kunnen blijven draaien terwijl:

- het dashboard refresht;
- Streamlit widgets opnieuw renderen;
- de operator tabs wisselt;
- de runner periodiek reconciliation/account sync uitvoert;
- de operator live status en heartbeat ziet;
- stop/cancel/reconcile commands veilig worden doorgegeven;
- stale/crash situaties automatisch zichtbaar worden.

Zonder persistente runner blijft de pilot te afhankelijk van dashboardinteractie. Roadmap 021 maakt de brug van "acceptance gate bestaat" naar "ik kan de bot lokaal stabiel aan het werk zien".

## Doel

Maak een lokale Demo Spot pilot runner die:

1. Als aparte lokale achtergrond-run beheerd kan worden.
2. Niet dubbel gestart kan worden.
3. Heartbeats en telemetry schrijft.
4. Commands ontvangt voor stop, cancel en reconcile.
5. Dashboard health toont.
6. Stale/crash detecteert.
7. Bestaande `DemoPilotOrchestrator`, `PilotRunStore`, runtime, reconciliation en reports gebruikt.
8. Bij stop altijd de veilige stop-flow uit roadmap 020 uitvoert.

## In Scope

- Persistent runner state.
- PID/lockfile.
- Heartbeat store.
- Command queue.
- Runner telemetry snapshots.
- Dashboard runner health paneel.
- Start/stop runner vanuit dashboard.
- CLI helpers voor runner start/status/stop.
- Crash/stale detection.
- Tests voor lock, heartbeat, commands, stale detection en safe stop.

## Niet In Scope

- Binance live trading.
- Futures/margin.
- Nieuwe exchange-integraties.
- Nieuwe ML-strategie.
- RL.
- Autonome LLM-orders.
- Tweede dashboard bouwen.
- Tweede order engine bouwen.
- Secrets opslaan in repo/logs/telemetry.

## Niet Opnieuw Bouwen

Gebruik bestaande modules:

- `runtime.py`
- `pilot_orchestrator.py`
- `demo_pilot.py`
- `demo_spot.py`
- `order_lifecycle.py`
- `session_report.py`
- `ui/streamlit_app.py`
- `control_center.py`
- `check_all.py`
- `cli.py`

Nieuwe code moet een dunne runner-laag zijn bovenop bestaande runtime/orchestrator, geen parallelle bot.

## Architectuur

Voeg toe:

- `PilotRunnerService`
  - start runtime;
  - voert `run_steps` of tick-loop uit;
  - schrijft heartbeat;
  - schrijft telemetry;
  - leest commands;
  - voert safe stop uit;
  - exporteert report.

- `PilotHeartbeatStore`
  - bewaart `runner.json`;
  - bevat run id, pid, status, started/updated timestamps, heartbeat age, command status;
  - bevat geen secrets.

- `PilotCommandQueue`
  - schrijft command JSON files naar `data/pilot-runs/<run-id>/commands/`;
  - commands:
    - `stop`;
    - `reconcile`;
    - `cancel_open_orders`;
    - `export_report`;
  - runner markeert command als `processed`, `failed` of `ignored`.

- `PilotTelemetryStore`
  - schrijft `telemetry.jsonl`;
  - laatste snapshot ook in `latest-telemetry.json`;
  - bevat:
    - runtime status;
    - pilot state;
    - heartbeat timestamp;
    - equity/PnL;
    - orders/rejects/API errors;
    - reconciliation status;
    - account sync status;
    - open orders;
    - latest signal/risk/execution;
    - alerts count;
    - report paths.

## Runner State

Minimale runner states:

- `not_running`
- `starting`
- `running`
- `stopping`
- `stopped`
- `completed`
- `failed`
- `stale`
- `resume_required`

Regels:

- Eén actieve runner per workspace.
- Lockfile blokkeert dubbele start.
- Stale heartbeat zet dashboard status naar `stale`.
- Stale + open orders/reconciliation blocker zet pilot status naar `resume_required`.
- Stop command moet safe stop-flow uitvoeren.
- Failed runner mag geen nieuwe start toestaan tot reconcile/resume checks groen zijn.

## Lockfile en PID

Gebruik een lockfile:

- `data/pilot-runs/runner.lock.json`

Inhoud:

- runner id;
- run id;
- pid;
- started_at_ms;
- updated_at_ms;
- status;
- command directory;
- telemetry paths;
- process command;

Acceptatie:

- Tweede start wordt geblokkeerd als lock actief is en heartbeat vers is.
- Oude lock wordt als stale gemarkeerd als heartbeat te oud is.
- Stale lock kan pas worden opgeruimd na resume checks.

## Heartbeat

Runner schrijft elke paar seconden:

- pid;
- run id;
- state;
- timestamp;
- last tick;
- last reconciliation;
- last account sync;
- last command;
- last error;

Dashboard berekent:

- alive;
- heartbeat age;
- stale;
- next safe action.

Acceptatie:

- Dashboard ziet runner binnen enkele seconden als alive.
- Stale wordt zichtbaar bij oude heartbeat.
- Heartbeat bevat geen secrets.

## Commands

Dashboard schrijft commands in command queue.

Command schema:

- `command_id`;
- `type`;
- `created_at_ms`;
- `status`;
- `payload`;
- `processed_at_ms`;
- `result`;

Supported commands:

- `stop`: voert safe stop-flow uit.
- `reconcile`: roept bestaande reconciliation aan.
- `cancel_open_orders`: roept bestaande cancel flow aan.
- `export_report`: exporteert report zonder orders te plaatsen.

Acceptatie:

- Commands zijn idempotent waar mogelijk.
- Onbekende command types worden `ignored`.
- Fouten worden redacted opgeslagen.

## Dashboard UX

Breid bestaande Demo Pilot tab uit met `Runner` paneel:

- runner state;
- PID;
- run id;
- heartbeat age;
- stale indicator;
- latest telemetry;
- command status;
- buttons:
  - start runner;
  - stop runner;
  - reconcile now;
  - cancel open demo orders;
  - export report;
  - clear stale lock alleen als checks groen zijn.

Dashboard moet blijven tonen:

- live disabled;
- Demo Spot base URL;
- armed state;
- pilot acceptance gate;
- runner health;
- next safe action.

Raw JSON blijft in expanders.

## CLI

Voeg read/write-safe local commands toe:

- `pilot-runner-start`
- `pilot-runner-status`
- `pilot-runner-stop`
- `pilot-runner-command --type reconcile|cancel_open_orders|export_report`

CLI mag geen secrets printen.

Start via CLI gebruikt:

- existing settings;
- Demo Spot profile;
- acceptance gate;
- safe lock behavior.

## Windows One-Click

Gebruik bestaande one-click launcher en dashboard.

Verbeter alleen waar nodig:

- dashboard moet runner-status tonen na start;
- geen extra terminalkennis vereist;
- log/telemetry path zichtbaar;
- live disabled zichtbaar.

Geen aparte Windows app bouwen in deze roadmap.

## Reports

Acceptance report uit roadmap 020 uitbreiden met runner-sectie:

- runner id;
- PID;
- heartbeat summary;
- command history;
- telemetry summary;
- stale/crash events;
- stop command result.

Geen secrets.

## Testplan

Unit tests:

- lockfile write/read.
- active lock blocks duplicate start.
- stale lock detection.
- heartbeat write/read.
- telemetry write/read latest.
- command queue create/process/fail/ignore.
- command payload redaction.
- runner status payload zonder actieve runner.

Integration/fake runtime tests:

- runner start schrijft lock + heartbeat.
- runner processes reconcile command.
- runner processes cancel command.
- runner processes stop command and writes completed state.
- cancel failure resulteert in `resume_required`.
- stale heartbeat wordt correct gedetecteerd.

Dashboard/import tests:

- dashboard import blijft groen.
- runner status helper kan lege state renderen.
- stale state toont next safe action.

Validation:

- `python -m unittest discover -s tests`
- `python -m binance_spot_bot.cli check-all --json`
- secret scan groen.
- live trading disabled.

## Acceptatiecriteria

Roadmap 021 is volledig afgewerkt wanneer:

- Er een persistente lokale Demo Spot pilot runner bestaat.
- Dubbele runner start geblokkeerd wordt.
- Heartbeat en telemetry worden geschreven.
- Dashboard runner health toont.
- Dashboard commands naar runner kan sturen.
- Stop command voert safe stop-flow uit.
- Stale/crash state wordt gedetecteerd.
- Resume-required blijft blocker voor nieuwe starts.
- Reports bevatten runner summary.
- Tests en `check-all` groen zijn.
- Roadmapbestand na implementatie naar `Voltooid docs/` wordt verplaatst.

## Veiligheidsregels

- Geen secrets in lockfile, telemetry, commands, logs of reports.
- Geen live trading.
- Demo trading blijft achter explicit arm en acceptance gate.
- Risk engine blijft verplicht.
- Orphan/unknown orders blokkeren nieuwe start.
- Runner mag geen nieuwe orderroute toevoegen buiten bestaande runtime/execution engine.
- LLM mag geen commands autoriseren of orders plaatsen.

## Aanbevolen Implementatievolgorde

1. `PilotHeartbeatStore`, `PilotCommandQueue`, `PilotTelemetryStore` toevoegen.
2. `PilotRunnerService` toevoegen met fake/testable loop.
3. Lock/stale detection implementeren.
4. CLI runner commands toevoegen.
5. Dashboard Runner paneel toevoegen.
6. Reports uitbreiden met runner summary.
7. Tests toevoegen.
8. `check-all` draaien.
9. Roadmap naar `Voltooid docs/` verplaatsen na volledige validatie.

## Uitvoering

Afgewerkt op 2026-05-10.

- `PilotHeartbeatStore`, `PilotCommandQueue` en `PilotTelemetryStore` toegevoegd voor lockfile, runner heartbeat, commands en live telemetry.
- `PilotRunnerService` toegevoegd als persistente lokale runner-laag bovenop bestaande `BotRuntime`, `DemoPilotOrchestrator`, reconciliation en reports.
- Lock/stale detection toegevoegd met `runner.lock.json` en `runner.json`.
- Runner command verwerking toegevoegd voor `stop`, `reconcile`, `cancel_open_orders`, `export_report` en onbekende commands als `ignored`.
- CLI uitgebreid met `pilot-runner-start`, `pilot-runner-status`, `pilot-runner-stop` en `pilot-runner-command`.
- Dashboard Demo Pilot tab uitgebreid met Runner paneel, heartbeat state, stale/alive status, PID, telemetry, commands en runner command buttons.
- Acceptance report uitgebreid met runner summary, runner id/status en command history.
- `check-all` uitgebreid met runner import en runner status smoke checks.
- Tests toegevoegd voor lock/stale, duplicate start, telemetry, command queue redaction/statussen, empty runner status, service run, command processing en stale cleanup.

## Validatie

- `python -m unittest tests.test_roadmap_021_pilot_runner` groen: 8 tests.
- `python -m unittest discover -s tests` groen: 114 tests.
- `python -m binance_spot_bot.cli check-all --json` groen.
- Secret scan groen: geen secret artifacts.
- `git diff --check` zonder whitespace errors; alleen bestaande Windows line-ending waarschuwingen.
