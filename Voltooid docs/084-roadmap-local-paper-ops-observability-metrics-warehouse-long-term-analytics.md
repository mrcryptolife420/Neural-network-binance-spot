# Roadmap 084 - Local Paper Ops Observability, Metrics Warehouse \& Long-Term Analytics

Status: Niet volledig voltooid / opnieuw gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/084-roadmap-local-paper-ops-observability-metrics-warehouse-long-term-analytics.md
```

Volgt op:

* `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
* `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
* `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
* `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
* `Voltooid docs/005` t/m `Voltooid docs/075`
* `Roadmap docs/076-roadmap-binance-public-data-ingestion-indicator-warmup-feature-expansion.md`
* `Roadmap docs/077-roadmap-data-driven-strategy-confidence-backtest-dataset-builder-indicator-calibration.md`
* `Roadmap docs/078-roadmap-paper-strategy-deployment-continuous-evaluation-auto-rollback.md`
* `Roadmap docs/079-roadmap-paper-portfolio-operations-capital-allocation-strategy-rotation.md`
* `Roadmap docs/080-roadmap-paper-portfolio-benchmarking-stress-testing-scenario-replay.md`
* `Roadmap docs/081-roadmap-paper-portfolio-optimization-risk-budget-search-robust-allocation-selection.md`
* `Roadmap docs/082-roadmap-paper-policy-rollout-ab-paper-experiments-champion-challenger-governance.md`
* `Roadmap docs/083-roadmap-local-paper-operations-automation-scheduled-reports-operator-runbooks.md`

Doel: Roadmap 083 maakt lokale paper-ops automatisering mogelijk met jobs, scheduled reports, runbooks, support bundles en governance reminders. Roadmap 084 bouwt daarop een **lokale observability- en analyticslaag**: een metrics warehouse, trends over dagen/weken, SLO/SLA-achtige paper-ops health, long-term paper performance analytics, storage-efficiënte aggregaties, anomaly detection en een dashboard waarmee je ziet of de demo/paper bot en lokale operatorflow beter of slechter worden over tijd.

Live trading blijft volledig buiten scope.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] `Voltooid docs/075-roadmap-simple-demo-multi-symbol-final-validation.md` bestaat.
* \[x] Roadmap 075 heeft status `Voltooid`.
* \[x] Roadmap 075 bevestigt:

  * multi-symbol dashboard helpers;
  * budget allocation;
  * risk summary;
  * evidence export;
  * full pytest;
  * check-all;
  * browser smoke;
  * live trading disabled.
* \[x] Geen bestaande Roadmap 084 gevonden via repo-search.
* \[x] Roadmap 076 is lokaal aangemaakt voor Binance public data ingestion.
* \[x] Roadmap 077 is lokaal aangemaakt voor backtest/calibration/confidence.
* \[x] Roadmap 078 is lokaal aangemaakt voor paper deployment/rollback.
* \[x] Roadmap 079 is lokaal aangemaakt voor paper portfolio operations.
* \[x] Roadmap 080 is lokaal aangemaakt voor stress testing/scenario replay.
* \[x] Roadmap 081 is lokaal aangemaakt voor portfolio optimization.
* \[x] Roadmap 082 is lokaal aangemaakt voor paper policy governance.
* \[x] Roadmap 083 is lokaal aangemaakt voor local paper ops automation.

### Codebasecontrole

Gecontroleerde relevante modules:

* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] bestaande CLI heeft al operator commands voor:

  * diagnostics;
  * support-bundle;
  * support-bundle-verify;
  * retention-preview;
  * state-archive;
  * incident-timeline;
  * operator-report;
  * operator-quality-gate;
  * artifact-catalog;
  * operator-health-score;
  * evidence-chain;
  * environment-doctor;
  * data-growth-budget;
  * diagnostics-baseline;
  * report-index;
  * support-bundles-verify;
  * redaction-self-test;
  * local-ops-snapshot;
  * operator-command-manifest;
  * evidence-manifest;
  * check-all;
  * dashboard-smoke;
  * dashboard-browser-smoke.
* \[x] `operator\_ops.py` bevat al:

  * artifact catalog;
  * operator health score;
  * evidence chain;
  * environment doctor;
  * data growth budget;
  * diagnostics baseline;
  * report index;
  * support bundle verification;
  * redaction self-test;
  * local ops snapshot;
  * operator quality gate;
  * incident timeline;
  * retention preview;
  * state archive.
* \[x] Alle bestaande operator outputs bevatten of forceren `live\_trading\_enabled=False`.

### Belangrijkste gat na Roadmap 083

Roadmap 083 maakt lokale jobs/schedules/runbooks mogelijk. Wat daarna nog mist:

* \[ ] centrale metrics opslag;
* \[ ] trendanalyse over meerdere dagen/weken;
* \[ ] health-score history;
* \[ ] report latency/failure trends;
* \[ ] paper performance analytics over lange periode;
* \[ ] data growth trend;
* \[ ] evidence freshness trend;
* \[ ] dashboard smoke trend;
* \[ ] policy governance trend;
* \[ ] scheduled analytics dashboards;
* \[ ] anomaly detection;
* \[ ] local metrics retention/compaction;
* \[ ] metrics query CLI;
* \[ ] long-term analytics reports.

\---

## 1\. Hoofddoel Roadmap 084

Maak een lokale observabilitylaag:

```text
Local jobs + reports + sessions + governance evidence
→ metrics extraction
→ local metrics warehouse
→ daily/weekly aggregations
→ anomaly detection
→ long-term analytics
→ observability dashboard
→ evidence-backed ops decisions
```

Na Roadmap 084 moet de bot kunnen tonen:

* \[ ] worden local ops gezonder of slechter?
* \[ ] falen scheduled reports vaker?
* \[ ] blijft check-all groen over tijd?
* \[ ] worden support bundles groter?
* \[ ] groeit data te hard?
* \[ ] blijven paper strategies stabiel?
* \[ ] welke policy/strategy veroorzaakt meeste warnings?
* \[ ] welke symbolen zorgen voor meeste blocks/conflicts?
* \[ ] hoe vaak faalt dashboard smoke?
* \[ ] hoe snel worden incidents opgelost?
* \[ ] wanneer is evidence stale?
* \[ ] welke acties moet de operator prioriteren?

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen cloud observability stack.
* \[ ] Geen externe telemetry.
* \[ ] Geen Prometheus/Grafana verplicht maken.
* \[ ] Geen remote uploads.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen nieuwe scheduler; Roadmap 083 doet scheduling.
* \[ ] Geen nieuwe governance engine; Roadmap 082 doet governance.
* \[ ] Geen nieuwe optimizer; Roadmap 081 doet optimization.
* \[ ] Geen nieuwe portfolio engine; Roadmap 079 doet portfolio ops.

Wel doen:

* \[ ] bestaande operator outputs indexeren;
* \[ ] lokale metrics warehouse bouwen;
* \[ ] metrics uit jobs, reports, sessions, evidence en governance halen;
* \[ ] trends/aggregaties berekenen;
* \[ ] anomaly detection toevoegen;
* \[ ] dashboard analytics toevoegen;
* \[ ] CLI queries toevoegen;
* \[ ] retention/compaction voor metrics toevoegen;
* \[ ] alles lokaal en secret-free houden.

\---

## 3\. Fase 0 - Observability Safety Contract

Doel: metrics/analytics mogen geen secrets lekken en geen live acties triggeren.

### Nieuwe doc

```text
docs/local-observability-safety-contract.md
```

### Regels

* \[ ] Metrics warehouse is local-only.
* \[ ] Geen remote telemetry.
* \[ ] Geen cloud upload.
* \[ ] Geen API secrets opslaan.
* \[ ] Geen raw credentials in metrics labels.
* \[ ] Geen signed endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen live mode.
* \[ ] Metrics collectors zijn read-only.
* \[ ] Analytics mag alleen recommendations geven, geen risk verhogen.
* \[ ] Anomaly actions mogen support bundle/runbook triggeren, niet trading activeren.
* \[ ] Exports worden geredact.

### Acceptatiecriteria

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen dat metrics labels/secrets geredact worden.
* \[ ] Dashboard toont `LOCAL OBSERVABILITY ONLY`.
* \[ ] CLI faalt als remote export wordt gevraagd.
* \[ ] No-live statement staat in reports.

\---

## 4\. Fase 1 - Metrics Event Schema

Doel: één uniform eventformaat voor alle lokale metrics.

### Nieuwe module

```text
src/binance\_spot\_bot/metrics\_schema.py
```

### Dataclasses

* \[ ] `MetricEvent`
* \[ ] `MetricSeries`
* \[ ] `MetricPoint`
* \[ ] `MetricLabel`
* \[ ] `MetricIngestResult`
* \[ ] `MetricAggregation`
* \[ ] `MetricAnomaly`

### MetricEvent velden

* \[ ] event\_id;
* \[ ] timestamp\_ms;
* \[ ] source;
* \[ ] category;
* \[ ] name;
* \[ ] value;
* \[ ] unit;
* \[ ] status;
* \[ ] severity;
* \[ ] labels;
* \[ ] artifact\_path;
* \[ ] evidence\_id;
* \[ ] redacted;
* \[ ] live\_trading\_enabled=false.

### Categories

* \[ ] job;
* \[ ] scheduler;
* \[ ] report;
* \[ ] health;
* \[ ] check;
* \[ ] dashboard;
* \[ ] session;
* \[ ] paper\_performance;
* \[ ] portfolio;
* \[ ] governance;
* \[ ] support;
* \[ ] storage;
* \[ ] evidence;
* \[ ] data\_quality;
* \[ ] incident.

### Acceptatiecriteria

* \[ ] MetricEvent is JSON-serializable.
* \[ ] Labels worden geredact.
* \[ ] Geen secrets in event.
* \[ ] Event schema heeft versie.
* \[ ] Tests dekken invalid/missing fields.

\---

## 5\. Fase 2 - Local Metrics Warehouse

Doel: metrics lokaal opslaan en snel kunnen queryen.

### Nieuwe module

```text
src/binance\_spot\_bot/metrics\_warehouse.py
```

### Storage opties

Start simpel:

```text
data/metrics/
  metrics.jsonl
  daily/
  weekly/
  manifests/
