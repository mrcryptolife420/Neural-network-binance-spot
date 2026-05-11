# Roadmap 106 - Dashboard V2 Performance, Desktop Packaging \& Streamlit Cutover Readiness

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/106-roadmap-dashboard-v2-performance-desktop-packaging-streamlit-cutover-readiness.md
```

## Samenvatting

Roadmap 104 bouwt het fundament voor een nieuw lokaal realtime dashboard zonder Streamlit: FastAPI/Uvicorn backend, WebSocket events, React/Vite frontend, action policy, runtime bridge, API smoke en browser smoke.

Roadmap 105 migreert daarna de belangrijkste Streamlit features naar Dashboard V2: page parity, advanced pages, Streamlit legacy/fallback mode, realtime UX en operator/UAT integratie.

Roadmap 106 is de logische volgende stap: **Dashboard V2 hard maken als de aanbevolen lokale operator UI**. De focus ligt op performance, realtime stabiliteit, desktop/local packaging, frontend/backend latency budgets, offline static builds, operator launch experience, crash recovery, update/migration safety, Streamlit cutover readiness en evidence.

Streamlit wordt in deze roadmap nog niet blind verwijderd. Streamlit blijft fallback totdat Dashboard V2 aantoonbaar sneller, stabieler, volledig smoke-tested en operator-accepted is.

Live trading blijft volledig buiten scope. Dashboard V2 blijft alleen demo/paper/testnet-readiness. Geen live mode, geen signed real-order endpoints, geen echte account workflows en geen cloud/remote telemetry.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 106`, `106-roadmap`, `Dashboard V2 Performance`, `Streamlit Deprecation`, `Desktop Launcher`, `Realtime UX` en `Dashboard V2 Packaging`.
* \[x] Geen bestaande Roadmap 106 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 104 en 105 zijn de directe dashboard-vervolgroadmaps.

### Codebasecontrole

Breed bekeken met focus op dashboard, runtime, CLI, smoke, safety en packaging:

* \[x] `src/binance\_spot\_bot/ui/streamlit\_app.py`
* \[x] `src/binance\_spot\_bot/ui/page\_registry.py`
* \[x] `src/binance\_spot\_bot/ui/components.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] `pyproject.toml`

### Belangrijke conclusies

De huidige Streamlit UI is groot en centraliseert heel veel dashboard-gedrag:

* \[x] `streamlit\_app.py` bevat veel imports, sidebar state, runtime creation, 36 tabs/pages, runtime controls, demo trading, support/evidence, paper OS audit, stabilization en operator training.
* \[x] Bij running state gebruikt Streamlit `time.sleep(2.0)` en `st.rerun()`, waardoor updates als volledige refresh voelen.
* \[x] `ui/page\_registry.py` heeft 36 pages en blokkeert live trading pages. Dit is de basis voor Dashboard V2 page parity en cutover readiness.
* \[x] `cli.py` heeft al veel commands voor dashboard, smoke, paper sessions, support/evidence, demo execution en check-all. Dashboard V2 moet hier netjes in worden geïntegreerd.
* \[x] `check\_all.py` forceert veilige env vars met `LIVE\_TRADING\_ENABLED=false` en `KILL\_SWITCH=true`; Dashboard V2 checks moeten dezelfde safety basis gebruiken.
* \[x] Runtime modes blijven beperkt tot `demo`, `paper` en `testnet-readiness`.
* \[x] Operator tooling heeft al evidence, redaction, local ops snapshot, command manifest en operator quality gate.

### Belangrijkste gat na Roadmap 105

Na Roadmap 105 heeft Dashboard V2 feature parity en migratiebasis, maar er blijven production-quality lokale UI zorgen:

* \[ ] Is Dashboard V2 sneller dan Streamlit bij grote snapshots?
* \[ ] Zijn WebSocket reconnects stabiel?
* \[ ] Zijn chart updates performant bij veel candles/fills/signals?
* \[ ] Is de frontend build offline en reproduceerbaar?
* \[ ] Is er een simpele lokale launcher voor operators?
* \[ ] Zijn logs, crashes en backend errors begrijpelijk?
* \[ ] Kan Dashboard V2 zonder Node dev server draaien?
* \[ ] Zijn API payloads begrensd en gemeten?
* \[ ] Is er een cutover scorecard van Streamlit naar Dashboard V2?
* \[ ] Kan Streamlit veilig legacy/fallback worden?
* \[ ] Zijn browser smoke en API smoke voldoende betrouwbaar voor check-all?
* \[ ] Is er een rollback/fallback plan als Dashboard V2 faalt?

Roadmap 106 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 106

Maak Dashboard V2 klaar als aanbevolen lokale operator UI:

```text
Dashboard V2 feature parity
→ performance budgets
→ WebSocket stability
→ static/offline frontend build
→ desktop/local launcher
→ smoke/reliability evidence
→ Streamlit legacy fallback
→ cutover readiness score
```

Na deze roadmap moet Dashboard V2:

* \[ ] lokaal starten met één command;
* \[ ] frontend static build serveren zonder Node dev server;
* \[ ] realtime updates tonen zonder full page rerun;
* \[ ] WebSocket reconnects betrouwbaar afhandelen;
* \[ ] API payloads begrenzen en meten;
* \[ ] charts snel houden bij grotere datasets;
* \[ ] browser smoke stabiel doorstaan;
* \[ ] logs/crashes/operator errors begrijpelijk tonen;
* \[ ] Streamlit legacy/fallback status duidelijk tonen;
* \[ ] no-live proof altijd tonen;
* \[ ] check-all/deep profile integratie hebben;
* \[ ] een cutover readiness score halen.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe trading runtime.
* \[ ] Geen nieuwe modeltraining pipeline.
* \[ ] Geen nieuwe data pipeline.
* \[ ] Geen Dashboard V2 foundation opnieuw bouwen; Roadmap 104 doet dat.
* \[ ] Geen page feature parity opnieuw plannen; Roadmap 105 doet dat.
* \[ ] Geen Streamlit direct verwijderen.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte account workflows.
* \[ ] Geen cloud deployment.
* \[ ] Geen remote telemetry.
* \[ ] Geen externe frontend CDN.
* \[ ] Geen auto-updater die code downloadt.
* \[ ] Geen desktop app die firewall/remote access opent.

Wel doen:

* \[ ] Dashboard V2 performance hardening;
* \[ ] WebSocket reconnect/stability;
* \[ ] frontend production build pipeline;
* \[ ] local launcher/desktop shortcut;
* \[ ] crash/error reporting local-only;
* \[ ] API payload budgets;
* \[ ] browser smoke reliability;
* \[ ] Streamlit legacy fallback;
* \[ ] cutover readiness evidence.

\---

## 3\. Fase 0 - Dashboard V2 Cutover Safety Contract

Nieuw docbestand:

```text
docs/dashboard-v2-cutover-safety-contract.md
```

Regels:

* \[ ] Dashboard V2 cutover is local-only.
* \[ ] Geen live trading.
* \[ ] Geen live mode in frontend/backend/CLI.
* \[ ] Alleen `demo`, `paper`, `testnet-readiness`.
* \[ ] Streamlit blijft fallback tot cutover gate pass.
* \[ ] Dashboard V2 launcher bindt default alleen op `127.0.0.1`.
* \[ ] Geen remote telemetry.
* \[ ] Geen externe CDN.
* \[ ] Geen raw secrets in API/WebSocket/frontend logs.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte account workflows.
* \[ ] Local crash reports worden geredact.
* \[ ] Cutover readiness vereist no-live proof.
* \[ ] Rollback naar Streamlit fallback moet gedocumenteerd zijn.
* \[ ] Operator moet kunnen zien welk dashboard actief is.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen live mode niet in Dashboard V2 cutover config zit.
* \[ ] Tests bewijzen launcher default localhost is.
* \[ ] Tests bewijzen crash reports secret-free zijn.
* \[ ] Tests bewijzen Streamlit fallback niet verwijderd is.

\---

## 4\. Fase 1 - Dashboard V2 Performance Baseline

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/performance\_baseline.py
```

Doel: meetbare baseline maken vóór optimalisaties.

Te meten:

* \[ ] backend startup time;
* \[ ] `/api/health` latency;
* \[ ] `/api/config` latency;
* \[ ] `/api/pages` latency;
* \[ ] `/api/runtime/snapshot` latency;
* \[ ] WebSocket connect latency;
* \[ ] WebSocket heartbeat interval stability;
* \[ ] snapshot serialization duration;
* \[ ] payload bytes per endpoint;
* \[ ] frontend initial load time;
* \[ ] route navigation time;
* \[ ] chart render/update time;
* \[ ] memory best-effort;
* \[ ] CPU best-effort;
* \[ ] browser console errors.

Output:

```text
data/dashboard-v2/performance/
  baseline.json
  baseline.md
```

Acceptatiecriteria:

* \[ ] Baseline kan offline draaien.
* \[ ] Baseline heeft JSON + Markdown output.
* \[ ] Baseline bevat no-live proof.
* \[ ] Baseline is secret-free.
* \[ ] Tests gebruiken fake timings/payloads.

\---

