# Roadmap 110 - Dashboard V2 Advanced Realtime Analytics, Multi-Panel Layouts \& Operator Customization

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/110-roadmap-dashboard-v2-advanced-realtime-analytics-multi-panel-layouts-operator-customization.md
```

## Samenvatting

Roadmap 104 bouwt Dashboard V2 naast Streamlit met FastAPI/WebSocket/React.

Roadmap 105 migreert feature parity van Streamlit naar Dashboard V2.

Roadmap 106 maakt Dashboard V2 performant, lokaal packagebaar, offline/static, browser-smoke-ready en cutover-ready.

Roadmap 107 vereenvoudigt operatorflows, verwerkt UAT-feedback en maakt Streamlit deprecation planning concreet.

Roadmap 108 zet Dashboard V2 als primaire UI neer, maakt V2-only operator mode en houdt Streamlit als legacy/fallback.

Roadmap 109 maakt Streamlit removal-candidate, dependency isolation, V2-only release hardening, legacy archive en removal readiness gate.

Roadmap 110 is de logische volgende stap als Dashboard V2 primary/V2-only betrouwbaar is: **maak Dashboard V2 krachtiger dan Streamlit ooit was** met advanced realtime analytics, multi-panel workspaces, opgeslagen operator layouts, watchlists, symbol groups, synchronized charts, local-only personalization, analytics presets, share/export/import van layouts en evidence-backed workspace validation.

Live trading blijft volledig buiten scope. Alle analytics, customization en dashboards blijven local-only en demo/paper/testnet-readiness-only. Geen live mode, geen signed real-order endpoints, geen echte account workflows en geen externe telemetry.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 110`, `110-roadmap`, `Dashboard V2 Advanced Realtime Analytics`, `Multi-Panel Layouts`, `Operator Customization` en `custom dashboard layout`.
* \[x] Geen bestaande Roadmap 110 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 109 is lokaal aangemaakt als Streamlit Removal Candidate, Legacy Cleanup \& Dashboard V2-Only Release Hardening.

### Codebasecontrole

Breed bekeken met focus op Dashboard V2 vervolg, runtime snapshots, page registry, safe modes, check-all en operator evidence:

* \[x] `src/binance\_spot\_bot/ui/page\_registry.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] roadmaplijn 104-109.

### Belangrijke bestaande basis

De codebase heeft nu:

* \[x] Een page registry met 36 dashboard pages en een guard die live trading pages blokkeert.
* \[x] Runtime modes beperkt tot `demo`, `paper` en `testnet-readiness`.
* \[x] Runtime snapshots met candles, signals, fills, equity, testnet prechecks, market data, top of book, data quality, session summary, recent sessions, active model, exchange profile, credential status, alerts, paper account, report paths, readiness, demo connection, demo account, open demo orders, demo pilot, reconciliation en demo order errors.
* \[x] Check-all forceert `LIVE\_TRADING\_ENABLED=false`, `KILL\_SWITCH=true` en `PYTHONPATH=src`.
* \[x] Operator tooling heeft al evidence, support bundles, redaction, operator quality gate, local ops snapshots en reports.
* \[x] Roadmap 104-109 plannen Dashboard V2 foundation, parity, performance, UX, V2-only release en Streamlit legacy/removal gates.

### Belangrijkste gat na Roadmap 109

Na Roadmap 109 is Dashboard V2 primair/V2-only en Streamlit legacy/verwijderd/geïsoleerd volgens gate. Daarna mist nog de echte meerwaarde van een moderne dashboard UI:

* \[ ] Geen aanpasbare operator workspaces.
* \[ ] Geen drag/drop of config-based multi-panel layouts.
* \[ ] Geen opgeslagen views per workflow.
* \[ ] Geen watchlists/symbol groups.
* \[ ] Geen synchronized charts.
* \[ ] Geen multi-chart layout voor symbol + indicator + equity + orders.
* \[ ] Geen local-only operator customization store.
* \[ ] Geen workspace import/export.
* \[ ] Geen workspace evidence bundle.
* \[ ] Geen analytics presets voor paper/demo/model/portfolio workflows.
* \[ ] Geen operator productivity metrics per workspace.
* \[ ] Geen V2 advanced dashboard mode met performance budgets.

Roadmap 110 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 110

Maak Dashboard V2 een echte lokale realtime operator workspace:

```text
Dashboard V2 V2-only
→ workspace schema
→ widget registry
→ saved layouts
→ realtime analytics query layer
→ multi-panel dashboard
→ synchronized charts
→ local personalization
→ workspace evidence
```

Na Roadmap 110 moet de operator:

* \[ ] eigen dashboard layouts kunnen opslaan;
* \[ ] widgets kunnen toevoegen/verwijderen/verplaatsen;
* \[ ] meerdere panels tegelijk kunnen monitoren;
* \[ ] watchlists/symbol groups kunnen beheren;
* \[ ] candle/equity/signal/fill/risk/model/portfolio widgets combineren;
* \[ ] chart crosshair/time-range sync kunnen gebruiken;
* \[ ] analytics presets kunnen kiezen;
* \[ ] workspace layouts kunnen exporteren/importeren;
* \[ ] local-only personalisatie kunnen resetten;
* \[ ] no-live proof en safety banners in elke workspace blijven zien;
* \[ ] performance en evidence rapporten voor workspaces kunnen maken.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen Dashboard V2 foundation opnieuw bouwen.
* \[ ] Geen Streamlit removal opnieuw bouwen.
* \[ ] Geen runtime refactor opnieuw bouwen.
* \[ ] Geen trading engine opnieuw bouwen.
* \[ ] Geen modeltraining/data/portfolio pipeline opnieuw bouwen.
* \[ ] Geen cloud dashboard.
* \[ ] Geen remote telemetry.
* \[ ] Geen externe layout sync.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte account workflows.
* \[ ] Geen customization die safety/no-live widgets kan verbergen.
* \[ ] Geen dashboard plugin systeem dat arbitraire code uitvoert.

Wel doen:

* \[ ] local-only workspace schema;
* \[ ] safe widget registry;
* \[ ] saved layouts;
* \[ ] workspace import/export;
* \[ ] realtime analytics query layer;
* \[ ] multi-panel frontend;
* \[ ] synchronized charts;
* \[ ] watchlists;
* \[ ] operator customization store;
* \[ ] workspace performance budgets;
* \[ ] evidence/reporting/tests.

\---

## 3\. Fase 0 - Dashboard V2 Customization Safety Contract

Nieuw docbestand:

```text
docs/dashboard-v2-customization-safety-contract.md
```

Regels:

* \[ ] Customization is local-only.
* \[ ] Geen remote telemetry.
* \[ ] Geen cloud layout sync.
* \[ ] Geen live trading.
* \[ ] Geen live mode in layouts/widgets/actions.
* \[ ] Alleen demo, paper en testnet-readiness.
* \[ ] Safety banner/no-live proof mag niet verborgen worden.
* \[ ] Stop/runtime safety controls mogen niet verborgen worden in operator mode.
* \[ ] Widget registry is allowlisted.
* \[ ] Geen arbitraire JS/plugin code in layouts.
* \[ ] Geen raw secrets in layouts.
* \[ ] Layout import moet gevalideerd en geredact worden.
* \[ ] Export moet secret-free zijn.
* \[ ] Reports bevatten `live\_trading\_enabled=False`.
* \[ ] Workspace evidence is verplicht voor advanced workspace release.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen no-live widget niet verwijderd kan worden.
* \[ ] Tests bewijzen live widgets/actions geblokkeerd worden.
* \[ ] Tests bewijzen layout import geen scripts accepteert.
* \[ ] Tests bewijzen exports secret-free zijn.

\---

## 4\. Fase 1 - Workspace Schema

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/workspace\_schema.py
```

