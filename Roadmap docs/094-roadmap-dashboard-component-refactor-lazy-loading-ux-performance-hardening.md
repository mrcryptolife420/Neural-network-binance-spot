# Roadmap 094 - Dashboard Component Refactor, Lazy Loading \& UX Performance Hardening

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/094-roadmap-dashboard-component-refactor-lazy-loading-ux-performance-hardening.md
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

Doel: Roadmap 093 maakt performance profiling, bottleneck analysis en resource budgeting mogelijk. Roadmap 094 past die inzichten toe op de grootste zichtbare onderhouds- en performancezone: het Streamlit dashboard. De roadmap splitst de brede `streamlit\_app.py` op in page modules en componenten, voegt lazy loading toe voor zware panels/imports, hardent UX rond demo trading en operator evidence, voorkomt Streamlit key regressies, beperkt chart/table payloads, en maakt dashboard smoke/browser smoke strenger.

Live trading blijft volledig buiten scope. Het dashboard blijft `LIVE TRADING DISABLED` en mag geen live mode, signed order endpoints of echte account/order acties beschikbaar maken.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 094`, `094-roadmap`, `Dashboard Component Refactor`, `Lazy Loading`, `UX Performance Hardening` en `dashboard performance`.
* \[x] Geen bestaande Roadmap 094 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 093 is lokaal aangemaakt als Performance Profiling, Runtime Bottleneck Analysis \& Resource Budgeting.

### Codebasecontrole

Breed bekeken met focus op dashboardarchitectuur:

* \[x] `src/binance\_spot\_bot/ui/streamlit\_app.py`
* \[x] `src/binance\_spot\_bot/ui/components.py`
* \[x] `src/binance\_spot\_bot/ui/page\_registry.py`
* \[x] `src/binance\_spot\_bot/ui/chart\_registry.py`
* \[x] `src/binance\_spot\_bot/ui/charts.py`
* \[x] `src/binance\_spot\_bot/ui/state.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] bestaande roadmaplijn tot en met Roadmap 093.

### Belangrijke bestaande basis

De codebase heeft nu:

* \[x] Een brede Streamlit-app met veel imports, sidebar controls, simple/advanced dashboard modes, 16 advanced tabs, demo trading, multi-symbol demo runtime, evidence export en demo pilot.
* \[x] Een bestaande page registry met 16 pages en no-live validatie via `live\_trading\_enabled=False`.
* \[x] Een component wrapper `render\_plotly\_chart(...)` die stabiele niet-lege Streamlit keys afdwingt.
* \[x] Een chart registry met vaste chart keys voor overview en demo pilot charts.
* \[x] Chart helpers in `ui/charts.py`, maar met vaste kleuren/layouts en zware figuren zoals candlestick/equity/multi-symbol/runner charts.
* \[x] `ui/state.py` maakt runtime aan met `live\_trading\_enabled=False`.
* \[x] `check\_all.py` draait al dashboard import en no-live UI checks met `LIVE\_TRADING\_ENABLED=false` en `KILL\_SWITCH=true`.
* \[x] Roadmap 093 plant profiling voor dashboard import/render/panel/chart timing.

### Belangrijkste gat na Roadmap 093

Na Roadmap 093 kun je meten welke dashboarddelen traag of zwaar zijn. Wat dan nog mist:

* \[ ] `streamlit\_app.py` is nog te breed en moeilijk gericht te testen.
* \[ ] Dashboard pages zijn nog niet opgesplitst in modules.
* \[ ] Heavy imports worden nog bij dashboardboot geladen.
* \[ ] Simple demo dashboard en advanced dashboard delen nog veel directe logica.
* \[ ] Page registry bevat alleen titel/key, niet module/render/smoke/budget metadata.
* \[ ] Chart registry bevat nog maar een klein deel van alle mogelijke chart/widget keys.
* \[ ] Table/chart payload limits zijn nog niet centraal afgedwongen.
* \[ ] Debug expanders kunnen zware JSON payloads tonen zonder size guard.
* \[ ] Dashboard action buttons/forms hebben nog geen centraal key/permission/action policy.
* \[ ] Browser smoke is nog niet page-budget aware.
* \[ ] Dashboard UX heeft nog geen consistente status cards, loading states en error boundaries per panel.
* \[ ] Performance budget uit Roadmap 093 wordt nog niet toegepast op dashboard pages.

Roadmap 094 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 094

Maak het dashboard modulair, sneller en harder getest:

```text
streamlit\_app.py monolith
→ page modules
→ shared component system
→ lazy panel loading
→ key registry
→ payload limits
→ UX error boundaries
→ page performance budgets
→ dashboard smoke/browser smoke coverage
```

Na Roadmap 094 moet het dashboard:

* \[ ] sneller importeren;
* \[ ] minder zware imports bij boot uitvoeren;
* \[ ] per page/panel testbaar zijn;
* \[ ] stabiele widget/chart/table keys afdwingen;
* \[ ] grote chart/table/debug payloads begrenzen;
* \[ ] panel-level loading/error states hebben;
* \[ ] simple demo trading UX duidelijker maken;
* \[ ] advanced tabs overzichtelijker maken;
* \[ ] performance budgets per page hebben;
* \[ ] browser smoke per kritieke page ondersteunen;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe dashboardtechnologie.
* \[ ] Geen complete UI rewrite naar React/Vue.
* \[ ] Geen nieuwe runtime engine.
* \[ ] Geen nieuwe demo trading engine.
* \[ ] Geen nieuwe performance profiler; Roadmap 093 doet dat.
* \[ ] Geen nieuwe testselector; Roadmap 092 doet dat.
* \[ ] Geen nieuwe knowledge graph; Roadmap 091 doet dat.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen Binance account endpoints.
* \[ ] Geen echte order endpoints.
* \[ ] Geen automatische dashboardacties zonder operatorbevestiging.
* \[ ] Geen externe telemetry.

Wel doen:

* \[ ] bestaande Streamlit app modulair maken;
* \[ ] pages/panels opsplitsen;
* \[ ] imports lazy maken;
* \[ ] component wrappers uitbreiden;
* \[ ] chart/table/debug limits toevoegen;
* \[ ] page registry uitbreiden;
* \[ ] dashboard smoke uitbreiden;
* \[ ] UX states/guardrails toevoegen;
* \[ ] dashboard performance budgets toepassen;
* \[ ] alles local-only en no-live houden.

\---

## 3\. Fase 0 - Dashboard Refactor Safety Contract

Nieuwe doc:

```text
docs/dashboard-refactor-safety-contract.md
```

Regels:

* \[ ] Dashboard blijft local-only.
* \[ ] Dashboard toont `LIVE TRADING DISABLED`.
* \[ ] Geen live mode in `SELECTABLE\_MODES`.
* \[ ] Geen dashboard page mag `live\_trading\_enabled=True` registreren.
* \[ ] Geen signed order endpoint via dashboard.
* \[ ] Geen account endpoint via dashboard buiten bestaande demo/testnet-readiness guardrails.
* \[ ] Demo trading blijft expliciet armed/confirmed.
* \[ ] Page modules mogen runtime business logic niet dupliceren.
* \[ ] Componenten mogen geen secrets tonen.
* \[ ] Debug payloads worden begrensd en geredact.
* \[ ] Heavy actions hebben confirmation/disabled state.
* \[ ] Browser smoke blijft verplicht voor dashboardwijzigingen.
* \[ ] Performance budgets mogen UI waarschuwingen geven, geen trading acties starten.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen `live` niet selecteerbaar is.
* \[ ] Tests bewijzen page registry geen live page toelaat.
* \[ ] Tests bewijzen debug payloads redacted/limited zijn.
* \[ ] Dashboard toont `DASHBOARD REFACTOR - NO LIVE TRADING`.

\---

## 4\. Fase 1 - Dashboard Page Module Architecture

Doel: `streamlit\_app.py` terugbrengen tot bootstrap/router/controller.

Nieuwe map:

```text
src/binance\_spot\_bot/ui/pages/
```

Nieuwe modules:

* \[ ] `pages/overview.py`
* \[ ] `pages/simple\_demo.py`
* \[ ] `pages/demo\_spot\_trading.py`
* \[ ] `pages/credentials\_profile.py`
* \[ ] `pages/bot\_controls.py`
* \[ ] `pages/risk\_controls.py`
* \[ ] `pages/strategy\_model.py`
* \[ ] `pages/market\_data.py`
* \[ ] `pages/orders\_account.py`
* \[ ] `pages/sessions.py`
* \[ ] `pages/evaluation.py`
* \[ ] `pages/strategy\_lab.py`
* \[ ] `pages/research.py`
* \[ ] `pages/portfolio.py`
* \[ ] `pages/readiness.py`
* \[ ] `pages/logs\_security.py`
* \[ ] `pages/demo\_pilot.py`

Nieuwe structuren:

```text
src/binance\_spot\_bot/ui/app\_shell.py
src/binance\_spot\_bot/ui/routing.py
src/binance\_spot\_bot/ui/context.py
```

Dataclasses:

* \[ ] `DashboardContext`
* \[ ] `DashboardPageResult`
* \[ ] `DashboardActionResult`
* \[ ] `DashboardRenderState`

Acceptatiecriteria:

* \[ ] `streamlit\_app.py` bevat alleen parse args, app setup, context build, routing en rerun loop.
* \[ ] Elke page module heeft één publieke `render(context)` functie.
* \[ ] Pages dupliceren geen runtime creation logic.
* \[ ] Alle imports blijven compatibel.
* \[ ] Dashboard import smoke blijft groen.

\---

## 5\. Fase 2 - Page Registry V2

Uitbreiden:

```text
src/binance\_spot\_bot/ui/page\_registry.py
```

Nieuwe velden in `PageDefinition`:

* \[ ] key;
* \[ ] title;
* \[ ] module\_path;
* \[ ] render\_function;
* \[ ] category:

  * core;
  * demo;
  * trading\_demo;
  * operator;
  * analytics;
  * safety;
  * advanced.
