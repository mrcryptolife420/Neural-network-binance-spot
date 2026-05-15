# Roadmap 093 - Performance Profiling, Runtime Bottleneck Analysis \& Resource Budgeting

Status: Niet volledig voltooid / opnieuw gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/093-roadmap-performance-profiling-runtime-bottleneck-analysis-resource-budgeting.md
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
* `Roadmap docs/084-roadmap-local-paper-ops-observability-metrics-warehouse-long-term-analytics.md`
* `Roadmap docs/085-roadmap-local-ai-ops-assistant-natural-language-queries-safe-operator-guidance.md`
* `Roadmap docs/086-roadmap-safe-human-in-the-loop-action-center-approval-workflows-operator-decision-journal.md`
* `Roadmap docs/087-roadmap-local-permission-profiles-operator-roles-hardening-audit-grade-compliance-reports.md`
* `Roadmap docs/088-roadmap-offline-disaster-recovery-backup-restore-drills-local-state-integrity.md`
* `Roadmap docs/089-roadmap-local-release-management-versioned-upgrade-paths-migration-safety.md`
* `Roadmap docs/090-roadmap-developer-experience-codex-task-packs-roadmap-execution-automation.md`
* `Roadmap docs/091-roadmap-repository-knowledge-graph-code-ownership-impact-analysis.md`
* `Roadmap docs/092-roadmap-intelligent-test-selection-ci-acceleration-regression-risk-scoring.md`

Doel: Roadmap 092 maakt slimme testselectie en regression risk scoring mogelijk. Roadmap 093 bouwt daarop een **performance- en resource-budgetlaag**: runtime profiling, dashboard render profiling, CLI timing, memory/file I/O tracking, data/cache bottleneck detection, slow test/performance regression detection, performance budgets en performance evidence reports. Zo kan de bot niet alleen veilig en correct blijven, maar ook sneller en lichter worden terwijl de codebase groeit.

Live trading blijft volledig buiten scope. Profiling mag nooit live trading activeren, signed endpoints gebruiken of echte account/order endpoints aanraken.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 093`, `093-roadmap`, `Performance Profiling`, `Runtime Bottleneck`, `Resource Budgeting` en `performance budget`.
* \[x] Geen bestaande Roadmap 093 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 092 is lokaal aangemaakt als Intelligent Test Selection, CI Acceleration \& Regression Risk Scoring.
* \[x] Repo-search naar bestaande profiler/performance-budget laag gaf geen bestaande profiler-roadmap/module terug.

### Codebasecontrole

Breed bekeken met performance-focus:

* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/ui/streamlit\_app.py`
* \[x] eerdere brede analyse van `cli.py`, `operator\_ops.py`, `evaluation.py`, `pyproject.toml`
* \[x] bestaande roadmaplijn tot en met Roadmap 092

### Belangrijke bestaande basis

De codebase heeft nu:

* \[x] Een centrale `BotRuntime` met veel runtime-stappen: data source event, data quality, feature rows, model signal, risk decision, paper fill, order lifecycle, demo pilot maintenance, session snapshots en reports.
* \[x] Een check-all flow die commands veilig uitvoert met `LIVE\_TRADING\_ENABLED=false`, `KILL\_SWITCH=true`, timeout, stdout/stderr tails en meerdere operator/security/dashboard checks.
* \[x] Een zeer brede Streamlit dashboard-app met veel imports, tabs, charts, metrics, multi-symbol live fragments, demo/paper controls en operator evidence exports.
* \[x] Een groeiende operator/evidence/reporting-laag met support bundles, evidence manifests, local ops snapshots, report indexes en quality gates.
* \[x] Roadmap 091 plant repository impactanalyse.
* \[x] Roadmap 092 plant intelligente testselectie en runtime history.

### Belangrijkste gat na Roadmap 092

Na Roadmap 092 weet je welke tests je moet draaien en wat regressierisico is. Wat nog mist:

* \[ ] exact meten welke runtime-stap traag is;
* \[ ] exact meten welke dashboard render/panel traag is;
* \[ ] exact meten welke CLI command traag is;
* \[ ] memory- en file-I/O-impact zichtbaar maken;
* \[ ] performance budgets per domein;
* \[ ] slow test/slow command trends;
* \[ ] detectie van performance regressies;
* \[ ] profiling artifacts voor Codex/PR/release;
* \[ ] dashboard performance recommendations;
* \[ ] resource budget enforcement in check-all/check-all-v2;
* \[ ] performance evidence bundels.

Roadmap 093 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 093

Maak een lokale performance- en resource-budgetlaag:

```text
Runtime/CLI/dashboard/test commands
→ profiling wrappers
→ timing/memory/I/O metrics
→ bottleneck reports
→ performance budgets
→ regression detection
→ optimization recommendations
→ evidence bundle
```

