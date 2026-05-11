# Roadmap 095 - Runtime Core Decomposition, Event Bus \& Snapshot Optimization

Status: Niet volledig voltooid / opnieuw gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/095-roadmap-runtime-core-decomposition-event-bus-snapshot-optimization.md
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
* `Roadmap docs/093-roadmap-performance-profiling-runtime-bottleneck-analysis-resource-budgeting.md`
* `Roadmap docs/094-roadmap-dashboard-component-refactor-lazy-loading-ux-performance-hardening.md`

Doel: Roadmap 094 maakt het dashboard modulair, sneller en beter testbaar. Roadmap 095 pakt daarna de kern aan waar dashboard, demo trading, paper sessions, profiling, evidence en testselectie allemaal op steunen: `BotRuntime`. De runtime wordt opgesplitst in kleine services, krijgt een typed runtime event bus, een duidelijke step pipeline, snapshot builders met payload limits, session/event batching, demo-pilot isolatie, en integratie met performance budgets, knowledge graph, testselectie en release evidence.

Live trading blijft volledig buiten scope. Deze roadmap mag geen live mode toevoegen, geen signed real-order endpoints activeren en geen echte account/order acties buiten bestaande demo/testnet-readiness guardrails uitvoeren.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 095`, `095-roadmap`, `Runtime Core Decomposition`, `Event Bus`, `Snapshot Optimization` en `runtime core`.
* \[x] Geen bestaande Roadmap 095 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 094 is lokaal aangemaakt als Dashboard Component Refactor, Lazy Loading \& UX Performance Hardening.

### Codebasecontrole

Breed bekeken met runtime-focus:

* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/session\_store.py`
* \[x] `src/binance\_spot\_bot/execution.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] eerdere brede analyse van dashboard, CLI, operator/evidence, evaluation, performance en testselectie roadmaps.

### Belangrijke bestaande basis

De codebase heeft nu:

* \[x] Een centrale `BotRuntime` die veel verantwoordelijkheden combineert:

  * settings/options;
  * datastore;
  * audit;
  * runtime metrics;
  * session store;
  * model registry;
  * paper account;
  * signal/risk/execution;
  * data source;
  * user data stream;
  * order lifecycle;
  * alerts;
  * demo adapter/reconciler/account sync;
  * demo pilot orchestration;
  * session finish/report paths;
  * snapshot payload.
* \[x] `RuntimeSnapshot` is breed en bevat veel UI-, runtime-, market-, demo-, reconciliation-, account-, alert-, session- en reportdata.
* \[x] `BotRuntime.step()` is een centrale pipeline die market data, data quality, feature building, model/risk, execution, paper accounting, order events, demo pilot maintenance, session snapshots, alerts en final snapshot combineert.
* \[x] `SessionStore` schrijft snapshots, fills, alerts, orders en heartbeats als JSONL en bewaart summary JSON.
* \[x] `ExecutionEngine` bevat al harde gates voor DISABLED/PAPER/TESTNET/LIVE en blokkeert live order placement met aparte manual implementation requirement.
* \[x] `check\_all.py` draait checks met `LIVE\_TRADING\_ENABLED=false` en `KILL\_SWITCH=true`.

### Belangrijkste gat na Roadmap 094

Na Dashboard Refactor blijft de runtime zelf nog te veel een centrale monoliet:

* \[ ] `BotRuntime` heeft te veel verantwoordelijkheden.
* \[ ] Runtime-events zijn impliciet verspreid over audit/session/logica.
* \[ ] Er is geen typed runtime event bus.
* \[ ] Session writes gebeuren per event/snapshot en zijn niet gebatcht.
* \[ ] Snapshot bouwt volledige lijsten zonder expliciete payload limits.
* \[ ] Dashboard krijgt mogelijk zwaardere snapshotdata dan nodig.
* \[ ] Demo pilot logic zit door runtime lifecycle heen verweven.
* \[ ] Runtime step pipeline is moeilijk afzonderlijk te testen.
* \[ ] Runtime performance budgets uit Roadmap 093 worden nog niet per stage afgedwongen.
* \[ ] Impact/testselectie uit Roadmap 091/092 kan runtime stages nog niet precies herkennen.
* \[ ] Release/migration evidence kan runtime schema changes nog niet goed tracken.

Roadmap 095 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 095

Maak de runtime modulair, event-driven en snapshot-efficiënt:

```text
BotRuntime monolith
→ RuntimeState
→ RuntimeEventBus
→ RuntimeStepPipeline
→ small runtime services
→ SnapshotBuilder
→ Snapshot limits/profiles
→ batched session/event writes
→ performance/test/evidence integration
```

Na Roadmap 095 moet de bot kunnen:

* \[ ] runtime services los testen;
* \[ ] runtime events typed publiceren;
* \[ ] audit/session/evidence vanuit events voeden;
* \[ ] snapshots bouwen met profiles:

  * compact;
  * dashboard;
  * full;
  * evidence.
* \[ ] snapshot payloads begrenzen;
* \[ ] runtime step stages meten;
* \[ ] session/event writes batchen;
* \[ ] demo-pilot lifecycle isoleren;
* \[ ] runtime schema/evidence manifesteren;
* \[ ] dashboard sneller voeden;
* \[ ] no-live veiligheid behouden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe tradingstrategie.
* \[ ] Geen nieuwe model inference engine.
* \[ ] Geen nieuwe execution engine vanaf nul.
* \[ ] Geen nieuwe dashboard-app.
* \[ ] Geen nieuwe performance profiler; Roadmap 093 doet dat.
* \[ ] Geen nieuwe dashboard refactor; Roadmap 094 doet dat.
* \[ ] Geen live trading.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen Binance account endpoints buiten bestaande demo/testnet-readiness guardrails.
* \[ ] Geen order placement buiten bestaande demo/testnet sandbox gates.
* \[ ] Geen event bus die automatisch trading actions uitvoert.
* \[ ] Geen async/concurrency rewrite in deze roadmap.
* \[ ] Geen breaking snapshot schema zonder migration/release evidence.

Wel doen:

* \[ ] `BotRuntime` intern opsplitsen;
* \[ ] typed event bus toevoegen;
* \[ ] snapshot builder toevoegen;
* \[ ] snapshot limits/profiles toevoegen;
* \[ ] services één voor één uit runtime halen;
* \[ ] backward-compatible public API houden;
* \[ ] tests en evidence versterken;
* \[ ] dashboard en performance integreren;
* \[ ] alles local-only, paper/demo/testnet-readiness en no-live houden.

\---

## 3\. Fase 0 - Runtime Refactor Safety Contract

Nieuwe doc:

```text
docs/runtime-refactor-safety-contract.md
```

Regels:

* \[ ] Runtime refactor mag geen live mode toevoegen.
* \[ ] `UI\_MODES` blijft zonder `live`.
* \[ ] `RuntimeOptions` blijft demo/paper/testnet-readiness gericht.
* \[ ] `ExecutionEngine` live branch blijft geblokkeerd.
* \[ ] Event bus mag geen order plaatsen.
* \[ ] Event handlers zijn read-only of local artifact writers.
* \[ ] Snapshot builder mag geen secrets lekken.
* \[ ] Credential status blijft alleen fingerprint/status, geen raw keys.
* \[ ] Demo trading blijft gated door demo profile, credentials, armed state, kill switch en max orders.
* \[ ] Runtime tests moeten no-live bewijzen.
* \[ ] Session/event writes moeten redacted zijn.
* \[ ] Runtime schema changes krijgen release/migration note.
* \[ ] Backward-compatible dashboard snapshot blijft bestaan tijdens migratie.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen `live` niet in `UI\_MODES` staat.
* \[ ] Tests bewijzen event bus geen execution side-effect heeft zonder service call.
* \[ ] Tests bewijzen snapshot geen raw API keys/secrets bevat.
* \[ ] Check-all blijft groen.

\---

## 4\. Fase 1 - Runtime State Model

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_state.py
```

