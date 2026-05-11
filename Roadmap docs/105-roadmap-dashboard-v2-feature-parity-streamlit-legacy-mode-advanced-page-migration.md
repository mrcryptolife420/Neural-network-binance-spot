# Roadmap 105 - Dashboard V2 Feature Parity, Streamlit Legacy Mode \& Advanced Page Migration

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/105-roadmap-dashboard-v2-feature-parity-streamlit-legacy-mode-advanced-page-migration.md
```

## Samenvatting

Roadmap 104 bouwt het fundament voor een nieuw lokaal realtime dashboard zonder Streamlit: FastAPI/Uvicorn backend, WebSocket events, React/Vite frontend, runtime bridge, action policy, lokale launcher en smoke tests. Roadmap 105 is de beste vervolgstap: **Dashboard V2 naar feature parity brengen met het bestaande Streamlit dashboard**, de Streamlit UI als legacy/fallback markeren, alle advanced pages gefaseerd migreren, realtime charts en frontend-state optimaliseren, en operator/UAT/browser-smoke evidence toevoegen.

Doel: van een Dashboard V2 skeleton/MVP naar een praktisch bruikbaar lokaal dashboard dat de belangrijkste workflows uit Streamlit vervangt zonder full-page refresh.

Live trading blijft volledig buiten scope. Dashboard V2 mag geen live mode, signed real-order endpoints of echte account/order workflows toevoegen.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 105`, `105-roadmap`, `Dashboard V2 Feature Parity`, `Streamlit Legacy`, `Advanced Page Migration` en `Realtime Chart Optimization`.
* \[x] Geen bestaande Roadmap 105 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 104 is lokaal aangemaakt als Local Realtime Dashboard V2, FastAPI/WebSocket Backend \& React Operator UI.

### Codebasecontrole

Breed bekeken met focus op dashboard, runtime, page registry, CLI en safety:

* \[x] `src/binance\_spot\_bot/ui/streamlit\_app.py`
* \[x] `src/binance\_spot\_bot/ui/page\_registry.py`
* \[x] `src/binance\_spot\_bot/ui/components.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] `pyproject.toml`

### Conclusie

De bestaande Streamlit app is breed en bevat veel pages, acties, reports en runtime-koppelingen. Dashboard V2 mag niet simpelweg een mini-dashboard blijven; het moet page-by-page parity krijgen met duidelijke prioriteit. Omdat `page\_registry.py` al alle dashboard pages definieert en live trading pages blokkeert, wordt die registry de centrale bron voor V2-route-parity. De runtime heeft al snapshots met de benodigde data, maar Dashboard V2 heeft compactere DTOs, event streams en payload limits nodig om instant updates soepel te houden.

\---

## 1\. Hoofddoel Roadmap 105

Maak Dashboard V2 bruikbaar als primaire lokale operator UI:

```text
Dashboard V2 MVP
→ page parity matrix
→ critical workflow migration
→ advanced page migration
→ realtime chart/state optimization
→ Streamlit legacy fallback
→ browser smoke + UAT acceptance
→ Dashboard V2 recommended mode
```

Na Roadmap 105 moet kunnen:

* \[ ] Dashboard V2 starten via CLI en lokaal gebruiken.
* \[ ] Alle page registry items hebben een V2-route of expliciete legacy placeholder.
* \[ ] Critical workflows werken in V2:

  * overview;
  * runtime controls;
  * demo spot trading;
  * demo pilot;
  * sessions;
  * evidence;
  * support/operator health;
  * readiness/logs/security.
* \[ ] Advanced workflows zijn gemigreerd of duidelijk als legacy gemarkeerd.
* \[ ] Streamlit blijft fallback maar wordt niet meer de aanbevolen UI voor realtime gebruik.
* \[ ] Dashboard V2 heeft API smoke, browser smoke, page parity report en no-live proof.
* \[ ] Dashboard V2 performance heeft meetbare budgets.
* \[ ] Operator docs/UAT scenario’s bevatten Dashboard V2.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe trading engine.
* \[ ] Geen nieuwe runtime refactor opnieuw bouwen.
* \[ ] Geen nieuwe data pipeline opnieuw bouwen.
* \[ ] Geen nieuwe modeltraining pipeline opnieuw bouwen.
* \[ ] Geen Streamlit direct verwijderen.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte account endpoint workflows.
* \[ ] Geen frontend CDN dat internet vereist.
* \[ ] Geen cloud dashboard.
* \[ ] Geen API endpoint dat raw secrets teruggeeft.

Wel doen:

* \[ ] Dashboard V2 feature parity bouwen.
* \[ ] Page-by-page migratie uitvoeren.
* \[ ] Streamlit legacy/fallback flow toevoegen.
* \[ ] Realtime charts verbeteren.
* \[ ] Frontend state reducer optimaliseren.
* \[ ] Browser smoke uitbreiden.
* \[ ] Operator docs/UAT integreren.
* \[ ] Performance budgets voor Dashboard V2 toevoegen.

\---

## 3\. Fase 0 - Dashboard V2 Parity Safety Contract

Nieuwe doc:

```text
docs/dashboard-v2-parity-safety-contract.md
```

Regels:

* \[ ] Dashboard V2 parity is local-only.
* \[ ] Geen live trading.
* \[ ] Geen live mode in routes, settings, selectors, tests of docs.
* \[ ] Alle POST actions gebruiken Dashboard V2 action policy.
* \[ ] Demo actions gebruiken bestaande demo guardrails.
* \[ ] Paper actions blijven paper-only.
* \[ ] Testnet-readiness stuurt geen orders.
* \[ ] Credential panels tonen alleen status/fingerprint.
* \[ ] WebSocket en REST payloads zijn secret-free.
* \[ ] Frontend toont altijd no-live banner.
* \[ ] Streamlit legacy mode mag geen extra capabilities krijgen.
* \[ ] Page parity mag geen live page introduceren.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen V2 parity geen live route/page toevoegt.
* \[ ] Tests bewijzen legacy Streamlit fallback geen live mode toevoegt.
* \[ ] Browser smoke valideert no-live banner op critical routes.
* \[ ] API smoke valideert no-live root payloads.

\---

## 4\. Fase 1 - Page Parity Matrix

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/page\_parity.py
```