Dataclasses:

* \[ ] `DashboardWorkspace`
* \[ ] `DashboardWorkspaceGrid`
* \[ ] `DashboardWorkspacePanel`
* \[ ] `DashboardWorkspaceWidget`
* \[ ] `DashboardWorkspaceLayout`
* \[ ] `DashboardWorkspaceValidationResult`
* \[ ] `DashboardWorkspaceMetadata`

Workspace fields:

* \[ ] workspace\_id;
* \[ ] name;
* \[ ] description;
* \[ ] version;
* \[ ] operator\_level;
* \[ ] mode\_scope:

  * demo;
  * paper;
  * testnet-readiness;
  * all\_safe\_modes.
* \[ ] grid columns;
* \[ ] panels;
* \[ ] widgets;
* \[ ] widget settings;
* \[ ] safety widgets locked;
* \[ ] created\_at\_ms;
* \[ ] updated\_at\_ms;
* \[ ] live\_trading\_enabled=false;
* \[ ] no\_live\_statement.

Panel fields:

* \[ ] panel\_id;
* \[ ] title;
* \[ ] x/y/w/h;
* \[ ] min\_w/min\_h;
* \[ ] widget\_id;
* \[ ] pinned;
* \[ ] collapsed;
* \[ ] refresh\_policy;
* \[ ] query\_scope.

Acceptatiecriteria:

* \[ ] Workspace schema is JSON-serializable.
* \[ ] Duplicate panel/widget ids worden geblokkeerd.
* \[ ] Safety widgets kunnen niet verwijderd worden.
* \[ ] Live mode scope wordt geblokkeerd.
* \[ ] Tests dekken valid/invalid layouts.

\---

## 5\. Fase 2 - Safe Widget Registry

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/widget\_registry.py
```

Widget categories:

* \[ ] safety;
* \[ ] runtime;
* \[ ] market;
* \[ ] chart;
* \[ ] paper;
* \[ ] demo;
* \[ ] risk;
* \[ ] model;
* \[ ] portfolio;
* \[ ] evidence;
* \[ ] support;
* \[ ] operator;
* \[ ] performance;
* \[ ] logs;
* \[ ] training/uat;
* \[ ] advanced.

Core widgets:

* \[ ] no\_live\_banner;
* \[ ] runtime\_status;
* \[ ] stop\_button;
* \[ ] mode\_source\_symbol;
* \[ ] candle\_chart;
* \[ ] equity\_chart;
* \[ ] signal\_markers;
* \[ ] fill\_markers;
* \[ ] paper\_account;
* \[ ] risk\_decision;
* \[ ] risk\_block\_summary;
* \[ ] alerts\_inbox;
* \[ ] demo\_order\_status;
* \[ ] session\_summary;
* \[ ] active\_model;
* \[ ] model\_health;
* \[ ] portfolio\_allocation;
* \[ ] evidence\_manifest;
* \[ ] support\_bundle\_status;
* \[ ] operator\_quality\_gate;
* \[ ] websocket\_status;
* \[ ] performance\_budget\_status.

Per widget:

* \[ ] widget\_type;
* \[ ] title;
* \[ ] category;
* \[ ] required\_permissions;
* \[ ] safe\_modes;
* \[ ] data\_sources;
* \[ ] default\_size;
* \[ ] min\_size;
* \[ ] max\_instances;
* \[ ] locked;
* \[ ] can\_export;
* \[ ] action\_policy;
* \[ ] secret\_safe=true.

Acceptatiecriteria:

* \[ ] Registry is allowlisted.
* \[ ] Geen live widget types.
* \[ ] Safety widgets locked.
* \[ ] Widget settings validated.
* \[ ] Tests cover widget registry validation.

\---

## 6\. Fase 3 - Workspace Store

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/workspace\_store.py
```