Dataclasses:

* \[ ] `RuntimeState`
* \[ ] `RuntimeIdentity`
* \[ ] `RuntimeLifecycleState`
* \[ ] `RuntimeMarketState`
* \[ ] `RuntimePaperState`
* \[ ] `RuntimeModelState`
* \[ ] `RuntimeDemoState`
* \[ ] `RuntimeReportState`
* \[ ] `RuntimeSafetyState`

Doel: de mutable state van `BotRuntime` expliciet maken.

RuntimeState bevat:

* \[ ] mode;
* \[ ] symbol;
* \[ ] interval;
* \[ ] status;
* \[ ] message;
* \[ ] session\_id;
* \[ ] current candle;
* \[ ] latest signal;
* \[ ] latest risk decision;
* \[ ] latest execution result;
* \[ ] candles;
* \[ ] signal points;
* \[ ] fill points;
* \[ ] equity points;
* \[ ] paper balances;
* \[ ] top of book;
* \[ ] latest data quality;
* \[ ] alerts summary;
* \[ ] demo pilot counters;
* \[ ] reconciliation status;
* \[ ] report paths;
* \[ ] resume\_required;
* \[ ] live\_trading\_enabled=False.

Acceptatiecriteria:

* \[ ] RuntimeState is JSON/debug serializable zonder secrets.
* \[ ] BotRuntime kan intern RuntimeState opbouwen.
* \[ ] Bestaande snapshot output blijft gelijk.
* \[ ] Tests vergelijken oude snapshot fields met RuntimeState-derived snapshot.
* \[ ] Live disabled blijft expliciet.

\---