Dataclasses:

* \[ ] `DashboardV2PageParityItem`
* \[ ] `DashboardV2PageParityReport`
* \[ ] `DashboardV2MigrationStatus`
* \[ ] `DashboardV2RouteRef`

Statuses:

* \[ ] migrated;
* \[ ] partial;
* \[ ] legacy\_placeholder;
* \[ ] planned;
* \[ ] blocked;
* \[ ] removed\_not\_allowed.

Per page:

* \[ ] page key;
* \[ ] Streamlit title;
* \[ ] V2 route;
* \[ ] migration status;
* \[ ] required API endpoints;
* \[ ] required WebSocket topics;
* \[ ] tests;
* \[ ] browser smoke coverage;
* \[ ] no-live proof status;
* \[ ] parity notes.

Acceptatiecriteria:

* \[ ] Report gebruikt `ui.page\_registry.PAGES` als bron.
* \[ ] Elke bestaande page heeft V2 status.
* \[ ] Missing V2 route wordt gerapporteerd.
* \[ ] Live page status is hard fail.
* \[ ] Report exporteert Markdown + JSON.

\---

## 5\. Fase 2 - V2 Navigation Shell \& Layout

Frontend:

```text
dashboard-v2/src/components/
  AppShell.tsx
  Sidebar.tsx
  TopBar.tsx
  RouteTabs.tsx
  SafetyBanner.tsx
  ConnectionStatus.tsx
  LegacyBadge.tsx
```

Taken:

* \[ ] Sidebar uit page parity matrix opbouwen.
* \[ ] Critical routes bovenaan zetten.
* \[ ] Advanced routes groeperen.
* \[ ] Legacy placeholders tonen met reden.
* \[ ] WebSocket status altijd zichtbaar.
* \[ ] Runtime mode/source/symbol altijd zichtbaar.
* \[ ] No-live banner sticky maken.
* \[ ] Error boundary per route.
* \[ ] Keyboard-safe navigation.

Acceptatiecriteria:

* \[ ] Alle V2 routes zichtbaar in navigatie.
* \[ ] Legacy pages zijn duidelijk gelabeld.
* \[ ] No-live banner blijft zichtbaar bij routewissel.
* \[ ] Browser smoke navigeert critical routes.
* \[ ] Geen full page reload bij routewissel.

\---

## 6\. Fase 3 - Critical Route Migration Pack 1

Migreer als eerste:

* \[ ] Overview.
* \[ ] Runtime Controls.
* \[ ] Readiness.
* \[ ] Logs \& Security.

Backend endpoints:

```text
GET /api/runtime/summary
GET /api/runtime/snapshot
GET /api/readiness
GET /api/logs/audit-tail
GET /api/security/redaction-self-test
POST /api/runtime/start
POST /api/runtime/pause
POST /api/runtime/stop
POST /api/runtime/step
POST /api/runtime/reset
```

WebSocket topics:

* \[ ] `runtime.status`
* \[ ] `runtime.snapshot.compact`
* \[ ] `runtime.alert`
* \[ ] `runtime.readiness`
* \[ ] `system.security`

Acceptatiecriteria:

* \[ ] Operator kan runtime starten/stoppen/stappen in V2.
* \[ ] Overview update realtime zonder full refresh.
* \[ ] Readiness blockers zichtbaar.
* \[ ] Logs/security tonen redacted data.
* \[ ] Browser smoke voor deze routes groen.

\---

## 7\. Fase 4 - Demo Spot Trading Migration

Frontend route:

```text
/demo-spot-trading
```

Panels:

* \[ ] Profile status.
* \[ ] Credential status/fingerprint.
* \[ ] Demo armed/disarmed.
* \[ ] Demo trading gate.
* \[ ] Order preview.
* \[ ] Test order.
* \[ ] Guarded demo place.
* \[ ] Open orders.
* \[ ] Reconciliation.
* \[ ] Demo order errors.
* \[ ] Cancel-on-stop status.

Backend endpoints:

```text
GET  /api/demo/status
POST /api/demo/arm
POST /api/demo/disarm
POST /api/demo/order-preview
POST /api/demo/test-order
POST /api/demo/place-guarded
POST /api/demo/reconcile
POST /api/demo/cancel-open-orders
```

Guardrails:

* \[ ] Wrong profile blocks actions.
* \[ ] Missing credentials blocks signed demo actions.
* \[ ] Not armed blocks guarded place.
* \[ ] Confirm phrase required.
* \[ ] Payload redacted.
* \[ ] No live wording.

Acceptatiecriteria:

* \[ ] Demo page reaches parity with Streamlit critical demo actions.
* \[ ] Guarded demo place cannot run without explicit guardrails.
* \[ ] Open orders update via WebSocket.
* \[ ] Reconciliation update via WebSocket.
* \[ ] Safety tests cover all action states.

\---

## 8\. Fase 5 - Demo Pilot Migration

Frontend route:

```text
/demo-pilot
```

Panels:

* \[ ] Pilot status.
* \[ ] Preset selector.
* \[ ] Start gate.
* \[ ] Operator checklist.
* \[ ] Pipeline rows.
* \[ ] Runner status.
* \[ ] Runner counters.
* \[ ] Runner heartbeat.
* \[ ] Runner command status.
* \[ ] Equity/PnL.
* \[ ] Reconciliation.
* \[ ] Export pilot report.

Backend endpoints:

```text
GET  /api/demo-pilot/status
GET  /api/demo-pilot/presets
GET  /api/demo-pilot/checklist
POST /api/demo-pilot/preflight
POST /api/demo-pilot/runner-start
POST /api/demo-pilot/runner-stop
POST /api/demo-pilot/runner-command
GET  /api/demo-pilot/report
```

Acceptatiecriteria:

* \[ ] Pilot runner status updates live.
* \[ ] Counters/heartbeat charts update without full refresh.
* \[ ] Stop command always accessible.
* \[ ] Reports downloadable.
* \[ ] Browser smoke covers demo pilot critical path.

\---

## 9\. Fase 6 - Sessions, Evidence \& Support Migration

Routes:

```text
/sessions
/evidence
/support
/operator
```

Sessions:

* \[ ] List sessions.
* \[ ] Session detail.
* \[ ] Fills.
* \[ ] Equity points.
* \[ ] Report paths.
* \[ ] Compare sessions placeholder.

Evidence:

* \[ ] Evidence manifest.
* \[ ] Evidence chain.
* \[ ] Operator evidence export.
* \[ ] No-live proof.
* \[ ] Download artifacts.

Support:

* \[ ] Support bundle create.
* \[ ] Support bundle verify.
* \[ ] Restore preview.
* \[ ] Redaction self-test.

Operator:

* \[ ] Operator health score.
* \[ ] Local ops snapshot.
* \[ ] Command manifest.
* \[ ] Environment doctor.
* \[ ] Artifact catalog.

Acceptatiecriteria:

* \[ ] Support/evidence flows work without Streamlit.
* \[ ] Downloads are restricted to allowed artifact paths.
* \[ ] Long-running actions show status.
* \[ ] Secret redaction tests pass.
* \[ ] Browser smoke covers support/evidence/operator routes.

\---

## 10\. Fase 7 - Market, Orders \& Account Migration

Routes:

```text
/market-data
/orders-account
```

Market data panels:

* \[ ] Source status.
* \[ ] REST/websocket/demo status.
* \[ ] Last candle.
* \[ ] Top of book.
* \[ ] Data quality.
* \[ ] Public cache status if available.
* \[ ] Chart data limits.

Orders/account panels:

* \[ ] Paper account.
* \[ ] Paper balances.
* \[ ] Paper fills.
* \[ ] Order lifecycle.
* \[ ] Demo open orders.
* \[ ] Reconciliation status.
* \[ ] Execution result.

Acceptatiecriteria:

* \[ ] Market status updates via WebSocket.
* \[ ] Paper account updates via WebSocket.
* \[ ] Order lifecycle table trims safely.
* \[ ] No raw account secrets.
* \[ ] Browser smoke covers market/orders routes.

\---

## 11\. Fase 8 - Strategy, Model, Evaluation \& Research Migration

Routes:

```text
/strategy-model
/evaluation
/strategy-lab
/research
```

Panels:

* \[ ] Active model metadata.
* \[ ] Signal explanation.
* \[ ] Model registry summary.
* \[ ] Evaluation report.
* \[ ] Walk-forward status.
* \[ ] Strategy templates.
* \[ ] Indicator warmup.
* \[ ] Notebook export.
* \[ ] Research artifacts.

Acceptatiecriteria:

* \[ ] Read-only model/evaluation panels migrated.
* \[ ] Any write/promote action remains confirm-gated or legacy placeholder.
* \[ ] Long reports lazy-load.
* \[ ] No live promotion language.
* \[ ] API smoke covers endpoints.

\---

## 12\. Fase 9 - Advanced Ops Pages Migration

Routes:

```text
/policy-governance
/ops-automation
/observability
/ai-ops-assistant
/action-center
/permissions
/disaster-recovery
/release-management
/roadmap-automation
/repo-knowledge
/test-selection
/performance
```

Migration approach:

* \[ ] Read-only first.
* \[ ] Export/report actions second.
* \[ ] Confirm-gated actions last.
* \[ ] Legacy placeholders where not safe yet.
* \[ ] Every action maps to existing CLI/operator function.
* \[ ] Every page has no-live banner.

Acceptatiecriteria:

* \[ ] All advanced pages have V2 route.
* \[ ] At least read-only payload available for each route.
* \[ ] Unsafe/destructive actions are not implemented or confirm-gated.
* \[ ] Page parity report marks status accurately.
* \[ ] Browser smoke covers selected advanced pages.

\---

## 13\. Fase 10 - Future Roadmap Pages Placeholder Migration

Routes from Roadmaps 095-103 currently represented in Streamlit:

* \[ ] Runtime Core.
* \[ ] Data Pipeline.
* \[ ] Model Training.
* \[ ] Model Monitoring.
* \[ ] Portfolio Ensemble.
* \[ ] Paper OS Audit.
* \[ ] Stabilization.
* \[ ] Operator Training.
* \[ ] UAT if Roadmap 103 added.

For each:

* \[ ] V2 route exists.
* \[ ] Shows implementation status.
* \[ ] Shows planned/available commands.
* \[ ] Shows no-live statement.
* \[ ] Links roadmap docs.
* \[ ] Does not fake completed implementation.

Acceptatiecriteria:

* \[ ] Planned pages are honest about availability.
* \[ ] Missing modules do not crash dashboard.
* \[ ] Placeholder is useful and operator-safe.
* \[ ] Page parity report distinguishes planned vs implemented.
* \[ ] Docs link to roadmap files.

\---

## 14\. Fase 11 - Realtime Chart Engine Optimization

Frontend chart architecture:

```text
dashboard-v2/src/charts/
  CandleChart.tsx
  EquityChart.tsx
  SignalMarkers.tsx
  FillMarkers.tsx
  RunnerCharts.tsx
  useChartData.ts
  chartLimits.ts
```

Optimization tasks:

* \[ ] Incremental candle append.
* \[ ] Incremental equity append.
* \[ ] Point trimming in reducer.
* \[ ] Avoid re-rendering entire dashboard on chart event.
* \[ ] Use memoized selectors.
* \[ ] Separate high-frequency chart state from global app state.
* \[ ] Drop stale events if client lagging.
* \[ ] Render payload-size warning.
* \[ ] Backend emits compact chart events.

Performance targets:

* \[ ] Chart append under 50 ms in normal local run.
* \[ ] Snapshot reducer under 30 ms for compact payload.
* \[ ] UI remains responsive with 1,000 candle points.
* \[ ] WebSocket reconnect under 3 seconds.

Acceptatiecriteria:

* \[ ] Chart reducer tests pass.
* \[ ] Payload limit tests pass.
* \[ ] Performance smoke produces report.
* \[ ] No chart requires full page reload.
* \[ ] Browser smoke verifies chart visible after live event.

\---

## 15\. Fase 12 - Frontend State Store Hardening

Store modules:

```text
dashboard-v2/src/store/
  runtimeStore.ts
  connectionStore.ts
  settingsStore.ts
  notificationStore.ts
  sessionStore.ts
  evidenceStore.ts
  operatorStore.ts
```

Tasks:

* \[ ] Normalize API entities.
* \[ ] Separate snapshot state from UI state.
* \[ ] Add event sequence numbers.
* \[ ] Ignore out-of-order events.
* \[ ] Add reconnect state hydration from `/api/runtime/snapshot`.
* \[ ] Add optimistic action status for POST actions.
* \[ ] Add error/toast store.
* \[ ] Add no-live proof status.