Storage:

```text
data/dashboard-v2/workspaces/
  layouts/
  presets/
  exports/
  reports/
  evidence/
```

Functies:

* \[ ] save workspace;
* \[ ] load workspace;
* \[ ] list workspaces;
* \[ ] delete workspace with confirm;
* \[ ] clone workspace;
* \[ ] set default workspace;
* \[ ] export workspace;
* \[ ] import workspace;
* \[ ] validate workspace manifest;
* \[ ] verify hashes.

Acceptatiecriteria:

* \[ ] Store is local-only.
* \[ ] Store uses manifest/hash.
* \[ ] Store rejects unsafe paths.
* \[ ] Store redacts secret-like values.
* \[ ] Tests use temp dirs.

\---

## 7\. Fase 4 - Workspace Presets

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/workspace\_presets.py
```

Presets:

### `operator\_overview`

* \[ ] no-live banner;
* \[ ] runtime status;
* \[ ] candle chart;
* \[ ] equity;
* \[ ] alerts;
* \[ ] session summary.

### `demo\_spot\_monitor`

* \[ ] no-live banner;
* \[ ] demo connection;
* \[ ] demo order status;
* \[ ] reconciliation;
* \[ ] candle chart;
* \[ ] alerts.

### `paper\_session\_trader`

* \[ ] no-live banner;
* \[ ] paper account;
* \[ ] risk decision;
* \[ ] equity curve;
* \[ ] fills table;
* \[ ] session report.

### `market\_analysis`

* \[ ] candle chart;
* \[ ] top of book;
* \[ ] spread;
* \[ ] volume;
* \[ ] data quality;
* \[ ] watchlist.

### `model\_ops`

* \[ ] active model;
* \[ ] model health;
* \[ ] signal confidence;
* \[ ] prediction drift;
* \[ ] monitoring alerts.

### `portfolio\_ops`

* \[ ] portfolio allocation;
* \[ ] risk budget;
* \[ ] attribution;
* \[ ] rotation status.

### `support\_evidence`

* \[ ] support bundle;
* \[ ] evidence manifest;
* \[ ] local ops snapshot;
* \[ ] operator quality gate.

Acceptatiecriteria:

* \[ ] Presets validate through workspace schema.
* \[ ] Presets contain mandatory safety widgets.
* \[ ] Presets can be cloned.
* \[ ] Presets are versioned.
* \[ ] Tests cover all presets.

\---

## 8\. Fase 5 - Realtime Analytics Query Layer

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/analytics\_query.py
```

Query scopes:

* \[ ] runtime\_snapshot;
* \[ ] candles;
* \[ ] equity\_points;
* \[ ] signals;
* \[ ] fills;
* \[ ] risk\_blocks;
* \[ ] alerts;
* \[ ] sessions;
* \[ ] model\_status;
* \[ ] portfolio\_status;
* \[ ] operator\_evidence;
* \[ ] support\_status;
* \[ ] performance\_metrics.

Query features:

* \[ ] tail limit;
* \[ ] time range;
* \[ ] symbol filter;
* \[ ] mode filter;
* \[ ] session filter;
* \[ ] model alias filter;
* \[ ] severity filter;
* \[ ] aggregation;
* \[ ] downsampling;
* \[ ] payload size limit;
* \[ ] secret redaction.

Acceptatiecriteria:

* \[ ] Query layer works from current RuntimeSnapshot.
* \[ ] Query layer works from session store fixtures.
* \[ ] Tail limits enforced.
* \[ ] Live mode blocked.
* \[ ] Tests cover filters/aggregation/downsampling.

\---

## 9\. Fase 6 - Analytics API Endpoints

Nieuwe API routes:

```text
GET /api/workspaces
POST /api/workspaces
GET /api/workspaces/{workspace\_id}
PUT /api/workspaces/{workspace\_id}
DELETE /api/workspaces/{workspace\_id}
POST /api/workspaces/{workspace\_id}/clone
POST /api/workspaces/{workspace\_id}/export
POST /api/workspaces/import
GET /api/workspace-presets
GET /api/widgets
GET /api/analytics/query
GET /api/analytics/series/{series\_name}
GET /api/analytics/summary
WS  /ws/workspace/{workspace\_id}
```

API regels:

* \[ ] All responses include `live\_trading\_enabled=False`.
* \[ ] Mutation routes use local action policy.
* \[ ] Delete requires confirm.
* \[ ] Import validates schema.
* \[ ] Export redacts.
* \[ ] WebSocket workspace stream only allowed widgets.
* \[ ] Payload limits enforced.