## 5\. Fase 2 - Runtime Event Schema

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_events.py
```

Dataclasses:

* \[ ] `RuntimeEvent`
* \[ ] `RuntimeEventType`
* \[ ] `RuntimeEventSeverity`
* \[ ] `RuntimeEventSource`
* \[ ] `RuntimeEventPayload`
* \[ ] `RuntimeEventBatch`

Event types:

* \[ ] runtime\_created;
* \[ ] runtime\_started;
* \[ ] runtime\_start\_blocked;
* \[ ] runtime\_stopped;
* \[ ] runtime\_completed;
* \[ ] candle\_received;
* \[ ] market\_snapshot\_received;
* \[ ] data\_quality\_updated;
* \[ ] feature\_built;
* \[ ] signal\_generated;
* \[ ] risk\_decision\_created;
* \[ ] execution\_result\_created;
* \[ ] paper\_fill\_applied;
* \[ ] equity\_recorded;
* \[ ] order\_event\_recorded;
* \[ ] session\_snapshot\_recorded;
* \[ ] alert\_emitted;
* \[ ] demo\_reconciliation\_completed;
* \[ ] demo\_account\_synced;
* \[ ] demo\_pilot\_paused;
* \[ ] session\_finished;
* \[ ] report\_exported;
* \[ ] snapshot\_built;
* \[ ] error\_captured.

Event velden:

* \[ ] event\_id;
* \[ ] timestamp\_ms;
* \[ ] session\_id;
* \[ ] runtime\_id;
* \[ ] type;
* \[ ] source;
* \[ ] severity;
* \[ ] payload;
* \[ ] redacted;
* \[ ] live\_trading\_enabled=false.

Acceptatiecriteria:

* \[ ] Events zijn JSON-serializable.
* \[ ] Events bevatten geen raw secrets.
* \[ ] Event types zijn stabiel en getest.
* \[ ] Event payloads zijn begrensd.
* \[ ] Tests dekken alle core event types.

\---

## 6\. Fase 3 - Runtime Event Bus

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_event\_bus.py
```

Doel: runtime events publiceren en handlers koppelen zonder runtime zelf steeds direct audit/session/evidence te laten schrijven.

Dataclasses:

* \[ ] `RuntimeEventBus`
* \[ ] `RuntimeEventHandler`
* \[ ] `RuntimeEventPublishResult`
* \[ ] `RuntimeEventSubscription`

Handlers:

* \[ ] audit handler;
* \[ ] session event handler;
* \[ ] metrics handler;
* \[ ] alert handler;
* \[ ] profiling handler;
* \[ ] evidence handler;
* \[ ] debug in-memory handler.

Regels:

* \[ ] Synchronous by default.
* \[ ] No automatic trading side effects.
* \[ ] Handler failures worden captured als warnings.
* \[ ] Critical handler failure kan runtime warning geven, niet live action.
* \[ ] Event bus kan disabled/null zijn voor tests.
* \[ ] Events worden redacted vóór persist.

Acceptatiecriteria:

* \[ ] Event bus publish werkt met meerdere handlers.
* \[ ] Handler failure crasht runtime niet tenzij configured strict.
* \[ ] No side effect handler can place orders.
* \[ ] Tests bewijzen event order.
* \[ ] Tests bewijzen no-live/no-secrets.

\---

## 7\. Fase 4 - Runtime Step Pipeline

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_pipeline.py
```

Dataclasses:

* \[ ] `RuntimeStepContext`
* \[ ] `RuntimeStepResult`
* \[ ] `RuntimePipelineStage`
* \[ ] `RuntimePipelineReport`

Stages:

* \[ ] ensure\_started;
* \[ ] handle\_stopped\_or\_readiness;
* \[ ] fetch\_market\_event;
* \[ ] update\_market\_snapshot;
* \[ ] update\_data\_quality;
* \[ ] handle\_waiting\_for\_data;
* \[ ] build\_feature;
* \[ ] build\_market\_account\_state;
* \[ ] run\_signal\_risk\_execution;
* \[ ] apply\_paper\_fill;
* \[ ] record\_order\_event;
* \[ ] update\_demo\_pilot\_after\_execution;
* \[ ] periodic\_demo\_maintenance;
* \[ ] record\_signal\_point;
* \[ ] record\_equity;
* \[ ] record\_session\_snapshot;
* \[ ] evaluate\_pause\_stop\_alerts;
* \[ ] build\_snapshot.

Acceptatiecriteria:

* \[ ] Pipeline stages zijn apart testbaar.
* \[ ] `BotRuntime.step()` gebruikt pipeline facade of staged helpers.
* \[ ] Stages publiceren RuntimeEvents.
* \[ ] Stage timings kunnen Roadmap 093 profiler gebruiken.
* \[ ] Bestaand runtime gedrag blijft backward-compatible.

\---

## 8\. Fase 5 - Market Data Runtime Service

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_market\_service.py
```

Taken:

* \[ ] data source create/resolve;
* \[ ] next candle fetch;
* \[ ] market snapshot update;
* \[ ] top of book update;
* \[ ] data source close;
* \[ ] connectivity degraded event;
* \[ ] source labels.

Input/output:

* \[ ] `MarketStepInput`
* \[ ] `MarketStepOutput`

Acceptatiecriteria:

* \[ ] Service werkt met StaticMarketDataSource.
* \[ ] Service werkt met DemoMarketReplaySource.
* \[ ] Service geeft degraded status als event.
* \[ ] BotRuntime gebruikt service zonder gedragbreuk.
* \[ ] Tests dekken candle none/completed/degraded.

\---