Na Roadmap 093 moet de bot kunnen:

* \[ ] runtime step duration meten;
* \[ ] runtime substep duration meten;
* \[ ] dashboard render duration per panel meten;
* \[ ] chart/render bottlenecks detecteren;
* \[ ] CLI command duration meten;
* \[ ] check-all/check-all-v2 duration meten;
* \[ ] memory usage snapshots opslaan;
* \[ ] file I/O hotspots detecteren;
* \[ ] data/cache read/write bottlenecks detecteren;
* \[ ] slow tests en slow commands tracken;
* \[ ] performance budget pass/fail bepalen;
* \[ ] performance regressies rapporteren;
* \[ ] performance reports exporteren;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe runtime engine.
* \[ ] Geen nieuwe dashboard-app.
* \[ ] Geen nieuwe testselector; Roadmap 092 doet dat.
* \[ ] Geen nieuwe repository knowledge graph; Roadmap 091 doet dat.
* \[ ] Geen cloud profiler.
* \[ ] Geen remote telemetry.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen Binance account endpoints.
* \[ ] Geen order endpoints.
* \[ ] Geen profiler die secrets/logs ongefilterd opslaat.
* \[ ] Geen automatische performance refactor zonder operator review.

Wel doen:

* \[ ] lichte lokale profiling utilities toevoegen;
* \[ ] bestaande runtime/dashboard/CLI wrappers instrumenteren;
* \[ ] performance budgets configureren;
* \[ ] reports/evidence maken;
* \[ ] check-all-v2 integratie toevoegen;
* \[ ] dashboard performance panel toevoegen;
* \[ ] Codex/release/testselectie voeden met performance data;
* \[ ] alles local-only en secret-free houden.

\---

## 3\. Fase 0 - Performance Profiling Safety Contract

Nieuwe doc:

```text
docs/performance-profiling-safety-contract.md
```

Regels:

* \[ ] Profiling is local-only.
* \[ ] Geen remote telemetry.
* \[ ] Geen network upload.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen order endpoints.
* \[ ] Profiling wrappers zijn read-only rond timing/memory/I/O.
* \[ ] Profiling mag geen runtime business logic veranderen.
* \[ ] Profiler output is redacted.
* \[ ] Profiler output bevat geen API keys/secrets.
* \[ ] Performance reports bevatten no-live proof.
* \[ ] Performance budget failures mogen build/check blokkeren, maar geen trading acties uitvoeren.
* \[ ] Dashboard toont performance data, maar voert geen live acties uit.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen profiler geen live/signed/order/account commands maakt.
* \[ ] Reports bevatten `live\_trading\_enabled=False`.
* \[ ] Dashboard toont `LOCAL PERFORMANCE PROFILING ONLY`.
* \[ ] Profiler output is secret-free.

\---

## 4\. Fase 1 - Profiling Core Utilities

Nieuwe module:

```text
src/binance\_spot\_bot/profiling\_core.py
```

Dataclasses:

* \[ ] `ProfileSpan`
* \[ ] `ProfileMetric`
* \[ ] `ProfileRun`
* \[ ] `ProfileSummary`
* \[ ] `ProfileBudget`
* \[ ] `ProfileBudgetResult`

Core functies:

* \[ ] `start\_span(name, category, labels)`
* \[ ] `finish\_span(span)`
* \[ ] `profile\_block(name, category, labels)`
* \[ ] `now\_monotonic\_ms()`
* \[ ] `redact\_profile\_payload(...)`
* \[ ] `summarize\_profile\_run(...)`
* \[ ] `write\_profile\_run(...)`

Span velden:

* \[ ] span\_id;
* \[ ] parent\_span\_id;
* \[ ] name;
* \[ ] category:

  * runtime;
  * dashboard;
  * cli;
  * test;
  * io;
  * data;
  * report;
  * evidence;
  * model;
  * risk;
  * execution;
  * unknown.
* \[ ] started\_at\_ms;
* \[ ] duration\_ms;
* \[ ] status;
* \[ ] labels;
* \[ ] error\_type;
* \[ ] redacted;
* \[ ] live\_trading\_enabled=false.

Acceptatiecriteria:

* \[ ] Profiling core werkt zonder extra dependency.
* \[ ] Context manager meet duration.
* \[ ] Exceptions worden veilig geregistreerd.
* \[ ] Output is JSON-serializable.
* \[ ] Output is secret-free.

\---

## 5\. Fase 2 - Local Performance Store

Nieuwe module:

```text
src/binance\_spot\_bot/performance\_store.py
```

Storage:

```text
data/performance/
  runs/
  summaries/
  budgets/
  regressions/
  reports/
  manifests/
```

Core functies:

* \[ ] save profile run;
* \[ ] load profile run;
* \[ ] latest profile run;
* \[ ] list runs by category;
* \[ ] write summary;
* \[ ] write manifest;
* \[ ] verify manifest;
* \[ ] compact old profiling data;
* \[ ] export performance history.