```

Optioneel later:

```text
data/metrics/metrics.sqlite
```

### Core functies

* \[ ] `append\_metric(event)`
* \[ ] `append\_many(events)`
* \[ ] `query\_metrics(filters)`
* \[ ] `latest\_metric(name)`
* \[ ] `series(name, labels, range)`
* \[ ] `aggregate\_daily(...)`
* \[ ] `aggregate\_weekly(...)`
* \[ ] `write\_manifest()`
* \[ ] `verify\_manifest()`
* \[ ] `compact\_old\_metrics()`

### Acceptatiecriteria

* \[ ] Warehouse werkt zonder extra database dependency.
* \[ ] JSONL fallback is default.
* \[ ] SQLite is optioneel.
* \[ ] Writes zijn append-only.
* \[ ] Manifest/hashes bestaan.
* \[ ] Geen secrets in metrics.

\---

## 6\. Fase 3 - Metrics Collectors

Doel: bestaande artifacts omzetten naar metrics.

### Nieuwe module

```text
src/binance\_spot\_bot/metrics\_collectors.py
```

### Collectors

* \[ ] `collect\_check\_all\_metrics`
* \[ ] `collect\_operator\_health\_metrics`
* \[ ] `collect\_diagnostics\_metrics`
* \[ ] `collect\_support\_bundle\_metrics`
* \[ ] `collect\_report\_index\_metrics`
* \[ ] `collect\_artifact\_catalog\_metrics`
* \[ ] `collect\_data\_growth\_metrics`
* \[ ] `collect\_evidence\_metrics`
* \[ ] `collect\_dashboard\_smoke\_metrics`
* \[ ] `collect\_local\_job\_metrics`
* \[ ] `collect\_scheduler\_metrics`
* \[ ] `collect\_runbook\_metrics`
* \[ ] `collect\_governance\_metrics`
* \[ ] `collect\_paper\_session\_metrics`
* \[ ] `collect\_portfolio\_metrics`
* \[ ] `collect\_policy\_experiment\_metrics`

### Acceptatiecriteria

* \[ ] Collectors zijn read-only.
* \[ ] Collectors werken ook als artifact ontbreekt.
* \[ ] Missing artifact wordt metric warning.
* \[ ] Collectors gebruiken redaction.
* \[ ] Tests gebruiken fixtures.

\---

## 7\. Fase 4 - Local Ops Metrics Ingestion

Doel: Roadmap 083 local jobs en reports automatisch in metrics verwerken.

### Nieuwe module

```text
src/binance\_spot\_bot/local\_ops\_metrics.py
```

### Metrics uit jobs

* \[ ] job run count;
* \[ ] job success count;
* \[ ] job failure count;
* \[ ] job duration;
* \[ ] timeout count;
* \[ ] retry count;
* \[ ] failed job category;
* \[ ] support bundle created;
* \[ ] runbook triggered;
* \[ ] last successful run age;
* \[ ] stale job count.

### Metrics uit scheduled reports

* \[ ] reports generated;
* \[ ] report generation failures;
* \[ ] report latency;
* \[ ] report size;
* \[ ] stale reports;
* \[ ] missing daily report;
* \[ ] missing weekly report.

### Acceptatiecriteria

* \[ ] Local jobs hebben trends.
* \[ ] Scheduler health is zichtbaar.
* \[ ] Failed scheduled reports worden meetbaar.
* \[ ] Metrics werken zonder scheduler loop actief.

\---

## 8\. Fase 5 - Paper Performance Metrics Ingestion

Doel: paper bot prestaties over tijd analyseren.

### Nieuwe module

```text
src/binance\_spot\_bot/paper\_performance\_metrics.py
```

### Metrics

* \[ ] paper sessions count;
* \[ ] session duration;
* \[ ] fills count;
* \[ ] PnL per session;
* \[ ] drawdown per session;
* \[ ] alerts per session;
* \[ ] critical alerts;
* \[ ] blocked trades;
* \[ ] confidence distribution;
* \[ ] data quality warnings;
* \[ ] liquidity warnings;
* \[ ] symbol-level PnL;
* \[ ] strategy-level PnL;
* \[ ] portfolio-level PnL;
* \[ ] rollback count;
* \[ ] watchdog action count.

### Acceptatiecriteria

* \[ ] Session reports worden metrics.
* \[ ] Portfolio reports worden metrics.
* \[ ] Strategy deployment reports worden metrics.
* \[ ] Missing report geeft warning.
* \[ ] Geen secrets.

\---

## 9\. Fase 6 - Governance Metrics Ingestion

Doel: Roadmap 082 governance meetbaar maken.

### Nieuwe module

```text
src/binance\_spot\_bot/governance\_metrics.py
```

### Metrics

* \[ ] active champion age;
* \[ ] challenger count;
* \[ ] active experiments;
* \[ ] completed experiments;
* \[ ] experiment stop count;
* \[ ] promotion count;
* \[ ] rollback count;
* \[ ] governance decision latency;
* \[ ] weekly report freshness;
* \[ ] stale evidence count;
* \[ ] policies suspended;
* \[ ] policies archived;
* \[ ] operator pending confirmations.

### Acceptatiecriteria

* \[ ] Governance dashboard kan trend tonen.
* \[ ] Stale governance evidence wordt zichtbaar.
* \[ ] Experiment failures worden meetbaar.
* \[ ] No-live proof blijft onderdeel van metrics.

\---

## 10\. Fase 7 - Daily/Weekly Aggregation Engine

Doel: ruwe metrics samenvatten naar bruikbare trends.

### Nieuwe module

```text
src/binance\_spot\_bot/metrics\_aggregation.py
```

### Aggregaties

Daily:

* \[ ] total jobs;
* \[ ] failed jobs;
* \[ ] report success rate;
* \[ ] health score;
* \[ ] check-all status;
* \[ ] browser smoke status;
* \[ ] data growth;
* \[ ] evidence freshness;
* \[ ] paper PnL;
* \[ ] paper drawdown;
* \[ ] alerts;
* \[ ] governance pending items.

Weekly:

* \[ ] weekly health average;
* \[ ] weekly failure rate;
* \[ ] weekly paper performance;
* \[ ] weekly storage growth;
* \[ ] weekly governance activity;
* \[ ] weekly evidence integrity;
* \[ ] weekly operator workload.

### Acceptatiecriteria

* \[ ] Aggregaties zijn deterministic.
* \[ ] Aggregaties zijn reproduceerbaar uit raw metrics.
* \[ ] Aggregates hebben manifest/hash.
* \[ ] Missing data wordt duidelijk gemarkeerd.

\---

## 11\. Fase 8 - Paper Ops SLO/SLA Layer

Doel: operator health meetbaar maken als doelen.

### Nieuwe module

```text
src/binance\_spot\_bot/ops\_slo.py
```

### SLO voorbeelden

* \[ ] Check-all success rate >= 95% per week.
* \[ ] Dashboard smoke success rate >= 95% per week.
* \[ ] Daily report freshness <= 24h.
* \[ ] Weekly governance report freshness <= 7d.
* \[ ] Support bundle verify success >= 99%.
* \[ ] Redaction self-test success = 100%.
* \[ ] Evidence manifest freshness <= 24h.
* \[ ] Critical alert unresolved age <= threshold.
* \[ ] Data growth below budget.
* \[ ] No live trading proof always true.

### SLO statuses

* \[ ] ok;
* \[ ] warning;
* \[ ] breach;
* \[ ] unknown.

### Acceptatiecriteria

* \[ ] SLO config is local JSON.
* \[ ] SLO results zijn dashboard-ready.
* \[ ] SLO breach kan runbook reminder triggeren.
* \[ ] No-live proof SLO bestaat.
* \[ ] SLO reports zijn secret-free.

\---

## 12\. Fase 9 - Anomaly Detection

Doel: rare veranderingen vroeg signaleren.

### Nieuwe module

```text
src/binance\_spot\_bot/metrics\_anomaly\_detection.py
```

### Anomalies

* \[ ] sudden job failure spike;
* \[ ] check-all turns red;
* \[ ] dashboard smoke failure;
* \[ ] support bundle size spike;
* \[ ] data growth spike;
* \[ ] evidence chain break;
* \[ ] paper drawdown spike;
* \[ ] critical alerts spike;
* \[ ] strategy rollback spike;
* \[ ] governance experiment failures;
* \[ ] stale data quality metrics;
* \[ ] report generation latency spike.

### Methods

* \[ ] static threshold;
* \[ ] rolling average deviation;
* \[ ] week-over-week change;
* \[ ] missing expected metric;
* \[ ] stale metric detection.

### Acceptatiecriteria

* \[ ] Anomalies hebben severity.
* \[ ] Anomalies hebben recommended action.
* \[ ] Anomalies triggeren geen live acties.
* \[ ] Tests dekken threshold en missing data.
* \[ ] Dashboard toont anomalies.

\---

## 13\. Fase 10 - Metrics Query CLI

Doel: metrics snel kunnen bekijken zonder dashboard.

### Nieuwe commands

```powershell
python -m binance\_spot\_bot.cli metrics-ingest --source all
python -m binance\_spot\_bot.cli metrics-query --name operator.health\_score --days 7
python -m binance\_spot\_bot.cli metrics-latest --category health
python -m binance\_spot\_bot.cli metrics-aggregate --daily
python -m binance\_spot\_bot.cli metrics-slo
python -m binance\_spot\_bot.cli metrics-anomalies
python -m binance\_spot\_bot.cli metrics-export --days 30
python -m binance\_spot\_bot.cli metrics-compact --older-than-days 30 --confirm COMPACT\_METRICS
```

### Acceptatiecriteria

* \[ ] Commands werken zonder API keys.
* \[ ] Commands zijn read-only behalve ingest/compact.
* \[ ] Compact vereist confirm.
* \[ ] JSON output mogelijk.
* \[ ] Geen live/signed endpoints.

\---

## 14\. Fase 11 - Observability Dashboard Panel

Doel: trends en health zichtbaar maken in de UI.

### Nieuwe dashboardsectie

```text
Local Observability
```

### Panels

* \[ ] health score trend;
* \[ ] check-all trend;
* \[ ] dashboard smoke trend;
* \[ ] scheduled jobs success/fail trend;
* \[ ] report freshness;
* \[ ] support bundle verify status;
* \[ ] evidence freshness;
* \[ ] data growth trend;
* \[ ] paper performance trend;
* \[ ] portfolio drawdown trend;
* \[ ] governance status trend;
* \[ ] anomalies;
* \[ ] SLO status;
* \[ ] next recommended action.

### Charts

* \[ ] daily health score line;
* \[ ] job failures bar;
* \[ ] report freshness timeline;
* \[ ] data growth area chart;
* \[ ] paper PnL trend;
* \[ ] drawdown trend;
* \[ ] governance pending count;
* \[ ] anomaly severity timeline.

### Acceptatiecriteria

* \[ ] Dashboard toont `LOCAL OBSERVABILITY ONLY`.
* \[ ] Raw JSON alleen in debug expander.
* \[ ] Charts gebruiken unieke keys.
* \[ ] Browser smoke dekt panel.
* \[ ] Geen live controls.

\---

## 15\. Fase 12 - Long-Term Analytics Reports

Doel: periodieke analyticsrapporten maken.

### Nieuwe module

```text
src/binance\_spot\_bot/long\_term\_analytics\_report.py
```

### Reports

Daily:

* \[ ] local observability daily report;
* \[ ] paper performance daily analytics;
* \[ ] data growth daily summary.

Weekly:

* \[ ] weekly ops analytics;
* \[ ] weekly paper performance analytics;
* \[ ] weekly governance analytics;
* \[ ] weekly evidence freshness report.

Monthly:

* \[ ] monthly paper strategy review;
* \[ ] monthly storage/data growth review;
* \[ ] monthly reliability review.

### Output

```text
data/metrics/reports/
  daily/YYYY-MM-DD/
  weekly/YYYY-WW/
  monthly/YYYY-MM/
