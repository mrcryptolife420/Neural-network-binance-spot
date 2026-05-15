# Roadmap 106 - Dashboard V2 Performance, Desktop Packaging \& Streamlit Cutover Readiness

Status: Voltooid  
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
* \[x] `cli.py` heeft al veel commands voor dashboard, smoke, paper sessions, support/evidence, demo execution en check-all. Dashboard V2 moet hier netjes in worden geÃ¯ntegreerd.
* \[x] `check\_all.py` forceert veilige env vars met `LIVE\_TRADING\_ENABLED=false` en `KILL\_SWITCH=true`; Dashboard V2 checks moeten dezelfde safety basis gebruiken.
* \[x] Runtime modes blijven beperkt tot `demo`, `paper` en `testnet-readiness`.
* \[x] Operator tooling heeft al evidence, redaction, local ops snapshot, command manifest en operator quality gate.

### Belangrijkste gat na Roadmap 105

Na Roadmap 105 heeft Dashboard V2 feature parity en migratiebasis, maar er blijven production-quality lokale UI zorgen:

* \[x] Is Dashboard V2 sneller dan Streamlit bij grote snapshots?
* \[x] Zijn WebSocket reconnects stabiel?
* \[x] Zijn chart updates performant bij veel candles/fills/signals?
* \[x] Is de frontend build offline en reproduceerbaar?
* \[x] Is er een simpele lokale launcher voor operators?
* \[x] Zijn logs, crashes en backend errors begrijpelijk?
* \[x] Kan Dashboard V2 zonder Node dev server draaien?
* \[x] Zijn API payloads begrensd en gemeten?
* \[x] Is er een cutover scorecard van Streamlit naar Dashboard V2?
* \[x] Kan Streamlit veilig legacy/fallback worden?
* \[x] Zijn browser smoke en API smoke voldoende betrouwbaar voor check-all?
* \[x] Is er een rollback/fallback plan als Dashboard V2 faalt?

Roadmap 106 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 106

Maak Dashboard V2 klaar als aanbevolen lokale operator UI:

```text
Dashboard V2 feature parity
â†’ performance budgets
â†’ WebSocket stability
â†’ static/offline frontend build
â†’ desktop/local launcher
â†’ smoke/reliability evidence
â†’ Streamlit legacy fallback
â†’ cutover readiness score
```

Na deze roadmap moet Dashboard V2:

* \[x] lokaal starten met Ã©Ã©n command;
* \[x] frontend static build serveren zonder Node dev server;
* \[x] realtime updates tonen zonder full page rerun;
* \[x] WebSocket reconnects betrouwbaar afhandelen;
* \[x] API payloads begrenzen en meten;
* \[x] charts snel houden bij grotere datasets;
* \[x] browser smoke stabiel doorstaan;
* \[x] logs/crashes/operator errors begrijpelijk tonen;
* \[x] Streamlit legacy/fallback status duidelijk tonen;
* \[x] no-live proof altijd tonen;
* \[x] check-all/deep profile integratie hebben;
* \[x] een cutover readiness score halen.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[x] Geen nieuwe trading runtime.
* \[x] Geen nieuwe modeltraining pipeline.
* \[x] Geen nieuwe data pipeline.
* \[x] Geen Dashboard V2 foundation opnieuw bouwen; Roadmap 104 doet dat.
* \[x] Geen page feature parity opnieuw plannen; Roadmap 105 doet dat.
* \[x] Geen Streamlit direct verwijderen.
* \[x] Geen live trading.
* \[x] Geen live mode.
* \[x] Geen signed real-order endpoints.
* \[x] Geen echte account workflows.
* \[x] Geen cloud deployment.
* \[x] Geen remote telemetry.
* \[x] Geen externe frontend CDN.
* \[x] Geen auto-updater die code downloadt.
* \[x] Geen desktop app die firewall/remote access opent.

Wel doen:

* \[x] Dashboard V2 performance hardening;
* \[x] WebSocket reconnect/stability;
* \[x] frontend production build pipeline;
* \[x] local launcher/desktop shortcut;
* \[x] crash/error reporting local-only;
* \[x] API payload budgets;
* \[x] browser smoke reliability;
* \[x] Streamlit legacy fallback;
* \[x] cutover readiness evidence.

\---

## 3\. Fase 0 - Dashboard V2 Cutover Safety Contract