Acceptatiecriteria:

* \[ ] Store is local-only.
* \[ ] Store has manifest/hash.
* \[ ] Store is append-only by default.
* \[ ] No secrets in store.
* \[ ] Tests use temp dirs.

\---

## 6\. Fase 3 - Runtime Step Profiler

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_profiler.py
```

Te meten runtime-stappen:

* \[ ] `BotRuntime.start`;
* \[ ] `BotRuntime.stop`;
* \[ ] `BotRuntime.step`;
* \[ ] `data\_source.next\_event`;
* \[ ] `data\_source.snapshot`;
* \[ ] data quality check;
* \[ ] feature row build;
* \[ ] model signal;
* \[ ] risk decision;
* \[ ] paper execution;
* \[ ] paper fill application;
* \[ ] order event recording;
* \[ ] session snapshot recording;
* \[ ] equity calculation;
* \[ ] demo pilot maintenance;
* \[ ] session report export;
* \[ ] `snapshot()` payload build.

Output:

* \[ ] runtime span tree;
* \[ ] per-step duration;
* \[ ] p50/p95/max duration;
* \[ ] slowest steps;
* \[ ] symbols/interval labels;
* \[ ] mode/source labels;
* \[ ] no-live proof.

Acceptatiecriteria:

* \[ ] Runtime profiling can be enabled/disabled.
* \[ ] Disabled profiler has near-zero behavior impact.
* \[ ] Profiling does not change runtime decisions.
* \[ ] Slow runtime steps are reported.
* \[ ] Tests use fake runtime/data source.

\---

## 7\. Fase 4 - CLI Command Profiler

Nieuwe module:

```text
src/binance\_spot\_bot/cli\_profiler.py
```

Te meten:

* \[ ] command name;
* \[ ] args category;
* \[ ] duration;
* \[ ] exit status;
* \[ ] stdout/stderr tail size;
* \[ ] artifact count produced;
* \[ ] report paths;
* \[ ] memory snapshot if available;
* \[ ] timeout;
* \[ ] safety env.

Integratie:

* \[ ] check-all commands;
* \[ ] check-all-v2 commands;
* \[ ] diagnostics;
* \[ ] support-bundle;
* \[ ] support-bundle-verify;
* \[ ] operator-quality-gate;
* \[ ] local-ops-snapshot;
* \[ ] dashboard-smoke;
* \[ ] dashboard-browser-smoke;
* \[ ] roadmap/release/knowledge/test commands.

Acceptatiecriteria:

* \[ ] CLI profiler wraps commands without altering output semantics.
* \[ ] Captures duration and status.
* \[ ] Redacts command args/output where needed.
* \[ ] Never stores secrets.
* \[ ] Tests use fake command runner.

\---

## 8\. Fase 5 - Dashboard Render Profiler

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_profiler.py
```

Te meten:

* \[ ] dashboard boot/import time;
* \[ ] page registry validation time;
* \[ ] tab render time;
* \[ ] panel render time;
* \[ ] chart creation time;
* \[ ] chart render wrapper time;
* \[ ] table render time;
* \[ ] debug expander payload size;
* \[ ] session state size estimate;
* \[ ] multi-symbol fragment render time;
* \[ ] dashboard evidence export time.

Specifieke checks:

* \[ ] panels boven duration budget;
* \[ ] chart payload te groot;
* \[ ] te veel rows in table;
* \[ ] duplicated expensive computations;
* \[ ] repeated file reads during render;
* \[ ] no stable chart key risk;
* \[ ] optional-heavy import warning.

Acceptatiecriteria:

* \[ ] Dashboard profiler is opt-in.
* \[ ] Dashboard still works without profiler.
* \[ ] Dashboard charts get stable profiling labels.
* \[ ] Slow panels are reported.
* \[ ] Browser smoke can run with profiler on.

\---

## 9\. Fase 6 - Memory \& Resource Snapshot

Nieuwe module:

```text
src/binance\_spot\_bot/resource\_monitor.py
```

Zonder verplichte externe dependency:

* \[ ] Python process memory best-effort via stdlib/platform.
* \[ ] `tracemalloc` optional snapshot.
* \[ ] object allocation top stats optional.
* \[ ] file count touched by run.
* \[ ] artifact bytes written.
* \[ ] data dir size estimate.
* \[ ] open file handles best-effort.
* \[ ] CPU time best-effort.

Metrics:

* \[ ] rss\_mb if available;
* \[ ] peak\_traced\_mb if tracemalloc enabled;
* \[ ] artifact\_bytes\_written;
* \[ ] files\_written;
* \[ ] files\_read estimate;
* \[ ] run\_duration\_ms;
* \[ ] data\_dir\_growth\_bytes.

