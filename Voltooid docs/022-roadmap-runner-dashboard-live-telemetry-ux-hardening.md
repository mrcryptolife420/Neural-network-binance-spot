# Roadmap 022: Runner Dashboard Live Telemetry en UX Hardening

## Status

Voltooid.

Deze roadmap bouwt direct voort op roadmaps 001 t/m 021. De bot heeft nu een persistente lokale Demo Spot pilot runner met lockfile, heartbeat, command queue, telemetry, stale detection, acceptance gate en reports. Roadmap 022 richt zich niet op nieuwe tradinglogica, maar op de operatorervaring rond die runner.

**Maak het dashboard rond de persistente runner professioneel, scanbaar en veilig bedienbaar tijdens een Demo Spot pilot.**

Live trading blijft buiten scope en disabled.

## Waarom deze roadmap nu nodig is

Roadmap 021 heeft de technische runner-laag toegevoegd. De volgende zwakke plek is operator clarity:

- runner leeft, maar telemetry is nog niet compact samengevat;
- commands bestaan, maar command health/latency is niet duidelijk genoeg;
- stale/crash recovery kan concreter;
- report/telemetry paths zijn niet optimaal zichtbaar;
- start/stop/cancel/clear stale lock acties hebben extra UX-guarding nodig;
- charts voor heartbeat/equity/orders/reconciliation ontbreken nog als runner overzicht.

Voordat model/AI complexer wordt, moet de lokale operator-app duidelijk tonen wat de runner doet en welke actie veilig is.

## Doel

Maak een centraal Runner Mission Control paneel dat:

1. Runner health compact samenvat.
2. Live telemetry uit `telemetry.jsonl` aggregeert.
3. Charts toont voor heartbeat, equity/PnL, orders, rejects, reconciliation en command latency.
4. Command history toont met pending/processed/failed/ignored.
5. Stale/crash recovery flow expliciet maakt.
6. Safe command UX toevoegt voor stop/cancel/clear stale.
7. Report en telemetry paths zichtbaar maakt.

## In Scope

- Runner health payload/helper.
- Telemetry aggregation.
- Runner charts.
- Mission Control dashboard paneel.
- Stale recovery payload.
- Safe command confirmation checkboxes.
- Report/telemetry path table.
- Tests voor helpers en dashboard import.
- `check-all` validatie.

## Niet In Scope

- Binance live trading.
- Nieuwe exchange-integraties.
- Nieuwe ML-strategie.
- Tweede dashboard.
- Tweede runner.
- Nieuwe orderroute.
- LLM-autonomie.

## Niet Opnieuw Bouwen

Gebruik bestaande modules:

- `pilot_runner.py`
- `pilot_orchestrator.py`
- `runtime.py`
- `session_report.py`
- `ui/streamlit_app.py`
- `ui/charts.py`
- `ui/components.py`
- `check_all.py`
- `cli.py`

Nieuwe code moet helper/payload/chart laag zijn bovenop bestaande runner telemetry.

## Taken

### Runner Health Payload

- Voeg helper toe voor:
  - runner state;
  - alive/stale;
  - heartbeat age;
  - active run id;
  - latest command;
  - failed command count;
  - pending command count;
  - telemetry row count;
  - latest report paths;
  - next safe action.

Acceptatie:

- Werkt zonder actieve runner.
- Werkt met lege telemetry.
- Geen secrets in payload.

### Telemetry Aggregation

- Lees `telemetry.jsonl`.
- Maak samenvatting:
  - first/last timestamp;
  - row count;
  - max heartbeat age;
  - latest equity/PnL;
  - latest runner/runtime status;
  - order/reject/API error counters;
  - reconciliation status counts;
  - alert count.

Acceptatie:

- Crasht niet bij lege/kapotte files.
- Negeert corrupte regels.
- Redacted output.

### Runner Charts

- Voeg chart helpers toe voor:
  - heartbeat age over tijd;
  - equity/PnL over tijd;
  - orders/rejects/API errors counters;
  - command status/latency;
  - reconciliation status counts.

Acceptatie:

- Charts crashen niet bij lege data.
- Dashboard import blijft groen.

### Dashboard Mission Control

- Breid Demo Pilot tab uit met Mission Control:
  - state badges;
  - runner health table;
  - telemetry summary;
  - charts;
  - command history;
  - report/telemetry paths;
  - stale recovery panel.

Acceptatie:

- Operator ziet binnen 5 seconden runner status en next safe action.
- Raw JSON blijft in expanders.
- Live disabled blijft zichtbaar.

### Safe Command UX

- Voeg confirmaties toe:
  - stop runner;
  - cancel open demo orders;
  - clear stale lock.

Acceptatie:

- Gevaarlijke commands worden niet per ongeluk verzonden.
- Clear stale lock toont blocker als runner niet stale is.

### Stale Recovery

- Helper toont stappen:
  - inspect stale state;
  - reconcile;
  - cancel open orders;
  - export report;
  - clear stale lock;
  - mark resolved via acceptance gate.

Acceptatie:

- Stale state heeft concrete next safe action.
- New start blijft geblokkeerd tot clean.

## Testplan

- Unit tests voor runner health payload.
- Unit tests voor telemetry aggregation met lege, geldige en corrupte regels.
- Unit tests voor stale recovery payload.
- Unit tests voor chart helpers met lege data.
- Dashboard import test.
- `python -m unittest discover -s tests`
- `python -m binance_spot_bot.cli check-all --json`
- Secret scan groen.

## Definition of Done

Roadmap 022 is volledig afgewerkt wanneer:

- Runner Mission Control paneel bestaat.
- Runner health payload compact en redacted is.
- Telemetry aggregatie en charts werken.
- Command history en command health zichtbaar zijn.
- Stop/cancel/clear stale UX confirmations hebben.
- Stale recovery flow concreet is.
- Tests en `check-all` groen zijn.
- Roadmap naar `Voltooid docs/` is verplaatst.

## Veiligheidsregels

- Geen secrets in telemetry, commands, reports, dashboard of logs.
- Geen live trading.
- Demo trading blijft achter explicit arm, acceptance gate en runner lock.
- Risk engine blijft verplicht.
- Orphan/unknown orders blokkeren nieuwe start.
- Runner commands mogen geen orders autoriseren buiten bestaande runtime.

## Uitvoering

Afgewerkt op 2026-05-10.

- Runner health payload toegevoegd met state, alive/stale, heartbeat age, command health, telemetry rows, report count en next safe action.
- Telemetry aggregatie toegevoegd met robuuste JSONL parsing, corrupte-regel tolerantie, status counts, equity/PnL en counters.
- Stale recovery payload toegevoegd met concrete herstelstappen.
- Runner charts toegevoegd voor heartbeat age, equity/PnL, orders/rejects/API errors en command status.
- Demo Pilot dashboard uitgebreid met Runner Mission Control, telemetry summary, charts, command history, report/telemetry paths en safe confirmations voor stop/cancel/clear stale.
- Tests toegevoegd voor telemetry aggregation, empty states, health payload, stale recovery, chart helpers en dashboard import.

## Validatie

- `python -m unittest tests.test_roadmap_022_runner_dashboard_telemetry` groen: 6 tests.
- `python -m unittest discover -s tests` groen: 120 tests.
- `python -m binance_spot_bot.cli check-all --json` groen.
- Secret scan groen: geen secret artifacts.
- `git diff --check` zonder whitespace errors; alleen bestaande Windows line-ending waarschuwingen.