Nieuw docbestand:

```text
docs/dashboard-v2-cutover-safety-contract.md
```

Regels:

* \[x] Dashboard V2 cutover is local-only.
* \[x] Geen live trading.
* \[x] Geen live mode in frontend/backend/CLI.
* \[x] Alleen `demo`, `paper`, `testnet-readiness`.
* \[x] Streamlit blijft fallback tot cutover gate pass.
* \[x] Dashboard V2 launcher bindt default alleen op `127.0.0.1`.
* \[x] Geen remote telemetry.
* \[x] Geen externe CDN.
* \[x] Geen raw secrets in API/WebSocket/frontend logs.
* \[x] Geen signed real-order endpoints.
* \[x] Geen echte account workflows.
* \[x] Local crash reports worden geredact.
* \[x] Cutover readiness vereist no-live proof.
* \[x] Rollback naar Streamlit fallback moet gedocumenteerd zijn.
* \[x] Operator moet kunnen zien welk dashboard actief is.

Acceptatiecriteria:

* \[x] Safety contract bestaat.
* \[x] Tests bewijzen live mode niet in Dashboard V2 cutover config zit.
* \[x] Tests bewijzen launcher default localhost is.
* \[x] Tests bewijzen crash reports secret-free zijn.
* \[x] Tests bewijzen Streamlit fallback niet verwijderd is.

\---

## 4\. Fase 1 - Dashboard V2 Performance Baseline

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/performance\_baseline.py
```

Doel: meetbare baseline maken vÃ³Ã³r optimalisaties.

Te meten:

* \[x] backend startup time;
* \[x] `/api/health` latency;
* \[x] `/api/config` latency;
* \[x] `/api/pages` latency;
* \[x] `/api/runtime/snapshot` latency;
* \[x] WebSocket connect latency;
* \[x] WebSocket heartbeat interval stability;
* \[x] snapshot serialization duration;
* \[x] payload bytes per endpoint;
* \[x] frontend initial load time;
* \[x] route navigation time;
* \[x] chart render/update time;
* \[x] memory best-effort;
* \[x] CPU best-effort;
* \[x] browser console errors.

Output:

```text
data/dashboard-v2/performance/
  baseline.json
  baseline.md
```

Acceptatiecriteria:

* \[x] Baseline kan offline draaien.
* \[x] Baseline heeft JSON + Markdown output.
* \[x] Baseline bevat no-live proof.
* \[x] Baseline is secret-free.
* \[x] Tests gebruiken fake timings/payloads.

\---

## 5\. Fase 2 - Dashboard V2 Performance Budgets

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/performance\_budgets.py
```

Budgetten:

* \[x] backend startup max ms;
* \[x] health/config/pages endpoint max ms;
* \[x] snapshot endpoint max ms;
* \[x] snapshot max bytes;
* \[x] WebSocket connect max ms;
* \[x] WebSocket event max bytes;
* \[x] frontend initial load max ms;
* \[x] route switch max ms;
* \[x] chart update max ms;
* \[x] max frontend JS bundle bytes warning;
* \[x] max static asset count;
* \[x] max browser console fatal errors;
* \[x] max reconnect failure count.

Budget statuses:

* \[x] pass;
* \[x] warn;
* \[x] fail;
* \[x] skipped;
* \[x] unknown.

Acceptatiecriteria:

* \[x] Budget evaluator werkt op baseline report.
* \[x] Hard fail bij no-live proof missing.
* \[x] Snapshot payload oversize wordt fail/warn volgens policy.
* \[x] Markdown report met aanbevelingen.
* \[x] Check-all kan budget evaluator draaien.

\---

## 6\. Fase 3 - API Payload Slimming \& Snapshot Profiles

Uitbreiding op Dashboard V2 backend:

```text
src/binance\_spot\_bot/dashboard\_v2/payload\_profiles.py
```

Profiles:

* \[x] `header`
* \[x] `overview`
* \[x] `chart`
* \[x] `orders`
* \[x] `sessions`
* \[x] `evidence`
* \[x] `debug`
* \[x] `full`

Regels:

* \[x] Frontend vraagt niet altijd full snapshot.
* \[x] Header gebruikt compact summary.
* \[x] Charts gebruiken chart payload met limits.
* \[x] Sessions/evidence lazy loaded.
* \[x] Debug JSON alleen op expliciete vraag.
* \[x] Payload stats teruggeven in response metadata.
* \[x] Trimmed counts zichtbaar maken.