* \[ ] simple\_mode\_visible;
* \[ ] advanced\_mode\_visible;
* \[ ] requires\_runtime;
* \[ ] requires\_credentials;
* \[ ] requires\_demo\_profile;
* \[ ] performance\_budget\_ms;
* \[ ] browser\_smoke\_required;
* \[ ] live\_trading\_enabled=False;
* \[ ] safety\_level:

  * low;
  * medium;
  * high;
  * critical.

Validaties:

* \[ ] unieke keys;
* \[ ] unieke titles;
* \[ ] module importable;
* \[ ] render function bestaat;
* \[ ] geen live page;
* \[ ] performance budget aanwezig voor critical pages;
* \[ ] browser smoke required voor demo/action pages.

Acceptatiecriteria:

* \[ ] Registry kan alle pages laden.
* \[ ] Registry kan selected pages/filter geven.
* \[ ] Registry valideert modules/render functions.
* \[ ] Registry faalt als `live\_trading\_enabled=True`.
* \[ ] Tests dekken duplicate, missing module en live page.

\---

## 6\. Fase 3 - Dashboard Context Builder

Nieuwe module:

```text
src/binance\_spot\_bot/ui/context.py
```

Doel: alle gedeelde dashboardstate bundelen zonder overal losse parameters.

Dataclasses:

* \[ ] `DashboardContext`
* \[ ] `DashboardSettingsContext`
* \[ ] `DashboardRuntimeContext`
* \[ ] `DashboardCredentialContext`
* \[ ] `DashboardProfileContext`
* \[ ] `DashboardSafetyContext`
* \[ ] `DashboardPerformanceContext`

Context bevat:

* \[ ] base\_settings;
* \[ ] runtime\_settings;
* \[ ] selected\_profile;
* \[ ] profile;
* \[ ] saved dashboard settings;
* \[ ] settings store;
* \[ ] credential manager;
* \[ ] runtime;
* \[ ] snapshot;
* \[ ] simple\_dashboard bool;
* \[ ] selected symbol/interval/source/scenario;
* \[ ] risk settings;
* \[ ] demo armed state;
* \[ ] runner status;
* \[ ] performance profiler optional;
* \[ ] no-live proof.

Acceptatiecriteria:

* \[ ] Pages krijgen context object in plaats van 20+ losse parameters.
* \[ ] Context is testbaar met fake runtime/snapshot.
* \[ ] Context bevat geen raw secrets.
* \[ ] Context geeft `live\_trading\_enabled=False` door.
* \[ ] Tests dekken simple/advanced context.

\---

## 7\. Fase 4 - Lazy Import \& Lazy Panel Loader

Nieuwe module:

```text
src/binance\_spot\_bot/ui/lazy.py
```

Doel: zware imports/panels pas laden wanneer page wordt geopend.

Functionaliteit:

* \[ ] `lazy\_import(module\_path)`
* \[ ] `lazy\_render(page\_definition, context)`
* \[ ] cache import result per session waar veilig;
* \[ ] lazy panel metadata;
* \[ ] loading spinner;
* \[ ] import error boundary;
* \[ ] fallback UI;
* \[ ] performance span integration from Roadmap 093.

Heavy candidates:

* \[ ] evaluation/backtest/report modules;
* \[ ] notebook export;
* \[ ] html reports;
* \[ ] experiment DB;
* \[ ] replay sandbox;
* \[ ] research panels;
* \[ ] strategy lab panels;
* \[ ] support bundle export panels;
* \[ ] dashboard evidence export panels;
* \[ ] charts for pages not open.

Acceptatiecriteria:

* \[ ] Dashboard boot imports minder heavy page-only modules.
* \[ ] Page render lazy-loadt module wanneer nodig.
* \[ ] Lazy import failures tonen veilige error card.
* \[ ] No-live checks blijven actief vóór lazy imports.
* \[ ] Tests gebruiken fake page modules.

\---

## 8\. Fase 5 - Component System V2

Uitbreiden:

```text
src/binance\_spot\_bot/ui/components.py
```

Nieuwe componenten:

* \[ ] `render\_status\_card`
* \[ ] `render\_safety\_banner`
* \[ ] `render\_action\_button`
* \[ ] `render\_confirmed\_action`
* \[ ] `render\_payload\_preview`
* \[ ] `render\_limited\_table`
* \[ ] `render\_limited\_json`
* \[ ] `render\_error\_boundary`
* \[ ] `render\_loading\_state`
* \[ ] `render\_empty\_state`
* \[ ] `render\_metric\_row`
* \[ ] `render\_copyable\_command`
* \[ ] `render\_evidence\_link`
* \[ ] `render\_download\_card`

Componentregels:

* \[ ] elke action button heeft stable key;
* \[ ] confirmed action vereist confirmation phrase waar nodig;
* \[ ] payload preview heeft size/row limits;
* \[ ] debug JSON wordt geredact/limited;
* \[ ] tables hebben max rows en download-optie;
* \[ ] charts moeten stable key hebben;
* \[ ] safety banners altijd no-live tonen op critical pages.