Acceptatiecriteria:

* \[ ] Works on Windows.
* \[ ] Works without psutil.
* \[ ] Tracemalloc can be disabled.
* \[ ] No secrets in memory reports.
* \[ ] Tests use best-effort assertions.

\---

## 10\. Fase 7 - File I/O \& Artifact Performance Profiler

Nieuwe module:

```text
src/binance\_spot\_bot/io\_profiler.py
```

Te meten:

* \[ ] JSON read duration;
* \[ ] JSON write duration;
* \[ ] JSONL append duration;
* \[ ] CSV read/write duration;
* \[ ] report generation writes;
* \[ ] support bundle zip duration;
* \[ ] evidence manifest generation;
* \[ ] session store writes;
* \[ ] data cache reads/writes;
* \[ ] backup/release/roadmap artifact writes.

Bottleneck detectie:

* \[ ] many small writes;
* \[ ] repeated reads of same file;
* \[ ] large JSON payload;
* \[ ] slow manifest hash;
* \[ ] report index too large;
* \[ ] support bundle size spike;
* \[ ] session snapshot write frequency too high.

Acceptatiecriteria:

* \[ ] I/O profiler is opt-in.
* \[ ] I/O wrappers are safe.
* \[ ] No file content stored by default.
* \[ ] Only paths/size/duration/hashes stored.
* \[ ] Reports are secret-free.

\---

## 11\. Fase 8 - Data/Cache Performance Analysis

Nieuwe module:

```text
src/binance\_spot\_bot/data\_performance.py
```

Te analyseren:

* \[ ] DataStore reads/writes;
* \[ ] public candle cache reads/writes;
* \[ ] feature row build duration;
* \[ ] indicator calculations;
* \[ ] backtest dataset reads;
* \[ ] evaluation report generation;
* \[ ] metrics warehouse reads/writes;
* \[ ] knowledge graph build time;
* \[ ] roadmap index build time;
* \[ ] backup/restore inventory time.

Output:

* \[ ] slow data source operations;
* \[ ] cache hit/miss estimate if available;
* \[ ] expensive feature windows;
* \[ ] large artifact warnings;
* \[ ] recommended cache/indexing actions.

Acceptatiecriteria:

* \[ ] Data performance report works offline.
* \[ ] Missing artifacts produce warnings, not crash.
* \[ ] No external data needed.
* \[ ] Output is dashboard-ready.
* \[ ] No secrets.

\---

## 12\. Fase 9 - Performance Budget Configuration

Nieuwe config:

```text
config/performance-budgets.json
```

Budget categories:

* \[ ] runtime step max duration;
* \[ ] runtime full session max duration;
* \[ ] dashboard import max duration;
* \[ ] dashboard panel max duration;
* \[ ] chart creation max duration;
* \[ ] CLI command max duration;
* \[ ] check-all max duration;
* \[ ] check-all-v2 profile duration;
* \[ ] support bundle max duration;
* \[ ] evidence manifest max duration;
* \[ ] backup inventory max duration;
* \[ ] memory peak budget;
* \[ ] data\_dir growth budget;
* \[ ] artifact size budget.

Default profiles:

* \[ ] local\_dev\_fast;
* \[ ] balanced\_default;
* \[ ] strict\_release;
* \[ ] dashboard\_heavy;
* \[ ] low\_resource\_machine.

Acceptatiecriteria:

* \[ ] Budget config validates.
* \[ ] Invalid budget falls back to strict safe default.
* \[ ] Budgets can be per domain.
* \[ ] Budget output is secret-free.
* \[ ] Tests cover invalid configs.

\---

## 13\. Fase 10 - Performance Budget Evaluator

Nieuwe module:

```text
src/binance\_spot\_bot/performance\_budget.py
```

Budget result:

* \[ ] budget\_id;
* \[ ] category;
* \[ ] measured\_value;
* \[ ] budget\_value;
* \[ ] status:

  * ok;
  * warn;
  * fail;
  * unknown.
* \[ ] severity;
* \[ ] reason;
* \[ ] suggested\_action;
* \[ ] evidence\_links.

Rules:

* \[ ] fail if critical command exceeds hard budget;
* \[ ] warn if dashboard panel exceeds soft budget;
* \[ ] fail if memory/report size grows too much;
* \[ ] warn if runtime p95 exceeds threshold;
* \[ ] fail release gate if strict\_release budget fails.

Acceptatiecriteria:

* \[ ] Budget evaluator compares run vs config.
* \[ ] Results are explainable.
* \[ ] Critical budget failures can block release/check gate.
* \[ ] Dashboard can show budget status.
* \[ ] Tests cover ok/warn/fail.

\---

## 14\. Fase 11 - Performance Regression Detector

Nieuwe module:

```text
src/binance\_spot\_bot/performance\_regression.py
```