Acceptatiecriteria:

* \[x] `/api/runtime/snapshot?profile=overview` werkt.
* \[x] `/api/runtime/snapshot?profile=chart` werkt.
* \[x] Full profile blijft beschikbaar voor debug.
* \[x] Payload size daalt voor overview.
* \[x] Tests dekken trimming en redaction.

\---

## 7\. Fase 4 - WebSocket Stability \& Reconnect

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/ws\_stability.py
```

Backend:

* \[x] heartbeat events;
* \[x] client id;
* \[x] reconnect token optional local-only;
* \[x] last event id;
* \[x] replay latest buffered events;
* \[x] disconnect cleanup;
* \[x] max clients;
* \[x] stale client cleanup;
* \[x] backpressure/drop policy;
* \[x] event size guard.

Frontend:

* \[x] exponential reconnect;
* \[x] visible connection status;
* \[x] stale data badge;
* \[x] missed event counter;
* \[x] manual reconnect;
* \[x] fallback REST refresh;
* \[x] no duplicate event application.

Acceptatiecriteria:

* \[x] Reconnect test passes.
* \[x] Duplicate events are ignored or idempotent.
* \[x] Lost connection shows UI warning.
* \[x] REST fallback works.
* \[x] Tests cover disconnect/reconnect/replay.

\---

## 8\. Fase 5 - Frontend State \& Render Optimization

Frontend tasks:

* \[x] split global state into slices:

  * runtime;
  * charts;
  * orders;
  * sessions;
  * evidence;
  * operator;
  * settings.
* \[x] memoize heavy chart components;
* \[x] virtualize large tables;
* \[x] lazy-load advanced pages;
* \[x] route-level code splitting;
* \[x] avoid full app state replacement;
* \[x] diff incoming event payloads;
* \[x] cap chart data points;
* \[x] cap table rows;
* \[x] add render counter in debug mode;
* \[x] add slow render warning.

Acceptatiecriteria:

* \[x] Overview updates do not rerender all pages.
* \[x] Heavy pages lazy load.
* \[x] Large tables do not freeze UI.
* \[x] Debug render stats visible.
* \[x] Frontend tests cover reducers/selectors.

\---

## 9\. Fase 6 - Realtime Chart Optimization

Frontend chart improvements:

* \[x] append candle updates instead of replacing all data.
* \[x] append equity points.
* \[x] update signal markers incrementally.
* \[x] update fill markers incrementally.
* \[x] use fixed max point window.
* \[x] use downsampling for long histories.
* \[x] separate live view vs history view.
* \[x] pause chart updates toggle.
* \[x] chart error boundary.
* \[x] chart performance telemetry.

Backend chart API:

```text
GET /api/charts/candles?tail=500
GET /api/charts/equity?tail=500
GET /api/charts/signals?tail=200
GET /api/charts/fills?tail=200
```

Acceptatiecriteria:

* \[x] Chart updates feel instant.
* \[x] No full chart rebuild for every event where possible.
* \[x] Tail limits enforced backend/frontend.
* \[x] Chart pause works.
* \[x] Browser smoke covers chart update.

\---

## 10\. Fase 7 - Static Frontend Build \& Offline Assets

Frontend build tasks:

* \[x] `npm run build`;
* \[x] static assets output to package static dir;
* \[x] asset manifest generated;
* \[x] no external CDN links;
* \[x] no remote fonts;
* \[x] cache busting via hashed filenames;
* \[x] build metadata JSON;
* \[x] frontend version shown in UI;
* \[x] backend validates static build exists;
* \[x] static build verification command.

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/static\_build.py
```

Acceptatiecriteria:

* \[x] Static build can be served by backend.
* \[x] Static build has manifest.
* \[x] No external URLs required.
* \[x] Missing build gives clear operator error.
* \[x] Tests verify manifest and no external CDN.

\---

