# Roadmap 083 - Local Paper Operations Automation, Scheduled Reports \& Operator Runbooks

Status: Niet volledig voltooid / opnieuw gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/083-roadmap-local-paper-operations-automation-scheduled-reports-operator-runbooks.md
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

Doel: Roadmap 082 maakt paper policy rollout, A/B paper experiments en champion/challenger governance mogelijk. Roadmap 083 maakt dit dagelijks bruikbaar door lokale paper operations te automatiseren: scheduled reports, local job runner, health checks, operator runbooks, incident workflows, automatic support bundles, evidence reminders en dashboard/CLI control voor lokale taken.

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
* \[x] Geen bestaande Roadmap 083 gevonden via repo-search.
* \[x] Roadmap 076 is lokaal aangemaakt voor Binance public data ingestion.
* \[x] Roadmap 077 is lokaal aangemaakt voor backtest/calibration/confidence.
* \[x] Roadmap 078 is lokaal aangemaakt voor paper deployment/rollback.
* \[x] Roadmap 079 is lokaal aangemaakt voor paper portfolio operations.
* \[x] Roadmap 080 is lokaal aangemaakt voor stress testing/scenario replay.
* \[x] Roadmap 081 is lokaal aangemaakt voor paper portfolio optimization.
* \[x] Roadmap 082 is lokaal aangemaakt voor paper policy governance.

### Codebasecontrole

Gecontroleerde relevante modules:

* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/model\_registry.py`
* \[x] bestaande CLI heeft al veel operator-achtige commands:

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
  * rehearsal-profiles;
  * operator-report-diff;
  * support-bundle-restore-preview;
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

### Belangrijkste gat na Roadmap 082

Na Roadmap 082 heb je policy governance, maar nog geen volledige dagelijkse lokale operations-automatisering:

* \[ ] Geen lokale scheduler/job runner voor terugkerende paper taken.
* \[ ] Geen daily/weekly scheduled report plans.
* \[ ] Geen operator runbooks als machine-readable flows.
* \[ ] Geen automatic support bundle on failure.
* \[ ] Geen governance reminders.
* \[ ] Geen morning/evening checklist.
* \[ ] Geen local Windows Task Scheduler integratie.
* \[ ] Geen paper operations calendar.
* \[ ] Geen retry/backoff policy voor lokale jobs.
* \[ ] Geen job history dashboard.
* \[ ] Geen incident drill automation.
* \[ ] Geen scheduled evidence validation.

\---

## 1\. Hoofddoel Roadmap 083

Maak een lokale operator automation-laag:

```text
Paper governance
→ local task plans
→ scheduled paper reports
→ health checks
→ runbooks
→ support bundles on failure
→ evidence reminders
→ operator dashboard
→ weekly ops review
```

Na Roadmap 083 moet de bot:

* \[ ] lokale scheduled jobs kunnen definiëren;
* \[ ] paper-only daily reports automatisch genereren;
* \[ ] governance reminders tonen;
* \[ ] health checks periodiek draaien;
* \[ ] failure bundles automatisch maken;
* \[ ] operator runbooks aanbieden;
* \[ ] incident timelines automatisch vullen;
* \[ ] Windows Task Scheduler scripts genereren;
* \[ ] job history en status tonen;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen cloud scheduler.
* \[ ] Geen externe telemetry.
* \[ ] Geen live trading.
* \[ ] Geen signed order endpoints.
* \[ ] Geen Binance account endpoints.
* \[ ] Geen nieuwe policy governance engine; Roadmap 082 doet dat.
* \[ ] Geen nieuwe portfolio optimizer; Roadmap 081 doet dat.
* \[ ] Geen nieuwe dashboard-app.
* \[ ] Geen background service die orders kan plaatsen.
* \[ ] Geen secrets in scheduled tasks.

Wel doen:

* \[ ] bestaande CLI operator commands orkestreren;
* \[ ] lokale job runner toevoegen;
* \[ ] scheduled report definitions maken;
* \[ ] runbooks documenteren en machine-readable maken;
* \[ ] support bundle automation toevoegen;
* \[ ] dashboard operations panel uitbreiden;
* \[ ] Windows helper scripts genereren;
* \[ ] alles paper/demo/read-only houden.

\---

## 3\. Fase 0 - Local Ops Safety Contract

Doel: garanderen dat automation alleen veilige lokale paper/read-only taken uitvoert.

### Nieuwe doc

```text
docs/local-paper-ops-automation-safety-contract.md
```

### Regels

* \[ ] Scheduler mag alleen allowlisted commands uitvoeren.
* \[ ] Allowlisted commands moeten paper/read-only zijn.
* \[ ] Geen command met live mode.
* \[ ] Geen signed order endpoint.
* \[ ] Geen account endpoint.
* \[ ] Geen API secrets in task definitions.
* \[ ] Geen external telemetry.
* \[ ] Geen remote upload.
* \[ ] Support bundles worden redacted.
* \[ ] Jobs mogen risico verlagen, nooit verhogen.
* \[ ] Dangerous paper actions vereisen manual confirmation en mogen niet unattended draaien.

### Acceptatiecriteria

* \[ ] Safety contract bestaat.
* \[ ] Scheduler heeft command allowlist.
* \[ ] Tests bewijzen dat live/signed commands geweigerd worden.
* \[ ] Dashboard toont `LOCAL PAPER OPS ONLY`.
* \[ ] Task definitions bevatten geen secrets.

\---

## 4\. Fase 1 - Local Job Definition Schema

Doel: lokale paper jobs als data vastleggen.

### Nieuwe module

```text
src/binance\_spot\_bot/local\_jobs.py
```

### Dataclasses

* \[ ] `LocalJobDefinition`
* \[ ] `LocalJobSchedule`
* \[ ] `LocalJobRun`
* \[ ] `LocalJobResult`
* \[ ] `LocalJobAllowlistRule`
* \[ ] `LocalJobFailurePolicy`

### JobDefinition velden

* \[ ] job\_id;
* \[ ] name;
* \[ ] description;
* \[ ] command;
* \[ ] args;
* \[ ] schedule\_type:

  * manual;
  * daily;
  * weekly;
  * interval;
  * on\_startup;
  * on\_failure;
  * on\_shutdown.
* \[ ] schedule\_config;
* \[ ] enabled;
* \[ ] category:

  * report;
  * health;
  * evidence;
  * governance;
  * cleanup;
  * diagnostics;
  * drill.
* \[ ] allowlist\_policy;
* \[ ] max\_runtime\_seconds;
* \[ ] retry\_policy;
* \[ ] failure\_policy;
* \[ ] output\_dir;
* \[ ] created\_at\_ms;
* \[ ] updated\_at\_ms.

### Acceptatiecriteria

* \[ ] Jobs zijn JSON-serializable.
* \[ ] Job schema bevat geen secrets.
* \[ ] Invalid commands worden geweigerd.
* \[ ] Disabled jobs draaien niet.
* \[ ] Tests dekken valid/invalid schedules.

\---

## 5\. Fase 2 - Command Allowlist \& Safety Validator

Doel: alleen veilige CLI commands kunnen scheduled draaien.

### Nieuwe module

```text
src/binance\_spot\_bot/local\_job\_allowlist.py
```

### Default allowlist

Toegestaan:

* \[ ] `diagnostics`
* \[ ] `support-bundle`
* \[ ] `support-bundle-verify`
* \[ ] `operator-report`
* \[ ] `operator-quality-gate`
* \[ ] `operator-health-score`
* \[ ] `artifact-catalog`
* \[ ] `evidence-chain`
* \[ ] `evidence-manifest`
* \[ ] `report-index`
* \[ ] `redaction-self-test`
* \[ ] `local-ops-snapshot`
* \[ ] `dashboard-smoke`
* \[ ] `dashboard-browser-smoke`
* \[ ] `paper-session` alleen met safe max limits en mode paper/demo
* \[ ] Roadmap 082 governance reports/exports zodra beschikbaar.

Verboden:

* \[ ] live mode;
* \[ ] signed orders;
* \[ ] account queries;
* \[ ] cancel/place/query real order;
* \[ ] commands met onbekende executable;
* \[ ] shell injection;
* \[ ] external upload;
* \[ ] commands met secrets in args;
* \[ ] destructive cleanup zonder confirm.

### Acceptatiecriteria

* \[ ] Allowlist blokkeert onbekende commands.
* \[ ] Allowlist blokkeert live/signed/order/account commands.
* \[ ] Allowlist blokkeert shell injection.
* \[ ] Allowlist redaction self-test draait in check-all.
* \[ ] Tests dekken allow/deny cases.

\---

## 6\. Fase 3 - Local Job Store

Doel: jobs, runs en outputs lokaal beheren.

### Nieuwe module

```text
src/binance\_spot\_bot/local\_job\_store.py
```

### Storage

```text
data/local-jobs/
  jobs.json
  runs/
    <job\_id>/
      <run\_id>/
        run.json
        stdout.txt
        stderr.txt
        result.json
        artifacts/