Detectie:

* \[ ] current run vs previous run;
* \[ ] current run vs rolling average;
* \[ ] current run vs release baseline;
* \[ ] current run vs budget;
* \[ ] test command slowdown;
* \[ ] dashboard import slowdown;
* \[ ] runtime step slowdown;
* \[ ] support bundle slowdown;
* \[ ] artifact size increase;
* \[ ] memory increase.

Regression output:

* \[ ] regression\_id;
* \[ ] metric;
* \[ ] previous\_value;
* \[ ] current\_value;
* \[ ] delta\_abs;
* \[ ] delta\_pct;
* \[ ] severity;
* \[ ] likely\_cause;
* \[ ] recommended\_tests;
* \[ ] recommended\_refactor;
* \[ ] blockers.

Acceptatiecriteria:

* \[ ] Regression detection is deterministic.
* \[ ] Can run without previous history.
* \[ ] Supports baseline creation.
* \[ ] Reports are secret-free.
* \[ ] Tests use synthetic history.

\---

## 15\. Fase 12 - Performance Profiling CLI

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli perf-profile-runtime --steps 100 --mode demo
python -m binance\_spot\_bot.cli perf-profile-cli --command diagnostics
python -m binance\_spot\_bot.cli perf-profile-dashboard-import
python -m binance\_spot\_bot.cli perf-profile-dashboard-smoke
python -m binance\_spot\_bot.cli perf-profile-check-all
python -m binance\_spot\_bot.cli perf-budget-check --profile balanced\_default
python -m binance\_spot\_bot.cli perf-regression-check
python -m binance\_spot\_bot.cli perf-history --days 14
python -m binance\_spot\_bot.cli perf-report
python -m binance\_spot\_bot.cli perf-evidence-export --run-id latest
```

Acceptatiecriteria:

* \[ ] Commands werken offline waar mogelijk.
* \[ ] Commands gebruiken veilige env.
* \[ ] Commands ondersteunen JSON output.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account/order endpoints.
* \[ ] Reports zijn secret-free.

\---

## 16\. Fase 13 - Performance Dashboard Panel

Nieuwe dashboardsectie:

```text
Performance \& Resource Budgets
```

Panels:

* \[ ] latest profile summary;
* \[ ] runtime step timings;
* \[ ] dashboard panel timings;
* \[ ] CLI command timings;
* \[ ] check-all/check-all-v2 timings;
* \[ ] memory/resource snapshots;
* \[ ] file I/O hotspots;
* \[ ] data/cache bottlenecks;
* \[ ] budget status;
* \[ ] regression status;
* \[ ] slowest operations;
* \[ ] recommended optimizations;
* \[ ] evidence export;
* \[ ] no-live proof.

Actions:

* \[ ] run lightweight profile;
* \[ ] profile runtime demo steps;
* \[ ] profile dashboard import;
* \[ ] run budget check;
* \[ ] run regression check;
* \[ ] export performance report;
* \[ ] copy recommended profiling commands.

Safeguards:

* \[ ] `LOCAL PERFORMANCE PROFILING ONLY` badge.
* \[ ] No live controls.
* \[ ] Profiling commands visible before running.
* \[ ] Raw JSON only in debug expanders.
* \[ ] Stable widget keys.
* \[ ] Browser smoke covers panel.

Acceptatiecriteria:

* \[ ] Dashboard shows runtime and CLI timings.
* \[ ] Dashboard shows budget pass/fail.
* \[ ] Dashboard shows regression warnings.
* \[ ] Dashboard does not run live actions.
* \[ ] Browser smoke passes.

\---

## 17\. Fase 14 - Check-All V2 \& Test Selection Integration

Uitbreiding op Roadmap 092:

* \[ ] check-all-v2 records command durations.
* \[ ] test runtime history receives profiler data.
* \[ ] selected profile has estimated vs actual duration.
* \[ ] slow selected commands get warnings.
* \[ ] fast profile gets runtime budget.
* \[ ] deep profile gets stricter performance summary.
* \[ ] flaky test tracker receives duration spikes.

Acceptatiecriteria:

* \[ ] check-selected writes performance data.
* \[ ] test-evidence bundle includes performance summary.
* \[ ] slow command warning appears in regression risk report.
* \[ ] no-live env remains forced.
* \[ ] Tests use fake runner.

\---

## 18\. Fase 15 - Repository Knowledge Integration

Uitbreiding op Roadmap 091:

* \[ ] knowledge graph stores performance hot modules.
* \[ ] ownership map includes performance risk.
* \[ ] impact analysis includes performance-sensitive modules.
* \[ ] refactor candidate detector uses profiler data.
* \[ ] artifact flow graph includes slow artifacts.
* \[ ] Codex task pack gets performance budget checks.

Acceptatiecriteria:

* \[ ] Impact analysis can say “this change touches slow module”.
* \[ ] Refactor candidate report includes measured slow paths.
* \[ ] Task packs can require perf-budget-check.
* \[ ] Reports are secret-free.
* \[ ] No live trading.

\---

## 19\. Fase 16 - Release \& Roadmap Integration

Uitbreiding op Roadmap 089/090:

* \[ ] release quality gate reads performance budget result.
* \[ ] release evidence bundle includes performance report.
* \[ ] roadmap completion gate can require performance budget pass.
* \[ ] roadmap evidence bundle includes profiler output if performance-sensitive.
* \[ ] release notes mention performance improvements/regressions.
* \[ ] upgrade/migration roadmaps require performance sanity check.

Acceptatiecriteria:

* \[ ] Release gate blocks strict performance budget failure.
* \[ ] Roadmap completion can include perf evidence.
* \[ ] Release notes input includes perf summary.
* \[ ] No-live proof preserved.
* \[ ] Reports are secret-free.

\---

## 20\. Fase 17 - Performance Optimization Recommendation Engine

Nieuwe module:

```text
src/binance\_spot\_bot/performance\_recommendations.py
```

Recommendation types:

* \[ ] cache repeated file read;
* \[ ] reduce dashboard table rows;
* \[ ] move heavy import behind optional lazy import;
* \[ ] split large dashboard panel;
* \[ ] avoid repeated snapshot building;
* \[ ] batch JSONL writes;
* \[ ] compact old metrics/reports;
* \[ ] lower default visible candles;
* \[ ] add manifest/index cache;
* \[ ] run deep profile before release.

Per recommendation:

* \[ ] recommendation\_id;
* \[ ] target module/function/panel;
* \[ ] evidence;
* \[ ] expected impact;
* \[ ] risk level;
* \[ ] suggested tests;
* \[ ] suggested Codex task;
* \[ ] no-live constraints.

Acceptatiecriteria:

* \[ ] Recommendations are evidence-based.
* \[ ] Recommendations do not auto-edit code.
* \[ ] Recommendations include tests.
* \[ ] High-risk optimizations require review.
* \[ ] Output is dashboard-ready.

\---

## 21\. Fase 18 - Performance Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/performance\_evidence\_bundle.py
```