## 9\. Fase 6 - Feature/Signal Runtime Service

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_signal\_service.py
```

Taken:

* \[ ] feature rows bouwen;
* \[ ] feature warmup check;
* \[ ] market/account state bouwen;
* \[ ] model signal trigger;
* \[ ] active model payload helper;
* \[ ] model version helper.

Dataclasses:

* \[ ] `FeatureSignalInput`
* \[ ] `FeatureSignalOutput`

Acceptatiecriteria:

* \[ ] Warmup path blijft `waiting\_for\_data`.
* \[ ] Feature build is apart testbaar.
* \[ ] Model metadata blijft snapshot-compatible.
* \[ ] Events voor feature\_built/signal\_generated bestaan.
* \[ ] Tests dekken rule model en model alias fallback.

\---

## 10\. Fase 7 - Risk/Execution Runtime Service

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_execution\_service.py
```

Taken:

* \[ ] Risk decision uitvoeren via bestaande PaperTrader/RiskEngine/ExecutionEngine.
* \[ ] Latest signal/risk/execution result updaten.
* \[ ] Metrics blocks/signals updaten.
* \[ ] Paper fill request doorgeven aan paper accounting service.
* \[ ] Execution events publiceren.
* \[ ] Demo/testnet execution gates behouden.

Dataclasses:

* \[ ] `ExecutionStepInput`
* \[ ] `ExecutionStepOutput`

Acceptatiecriteria:

* \[ ] DISABLED/PAPER/TESTNET gedrag blijft gelijk.
* \[ ] Live branch blijft geblokkeerd.
* \[ ] Demo profile/armed gating blijft gelijk.
* \[ ] Tests dekken blocked/fill/rejected paths.
* \[ ] No-live tests verplicht.

\---

## 11\. Fase 8 - Paper Accounting Runtime Service

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_paper\_accounting.py
```

Taken:

* \[ ] `\_apply\_paper\_fill` verplaatsen;
* \[ ] `\_record\_equity` verplaatsen;
* \[ ] max drawdown helper;
* \[ ] fee/slippage/pnl aggregation;
* \[ ] paper account payload build;
* \[ ] fill events publiceren.

Acceptatiecriteria:

* \[ ] Paper fill output blijft backward-compatible.
* \[ ] Equity points blijven hetzelfde format.
* \[ ] Max drawdown blijft hetzelfde.
* \[ ] Tests dekken BUY/SELL/accounting block.
* \[ ] Event output is secret-free.

\---

## 12\. Fase 9 - Session Event Writer \& Batching

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_session\_writer.py
```

Doel: session writes betrouwbaarder en efficiënter maken.

Taken:

* \[ ] record snapshot event;
* \[ ] record fill event;
* \[ ] record alert event;
* \[ ] record order event;
* \[ ] record heartbeat event;
* \[ ] batch JSONL writes optioneel;
* \[ ] flush on stop/finish;
* \[ ] write queue size limit;
* \[ ] write failure event;
* \[ ] session summary update helper.

Dataclasses:

* \[ ] `SessionWriteRequest`
* \[ ] `SessionWriteBatch`
* \[ ] `SessionWriteResult`

Acceptatiecriteria:

* \[ ] Default gedrag blijft direct write of safe flush.
* \[ ] Batch mode kan aangezet worden.
* \[ ] Flush bij stop/completed.
* \[ ] Tests dekken write/flush/failure.
* \[ ] Geen data loss bij normale stop.

\---

## 13\. Fase 10 - Demo Pilot Runtime Service

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_demo\_pilot\_service.py
```

Taken:

* \[ ] demo adapter setup;
* \[ ] demo reconciler setup;
* \[ ] demo account sync setup;
* \[ ] clean start gate;
* \[ ] pilot mark running/stopping/completed;
* \[ ] update after execution;
* \[ ] periodic maintenance;
* \[ ] pause/stop decision;
* \[ ] cancel-on-stop status;
* \[ ] reconciliation payload;
* \[ ] demo account payload;
* \[ ] demo open orders payload.

Acceptatiecriteria:

* \[ ] Demo pilot behavior blijft backward-compatible.
* \[ ] Demo pilot service kan uitgeschakeld worden voor paper/demo replay.
* \[ ] Start gate is apart testbaar.
* \[ ] Pause rules zijn apart testbaar.
* \[ ] Demo pilot events zijn typed.

\---

## 14\. Fase 11 - Alert \& Watchdog Runtime Service

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_alert\_service.py
```

Taken:

* \[ ] `\_emit\_alert` centraliseren;
* \[ ] alert event publiceren;
* \[ ] alert session recording via event handler;
* \[ ] should stop runtime helper;
* \[ ] data quality issue → alert mapping;
* \[ ] risk block alert mapping;
* \[ ] max loss alert mapping.

Acceptatiecriteria:

* \[ ] Alert behavior blijft gelijk.
* \[ ] Alert events zijn typed.
* \[ ] Critical alert stops runtime zoals nu.
* \[ ] Tests dekken warning/error/critical.
* \[ ] Event payloads zijn redacted.

\---