```

### Taken

* \[ ] Save/load job definitions.
* \[ ] Append job run.
* \[ ] Track last success/failure.
* \[ ] Store stdout/stderr redacted.
* \[ ] Store artifacts paths.
* \[ ] Prune old runs with retention preview.
* \[ ] Export job history.

### Acceptatiecriteria

* \[ ] Job history blijft lokaal.
* \[ ] Failures zijn zichtbaar.
* \[ ] Outputs zijn redacted.
* \[ ] Retention preview werkt vóór delete/archive.
* \[ ] Geen secrets in store.

\---

## 7\. Fase 4 - Local Job Runner

Doel: jobs veilig uitvoeren.

### Nieuwe module

```text
src/binance\_spot\_bot/local\_job\_runner.py
```

### Runner behavior

* \[ ] Validate job via allowlist.
* \[ ] Prepare safe environment:

  * `LIVE\_TRADING\_ENABLED=false`;
  * `KILL\_SWITCH=true`;
  * no API secret env exposure where possible.
* \[ ] Execute command with timeout.
* \[ ] Capture stdout/stderr.
* \[ ] Redact output.
* \[ ] Parse JSON output when possible.
* \[ ] Write result artifact.
* \[ ] Trigger failure policy.
* \[ ] Update job store.
* \[ ] Return structured result.

### Failure policies

* \[ ] record only;
* \[ ] create support bundle;
* \[ ] create incident timeline;
* \[ ] notify dashboard;
* \[ ] disable job after N failures;
* \[ ] run diagnostics;
* \[ ] run redaction self-test.

### Acceptatiecriteria

* \[ ] Runner executes safe commands.
* \[ ] Runner rejects unsafe commands.
* \[ ] Timeout kills job safely.
* \[ ] Failure creates support bundle if configured.
* \[ ] No live trading env leaks.

\---

## 8\. Fase 5 - Scheduler Engine

Doel: bepalen welke jobs wanneer moeten draaien.

### Nieuwe module

```text
src/binance\_spot\_bot/local\_scheduler.py
```

### Modes

* \[ ] CLI one-shot tick;
* \[ ] foreground loop;
* \[ ] dashboard manual trigger;
* \[ ] Windows Task Scheduler wrapper;
* \[ ] startup check.

### Schedule types

* \[ ] daily at HH:MM;
* \[ ] weekly on weekday;
* \[ ] interval minutes/hours;
* \[ ] on startup;
* \[ ] after paper session stop;
* \[ ] after governance decision;
* \[ ] on failure.

### Acceptatiecriteria

* \[ ] Scheduler kan due jobs vinden.
* \[ ] Scheduler draait jobs één voor één of met veilige concurrency limit.
* \[ ] Scheduler voorkomt dubbele runs via lockfile.
* \[ ] Scheduler heeft dry-run mode.
* \[ ] Tests gebruiken fake clock.

\---

## 9\. Fase 6 - Scheduled Report Plans

Doel: daily/weekly reports automatiseren.

### Nieuwe module

```text
src/binance\_spot\_bot/scheduled\_reports.py
```

### Default report jobs

Daily:

* \[ ] daily paper deployment report;
* \[ ] daily portfolio report;
* \[ ] daily data quality report;
* \[ ] daily local ops snapshot;
* \[ ] daily operator health score;
* \[ ] daily evidence manifest.

Weekly:

* \[ ] weekly governance report;
* \[ ] weekly policy comparison;
* \[ ] weekly benchmark summary;
* \[ ] weekly support bundle verify;
* \[ ] weekly data growth budget;
* \[ ] weekly report index.

### Acceptatiecriteria

* \[ ] Default report plan kan gegenereerd worden.
* \[ ] Reports draaien met allowlisted commands.
* \[ ] Failed report maakt failure event.
* \[ ] Reports zijn secret-free.
* \[ ] Dashboard toont last generated status.

\---

## 10\. Fase 7 - Operator Runbook System

Doel: runbooks machine-readable en uitvoerbaar maken.

### Nieuwe module

```text
src/binance\_spot\_bot/operator\_runbooks.py
```

### Runbook types

* \[ ] morning check;
* \[ ] evening review;
* \[ ] dashboard crash;
* \[ ] data unavailable;
* \[ ] degraded data quality;
* \[ ] failed paper session;
* \[ ] failed scheduled report;
* \[ ] policy challenger failed;
* \[ ] rollback required;
* \[ ] evidence missing;
* \[ ] support bundle required;
* \[ ] cache/data growth too large;
* \[ ] browser smoke failed.

### Runbook schema

* \[ ] runbook\_id;
* \[ ] title;
* \[ ] trigger;
* \[ ] severity;
* \[ ] steps;
* \[ ] commands;
* \[ ] expected outputs;
* \[ ] escalation;
* \[ ] done criteria;
* \[ ] safety notes.

### Acceptatiecriteria

* \[ ] Runbooks zijn JSON/Markdown exporteerbaar.
* \[ ] Dashboard kan runbook tonen.
* \[ ] Runbook commands zijn allowlisted.
* \[ ] Operator kan stappen afvinken.
* \[ ] Completion wordt gelogd.

\---

## 11\. Fase 8 - Automatic Support Bundle on Failure

Doel: bij problemen automatisch bewijs verzamelen.

### Uitbreiding

Bestaande support-bundle command gebruiken, maar triggeren via job failure.

### Taken

* \[ ] Failure policy `create\_support\_bundle`.
* \[ ] Bundle bevat:

  * failed job definition;
  * run result;
  * stdout/stderr redacted;
  * diagnostics;
  * operator report;
  * health score;
  * evidence manifest;
  * recent logs;
  * recent reports.
* \[ ] Bundle verify direct na creatie.
* \[ ] Dashboard link naar bundle.
* \[ ] Incident timeline event toevoegen.

### Acceptatiecriteria

* \[ ] Failure bundle wordt gemaakt bij configured jobs.
* \[ ] Bundle is secret-free.
* \[ ] Bundle verify slaagt.
* \[ ] Incident timeline linkt naar bundle.
* \[ ] No external upload.

\---

## 12\. Fase 9 - Governance Reminders

Doel: operator herinneren aan open governance/paper tasks.

### Nieuwe module

```text
src/binance\_spot\_bot/governance\_reminders.py
```

### Reminders

* \[ ] challenger experiment needs review;
* \[ ] weekly governance report due;
* \[ ] policy evidence missing;
* \[ ] paper policy approval pending;
* \[ ] rollback decision unresolved;
* \[ ] stale benchmark evidence;
* \[ ] failed scheduled report;
* \[ ] support bundle needs review;
* \[ ] data cache stale;
* \[ ] browser smoke stale;
* \[ ] check-all stale.

### Acceptatiecriteria

* \[ ] Reminders zijn lokaal.
* \[ ] Dashboard toont due reminders.
* \[ ] CLI kan reminders exporteren.
* \[ ] Reminders bevatten geen secrets.
* \[ ] No external notifications in this roadmap.

\---

## 13\. Fase 10 - Paper Operations Calendar

Doel: overzicht van alle lokale paper ops taken.

### Nieuwe module

```text
src/binance\_spot\_bot/paper\_ops\_calendar.py
```

### Calendar items

* \[ ] scheduled jobs;
* \[ ] report due dates;
* \[ ] governance review dates;
* \[ ] experiment end dates;
* \[ ] support bundle review;
* \[ ] data retention review;
* \[ ] evidence expiry;
* \[ ] browser smoke schedule.

### Output

* \[ ] JSON calendar;
* \[ ] Markdown calendar;
* \[ ] dashboard calendar table;
* \[ ] optional `.ics` export for local calendar import.

### Acceptatiecriteria

* \[ ] Calendar werkt offline.
* \[ ] Calendar bevat geen secrets.
* \[ ] Dashboard toont upcoming tasks.
* \[ ] ICS export is optional and local-only.

\---

## 14\. Fase 11 - Windows Task Scheduler Integration

Doel: lokale Windows-scheduled jobs makkelijker instellen.

### Nieuwe module

```text
src/binance\_spot\_bot/windows\_task\_scheduler.py
```

### Scripts

```text
scripts/install-local-ops-scheduler.ps1
scripts/uninstall-local-ops-scheduler.ps1
scripts/run-local-ops-tick.ps1
scripts/run-daily-paper-report.ps1
scripts/run-weekly-governance-report.ps1
```

### Taken

* \[ ] Generate Task Scheduler XML/PowerShell.
* \[ ] Dry-run output.
* \[ ] Install daily local scheduler tick.
* \[ ] Install weekly governance report.
* \[ ] Uninstall tasks.
* \[ ] Show task status.
* \[ ] Use safe env:

  * `LIVE\_TRADING\_ENABLED=false`;
  * `KILL\_SWITCH=true`.

### Acceptatiecriteria

* \[ ] Scripts werken met paths met spaties.
* \[ ] Install/uninstall vraagt confirmation.
* \[ ] Tasks draaien alleen allowlisted CLI.
* \[ ] Geen secrets in task XML.
* \[ ] Docs voor Windows setup.

\---

## 15\. Fase 12 - Operations Dashboard Panel

Doel: alles bedienen zonder raw JSON.

### Nieuwe/uitgebreide dashboardsectie

```text
Local Paper Operations
```

### Panels

* \[ ] local job status;
* \[ ] next scheduled jobs;
* \[ ] last job runs;
* \[ ] failed jobs;
* \[ ] scheduled reports;
* \[ ] governance reminders;
* \[ ] runbooks;
* \[ ] support bundles on failure;
* \[ ] paper ops calendar;
* \[ ] Windows scheduler status;
* \[ ] health score;
* \[ ] evidence freshness.

### Actions

* \[ ] run due jobs now;
* \[ ] run one job;
* \[ ] disable/enable job;
* \[ ] generate default schedule;
* \[ ] export calendar;
* \[ ] create support bundle;
* \[ ] open runbook;
* \[ ] mark runbook step done;
* \[ ] install/uninstall Windows tasks;
* \[ ] export ops report.

### Acceptatiecriteria

* \[ ] Dashboard toont `LOCAL PAPER OPS ONLY`.
* \[ ] Dangerous actions require confirmation.
* \[ ] Raw JSON only in debug expanders.
* \[ ] Browser smoke covers panel.
* \[ ] No live controls.

\---

## 16\. Fase 13 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli local-job-list
python -m binance\_spot\_bot.cli local-job-create-defaults
python -m binance\_spot\_bot.cli local-job-run --job-id <id>
python -m binance\_spot\_bot.cli local-scheduler-tick
python -m binance\_spot\_bot.cli local-scheduler-loop --minutes 60
python -m binance\_spot\_bot.cli scheduled-report-plan --default
python -m binance\_spot\_bot.cli runbook-list
python -m binance\_spot\_bot.cli runbook-show --runbook-id <id>
python -m binance\_spot\_bot.cli governance-reminders
python -m binance\_spot\_bot.cli paper-ops-calendar
python -m binance\_spot\_bot.cli windows-scheduler-install --confirm INSTALL\_LOCAL\_OPS
python -m binance\_spot\_bot.cli windows-scheduler-uninstall --confirm UNINSTALL\_LOCAL\_OPS
```