## 11\. Fase 8 - Local Launcher UX

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/launcher.py
```

Launcher features:

* \[x] `dashboard-v2` command opens browser by default.
* \[x] `--no-browser`.
* \[x] `--host 127.0.0.1`.
* \[x] `--port 8800`.
* \[x] `--find-free-port`.
* \[x] startup health wait.
* \[x] browser open after healthy.
* \[x] print local URL.
* \[x] print no-live statement.
* \[x] write launcher session file.
* \[x] graceful shutdown.
* \[x] useful error if dependencies missing.
* \[x] useful error if frontend build missing.

Acceptatiecriteria:

* \[x] One command starts local UI.
* \[x] Default host is localhost.
* \[x] Live trading disabled shown in console.
* \[x] Launcher session file written.
* \[x] Tests use fake server/bind.

\---

## 12\. Fase 9 - Desktop Shortcut / Windows Local App Helper

Geen Electron verplicht. Simpel en lokaal:

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/desktop\_shortcut.py
```

Windows helper:

* \[x] generate `.cmd` launcher;
* \[x] generate PowerShell launcher;
* \[x] optional Desktop shortcut instructions;
* \[x] check Python path;
* \[x] check venv path if available;
* \[x] check project root;
* \[x] run `dashboard-v2 --find-free-port`;
* \[x] no-live statement in launcher.
* \[x] safe uninstall shortcut instructions.

Commands:

```powershell
python -m binance\_spot\_bot.cli dashboard-v2-create-shortcut
python -m binance\_spot\_bot.cli dashboard-v2-shortcut-info
```

Acceptatiecriteria:

* \[x] Shortcut generation is optional.
* \[x] No admin privileges required.
* \[x] Generated script contains no secrets.
* \[x] Script uses localhost.
* \[x] Tests validate generated script content.

\---

## 13\. Fase 10 - Local Crash \& Error Reports

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/error\_reports.py
```

Report captures:

* \[x] backend exception summary;
* \[x] route/action context;
* \[x] redacted stack trace;
* \[x] frontend error boundary report;
* \[x] WebSocket disconnect summary;
* \[x] startup failure;
* \[x] static build missing;
* \[x] dependency missing;
* \[x] no-live proof;
* \[x] suggested playbook.

Storage:

```text
data/dashboard-v2/errors/
```

Acceptatiecriteria:

* \[x] Error reports are redacted.
* \[x] Frontend can submit local error report.
* \[x] Backend never prints secrets.
* \[x] Reports link to troubleshooting docs.
* \[x] Tests cover secret-like exception message.

\---

## 14\. Fase 11 - Dashboard V2 Logs Panel

Frontend page/panel:

```text
/system/logs
```

Features:

* \[x] backend status;
* \[x] recent dashboard-v2 errors;
* \[x] WebSocket connection history;
* \[x] API latency summary;
* \[x] frontend error boundary events;
* \[x] static build info;
* \[x] launcher info;
* \[x] no-live proof;
* \[x] support bundle export link.

Guardrails:

* \[x] no raw secrets;
* \[x] local-only;
* \[x] copy report button;
* \[x] clear local frontend logs button confirm-gated.

Acceptatiecriteria:

* \[x] Operator can see why dashboard failed.
* \[x] Logs are redacted.
* \[x] Error report can be exported.
* \[x] Browser smoke covers logs panel.
* \[x] Support bundle includes dashboard-v2 logs.

\---

## 15\. Fase 12 - Dashboard V2 Support Bundle Integration

Uitbreid support bundle:

* \[x] dashboard-v2 build manifest;
* \[x] dashboard-v2 launcher session;
* \[x] dashboard-v2 performance report;
* \[x] dashboard-v2 error reports;
* \[x] dashboard-v2 route list;
* \[x] dashboard-v2 no-live proof;
* \[x] dashboard-v2 browser smoke output;
* \[x] dashboard-v2 API smoke output.

Acceptatiecriteria:

* \[x] Support bundle includes V2 diagnostics.
* \[x] Support bundle verify checks V2 artifacts.
* \[x] Redaction self-test covers V2 files.
* \[x] Missing optional artifacts are warnings.
* \[x] Tests use fixture support bundle.

\---

## 16\. Fase 13 - Browser Smoke Reliability Matrix

Nieuwe smoke matrix:

```text
tests/browser/dashboard\_v2/
```

Critical routes:

* \[x] `/`
* \[x] `/demo-spot-trading`
* \[x] `/bot-controls`
* \[x] `/market-data`
* \[x] `/orders-account`
* \[x] `/sessions`
* \[x] `/readiness`
* \[x] `/logs-security`
* \[x] `/support`
* \[x] `/evidence`
* \[x] `/system/logs`

Checks:

* \[x] no-live banner visible;
* \[x] route loads;
* \[x] no console fatal error;
* \[x] WebSocket status visible;
* \[x] key metric visible;
* \[x] safe action buttons disabled/enabled correctly;
* \[x] no live option in any mode dropdown.

Acceptatiecriteria:

* \[x] Matrix can run in fast mode.
* \[x] Matrix can run in deep mode.
* \[x] Failures produce screenshots/traces if enabled.
* \[x] No-live missing is hard fail.
* \[x] Reports are secret-free.

\---

## 17\. Fase 14 - Streamlit Legacy/Fallback Mode

Doel: geen plotselinge breuk.

Nieuwe docs:

```text
docs/dashboard-v2/streamlit-legacy-fallback.md
```

CLI behavior:

* \[x] `dashboard` blijft Streamlit of keuze-menu.
* \[x] `dashboard-v2` start V2.
* \[x] `dashboard --legacy-streamlit` forceert Streamlit.
* \[x] `dashboard --v2` forceert V2.
* \[x] README legt keuze uit.

UI/CLI waarschuwingen:

* \[x] Streamlit toont legacy/fallback badge.
* \[x] Dashboard V2 toont recommended/preview/ready status afhankelijk gate.
* \[x] Fallback instructie zichtbaar als V2 faalt.
* \[x] No-live statement in beide dashboards.

Acceptatiecriteria:

* \[x] Streamlit fallback blijft werken.
* \[x] Dashboard V2 failure suggests fallback.
* \[x] No breaking CLI changes.
* \[x] Tests cover command selection.
* \[x] Docs explain fallback.

\---

## 18\. Fase 15 - Cutover Readiness Score

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/cutover\_readiness.py
```

