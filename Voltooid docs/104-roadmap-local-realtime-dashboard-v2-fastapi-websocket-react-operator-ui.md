# Roadmap 104 - Local Realtime Dashboard V2, FastAPI/WebSocket Backend \& React Operator UI

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/104-roadmap-local-realtime-dashboard-v2-fastapi-websocket-react-operator-ui.md
```

## Samenvatting

Deze roadmap bouwt een volledig nieuw lokaal dashboard naast het bestaande Streamlit dashboard. Het nieuwe dashboard gebruikt **geen Streamlit** en hoeft dus niet bij elke update de volledige pagina opnieuw te rerunnen. De voorgestelde architectuur is:

```text
Python backend:
  FastAPI + Uvicorn + WebSocket/SSE + local REST API

Frontend:
  React + Vite + TypeScript + WebSocket client + lokale static build

Runtime bridge:
  BotRuntime / SessionStore / OperatorOps / ModelRegistry / Evidence
  -> typed API DTOs
  -> WebSocket event stream
  -> frontend state store
  -> instant component updates
```

Het dashboard draait volledig lokaal via Ã©Ã©n CLI command. Streamlit blijft tijdelijk bestaan als fallback totdat Dashboard V2 feature-parity, browser-smoke, no-live proof en operator acceptance heeft.

Live trading blijft volledig buiten scope. Dashboard V2 mag geen live mode toevoegen, geen signed real-order endpoints activeren en geen echte Binance account/order workflows uitvoeren. Demo/paper/testnet-readiness blijven strikt gescheiden.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 104`, `104-roadmap`, `new dashboard`, `non-streamlit`, `React dashboard`, `FastAPI dashboard`, `instant refresh` en `websocket dashboard`.
* \[x] Geen bestaande Roadmap 104 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Laatste roadmap in deze reeks is Roadmap 103: Local Paper OS User Acceptance Testing, Guided Rehearsals \& Operator Feedback Loop.

### Codebaseanalyse

Breed bekeken met focus op dashboard, runtime, CLI, checks en lokale safety:

* \[x] `src/binance\_spot\_bot/ui/streamlit\_app.py`
* \[x] `src/binance\_spot\_bot/ui/components.py`
* \[x] `src/binance\_spot\_bot/ui/page\_registry.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] `pyproject.toml`

### Belangrijke conclusies uit de codebase

* \[x] De huidige UI is sterk aan Streamlit gekoppeld. `streamlit\_app.py` bouwt sidebar controls, tabs, metrics, charts, forms, runtime state en runtime acties direct in Ã©Ã©n grote Streamlit app. Aan het einde van de loop gebruikt de app `time.sleep(2.0)` en `st.rerun()`, waardoor het dashboard steeds opnieuw voelt alsof de hele app ververst.
* \[x] `ui/components.py` gebruikt Streamlit wrappers voor Plotly charts, badges, tables, debug expanders en alerts. Dit is nuttig als referentie, maar moet voor Dashboard V2 vervangen worden door frontend components en API payloads.
* \[x] `ui/page\_registry.py` bevat 16 bestaande page definitions en valideert duplicate keys/titles plus live trading pages. Deze registry kan de bron worden voor Dashboard V2 routes en page parity checks.
* \[x] `runtime.py` heeft al duidelijke lokale modes: `demo`, `paper` en `testnet-readiness`. Unsupported modes worden geweigerd. Dit is belangrijk: Dashboard V2 moet deze modes exact volgen en nooit `live` aanbieden.
* \[x] `RuntimeSnapshot` bevat al veel data die direct bruikbaar is voor een realtime dashboard: candles, signals, fills, equity, sessions, active model, credential status, alerts, readiness, demo connection, demo orders, reconciliation en demo pilot.
* \[x] `cli.py` heeft al veel lokale operator commands, dashboard commands, demo/paper runtime commands, support/evidence commands en smoke commands. Dit is de juiste plek om `dashboard-v2` commands toe te voegen.
* \[x] `check\_all.py` forceert veilige env vars `PYTHONPATH=src`, `LIVE\_TRADING\_ENABLED=false` en `KILL\_SWITCH=true`, en draait onder meer unit tests, dashboard import, operator quality gate, local ops snapshot, CLI smoke en no-live UI check. Dashboard V2 moet hierin worden opgenomen.
* \[x] `operator\_ops.py` heeft al operator health, rehearsal profiles, support bundle restore preview, evidence chain, environment doctor, redaction self-test, command manifest, evidence manifest, local ops snapshot en operator quality gate. Dashboard V2 moet deze reports via API kunnen tonen.
* \[x] `pyproject.toml` heeft nu optionele UI dependencies voor `streamlit` en `plotly`, plus `visual` voor Playwright en `realtime` voor `websockets`. Er is nog geen FastAPI/Uvicorn/React dashboard dependency-profiel.

### Grootste probleem dat Roadmap 104 oplost

Streamlit is handig voor snelle lokale UI, maar bij een realtime bot-dashboard geeft het nadelen:

* \[ ] volledige app-reruns in plaats van component-level updates;
* \[ ] runtime/UI state zit sterk aan `st.session\_state` vast;
* \[ ] charts/tables/panels worden vaak opnieuw opgebouwd;
* \[ ] WebSocket/SSE push is niet de natuurlijke Streamlit-flow;
* \[ ] instant updates per kaart, chart of table zijn moeilijk;
* \[ ] dashboard voelt zwaar wanneer de runtime loopt.

Dashboard V2 lost dit op met een backend die events pusht naar een frontend die alleen gewijzigde componenten bijwerkt.

\---

## 1\. Hoofddoel Roadmap 104

Bouw een nieuw lokaal dashboard met instant refresh:

```text
BotRuntime / OperatorOps / SessionStore
-> Dashboard V2 Backend API
-> WebSocket/SSE live event stream
-> React/Vite frontend state store
-> component-level updates zonder full page rerun
```

Na deze roadmap moet het dashboard:

* \[ ] geen Streamlit nodig hebben;
* \[ ] lokaal draaien via Ã©Ã©n command;
* \[ ] runtime status instant tonen via WebSocket/SSE;
* \[ ] charts incrementally updaten;
* \[ ] bot starten/stoppen/stappen via veilige API actions;
* \[ ] demo/paper/testnet-readiness strikt scheiden;
* \[ ] local evidence/support/operator reports tonen;
* \[ ] no-live proof altijd zichtbaar maken;
* \[ ] browser smoke en API smoke hebben;
* \[ ] Streamlit pas later uitfaseren nadat Dashboard V2 stabiel is.

\---

## 2\. Techkeuze

### Aanbevolen standaard

```text
Backend:
  FastAPI
  Uvicorn
  Pydantic/dataclasses DTOs
  WebSocket voor live runtime events
  Server-Sent Events fallback optioneel
  Static file serving voor frontend build