### Acceptatiecriteria

* \[ ] Commands werken zonder API keys.
* \[ ] Commands ondersteunen JSON output.
* \[ ] Commands gebruiken allowlist.
* \[ ] Scheduler commands weigeren live/signed routes.
* \[ ] Confirm vereist voor install/uninstall.

\---

## 17\. Fase 14 - Local Ops Reports \& Evidence

### Nieuwe output

```text
data/local-ops/
  scheduler/
  jobs/
  runbooks/
  calendars/
  reports/
  evidence/
```

### Reports

* \[ ] `local\_ops\_daily\_report.md`
* \[ ] `local\_ops\_daily\_report.json`
* \[ ] `scheduled\_jobs\_status.csv`
* \[ ] `failed\_jobs.jsonl`
* \[ ] `runbook\_completions.jsonl`
* \[ ] `governance\_reminders.json`
* \[ ] `paper\_ops\_calendar.md`
* \[ ] `local\_ops\_evidence\_manifest.json`

### Acceptatiecriteria

* \[ ] Reports zijn secret-free.
* \[ ] Evidence manifest heeft hashes.
* \[ ] Dashboard kan reports downloaden.
* \[ ] Support bundle linkt reports.

\---

## 18\. Fase 15 - Runbook Drill Suite

Doel: operator workflows testen voordat het misgaat.