ScorecategorieÃ«n:

* \[x] feature parity;
* \[x] API smoke;
* \[x] browser smoke;
* \[x] performance budgets;
* \[x] WebSocket stability;
* \[x] static build/offline assets;
* \[x] support bundle integration;
* \[x] operator/UAT acceptance;
* \[x] Streamlit fallback available;
* \[x] no-live proof.

Grades:

* \[x] A: V2 recommended;
* \[x] B: V2 recommended with warnings;
* \[x] C: V2 preview only;
* \[x] D: V2 blocked;
* \[x] F: V2 unsafe/failing.

Hard blockers:

* \[x] live mode found;
* \[x] no-live banner missing;
* \[x] API smoke failed;
* \[x] browser smoke failed on overview;
* \[x] static build missing for release package;
* \[x] WebSocket cannot connect;
* \[x] support bundle leaks secret;
* \[x] Streamlit fallback broken before cutover.

Acceptatiecriteria:

* \[x] Score is explainable.
* \[x] Hard blockers force D/F.
* \[x] Report is Markdown + JSON.
* \[x] Dashboard shows score.
* \[x] Check-all deep profile can require B or higher.

\---

## 19\. Fase 16 - Dashboard V2 Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/evidence\_bundle.py
```

Bundle bevat:

* \[x] dashboard-v2 safety contract;
* \[x] performance baseline;
* \[x] performance budget report;
* \[x] payload profile report;
* \[x] WebSocket stability report;
* \[x] static build manifest;
* \[x] launcher report;
* \[x] browser smoke report;
* \[x] API smoke report;
* \[x] support bundle integration report;
* \[x] cutover readiness report;
* \[x] Streamlit fallback verification;
* \[x] no-live proof;
* \[x] hashes.

Output:

```text
data/dashboard-v2/evidence/<run\_id>/
  dashboard\_v2\_evidence\_manifest.json
  dashboard\_v2\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[x] Bundle is secret-free.
* \[x] Bundle has manifest/hash.
* \[x] Bundle can be verified.
* \[x] Bundle is included in operator support bundle.
* \[x] Dashboard can download bundle.

\---

## 20\. Fase 17 - Check-All / Deep Profile Integration

Uitbreid check-all:

* \[x] dashboard-v2 import smoke;
* \[x] dashboard-v2 API smoke;
* \[x] dashboard-v2 no-live proof;
* \[x] dashboard-v2 static build verify if build exists;
* \[x] dashboard-v2 performance budget in deep profile;
* \[x] dashboard-v2 browser smoke in deep profile;
* \[x] cutover readiness in deep profile;
* \[x] Streamlit fallback verify.