## 15\. Fase 12 - Snapshot Builder V2

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_snapshot\_builder.py
```

Doel: snapshots losmaken van BotRuntime en payloads beheersen.

Dataclasses:

* \[ ] `SnapshotProfile`
* \[ ] `SnapshotBuildRequest`
* \[ ] `SnapshotBuildResult`
* \[ ] `SnapshotLimitConfig`
* \[ ] `SnapshotPayloadStats`

Profiles:

### `compact`

* \[ ] status/message;
* \[ ] current candle summary;
* \[ ] latest signal/risk/execution summary;
* \[ ] equity/position;
* \[ ] health/status;
* \[ ] no big lists.

### `dashboard`

* \[ ] compact + limited candles/signals/fills/equity points;
* \[ ] limited alerts;
* \[ ] limited recent sessions;
* \[ ] limited order lifecycle;
* \[ ] demo/pilot/reconciliation summaries.

### `full`

* \[ ] backward-compatible RuntimeSnapshot fields;
* \[ ] still applies safety limits where required.

### `evidence`

* \[ ] includes hashes/report paths/session IDs;
* \[ ] no secrets;
* \[ ] artifact/evidence friendly.

Acceptatiecriteria:

* \[ ] Bestaande `snapshot()` blijft default full/backward-compatible.
* \[ ] Dashboard kan `snapshot(profile="dashboard")` gebruiken na integratie.
* \[ ] Compact snapshot is kleiner.
* \[ ] Payload stats worden gerapporteerd.
* \[ ] Tests vergelijken expected field coverage.

\---

## 16\. Fase 13 - Snapshot Limits \& Payload Optimization

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_snapshot\_limits.py
```

Limits:

* \[ ] max candles;
* \[ ] max signal points;
* \[ ] max fill points;
* \[ ] max equity points;
* \[ ] max audit tail;
* \[ ] max recent sessions;
* \[ ] max order lifecycle;
* \[ ] max alerts;
* \[ ] max demo open orders;
* \[ ] max demo order errors;
* \[ ] max cancel-on-stop rows;
* \[ ] max JSON payload bytes estimate.

Helpers:

* \[ ] trim list tail;
* \[ ] estimate payload size;
* \[ ] redact snapshot payload;
* \[ ] snapshot warning metadata;
* \[ ] payload hash.

Acceptatiecriteria:

* \[ ] Snapshot lists are bounded for dashboard profile.
* \[ ] Full snapshot has configurable safe limits.
* \[ ] Payload stats include trimmed counts.
* \[ ] Secrets are redacted.
* \[ ] Tests cover large lists.

\---

## 17\. Fase 14 - Runtime Schema Versioning

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_schema.py
```

Doel: runtime options/events/snapshots versioned maken voor release/migration safety.

Schemas:

* \[ ] RuntimeOptions schema version;
* \[ ] RuntimeState schema version;
* \[ ] RuntimeEvent schema version;
* \[ ] RuntimeSnapshot schema version;
* \[ ] Session event schema version;
* \[ ] Demo pilot schema version.

Functionaliteit:

* \[ ] schema version constants;
* \[ ] schema manifest;
* \[ ] compatibility check;
* \[ ] snapshot schema report;
* \[ ] event schema report.

Acceptatiecriteria:

* \[ ] Schema manifest is JSON.
* \[ ] Release tooling kan runtime schema lezen.
* \[ ] Snapshot builder schrijft schema\_version.
* \[ ] Event bus schrijft schema\_version.
* \[ ] Tests dekken schema compatibility.

\---

## 18\. Fase 15 - Runtime Public API Compatibility Layer

Doel: bestaande callers niet breken.

Te behouden:

* \[ ] `BotRuntime(settings, options, candles=None)`
* \[ ] `start()`
* \[ ] `stop()`
* \[ ] `step()`
* \[ ] `run\_steps(count)`
* \[ ] `snapshot()`
* \[ ] `audit\_tail()`
* \[ ] `testnet\_prechecks()`
* \[ ] `cancel\_demo\_open\_orders()`
* \[ ] `reconcile\_demo\_orders()`

Nieuwe optionele API:

* \[ ] `snapshot(profile="full")`
* \[ ] `runtime\_events(limit=...)`
* \[ ] `flush\_events()`
* \[ ] `performance\_summary()`
* \[ ] `runtime\_state()`

Acceptatiecriteria:

* \[ ] Oude tests blijven groen.
* \[ ] Dashboard blijft werken tijdens migratie.
* \[ ] CLI blijft werken.
* \[ ] New API is optional.
* \[ ] Backward compatibility report bestaat.

\---

## 19\. Fase 16 - Runtime Performance Integration

Uitbreiding op Roadmap 093:

* \[ ] profile spans per pipeline stage;
* \[ ] runtime p50/p95 per stage;
* \[ ] snapshot build duration;
* \[ ] session write duration;
* \[ ] event bus publish duration;
* \[ ] demo pilot maintenance duration;
* \[ ] performance budget per stage.

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_performance.py
```

Acceptatiecriteria:

* \[ ] Runtime profile command kan stage timings tonen.
* \[ ] Slow stage wordt gerapporteerd.
* \[ ] Snapshot payload size wordt gemeten.
* \[ ] Performance budget failures zijn warnings/fails volgens config.
* \[ ] No-live proof behouden.

\---

## 20\. Fase 17 - Dashboard Runtime Integration

Uitbreiding op Roadmap 094:

* \[ ] dashboard gebruikt dashboard snapshot profile;
* \[ ] simple demo gebruikt compact/dashboard data waar mogelijk;
* \[ ] heavy panels vragen full/evidence data pas lazy op;
* \[ ] status header gebruikt compact snapshot;
* \[ ] chart payloads krijgen trimmed runtime lists;
* \[ ] snapshot payload stats zichtbaar in performance/debug panel;
* \[ ] demo pilot panel gebruikt demo\_pilot-specific payload helper.

Acceptatiecriteria:

* \[ ] Dashboard render blijft functioneel.
* \[ ] Dashboard snapshot payload kleiner.
* \[ ] No-live status blijft zichtbaar.
* \[ ] Browser smoke blijft groen.
* \[ ] Dashboard profiling toont snapshot build time.

\---

## 21\. Fase 18 - Runtime Evidence \& Reports

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_evidence.py
```

Reports:

```text
data/runtime/
  events/
  snapshots/
  reports/
  evidence/
```

Report types:

* \[ ] runtime architecture report;
* \[ ] runtime event report;
* \[ ] runtime pipeline report;
* \[ ] snapshot payload report;
* \[ ] session writer report;
* \[ ] demo pilot lifecycle report;
* \[ ] runtime safety report;
* \[ ] backward compatibility report.

Evidence bundle bevat:

* \[ ] runtime schema manifest;
* \[ ] event schema manifest;
* \[ ] snapshot stats;
* \[ ] pipeline stage timings;
* \[ ] no-live proof;
* \[ ] execution live-block proof;
* \[ ] session write report;
* \[ ] tests summary;
* \[ ] hashes.

Acceptatiecriteria:

* \[ ] Evidence bundle is secret-free.
* \[ ] Evidence bundle has manifest/hash.
* \[ ] Bundle can be linked to roadmap/release/test evidence.
* \[ ] Reports are dashboard-downloadable.
* \[ ] No-live proof included.

\---

## 22\. Fase 19 - Runtime CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli runtime-schema
python -m binance\_spot\_bot.cli runtime-event-smoke
python -m binance\_spot\_bot.cli runtime-pipeline-smoke
python -m binance\_spot\_bot.cli runtime-snapshot --profile compact
python -m binance\_spot\_bot.cli runtime-snapshot --profile dashboard
python -m binance\_spot\_bot.cli runtime-snapshot --profile full
python -m binance\_spot\_bot.cli runtime-snapshot-report
python -m binance\_spot\_bot.cli runtime-performance-summary
python -m binance\_spot\_bot.cli runtime-evidence-export
```

Acceptatiecriteria:

* \[ ] Commands werken offline/demo.
* \[ ] Commands ondersteunen JSON output.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed real-order/account endpoints.
* \[ ] Reports zijn secret-free.

\---

## 23\. Fase 20 - Knowledge/Test/Release Integraties

### Roadmap 091 integratie

* \[ ] Knowledge graph herkent runtime services.
* \[ ] Impact analysis onderscheidt market/signal/execution/session/snapshot services.
* \[ ] Ownership map krijgt runtime service domeinen.
* \[ ] Safety surface map linkt event bus/execution/snapshot.

### Roadmap 092 integratie

* \[ ] Runtime service changes selecteren gerichte tests.
* \[ ] Execution/risk/session writer changes forceren deep profile.
* \[ ] Snapshot-only changes selecteren snapshot/dashboard tests.
* \[ ] Event bus changes selecteren event/evidence tests.

### Roadmap 093 integratie

* \[ ] Runtime stage profiler gebruikt pipeline stage names.
* \[ ] Snapshot payload budgets worden performance budgets.
* \[ ] Session batching performance wordt gemeten.

### Roadmap 094 integratie

* \[ ] Dashboard gebruikt compact/dashboard snapshot profile.
* \[ ] Dashboard pages krijgen minder payload.
* \[ ] Browser smoke verifieert snapshot profile no-live.

### Roadmap 089/090 integratie

* \[ ] Runtime schema changes voeren release/migration notes.
* \[ ] Roadmap completion gate vereist runtime evidence.
* \[ ] Release evidence bundle bevat runtime schema/safety report.

Acceptatiecriteria:

* \[ ] Runtime changes leiden tot juiste testselectie.
* \[ ] Runtime schema changes leiden tot release notes input.
* \[ ] Dashboard changes zien snapshot profile impact.
* \[ ] Performance report bevat runtime stages.
* \[ ] No-live proof preserved.

\---

## 24\. Fase 21 - Tests

### Unit tests

* \[ ] `tests/test\_runtime\_refactor\_safety\_contract.py`
* \[ ] `tests/test\_runtime\_state.py`
* \[ ] `tests/test\_runtime\_events.py`
* \[ ] `tests/test\_runtime\_event\_bus.py`
* \[ ] `tests/test\_runtime\_pipeline.py`
* \[ ] `tests/test\_runtime\_market\_service.py`
* \[ ] `tests/test\_runtime\_signal\_service.py`
* \[ ] `tests/test\_runtime\_execution\_service.py`
* \[ ] `tests/test\_runtime\_paper\_accounting.py`
* \[ ] `tests/test\_runtime\_session\_writer.py`
* \[ ] `tests/test\_runtime\_demo\_pilot\_service.py`
* \[ ] `tests/test\_runtime\_alert\_service.py`
* \[ ] `tests/test\_runtime\_snapshot\_builder.py`
* \[ ] `tests/test\_runtime\_snapshot\_limits.py`
* \[ ] `tests/test\_runtime\_schema.py`
* \[ ] `tests/test\_runtime\_performance.py`
* \[ ] `tests/test\_runtime\_evidence.py`