### Nieuwe module

```text
src/binance\_spot\_bot/runbook\_drills.py
```

### Drills

* \[ ] dashboard crash drill;
* \[ ] failed scheduled report drill;
* \[ ] data quality degraded drill;
* \[ ] support bundle drill;
* \[ ] governance review overdue drill;
* \[ ] evidence missing drill;
* \[ ] browser smoke failed drill;
* \[ ] rollback required drill.

### Acceptatiecriteria

* \[ ] Drills draaien offline.
* \[ ] Drills genereren fake incidents.
* \[ ] Expected runbook wordt gekozen.
* \[ ] Completion wordt gelogd.
* \[ ] No live mode.

\---

## 19\. Fase 16 - Retention \& Data Growth Automation

Doel: lokale data beheersbaar houden.

### Uitbreiding op bestaande operator commands

* \[ ] `retention-preview`
* \[ ] `state-archive`
* \[ ] `data-growth-budget`
* \[ ] `artifact-catalog`
* \[ ] `report-index`

### Taken

* \[ ] Scheduled retention preview.
* \[ ] Scheduled state archive.
* \[ ] Data growth warning.
* \[ ] Stale report warning.
* \[ ] Large cache warning.
* \[ ] No automatic destructive delete without confirm.
* \[ ] Dashboard cleanup recommendations.