Acceptatiecriteria:

* \[ ] Oude componenten blijven backward compatible.
* \[ ] Nieuwe componenten zijn unit-testbaar zonder Streamlit runtime via payload builders waar mogelijk.
* \[ ] Stable key vereist voor actions/charts.
* \[ ] Large payloads worden niet volledig gerenderd.
* \[ ] Tests dekken key/limit/redaction gedrag.

\---

## 9\. Fase 6 - Widget \& Chart Key Registry V2

Uitbreiden:

```text
src/binance\_spot\_bot/ui/chart\_registry.py
```

Nieuwe module:

```text
src/binance\_spot\_bot/ui/widget\_registry.py
```

Doel: alle chart/form/button/table/debug keys centraal en uniek maken.

Te registreren:

* \[ ] chart keys;
* \[ ] button keys;
* \[ ] form keys;
* \[ ] input keys;
* \[ ] table keys;
* \[ ] debug expander keys;
* \[ ] download keys;
* \[ ] fragment keys;
* \[ ] action keys.

Validaties:

* \[ ] unieke keys;
* \[ ] key namespace per page;
* \[ ] geen lege key;
* \[ ] geen auto-generated plotly chart key;
* \[ ] key name follows convention:

  * `page.section.component.action`;
* \[ ] page registry link.

Acceptatiecriteria:

* \[ ] All known charts use registry keys.
* \[ ] Plotly charts zonder key blijven verboden.
* \[ ] Dashboard duplicate element regressie krijgt test.
* \[ ] Widget registry kan smoke test draaien.
* \[ ] Tests detecteren duplicate keys.

\---

## 10\. Fase 7 - Chart Payload \& Rendering Hardening

Uitbreiden:

```text
src/binance\_spot\_bot/ui/charts.py
```

Nieuwe module:

```text
src/binance\_spot\_bot/ui/chart\_limits.py
```

Doel: charts sneller en veiliger maken.

Limits:

* \[ ] max candle points visible;
* \[ ] max signal markers;
* \[ ] max fill markers;
* \[ ] max open order markers;
* \[ ] max reconciliation markers;
* \[ ] max runner telemetry points;
* \[ ] max bar categories;
* \[ ] max chart traces;
* \[ ] max chart payload bytes estimate.

Nieuwe helpers:

* \[ ] `trim\_candles\_for\_chart`
* \[ ] `trim\_points\_for\_chart`
* \[ ] `estimate\_chart\_payload`
* \[ ] `chart\_limit\_warning`
* \[ ] `safe\_chart\_figure`
* \[ ] `chart\_perf\_metadata`

Acceptatiecriteria:

* \[ ] Large snapshot charts worden begrensd.
* \[ ] Chart shows warning when trimmed.
* \[ ] Existing chart output blijft functioneel.
* \[ ] Chart functions krijgen performance metadata.
* \[ ] Tests dekken trimming en payload estimate.

\---

## 11\. Fase 8 - Table \& Debug Payload Hardening

Nieuwe module:

```text
src/binance\_spot\_bot/ui/payload\_limits.py
```

Doel: tables/debug expanders veilig en performant maken.

Limits:

* \[ ] max table rows default 100;
* \[ ] max table columns default 50;
* \[ ] max JSON depth;
* \[ ] max JSON string length;
* \[ ] max debug payload bytes;
* \[ ] max session list rows;
* \[ ] max audit tail rows;
* \[ ] max support bundle rows;
* \[ ] max evidence rows.

Functionaliteit:

* \[ ] payload redaction;
* \[ ] payload truncation;
* \[ ] row count warning;
* \[ ] download full artifact link where safe;
* \[ ] debug-only raw preview disabled by default;
* \[ ] secret scan before render.

Acceptatiecriteria:

* \[ ] `render\_debug` gebruikt payload limits.
* \[ ] `render\_table` gebruikt row limits.
* \[ ] Secrets worden niet getoond.
* \[ ] Large payloads crashen dashboard niet.
* \[ ] Tests dekken truncation/redaction.

\---

## 12\. Fase 9 - Simple Demo UX Hardening

Doel: de eenvoudige demo trading flow duidelijker, veiliger en sneller maken.

Nieuwe module:

```text
src/binance\_spot\_bot/ui/pages/simple\_demo.py
src/binance\_spot\_bot/ui/simple\_demo\_presenter.py
```

Verbeteringen:

* \[ ] Stepper:

  * 

    1. keys laden;
  * 

    2. verbinding testen;
  * 

    3. demo trading connecten;
  * 

    4. symbolen kiezen;
  * 

    5. start selected symbols;
  * 

    6. monitor/stop.
* \[ ] Status cards voor:

  * keys;
  * connection;
  * profile;
  * armed state;
  * symbols validation;
  * running runtimes;
  * live disabled.
* \[ ] Action buttons disabled met duidelijke reden.
* \[ ] Stop all en stop one symbol duidelijk gescheiden.
* \[ ] Per-symbol cards met status/equity/fills/open orders.
* \[ ] Error boundary rond multi-runtime sync.
* \[ ] Evidence export card.
* \[ ] Performance hint voor live fragment.