Frontend:
  React
  Vite
  TypeScript
  Zustand of simpele React context voor state
  Lightweight chart rendering met Plotly.js of Apache ECharts
  Fetch API + WebSocket client
```

Waarom:

* \[ ] FastAPI past goed bij Python runtime/CLI.
* \[ ] Uvicorn kan lokaal snel draaien.
* \[ ] WebSockets geven echte push updates.
* \[ ] React/Vite geeft component-level updates zonder volledige refresh.
* \[ ] Static build kan door dezelfde lokale backend geserveerd worden.
* \[ ] Playwright browser smoke kan hergebruikt worden.
* \[ ] API contracten zijn goed testbaar zonder browser.
* \[ ] Streamlit kan als fallback blijven bestaan.

### Alternatieve lichte optie

```text
FastAPI + HTMX + Server-Sent Events + Alpine.js
```

Deze optie heeft minder Node/React complexiteit, maar React/Vite is beter voor een groter dashboard met veel charts, pages, state, filters, panels en realtime widgets.

### Besluit Roadmap 104

* \[x] Backend: FastAPI + Uvicorn.
* \[x] Live updates: WebSocket first, SSE fallback later.
* \[x] Frontend: React + Vite + TypeScript.
* \[x] Local-only hosting: Python backend serveert frontend build.
* \[x] Streamlit blijft fallback tot Dashboard V2 feature-parity heeft.

\---

## 3\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen trading runtime opnieuw bouwen.
* \[ ] Geen strategy/model/data pipeline opnieuw bouwen.
* \[ ] Geen operator evidence opnieuw bouwen.
* \[ ] Geen Streamlit direct verwijderen.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte account workflows.
* \[ ] Geen cloud deployment.
* \[ ] Geen remote telemetry.
* \[ ] Geen frontend CDN verplicht maken.
* \[ ] Geen dashboard action zonder policy/no-live guard.
* \[ ] Geen API endpoint dat raw secrets toont.

Wel doen:

* \[ ] nieuw dashboard naast bestaande Streamlit bouwen;
* \[ ] typed API DTOs toevoegen;
* \[ ] runtime bridge toevoegen;
* \[ ] WebSocket event stream toevoegen;
* \[ ] React frontend toevoegen;
* \[ ] lokale launcher en smoke tests toevoegen;
* \[ ] page-by-page migratie uitvoeren;
* \[ ] no-live proof en action policy hard afdwingen.

\---

## 4\. Fase 0 - Dashboard V2 Safety Contract

Nieuwe doc:

```text
docs/dashboard-v2-safety-contract.md
```

Regels:

* \[ ] Dashboard V2 is local-only.
* \[ ] Geen live trading.
* \[ ] Geen live mode in frontend, backend, API of CLI.
* \[ ] Alleen modes: `demo`, `paper`, `testnet-readiness`.
* \[ ] Dashboard V2 action endpoints zijn allowlisted.
* \[ ] Demo order actions vereisen bestaande demo guardrails.
* \[ ] Paper actions blijven paper-only.
* \[ ] Testnet-readiness stuurt geen orders.
* \[ ] Geen raw API keys/secrets via API.
* \[ ] Credential status is alleen fingerprint/status.
* \[ ] WebSocket events zijn redacted.
* \[ ] Frontend toont altijd `LIVE TRADING DISABLED`.
* \[ ] Backend forceert `live\_trading\_enabled=False`.
* \[ ] Browser smoke valideert no-live banner.
* \[ ] API smoke valideert geen live routes.
* \[ ] Streamlit fallback blijft onaangeraakt.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen live mode geblokkeerd is.
* \[ ] Tests bewijzen API geen live routes registreert.
* \[ ] Tests bewijzen WebSocket events secret-free zijn.
* \[ ] Dashboard V2 toont `LOCAL REALTIME DASHBOARD - NO LIVE TRADING`.

\---

## 5\. Fase 1 - Dependency \& Project Layout

Nieuwe optionele dependency group in `pyproject.toml`:

```toml
\[project.optional-dependencies]
dashboard-v2 = \[
  "fastapi>=0.115",
  "uvicorn>=0.30",
  "pydantic>=2.7",
  "websockets>=12",
]
```

Nieuwe backend map:

```text
src/binance\_spot\_bot/dashboard\_v2/
  \_\_init\_\_.py
  app.py
  api.py
  server.py
  schemas.py
  state.py
  runtime\_bridge.py
  event\_bus.py
  action\_policy.py
  redaction.py
  static.py
  smoke.py
```

Nieuwe frontend map:

```text
dashboard-v2/
  package.json
  vite.config.ts
  tsconfig.json
  index.html
  src/
    main.tsx
    App.tsx
    api/
    store/
    components/
    pages/
    charts/
    styles/
```

Build output:

```text
src/binance\_spot\_bot/dashboard\_v2/static/
```

Acceptatiecriteria:

* \[ ] Backend importeert met duidelijke error als FastAPI dependency ontbreekt.
* \[ ] `pip install -e .\[dashboard-v2]` ondersteunt backend.
* \[ ] Frontend is apart buildbaar.
* \[ ] Static build kan door Python package geserveerd worden.
* \[ ] Streamlit dependency blijft optioneel in `\[project.optional-dependencies].ui`.

\---

## 6\. Fase 2 - Dashboard V2 API Schemas

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/schemas.py
```

DTOs:

* \[ ] `DashboardV2Health`
* \[ ] `DashboardV2Config`
* \[ ] `DashboardV2Page`
* \[ ] `DashboardV2RuntimeSnapshot`
* \[ ] `DashboardV2RuntimeSummary`
* \[ ] `DashboardV2CandlePoint`
* \[ ] `DashboardV2SignalPoint`
* \[ ] `DashboardV2FillPoint`
* \[ ] `DashboardV2EquityPoint`
* \[ ] `DashboardV2Alert`
* \[ ] `DashboardV2SessionSummary`
* \[ ] `DashboardV2CredentialStatus`
* \[ ] `DashboardV2Readiness`
* \[ ] `DashboardV2ActionRequest`
* \[ ] `DashboardV2ActionResult`
* \[ ] `DashboardV2Event`
* \[ ] `DashboardV2Error`

Schema principes:

* \[ ] JSON-serializable.
* \[ ] Decimal altijd als string of safe number.
* \[ ] Timestamps in ms.
* \[ ] Geen raw secrets.
* \[ ] `live\_trading\_enabled=False` in alle root payloads.
* \[ ] `no\_live\_statement` in health/config/action payloads.
* \[ ] Grootte-limits voor candles/signals/fills/equity.
* \[ ] Backward-compatible mapping vanuit `RuntimeSnapshot`.

Acceptatiecriteria:

* \[ ] Schema tests met fake RuntimeSnapshot.
* \[ ] Secret-like values worden geredact.
* \[ ] Decimal serialization werkt.
* \[ ] Large lists worden getrimd.
* \[ ] JSON schema snapshot tests bestaan.

\---

## 7\. Fase 3 - Runtime Bridge

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/runtime\_bridge.py
```

Doel: Streamlit `st.session\_state` vervangen door backend-managed local runtime state.

Taken:

* \[ ] runtime instance lifecycle beheren;
* \[ ] selected profile/mode/source/symbol/interval/scenario/model alias beheren;
* \[ ] start/pause/stop/step/run\_steps;
* \[ ] snapshot ophalen;
* \[ ] snapshot reducer naar Dashboard V2 DTO;
* \[ ] demo armed state beheren met policy;
* \[ ] no-live proof toevoegen;
* \[ ] thread-safe lock rond runtime acties;
* \[ ] safe shutdown.

Dataclasses:

* \[ ] `DashboardRuntimeHandle`
* \[ ] `DashboardRuntimeConfig`
* \[ ] `DashboardRuntimeBridgeState`
* \[ ] `DashboardRuntimeCommandResult`

Acceptatiecriteria:

* \[ ] Bridge kan runtime creÃ«ren zonder Streamlit.
* \[ ] Bridge kan step/start/stop doen.
* \[ ] Bridge weigert `live`.
* \[ ] Bridge snapshot is redacted.
* \[ ] Tests gebruiken fake settings/runtime.

\---

## 8\. Fase 4 - Realtime Event Bus

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/event\_bus.py
```

Event types:

* \[ ] `runtime.snapshot`
* \[ ] `runtime.status`
* \[ ] `runtime.candle`
* \[ ] `runtime.signal`
* \[ ] `runtime.fill`
* \[ ] `runtime.equity`
* \[ ] `runtime.alert`
* \[ ] `runtime.session`
* \[ ] `demo.order`
* \[ ] `demo.reconciliation`
* \[ ] `operator.evidence`
* \[ ] `support.bundle`
* \[ ] `system.health`
* \[ ] `dashboard.error`

Functionaliteit:

* \[ ] subscribe/unsubscribe clients;
* \[ ] broadcast event naar WebSocket clients;
* \[ ] per-topic subscriptions;
* \[ ] event buffer latest N;
* \[ ] heartbeat ping;
* \[ ] client disconnect cleanup;
* \[ ] payload redaction;
* \[ ] payload size limit;
* \[ ] no-live proof per event.

Acceptatiecriteria:

* \[ ] Event bus kan meerdere clients bedienen.
* \[ ] Disconnected clients worden opgeschoond.
* \[ ] Events zijn secret-free.
* \[ ] Large payload wordt getrimd.
* \[ ] Tests dekken subscribe/broadcast/disconnect.

\---

## 9\. Fase 5 - FastAPI App

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/app.py
```

Routes:

```text
GET  /api/health
GET  /api/config
GET  /api/pages
GET  /api/runtime/snapshot
POST /api/runtime/config
POST /api/runtime/start
POST /api/runtime/pause
POST /api/runtime/stop
POST /api/runtime/step
POST /api/runtime/reset
GET  /api/sessions
GET  /api/sessions/{session\_id}
GET  /api/operator/health
GET  /api/operator/command-manifest
GET  /api/operator/local-ops-snapshot
POST /api/evidence/operator-export
POST /api/support-bundle/create
GET  /api/no-live-proof
WS   /ws/events
GET  /\*
```

Route regels:

* \[ ] Alle API responses hebben `live\_trading\_enabled=False`.
* \[ ] POST actions gaan door action policy.
* \[ ] Geen live route.
* \[ ] Geen account/raw-secret route.
* \[ ] Static frontend wordt lokaal geserveerd.
* \[ ] CORS beperkt tot localhost.
* \[ ] Request/response logging redacted.

Acceptatiecriteria:

* \[ ] FastAPI app kan lokaal starten.
* \[ ] `/api/health` werkt zonder runtime.
* \[ ] `/api/pages` gebruikt page registry.
* \[ ] `/ws/events` streamt heartbeat.
* \[ ] Tests met FastAPI TestClient.

\---

## 10\. Fase 6 - Dashboard V2 Action Policy

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/action\_policy.py
```

Action classes:

* \[ ] read\_only;
* \[ ] runtime\_control;
* \[ ] paper\_control;
* \[ ] demo\_connect;
* \[ ] demo\_order\_preview;
* \[ ] demo\_order\_test;
* \[ ] demo\_order\_place\_guarded;
* \[ ] evidence\_export;
* \[ ] support\_bundle;
* \[ ] forbidden.

Policy checks:

* \[ ] allowed mode;
* \[ ] requires no-live proof;
* \[ ] requires demo profile;
* \[ ] requires demo armed;
* \[ ] requires confirmation phrase;
* \[ ] blocks live mode;
* \[ ] blocks signed real-order endpoint;
* \[ ] blocks account workflow;
* \[ ] redacts result;
* \[ ] writes local audit event.

Acceptatiecriteria:

* \[ ] Runtime start/stop allowed only safe modes.
* \[ ] Live action blocked.
* \[ ] Demo place action requires existing demo guardrails.
* \[ ] Evidence/support actions allowed and redacted.
* \[ ] Tests cover action matrix.

\---

## 11\. Fase 7 - Background Runtime Loop

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/state.py
```

Doel: dashboard updates automatisch pushen zonder frontend full refresh.

Functionaliteit:

* \[ ] backend-owned run loop;
* \[ ] configurable tick interval;
* \[ ] runtime step per tick;
* \[ ] snapshot diff detectie;
* \[ ] only changed events broadcasten;
* \[ ] safe pause/stop;
* \[ ] max error count;
* \[ ] heartbeat status;
* \[ ] no-live proof status.

Loop states:

* \[ ] idle;
* \[ ] running;
* \[ ] paused;
* \[ ] stopping;
* \[ ] stopped;
* \[ ] error.

Acceptatiecriteria:

* \[ ] Run loop pusht snapshots via WebSocket.
* \[ ] Stop werkt zonder race.
* \[ ] Errors worden dashboard events.
* \[ ] Loop draait niet in testnet-readiness orders.
* \[ ] Tests met fake runtime en fake event bus.

\---

## 12\. Fase 8 - Frontend Foundation

Nieuwe frontend:

```text
dashboard-v2/src/
```

Core files:

* \[ ] `main.tsx`
* \[ ] `App.tsx`
* \[ ] `api/client.ts`
* \[ ] `api/ws.ts`
* \[ ] `store/dashboardStore.ts`
* \[ ] `types/api.ts`
* \[ ] `components/Layout.tsx`
* \[ ] `components/SafetyBanner.tsx`
* \[ ] `components/StatusBar.tsx`
* \[ ] `components/ErrorBoundary.tsx`
* \[ ] `components/MetricCard.tsx`
* \[ ] `components/ActionButton.tsx`
* \[ ] `components/LiveIndicator.tsx`

Frontend principes:

* \[ ] Geen full page refresh.
* \[ ] WebSocket reconnect.
* \[ ] REST fallback for initial load.
* \[ ] Component-level state updates.
* \[ ] Safety banner altijd zichtbaar.
* \[ ] Local-only label altijd zichtbaar.
* \[ ] Error boundary per page/panel.
* \[ ] Geen raw secrets in state.
* \[ ] Build zonder externe CDN.

Acceptatiecriteria:

* \[ ] React app start in dev.
* \[ ] Build output wordt static.
* \[ ] Health/config/snapshot laden via API.
* \[ ] WebSocket events updaten state.
* \[ ] No-live banner zichtbaar.

\---

## 13\. Fase 9 - Frontend Routing \& Page Parity

Routes gebaseerd op bestaande page registry:

```text
/
/demo-spot-trading
/credentials-profile
/bot-controls
/risk-controls
/strategy-model
/market-data
/orders-account
/sessions
/evaluation
/strategy-lab
/research
/portfolio
/readiness
/logs-security
/demo-pilot
```

Extra V2 routes:

```text
/realtime
/system
/operator
/support
/evidence
/settings
```

Migratiestrategie:

* \[ ] Eerst overview/status + runtime controls.
* \[ ] Daarna demo spot trading.
* \[ ] Daarna sessions/evidence/support.
* \[ ] Daarna market/orders/charts.
* \[ ] Daarna alle advanced pages.
* \[ ] Streamlit blijft fallback per page.

Acceptatiecriteria:

* \[ ] Alle bestaande page keys hebben V2 route of placeholder.
* \[ ] Missing route wordt in smoke gemeld.
* \[ ] No-live banner op elke route.
* \[ ] Browser smoke test critical routes.
* \[ ] Page parity report bestaat.

\---

## 14\. Fase 10 - Realtime Overview Page

Frontend page:

```text
dashboard-v2/src/pages/OverviewPage.tsx
```

Widgets:

* \[ ] runtime status;
* \[ ] live disabled;
* \[ ] mode/source/symbol/interval;
* \[ ] equity;
* \[ ] paper position;
* \[ ] active model;
* \[ ] readiness;
* \[ ] latest candle;
* \[ ] latest signal;
* \[ ] latest risk decision;
* \[ ] alerts;
* \[ ] WebSocket connection status;
* \[ ] backend loop state.

Charts:

* \[ ] candle chart;
* \[ ] equity chart;
* \[ ] signal markers;
* \[ ] fill markers;
* \[ ] chart point limit.

Acceptatiecriteria:

* \[ ] Overview update zonder full page refresh.
* \[ ] WebSocket disconnect toont warning.
* \[ ] REST refresh button haalt snapshot.
* \[ ] Chart krijgt nieuwe candles incrementally.
* \[ ] No-live proof zichtbaar.

\---

## 15\. Fase 11 - Runtime Controls Page

Frontend page:

```text
dashboard-v2/src/pages/RuntimeControlsPage.tsx
```

Actions:

* \[ ] configure runtime;
* \[ ] start;
* \[ ] pause;
* \[ ] stop;
* \[ ] step once;
* \[ ] reset;
* \[ ] set speed/tick interval;
* \[ ] select source/mode/symbol/interval/scenario;
* \[ ] select model alias.

Guardrails:

* \[ ] mode dropdown bevat geen live;
* \[ ] start disabled bij invalid config;
* \[ ] stop altijd bereikbaar;
* \[ ] action result toast/log;
* \[ ] no-live proof check voor elke POST.

Acceptatiecriteria:

* \[ ] Start/stop werkt via API.
* \[ ] UI state update via WebSocket.
* \[ ] Invalid mode geblokkeerd frontend en backend.
* \[ ] Stop action werkt ook bij backend warning.
* \[ ] Tests dekken action buttons.

\---

## 16\. Fase 12 - Demo Spot Trading Page

Frontend page:

```text
dashboard-v2/src/pages/DemoSpotTradingPage.tsx
```

Panels:

* \[ ] demo connection status;
* \[ ] credential/profile status;
* \[ ] armed/disarmed;
* \[ ] demo order preview;
* \[ ] demo test order;
* \[ ] guarded demo place;
* \[ ] open demo orders;
* \[ ] reconciliation;
* \[ ] demo order errors;
* \[ ] cancel-on-stop status;
* \[ ] audit/evidence.

Guardrails:

* \[ ] demo-only badge;
* \[ ] confirm phrase for guarded actions;
* \[ ] no real account/order wording;
* \[ ] signed credentials status redacted;
* \[ ] cannot run if profile wrong;
* \[ ] cannot run if no demo armed.

Acceptatiecriteria:

* \[ ] Demo page has instant status updates.
* \[ ] Open orders update via event stream.
* \[ ] Reconciliation result update via event stream.
* \[ ] Guarded action blocked without confirm.
* \[ ] No-live smoke passes.

\---

## 17\. Fase 13 - Sessions, Evidence \& Support Pages

Frontend pages:

```text
SessionsPage.tsx
EvidencePage.tsx
SupportPage.tsx
OperatorPage.tsx
```

Sessions:

* \[ ] list sessions;
* \[ ] session detail;
* \[ ] fills;
* \[ ] snapshots summary;
* \[ ] report paths;
* \[ ] export session report.

Evidence:

* \[ ] operator evidence export;
* \[ ] evidence manifest;
* \[ ] evidence chain;
* \[ ] no-live proof;
* \[ ] recent evidence artifacts.

Support:

* \[ ] create support bundle;
* \[ ] verify support bundles;
* \[ ] support bundle restore preview;
* \[ ] redaction self-test.

Operator:

* \[ ] operator health score;
* \[ ] local ops snapshot;
* \[ ] command manifest;
* \[ ] environment doctor;
* \[ ] data growth budget.

Acceptatiecriteria:

* \[ ] Pages work without Streamlit.
* \[ ] Long operations show progress/status.
* \[ ] Reports are downloadable.
* \[ ] Payloads are redacted.
* \[ ] Browser smoke covers support/evidence critical path.

\---

## 18\. Fase 14 - Realtime Charts \& Data Limits

Nieuwe frontend chart helpers:

```text
dashboard-v2/src/charts/
```

Charts:

* \[ ] candles;
* \[ ] equity;
* \[ ] fills;
* \[ ] signals;
* \[ ] alerts timeline;
* \[ ] runner heartbeat;
* \[ ] demo pilot counters;
* \[ ] model confidence;
* \[ ] risk blocks.

Data limits:

* \[ ] max candles in chart;
* \[ ] max signals;
* \[ ] max fills;
* \[ ] max alerts;
* \[ ] max table rows;
* \[ ] max JSON payload size;
* \[ ] frontend trimming fallback;
* \[ ] backend trimming primary.

Acceptatiecriteria:

* \[ ] Chart updates incrementally.
* \[ ] Large snapshots do not freeze frontend.
* \[ ] Backend and frontend both enforce limits.
* \[ ] Trimming warning visible.
* \[ ] Tests cover reducer behavior.

\---

## 19\. Fase 15 - Local Launcher

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/server.py
```