Bundle bevat:

* \[ ] profile run;
* \[ ] runtime step summary;
* \[ ] CLI timing summary;
* \[ ] dashboard timing summary;
* \[ ] resource snapshot;
* \[ ] I/O hotspot report;
* \[ ] budget check;
* \[ ] regression check;
* \[ ] recommendations;
* \[ ] no-live proof;
* \[ ] redaction proof;
* \[ ] hashes.

Output:

```text
data/performance/evidence/<run\_id>/
  performance\_evidence\_manifest.json
  performance\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Dashboard/CLI export works.
* \[ ] Bundle links to release/roadmap/test evidence where relevant.

\---

## 22\. Fase 19 - Scheduled Performance Monitoring

Uitbreiding op Roadmap 083/084:

Scheduled jobs:

* \[ ] daily lightweight performance profile;
* \[ ] daily check-all-v2 duration summary;
* \[ ] weekly dashboard import/profile;
* \[ ] weekly runtime demo profile;
* \[ ] weekly performance budget check;
* \[ ] weekly regression report;
* \[ ] post-roadmap performance check;
* \[ ] pre-release strict performance check.

Metrics naar Roadmap 084:

* \[ ] runtime step p95;
* \[ ] dashboard import duration;
* \[ ] CLI command duration;
* \[ ] check-all duration;
* \[ ] support bundle duration;
* \[ ] artifact size trend;
* \[ ] memory peak trend;
* \[ ] budget failures;
* \[ ] regression count.

Acceptatiecriteria:

* \[ ] Scheduled jobs are allowlisted.
* \[ ] Jobs are local-only.
* \[ ] Failed perf job can create support bundle.
* \[ ] Metrics are secret-free.
* \[ ] No live trading.

\---

## 23\. Fase 20 - Tests

### Unit tests

* \[ ] `tests/test\_profiling\_core.py`
* \[ ] `tests/test\_performance\_store.py`
* \[ ] `tests/test\_runtime\_profiler.py`
* \[ ] `tests/test\_cli\_profiler.py`
* \[ ] `tests/test\_dashboard\_profiler.py`
* \[ ] `tests/test\_resource\_monitor.py`
* \[ ] `tests/test\_io\_profiler.py`
* \[ ] `tests/test\_data\_performance.py`
* \[ ] `tests/test\_performance\_budget.py`
* \[ ] `tests/test\_performance\_regression.py`
* \[ ] `tests/test\_performance\_recommendations.py`
* \[ ] `tests/test\_performance\_evidence\_bundle.py`

### Integration tests

* \[ ] Profile fake runtime step.
* \[ ] Profile fake CLI command.
* \[ ] Profile dashboard import stub.
* \[ ] Store profile run and verify manifest.
* \[ ] Evaluate budget ok/warn/fail.
* \[ ] Detect regression from synthetic history.
* \[ ] Generate performance report.
* \[ ] Export performance evidence bundle.
* \[ ] Feed performance summary into fake release gate.
* \[ ] Feed performance summary into fake roadmap evidence.

### Safety tests

* \[ ] Profiler does not execute arbitrary code.
* \[ ] Profiler uses safe env for commands.
* \[ ] Profiler never enables live.
* \[ ] Profiler never calls signed/order/account endpoints.
* \[ ] Profiler redacts command args/output.
* \[ ] Reports contain no secrets.
* \[ ] Performance budget failure does not trigger trading.
* \[ ] No-live proof remains true.

\---

## 24\. Docs

Nieuwe docs:

* \[ ] `docs/performance-profiling-safety-contract.md`
* \[ ] `docs/profiling-core.md`
* \[ ] `docs/runtime-step-profiler.md`
* \[ ] `docs/cli-command-profiler.md`
* \[ ] `docs/dashboard-render-profiler.md`
* \[ ] `docs/resource-monitor.md`
* \[ ] `docs/io-profiler.md`
* \[ ] `docs/data-cache-performance.md`
* \[ ] `docs/performance-budgets.md`
* \[ ] `docs/performance-regression-detection.md`
* \[ ] `docs/performance-dashboard.md`
* \[ ] `docs/performance-evidence-bundle.md`
* \[ ] `docs/performance-optimization-recommendations.md`
* \[ ] `docs/scheduled-performance-monitoring.md`

README updates:

* \[ ] performance profiling workflow;
* \[ ] runtime profiling command;
* \[ ] dashboard profiling command;
* \[ ] CLI profiling command;
* \[ ] performance budgets;
* \[ ] regression checks;
* \[ ] no-live statement.

\---

## 25\. CLI command examples

### Runtime profile

```powershell
python -m binance\_spot\_bot.cli perf-profile-runtime --steps 100 --mode demo --json
```

### Dashboard import profile

```powershell
python -m binance\_spot\_bot.cli perf-profile-dashboard-import --json
```

### CLI command profile

```powershell
python -m binance\_spot\_bot.cli perf-profile-cli --command diagnostics --json
```

### Budget check

```powershell
python -m binance\_spot\_bot.cli perf-budget-check --profile balanced\_default --json
```

### Regression check

```powershell
python -m binance\_spot\_bot.cli perf-regression-check --json
```

### Evidence export

```powershell
python -m binance\_spot\_bot.cli perf-evidence-export --run-id latest
```

\---

## 26\. Codex bouwvolgorde

### PR 1 - Profiling Core + Safety Contract

* \[ ] `profiling\_core.py`
* \[ ] safety contract doc
* \[ ] basic span/timing tests
* \[ ] redaction/no-live tests.

### PR 2 - Performance Store

* \[ ] `performance\_store.py`
* \[ ] save/load profile runs
* \[ ] manifest verify
* \[ ] tests.

### PR 3 - Runtime Profiler

* \[ ] `runtime\_profiler.py`
* \[ ] runtime step span wrappers
* \[ ] fake runtime tests.

### PR 4 - CLI Profiler

* \[ ] `cli\_profiler.py`
* \[ ] safe command profiling
* \[ ] fake runner tests.

### PR 5 - Dashboard Profiler

* \[ ] `dashboard\_profiler.py`
* \[ ] render/panel/chart timings
* \[ ] browser smoke compatibility.

### PR 6 - Resource + I/O Profilers

* \[ ] `resource\_monitor.py`
* \[ ] `io\_profiler.py`
* \[ ] tests.

### PR 7 - Performance Budgets

* \[ ] `performance\_budget.py`
* \[ ] config validation
* \[ ] ok/warn/fail tests.

### PR 8 - Regression + Recommendations

* \[ ] `performance\_regression.py`
* \[ ] `performance\_recommendations.py`
* \[ ] synthetic history tests.

### PR 9 - CLI + Reports + Evidence

* \[ ] CLI commands
* \[ ] performance reports
* \[ ] evidence bundle
* \[ ] tests.

### PR 10 - Dashboard + Integrations + Docs

* \[ ] Performance dashboard panel
* \[ ] check-all-v2/test selection integration
* \[ ] release/roadmap/metrics integration
* \[ ] docs
* \[ ] browser smoke.

\---

## 27\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 093 PR 1: Profiling Core + Performance Profiling Safety Contract.

Maak docs/performance-profiling-safety-contract.md.

Maak src/binance\_spot\_bot/profiling\_core.py met:
- ProfileSpan
- ProfileMetric
- ProfileRun
- ProfileSummary
- ProfileBudget
- ProfileBudgetResult
- now\_monotonic\_ms()
- profile\_block(...)
- summarize\_profile\_run(...)
- redact\_profile\_payload(...)
- write\_profile\_run(...)

Gebruik alleen stdlib.
Maak profile\_block als context manager.
Zorg dat exceptions in spans worden geregistreerd zonder business logic te veranderen.
Zorg dat alle outputs:
- JSON serializable zijn
- secret-free zijn
- live\_trading\_enabled=False bevatten
- no\_live\_statement bevatten waar relevant

Voeg tests toe voor:
- basic duration measurement
- nested spans
- exception span status
- JSON serialization
- secret redaction
- live\_trading\_enabled=False
- no network/API/order/account usage

Geen runtime integratie in deze PR.
Geen dashboard integratie in deze PR.
Geen command runner.
Geen API calls.
Geen signed endpoints.
Geen orders.
Geen live trading.
```