Acceptatiecriteria:

* \[ ] Store survives WebSocket reconnect.
* \[ ] Out-of-order event ignored safely.
* \[ ] Actions show pending/success/fail.
* \[ ] No secrets stored in frontend local storage.
* \[ ] Unit tests cover reducers.

\---

## 16\. Fase 13 - Streamlit Legacy Mode

Goal: keep Streamlit as fallback while Dashboard V2 becomes recommended.

Changes:

* \[ ] Add docs explaining Streamlit legacy/fallback.
* \[ ] Add CLI message recommending Dashboard V2 for realtime use.
* \[ ] Add `dashboard-legacy` alias for Streamlit launcher.
* \[ ] Keep old `dashboard` command backward-compatible.
* \[ ] Add optional prompt/flag to choose V2 vs legacy.
* \[ ] Add Streamlit banner: `Legacy dashboard - realtime Dashboard V2 recommended`.
* \[ ] Do not remove Streamlit tests.

Acceptatiecriteria:

* \[ ] Existing Streamlit launch still works.
* \[ ] Dashboard V2 launch works separately.
* \[ ] Docs explain difference.
* \[ ] No breaking CLI changes.
* \[ ] Legacy mode does not introduce live mode.

\---

## 17\. Fase 14 - API \& Frontend Error Handling

Backend:

* \[ ] Typed error model.
* \[ ] Redacted exception messages.
* \[ ] Action failure details.
* \[ ] WebSocket error events.
* \[ ] Health degraded state.
* \[ ] 404/route fallback safe.

Frontend:

* \[ ] Route-level error boundaries.
* \[ ] Panel-level error boxes.
* \[ ] Retry buttons.
* \[ ] WebSocket reconnect notice.
* \[ ] Last successful snapshot shown.
* \[ ] Safe empty states.

Acceptatiecriteria:

* \[ ] Backend exception does not leak secrets.
* \[ ] Frontend panel failure does not crash whole app.
* \[ ] WebSocket disconnect recovers.
* \[ ] Browser smoke checks no fatal console errors.
* \[ ] Error screenshots optional.

\---

## 18\. Fase 15 - Dashboard V2 Performance Budgets

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/performance.py
```

Metrics:

* \[ ] backend health latency;
* \[ ] snapshot API latency;
* \[ ] WebSocket event latency;
* \[ ] events per second;
* \[ ] dropped events;
* \[ ] payload size;
* \[ ] frontend initial load;
* \[ ] chart update latency;
* \[ ] route transition time;
* \[ ] memory estimate best-effort.

Budgets:

* \[ ] `/api/health` under 100 ms local.
* \[ ] compact snapshot under 200 ms local.
* \[ ] WebSocket heartbeat stable.
* \[ ] initial app load under 3 seconds local after build.
* \[ ] critical route render under 1 second after data loaded.
* \[ ] payload under configured limit.

Acceptatiecriteria:

* \[ ] Performance report is JSON + Markdown.
* \[ ] Check-all deep profile can run budget check.
* \[ ] Budget failures show exact route/API.
* \[ ] Performance report links Roadmap 093 where available.
* \[ ] No-live proof included.

\---

## 19\. Fase 16 - Dashboard V2 Browser Smoke Matrix

Critical routes:

* \[ ] `/`
* \[ ] `/runtime`
* \[ ] `/demo-spot-trading`
* \[ ] `/demo-pilot`
* \[ ] `/sessions`
* \[ ] `/evidence`
* \[ ] `/support`
* \[ ] `/operator`
* \[ ] `/readiness`
* \[ ] `/logs-security`

Checks per route:

* \[ ] route loads;
* \[ ] no-live banner visible;
* \[ ] no console fatal error;
* \[ ] WebSocket status visible;
* \[ ] primary panel visible;
* \[ ] safe empty state if no data;
* \[ ] no live selector visible.

Acceptatiecriteria:

* \[ ] Browser smoke matrix report exists.
* \[ ] No-live missing is hard fail.
* \[ ] Route failure maps to page parity item.
* \[ ] Screenshots optional.
* \[ ] Report secret-free.

\---

## 20\. Fase 17 - Dashboard V2 API Contract Tests

Contract files:

```text
tests/contracts/dashboard\_v2/
  health.schema.json
  config.schema.json
  pages.schema.json
  snapshot.schema.json
  event.schema.json
  action-result.schema.json