Acceptatiecriteria:

* \[ ] FastAPI TestClient covers routes.
* \[ ] Import rejects unsafe layout.
* \[ ] Delete requires confirm.
* \[ ] Widget list has no live widgets.
* \[ ] WebSocket workspace stream works with fake events.

\---

## 10\. Fase 7 - Frontend Workspace Grid

Frontend modules:

```text
dashboard-v2/src/workspace/
  WorkspacePage.tsx
  WorkspaceGrid.tsx
  WorkspacePanel.tsx
  WidgetFrame.tsx
  WidgetPicker.tsx
  WorkspaceToolbar.tsx
  WorkspaceSettings.tsx
```

Functionaliteit:

* \[ ] multi-panel grid;
* \[ ] add widget;
* \[ ] remove widget;
* \[ ] resize panel;
* \[ ] move panel;
* \[ ] clone panel;
* \[ ] collapse panel;
* \[ ] save layout;
* \[ ] reset layout;
* \[ ] switch workspace;
* \[ ] safety widgets locked;
* \[ ] responsive layout.

Acceptatiecriteria:

* \[ ] Operator can create workspace from preset.
* \[ ] Operator can add/remove non-safety widget.
* \[ ] Safety banner cannot be removed.
* \[ ] Layout saves locally.
* \[ ] Browser smoke covers workspace edit flow.

\---

## 11\. Fase 8 - Widget Library Frontend

Frontend widgets:

```text
dashboard-v2/src/widgets/
```

Safety:

* \[ ] NoLiveBannerWidget;
* \[ ] StopButtonWidget;
* \[ ] RuntimeModeWidget;
* \[ ] WebSocketStatusWidget.

Runtime:

* \[ ] RuntimeStatusWidget;
* \[ ] RuntimeControlsWidget;
* \[ ] LatestSnapshotWidget.

Market:

* \[ ] CandleChartWidget;
* \[ ] TopOfBookWidget;
* \[ ] DataQualityWidget;
* \[ ] WatchlistWidget.

Paper/demo:

* \[ ] PaperAccountWidget;
* \[ ] EquityCurveWidget;
* \[ ] FillsWidget;
* \[ ] DemoOrdersWidget;
* \[ ] ReconciliationWidget.

Risk/model/portfolio:

* \[ ] RiskDecisionWidget;
* \[ ] AlertsWidget;
* \[ ] ActiveModelWidget;
* \[ ] ModelHealthWidget;
* \[ ] PortfolioAllocationWidget.

Operator:

* \[ ] EvidenceManifestWidget;
* \[ ] SupportBundleWidget;
* \[ ] OperatorQualityGateWidget;
* \[ ] PerformanceBudgetWidget.

Acceptatiecriteria:

* \[ ] Widgets render from API DTOs.
* \[ ] Widgets handle loading/error/empty.
* \[ ] Widgets enforce safe modes.
* \[ ] Widgets can export local report if supported.
* \[ ] Frontend tests cover core widgets.

\---

## 12\. Fase 9 - Synchronized Charts

Nieuwe frontend/backend support:

* \[ ] shared time range;
* \[ ] crosshair sync;
* \[ ] zoom sync;
* \[ ] symbol sync optional;
* \[ ] session sync;
* \[ ] pause live updates;
* \[ ] replay mode scrubber;
* \[ ] compare current vs previous session;
* \[ ] overlay fills/signals/risk blocks;
* \[ ] chart annotations.

Backend:

```text
src/binance\_spot\_bot/dashboard\_v2/chart\_sync.py
```

Acceptatiecriteria:

* \[ ] Multiple charts can share time range.
* \[ ] Pausing live update works.
* \[ ] Fills/signals overlay on candle chart.
* \[ ] Session compare works with fixture sessions.
* \[ ] Performance budget passes.

\---

## 13\. Fase 10 - Watchlists \& Symbol Groups

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/watchlists.py
```

Watchlist fields:

* \[ ] watchlist\_id;
* \[ ] name;
* \[ ] symbols;
* \[ ] default\_interval;
* \[ ] source preference;
* \[ ] notes;
* \[ ] tags;
* \[ ] created\_at\_ms;
* \[ ] updated\_at\_ms.

Features:

* \[ ] create watchlist;
* \[ ] edit watchlist;
* \[ ] delete watchlist with confirm;
* \[ ] import/export watchlist;
* \[ ] select active symbol from watchlist;
* \[ ] quick switch symbol;
* \[ ] favorite symbols;
* \[ ] validate symbol format;
* \[ ] no live dependency.

Acceptatiecriteria:

* \[ ] Watchlists are local-only.
* \[ ] Invalid symbols rejected.
* \[ ] Delete requires confirm.
* \[ ] Frontend quick switch works.
* \[ ] Tests cover store/validation.

\---

## 14\. Fase 11 - Local Operator Preferences

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/operator\_preferences.py
```

Preferences:

* \[ ] default workspace;
* \[ ] default mode;
* \[ ] default source;
* \[ ] default symbol;
* \[ ] default interval;
* \[ ] chart point limits;
* \[ ] theme:

  * system;
  * light;
  * dark.