Acceptatiecriteria:

* \[ ] Simple demo page gebruikt presenter payloads.
* \[ ] UX toont next best action.
* \[ ] Buttons zijn disabled met reason.
* \[ ] Demo start blijft alleen mogelijk met demo profile en armed state.
* \[ ] Browser smoke dekt simple demo page.

\---

## 13\. Fase 10 - Advanced Dashboard Navigation Hardening

Doel: advanced tabs beter organiseren en sneller laden.

Verbeteringen:

* \[ ] Page category grouping.
* \[ ] Optional page search/filter.
* \[ ] Critical pages bovenaan:

  * Overview;
  * Demo Spot Trading;
  * Risk Controls;
  * Orders \& Account;
  * Logs \& Security.
* \[ ] Heavy pages lazy:

  * Evaluation;
  * Research;
  * Strategy Lab;
  * Reports/evidence-heavy pages.
* \[ ] Page metadata sidebar.
* \[ ] Page load warning if heavy.
* \[ ] Page performance budget badge.
* \[ ] Page safety level badge.

Acceptatiecriteria:

* \[ ] Advanced pages blijven bereikbaar.
* \[ ] Page registry bepaalt zichtbaarheid/order.
* \[ ] Heavy page is lazy-loaded.
* \[ ] Page performance badge werkt met Roadmap 093 data indien aanwezig.
* \[ ] Browser smoke dekt page registry routing.

\---

## 14\. Fase 11 - Dashboard Error Boundaries

Nieuwe module:

```text
src/binance\_spot\_bot/ui/error\_boundary.py
```

Doel: één page/panel mag niet het hele dashboard laten crashen.

Functionaliteit:

* \[ ] `render\_with\_boundary(page\_key, title, render\_fn)`
* \[ ] catch expected exceptions;
* \[ ] redacted error message;
* \[ ] troubleshooting card;
* \[ ] support bundle action suggestion;
* \[ ] copy diagnostics command;
* \[ ] evidence path if available;
* \[ ] optional re-raise in dev mode.

Acceptatiecriteria:

* \[ ] Page render exception toont error card.
* \[ ] Error card bevat geen secrets.
* \[ ] Error card stelt veilige diagnostics/support-bundle commands voor.
* \[ ] Critical no-live banner blijft zichtbaar.
* \[ ] Tests gebruiken failing fake page.

\---

## 15\. Fase 12 - Dashboard Action Policy

Nieuwe module:

```text
src/binance\_spot\_bot/ui/action\_policy.py
```

Doel: dashboardactions consistent beveiligen.

Action classes:

* \[ ] read\_only;
* \[ ] local\_artifact\_generation;
* \[ ] demo\_connect;
* \[ ] demo\_start;
* \[ ] demo\_stop;
* \[ ] export\_evidence;
* \[ ] run\_smoke;
* \[ ] support\_bundle;
* \[ ] destructive\_local\_preview;
* \[ ] forbidden.

Policy checks:

* \[ ] requires key;
* \[ ] requires confirmation phrase;
* \[ ] requires demo profile;
* \[ ] requires credentials;
* \[ ] requires armed state;
* \[ ] requires no-live proof;
* \[ ] disabled reason;
* \[ ] action audit payload.

Forbidden:

* \[ ] live mode;
* \[ ] signed real order;
* \[ ] real account endpoint;
* \[ ] arbitrary shell;
* \[ ] remote upload.

Acceptatiecriteria:

* \[ ] Dashboard action policy returns disabled reason.
* \[ ] Demo start action uses policy.
* \[ ] Evidence/support bundle actions use policy.
* \[ ] Forbidden actions cannot render active buttons.
* \[ ] Tests cover action classes.

\---

## 16\. Fase 13 - Dashboard State Slimming

Doel: `st.session\_state` overzichtelijker en kleiner maken.

Nieuwe module:

```text
src/binance\_spot\_bot/ui/session\_state.py
```

Functionaliteit:

* \[ ] typed keys;
* \[ ] default initialization;
* \[ ] session state size estimate;
* \[ ] cleanup stale keys;
* \[ ] per-page state namespaces;
* \[ ] multi-demo runtime state helper;
* \[ ] safe credential-state wrapper;
* \[ ] redacted state debug.

Acceptatiecriteria:

* \[ ] Session state init centralized.
* \[ ] Existing keys migrate safely.
* \[ ] State debug does not leak secrets.
* \[ ] Simple/advanced state namespaced.
* \[ ] Tests dekken default/migration/cleanup.

\---

## 17\. Fase 14 - Dashboard Performance Budget Integration

Uitbreiding op Roadmap 093:

* \[ ] page import budget;
* \[ ] page render budget;
* \[ ] chart build budget;
* \[ ] table render budget;
* \[ ] debug payload budget;
* \[ ] simple demo fragment budget;
* \[ ] demo pilot panel budget;
* \[ ] dashboard boot budget.

Nieuwe module:

```text
src/binance\_spot\_bot/ui/performance\_budget.py
```