Waarom eerst:

* Alle performance-roadmapdelen hebben een veilige basisprofiler nodig.
* Dit raakt geen trading runtime en verandert geen beslislogica.
* Het is klein genoeg voor Codex.
* Safety/no-live/redaction kan direct getest worden.
* Daarna kunnen runtime, CLI, dashboard en check-all veilig geïnstrumenteerd worden.

\---

## 28\. Definition of Done

Roadmap 093 is klaar als:

* \[ ] Performance Profiling Safety Contract bestaat.
* \[ ] Profiling Core Utilities werken.
* \[ ] Local Performance Store werkt.
* \[ ] Runtime Step Profiler werkt.
* \[ ] CLI Command Profiler werkt.
* \[ ] Dashboard Render Profiler werkt.
* \[ ] Memory \& Resource Snapshot werkt.
* \[ ] File I/O \& Artifact Performance Profiler werkt.
* \[ ] Data/Cache Performance Analysis werkt.
* \[ ] Performance Budget Configuration werkt.
* \[ ] Performance Budget Evaluator werkt.
* \[ ] Performance Regression Detector werkt.
* \[ ] Performance Profiling CLI werkt.
* \[ ] Performance Dashboard Panel werkt.
* \[ ] Check-All V2 \& Test Selection Integration werkt.
* \[ ] Repository Knowledge Integration werkt.
* \[ ] Release \& Roadmap Integration werkt.
* \[ ] Performance Optimization Recommendation Engine werkt.
* \[ ] Performance Evidence Bundle werkt.
* \[ ] Scheduled Performance Monitoring werkt.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen profiler geen business logic verandert.
* \[ ] Reports/evidence zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 093 kan na uitvoering naar `Voltooid docs`.