CLI commands:

```powershell
python -m binance\_spot\_bot.cli dashboard-v2
python -m binance\_spot\_bot.cli dashboard-v2 --host 127.0.0.1 --port 8800
python -m binance\_spot\_bot.cli dashboard-v2 --no-browser
python -m binance\_spot\_bot.cli dashboard-v2-smoke
python -m binance\_spot\_bot.cli dashboard-v2-api-smoke
python -m binance\_spot\_bot.cli dashboard-v2-browser-smoke --url http://127.0.0.1:8800
```

Launcher regels:

* \[ ] default host `127.0.0.1`;
* \[ ] default port `8800`;
* \[ ] auto-open browser optional;
* \[ ] safe env force:

  * `LIVE\_TRADING\_ENABLED=false`;
  * `KILL\_SWITCH=true`.
* \[ ] logs redacted;
* \[ ] graceful shutdown;
* \[ ] static build missing gives helpful error.

Acceptatiecriteria:

* \[ ] Dashboard V2 launches locally.
* \[ ] Uses localhost by default.
* \[ ] No API keys required.
* \[ ] Safe env verified.
* \[ ] CLI smoke passes.

\---

## 20\. Fase 16 - Dashboard V2 Smoke Tests

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/smoke.py
```

Smoke checks:

* \[ ] backend import;
* \[ ] app creation;
* \[ ] route inventory;
* \[ ] forbidden live routes absent;
* \[ ] `/api/health`;
* \[ ] `/api/config`;
* \[ ] `/api/pages`;
* \[ ] `/api/runtime/snapshot`;
* \[ ] action policy matrix;
* \[ ] WebSocket heartbeat;
* \[ ] no-live proof;
* \[ ] static build exists;
* \[ ] page parity.

Acceptatiecriteria:

* \[ ] Smoke works offline.
* \[ ] Smoke fails if live route exists.
* \[ ] Smoke fails if no-live missing.
* \[ ] Smoke exports JSON report.
* \[ ] `check-all` includes dashboard-v2 smoke.

\---

## 21\. Fase 17 - Browser Smoke for Dashboard V2

Playwright smoke:

```text
tests/browser/test\_dashboard\_v2\_browser\_smoke.py
```

Checks:

* \[ ] homepage loads;
* \[ ] no-live banner visible;
* \[ ] WebSocket connected indicator;
* \[ ] overview metrics visible;
* \[ ] start/stop buttons visible;
* \[ ] no live option in mode selector;
* \[ ] navigate demo spot page;
* \[ ] navigate sessions/evidence/support;
* \[ ] chart visible;
* \[ ] no console fatal errors;
* \[ ] screenshot artifacts optional.

Acceptatiecriteria:

* \[ ] Browser smoke can run locally.
* \[ ] Fails if no-live banner missing.
* \[ ] Fails if route unavailable.
* \[ ] Report is secret-free.
* \[ ] Baseline screenshot optional.

\---

## 22\. Fase 18 - API Security \& Local Access

Security choices:

* \[ ] Bind only to localhost by default.
* \[ ] Optional local token for API mutation routes.
* \[ ] CORS only localhost.
* \[ ] No cookie/session auth initially.
* \[ ] Redacted request logs.
* \[ ] Block path traversal.
* \[ ] Block raw file reads outside allowed artifacts.
* \[ ] File downloads only for allowed evidence/report/support artifacts.
* \[ ] Rate-limit heavy actions lightly.
* \[ ] WebSocket max clients configurable.

Acceptatiecriteria:

* \[ ] Mutation routes blocked without local token if enabled.
* \[ ] Path traversal tests pass.
* \[ ] CORS config is local only.
* \[ ] Raw secrets never returned.
* \[ ] Security scan passes.

\---

## 23\. Fase 19 - Replace Streamlit Gradually

Migration plan:

### Stage A - Run side-by-side

* \[ ] Streamlit remains default.
* \[ ] Dashboard V2 is opt-in command.
* \[ ] Both can read same runtime/settings artifacts.
* \[ ] No shared mutable state conflict in default mode.

### Stage B - Feature parity for critical workflows

* \[ ] Overview.
* \[ ] Runtime control.
* \[ ] Demo spot trading.
* \[ ] Sessions.
* \[ ] Evidence.
* \[ ] Support.
* \[ ] Operator health.
* \[ ] Logs/security.
* \[ ] Readiness.

### Stage C - V2 becomes recommended

* \[ ] README recommends Dashboard V2.
* \[ ] Streamlit marked legacy/fallback.
* \[ ] `dashboard` command can show choice.

### Stage D - Optional Streamlit deprecation roadmap later

* \[ ] No deletion in Roadmap 104.
* \[ ] Future Roadmap 105/106 can deprecate if V2 stable.

Acceptatiecriteria:

* \[ ] Existing Streamlit tests keep passing.
* \[ ] Dashboard V2 tests pass.
* \[ ] No CLI breaking changes.
* \[ ] Docs explain both dashboards.
* \[ ] Operator can choose V2 safely.

\---

## 24\. Fase 20 - Documentation

Nieuwe docs:

```text
docs/dashboard-v2/
  architecture.md
  safety-contract.md
  backend-api.md
  websocket-events.md
  frontend-architecture.md
  local-launcher.md
  action-policy.md
  page-parity.md
  browser-smoke.md
  migration-from-streamlit.md
  troubleshooting.md