## 5\. Fase 2 - Dashboard V2 Performance Budgets

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/performance\_budgets.py
```

Budgetten:

* \[ ] backend startup max ms;
* \[ ] health/config/pages endpoint max ms;
* \[ ] snapshot endpoint max ms;
* \[ ] snapshot max bytes;
* \[ ] WebSocket connect max ms;
* \[ ] WebSocket event max bytes;
* \[ ] frontend initial load max ms;
* \[ ] route switch max ms;
* \[ ] chart update max ms;
* \[ ] max frontend JS bundle bytes warning;
* \[ ] max static asset count;
* \[ ] max browser console fatal errors;
* \[ ] max reconnect failure count.

Budget statuses:

* \[ ] pass;
* \[ ] warn;
* \[ ] fail;
* \[ ] skipped;
* \[ ] unknown.

Acceptatiecriteria:

* \[ ] Budget evaluator werkt op baseline report.
* \[ ] Hard fail bij no-live proof missing.
* \[ ] Snapshot payload oversize wordt fail/warn volgens policy.
* \[ ] Markdown report met aanbevelingen.
* \[ ] Check-all kan budget evaluator draaien.

\---

## 6\. Fase 3 - API Payload Slimming \& Snapshot Profiles

Uitbreiding op Dashboard V2 backend:

```text
src/binance\_spot\_bot/dashboard\_v2/payload\_profiles.py
```

Profiles:

* \[ ] `header`
* \[ ] `overview`
* \[ ] `chart`
* \[ ] `orders`
* \[ ] `sessions`
* \[ ] `evidence`
* \[ ] `debug`
* \[ ] `full`

Regels:

* \[ ] Frontend vraagt niet altijd full snapshot.
* \[ ] Header gebruikt compact summary.
* \[ ] Charts gebruiken chart payload met limits.
* \[ ] Sessions/evidence lazy loaded.
* \[ ] Debug JSON alleen op expliciete vraag.
* \[ ] Payload stats teruggeven in response metadata.
* \[ ] Trimmed counts zichtbaar maken.

Acceptatiecriteria:

* \[ ] `/api/runtime/snapshot?profile=overview` werkt.
* \[ ] `/api/runtime/snapshot?profile=chart` werkt.
* \[ ] Full profile blijft beschikbaar voor debug.
* \[ ] Payload size daalt voor overview.
* \[ ] Tests dekken trimming en redaction.

\---

## 7\. Fase 4 - WebSocket Stability \& Reconnect

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/ws\_stability.py
```

Backend:

* \[ ] heartbeat events;
* \[ ] client id;
* \[ ] reconnect token optional local-only;
* \[ ] last event id;
* \[ ] replay latest buffered events;
* \[ ] disconnect cleanup;
* \[ ] max clients;
* \[ ] stale client cleanup;
* \[ ] backpressure/drop policy;
* \[ ] event size guard.

Frontend:

* \[ ] exponential reconnect;
* \[ ] visible connection status;
* \[ ] stale data badge;
* \[ ] missed event counter;
* \[ ] manual reconnect;
* \[ ] fallback REST refresh;
* \[ ] no duplicate event application.

Acceptatiecriteria:

* \[ ] Reconnect test passes.
* \[ ] Duplicate events are ignored or idempotent.
* \[ ] Lost connection shows UI warning.
* \[ ] REST fallback works.
* \[ ] Tests cover disconnect/reconnect/replay.

\---

## 8\. Fase 5 - Frontend State \& Render Optimization

Frontend tasks:

* \[ ] split global state into slices:

  * runtime;
  * charts;
  * orders;
  * sessions;
  * evidence;
  * operator;
  * settings.
* \[ ] memoize heavy chart components;
* \[ ] virtualize large tables;
* \[ ] lazy-load advanced pages;
* \[ ] route-level code splitting;
* \[ ] avoid full app state replacement;
* \[ ] diff incoming event payloads;
* \[ ] cap chart data points;
* \[ ] cap table rows;
* \[ ] add render counter in debug mode;
* \[ ] add slow render warning.

Acceptatiecriteria:

* \[ ] Overview updates do not rerender all pages.
* \[ ] Heavy pages lazy load.
* \[ ] Large tables do not freeze UI.
* \[ ] Debug render stats visible.
* \[ ] Frontend tests cover reducers/selectors.

\---

## 9\. Fase 6 - Realtime Chart Optimization

Frontend chart improvements:

* \[ ] append candle updates instead of replacing all data.
* \[ ] append equity points.
* \[ ] update signal markers incrementally.
* \[ ] update fill markers incrementally.
* \[ ] use fixed max point window.
* \[ ] use downsampling for long histories.
* \[ ] separate live view vs history view.
* \[ ] pause chart updates toggle.
* \[ ] chart error boundary.
* \[ ] chart performance telemetry.

Backend chart API:

```text
GET /api/charts/candles?tail=500
GET /api/charts/equity?tail=500
GET /api/charts/signals?tail=200
GET /api/charts/fills?tail=200
```

Acceptatiecriteria:

* \[ ] Chart updates feel instant.
* \[ ] No full chart rebuild for every event where possible.
* \[ ] Tail limits enforced backend/frontend.
* \[ ] Chart pause works.
* \[ ] Browser smoke covers chart update.

\---

## 10\. Fase 7 - Static Frontend Build \& Offline Assets

Frontend build tasks:

* \[ ] `npm run build`;
* \[ ] static assets output to package static dir;
* \[ ] asset manifest generated;
* \[ ] no external CDN links;
* \[ ] no remote fonts;
* \[ ] cache busting via hashed filenames;
* \[ ] build metadata JSON;
* \[ ] frontend version shown in UI;
* \[ ] backend validates static build exists;
* \[ ] static build verification command.

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/static\_build.py
```

Acceptatiecriteria:

* \[ ] Static build can be served by backend.
* \[ ] Static build has manifest.
* \[ ] No external URLs required.
* \[ ] Missing build gives clear operator error.
* \[ ] Tests verify manifest and no external CDN.

\---

## 11\. Fase 8 - Local Launcher UX

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/launcher.py
```

Launcher features:

* \[ ] `dashboard-v2` command opens browser by default.
* \[ ] `--no-browser`.
* \[ ] `--host 127.0.0.1`.
* \[ ] `--port 8800`.
* \[ ] `--find-free-port`.
* \[ ] startup health wait.
* \[ ] browser open after healthy.
* \[ ] print local URL.
* \[ ] print no-live statement.
* \[ ] write launcher session file.
* \[ ] graceful shutdown.
* \[ ] useful error if dependencies missing.
* \[ ] useful error if frontend build missing.

Acceptatiecriteria:

* \[ ] One command starts local UI.
* \[ ] Default host is localhost.
* \[ ] Live trading disabled shown in console.
* \[ ] Launcher session file written.
* \[ ] Tests use fake server/bind.

\---

## 12\. Fase 9 - Desktop Shortcut / Windows Local App Helper

Geen Electron verplicht. Simpel en lokaal:

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/desktop\_shortcut.py
```

Windows helper:

* \[ ] generate `.cmd` launcher;
* \[ ] generate PowerShell launcher;
* \[ ] optional Desktop shortcut instructions;
* \[ ] check Python path;
* \[ ] check venv path if available;
* \[ ] check project root;
* \[ ] run `dashboard-v2 --find-free-port`;
* \[ ] no-live statement in launcher.
* \[ ] safe uninstall shortcut instructions.

Commands:

```powershell
python -m binance\_spot\_bot.cli dashboard-v2-create-shortcut
python -m binance\_spot\_bot.cli dashboard-v2-shortcut-info
```

Acceptatiecriteria:

* \[ ] Shortcut generation is optional.
* \[ ] No admin privileges required.
* \[ ] Generated script contains no secrets.
* \[ ] Script uses localhost.
* \[ ] Tests validate generated script content.

\---

## 13\. Fase 10 - Local Crash \& Error Reports

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/error\_reports.py
```

Report captures:

* \[ ] backend exception summary;
* \[ ] route/action context;
* \[ ] redacted stack trace;
* \[ ] frontend error boundary report;
* \[ ] WebSocket disconnect summary;
* \[ ] startup failure;
* \[ ] static build missing;
* \[ ] dependency missing;
* \[ ] no-live proof;
* \[ ] suggested playbook.

Storage:

```text
data/dashboard-v2/errors/
```

Acceptatiecriteria:

* \[ ] Error reports are redacted.
* \[ ] Frontend can submit local error report.
* \[ ] Backend never prints secrets.
* \[ ] Reports link to troubleshooting docs.
* \[ ] Tests cover secret-like exception message.

\---

## 14\. Fase 11 - Dashboard V2 Logs Panel

Frontend page/panel:

```text
/system/logs
```

Features:

* \[ ] backend status;
* \[ ] recent dashboard-v2 errors;
* \[ ] WebSocket connection history;
* \[ ] API latency summary;
* \[ ] frontend error boundary events;
* \[ ] static build info;
* \[ ] launcher info;
* \[ ] no-live proof;
* \[ ] support bundle export link.

Guardrails:

* \[ ] no raw secrets;
* \[ ] local-only;
* \[ ] copy report button;
* \[ ] clear local frontend logs button confirm-gated.

Acceptatiecriteria:

* \[ ] Operator can see why dashboard failed.
* \[ ] Logs are redacted.
* \[ ] Error report can be exported.
* \[ ] Browser smoke covers logs panel.
* \[ ] Support bundle includes dashboard-v2 logs.

\---

## 15\. Fase 12 - Dashboard V2 Support Bundle Integration

Uitbreid support bundle:

* \[ ] dashboard-v2 build manifest;
* \[ ] dashboard-v2 launcher session;
* \[ ] dashboard-v2 performance report;
* \[ ] dashboard-v2 error reports;
* \[ ] dashboard-v2 route list;
* \[ ] dashboard-v2 no-live proof;
* \[ ] dashboard-v2 browser smoke output;
* \[ ] dashboard-v2 API smoke output.

Acceptatiecriteria:

* \[ ] Support bundle includes V2 diagnostics.
* \[ ] Support bundle verify checks V2 artifacts.
* \[ ] Redaction self-test covers V2 files.
* \[ ] Missing optional artifacts are warnings.
* \[ ] Tests use fixture support bundle.

\---

## 16\. Fase 13 - Browser Smoke Reliability Matrix

Nieuwe smoke matrix:

```text
tests/browser/dashboard\_v2/
```

Critical routes:

* \[ ] `/`
* \[ ] `/demo-spot-trading`
* \[ ] `/bot-controls`
* \[ ] `/market-data`
* \[ ] `/orders-account`
* \[ ] `/sessions`
* \[ ] `/readiness`
* \[ ] `/logs-security`
* \[ ] `/support`
* \[ ] `/evidence`
* \[ ] `/system/logs`

Checks:

* \[ ] no-live banner visible;
* \[ ] route loads;
* \[ ] no console fatal error;
* \[ ] WebSocket status visible;
* \[ ] key metric visible;
* \[ ] safe action buttons disabled/enabled correctly;
* \[ ] no live option in any mode dropdown.

Acceptatiecriteria:

* \[ ] Matrix can run in fast mode.
* \[ ] Matrix can run in deep mode.
* \[ ] Failures produce screenshots/traces if enabled.
* \[ ] No-live missing is hard fail.
* \[ ] Reports are secret-free.

\---

## 17\. Fase 14 - Streamlit Legacy/Fallback Mode

Doel: geen plotselinge breuk.

Nieuwe docs:

```text
docs/dashboard-v2/streamlit-legacy-fallback.md
```

CLI behavior:

* \[ ] `dashboard` blijft Streamlit of keuze-menu.
* \[ ] `dashboard-v2` start V2.
* \[ ] `dashboard --legacy-streamlit` forceert Streamlit.
* \[ ] `dashboard --v2` forceert V2.
* \[ ] README legt keuze uit.

UI/CLI waarschuwingen:

* \[ ] Streamlit toont legacy/fallback badge.
* \[ ] Dashboard V2 toont recommended/preview/ready status afhankelijk gate.
* \[ ] Fallback instructie zichtbaar als V2 faalt.
* \[ ] No-live statement in beide dashboards.

Acceptatiecriteria:

* \[ ] Streamlit fallback blijft werken.
* \[ ] Dashboard V2 failure suggests fallback.
* \[ ] No breaking CLI changes.
* \[ ] Tests cover command selection.
* \[ ] Docs explain fallback.

\---

## 18\. Fase 15 - Cutover Readiness Score

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/cutover\_readiness.py
```

Scorecategorieën:

* \[ ] feature parity;
* \[ ] API smoke;
* \[ ] browser smoke;
* \[ ] performance budgets;
* \[ ] WebSocket stability;
* \[ ] static build/offline assets;
* \[ ] support bundle integration;
* \[ ] operator/UAT acceptance;
* \[ ] Streamlit fallback available;
* \[ ] no-live proof.

Grades:

* \[ ] A: V2 recommended;
* \[ ] B: V2 recommended with warnings;
* \[ ] C: V2 preview only;
* \[ ] D: V2 blocked;
* \[ ] F: V2 unsafe/failing.

Hard blockers:

* \[ ] live mode found;
* \[ ] no-live banner missing;
* \[ ] API smoke failed;
* \[ ] browser smoke failed on overview;
* \[ ] static build missing for release package;
* \[ ] WebSocket cannot connect;
* \[ ] support bundle leaks secret;
* \[ ] Streamlit fallback broken before cutover.

Acceptatiecriteria:

* \[ ] Score is explainable.
* \[ ] Hard blockers force D/F.
* \[ ] Report is Markdown + JSON.
* \[ ] Dashboard shows score.
* \[ ] Check-all deep profile can require B or higher.

\---

## 19\. Fase 16 - Dashboard V2 Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/evidence\_bundle.py
```

Bundle bevat:

* \[ ] dashboard-v2 safety contract;
* \[ ] performance baseline;
* \[ ] performance budget report;
* \[ ] payload profile report;
* \[ ] WebSocket stability report;
* \[ ] static build manifest;
* \[ ] launcher report;
* \[ ] browser smoke report;
* \[ ] API smoke report;
* \[ ] support bundle integration report;
* \[ ] cutover readiness report;
* \[ ] Streamlit fallback verification;
* \[ ] no-live proof;
* \[ ] hashes.

Output:

```text
data/dashboard-v2/evidence/<run\_id>/
  dashboard\_v2\_evidence\_manifest.json
  dashboard\_v2\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle is included in operator support bundle.
* \[ ] Dashboard can download bundle.

\---

## 20\. Fase 17 - Check-All / Deep Profile Integration

Uitbreid check-all:

* \[ ] dashboard-v2 import smoke;
* \[ ] dashboard-v2 API smoke;
* \[ ] dashboard-v2 no-live proof;
* \[ ] dashboard-v2 static build verify if build exists;
* \[ ] dashboard-v2 performance budget in deep profile;
* \[ ] dashboard-v2 browser smoke in deep profile;
* \[ ] cutover readiness in deep profile;
* \[ ] Streamlit fallback verify.

Acceptatiecriteria:

* \[ ] Normal check-all blijft snel.
* \[ ] Deep profile dekt Dashboard V2 grondig.
* \[ ] No-live failure is hard fail.
* \[ ] Optional frontend build missing is clear warning unless cutover profile.
* \[ ] Reports are secret-free.

\---

## 21\. Fase 18 - Operator/UAT Acceptance

Roadmap 102/103 integratie:

* \[ ] Operator manual krijgt Dashboard V2 performance/launcher docs.
* \[ ] UAT scenario voor one-click local launch.
* \[ ] UAT scenario voor WebSocket reconnect.
* \[ ] UAT scenario voor support bundle V2 diagnostics.
* \[ ] UAT scenario voor Streamlit fallback.
* \[ ] UAT scenario voor no-live proof in V2.
* \[ ] Usability scorecard bevat Dashboard V2 launch friction.
* \[ ] Feedback backlog kan Dashboard V2 performance issues aanmaken.

Acceptatiecriteria:

* \[ ] UAT can validate Dashboard V2 cutover.
* \[ ] Operator docs explain fallback.
* \[ ] UAT feedback enters backlog.
* \[ ] Cutover readiness requires UAT result if configured.
* \[ ] No-live proof preserved.

\---

## 22\. Fase 19 - Release \& Packaging Readiness

Release items:

* \[ ] include static frontend build in package;
* \[ ] include dashboard-v2 optional dependency instructions;
* \[ ] version manifest includes frontend build hash;
* \[ ] release notes mention Dashboard V2 status;
* \[ ] migration note: Streamlit fallback remains;
* \[ ] support bundle includes V2 diagnostics;
* \[ ] cutover readiness report attached to release evidence;
* \[ ] rollback instructions documented.

Acceptatiecriteria:

* \[ ] Release simulation includes Dashboard V2.
* \[ ] Package check verifies static files.
* \[ ] Version payload includes dashboard-v2 status.
* \[ ] Release evidence includes no-live proof.
* \[ ] No Streamlit removal yet.

\---

## 23\. Fase 20 - Knowledge/Test/Performance Integration

Roadmap 091:

* \[ ] Knowledge graph maps dashboard-v2 frontend routes to backend API routes.
* \[ ] Impact analysis detects frontend/backend/dashboard-v2 changes.
* \[ ] Ownership map includes V2 backend/frontend.

Roadmap 092:

* \[ ] Test selector chooses API smoke for backend changes.
* \[ ] Test selector chooses frontend/browser tests for frontend changes.
* \[ ] Test selector chooses cutover readiness for launcher/static changes.

Roadmap 093:

* \[ ] Performance reports include Dashboard V2.
* \[ ] Budgets tracked over time.
* \[ ] Slow chart/render issues become findings.

Roadmap 100/101:

* \[ ] Paper OS milestone includes Dashboard V2 readiness.
* \[ ] Stabilization backlog can import Dashboard V2 findings.
* \[ ] P0 no-live Dashboard V2 issues block readiness.

Acceptatiecriteria:

* \[ ] Dashboard V2 impact analysis works.
* \[ ] Test selection works.
* \[ ] Performance trends stored.
* \[ ] Milestone/stabilization reports include V2.
* \[ ] No-live proof preserved.

\---

## 24\. Fase 21 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli dashboard-v2-performance-baseline --json
python -m binance\_spot\_bot.cli dashboard-v2-performance-budget --json
python -m binance\_spot\_bot.cli dashboard-v2-payload-profile-report --json
python -m binance\_spot\_bot.cli dashboard-v2-ws-stability-smoke --json
python -m binance\_spot\_bot.cli dashboard-v2-static-verify --json
python -m binance\_spot\_bot.cli dashboard-v2-launcher-report --json
python -m binance\_spot\_bot.cli dashboard-v2-create-shortcut
python -m binance\_spot\_bot.cli dashboard-v2-error-report --json
python -m binance\_spot\_bot.cli dashboard-v2-support-diagnostics --json
python -m binance\_spot\_bot.cli dashboard-v2-browser-smoke-matrix --json
python -m binance\_spot\_bot.cli dashboard-v2-cutover-readiness --json
python -m binance\_spot\_bot.cli dashboard-v2-evidence-export
python -m binance\_spot\_bot.cli dashboard --legacy-streamlit
python -m binance\_spot\_bot.cli dashboard --v2
```

Acceptatiecriteria:

* \[ ] Commands werken offline.
* \[ ] Commands ondersteunen JSON waar relevant.
* \[ ] Commands gebruiken safe env.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Reports zijn secret-free.

\---

## 25\. Fase 22 - Tests

### Unit tests

* \[ ] `tests/test\_dashboard\_v2\_cutover\_safety\_contract.py`
* \[ ] `tests/test\_dashboard\_v2\_performance\_baseline.py`
* \[ ] `tests/test\_dashboard\_v2\_performance\_budgets.py`
* \[ ] `tests/test\_dashboard\_v2\_payload\_profiles.py`
* \[ ] `tests/test\_dashboard\_v2\_ws\_stability.py`
* \[ ] `tests/test\_dashboard\_v2\_static\_build.py`
* \[ ] `tests/test\_dashboard\_v2\_launcher.py`
* \[ ] `tests/test\_dashboard\_v2\_desktop\_shortcut.py`
* \[ ] `tests/test\_dashboard\_v2\_error\_reports.py`
* \[ ] `tests/test\_dashboard\_v2\_support\_bundle.py`
* \[ ] `tests/test\_dashboard\_v2\_cutover\_readiness.py`
* \[ ] `tests/test\_dashboard\_v2\_evidence\_bundle.py`