```

### Acceptatiecriteria

* \[ ] Reports zijn secret-free.
* \[ ] Reports linken naar metrics manifest.
* \[ ] Reports tonen trends en recommended actions.
* \[ ] Reports kunnen via dashboard gedownload worden.

\---

## 16\. Fase 13 - Metrics Retention \& Compaction

Doel: metrics niet onbeperkt laten groeien.

### Nieuwe module

```text
src/binance\_spot\_bot/metrics\_retention.py
```

### Policies

* \[ ] raw metrics bewaren 30/60/90 dagen;
* \[ ] daily aggregates langer bewaren;
* \[ ] weekly aggregates nog langer bewaren;
* \[ ] compact raw metrics naar aggregates;
* \[ ] archive old metrics;
* \[ ] retention preview before destructive action;
* \[ ] manifest/hash update na compaction.

### Acceptatiecriteria

* \[ ] Compaction vereist confirm.
* \[ ] Preview-first voor deletes.
* \[ ] Aggregates blijven reproduceerbaar.
* \[ ] Geen secrets in archives.
* \[ ] Data growth budget gebruikt metrics retention.

\---

## 17\. Fase 14 - Metrics Evidence Bundle

Doel: observability bewijs exporteerbaar maken.

### Nieuwe module

```text
src/binance\_spot\_bot/metrics\_evidence\_bundle.py
```

### Bundle bevat

* \[ ] raw metrics sample;
* \[ ] daily aggregates;
* \[ ] weekly aggregates;
* \[ ] SLO results;
* \[ ] anomaly report;
* \[ ] analytics reports;
* \[ ] metric manifests;
* \[ ] no-live proof;
* \[ ] redaction proof;
* \[ ] hashes.

### Acceptatiecriteria

* \[ ] Bundle is secret-free.
* \[ ] Bundle heeft manifest.
* \[ ] Bundle kan geverifieerd worden.
* \[ ] Dashboard/CLI export werkt.
* \[ ] Bundle ondersteunt toekomstige audits.

\---

## 18\. Fase 15 - Scheduled Analytics Integration

Doel: Roadmap 083 scheduler gebruikt Roadmap 084 analytics.

### Taken

* \[ ] Default scheduled job:

  * metrics ingest daily;
  * metrics aggregate daily;
  * SLO check daily;
  * anomaly detection daily;
  * analytics report daily;
  * weekly analytics report.
* \[ ] Runbook reminders bij:

  * SLO breach;
  * anomaly critical;
  * stale metrics;
  * failed ingest;
  * failed report.
* \[ ] Failure support bundle koppelen aan analytics failure.

### Acceptatiecriteria

* \[ ] Scheduled analytics jobs zijn allowlisted.
* \[ ] Jobs zijn read-only/metrics-only.
* \[ ] Failures maken support bundle indien geconfigureerd.
* \[ ] Dashboard toont last scheduled analytics run.

\---

## 19\. Fase 16 - Tests

### Unit tests

* \[ ] `tests/test\_metrics\_schema.py`
* \[ ] `tests/test\_metrics\_warehouse.py`
* \[ ] `tests/test\_metrics\_collectors.py`
* \[ ] `tests/test\_local\_ops\_metrics.py`
* \[ ] `tests/test\_paper\_performance\_metrics.py`
* \[ ] `tests/test\_governance\_metrics.py`
* \[ ] `tests/test\_metrics\_aggregation.py`
* \[ ] `tests/test\_ops\_slo.py`
* \[ ] `tests/test\_metrics\_anomaly\_detection.py`
* \[ ] `tests/test\_metrics\_cli.py`
* \[ ] `tests/test\_long\_term\_analytics\_report.py`
* \[ ] `tests/test\_metrics\_retention.py`
* \[ ] `tests/test\_metrics\_evidence\_bundle.py`

### Integration tests

* \[ ] Ingest metrics from fake operator report.
* \[ ] Ingest metrics from fake job run.
* \[ ] Ingest metrics from fake session report.
* \[ ] Ingest metrics from fake governance report.
* \[ ] Aggregate daily metrics.
* \[ ] Calculate SLO status.
* \[ ] Detect anomaly.
* \[ ] Export analytics report.
* \[ ] Compact old metrics.
* \[ ] Export metrics evidence bundle.

### Safety tests

* \[ ] Metrics labels redact secrets.
* \[ ] Metrics warehouse contains no secrets.
* \[ ] Metrics commands call no signed endpoints.
* \[ ] Metrics commands cannot enable live.
* \[ ] Remote export is blocked.
* \[ ] Reports/bundles are secret-free.
* \[ ] No-live proof remains true.

\---

## 20\. Docs

Nieuwe docs:

* \[ ] `docs/local-observability-safety-contract.md`
* \[ ] `docs/metrics-event-schema.md`
* \[ ] `docs/local-metrics-warehouse.md`
* \[ ] `docs/metrics-collectors.md`
* \[ ] `docs/local-ops-metrics.md`
* \[ ] `docs/paper-performance-metrics.md`
* \[ ] `docs/governance-metrics.md`
* \[ ] `docs/metrics-aggregation.md`
* \[ ] `docs/paper-ops-slo.md`
* \[ ] `docs/metrics-anomaly-detection.md`
* \[ ] `docs/metrics-query-cli.md`
* \[ ] `docs/local-observability-dashboard.md`
* \[ ] `docs/long-term-analytics-reports.md`
* \[ ] `docs/metrics-retention-compaction.md`
* \[ ] `docs/metrics-evidence-bundle.md`

README updates:

* \[ ] metrics ingest/query commands;
* \[ ] observability dashboard uitleg;
* \[ ] SLO uitleg;
* \[ ] anomaly detection uitleg;
* \[ ] metrics retention uitleg;
* \[ ] no-live statement.

\---

## 21\. Codex bouwvolgorde

### PR 1 - Metrics Event Schema + Warehouse

* \[ ] `metrics\_schema.py`
* \[ ] `metrics\_warehouse.py`
* \[ ] JSONL append/query.
* \[ ] manifest/hash.
* \[ ] tests.

### PR 2 - Metrics Collectors

* \[ ] operator/report/job/session/evidence collectors.
* \[ ] fixture tests.
* \[ ] redaction tests.

### PR 3 - Local Ops Metrics

* \[ ] scheduled job metrics.
* \[ ] report freshness metrics.
* \[ ] failure metrics.

### PR 4 - Paper/Governance Metrics

* \[ ] paper performance metrics.
* \[ ] governance metrics.
* \[ ] trend-ready outputs.

### PR 5 - Aggregation Engine

* \[ ] daily aggregations.
* \[ ] weekly aggregations.
* \[ ] manifest outputs.

### PR 6 - SLO Layer

* \[ ] SLO config.
* \[ ] SLO calculator.
* \[ ] breach reason codes.

### PR 7 - Anomaly Detection

* \[ ] threshold/rolling/stale anomalies.
* \[ ] recommended actions.
* \[ ] tests.

### PR 8 - CLI Commands

* \[ ] metrics-ingest/query/latest/aggregate/slo/anomalies/export/compact.
* \[ ] safety tests.

### PR 9 - Dashboard + Reports

* \[ ] Local Observability dashboard panel.
* \[ ] long-term analytics reports.
* \[ ] browser smoke.

### PR 10 - Retention + Evidence + Scheduler Integration

* \[ ] metrics retention.
* \[ ] evidence bundle.
* \[ ] scheduled analytics integration.
* \[ ] docs.

\---

## 22\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 084 PR 1: Metrics Event Schema + Local Metrics Warehouse.

Maak src/binance\_spot\_bot/metrics\_schema.py met MetricEvent, MetricPoint, MetricSeries, MetricIngestResult, MetricAggregation en MetricAnomaly.
Maak src/binance\_spot\_bot/metrics\_warehouse.py met JSONL storage onder data/metrics/metrics.jsonl.
Ondersteun append\_metric, append\_many, query\_metrics, latest\_metric, aggregate\_daily stub, write\_manifest en verify\_manifest.
Zorg dat alle metrics redacted zijn, live\_trading\_enabled=False bevatten en geen secrets in labels/values opslaan.
Voeg tests toe voor:
- metric serialization
- append/query/latest
- manifest hash
- secret redaction
- no-live flag

Geen API calls, geen signed endpoints, geen orders, geen live trading.
```