Acceptatiecriteria:

* \[x] Normal check-all blijft snel.
* \[x] Deep profile dekt Dashboard V2 grondig.
* \[x] No-live failure is hard fail.
* \[x] Optional frontend build missing is clear warning unless cutover profile.
* \[x] Reports are secret-free.

\---

## 21\. Fase 18 - Operator/UAT Acceptance

Roadmap 102/103 integratie:

* \[x] Operator manual krijgt Dashboard V2 performance/launcher docs.
* \[x] UAT scenario voor one-click local launch.
* \[x] UAT scenario voor WebSocket reconnect.
* \[x] UAT scenario voor support bundle V2 diagnostics.
* \[x] UAT scenario voor Streamlit fallback.
* \[x] UAT scenario voor no-live proof in V2.
* \[x] Usability scorecard bevat Dashboard V2 launch friction.
* \[x] Feedback backlog kan Dashboard V2 performance issues aanmaken.

Acceptatiecriteria:

* \[x] UAT can validate Dashboard V2 cutover.
* \[x] Operator docs explain fallback.
* \[x] UAT feedback enters backlog.
* \[x] Cutover readiness requires UAT result if configured.
* \[x] No-live proof preserved.

\---

## 22\. Fase 19 - Release \& Packaging Readiness

Release items:

* \[x] include static frontend build in package;
* \[x] include dashboard-v2 optional dependency instructions;
* \[x] version manifest includes frontend build hash;
* \[x] release notes mention Dashboard V2 status;
* \[x] migration note: Streamlit fallback remains;
* \[x] support bundle includes V2 diagnostics;
* \[x] cutover readiness report attached to release evidence;
* \[x] rollback instructions documented.

Acceptatiecriteria:

* \[x] Release simulation includes Dashboard V2.
* \[x] Package check verifies static files.
* \[x] Version payload includes dashboard-v2 status.
* \[x] Release evidence includes no-live proof.
* \[x] No Streamlit removal yet.

\---

## 23\. Fase 20 - Knowledge/Test/Performance Integration

Roadmap 091:

* \[x] Knowledge graph maps dashboard-v2 frontend routes to backend API routes.
* \[x] Impact analysis detects frontend/backend/dashboard-v2 changes.
* \[x] Ownership map includes V2 backend/frontend.

Roadmap 092:

* \[x] Test selector chooses API smoke for backend changes.
* \[x] Test selector chooses frontend/browser tests for frontend changes.
* \[x] Test selector chooses cutover readiness for launcher/static changes.

Roadmap 093:

* \[x] Performance reports include Dashboard V2.
* \[x] Budgets tracked over time.
* \[x] Slow chart/render issues become findings.

Roadmap 100/101:

* \[x] Paper OS milestone includes Dashboard V2 readiness.
* \[x] Stabilization backlog can import Dashboard V2 findings.
* \[x] P0 no-live Dashboard V2 issues block readiness.

Acceptatiecriteria:

* \[x] Dashboard V2 impact analysis works.
* \[x] Test selection works.
* \[x] Performance trends stored.
* \[x] Milestone/stabilization reports include V2.
* \[x] No-live proof preserved.

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

* \[x] Commands werken offline.
* \[x] Commands ondersteunen JSON waar relevant.
* \[x] Commands gebruiken safe env.
* \[x] Commands gebruiken geen API keys.
* \[x] Commands gebruiken geen signed/order/account endpoints.
* \[x] Reports zijn secret-free.

\---

## 25\. Fase 22 - Tests

### Unit tests

* \[x] `tests/test\_dashboard\_v2\_cutover\_safety\_contract.py`
* \[x] `tests/test\_dashboard\_v2\_performance\_baseline.py`
* \[x] `tests/test\_dashboard\_v2\_performance\_budgets.py`
* \[x] `tests/test\_dashboard\_v2\_payload\_profiles.py`
* \[x] `tests/test\_dashboard\_v2\_ws\_stability.py`
* \[x] `tests/test\_dashboard\_v2\_static\_build.py`
* \[x] `tests/test\_dashboard\_v2\_launcher.py`
* \[x] `tests/test\_dashboard\_v2\_desktop\_shortcut.py`
* \[x] `tests/test\_dashboard\_v2\_error\_reports.py`
* \[x] `tests/test\_dashboard\_v2\_support\_bundle.py`
* \[x] `tests/test\_dashboard\_v2\_cutover\_readiness.py`
* \[x] `tests/test\_dashboard\_v2\_evidence\_bundle.py`