### Frontend tests

* \[ ] state slices;
* \[ ] reducer diff application;
* \[ ] reconnect state;
* \[ ] stale data badge;
* \[ ] chart tail trimming;
* \[ ] route lazy loading;
* \[ ] no-live banner;
* \[ ] fallback message;
* \[ ] error boundary.

### Integration tests

* \[ ] static build verification fixture;
* \[ ] launcher smoke with fake server;
* \[ ] WebSocket reconnect smoke;
* \[ ] API payload profile smoke;
* \[ ] browser smoke matrix fixture;
* \[ ] cutover readiness pass/fail fixture;
* \[ ] support bundle V2 diagnostics fixture;
* \[ ] evidence bundle export/verify.

### Safety tests

* \[ ] live mode blocked.
* \[ ] live route absent.
* \[ ] external CDN absent.
* \[ ] localhost default.
* \[ ] secrets redacted from error reports.
* \[ ] support bundle V2 artifacts secret-free.
* \[ ] Streamlit fallback exists.
* \[ ] no-live banner visible.
* \[ ] no signed/order/account endpoint routes.
* \[ ] safe env preserved.

\---

## 26\. Fase 23 - Docs

Nieuwe docs:

```text
docs/dashboard-v2/performance-baseline.md
docs/dashboard-v2/performance-budgets.md
docs/dashboard-v2/payload-profiles.md
docs/dashboard-v2/websocket-stability.md
docs/dashboard-v2/static-build-offline-assets.md
docs/dashboard-v2/local-launcher.md
docs/dashboard-v2/windows-shortcut.md
docs/dashboard-v2/error-reports.md
docs/dashboard-v2/logs-panel.md
docs/dashboard-v2/support-bundle-integration.md
docs/dashboard-v2/browser-smoke-matrix.md
docs/dashboard-v2/streamlit-legacy-fallback.md
docs/dashboard-v2/cutover-readiness.md
docs/dashboard-v2/evidence-bundle.md
docs/dashboard-v2/release-packaging.md
```

README updates:

* \[ ] Dashboard V2 recommended/preview status.
* \[ ] How to install `\[dashboard-v2]`.
* \[ ] How to launch.
* \[ ] How to create shortcut.
* \[ ] How to run smoke.
* \[ ] How to use Streamlit fallback.
* \[ ] No-live statement.

Acceptatiecriteria:

* \[ ] Docs are linked from operator manual.
* \[ ] Docs mention no-live proof.
* \[ ] Docs contain no live approval language.
* \[ ] Docs consistency tests pass.
* \[ ] UAT scenario links are valid.

\---

## 27\. Codex bouwvolgorde

### PR 1 - Cutover Safety Contract + Performance Baseline

* \[ ] `docs/dashboard-v2-cutover-safety-contract.md`
* \[ ] `dashboard\_v2/performance\_baseline.py`
* \[ ] baseline tests.
* \[ ] no-live tests.

### PR 2 - Performance Budgets + Payload Profiles

* \[ ] `dashboard\_v2/performance\_budgets.py`
* \[ ] `dashboard\_v2/payload\_profiles.py`
* \[ ] payload trimming tests.

### PR 3 - WebSocket Stability

* \[ ] `dashboard\_v2/ws\_stability.py`
* \[ ] reconnect/replay/backpressure tests.
* \[ ] frontend reconnect state.

### PR 4 - Frontend State \& Chart Optimization

* \[ ] state slices.
* \[ ] chart append/tail/downsampling.
* \[ ] lazy routes.
* \[ ] frontend tests.

### PR 5 - Static Build \& Offline Assets

* \[ ] `dashboard\_v2/static\_build.py`
* \[ ] build manifest.
* \[ ] no-CDN verification.

### PR 6 - Launcher \& Desktop Shortcut

* \[ ] `dashboard\_v2/launcher.py`
* \[ ] `dashboard\_v2/desktop\_shortcut.py`
* \[ ] launcher/shortcut tests.

### PR 7 - Error Reports \& Logs Panel

* \[ ] `dashboard\_v2/error\_reports.py`
* \[ ] frontend error boundary submit.
* \[ ] logs panel.
* \[ ] redaction tests.

### PR 8 - Support Bundle + Browser Smoke Matrix

* \[ ] support bundle V2 integration.
* \[ ] browser smoke matrix.
* \[ ] screenshot/report artifacts.

### PR 9 - Cutover Readiness + Evidence Bundle