\---

## 29\. Verwachte Roadmap 094 daarna

Na Roadmap 093 zou Roadmap 094 logisch focussen op:

```text
Roadmap 094 - Dashboard Component Refactor, Lazy Loading \& UX Performance Hardening
```

Mogelijke inhoud:

* \[ ] dashboard panels opsplitsen;
* \[ ] lazy imports;
* \[ ] fragment-level caching;
* \[ ] chart payload limits;
* \[ ] stable widget keys enforcement;
* \[ ] dashboard performance budgets toepassen;
* \[ ] browser smoke voor zware panels;
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

Gebouwd: profiling, resource budget, regression, evidence. Dashboard surface en docs toegevoegd waar van toepassing.

Validatie: tests/test_roadmaps_089_096_full_surface.py, compileall, dashboard-smoke.

Safety: lokaal/paper-only, geen live trading enablement.


---

## Definitieve afwerking 2026-05-15

Status: Voltooid na volledige hercontrole.

Gebouwd:
- runtime, CLI, dashboard, resource, I/O en data/cache profiling;
- performance budget evaluator, regression detector, recommendations en evidence bundle;
- dashboard performance panel met lokale safety caption en resource budget status;
- repo-lokale test-temp harness voor Windows 11 permissieproblemen;
- browser-smoke HTTP-fallback wanneer Playwright door Windows pipe-permissies wordt geblokkeerd;
- security-scan negeert alleen repo-interne pytest-temp artefacten, niet echte projectbestanden.

Validatie:
- `python -m pytest -q` -> 346 passed, 1 warning;
- `python -m binance_spot_bot.cli check-all --skip-tests --json` -> ok;
- `python -m binance_spot_bot.cli dashboard-smoke --seconds 1` -> ok;
- `python -m binance_spot_bot.cli dashboard-browser-smoke --url http://127.0.0.1:8506/ --seconds 10` -> ok via http-fallback;
- 093 performance CLI flow volledig groen.

Safety:
- live trading blijft disabled;
- geen signed/order/account/live endpoints toegevoegd;
- generated pytest-temp secret fixtures worden niet als repo-secret beschouwd.