Waarom eerst:

* alle observability bouwt op een stabiel metric event format;
* warehouse is nodig voordat collectors/aggregaties/dashboard kunnen werken;
* het raakt geen trading runtime;
* het is klein genoeg voor Codex;
* safety/redaction kan meteen getest worden.

\---

## 23\. Definition of Done

Roadmap 084 is klaar als:

* \[ ] Observability Safety Contract bestaat.
* \[ ] Metrics Event Schema werkt.
* \[ ] Local Metrics Warehouse werkt.
* \[ ] Metrics Collectors werken.
* \[ ] Local Ops Metrics Ingestion werkt.
* \[ ] Paper Performance Metrics Ingestion werkt.
* \[ ] Governance Metrics Ingestion werkt.
* \[ ] Daily/Weekly Aggregation Engine werkt.
* \[ ] Paper Ops SLO/SLA Layer werkt.
* \[ ] Anomaly Detection werkt.
* \[ ] Metrics Query CLI werkt.
* \[ ] Observability Dashboard Panel werkt.
* \[ ] Long-Term Analytics Reports werken.
* \[ ] Metrics Retention \& Compaction werkt.
* \[ ] Metrics Evidence Bundle werkt.
* \[ ] Scheduled Analytics Integration werkt.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Metrics/reports/bundles zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 084 kan na uitvoering naar `Voltooid docs`.