Acceptatiecriteria:

* \[ ] Page registry bevat performance budgets.
* \[ ] Performance profiler kan per page budget evalueren.
* \[ ] Dashboard toont budget warning.
* \[ ] Browser smoke kan budget report exporteren.
* \[ ] Budget failure blokkeert geen demo stop/safety actions.

\---

## 18\. Fase 15 - Dashboard Smoke V2

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_smoke\_v2.py
```

Checks:

* \[ ] streamlit app import;
* \[ ] page registry validation;
* \[ ] page modules import;
* \[ ] render payload builders import;
* \[ ] widget/chart registry validation;
* \[ ] no live selectable modes;
* \[ ] action policy validation;
* \[ ] payload limit validation;
* \[ ] chart key validation;
* \[ ] smoke selected pages;
* \[ ] performance budget smoke where available.

Commands:

```powershell
python -m binance\_spot\_bot.cli dashboard-smoke-v2
python -m binance\_spot\_bot.cli dashboard-page-smoke --page simple\_demo
python -m binance\_spot\_bot.cli dashboard-page-smoke --page demo\_pilot
python -m binance\_spot\_bot.cli dashboard-widget-key-check
```

Acceptatiecriteria:

* \[ ] Smoke V2 works offline.
* \[ ] Smoke V2 fails on duplicate keys.
* \[ ] Smoke V2 fails on live page.
* \[ ] Smoke V2 includes page module import.
* \[ ] Existing `dashboard-smoke` remains working.

\---

## 19\. Fase 16 - Browser Smoke Page Matrix

Doel: browser smoke gerichter en sterker maken.

Nieuwe config:

```text
config/dashboard-browser-smoke-pages.json
```

Page matrix:

* \[ ] simple demo page;
* \[ ] overview;
* \[ ] demo spot trading;
* \[ ] risk controls;
* \[ ] orders/account;
* \[ ] logs/security;
* \[ ] demo pilot;
* \[ ] one heavy/lazy page sample.

Per page:

* \[ ] URL/query;
* \[ ] expected title;
* \[ ] expected no-live text;
* \[ ] expected safety badge;
* \[ ] max render time;
* \[ ] screenshot optional;
* \[ ] critical selectors/text.

Acceptatiecriteria:

* \[ ] Browser smoke can run selected page matrix.
* \[ ] No-live text verified on every page.
* \[ ] Simple demo page has smoke coverage.
* \[ ] Lazy page smoke validates loading/error boundary.
* \[ ] Reports are secret-free.

\---

## 20\. Fase 17 - Dashboard UX Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_ux\_evidence.py
```

Bundle bevat:

* \[ ] page registry report;
* \[ ] widget key report;
* \[ ] chart key report;
* \[ ] payload limit report;
* \[ ] action policy report;
* \[ ] dashboard smoke v2 report;
* \[ ] browser smoke matrix report;
* \[ ] performance budget report;
* \[ ] no-live proof;
* \[ ] screenshots optional;
* \[ ] hashes.

Output:

```text
data/dashboard/evidence/<run\_id>/
  dashboard\_ux\_evidence\_manifest.json
  dashboard\_ux\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle links to Roadmap 093 performance evidence.
* \[ ] Bundle links to Roadmap 092 test evidence.

\---

## 21\. Fase 18 - Dashboard Docs \& Component Guide

Nieuwe docs:

```text
docs/dashboard/
```

Docs:

* \[ ] `dashboard-architecture.md`
* \[ ] `dashboard-page-modules.md`
* \[ ] `dashboard-component-system.md`
* \[ ] `dashboard-widget-key-registry.md`
* \[ ] `dashboard-lazy-loading.md`
* \[ ] `dashboard-payload-limits.md`
* \[ ] `dashboard-action-policy.md`
* \[ ] `dashboard-smoke-v2.md`
* \[ ] `dashboard-browser-smoke-matrix.md`
* \[ ] `dashboard-performance-budgets.md`
* \[ ] `simple-demo-ux-flow.md`

Acceptatiecriteria:

* \[ ] Docs leggen uit hoe nieuwe page toegevoegd wordt.
* \[ ] Docs leggen stable key regels uit.
* \[ ] Docs leggen lazy loading regels uit.
* \[ ] Docs leggen no-live/safety regels uit.
* \[ ] README linkt naar dashboard docs.

\---

## 22\. Fase 19 - Roadmap/Knowledge/Test/Release Integraties

### Roadmap 091 integratie

* \[ ] Repository knowledge graph detecteert page modules.
* \[ ] Dashboard surface map leest Page Registry V2.
* \[ ] Impact analysis weet welke page geraakt is.
* \[ ] Ownership map markeert dashboard components.

### Roadmap 092 integratie

* \[ ] Test selector kiest dashboard profile bij page/component changes.
* \[ ] Critical dashboard actions vereisen browser smoke.
* \[ ] Dashboard smoke V2 evidence voedt test evidence.

### Roadmap 093 integratie

* \[ ] Performance profiler meet page/panel render.
* \[ ] Dashboard budgets voeden performance reports.
* \[ ] Refactor recommendations gebruiken page timings.

### Roadmap 090 integratie

* \[ ] Codex task packs voor dashboard PR bevatten widget-key/smoke/browser-smoke requirements.
* \[ ] Completion gate vereist dashboard UX evidence.

### Roadmap 089 integratie

* \[ ] Release notes krijgen dashboard changed pages.
* \[ ] Release quality gate checkt dashboard smoke V2.

Acceptatiecriteria:

* \[ ] Dashboard changes krijgen automatisch juiste tests.
* \[ ] Release evidence bevat dashboard UX evidence bij UI changes.
* \[ ] Knowledge graph kan page modules tonen.
* \[ ] Completion gate kan widget key evidence lezen.
* \[ ] No-live proof preserved.

\---

## 23\. Fase 20 - Tests

### Unit tests

* \[ ] `tests/test\_dashboard\_refactor\_safety\_contract.py`
* \[ ] `tests/test\_page\_registry\_v2.py`
* \[ ] `tests/test\_dashboard\_context.py`
* \[ ] `tests/test\_ui\_lazy.py`
* \[ ] `tests/test\_ui\_components\_v2.py`
* \[ ] `tests/test\_widget\_registry.py`
* \[ ] `tests/test\_chart\_limits.py`
* \[ ] `tests/test\_payload\_limits.py`
* \[ ] `tests/test\_simple\_demo\_presenter.py`
* \[ ] `tests/test\_ui\_error\_boundary.py`
* \[ ] `tests/test\_ui\_action\_policy.py`
* \[ ] `tests/test\_ui\_session\_state.py`
* \[ ] `tests/test\_dashboard\_performance\_budget.py`
* \[ ] `tests/test\_dashboard\_smoke\_v2.py`
* \[ ] `tests/test\_dashboard\_ux\_evidence.py`

### Integration tests

* \[ ] Import `streamlit\_app.py`.
* \[ ] Validate Page Registry V2.
* \[ ] Import every page module.
* \[ ] Render fake page with fake context.
* \[ ] Lazy import fake heavy page.
* \[ ] Duplicate widget/chart key detection.
* \[ ] Simple demo presenter with missing keys.
* \[ ] Simple demo presenter with ready state.
* \[ ] Action policy blocks forbidden action.
* \[ ] Payload limits truncate large JSON.
* \[ ] Chart limits trim large candle list.
* \[ ] Dashboard smoke V2 full.
* \[ ] Browser smoke matrix subset.

### Safety tests

* \[ ] `live` not in selectable modes.
* \[ ] Page registry rejects live page.
* \[ ] Action policy rejects real order/account/live action.
* \[ ] Debug payload redacts secret-like values.
* \[ ] Dashboard import does not require API keys.
* \[ ] Demo start still requires demo profile/armed state.
* \[ ] Browser smoke verifies no-live text.
* \[ ] Reports/evidence are secret-free.
* \[ ] No-live proof remains true.

\---

## 24\. CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli dashboard-smoke-v2
python -m binance\_spot\_bot.cli dashboard-page-smoke --page simple\_demo
python -m binance\_spot\_bot.cli dashboard-widget-key-check
python -m binance\_spot\_bot.cli dashboard-page-registry --json
python -m binance\_spot\_bot.cli dashboard-payload-limit-check
python -m binance\_spot\_bot.cli dashboard-action-policy-check
python -m binance\_spot\_bot.cli dashboard-ux-evidence-export
```

Acceptatiecriteria:

* \[ ] Commands werken offline.
* \[ ] Commands ondersteunen JSON output.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account/order endpoints.
* \[ ] Reports zijn secret-free.

\---

## 25\. Codex bouwvolgorde

### PR 1 - Safety Contract + Page Registry V2

* \[ ] `docs/dashboard-refactor-safety-contract.md`
* \[ ] `ui/page\_registry.py` uitbreiden
* \[ ] validation tests
* \[ ] no-live tests.

### PR 2 - Dashboard Context + App Shell

* \[ ] `ui/context.py`
* \[ ] `ui/app\_shell.py`
* \[ ] context builder
* \[ ] tests.

### PR 3 - Page Module Extraction Foundation

* \[ ] `ui/pages/overview.py`
* \[ ] `ui/pages/simple\_demo.py`
* \[ ] `ui/pages/demo\_pilot.py`
* \[ ] keep old render functions as compatibility wrappers where needed
* \[ ] import tests.

### PR 4 - Lazy Loading

* \[ ] `ui/lazy.py`
* \[ ] route via registry
* \[ ] lazy error boundary
* \[ ] tests.

### PR 5 - Components V2

* \[ ] `ui/components.py` uitbreiden
* \[ ] status cards/action buttons/limited JSON/table
* \[ ] tests.

### PR 6 - Widget/Chart Registry V2

* \[ ] `ui/widget\_registry.py`
* \[ ] expand `chart\_registry.py`
* \[ ] duplicate key tests
* \[ ] migrate known charts.

### PR 7 - Chart/Table/Payload Limits