* \[ ] compact mode;
* \[ ] advanced panels visible;
* \[ ] notification preferences;
* \[ ] data retention for local UI metrics;
* \[ ] disable local UX metrics.

Rules:

* \[ ] No secrets.
* \[ ] No live mode.
* \[ ] Preferences import validates.
* \[ ] Reset to safe defaults.

Acceptatiecriteria:

* \[ ] Preferences saved locally.
* \[ ] Preferences cannot set live mode.
* \[ ] Reset works.
* \[ ] Import/export redacted.
* \[ ] Tests cover invalid values.

\---

## 15\. Fase 12 - Advanced Analytics Panels

New analytics:

* \[ ] session PnL distribution;
* \[ ] equity drawdown;
* \[ ] fill quality summary;
* \[ ] risk block heatmap;
* \[ ] signal confidence trend;
* \[ ] data quality warnings trend;
* \[ ] market data latency/reconnects;
* \[ ] demo pilot counters;
* \[ ] model status summary;
* \[ ] portfolio exposure summary;
* \[ ] operator evidence status;
* \[ ] support bundle health.

Backend module:

```text
src/binance\_spot\_bot/dashboard\_v2/advanced\_analytics.py
```

Acceptatiecriteria:

* \[ ] Analytics use local data only.
* \[ ] Missing data gives empty-state explanation.
* \[ ] Metrics are deterministic.
* \[ ] Reports are Markdown + JSON.
* \[ ] Tests use fixture sessions/snapshots.

\---

## 16\. Fase 13 - Workspace Import/Export

Features:

* \[ ] export workspace as JSON.
* \[ ] export workspace as Markdown summary.
* \[ ] import workspace from JSON.
* \[ ] import preview before apply.
* \[ ] diff current vs imported workspace.
* \[ ] block unknown widget types.
* \[ ] block unsafe actions.
* \[ ] block live mode.
* \[ ] redact secret-like values.
* \[ ] hash manifest.

Acceptatiecriteria:

* \[ ] Import preview works.
* \[ ] Unsafe import blocked.
* \[ ] Unknown widget blocked or mapped to placeholder.
* \[ ] Export is secret-free.
* \[ ] Tests cover malicious layout fixture.

\---

## 17\. Fase 14 - Workspace Versioning \& Migration

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/workspace\_migrations.py
```

Features:

* \[ ] workspace schema version.
* \[ ] migration registry.
* \[ ] migrate old layout to new schema.
* \[ ] backup before migration.
* \[ ] migration dry-run.
* \[ ] migration report.
* \[ ] rollback to previous workspace version.
* \[ ] incompatible layout warning.

Acceptatiecriteria:

* \[ ] Migration dry-run works.
* \[ ] Backup created before migration.
* \[ ] Invalid migration blocks apply.
* \[ ] Reports secret-free.
* \[ ] Tests cover v1→v2 fixture.

\---

## 18\. Fase 15 - Workspace Performance Budgets

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/workspace\_performance.py
```

Budgets:

* \[ ] max widgets per workspace;
* \[ ] max chart widgets;
* \[ ] max event subscriptions;
* \[ ] max total payload bytes per tick;
* \[ ] max render duration warning;
* \[ ] max saved workspaces;
* \[ ] max import file size;
* \[ ] max query time;
* \[ ] max local store size.

Acceptatiecriteria:

* \[ ] Too many widgets gives warning/block.
* \[ ] Heavy workspace can be profiled.
* \[ ] Budget report explains expensive widgets.
* \[ ] Browser smoke uses standard workspace.
* \[ ] Tests cover budget pass/fail.

\---

## 19\. Fase 16 - Workspace Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/workspace\_evidence\_bundle.py
```

Bundle bevat:

* \[ ] safety contract;
* \[ ] workspace schema validation;
* \[ ] widget registry validation;
* \[ ] workspace store manifest;
* \[ ] preset validation;
* \[ ] analytics query report;
* \[ ] API route smoke;
* \[ ] workspace browser smoke;
* \[ ] import/export validation;
* \[ ] workspace migration report;
* \[ ] performance budget report;
* \[ ] operator preferences report;
* \[ ] no-live proof;
* \[ ] redaction proof;
* \[ ] hashes.

Output:

```text
data/dashboard-v2/workspaces/evidence/<run\_id>/
  workspace\_evidence\_manifest.json
  workspace\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle links to V2-only release evidence.
* \[ ] Dashboard can download bundle.

\---