### Acceptatiecriteria

* \[ ] Data cleanup is preview-first.
* \[ ] Destructive actions require confirmation.
* \[ ] Archive output is secret-free.
* \[ ] Data growth warning appears in dashboard.

\---

## 20\. Fase 17 - Tests

### Unit tests

* \[ ] `tests/test\_local\_jobs.py`
* \[ ] `tests/test\_local\_job\_allowlist.py`
* \[ ] `tests/test\_local\_job\_store.py`
* \[ ] `tests/test\_local\_job\_runner.py`
* \[ ] `tests/test\_local\_scheduler.py`
* \[ ] `tests/test\_scheduled\_reports.py`
* \[ ] `tests/test\_operator\_runbooks.py`
* \[ ] `tests/test\_failure\_support\_bundle.py`
* \[ ] `tests/test\_governance\_reminders.py`
* \[ ] `tests/test\_paper\_ops\_calendar.py`
* \[ ] `tests/test\_windows\_task\_scheduler.py`
* \[ ] `tests/test\_runbook\_drills.py`

### Integration tests

* \[ ] Create default local jobs.
* \[ ] Run scheduler dry-run.
* \[ ] Run one safe job.
* \[ ] Reject unsafe job.
* \[ ] Simulate failed job and support bundle creation.
* \[ ] Generate daily report plan.
* \[ ] Generate governance reminders.
* \[ ] Export paper ops calendar.
* \[ ] Generate Windows scheduler script.
* \[ ] Run runbook drill.