```

Tasks:

* \[ ] Snapshot schema stable.
* \[ ] Event schema stable.
* \[ ] Action result schema stable.
* \[ ] No-live root field required.
* \[ ] No raw secret fields allowed.
* \[ ] Decimal fields stringified.

Acceptatiecriteria:

* \[ ] Contract tests pass.
* \[ ] Breaking schema changes require docs/release note.
* \[ ] Frontend generated/manual types match API.
* \[ ] API examples in docs valid.
* \[ ] Secret-like fixture redacted.

\---

## 21\. Fase 18 - Dashboard V2 Docs \& Operator Training

Docs:

```text
docs/dashboard-v2/
  feature-parity.md
  route-guide.md
  realtime-updates.md
  streamlit-legacy-mode.md
  browser-smoke-matrix.md
  performance-budgets.md
  troubleshooting-v2.md
```

Operator docs updates:

* \[ ] Dashboard V2 quick start.
* \[ ] Dashboard V2 vs Streamlit explanation.
* \[ ] V2 route walkthroughs.
* \[ ] V2 troubleshooting playbook.
* \[ ] V2 no-live proof.
* \[ ] V2 support/evidence pages.

Acceptatiecriteria:

* \[ ] Docs mention local-only/no-live.
* \[ ] Docs include launch commands.
* \[ ] Docs include screenshots placeholders or descriptions.
* \[ ] Docs consistency checks pass.
* \[ ] UAT scenarios reference V2.

\---

## 22\. Fase 19 - UAT \& Feedback Integration

Roadmap 103 integration:

* \[ ] UAT scenario: first Dashboard V2 launch.
* \[ ] UAT scenario: realtime runtime updates.
* \[ ] UAT scenario: demo spot trading guardrails.
* \[ ] UAT scenario: sessions/evidence/support navigation.
* \[ ] UAT scenario: no-live proof in Dashboard V2.
* \[ ] Feedback form category for Dashboard V2 UX.
* \[ ] Usability scorecard includes Dashboard V2 route clarity.

Acceptatiecriteria:

* \[ ] UAT evidence can include Dashboard V2.
* \[ ] Feedback backlog can create V2 UX items.
* \[ ] No-live training includes V2 proof.
* \[ ] UAT sign-off can mention V2 paper-only acceptance.
* \[ ] No-live proof preserved.

\---

## 23\. Fase 20 - Check-All \& Test Selection Integration

Check-all additions:

* \[ ] `dashboard\_v2\_api\_smoke`
* \[ ] `dashboard\_v2\_page\_parity`
* \[ ] `dashboard\_v2\_no\_live\_routes`
* \[ ] `dashboard\_v2\_static\_build\_present` optional
* \[ ] `dashboard\_v2\_browser\_smoke` in deep/profile mode
* \[ ] `dashboard\_v2\_performance\_budget` optional/deep

Test selector:

* \[ ] Backend API changes select API contract tests.
* \[ ] Frontend route changes select browser smoke.
* \[ ] Action policy changes select safety tests.
* \[ ] Chart changes select reducer/performance tests.
* \[ ] Page registry changes select page parity tests.

Acceptatiecriteria:

* \[ ] Check-all remains green without frontend build when optional.
* \[ ] Deep profile requires V2 browser smoke if V2 enabled.
* \[ ] No-live route check is always hard fail.
* \[ ] Test selection maps changes correctly.
* \[ ] Reports secret-free.

\---

## 24\. Fase 21 - Release \& Migration Evidence

Roadmap 089/090 integration:

* \[ ] Dashboard V2 migration status in release notes.
* \[ ] Page parity report attached to release evidence.
* \[ ] Browser smoke report attached.
* \[ ] Performance budget report attached.
* \[ ] Streamlit legacy status documented.
* \[ ] Rollback path: use Streamlit legacy.
* \[ ] Roadmap completion gate requires V2 evidence.

Acceptatiecriteria:

* \[ ] Release evidence includes Dashboard V2 status.
* \[ ] Migration notes explain no breaking default.
* \[ ] Rollback path documented.
* \[ ] Roadmap mover can reference V2 evidence.
* \[ ] No-live proof included.

\---

## 25\. CLI Commands

Nieuwe of uitgebreide commands:

```powershell
python -m binance\_spot\_bot.cli dashboard-v2
python -m binance\_spot\_bot.cli dashboard-v2 --no-browser
python -m binance\_spot\_bot.cli dashboard-v2-route-list --json
python -m binance\_spot\_bot.cli dashboard-v2-page-parity --json
python -m binance\_spot\_bot.cli dashboard-v2-api-smoke --json
python -m binance\_spot\_bot.cli dashboard-v2-browser-smoke --url http://127.0.0.1:8800 --json
python -m binance\_spot\_bot.cli dashboard-v2-performance --json
python -m binance\_spot\_bot.cli dashboard-v2-no-live-proof --json
python -m binance\_spot\_bot.cli dashboard-legacy
python -m binance\_spot\_bot.cli dashboard-choice
```

Acceptatiecriteria:

* \[ ] Commands werken lokaal.
* \[ ] Commands ondersteunen JSON output.
* \[ ] Commands gebruiken safe env.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Commands zijn opgenomen in operator CLI cookbook.

\---

## 26\. Tests

### Backend tests

* \[ ] `tests/test\_dashboard\_v2\_page\_parity.py`
* \[ ] `tests/test\_dashboard\_v2\_route\_inventory.py`
* \[ ] `tests/test\_dashboard\_v2\_runtime\_routes.py`
* \[ ] `tests/test\_dashboard\_v2\_demo\_routes.py`
* \[ ] `tests/test\_dashboard\_v2\_operator\_routes.py`
* \[ ] `tests/test\_dashboard\_v2\_sessions\_evidence\_support.py`
* \[ ] `tests/test\_dashboard\_v2\_performance.py`
* \[ ] `tests/test\_dashboard\_v2\_legacy\_mode.py`

### Frontend tests

* \[ ] layout/no-live banner;
* \[ ] route navigation;
* \[ ] runtime store reducers;
* \[ ] WebSocket reconnect reducer;
* \[ ] action button states;
* \[ ] chart reducers;
* \[ ] legacy placeholders;
* \[ ] error boundaries.

### Browser tests

* \[ ] critical route matrix;
* \[ ] runtime control smoke;
* \[ ] demo guardrail smoke;
* \[ ] support/evidence smoke;
* \[ ] no-live selector proof;
* \[ ] console error check.

### Safety tests

* \[ ] live route absent;
* \[ ] live mode selector absent;
* \[ ] signed/order/account routes absent;
* \[ ] raw secrets redacted;
* \[ ] demo guarded actions require confirm;
* \[ ] Streamlit legacy still no-live;
* \[ ] WebSocket payload secret-free;
* \[ ] all root payloads have `live\_trading\_enabled=False`.

\---

## 27\. Codex bouwvolgorde

### PR 1 - Parity Safety Contract + Page Parity

* \[ ] `docs/dashboard-v2-parity-safety-contract.md`
* \[ ] `dashboard\_v2/page\_parity.py`
* \[ ] page parity CLI command.
* \[ ] tests for all page registry items.

### PR 2 - Navigation Shell + Route Placeholders

* \[ ] React shell.
* \[ ] route config from API.
* \[ ] legacy placeholder component.
* \[ ] no-live banner.
* \[ ] browser smoke for nav.

### PR 3 - Critical Route Pack 1

* \[ ] Overview.
* \[ ] Runtime Controls.
* \[ ] Readiness.
* \[ ] Logs/Security.
* \[ ] API routes and browser tests.

### PR 4 - Demo Spot Trading

* \[ ] Demo status/actions API.
* \[ ] Demo Spot route.
* \[ ] guardrail tests.
* \[ ] WebSocket open order updates.

### PR 5 - Demo Pilot

* \[ ] Demo pilot API.
* \[ ] Demo pilot page.
* \[ ] runner status/counters/heartbeat.
* \[ ] browser smoke.

### PR 6 - Sessions/Evidence/Support/Operator

* \[ ] Session APIs.
* \[ ] Evidence APIs.
* \[ ] Support APIs.
* \[ ] Operator APIs.
* \[ ] downloads and path safety.

### PR 7 - Market/Orders/Account + Charts

* \[ ] Market data route.
* \[ ] Orders/account route.
* \[ ] Chart components and reducers.
* \[ ] payload limits.

### PR 8 - Strategy/Model/Evaluation/Research + Advanced Read-Only Pages

* \[ ] Read-only advanced pages.
* \[ ] Lazy-loaded reports.
* \[ ] legacy placeholders for unsafe/missing actions.

### PR 9 - Performance, Smoke, Check-All

* \[ ] V2 performance report.
* \[ ] Browser smoke matrix.
* \[ ] Check-all integration.
* \[ ] Test selection integration.

### PR 10 - Streamlit Legacy, Docs, UAT, Release Evidence

* \[ ] Streamlit legacy docs/banner.
* \[ ] Dashboard V2 operator docs.
* \[ ] UAT scenarios.
* \[ ] release/migration evidence.
* \[ ] final page parity report.

\---

## 28\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 105 PR 1: Dashboard V2 Parity Safety Contract + Page Parity Matrix.

Maak docs/dashboard-v2-parity-safety-contract.md.

Maak src/binance\_spot\_bot/dashboard\_v2/page\_parity.py met:
- DashboardV2PageParityItem
- DashboardV2PageParityReport
- DashboardV2MigrationStatus
- DashboardV2RouteRef
- build\_dashboard\_v2\_page\_parity\_report(...)
- dashboard\_v2\_page\_parity\_to\_dict(...)
- write\_dashboard\_v2\_page\_parity\_report(...)

Gebruik src/binance\_spot\_bot/ui/page\_registry.py als bron.

Per page moet het report bevatten:
- page\_key
- title
- streamlit\_available=True
- v2\_route
- migration\_status: migrated, partial, legacy\_placeholder, planned, blocked
- required\_api\_endpoints
- required\_ws\_topics
- browser\_smoke\_required
- no\_live\_statement
- live\_trading\_enabled=False
- notes

Validatie:
- duplicate page keys blokkeren
- page met live\_trading\_enabled=True blokkeren
- missing v2 route wordt warning
- critical pages zonder migrated/partial/legacy\_placeholder worden warning
- output moet JSON serializable en secret-free zijn

Critical pages:
- overview
- demo\_spot\_trading
- bot\_controls
- risk\_controls
- market\_data
- orders\_account
- sessions
- readiness
- logs\_security
- demo\_pilot

Voeg CLI command toe:
python -m binance\_spot\_bot.cli dashboard-v2-page-parity --json

Voeg tests toe:
- test\_dashboard\_v2\_page\_parity\_all\_registry\_pages
- test\_dashboard\_v2\_page\_parity\_rejects\_live\_page
- test\_dashboard\_v2\_page\_parity\_warns\_missing\_route
- test\_dashboard\_v2\_page\_parity\_json\_serializable
- test\_dashboard\_v2\_page\_parity\_secret\_free
- test\_dashboard\_v2\_page\_parity\_no\_live\_statement

Geen React code in deze PR.
Geen runtime bridge wijzigen.
Geen Streamlit verwijderen.
Geen live trading.
Geen signed endpoints.
Geen account/order endpoints.
```