### Integration tests

* \[ ] BotRuntime start/step/stop unchanged behavior.
* \[ ] Runtime pipeline smoke with static candles.
* \[ ] Event bus captures events for one step.
* \[ ] Session writer records snapshots/fills/orders.
* \[ ] Snapshot compact/dashboard/full profiles.
* \[ ] Snapshot limits trim large lists.
* \[ ] Demo pilot start gate still blocks unsafe conditions.
* \[ ] Paper fill behavior unchanged.
* \[ ] Runtime evidence bundle export.
* \[ ] Dashboard import with new snapshot API.
* \[ ] CLI runtime-snapshot command.

### Safety tests

* \[ ] `live` not in `UI\_MODES`.
* \[ ] Runtime options reject unsupported live mode.
* \[ ] Execution live branch remains blocked.
* \[ ] Event bus cannot place orders.
* \[ ] Snapshot builder does not expose raw API key/secret.
* \[ ] Demo trading requires demo profile and armed state.
* \[ ] Session writer redacts event payloads.
* \[ ] Runtime evidence is secret-free.
* \[ ] Check-all safe env still forced.
* \[ ] No-live proof remains true.

\---

## 25\. Docs

Nieuwe docs:

* \[ ] `docs/runtime-refactor-safety-contract.md`
* \[ ] `docs/runtime-state-model.md`
* \[ ] `docs/runtime-event-schema.md`
* \[ ] `docs/runtime-event-bus.md`
* \[ ] `docs/runtime-step-pipeline.md`
* \[ ] `docs/runtime-market-service.md`
* \[ ] `docs/runtime-signal-service.md`
* \[ ] `docs/runtime-execution-service.md`
* \[ ] `docs/runtime-paper-accounting.md`
* \[ ] `docs/runtime-session-writer.md`
* \[ ] `docs/runtime-demo-pilot-service.md`
* \[ ] `docs/runtime-alert-service.md`
* \[ ] `docs/runtime-snapshot-builder.md`
* \[ ] `docs/runtime-snapshot-limits.md`
* \[ ] `docs/runtime-schema-versioning.md`
* \[ ] `docs/runtime-public-api-compatibility.md`
* \[ ] `docs/runtime-performance-integration.md`
* \[ ] `docs/runtime-evidence.md`

README updates:

* \[ ] Runtime architecture overview.
* \[ ] Snapshot profiles.
* \[ ] Runtime event bus.
* \[ ] Runtime service testing.
* \[ ] No-live runtime guarantees.

\---

## 26\. CLI command examples

### Runtime schema

```powershell
python -m binance\_spot\_bot.cli runtime-schema --json
```

### Runtime event smoke

```powershell
python -m binance\_spot\_bot.cli runtime-event-smoke --json
```

### Compact snapshot

```powershell
python -m binance\_spot\_bot.cli runtime-snapshot --profile compact --json
```

### Dashboard snapshot

```powershell
python -m binance\_spot\_bot.cli runtime-snapshot --profile dashboard --json
```

### Runtime pipeline smoke

```powershell
python -m binance\_spot\_bot.cli runtime-pipeline-smoke --steps 20 --json
```

### Runtime evidence

```powershell
python -m binance\_spot\_bot.cli runtime-evidence-export
```

\---

## 27\. Codex bouwvolgorde

### PR 1 - Runtime Safety Contract + Runtime Events

* \[ ] `docs/runtime-refactor-safety-contract.md`
* \[ ] `runtime\_events.py`
* \[ ] event schema tests.
* \[ ] no-live/no-secret tests.

### PR 2 - Runtime Event Bus

* \[ ] `runtime\_event\_bus.py`
* \[ ] handler interface.
* \[ ] publish/failure tests.

### PR 3 - Runtime State Model

* \[ ] `runtime\_state.py`
* \[ ] state conversion helpers.
* \[ ] compatibility tests.

### PR 4 - Snapshot Builder + Limits

* \[ ] `runtime\_snapshot\_builder.py`
* \[ ] `runtime\_snapshot\_limits.py`
* \[ ] compact/dashboard/full profiles.
* \[ ] snapshot tests.

### PR 5 - Runtime Pipeline Foundation

* \[ ] `runtime\_pipeline.py`
* \[ ] staged helpers.
* \[ ] pipeline smoke tests.

### PR 6 - Market + Signal Services

* \[ ] `runtime\_market\_service.py`
* \[ ] `runtime\_signal\_service.py`
* \[ ] tests.

### PR 7 - Execution + Paper Accounting Services

* \[ ] `runtime\_execution\_service.py`
* \[ ] `runtime\_paper\_accounting.py`
* \[ ] no-live/execution tests.