* \[ ] `ui/chart\_limits.py`
* \[ ] `ui/payload\_limits.py`
* \[ ] integrate in components/charts
* \[ ] tests.

### PR 8 - Simple Demo UX Hardening

* \[ ] `ui/simple\_demo\_presenter.py`
* \[ ] improved stepper/status cards
* \[ ] action disabled reasons
* \[ ] tests.

### PR 9 - Smoke V2 + UX Evidence

* \[ ] `dashboard\_smoke\_v2.py`
* \[ ] CLI commands
* \[ ] `dashboard\_ux\_evidence.py`
* \[ ] tests.

### PR 10 - Dashboard Performance + Browser Smoke + Docs

* \[ ] dashboard performance budget integration
* \[ ] browser smoke matrix
* \[ ] docs/dashboard
* \[ ] full browser smoke.

\---

## 26\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 094 PR 1: Dashboard Refactor Safety Contract + Page Registry V2.

Maak docs/dashboard-refactor-safety-contract.md.

Breid src/binance\_spot\_bot/ui/page\_registry.py uit:
- PageDefinition met:
  - key
  - title
  - module\_path
  - render\_function
  - category
  - simple\_mode\_visible
  - advanced\_mode\_visible
  - requires\_runtime
  - requires\_credentials
  - requires\_demo\_profile
  - performance\_budget\_ms
  - browser\_smoke\_required
  - live\_trading\_enabled=False
  - safety\_level
- behoud page\_titles()
- voeg page\_keys()
- voeg get\_page(key)
- voeg visible\_pages(simple\_mode: bool)
- breid validate\_page\_registry() uit met:
  - duplicate key/title detection
  - module path non-empty
  - render function non-empty
  - live page forbidden
  - critical/demo pages require browser\_smoke\_required
  - performance budget positive for high/critical pages

Werk bestaande PAGES bij voor alle 16 huidige pages:
- overview
- demo\_spot\_trading
- credentials\_profile
- bot\_controls
- risk\_controls
- strategy\_model
- market\_data
- orders\_account
- sessions
- evaluation
- strategy\_lab
- research
- portfolio
- readiness
- logs\_security
- demo\_pilot

Voeg tests toe voor:
- page\_titles backward compatible
- unique keys/titles
- get\_page
- visible\_pages simple/advanced
- reject live\_trading\_enabled=True
- reject duplicate page key
- reject critical page without performance\_budget\_ms
- reject demo/action page without browser\_smoke\_required

Geen page extraction in deze PR.
Geen dashboard routing rewrite in deze PR.
Geen live trading.
Geen signed endpoints.
Geen account/order endpoints.
```

Waarom eerst:

* Page Registry V2 is de basis voor alle verdere dashboardrefactor.
* Het is klein genoeg voor Codex.
* Het breekt de bestaande app niet als `page\_titles()` compatibel blijft.
* Het verankert no-live en browser-smoke regels meteen.
* Daarna kunnen page modules veilig één voor één worden uitgehaald.

\---

## 27\. Definition of Done

Roadmap 094 is klaar als:

* \[ ] Dashboard Refactor Safety Contract bestaat.
* \[ ] Dashboard Page Module Architecture werkt.
* \[ ] Page Registry V2 werkt.
* \[ ] Dashboard Context Builder werkt.
* \[ ] Lazy Import \& Lazy Panel Loader werkt.
* \[ ] Component System V2 werkt.
* \[ ] Widget \& Chart Key Registry V2 werkt.
* \[ ] Chart Payload \& Rendering Hardening werkt.
* \[ ] Table \& Debug Payload Hardening werkt.
* \[ ] Simple Demo UX Hardening werkt.
* \[ ] Advanced Dashboard Navigation Hardening werkt.
* \[ ] Dashboard Error Boundaries werken.
* \[ ] Dashboard Action Policy werkt.
* \[ ] Dashboard State Slimming werkt.
* \[ ] Dashboard Performance Budget Integration werkt.
* \[ ] Dashboard Smoke V2 werkt.
* \[ ] Browser Smoke Page Matrix werkt.
* \[ ] Dashboard UX Evidence Bundle werkt.
* \[ ] Dashboard docs/component guide bestaat.
* \[ ] Roadmap/Knowledge/Test/Release integraties werken.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen stable widget/chart keys.
* \[ ] Tests bewijzen payload limits/redaction.
* \[ ] Dashboard import smoke blijft groen.
* \[ ] Dashboard browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 094 kan na uitvoering naar `Voltooid docs`.

\---

## 28\. Verwachte Roadmap 095 daarna

Na Roadmap 094 zou Roadmap 095 logisch focussen op:

```text
Roadmap 095 - Runtime Core Decomposition, Event Bus \& Snapshot Optimization
```

Mogelijke inhoud:

* \[ ] `BotRuntime` opsplitsen in services;
* \[ ] typed event bus;
* \[ ] snapshot payload optimalisatie;
* \[ ] runtime step pipeline;
* \[ ] session/event batching;
* \[ ] demo pilot maintenance isolation;
* \[ ] runtime performance budgets toepassen;
* \[ ] still no live trading.