* \[ ] `dashboard\_v2/cutover\_readiness.py`
* \[ ] `dashboard\_v2/evidence\_bundle.py`
* \[ ] score/gate tests.

### PR 10 - Check-All, Docs, UAT \& Release Integration

* \[ ] check-all integration.
* \[ ] operator/UAT docs.
* \[ ] release/knowledge/test/performance integration.
* \[ ] README update.

\---

## 28\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 106 PR 1: Dashboard V2 Cutover Safety Contract + Performance Baseline.

Maak docs/dashboard-v2-cutover-safety-contract.md.

Maak src/binance\_spot\_bot/dashboard\_v2/performance\_baseline.py met:
- DashboardV2PerformanceSample
- DashboardV2PerformanceBaseline
- DashboardV2PerformanceReport
- measure\_dashboard\_v2\_baseline(...)
- dashboard\_v2\_performance\_report\_to\_dict(...)
- write\_dashboard\_v2\_performance\_report(...)

De baseline moet minimaal kunnen meten of accepteren als input:
- backend\_startup\_ms
- api\_health\_ms
- api\_config\_ms
- api\_pages\_ms
- api\_snapshot\_ms
- websocket\_connect\_ms
- websocket\_heartbeat\_ms
- snapshot\_serialization\_ms
- snapshot\_payload\_bytes
- frontend\_initial\_load\_ms
- route\_navigation\_ms
- chart\_update\_ms
- browser\_console\_errors
- live\_trading\_enabled=False
- no\_live\_statement

Gebruik alleen stdlib voor deze PR.
Geen echte server starten in unit tests; gebruik injectable measurement functions/fake samples.
Geen frontend build verplicht.
Geen runtime execution.
Geen Streamlit wijzigen.
Geen GitHub API calls.
Geen signed endpoints.
Geen account/order endpoints.
Geen live trading.

Voeg tests toe voor:
- baseline report JSON serialization
- no\_live\_statement aanwezig
- live\_trading\_enabled=False
- secret-like values worden geredact
- missing optional sample wordt warning
- browser\_console\_errors worden opgenomen
- write report naar temp dir
```

Waarom eerst:

* Cutover naar Dashboard V2 mag pas als performance meetbaar is.
* Dit raakt runtime/execution/frontend nog niet.
* Het is klein genoeg voor Codex.
* No-live en secret-free reporting kunnen meteen getest worden.
* Daarna kunnen performance budgets, WebSocket stability en launcher hardening veilig volgen.

\---

## 29\. Definition of Done

Roadmap 106 is klaar als:

* \[ ] Dashboard V2 Cutover Safety Contract bestaat.
* \[ ] Performance baseline werkt.
* \[ ] Performance budgets werken.
* \[ ] Payload profiles werken.
* \[ ] WebSocket stability/reconnect werkt.
* \[ ] Frontend state/render optimization werkt.
* \[ ] Realtime charts geoptimaliseerd zijn.
* \[ ] Static frontend build/offline assets werken.
* \[ ] Local launcher UX werkt.
* \[ ] Desktop shortcut helper werkt.
* \[ ] Local crash/error reports werken.
* \[ ] Dashboard V2 logs panel werkt.
* \[ ] Support bundle V2 integration werkt.
* \[ ] Browser smoke reliability matrix werkt.
* \[ ] Streamlit legacy/fallback mode werkt.
* \[ ] Cutover readiness score werkt.
* \[ ] Dashboard V2 evidence bundle werkt.
* \[ ] Check-all/deep profile integration werkt.
* \[ ] Operator/UAT acceptance werkt.
* \[ ] Release/packaging readiness werkt.
* \[ ] Knowledge/test/performance integration werkt.
* \[ ] CLI commands werken.
* \[ ] Docs bestaan.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen localhost default.
* \[ ] Tests bewijzen frontend assets offline zijn.
* \[ ] Tests bewijzen error/support/evidence secret-free zijn.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Streamlit fallback blijft beschikbaar.
* \[ ] Dashboard V2 heeft cutover readiness A/B.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 106 kan na uitvoering naar `Voltooid docs`.

\---

## 30\. Verwachte Roadmap 107 daarna

Na Roadmap 106 is de meest logische opvolger:

```text
Roadmap 107 - Dashboard V2 Operator Workflow Simplification, UX Backlog Execution \& Streamlit Deprecation Plan
```

Mogelijke inhoud:

* \[ ] UAT-feedback uit Roadmap 103 verwerken;
* \[ ] Dashboard V2 flows vereenvoudigen;
* \[ ] onboarding wizard voor Dashboard V2;
* \[ ] betere command/action hints;
* \[ ] Streamlit deprecation timeline;
* \[ ] legacy page removal criteria;
* \[ ] V2-only docs;
* \[ ] still no live trading.

```

Alternatief als Roadmap 106 performanceproblemen vindt:

```text
Roadmap 107 - Dashboard V2 Performance Regression Burn-Down, Chart Virtualization \& WebSocket Load Testing
```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Dashboard V2 packaging, performance and rollback readiness.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.