### Safety tests

* \[ ] Scheduler rejects live mode.
* \[ ] Scheduler rejects signed/order/account commands.
* \[ ] Job args cannot contain secrets.
* \[ ] Job output is redacted.
* \[ ] Support bundle is secret-free.
* \[ ] Destructive cleanup requires confirmation.
* \[ ] Live disabled remains true.

\---

## 21\. Docs

Nieuwe docs:

* \[ ] `docs/local-paper-ops-automation-safety-contract.md`
* \[ ] `docs/local-job-schema.md`
* \[ ] `docs/local-job-allowlist.md`
* \[ ] `docs/local-scheduler.md`
* \[ ] `docs/scheduled-reports.md`
* \[ ] `docs/operator-runbooks.md`
* \[ ] `docs/failure-support-bundles.md`
* \[ ] `docs/governance-reminders.md`
* \[ ] `docs/paper-ops-calendar.md`
* \[ ] `docs/windows-task-scheduler-local-ops.md`
* \[ ] `docs/local-ops-dashboard.md`
* \[ ] `docs/runbook-drills.md`
* \[ ] `docs/retention-data-growth-automation.md`

README updates:

* \[ ] local ops commands;
* \[ ] Windows scheduler setup;
* \[ ] scheduled reports;
* \[ ] runbooks;
* \[ ] failure support bundle flow;
* \[ ] no-live statement.

\---

## 22\. Codex bouwvolgorde

### PR 1 - Local Job Schema + Allowlist

* \[ ] `local\_jobs.py`
* \[ ] `local\_job\_allowlist.py`
* \[ ] safety tests.

### PR 2 - Job Store + Runner

* \[ ] `local\_job\_store.py`
* \[ ] `local\_job\_runner.py`
* \[ ] run output/redaction;
* \[ ] failure policy base.

### PR 3 - Scheduler Engine

* \[ ] `local\_scheduler.py`
* \[ ] fake clock tests;
* \[ ] lockfile;
* \[ ] dry-run.

### PR 4 - Scheduled Reports

* \[ ] `scheduled\_reports.py`
* \[ ] default daily/weekly plans;
* \[ ] report job tests.

### PR 5 - Operator Runbooks

* \[ ] `operator\_runbooks.py`
* \[ ] JSON/Markdown runbooks;
* \[ ] runbook dashboard payload.

### PR 6 - Failure Support Bundles

* \[ ] support bundle on job failure;
* \[ ] verify bundle;
* \[ ] incident timeline event.

### PR 7 - Governance Reminders + Calendar

* \[ ] reminders;
* \[ ] paper ops calendar;
* \[ ] optional ICS export.

### PR 8 - Windows Task Scheduler Scripts

* \[ ] PowerShell scripts;
* \[ ] install/uninstall dry-run;
* \[ ] docs.

### PR 9 - Operations Dashboard Panel

* \[ ] job status UI;
* \[ ] runbooks UI;
* \[ ] scheduled reports UI;
* \[ ] browser smoke.

### PR 10 - Drills + Retention Automation + Docs

* \[ ] runbook drills;
* \[ ] retention automation;
* \[ ] docs;
* \[ ] check-all integration.

\---

## 23\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 083 PR 1: Local Job Schema + Command Allowlist.

Maak src/binance\_spot\_bot/local\_jobs.py met LocalJobDefinition, LocalJobSchedule, LocalJobRun, LocalJobResult en LocalJobFailurePolicy.
Maak src/binance\_spot\_bot/local\_job\_allowlist.py met een allowlist voor veilige bestaande CLI commands zoals diagnostics, operator-report, operator-quality-gate, operator-health-score, evidence-manifest, report-index, redaction-self-test, local-ops-snapshot en dashboard-smoke.