```

README updates:

* \[ ] Explain Streamlit vs Dashboard V2.
* \[ ] Add install instructions.
* \[ ] Add launch command.
* \[ ] Add no-live statement.
* \[ ] Add dashboard-v2 smoke commands.
* \[ ] Add migration status.

Acceptatiecriteria:

* \[ ] Docs include architecture diagram.
* \[ ] Docs include API route list.
* \[ ] Docs include WebSocket event examples.
* \[ ] Docs include no-live proof.
* \[ ] Docs validated by docs consistency checks.

\---

## 25\. Fase 21 - Tests

### Backend unit tests

* \[ ] `tests/test\_dashboard\_v2\_safety\_contract.py`
* \[ ] `tests/test\_dashboard\_v2\_schemas.py`
* \[ ] `tests/test\_dashboard\_v2\_runtime\_bridge.py`
* \[ ] `tests/test\_dashboard\_v2\_event\_bus.py`
* \[ ] `tests/test\_dashboard\_v2\_action\_policy.py`
* \[ ] `tests/test\_dashboard\_v2\_app.py`
* \[ ] `tests/test\_dashboard\_v2\_smoke.py`
* \[ ] `tests/test\_dashboard\_v2\_static.py`

### Frontend tests

* \[ ] component rendering;
* \[ ] state reducer;
* \[ ] WebSocket event reducer;
* \[ ] no-live banner;
* \[ ] forbidden mode selector;
* \[ ] action disabled reasons.

### Integration tests

* \[ ] FastAPI TestClient health/config/pages.
* \[ ] Runtime snapshot mapping.
* \[ ] Runtime start/stop with fake runtime.
* \[ ] WebSocket heartbeat.
* \[ ] WebSocket runtime snapshot event.
* \[ ] Evidence/support API.
* \[ ] Dashboard V2 API smoke.
* \[ ] Dashboard V2 browser smoke.

### Safety tests

* \[ ] Live mode blocked.
* \[ ] Live route absent.
* \[ ] Signed/account/order route absent.
* \[ ] Demo place action requires guardrails.
* \[ ] API responses secret-free.
* \[ ] WebSocket events secret-free.
* \[ ] Localhost default.
* \[ ] No-live banner visible.
* \[ ] `check-all` safe env preserved.

\---

## 26\. Fase 22 - Check-All Integratie

`check\_all.py` uitbreiden met optionele Dashboard V2 checks:

* \[ ] `dashboard\_v2\_import`
* \[ ] `dashboard\_v2\_api\_smoke`
* \[ ] `dashboard\_v2\_no\_live\_routes`
* \[ ] `dashboard\_v2\_static\_exists` indien frontend build aanwezig;
* \[ ] `dashboard\_v2\_browser\_smoke` optioneel/profiel afhankelijk.

Acceptatiecriteria:

* \[ ] Check-all blijft werken zonder frontend build, maar geeft duidelijke optional warning.
* \[ ] Deep profile vereist Dashboard V2 browser smoke.
* \[ ] No-live route check is hard fail.
* \[ ] Smoke reports secret-free.
* \[ ] Existing Streamlit import check blijft.

\---

## 27\. Fase 23 - Operator/UAT Integratie

Roadmap 102 integratie:

* \[ ] Operator manual krijgt Dashboard V2 quick start.
* \[ ] Dashboard walkthroughs krijgen V2 routes.
* \[ ] CLI cookbook krijgt dashboard-v2 commands.
* \[ ] Support playbooks krijgen V2 troubleshooting.

Roadmap 103 integratie:

* \[ ] UAT scenario voor Dashboard V2 first launch.
* \[ ] UAT scenario voor realtime updates.
* \[ ] UAT scenario voor no-live route proof.
* \[ ] UAT feedback backlog kan V2 UX issues registreren.
* \[ ] UAT scorecard meet V2 usability.

Acceptatiecriteria:

* \[ ] Operator docs verwijzen naar Dashboard V2.
* \[ ] UAT scenarioâ€™s kunnen Dashboard V2 valideren.
* \[ ] Feedback-to-backlog werkt voor V2.
* \[ ] No-live training bevat V2 proof.
* \[ ] Browser smoke/UAT evidence linkt naar V2.

\---

## 28\. Fase 24 - Release/Migration/Knowledge/Test Integratie

Roadmap 089:

* \[ ] Release notes krijgen Dashboard V2 section.
* \[ ] Migration notes: Streamlit blijft fallback.
* \[ ] Version manifest bevat dashboard-v2 status.

Roadmap 090:

* \[ ] Codex task packs voor dashboard-v2.
* \[ ] Completion gate vereist API smoke + browser smoke.

Roadmap 091:

* \[ ] Knowledge graph herkent dashboard\_v2 backend/frontend.
* \[ ] Impact analysis koppelt frontend route aan backend APIs.

Roadmap 092:

* \[ ] Test selector selecteert dashboard\_v2 tests bij API/frontend changes.
* \[ ] UI changes selecteren browser smoke.

Roadmap 093:

* \[ ] Performance profiler meet API latency, WebSocket event rate, frontend load time.
* \[ ] Dashboard V2 budgets: initial load, event latency, chart update latency.

Acceptatiecriteria:

* \[ ] Release evidence bevat Dashboard V2 status.
* \[ ] Test selection werkt op dashboard\_v2 changes.
* \[ ] Knowledge graph toont dashboard\_v2 route/API map.
* \[ ] Performance budget report bevat dashboard\_v2.
* \[ ] No-live proof preserved.

\---

## 29\. CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli dashboard-v2
python -m binance\_spot\_bot.cli dashboard-v2 --host 127.0.0.1 --port 8800
python -m binance\_spot\_bot.cli dashboard-v2 --no-browser
python -m binance\_spot\_bot.cli dashboard-v2-build-info
python -m binance\_spot\_bot.cli dashboard-v2-route-list
python -m binance\_spot\_bot.cli dashboard-v2-api-smoke --json
python -m binance\_spot\_bot.cli dashboard-v2-smoke --json
python -m binance\_spot\_bot.cli dashboard-v2-browser-smoke --url http://127.0.0.1:8800 --json
python -m binance\_spot\_bot.cli dashboard-v2-page-parity --json
python -m binance\_spot\_bot.cli dashboard-v2-no-live-proof --json
```