Waarom eerst:

* Roadmap 105 draait om feature parity; daarvoor moet eerst exact zichtbaar zijn welke Streamlit pages al V2 hebben, welke ontbreken en welke legacy blijven.
* Het raakt runtime/execution niet.
* Het gebruikt de bestaande page registry als safety-bron.
* Het is klein genoeg voor Codex.
* Het maakt vervolg-PR’s veel gerichter.

\---

## 29\. Definition of Done

Roadmap 105 is klaar als:

* \[ ] Dashboard V2 Parity Safety Contract bestaat.
* \[ ] Page Parity Matrix werkt.
* \[ ] V2 navigation shell werkt.
* \[ ] Critical Route Migration Pack 1 klaar is.
* \[ ] Demo Spot Trading page gemigreerd is.
* \[ ] Demo Pilot page gemigreerd is.
* \[ ] Sessions/Evidence/Support/Operator pages gemigreerd zijn.
* \[ ] Market/Orders/Account pages gemigreerd zijn.
* \[ ] Strategy/Model/Evaluation/Research read-only pages gemigreerd zijn.
* \[ ] Advanced ops pages hebben V2 route of legacy placeholder.
* \[ ] Realtime charts zijn geoptimaliseerd.
* \[ ] Frontend state store is gehard.
* \[ ] Streamlit legacy mode is gedocumenteerd.
* \[ ] API/frontend error handling werkt.
* \[ ] Dashboard V2 performance budgets werken.
* \[ ] Browser smoke matrix werkt.
* \[ ] API contract tests werken.
* \[ ] Operator docs/UAT integratie bestaat.
* \[ ] Check-all bevat Dashboard V2 checks.
* \[ ] Release/migration evidence bevat Dashboard V2 status.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen payloads secret-free zijn.
* \[ ] Browser smoke groen is.
* \[ ] Streamlit fallback blijft werken.
* \[ ] Dashboard V2 is aanbevolen lokale realtime UI.
* \[ ] Roadmap 105 kan na uitvoering naar `Voltooid docs`.

\---

## 30\. Verwachte Roadmap 106 daarna

Na Roadmap 105 is de beste vervolgstap waarschijnlijk:

```text
Roadmap 106 - Dashboard V2 UX Polish, Realtime Chart Optimization \& Operator Workflow Simplification
```

Mogelijke inhoud:

* \[ ] UAT-feedback uit Roadmap 103 verwerken.
* \[ ] Dashboard V2 flows vereenvoudigen.
* \[ ] Onboarding wizard in V2.
* \[ ] Better empty states.
* \[ ] Mobile/responsive polish.
* \[ ] Chart performance verbeteren.
* \[ ] Accessibility verbeteringen.
* \[ ] Streamlit deprecation decision.
* \[ ] Still no live trading.

```

Alternatief als parity nog niet hoog genoeg is:

```text
Roadmap 106 - Dashboard V2 Remaining Page Migration, Legacy Gap Burn-Down \& Browser Smoke Hardening
```