Blokkeer:
- live mode
- signed/order/account commands
- shell injection
- commands met secrets in args
- onbekende commands

Voeg tests toe voor allow/deny cases.
Geen scheduler loop bouwen in deze PR.
Geen API calls, geen signed endpoints, geen orders, geen live trading.
```

Waarom eerst:

* Zonder job schema en allowlist is scheduler onveilig.
* Het bouwt voort op bestaande operator CLI commands.
* Het raakt geen trading runtime.
* Het is klein genoeg voor Codex.
* Safety kan meteen hard getest worden.

\---

## 24\. Definition of Done

Roadmap 083 is klaar als:

* \[ ] Local Ops Safety Contract bestaat.
* \[ ] Local Job Schema bestaat.
* \[ ] Command Allowlist werkt.
* \[ ] Local Job Store werkt.
* \[ ] Local Job Runner werkt.
* \[ ] Scheduler Engine werkt.
* \[ ] Scheduled Report Plans werken.
* \[ ] Operator Runbook System werkt.
* \[ ] Automatic Support Bundle on Failure werkt.
* \[ ] Governance Reminders werken.
* \[ ] Paper Ops Calendar werkt.
* \[ ] Windows Task Scheduler scripts werken.
* \[ ] Operations Dashboard Panel werkt.
* \[ ] Local Ops Reports/Evidence werken.
* \[ ] Runbook Drill Suite werkt.
* \[ ] Retention/Data Growth Automation werkt.
* \[ ] CLI commands werken.
* \[ ] Tests bewijzen geen live/signed/order/account endpoints.
* \[ ] Reports/bundles zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 083 kan na uitvoering naar `Voltooid docs`.

\---

## 25\. Verwachte Roadmap 084 daarna

Na Roadmap 083 zou Roadmap 084 logisch focussen op:

```text
Roadmap 084 - Local Paper Ops Observability, Metrics Warehouse \& Long-Term Analytics
```

Mogelijke inhoud:

* \[ ] lokale metrics warehouse;
* \[ ] long-term paper performance analytics;
* \[ ] scheduled analytics dashboards;
* \[ ] trend/drift over weken;
* \[ ] ops SLA metrics;
* \[ ] storage-efficient historical summaries;
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

Status: Voltooid na herimplementatie en hercontrole.

Gebouwd: local job schema, command allowlist, job store, runner, scheduler tick/dry-run, scheduled report plans, operator runbooks, governance reminders, paper ops calendar, Windows Task Scheduler script generation, runbook drills, local ops CLI commands en dashboardtab `Ops Automation`.

Docs: `docs/local-paper-ops-automation-safety-contract.md`, `docs/local-job-schema.md`, `docs/local-job-allowlist.md`, `docs/local-scheduler.md`, `docs/scheduled-reports.md`, `docs/operator-runbooks.md`, `docs/failure-support-bundles.md`, `docs/governance-reminders.md`, `docs/paper-ops-calendar.md`, `docs/windows-task-scheduler-local-ops.md`, `docs/local-ops-dashboard.md`, `docs/runbook-drills.md`, `docs/retention-data-growth-automation.md`.

Validatie:

- `python -m pytest tests/test_roadmap_083_local_ops_acceptance.py tests/test_roadmaps_083_088_full_surface.py tests/test_roadmaps_082_088_ops_governance.py -q` -> 19 passed.
- `python -m pytest -q` -> 307 passed, 1 bestaande PytestCollectionWarning.
- `python -m binance_spot_bot.cli check-all --skip-tests --json` -> ok.
- `python -m binance_spot_bot.cli dashboard-smoke --seconds 1` -> ok.
- `python -m binance_spot_bot.cli dashboard-browser-smoke --url http://127.0.0.1:8506/ --seconds 10` -> ok.
- CLI smoke: local-job-create-defaults, local-job-run, local-scheduler-tick, scheduled-report-plan, runbook-list, governance-reminders, paper-ops-calendar en windows-scheduler-install.

Safety: local/paper-only, unsafe order/live/withdraw commands blocked.