## 20\. Fase 17 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli dashboard-v2-workspaces --json
python -m binance\_spot\_bot.cli dashboard-v2-workspace-validate --workspace <id> --json
python -m binance\_spot\_bot.cli dashboard-v2-workspace-create --preset operator\_overview --name "My Workspace"
python -m binance\_spot\_bot.cli dashboard-v2-workspace-clone --workspace <id>
python -m binance\_spot\_bot.cli dashboard-v2-workspace-export --workspace <id>
python -m binance\_spot\_bot.cli dashboard-v2-workspace-import --path workspace.json --dry-run
python -m binance\_spot\_bot.cli dashboard-v2-widget-registry --json
python -m binance\_spot\_bot.cli dashboard-v2-workspace-presets --json
python -m binance\_spot\_bot.cli dashboard-v2-watchlists --json
python -m binance\_spot\_bot.cli dashboard-v2-watchlist-create --name "Majors" --symbols BTCUSDT,ETHUSDT,BNBUSDT
python -m binance\_spot\_bot.cli dashboard-v2-operator-preferences --json
python -m binance\_spot\_bot.cli dashboard-v2-analytics-query --scope runtime\_snapshot --json
python -m binance\_spot\_bot.cli dashboard-v2-workspace-performance --workspace <id> --json
python -m binance\_spot\_bot.cli dashboard-v2-workspace-evidence-export --workspace <id>
```

Acceptatiecriteria:

* \[ ] Commands werken offline.
* \[ ] Commands ondersteunen JSON waar relevant.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Commands bevatten no-live statement.
* \[ ] Reports zijn secret-free.

\---

## 21\. Fase 18 - Dashboard UI Integration

Nieuwe Dashboard V2 pages:

```text
/workspaces
/workspaces/:id
/workspaces/new
/workspaces/import
/watchlists
/preferences
/analytics
```

UX features:

* \[ ] workspace picker in header;
* \[ ] save layout button;
* \[ ] edit mode toggle;
* \[ ] widget picker drawer;
* \[ ] import/export menu;
* \[ ] preferences panel;
* \[ ] watchlist sidebar;
* \[ ] no-live banner locked;
* \[ ] stop button locked in operator mode;
* \[ ] safe reset button.

Acceptatiecriteria:

* \[ ] Workspace picker works.
* \[ ] Edit mode works.
* \[ ] No-live banner cannot be removed.
* \[ ] Preferences persist.
* \[ ] Browser smoke covers workspace create/edit/save.

\---

## 22\. Fase 19 - Operator/UAT Integration

Roadmap 102:

* \[ ] Operator manual krijgt workspace customization guide.
* \[ ] CLI cookbook krijgt workspace commands.
* \[ ] Troubleshooting krijgt layout import/export issues.
* \[ ] Support guide krijgt workspace evidence uitleg.

Roadmap 103:

* \[ ] UAT scenario: create workspace from preset.
* \[ ] UAT scenario: add/remove widget safely.
* \[ ] UAT scenario: import/export workspace.
* \[ ] UAT scenario: watchlist quick switch.
* \[ ] UAT scenario: no-live banner cannot be hidden.
* \[ ] UAT scorecard includes workspace usability.

Acceptatiecriteria:

* \[ ] UAT scenarios pass.
* \[ ] Docs link valid.
* \[ ] No-live proof included.
* \[ ] UAT feedback can create workspace backlog items.
* \[ ] Browser smoke and UAT evidence linked.

\---

## 23\. Fase 20 - Release/Knowledge/Test/Performance Integration

Roadmap 089:

* \[ ] Release notes include workspace/customization.
* \[ ] Version manifest includes workspace schema version.
* \[ ] Migration notes include workspace migration.

Roadmap 091:

* \[ ] Knowledge graph maps widget registry to API routes and frontend components.
* \[ ] Impact analysis detects widget/schema changes.

Roadmap 092:

* \[ ] Test selector chooses workspace tests for schema/widget/frontend changes.
* \[ ] Layout migration changes select migration tests.
* \[ ] Frontend workspace changes select browser smoke.

Roadmap 093:

* \[ ] Workspace performance budgets tracked.
* \[ ] Heavy workspace warnings become findings.
* \[ ] Chart/render metrics tied to workspace id.

Acceptatiecriteria:

* \[ ] Release evidence includes workspace evidence.
* \[ ] Knowledge graph updated.
* \[ ] Test selection works.
* \[ ] Performance reports include workspace budgets.
* \[ ] No-live proof preserved.

\---

## 24\. Fase 21 - Scheduled Workspace Reports

Uitbreiding op local scheduled reports:

Scheduled jobs:

* \[ ] weekly workspace validation;
* \[ ] weekly widget registry validation;
* \[ ] weekly workspace performance report;
* \[ ] weekly preferences sanity check;
* \[ ] weekly watchlist validation;
* \[ ] monthly workspace evidence export;
* \[ ] post-release workspace migration dry-run;
* \[ ] post-dashboard change workspace smoke.

Metrics:

* \[ ] workspace count;
* \[ ] invalid workspace count;
* \[ ] heavy workspace count;
* \[ ] widget usage counts;
* \[ ] watchlist count;
* \[ ] import/export failures;
* \[ ] workspace smoke pass/fail;
* \[ ] no-live widget lock pass/fail.

Acceptatiecriteria:

* \[ ] Reports are local-only.
* \[ ] Reports are secret-free.
* \[ ] Dashboard can show reports.
* \[ ] No-live proof included.
* \[ ] No live trading.

\---

## 25\. Tests

### Unit tests

* \[ ] `tests/test\_dashboard\_v2\_customization\_safety\_contract.py`
* \[ ] `tests/test\_dashboard\_v2\_workspace\_schema.py`
* \[ ] `tests/test\_dashboard\_v2\_widget\_registry.py`
* \[ ] `tests/test\_dashboard\_v2\_workspace\_store.py`
* \[ ] `tests/test\_dashboard\_v2\_workspace\_presets.py`
* \[ ] `tests/test\_dashboard\_v2\_analytics\_query.py`
* \[ ] `tests/test\_dashboard\_v2\_workspace\_api.py`
* \[ ] `tests/test\_dashboard\_v2\_chart\_sync.py`
* \[ ] `tests/test\_dashboard\_v2\_watchlists.py`
* \[ ] `tests/test\_dashboard\_v2\_operator\_preferences.py`
* \[ ] `tests/test\_dashboard\_v2\_advanced\_analytics.py`
* \[ ] `tests/test\_dashboard\_v2\_workspace\_import\_export.py`
* \[ ] `tests/test\_dashboard\_v2\_workspace\_migrations.py`
* \[ ] `tests/test\_dashboard\_v2\_workspace\_performance.py`
* \[ ] `tests/test\_dashboard\_v2\_workspace\_evidence\_bundle.py`

### Frontend tests

* \[ ] workspace grid renders.
* \[ ] widget picker works.
* \[ ] safety widgets locked.
* \[ ] panel resize/move.
* \[ ] layout save.
* \[ ] workspace import preview.
* \[ ] watchlist quick switch.
* \[ ] preferences panel.
* \[ ] chart sync.
* \[ ] no-live banner cannot be removed.

### Browser smoke

* \[ ] `/workspaces` loads.
* \[ ] create workspace from preset.
* \[ ] add widget.
* \[ ] remove non-safety widget.
* \[ ] attempt remove no-live widget fails.
* \[ ] save workspace.
* \[ ] export workspace.
* \[ ] watchlist page loads.
* \[ ] preferences page loads.
* \[ ] no live controls visible.

### Safety tests

* \[ ] Live mode blocked in workspace.
* \[ ] Live widget/action blocked.
* \[ ] Script injection in layout import blocked.
* \[ ] Secret-like values redacted from workspace export.
* \[ ] No-live banner locked.
* \[ ] Stop button locked in operator mode.
* \[ ] Reports/evidence secret-free.
* \[ ] Check-all safe env preserved.

\---

## 26\. Docs

Nieuwe docs:

```text
docs/dashboard-v2/customization-safety-contract.md
docs/dashboard-v2/workspace-schema.md
docs/dashboard-v2/widget-registry.md
docs/dashboard-v2/workspace-store.md
docs/dashboard-v2/workspace-presets.md
docs/dashboard-v2/analytics-query-layer.md
docs/dashboard-v2/workspace-api.md
docs/dashboard-v2/workspace-grid.md
docs/dashboard-v2/widget-library.md
docs/dashboard-v2/synchronized-charts.md
docs/dashboard-v2/watchlists.md
docs/dashboard-v2/operator-preferences.md
docs/dashboard-v2/advanced-analytics-panels.md
docs/dashboard-v2/workspace-import-export.md
docs/dashboard-v2/workspace-migrations.md
docs/dashboard-v2/workspace-performance-budgets.md
docs/dashboard-v2/workspace-evidence-bundle.md
```

README updates:

* \[ ] Dashboard V2 workspaces overview.
* \[ ] How to create workspace.
* \[ ] How to use presets.
* \[ ] How to import/export.
* \[ ] How to reset preferences.
* \[ ] No-live statement.

Operator docs updates:

* \[ ] Workspace guide.
* \[ ] Watchlist guide.
* \[ ] Widget guide.
* \[ ] Troubleshooting layout import.
* \[ ] Evidence export guide.

\---

## 27\. Codex bouwvolgorde

### PR 1 - Customization Safety Contract + Workspace Schema

* \[ ] `docs/dashboard-v2-customization-safety-contract.md`
* \[ ] `dashboard\_v2/workspace\_schema.py`
* \[ ] validation tests.
* \[ ] no-live lock tests.

### PR 2 - Widget Registry

* \[ ] `dashboard\_v2/widget\_registry.py`
* \[ ] core widget definitions.
* \[ ] safe widget tests.

### PR 3 - Workspace Store + Presets

* \[ ] `workspace\_store.py`
* \[ ] `workspace\_presets.py`
* \[ ] temp-dir tests.
* \[ ] preset validation.

### PR 4 - Analytics Query Layer + API

* \[ ] `analytics\_query.py`
* \[ ] API routes.
* \[ ] filter/downsampling/payload tests.

### PR 5 - Frontend Workspace Grid

* \[ ] workspace frontend components.
* \[ ] widget picker.
* \[ ] edit/save flow.
* \[ ] frontend tests.

### PR 6 - Core Widgets

* \[ ] safety/runtime/market/paper widgets.
* \[ ] loading/error/empty states.
* \[ ] widget tests.

### PR 7 - Synchronized Charts + Watchlists

* \[ ] `chart\_sync.py`
* \[ ] `watchlists.py`
* \[ ] chart sync frontend.
* \[ ] tests.

### PR 8 - Preferences + Advanced Analytics

* \[ ] `operator\_preferences.py`
* \[ ] `advanced\_analytics.py`
* \[ ] frontend preferences/analytics page.
* \[ ] tests.

### PR 9 - Import/Export + Migrations + Performance

* \[ ] `workspace\_migrations.py`
* \[ ] `workspace\_performance.py`
* \[ ] import/export validation.
* \[ ] migration tests.

### PR 10 - Evidence, CLI, Browser Smoke, Docs \& Integrations

* \[ ] `workspace\_evidence\_bundle.py`
* \[ ] CLI commands.
* \[ ] browser smoke.
* \[ ] docs/operator/UAT/release/test/knowledge integration.

\---

## 28\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 110 PR 1: Dashboard V2 Customization Safety Contract + Workspace Schema.

Maak docs/dashboard-v2-customization-safety-contract.md.

Maak src/binance\_spot\_bot/dashboard\_v2/workspace\_schema.py met:
- DashboardWorkspace
- DashboardWorkspaceGrid
- DashboardWorkspacePanel
- DashboardWorkspaceWidget
- DashboardWorkspaceLayout
- DashboardWorkspaceMetadata
- DashboardWorkspaceValidationResult
- validate\_dashboard\_workspace(workspace: DashboardWorkspace)
- dashboard\_workspace\_to\_dict(...)
- load\_dashboard\_workspace(path: Path)
- write\_dashboard\_workspace(path: Path, workspace: DashboardWorkspace)

Workspace moet minimaal ondersteunen:
- workspace\_id
- name
- description
- version
- operator\_level
- mode\_scope
- grid columns
- panels
- widgets
- widget settings
- safety\_widgets\_locked=True
- live\_trading\_enabled=False
- no\_live\_statement

Panel moet minimaal ondersteunen:
- panel\_id
- title
- x/y/w/h
- widget\_id
- pinned
- collapsed
- refresh\_policy
- query\_scope

Widget moet minimaal ondersteunen:
- widget\_id
- widget\_type
- title
- settings
- locked
- safe\_modes
- data\_sources

Validatie moet blokkeren op:
- live mode in mode\_scope of safe\_modes
- live\_trading\_enabled=True
- safety\_widgets\_locked=False
- missing no\_live\_banner widget
- missing stop/runtime safety widget in operator mode
- duplicate panel\_id
- duplicate widget\_id
- panel referencing missing widget\_id
- negative or zero width/height
- unknown refresh\_policy
- secret-like values in settings unless redacted
- script/html injection in title/settings

Gebruik alleen stdlib.
Geen command execution.
Geen frontend execution.
Geen backend server starten.
Geen Streamlit wijzigen.
Geen GitHub API calls.
Geen signed endpoints.
Geen account/order endpoints.
Geen live trading.

Voeg tests toe voor:
- valid workspace
- live mode blocked
- safety widgets locked
- no-live banner required
- duplicate panel id blocked
- duplicate widget id blocked
- missing widget reference blocked
- invalid dimensions blocked
- script injection blocked
- JSON serialization
- secret-like values worden geredact
- live\_trading\_enabled=False
- no\_live\_statement aanwezig
```