### Frontend tests

* \[x] state slices;
* \[x] reducer diff application;
* \[x] reconnect state;
* \[x] stale data badge;
* \[x] chart tail trimming;
* \[x] route lazy loading;
* \[x] no-live banner;
* \[x] fallback message;
* \[x] error boundary.

### Integration tests

* \[x] static build verification fixture;
* \[x] launcher smoke with fake server;
* \[x] WebSocket reconnect smoke;
* \[x] API payload profile smoke;
* \[x] browser smoke matrix fixture;
* \[x] cutover readiness pass/fail fixture;
* \[x] support bundle V2 diagnostics fixture;
* \[x] evidence bundle export/verify.

### Safety tests

* \[x] live mode blocked.
* \[x] live route absent.
* \[x] external CDN absent.
* \[x] localhost default.
* \[x] secrets redacted from error reports.
* \[x] support bundle V2 artifacts secret-free.
* \[x] Streamlit fallback exists.
* \[x] no-live banner visible.
* \[x] no signed/order/account endpoint routes.
* \[x] safe env preserved.

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

* \[x] Dashboard V2 recommended/preview status.
* \[x] How to install `\[dashboard-v2]`.
* \[x] How to launch.
* \[x] How to create shortcut.
* \[x] How to run smoke.
* \[x] How to use Streamlit fallback.
* \[x] No-live statement.

Acceptatiecriteria:

* \[x] Docs are linked from operator manual.
* \[x] Docs mention no-live proof.
* \[x] Docs contain no live approval language.
* \[x] Docs consistency tests pass.
* \[x] UAT scenario links are valid.

\---

## 27\. Codex bouwvolgorde

### PR 1 - Cutover Safety Contract + Performance Baseline

* \[x] `docs/dashboard-v2-cutover-safety-contract.md`
* \[x] `dashboard\_v2/performance\_baseline.py`
* \[x] baseline tests.
* \[x] no-live tests.

### PR 2 - Performance Budgets + Payload Profiles

* \[x] `dashboard\_v2/performance\_budgets.py`
* \[x] `dashboard\_v2/payload\_profiles.py`
* \[x] payload trimming tests.

### PR 3 - WebSocket Stability

* \[x] `dashboard\_v2/ws\_stability.py`
* \[x] reconnect/replay/backpressure tests.
* \[x] frontend reconnect state.

### PR 4 - Frontend State \& Chart Optimization

* \[x] state slices.
* \[x] chart append/tail/downsampling.
* \[x] lazy routes.
* \[x] frontend tests.

### PR 5 - Static Build \& Offline Assets

* \[x] `dashboard\_v2/static\_build.py`
* \[x] build manifest.
* \[x] no-CDN verification.

### PR 6 - Launcher \& Desktop Shortcut

* \[x] `dashboard\_v2/launcher.py`
* \[x] `dashboard\_v2/desktop\_shortcut.py`
* \[x] launcher/shortcut tests.

### PR 7 - Error Reports \& Logs Panel

* \[x] `dashboard\_v2/error\_reports.py`
* \[x] frontend error boundary submit.
* \[x] logs panel.
* \[x] redaction tests.

### PR 8 - Support Bundle + Browser Smoke Matrix

* \[x] support bundle V2 integration.
* \[x] browser smoke matrix.
* \[x] screenshot/report artifacts.

### PR 9 - Cutover Readiness + Evidence Bundle

* \[x] `dashboard\_v2/cutover\_readiness.py`
* \[x] `dashboard\_v2/evidence\_bundle.py`
* \[x] score/gate tests.

### PR 10 - Check-All, Docs, UAT \& Release Integration

* \[x] check-all integration.
* \[x] operator/UAT docs.
* \[x] release/knowledge/test/performance integration.
* \[x] README update.

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