\---

## 24\. Verwachte Roadmap 085 daarna

Na Roadmap 084 zou Roadmap 085 logisch focussen op:

```text
Roadmap 085 - Local AI Ops Assistant, Natural Language Queries \& Safe Operator Guidance
```

Mogelijke inhoud:

* \[ ] lokale vraag-en-antwoord over metrics/reports;
* \[ ] natural language query over paper ops;
* \[ ] safe operator guidance;
* \[ ] no-secrets context builder;
* \[ ] action suggestions zonder automatische execution;
* \[ ] incident explanation;
* \[ ] still no live trading.



---

## Afwerking

Status: Niet volledig voltooid / opnieuw gepland op 2026-05-11.

Implementatie/evidence: docs/roadmap-076-102-execution-evidence.md, src/binance_spot_bot/paper_os.py, 	ests/test_roadmaps_076_102_paper_os.py.

Validatie: gerichte tests groen, volledige pytest groen, check-all opnieuw uitgevoerd na verplaatsing.



---

## Correctie-audit 2026-05-11

Deze roadmap is teruggezet naar Roadmap docs/ omdat de eerdere markering als Voltooid te breed was. De huidige code bevat alleen een gedeelde foundation in src/binance_spot_bot/paper_os.py en regressietests in 	ests/test_roadmaps_076_102_paper_os.py. Niet alle checklistpunten uit deze roadmap zijn volledig als production-grade feature geimplementeerd.

Open status: opnieuw plannen, opdelen in kleinere uitvoerbare taken, en pas opnieuw naar Voltooid docs/ verplaatsen na concrete implementatie en validatie per roadmap.

---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: metric schema, metrics warehouse/reporting, artifact/local ops/paper/governance metrics, aggregation, SLO, anomaly detection, long-term analytics report, retention plan, evidence bundle, dashboardtab `Observability`, CLI smoke via `metrics-warehouse-report`.

Validatie: `tests/test_roadmaps_083_088_full_surface.py`, `tests/test_roadmaps_082_088_ops_governance.py`, dashboard-smoke en CLI smoke.

Safety: local-only metrics, redacted reports, no live trading.