Acceptatiecriteria:

* \[ ] Commands werken offline.
* \[ ] Commands ondersteunen JSON output.
* \[ ] Commands gebruiken safe env.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Reports zijn secret-free.

\---

## 30\. Codex bouwvolgorde

### PR 1 - Safety Contract + Backend Skeleton

* \[ ] `docs/dashboard-v2-safety-contract.md`
* \[ ] `dashboard\_v2/\_\_init\_\_.py`
* \[ ] `dashboard\_v2/schemas.py`
* \[ ] `dashboard\_v2/app.py`
* \[ ] `/api/health`
* \[ ] tests voor no-live health/config.

### PR 2 - Runtime Bridge

* \[ ] `dashboard\_v2/runtime\_bridge.py`
* \[ ] create/start/stop/step/snapshot.
* \[ ] fake runtime tests.
* \[ ] live mode block tests.

### PR 3 - Event Bus + WebSocket

* \[ ] `dashboard\_v2/event\_bus.py`
* \[ ] `/ws/events`
* \[ ] heartbeat.
* \[ ] redaction/payload limit tests.

### PR 4 - Action Policy + Runtime API

* \[ ] `dashboard\_v2/action\_policy.py`
* \[ ] runtime POST routes.
* \[ ] policy matrix tests.

### PR 5 - Frontend Foundation

* \[ ] React/Vite/TypeScript setup.
* \[ ] health/config API client.
* \[ ] WebSocket client.
* \[ ] safety banner/status bar.

### PR 6 - Overview + Runtime Controls

* \[ ] Overview page.
* \[ ] Runtime controls page.
* \[ ] realtime state updates.
* \[ ] frontend tests.

### PR 7 - Demo Spot + Sessions/Evidence/Support

* \[ ] Demo Spot Trading page.
* \[ ] Sessions page.
* \[ ] Evidence page.
* \[ ] Support page.
* \[ ] API endpoints.

### PR 8 - Charts + Data Limits

* \[ ] realtime chart components.
* \[ ] reducers/trimming.
* \[ ] chart tests.
* \[ ] payload warnings.

### PR 9 - Launcher + CLI + Smoke

* \[ ] `dashboard\_v2/server.py`
* \[ ] CLI commands.
* \[ ] API smoke.
* \[ ] no-live proof.
* \[ ] check-all integration.

### PR 10 - Browser Smoke + Docs + Migration

* \[ ] Playwright browser smoke.
* \[ ] docs/dashboard-v2.
* \[ ] README update.
* \[ ] page parity report.
* \[ ] operator/UAT integration.

\---

## 31\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 104 PR 1: Dashboard V2 Safety Contract + FastAPI Backend Skeleton.

Maak docs/dashboard-v2-safety-contract.md.

Voeg optionele dependency group dashboard-v2 toe aan pyproject.toml:
- fastapi>=0.115
- uvicorn>=0.30
- pydantic>=2.7
- websockets>=12

Maak package:
src/binance\_spot\_bot/dashboard\_v2/\_\_init\_\_.py
src/binance\_spot\_bot/dashboard\_v2/schemas.py
src/binance\_spot\_bot/dashboard\_v2/app.py

In schemas.py:
- DashboardV2Health
- DashboardV2Config
- DashboardV2Page
- DashboardV2Error
- helper dashboard\_v2\_no\_live\_statement()
- helper redact\_dashboard\_payload(payload)

In app.py:
- create\_dashboard\_v2\_app(settings: BotSettings | None = None)
- GET /api/health
- GET /api/config
- GET /api/pages

/api/health moet teruggeven:
- status
- app\_name
- version
- live\_trading\_enabled=False
- no\_live\_statement
- supported\_modes: demo, paper, testnet-readiness

/api/config moet teruggeven:
- supported\_modes zonder live
- supported\_sources
- default\_symbol
- live\_trading\_enabled=False
- no\_live\_statement

/api/pages moet gebaseerd zijn op ui.page\_registry.PAGES:
- key
- title
- live\_trading\_enabled=False

Validatie:
- als een page live\_trading\_enabled=True heeft, moet /api/pages of app startup falen
- live mag nergens in supported\_modes zitten
- payloads moeten secret-free zijn