Waarom eerst:

* Customization kan pas veilig als het workspace schema no-live, locked safety widgets en import/export-validatie afdwingt.
* Het is read-only en raakt runtime/trading/frontend niet.
* Het is klein genoeg voor Codex.
* No-live en secret-free gedrag kunnen meteen getest worden.
* Daarna kunnen widget registry, workspace store en frontend grid veilig op dit schema bouwen.

\---

## 29\. Definition of Done

Roadmap 110 is klaar als:

* \[ ] Dashboard V2 Customization Safety Contract bestaat.
* \[ ] Workspace Schema werkt.
* \[ ] Safe Widget Registry werkt.
* \[ ] Workspace Store werkt.
* \[ ] Workspace Presets werken.
* \[ ] Realtime Analytics Query Layer werkt.
* \[ ] Analytics API Endpoints werken.
* \[ ] Frontend Workspace Grid werkt.
* \[ ] Widget Library Frontend werkt.
* \[ ] Synchronized Charts werken.
* \[ ] Watchlists \& Symbol Groups werken.
* \[ ] Local Operator Preferences werken.
* \[ ] Advanced Analytics Panels werken.
* \[ ] Workspace Import/Export werkt.
* \[ ] Workspace Versioning \& Migration werkt.
* \[ ] Workspace Performance Budgets werken.
* \[ ] Workspace Evidence Bundle werkt.
* \[ ] CLI commands werken.
* \[ ] Dashboard UI integration werkt.
* \[ ] Operator/UAT integration werkt.
* \[ ] Release/Knowledge/Test/Performance integration werkt.
* \[ ] Scheduled Workspace Reports werken.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen no-live/safety widgets niet verborgen kunnen worden.
* \[ ] Tests bewijzen layout import/export secret-free is.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Dashboard V2 workspace mode is local-only.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 110 kan na uitvoering naar `Voltooid docs`.

\---

## 30\. Verwachte Roadmap 111 daarna

Als Roadmap 110 groen is:

```text
Roadmap 111 - Dashboard V2 Local Plugin-Less Extension Packs, Analytics Presets \& Operator Workspace Templates
```

Mogelijke inhoud:

* \[ ] extra veilige widget packs zonder arbitraire code;
* \[ ] analytics preset packs;
* \[ ] workspace templates per operator persona;
* \[ ] model ops workspace pack;
* \[ ] portfolio workspace pack;
* \[ ] support/evidence workspace pack;
* \[ ] no-live template validation;
* \[ ] still no live trading.

```

Als Roadmap 110 performanceproblemen vindt:

```text
Roadmap 111 - Dashboard V2 Workspace Performance Burn-Down, Chart Virtualization \& Large Snapshot Optimization
```

Mogelijke inhoud:

* \[ ] heavy workspace bottlenecks oplossen;
* \[ ] chart virtualization;
* \[ ] query cache;
* \[ ] payload diffing;
* \[ ] frontend render budget hardening;
* \[ ] still no live trading.

```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Advanced realtime analytics layouts and operator customization.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.