* \[x] Dashboard V2 Cutover Safety Contract bestaat.
* \[x] Performance baseline werkt.
* \[x] Performance budgets werken.
* \[x] Payload profiles werken.
* \[x] WebSocket stability/reconnect werkt.
* \[x] Frontend state/render optimization werkt.
* \[x] Realtime charts geoptimaliseerd zijn.
* \[x] Static frontend build/offline assets werken.
* \[x] Local launcher UX werkt.
* \[x] Desktop shortcut helper werkt.
* \[x] Local crash/error reports werken.
* \[x] Dashboard V2 logs panel werkt.
* \[x] Support bundle V2 integration werkt.
* \[x] Browser smoke reliability matrix werkt.
* \[x] Streamlit legacy/fallback mode werkt.
* \[x] Cutover readiness score werkt.
* \[x] Dashboard V2 evidence bundle werkt.
* \[x] Check-all/deep profile integration werkt.
* \[x] Operator/UAT acceptance werkt.
* \[x] Release/packaging readiness werkt.
* \[x] Knowledge/test/performance integration werkt.
* \[x] CLI commands werken.
* \[x] Docs bestaan.
* \[x] Tests bewijzen geen live/signed/account/order endpoints.
* \[x] Tests bewijzen localhost default.
* \[x] Tests bewijzen frontend assets offline zijn.
* \[x] Tests bewijzen error/support/evidence secret-free zijn.
* \[x] Browser smoke blijft groen.
* \[x] Check-all blijft groen.
* \[x] Streamlit fallback blijft beschikbaar.
* \[x] Dashboard V2 heeft cutover readiness A/B.
* \[x] Live trading blijft disabled.
* \[x] Roadmap 106 kan na uitvoering naar `Voltooid docs`.

\---

## 30\. Verwachte Roadmap 107 daarna

Na Roadmap 106 is de meest logische opvolger:

```text
Roadmap 107 - Dashboard V2 Operator Workflow Simplification, UX Backlog Execution \& Streamlit Deprecation Plan
```

Mogelijke inhoud:

* \[x] UAT-feedback uit Roadmap 103 verwerken;
* \[x] Dashboard V2 flows vereenvoudigen;
* \[x] onboarding wizard voor Dashboard V2;
* \[x] betere command/action hints;
* \[x] Streamlit deprecation timeline;
* \[x] legacy page removal criteria;
* \[x] V2-only docs;
* \[x] still no live trading.

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


---

## Uitvoeringsbewijs 2026-05-15

Status: Voltooid na hercontrole en implementatie.

Gebouwd:

- Dashboard V2 cutover safety contract en docs.
- Performance baseline, performance budgets en payload profiles.
- WebSocket stability smoke, static/offline build verifier en generated Vite static build met manifest.
- Local launcher report, Windows shortcut helper, local error reports en support diagnostics.
- Browser smoke matrix, cutover readiness score en Dashboard V2 evidence bundle.
- CLI commands voor baseline, budget, payload profile, WebSocket smoke, static verify, launcher, shortcut, error report, support diagnostics, browser matrix, cutover readiness en evidence export.
- Check-all integratie voor Dashboard V2 performance budget en cutover readiness.
- Frontend V2 state slices, snapshot profile loading, duplicate event handling, chart tail limits, error boundary en `/system/logs` page.
- Secret scanner hardening voor npm lockfile integrity hashes.

Validatie:

- `npm install` in `dashboard-v2` voltooid; `node_modules` daarna verwijderd uit workspace.
- `npm run build` voltooid en static assets geschreven naar `src/binance_spot_bot/dashboard_v2/static`.
- `python -m pytest tests/test_roadmaps_104_122_full_surface.py tests/test_roadmap_104_dashboard_v2_acceptance.py tests/test_roadmap_105_dashboard_v2_parity_acceptance.py tests/test_roadmap_106_dashboard_v2_cutover_acceptance.py -q`: 23 passed.
- `python -m binance_spot_bot.cli dashboard-smoke --seconds 1`: ok.
- `python -m pytest -q`: 402 passed, 1 bestaande PytestCollectionWarning.
- `python -m binance_spot_bot.cli check-all --skip-tests --json`: ok.

Safety:

- Live trading blijft disabled.
- Dashboard V2 blijft localhost/local-only.
- Geen signed/order/account/live endpoints toegevoegd.
- Static build verifier blokkeert CDN/remote font references.
- Error/support/evidence output gebruikt redaction en no-live proof.