Voeg tests toe:
- test\_dashboard\_v2\_health\_no\_live
- test\_dashboard\_v2\_config\_no\_live
- test\_dashboard\_v2\_pages\_from\_registry
- test\_dashboard\_v2\_rejects\_live\_page
- test\_dashboard\_v2\_payload\_redaction
- test\_dashboard\_v2\_no\_live\_statement\_present

Geen React frontend in deze PR.
Geen runtime bridge in deze PR.
Geen WebSocket in deze PR.
Geen Streamlit wijzigen.
Geen live trading.
Geen signed endpoints.
Geen account/order endpoints.
```

Waarom eerst:

* Het legt het nieuwe dashboardfundament zonder Streamlit aan.
* Het raakt runtime/execution nog niet.
* Het is klein genoeg voor Codex.
* No-live en page-registry regels worden meteen hard gemaakt.
* Daarna kan runtime bridge en WebSocket streaming veilig worden toegevoegd.

\---

## 32\. Definition of Done

Roadmap 104 is klaar als:

* \[ ] Dashboard V2 Safety Contract bestaat.
* \[ ] Dependency/project layout bestaat.
* \[ ] Dashboard V2 API schemas bestaan.
* \[ ] Runtime bridge werkt zonder Streamlit.
* \[ ] Realtime event bus werkt.
* \[ ] FastAPI app werkt.
* \[ ] Action policy werkt.
* \[ ] Background runtime loop werkt.
* \[ ] React/Vite frontend foundation werkt.
* \[ ] Frontend routing/page parity werkt.
* \[ ] Realtime overview werkt.
* \[ ] Runtime controls werken.
* \[ ] Demo Spot Trading page werkt.
* \[ ] Sessions/Evidence/Support pages werken.
* \[ ] Realtime charts en limits werken.
* \[ ] Local launcher werkt.
* \[ ] Dashboard V2 smoke werkt.
* \[ ] Browser smoke werkt.
* \[ ] API security/local access werkt.
* \[ ] Streamlit blijft fallback.
* \[ ] Docs bestaan.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen WebSocket/API payloads secret-free zijn.
* \[ ] Tests bewijzen instant updates zonder full rerun-flow.
* \[ ] Check-all blijft groen.
* \[ ] Dashboard V2 kan lokaal draaien.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 104 kan na uitvoering naar `Voltooid docs`.

\---

## 33\. Verwachte Roadmap 105 daarna

Na Roadmap 104 is de beste opvolger waarschijnlijk:

```text
Roadmap 105 - Dashboard V2 Feature Parity, Streamlit Legacy Mode \& Advanced Page Migration
```

Mogelijke inhoud:

* \[ ] alle overgebleven Streamlit pages migreren;
* \[ ] page parity score naar 100%;
* \[ ] advanced panels lazy laden;
* \[ ] Streamlit legacy banner;
* \[ ] operator/UAT feedback verwerken;
* \[ ] Dashboard V2 performance budgets;
* \[ ] eventueel Streamlit deprecation plan;
* \[ ] still no live trading.

```

Als Dashboard V2 UAT veel UX feedback oplevert:

```text
Roadmap 105 - Dashboard V2 UX Polish, Realtime Chart Optimization \& Operator Workflow Simplification
```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Dashboard V2 realtime contract, backend state, websocket events en no-refresh smoke.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.


---

## Implementatie-evidence 2026-05-15

Status: Volledig afgewerkt en gevalideerd.

Gebouwd:

* [x] Dashboard V2 safety contract en docs.
* [x] Optionele `dashboard-v2` dependency group.
* [x] `src/binance_spot_bot/dashboard_v2/` package.
* [x] API schemas met no-live/redaction/Decimal/list limits.
* [x] Runtime bridge zonder Streamlit session state.
* [x] Realtime event bus met subscribe/broadcast/unsubscribe en payload trimming.
* [x] FastAPI app factory met fallback als FastAPI niet geinstalleerd is.
* [x] Action policy met live/account/order blokkades en demo guardrails.
* [x] Background runtime loop die snapshot events pusht.
* [x] React/Vite/TypeScript frontend scaffold met safety banner en WebSocket client.
* [x] Page parity en route smoke.
* [x] Dashboard V2 local launcher plan.
* [x] Dashboard V2 CLI commands.
* [x] Check-all integratie voor Dashboard V2 import en API smoke.

Belangrijke bestanden:

* `src/binance_spot_bot/dashboard_v2/schemas.py`
* `src/binance_spot_bot/dashboard_v2/app.py`
* `src/binance_spot_bot/dashboard_v2/action_policy.py`
* `src/binance_spot_bot/dashboard_v2/event_bus.py`
* `src/binance_spot_bot/dashboard_v2/runtime_bridge.py`
* `src/binance_spot_bot/dashboard_v2/state.py`
* `src/binance_spot_bot/dashboard_v2/server.py`
* `src/binance_spot_bot/dashboard_v2/smoke.py`
* `dashboard-v2/src/App.tsx`
* `dashboard-v2/src/api/ws.ts`
* `dashboard-v2/src/store/dashboardStore.ts`
* `tests/test_roadmap_104_dashboard_v2_acceptance.py`

Validatie:

* [x] `python -m pytest tests/test_roadmap_104_dashboard_v2_acceptance.py tests/test_roadmaps_104_122_full_surface.py::test_104_dashboard_v2_realtime_contract_has_no_full_refresh -q` -> 7 passed.
* [x] Dashboard V2 CLI command flow uitgevoerd.
* [x] `python -m pytest tests/test_roadmaps_104_122_full_surface.py tests/test_roadmap_104_dashboard_v2_acceptance.py -q` -> 14 passed.
* [x] `python -m binance_spot_bot.cli check-all --skip-tests --json` -> ok.
* [x] `python -m binance_spot_bot.cli dashboard-smoke --seconds 1` -> ok.
* [x] `python -m pytest -q` -> 393 passed, 1 warning.

Safety-resultaat:

* [x] Live mode zit niet in Dashboard V2 supported modes.
* [x] Live routes zijn afwezig.
* [x] API/WebSocket payloads zijn redacted en bevatten `live_trading_enabled=False`.
* [x] Demo place action vereist demo mode, armed state en confirm phrase.
* [x] Streamlit blijft fallback; niets is verwijderd.