### PR 8 - Session Writer + Alert Service

* \[ ] `runtime\_session\_writer.py`
* \[ ] `runtime\_alert\_service.py`
* \[ ] batching/flush tests.

### PR 9 - Demo Pilot Service + Runtime Schema

* \[ ] `runtime\_demo\_pilot\_service.py`
* \[ ] `runtime\_schema.py`
* \[ ] demo pilot tests.

### PR 10 - Runtime Integration + CLI + Evidence + Docs

* \[ ] BotRuntime uses services gradually.
* \[ ] CLI commands.
* \[ ] runtime evidence.
* \[ ] performance/dashboard/test/release integration.
* \[ ] docs.

\---

## 28\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 095 PR 1: Runtime Refactor Safety Contract + Runtime Event Schema.

Maak docs/runtime-refactor-safety-contract.md.

Maak src/binance\_spot\_bot/runtime\_events.py met:
- RuntimeEventType
- RuntimeEventSeverity
- RuntimeEventSource
- RuntimeEventPayload
- RuntimeEvent
- RuntimeEventBatch
- create\_runtime\_event(...)
- redact\_runtime\_event(...)
- runtime\_event\_to\_dict(...)

Event fields:
- event\_id
- timestamp\_ms
- session\_id
- runtime\_id
- type
- source
- severity
- payload
- redacted
- live\_trading\_enabled=False
- schema\_version

Voeg event types toe voor minimaal:
- runtime\_created
- runtime\_started
- runtime\_stopped
- candle\_received
- data\_quality\_updated
- feature\_built
- signal\_generated
- risk\_decision\_created
- execution\_result\_created
- paper\_fill\_applied
- equity\_recorded
- order\_event\_recorded
- session\_snapshot\_recorded
- alert\_emitted
- demo\_reconciliation\_completed
- session\_finished
- snapshot\_built
- error\_captured

Gebruik bestaande redaction helpers waar mogelijk.
Voeg tests toe voor:
- event serialization
- event batch serialization
- schema\_version aanwezig
- live\_trading\_enabled=False
- secret-like payload redaction
- valid event type coverage
- no network/API/signed/order/account usage

Geen BotRuntime integratie in deze PR.
Geen event bus in deze PR.
Geen dashboard.
Geen live trading.
Geen signed endpoints.
Geen account/order endpoints.
```

Waarom eerst:

* Typed events zijn de basis voor event bus, session writer, performance profiling, evidence en snapshot reports.
* Het raakt de bestaande runtime nog niet direct.
* Het is klein genoeg voor Codex.
* Safety/no-live/redaction kan meteen hard getest worden.
* Daarna kan BotRuntime stap voor stap zonder big-bang refactor worden opgesplitst.

\---

## 29\. Definition of Done

Roadmap 095 is klaar als:

* \[ ] Runtime Refactor Safety Contract bestaat.
* \[ ] Runtime State Model werkt.
* \[ ] Runtime Event Schema werkt.
* \[ ] Runtime Event Bus werkt.
* \[ ] Runtime Step Pipeline werkt.
* \[ ] Market Data Runtime Service werkt.
* \[ ] Feature/Signal Runtime Service werkt.
* \[ ] Risk/Execution Runtime Service werkt.
* \[ ] Paper Accounting Runtime Service werkt.
* \[ ] Session Event Writer \& Batching werkt.
* \[ ] Demo Pilot Runtime Service werkt.
* \[ ] Alert \& Watchdog Runtime Service werkt.
* \[ ] Snapshot Builder V2 werkt.
* \[ ] Snapshot Limits \& Payload Optimization werkt.
* \[ ] Runtime Schema Versioning werkt.
* \[ ] Runtime Public API Compatibility Layer werkt.
* \[ ] Runtime Performance Integration werkt.
* \[ ] Dashboard Runtime Integration werkt.
* \[ ] Runtime Evidence \& Reports werken.
* \[ ] Runtime CLI commands werken.
* \[ ] Knowledge/Test/Release integraties werken.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen event bus geen trading side effects heeft.
* \[ ] Tests bewijzen snapshot geen secrets lekt.
* \[ ] Dashboard import smoke blijft groen.
* \[ ] Dashboard browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 095 kan na uitvoering naar `Voltooid docs`.

\---

## 30\. Verwachte Roadmap 096 daarna

Na Roadmap 095 zou Roadmap 096 logisch focussen op:

```text
Roadmap 096 - Data Pipeline Decomposition, Feature Store Contracts \& Indicator Compute Optimization
```

Mogelijke inhoud:

* \[ ] feature/indicator pipeline opsplitsen;
* \[ ] typed feature store contracts;
* \[ ] incremental indicator computation;
* \[ ] candle cache/index improvements;
* \[ ] backtest/evaluation data reuse;
* \[ ] feature drift and data-quality evidence;
* \[ ] performance budgets for feature computation;
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

Gebouwd: runtime events, event bus, services, snapshot builder/limits. Dashboard surface en docs toegevoegd waar van toepassing.

Validatie: tests/test_roadmaps_089_096_full_surface.py, compileall, dashboard-smoke.

Safety: lokaal/paper-only, geen live trading enablement.

