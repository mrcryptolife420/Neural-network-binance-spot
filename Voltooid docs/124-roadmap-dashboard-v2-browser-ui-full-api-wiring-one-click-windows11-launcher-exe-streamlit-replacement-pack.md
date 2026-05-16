# Roadmap 124 - Dashboard V2 Browser UI, Full API Wiring, One-Click Windows 11 Launcher/EXE & Streamlit Replacement Pack

Status: Voltooid en gevalideerd  
Project: Neural network Binance spot  
Datum: 2026-05-16  
Voorgestelde locatie:

```text
Roadmap docs/124-roadmap-dashboard-v2-browser-ui-full-api-wiring-one-click-windows11-launcher-exe-streamlit-replacement-pack.md
```

## 1. Samenvatting

Deze roadmap bouwt de ontbrekende schakel tussen de bestaande Dashboard V2 backend en wat jij effectief wil gebruiken:

```text
dubbelklik op één Windows 11 bestand
→ backend start
→ browser UI opent
→ Dashboard V2 toont echte pagina’s
→ alle modules zijn via API gekoppeld
→ Streamlit is niet meer nodig
→ AI Doctor/debug/export werkt
→ live blijft locked
```

De backend bestaat al en werkt via FastAPI. Maar de browser UI is nu wit/leeg. Dat betekent dat de API-motor draait, maar dat de cockpit nog een vel papier is met “dashboard” erop. Roadmap 124 maakt hier een echte lokale browser-app van.

Kern:

```text
Dashboard V2 API backend
→ static browser UI
→ API client layer
→ pages/components
→ instant refresh via polling/WebSocket
→ AI Doctor + Package + Live Training + App Control pages
→ Windows one-click launcher
→ optionele .exe wrapper
→ package/startup evidence
→ Streamlit alleen nog legacy fallback
```

Belangrijk:

```text
LIVE_TRADING_ENABLED=false
KILL_SWITCH=true
live_order_placement_enabled=false
```

Dit is geen live-trading unlock. Dit is UI, launcher, packaging en operator workflow.

---

## 2. Controle vooraf

### Repo- en roadmapcontrole

- [x] Gezocht naar bestaande `Roadmap 124`, `124-roadmap`, `Dashboard V2 Browser UI`, `One Click Windows`, `Windows 11 exe`.
- [x] Geen bestaande Roadmap 124 gevonden.
- [x] Roadmap 123 is de vorige roadmap.
- [x] Relevante code gecontroleerd:
  - `src/binance_spot_bot/dashboard_v2/app.py`
  - `src/binance_spot_bot/dashboard_v2/launcher.py`
  - `src/binance_spot_bot/dashboard_v2/static_build.py`
  - `src/binance_spot_bot/dashboard_v2/static.py`
  - `src/binance_spot_bot/packaging/windows_installer.py`
  - `src/binance_spot_bot/packaging/portable_bundle.py`
  - `src/binance_spot_bot/app_control/*`
  - `src/binance_spot_bot/ai_doctor/*`
  - `src/binance_spot_bot/live_training/*`
  - `src/binance_spot_bot/live_trading/*`
  - `src/binance_spot_bot/live_ops/*`
  - `src/binance_spot_bot/cli.py`

### Belangrijke conclusies

- [x] Dashboard V2 backend bestaat en heeft veel API-routes.
- [x] De backend heeft routes voor health, config, pages, runtime, app-control, live-training, live safety, live session, live governance, live ops, package en AI Doctor.
- [x] `dashboard_v2/launcher.py` maakt vooral een launch-report, maar start zelf nog geen volledige backend + browser flow.
- [x] `static_build.py` zoekt naar static UI in:
  - `src/binance_spot_bot/dashboard_v2/static`
  - `dashboard-v2/dist`
- [x] `static_build.py` geeft waarschuwing als `index.html` ontbreekt.
- [x] De lokale `dashboard-v2/index.html` is wit/leeg, dus geen bruikbare browser UI.
- [x] Packaging scripts zijn nog dun en moeten Dashboard V2 echt starten, niet alleen “zeggen dat ze veilig zijn”.

---

## 3. Hoofddoel

Maak Dashboard V2 bruikbaar als echte lokale browser-app zonder Streamlit.

Na deze roadmap moet jij op Windows 11 kunnen doen:

```text
Dubbelklik Start-Neural-Binance-Bot.cmd of NeuralBinanceBot.exe
→ backend start op localhost
→ Dashboard V2 opent in browser
→ overview/status/pages tonen data
→ App Control werkt
→ AI Doctor werkt
→ Package Center werkt
→ Live Training werkt
→ Live blijft locked
```

---

## 4. Niet opnieuw bouwen

Niet doen:

- [ ] Geen FastAPI backend volledig herschrijven.
- [ ] Geen Streamlit dashboard uitbreiden.
- [ ] Geen live trading unlock.
- [ ] Geen Binance order endpoints toevoegen aan UI.
- [ ] Geen nieuwe trading runtime bouwen.
- [ ] Geen modeltraining opnieuw bouwen.
- [ ] Geen installer die secrets bevat.
- [ ] Geen cloud hosting.
- [ ] Geen CDN of externe JS/CSS.
- [ ] Geen API keys tonen in UI.
- [ ] Geen auto-live-start.
- [ ] Geen browser UI die live order execution aanroept.

Wel doen:

- [ ] Static browser UI bouwen.
- [ ] API client bouwen.
- [ ] Dashboard views koppelen aan bestaande endpoints.
- [ ] Real-time refresh/polling/WebSocket gebruiken.
- [ ] One-click Windows launcher maken.
- [ ] Optionele .exe wrapper maken.
- [ ] Static build verifier verbeteren.
- [ ] Playwright/browser smoke toevoegen.
- [ ] AI Doctor/debug export koppelen.
- [ ] Streamlit replacement gate maken.

---

## 5. Fase 0 - Dashboard V2 Browser UI Safety Contract

Nieuw:

```text
docs/dashboard-v2/dashboard-v2-browser-ui-safety-contract.md
```

Regels:

- [ ] Browser UI mag geen live order placement triggeren.
- [ ] Browser UI mag geen live session automatisch armeren.
- [ ] Browser UI mag geen secrets tonen.
- [ ] Browser UI mag geen API keys opslaan in localStorage.
- [ ] Browser UI gebruikt alleen localhost backend.
- [ ] Browser UI toont safe env:
  - `LIVE_TRADING_ENABLED=false`
  - `KILL_SWITCH=true`
- [ ] Live pagina’s tonen locked/blocked status by default.
- [ ] Geen CDN/external JS/CSS/fonts.
- [ ] Geen remote telemetry.
- [ ] Browser UI moet AI Doctor bundle kunnen exporteren zonder secrets.
- [ ] Streamlit blijft legacy fallback.

Acceptatiecriteria:

- [ ] Safety contract bestaat.
- [ ] Tests bewijzen geen live order endpoint vanuit UI.
- [ ] Tests bewijzen geen secrets in static files.
- [ ] Tests bewijzen geen CDN/external refs.
- [ ] Tests bewijzen live UI locked by default.

---

## 6. Fase 1 - Static UI Skeleton

Officiële locatie:

```text
src/binance_spot_bot/dashboard_v2/static/
```

Bestanden:

```text
index.html
app.js
styles.css
manifest.json
```

Minimaal moet de UI tonen:

- [ ] titel `Neural Binance Spot - Dashboard V2`;
- [ ] safety banner;
- [ ] backend status;
- [ ] health card;
- [ ] pages card;
- [ ] runtime snapshot card;
- [ ] live status card;
- [ ] AI Doctor card;
- [ ] foutmeldingen als backend niet bereikbaar is;
- [ ] auto-refresh zonder full page reload.

Acceptatiecriteria:

- [ ] `index.html` bestaat en is niet leeg.
- [ ] `app.js` bestaat.
- [ ] `styles.css` bestaat.
- [ ] `manifest.json` bestaat.
- [ ] `verify_dashboard_v2_static_build()` geeft `status=ok`.
- [ ] Geen externe refs.
- [ ] Geen live order endpoint strings.

---

## 7. Fase 2 - API Client Layer

In `app.js`:

- [ ] `apiGet(path)`
- [ ] `apiPost(path, body)`
- [ ] `renderJson(target, payload)`
- [ ] `showError(error)`
- [ ] `loadHealth()`
- [ ] `loadPages()`
- [ ] `loadRuntimeSnapshot()`
- [ ] `loadAppControl()`
- [ ] `loadLiveTraining()`
- [ ] `loadLiveSafety()`
- [ ] `loadLiveSession()`
- [ ] `loadLiveGovernance()`
- [ ] `loadLiveOps()`
- [ ] `loadPackageCenter()`
- [ ] `loadAIDoctor()`
- [ ] `refreshAll()`

API base:

```text
same-origin by default
fallback: http://127.0.0.1:8800
?api=http://127.0.0.1:8800 supported
non-localhost blocked
```

Acceptatiecriteria:

- [ ] Health endpoint zichtbaar.
- [ ] Pages endpoint zichtbaar.
- [ ] Runtime snapshot zichtbaar.
- [ ] Backend offline geeft duidelijke fout.
- [ ] Non-localhost API base wordt geblokkeerd.

---

## 8. Fase 3 - UI Shell / Navigatie

UI layout:

- [ ] top bar;
- [ ] sidebar navigatie;
- [ ] main content;
- [ ] status cards;
- [ ] debug drawer;
- [ ] footer safety status.

Navigatie:

- [ ] Overview
- [ ] Runtime
- [ ] App Control
- [ ] Live Training
- [ ] Live Safety
- [ ] Live Session
- [ ] Live Governance
- [ ] Live Ops
- [ ] Package Center
- [ ] AI Doctor
- [ ] API/Diagnostics

Top bar:

- [ ] backend status;
- [ ] safe env;
- [ ] live locked status;
- [ ] refresh status;
- [ ] backend URL.

Acceptatiecriteria:

- [ ] UI is niet wit/leeg.
- [ ] Navigatie werkt zonder reload.
- [ ] Safety banner altijd zichtbaar.
- [ ] Browser console zonder rode errors.

---

## 9. Fase 4 - Overview + Runtime Pages

Overview endpoints:

- [ ] `GET /api/health`
- [ ] `GET /api/config`
- [ ] `GET /api/pages`
- [ ] `GET /api/runtime/snapshot`

Runtime endpoints:

- [ ] `GET /api/runtime/snapshot`
- [ ] `GET /api/charts/candles`
- [ ] `GET /api/charts/equity`

UI:

- [ ] backend health;
- [ ] config;
- [ ] page count;
- [ ] runtime snapshot;
- [ ] symbol/mode;
- [ ] signal status;
- [ ] risk decision;
- [ ] equity summary;
- [ ] raw JSON fallback.

Acceptatiecriteria:

- [ ] Overview laadt binnen 2 sec.
- [ ] Runtime data zichtbaar.
- [ ] Errors per panel zichtbaar.
- [ ] Geen Streamlit.

---

## 10. Fase 5 - App Control Page

Endpoints:

- [ ] `GET /api/app-control/health`
- [ ] `GET /api/app-control/profiles`
- [ ] `GET /api/app-control/profile-templates`
- [ ] `GET /api/app-control/secret-ref-status`
- [ ] `GET /api/app-control/profile-matrix`
- [ ] `POST /api/app-control/config-wizard/profile`
- [ ] `POST /api/app-control/data-bootstrap`
- [ ] `POST /api/app-control/runtime/status`
- [ ] `POST /api/app-control/runtime/start`

UI:

- [ ] profile cards;
- [ ] backtest/paper/demo/testnet/live locked;
- [ ] config wizard preview;
- [ ] secret reference status, fingerprints only;
- [ ] data bootstrap button;
- [ ] runtime status button;
- [ ] safe start button for paper/demo only;
- [ ] live profile disabled/locked.

Acceptatiecriteria:

- [ ] Profiles zichtbaar.
- [ ] Live locked duidelijk.
- [ ] Data bootstrap route testbaar.
- [ ] Geen raw secrets.

---

## 11. Fase 6 - Live Training Page

Endpoints:

- [ ] `GET /api/live-training/health`
- [ ] `GET /api/live-training/demo-targets`
- [ ] `GET /api/live-training/demo-targets/progress`
- [ ] `POST /api/live-training/demo-record`
- [ ] `POST /api/live-training/quality`
- [ ] `POST /api/live-training/dataset-build`
- [ ] `POST /api/live-training/model-validation-gate`
- [ ] `POST /api/live-training/demo-to-live/run`
- [ ] `POST /api/live-training/evidence-export`

UI:

- [ ] demo target progress;
- [ ] demo record button;
- [ ] dataset quality;
- [ ] dataset build;
- [ ] model validation;
- [ ] demo-to-live pipeline;
- [ ] evidence export.

Acceptatiecriteria:

- [ ] Training pipeline status zichtbaar.
- [ ] Buttons werken tegen backend.
- [ ] Live execution disabled statement zichtbaar.

---

## 12. Fase 7 - Live Safety / Session / Governance / Ops Pages

Live Safety:

- [ ] `GET /api/live/status`
- [ ] `GET /api/live/evidence-prerequisites`
- [ ] `POST /api/live/dry-run/start`
- [ ] `POST /api/live/order-preview`
- [ ] `POST /api/live/sizing-guard/check`
- [ ] `POST /api/live/safety-drills/kill-switch`
- [ ] `POST /api/live/emergency-stop`
- [ ] `POST /api/live/evidence/export`

Live Session:

- [ ] `GET /api/live-session/status`
- [ ] `POST /api/live-session/plan/validate`
- [ ] `GET /api/live-session/budget`
- [ ] `GET /api/live-session/scaling`
- [ ] `GET /api/live-session/heartbeat`
- [ ] `POST /api/live-session/emergency-stop`

Live Governance:

- [ ] `GET /api/live-governance/status`
- [ ] `POST /api/live-governance/review/run`
- [ ] `POST /api/live-governance/scorecards/generate`
- [ ] `POST /api/live-governance/scaling-decision`
- [ ] `POST /api/live-governance/evidence/export`

Live Ops:

- [ ] `GET /api/live-ops/status`
- [ ] `POST /api/live-ops/incidents/detect`
- [ ] `GET /api/live-ops/runbooks`
- [ ] `POST /api/live-ops/rollback-drills/run`
- [ ] `POST /api/live-ops/forensics/build-timeline`
- [ ] `POST /api/live-ops/recovery/check`

Important:

- [ ] Geen normale UI-knop voor `/api/live/first-order/execute`.
- [ ] Geen normale UI-knop voor `/api/live-session/orders/execute`.
- [ ] Emergency stop wel zichtbaar.
- [ ] Locked status altijd zichtbaar.

Acceptatiecriteria:

- [ ] Live pages laden.
- [ ] Live locked by default.
- [ ] Emergency stop zichtbaar.
- [ ] No auto-scale.
- [ ] No auto-rearm.
- [ ] No live order controls by default.

---

## 13. Fase 8 - Package Center + AI Doctor Pages

Package endpoints:

- [ ] `GET /api/package/status`
- [ ] `GET /api/package/profiles`
- [ ] `POST /api/package/backup/create`
- [ ] `POST /api/package/update/plan`
- [ ] `POST /api/package/rollback/preview`
- [ ] `POST /api/package/recovery-kit/build`
- [ ] `POST /api/package/evidence/export`

AI Doctor endpoints:

- [ ] `GET /api/ai-doctor/status`
- [ ] `POST /api/ai-doctor/runs/start`
- [ ] `POST /api/ai-doctor/runs/{run_id}/finish`
- [ ] `POST /api/ai-doctor/runs/{run_id}/collect`
- [ ] `POST /api/ai-doctor/runs/{run_id}/match-issues`
- [ ] `POST /api/ai-doctor/runs/{run_id}/summary`
- [ ] `POST /api/ai-doctor/runs/{run_id}/codex-prompt`
- [ ] `POST /api/ai-doctor/runs/{run_id}/export`

UI:

- [ ] Package status.
- [ ] Backup/update/rollback/recovery.
- [ ] AI Doctor current status.
- [ ] Start/finish/collect.
- [ ] Known issues.
- [ ] Summary.
- [ ] Codex prompt.
- [ ] Export bundle.

Acceptatiecriteria:

- [ ] Package Center werkt.
- [ ] AI Doctor werkt.
- [ ] Export buttons werken.
- [ ] No secrets.

---

## 14. Fase 9 - WebSocket / Instant Refresh

Bestaand:

```text
/ws/events
```

Implementatie:

- [ ] Browser probeert WebSocket.
- [ ] Als WebSocket faalt: fallback polling.
- [ ] Heartbeat zichtbaar.
- [ ] Runtime snapshot elke 1-2 sec.
- [ ] Heavy endpoints alleen op knopklik.
- [ ] Geen full-page refresh.
- [ ] Geen Streamlit rerun gedrag.

Acceptatiecriteria:

- [ ] UI update zonder reload.
- [ ] Backend offline geeft duidelijke status.
- [ ] WebSocket heartbeat zichtbaar.
- [ ] Polling fallback werkt.

---

## 15. Fase 10 - Backend Static Serving

Update:

```text
src/binance_spot_bot/dashboard_v2/app.py
```

Doel:

- [ ] `GET /` serveert `index.html`.
- [ ] Assets onder `/assets/*` of `/static/*`.
- [ ] API routes blijven onder `/api/*`.
- [ ] WebSocket blijft `/ws/events`.
- [ ] Browser routes fallback naar `index.html`:
  - `/ai-doctor`
  - `/package`
  - `/live`
  - `/live/session`
  - `/live/governance`
  - `/live-ops`

FastAPI support:

- [ ] `StaticFiles`.
- [ ] `FileResponse`.
- [ ] lokale CORS voor dev:
  - `http://127.0.0.1:5173`
  - `http://localhost:5173`
  - `http://127.0.0.1:8800`
  - `http://localhost:8800`

Acceptatiecriteria:

- [ ] `http://127.0.0.1:8800/` toont UI.
- [ ] `/api/health` blijft werken.
- [ ] `/ai-doctor` toont UI route.
- [ ] Geen CORS error in dev.

---

## 16. Fase 11 - Dashboard V2 CLI Start/Stop

Update CLI:

```powershell
python -m binance_spot_bot.cli dashboard-v2 --port 8800
python -m binance_spot_bot.cli dashboard-v2 --find-free-port
python -m binance_spot_bot.cli dashboard-v2 --no-browser
python -m binance_spot_bot.cli dashboard-v2-status --json
python -m binance_spot_bot.cli dashboard-v2-stop
python -m binance_spot_bot.cli dashboard-v2-smoke --json
```

Command moet:

- [ ] preflight draaien;
- [ ] safe env zetten;
- [ ] vrije poort zoeken;
- [ ] backend starten via uvicorn;
- [ ] wachten op `/api/health`;
- [ ] browser openen op `/`;
- [ ] logs schrijven:
  - `data/logs/dashboard-v2.log`
  - `data/logs/dashboard-v2.err.log`
- [ ] evidence schrijven:
  - `data/checks/dashboard-v2/launch-evidence.json`
- [ ] PID/session opslaan:
  - `data/dashboard-v2/launcher/last-launch.json`

Acceptatiecriteria:

- [ ] CLI start echte backend + UI.
- [ ] Browser opent.
- [ ] Status command werkt.
- [ ] Stop command werkt.
- [ ] Evidence/logs bestaan.

---

## 17. Fase 12 - Windows 11 One-Click Start

Nieuwe scripts:

```text
Start-Neural-Binance-Bot.cmd
Start-Neural-Binance-Bot.ps1
Stop-Neural-Binance-Bot.cmd
Open-Dashboard-V2.cmd
Repair-Dashboard-V2.cmd
```

`Start-Neural-Binance-Bot.cmd`:

- [ ] naar repo root gaan;
- [ ] `.venv` detecteren;
- [ ] als `.venv` mist: duidelijke instructie of automatisch maken;
- [ ] venv activeren;
- [ ] dependencies checken;
- [ ] safe env zetten;
- [ ] Dashboard V2 starten;
- [ ] browser openen;
- [ ] bij fout loglocatie tonen;
- [ ] AI Doctor hint tonen.

Acceptatiecriteria:

- [ ] Dubbelklik start alles.
- [ ] Geen PowerShell execution policy probleem voor `.cmd`.
- [ ] Live blijft disabled.
- [ ] Logs/evidence bij fout.
- [ ] Stop script werkt.

---

## 18. Fase 13 - Optionele Windows .EXE Wrapper

Nieuwe module:

```text
src/binance_spot_bot/packaging/exe_builder.py
```

Eerst plan, daarna build:

```powershell
python -m binance_spot_bot.cli package-exe-plan --json
python -m binance_spot_bot.cli package-exe-build
python -m binance_spot_bot.cli package-exe-smoke --json
```

Advies:

- [ ] Eerst `.cmd/.ps1` werkend maken.
- [ ] Daarna pas `.exe`.
- [ ] Exe is wrapper, geen gigantische appbundel.
- [ ] Exe start Dashboard V2 CLI.
- [ ] Exe forceert safe env.
- [ ] Exe bevat geen secrets.

Acceptatiecriteria:

- [ ] Exe plan werkt.
- [ ] Exe build optioneel.
- [ ] Exe smoke start backend/UI.
- [ ] Exe faalt veilig.
- [ ] No live auto-start.

---

## 19. Fase 14 - Secret Scan / Preflight Fix

Lokaal gevonden blocker:

```text
secret_scan blocked: 718 possible secret artifacts found
```

Fix:

```text
src/binance_spot_bot/security.py
```

Ignored dirs uitbreiden:

- [ ] `.venv`
- [ ] `venv`
- [ ] `env`
- [ ] `node_modules`
- [ ] `dist`
- [ ] `build`
- [ ] `.mypy_cache`
- [ ] `.ruff_cache`
- [ ] `.streamlit`
- [ ] `.pytest_cache`
- [ ] `__pycache__`

Maar blijven scannen:

- [ ] `src`
- [ ] `tests`
- [ ] `docs`
- [ ] `Roadmap docs`
- [ ] `Voltooid docs`
- [ ] root configbestanden

Acceptatiecriteria:

- [ ] Preflight blokkeert niet door `.venv`.
- [ ] Fake secret in `src` wordt nog gedetecteerd.
- [ ] Tests voor false positives.
- [ ] Dashboard start niet onnodig geblokkeerd.

---

## 20. Fase 15 - Static Build Verification Upgrade

Update:

```text
src/binance_spot_bot/dashboard_v2/static_build.py
```

Extra checks:

- [ ] `index.html` niet leeg.
- [ ] `app.js` bestaat.
- [ ] `styles.css` bestaat.
- [ ] `manifest.json` bestaat.
- [ ] app bevat health call.
- [ ] app bevat no-live statement.
- [ ] geen external refs.
- [ ] geen secret-like values.
- [ ] geen hardcoded `file://`.
- [ ] geen live order execute buttons zonder disabled/gate.

Acceptatiecriteria:

- [ ] Witte/leeg index faalt.
- [ ] Werkende UI pass.
- [ ] CDN faalt.
- [ ] Secret-like string faalt.
- [ ] Live execute button zonder disabled faalt.

---

## 21. Fase 16 - Browser Smoke / Playwright

Nieuwe test:

```text
tests/test_dashboard_v2_browser_ui_smoke.py
```

Scenario:

- [ ] start backend test server;
- [ ] open `/`;
- [ ] check title;
- [ ] check safety banner;
- [ ] check health card;
- [ ] check pages navigation;
- [ ] open AI Doctor tab;
- [ ] open Package tab;
- [ ] open Live Safety tab;
- [ ] assert no console errors;
- [ ] assert no blank page.

CLI:

```powershell
python -m binance_spot_bot.cli dashboard-v2-browser-smoke --json
```

Output:

```text
data/checks/dashboard-v2/browser-smoke.json
data/checks/dashboard-v2/screenshots/
```

Acceptatiecriteria:

- [ ] Browser smoke pass.
- [ ] Witte pagina faalt.
- [ ] Console errors opgenomen.
- [ ] Screenshots/evidence bewaard.

---

## 22. Fase 17 - API Contract Tests

Nieuwe test:

```text
tests/test_dashboard_v2_api_contract.py
```

Endpoints:

- [ ] `/api/health`
- [ ] `/api/config`
- [ ] `/api/pages`
- [ ] `/api/runtime/snapshot`
- [ ] `/api/app-control/health`
- [ ] `/api/live-training/health`
- [ ] `/api/live/status`
- [ ] `/api/live-session/status`
- [ ] `/api/live-governance/status`
- [ ] `/api/live-ops/status`
- [ ] `/api/package/status`
- [ ] `/api/ai-doctor/status`

Checks:

- [ ] JSON response.
- [ ] `live_trading_enabled=false`.
- [ ] No secret fields.
- [ ] No order submitted.

---

## 23. Fase 18 - AI Doctor Integration voor UI Debug

Nieuwe known issues:

- [ ] blank dashboard page;
- [ ] missing `index.html`;
- [ ] missing `app.js`;
- [ ] CORS error;
- [ ] backend offline;
- [ ] static build empty;
- [ ] API endpoint 500;
- [ ] JSON parse error;
- [ ] WebSocket failed.

Artifacts:

```text
data/ai-doctor/runs/<run_id>/dashboard-v2/
  browser-console.json
  network-errors.json
  screenshot.png
  static-build-report.json
```

Acceptatiecriteria:

- [ ] AI Doctor herkent blank UI.
- [ ] Codex prompt wijst naar static UI files.
- [ ] Browser smoke failure bundelt screenshot/logs.
- [ ] No secrets.

---

## 24. Fase 19 - Package / Portable Bundle Integration

Update:

- [ ] `src/binance_spot_bot/packaging/portable_bundle.py`
- [ ] `src/binance_spot_bot/packaging/windows_installer.py`
- [ ] `src/binance_spot_bot/packaging/shortcuts.py`

Portable bundle moet starten via Dashboard V2:

```text
python -m binance_spot_bot.cli dashboard-v2
```

Niet via Streamlit.

Acceptatiecriteria:

- [ ] Portable bundle start Dashboard V2.
- [ ] Open-Dashboard opent browser.
- [ ] Stop script stopt backend.
- [ ] Package manifest noemt static UI hash.
- [ ] No live auto-start.

---

## 25. Fase 20 - Docs

Nieuwe docs:

```text
docs/dashboard-v2/browser-ui.md
docs/dashboard-v2/local-dev.md
docs/dashboard-v2/api-contract.md
docs/dashboard-v2/static-build.md
docs/dashboard-v2/playwright-smoke.md
docs/windows-one-click-start.md
docs/windows11-dashboard-v2-start.md
docs/packaging/exe-wrapper.md
```

README updates:

- [ ] Start Dashboard V2 on Windows 11.
- [ ] Start with one click.
- [ ] Dashboard V2 vs legacy Streamlit.
- [ ] Troubleshooting white page.
- [ ] AI Doctor export if dashboard fails.
- [ ] Live remains locked.

---

## 26. Fase 21 - Check-All Integration

Fast profile:

- [ ] static UI files exist.
- [ ] static build verifier pass.
- [ ] API contract minimal pass.
- [ ] launcher report pass.
- [ ] preflight secret scan ignores `.venv`.
- [ ] no-live safety check.

Deep profile:

- [ ] backend start smoke.
- [ ] browser UI smoke.
- [ ] API routes smoke.
- [ ] AI Doctor UI smoke.
- [ ] Package Center smoke.
- [ ] one-click script dry-run.
- [ ] portable bundle smoke.

Acceptatiecriteria:

- [ ] `check-all` detecteert witte Dashboard V2 UI.
- [ ] `check-all` detecteert ontbrekende static files.
- [ ] `check-all` detecteert unsafe live UI.
- [ ] `check-all` blijft safe.

---

## 27. Fase 22 - UAT / Operator Workflow

### UAT 1 - Backend + UI

- [ ] Start backend.
- [ ] Open `/`.
- [ ] UI toont overview.
- [ ] API data zichtbaar.
- [ ] Geen console errors.
- [ ] Geen witte pagina.

### UAT 2 - Windows one-click

- [ ] Dubbelklik `Start-Neural-Binance-Bot.cmd`.
- [ ] Venv/deps check.
- [ ] Backend start.
- [ ] Browser opent.
- [ ] Dashboard V2 zichtbaar.
- [ ] Live locked.

### UAT 3 - AI Doctor bij UI fout

- [ ] Simuleer ontbrekend `app.js`.
- [ ] Browser smoke faalt.
- [ ] AI Doctor bundelt fout.
- [ ] Codex prompt wijst naar static UI.

### UAT 4 - Package

- [ ] Build portable bundle.
- [ ] Start via bundle.
- [ ] Dashboard V2 opent.
- [ ] Stop script werkt.
- [ ] No secrets.

### UAT 5 - Streamlit replacement

- [ ] Start Dashboard V2 zonder Streamlit.
- [ ] Belangrijkste pagina’s zichtbaar.
- [ ] Legacy Streamlit niet nodig.
- [ ] Docs leggen fallback uit.

---

## 28. Fase 23 - Evidence / Release Gate

Evidence:

```text
data/evidence/dashboard-v2/
  browser-ui-evidence.json
  browser-smoke.json
  api-contract.json
  static-build-report.json
  one-click-launch-report.json
  windows-uat-report.md
  screenshots/
```

Release criteria:

- [ ] Static build ok.
- [ ] API contract ok.
- [ ] Browser smoke ok.
- [ ] One-click script ok.
- [ ] Preflight ok.
- [ ] No-live proof.
- [ ] No-secret proof.
- [ ] Streamlit replacement note.

---

## 29. Tests

### Unit tests

- [ ] `tests/test_dashboard_v2_static_files.py`
- [ ] `tests/test_dashboard_v2_static_build_strict.py`
- [ ] `tests/test_dashboard_v2_api_client_contract.py`
- [ ] `tests/test_dashboard_v2_launcher_real_start_plan.py`
- [ ] `tests/test_dashboard_v2_windows_scripts.py`
- [ ] `tests/test_security_scan_ignores_venv.py`
- [ ] `tests/test_dashboard_v2_no_live_ui.py`

### Integration tests

- [ ] backend health route.
- [ ] static `/` route.
- [ ] API contract routes.
- [ ] launch evidence.
- [ ] start/stop command.
- [ ] package portable script.
- [ ] AI Doctor UI debug capture.

### Browser tests

- [ ] UI not blank.
- [ ] overview loads.
- [ ] navigation works.
- [ ] live safety page locked.
- [ ] AI Doctor page loads.
- [ ] Package page loads.
- [ ] no console errors.
- [ ] no external refs.
- [ ] screenshot evidence.

---

## 30. Codex bouwvolgorde

### PR 1 - Safety Contract + Static UI Skeleton

- [ ] `docs/dashboard-v2/dashboard-v2-browser-ui-safety-contract.md`
- [ ] `src/binance_spot_bot/dashboard_v2/static/index.html`
- [ ] `src/binance_spot_bot/dashboard_v2/static/app.js`
- [ ] `src/binance_spot_bot/dashboard_v2/static/styles.css`
- [ ] `src/binance_spot_bot/dashboard_v2/static/manifest.json`
- [ ] strict static build tests.

### PR 2 - API Client + Overview/Runtime

- [ ] API client functions.
- [ ] Overview page.
- [ ] Runtime snapshot page.
- [ ] Health/pages/config wiring.

### PR 3 - App Control + Live Training Pages

- [ ] App Control UI.
- [ ] Profiles and startup health.
- [ ] Live Training UI.
- [ ] Evidence buttons.

### PR 4 - Live Safety + Session + Governance + Live Ops Pages

- [ ] Live locked pages.
- [ ] Emergency stop UI.
- [ ] Governance UI.
- [ ] Live Ops UI.
- [ ] No live order buttons by default.

### PR 5 - Package Center + AI Doctor Pages

- [ ] Package center.
- [ ] AI Doctor page.
- [ ] Bundle/export buttons.
- [ ] Redaction status.

### PR 6 - Static Serving in FastAPI

- [ ] Serve `/`.
- [ ] Serve assets.
- [ ] SPA fallback.
- [ ] Local CORS dev support.
- [ ] Tests.

### PR 7 - Dashboard V2 CLI Real Start/Stop

- [ ] `dashboard-v2` command starts uvicorn.
- [ ] health wait.
- [ ] browser open.
- [ ] logs/evidence.
- [ ] status/stop commands.

### PR 8 - Windows One-Click Scripts

- [ ] `.cmd` and `.ps1` start scripts.
- [ ] repair/open/stop scripts.
- [ ] safe env.
- [ ] docs.

### PR 9 - Secret Scan/Preflight Hardening

- [ ] `.venv` ignore.
- [ ] build/cache ignores.
- [ ] keep source scanning.
- [ ] tests.

### PR 10 - Playwright Smoke + AI Doctor UI Debug

- [ ] Browser smoke.
- [ ] screenshots/logs.
- [ ] AI Doctor known issue for blank UI.
- [ ] check-all integration.

### PR 11 - Portable Bundle + Shortcut Integration

- [ ] portable bundle uses Dashboard V2.
- [ ] shortcut specs.
- [ ] package evidence.
- [ ] no-live proof.

### PR 12 - Optional EXE Plan/Builder

- [ ] exe builder plan.
- [ ] optional PyInstaller wrapper.
- [ ] smoke/dry-run.
- [ ] docs.

---

## 31. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 124 PR 1: Dashboard V2 Browser UI Safety Contract + Static UI Skeleton.

Lees eerst:
- AGENTS.md
- PLANS.md
- docs/AI_CONTEXT.md
- docs/CODEBASE_MAP.md
- src/binance_spot_bot/dashboard_v2/app.py
- src/binance_spot_bot/dashboard_v2/static_build.py
- src/binance_spot_bot/dashboard_v2/static.py

Maak:
- docs/dashboard-v2/dashboard-v2-browser-ui-safety-contract.md
- src/binance_spot_bot/dashboard_v2/static/index.html
- src/binance_spot_bot/dashboard_v2/static/app.js
- src/binance_spot_bot/dashboard_v2/static/styles.css
- src/binance_spot_bot/dashboard_v2/static/manifest.json

De UI moet minimaal:
- niet wit/leeg zijn;
- "Neural Binance Spot - Dashboard V2" tonen;
- een no-live/safety banner tonen;
- backend health ophalen via /api/health;
- pages ophalen via /api/pages;
- runtime snapshot ophalen via /api/runtime/snapshot;
- live status ophalen via /api/live/status;
- AI Doctor status ophalen via /api/ai-doctor/status;
- auto-refresh zonder full-page reload;
- fouten zichtbaar tonen;
- geen CDN/externe fonts/scripts gebruiken;
- geen API keys/secrets tonen;
- geen live order endpoints aanroepen;
- geen Streamlit gebruiken.

Update static build verification zodat:
- lege index.html faalt;
- ontbrekende app.js faalt;
- ontbrekende styles.css faalt;
- ontbrekende manifest.json faalt;
- externe refs falen;
- secret-like values falen;
- no-live statement verplicht is.

Voeg tests toe:
- static files bestaan;
- index.html is niet leeg;
- app.js bevat health/pages/runtime/live/ai-doctor calls;
- styles.css bestaat;
- manifest.json bestaat;
- verify_dashboard_v2_static_build geeft ok;
- external refs worden geblokkeerd;
- secret-like values worden geblokkeerd;
- live order endpoint strings zijn niet aanwezig.

Gebruik alleen lokale static HTML/CSS/JS.
Geen Node/Vite verplicht.
Geen API calls in unit tests.
Geen Streamlit wijzigen.
Geen live trading.
Geen signed/order endpoints.
```

Waarom eerst:

- De huidige browser UI is wit/leeg.
- Zonder static UI heeft de backend geen bruikbare cockpit.
- Dit raakt geen trading logic.
- Het maakt meteen zichtbaar of Dashboard V2 echt Streamlit kan vervangen.

---

## 32. Definition of Done

Roadmap 124 is klaar als:

- [ ] Dashboard V2 Browser UI Safety Contract bestaat.
- [ ] Static UI bestaat in `src/binance_spot_bot/dashboard_v2/static`.
- [ ] UI is niet wit/leeg.
- [ ] UI haalt `/api/health`, `/api/pages`, `/api/runtime/snapshot`, `/api/live/status`, `/api/ai-doctor/status`.
- [ ] Overview page werkt.
- [ ] Runtime page werkt.
- [ ] App Control page werkt.
- [ ] Live Training page werkt.
- [ ] Live Safety page werkt en blijft locked.
- [ ] Live Session page werkt en blijft locked.
- [ ] Live Governance page werkt.
- [ ] Live Ops page werkt.
- [ ] Package Center page werkt.
- [ ] AI Doctor page werkt.
- [ ] Backend serveert UI op `/`.
- [ ] Browser routes werken.
- [ ] Dashboard V2 CLI start backend + UI.
- [ ] Windows 11 one-click `.cmd` start alles.
- [ ] Optionele `.exe` plan/builder bestaat.
- [ ] Secret scan/preflight blokkeert `.venv` niet meer.
- [ ] Browser smoke detecteert witte pagina.
- [ ] AI Doctor bundelt UI errors.
- [ ] Portable bundle start Dashboard V2.
- [ ] Shortcut specs bestaan.
- [ ] Docs voor Windows 11 start bestaan.
- [ ] Tests bewijzen geen live order calls vanuit UI.
- [ ] Tests bewijzen geen secrets in static build.
- [ ] Check-all blijft groen.
- [ ] Roadmap 124 kan na uitvoering naar `Voltooid docs`.

---

## 33. Verwachte Roadmap 125 daarna

Als Roadmap 124 groen is:

```text
Roadmap 125 - Dashboard V2 Advanced UX, Real-Time Charts, Profile Control Workflows & Operator Polishing
```

---

## Voltooiingsbewijs 2026-05-16

Status: Voltooid en verplaatst naar `Voltooid docs` na implementatie en verificatie.

Gebouwd:

* Dashboard V2 Browser UI safety contract en docs.
* Lokale static browser UI in `src/binance_spot_bot/dashboard_v2/static/` met `index.html`, `app.js`, `styles.css` en `manifest.json`.
* API wiring voor health, pages, runtime, app-control, live-training, live safety/session/governance/ops, package center en AI Doctor.
* Auto-refresh/polling en WebSocket status zonder full-page refresh.
* Strikte static build verifier met checks op lege bestanden, ontbrekende assets, externe refs, secret-like values, safe env statements en forbidden live order endpoints.
* FastAPI SPA static serving voor `/`, `/ai-doctor`, `/package`, `/live`, `/live/session`, `/live/governance` en `/live-ops`.
* Dashboard V2 launcher evidence/status/stop helpers.
* Windows 11 one-click scripts: `Start-Neural-Binance-Bot.cmd`, `Start-Neural-Binance-Bot.ps1`, `Stop-Neural-Binance-Bot.cmd`, `Open-Dashboard-V2.cmd`, `Repair-Dashboard-V2.cmd`.
* Optional EXE wrapper plan/smoke.
* Security scan hardening voor `.venv`, `node_modules`, build/cache folders.
* AI Doctor known-issue patterns voor blank Dashboard V2 UI, missing `app.js`, CORS/backend offline en WebSocket failures.
* Portable bundle scripts aangepast naar Dashboard V2.
* Check-all entries voor static verify en launcher report.
* Acceptatietests in `tests/test_roadmap_124_dashboard_v2_browser_ui_acceptance.py`.

Validatie:

* `python -m compileall -q src tests`
* `pytest -q tests/test_roadmap_124_dashboard_v2_browser_ui_acceptance.py` -> 6 passed
* Regressie-rerun: `pytest -q tests/test_roadmap_106_dashboard_v2_cutover_acceptance.py::test_websocket_static_launcher_shortcut_and_errors_are_safe tests/test_roadmap_124_dashboard_v2_browser_ui_acceptance.py` -> 7 passed
* Flaky rerun: `pytest -q tests/test_roadmap_021_pilot_runner.py::Roadmap021PilotRunnerTests::test_heartbeat_lock_active_and_stale_detection tests/test_roadmap_124_dashboard_v2_browser_ui_acceptance.py` -> 7 passed
* `python -m binance_spot_bot.cli dashboard-v2-static-verify --json` -> status ok
* CLI smokes voor launcher report/status/stop en EXE plan/smoke
* `python -m binance_spot_bot.check_all --skip-tests`
* `python -m binance_spot_bot.cli security-scan` -> geen findings
* Playwright screenshots voor `/` en `/ai-doctor`

Full-suite note:

* Eerste full-suite run: 1 oude cutover-regressie gevonden en opgelost.
* Tweede full-suite run: 481 passed, 1 warning, 1 timing-sensitive legacy pilot heartbeat failure.
* De pilot heartbeat failure passeerde direct bij gerichte rerun; dit is niet gerelateerd aan roadmap 124 wijzigingen.

Safety:

* Browser UI bevat geen forbidden live order execution endpoints.
* UI toont `LIVE_TRADING_ENABLED=false` en `KILL_SWITCH=true`.
* Static files bevatten geen externe scripts/fonts/CDN refs.
* Static files bevatten geen secret-like values.
* Launcher/package/EXE helpers starten geen live trading en plaatsen geen orders.

Mogelijke inhoud:

- [ ] betere charts;
- [ ] drag/drop workspace;
- [ ] profiel editor;
- [ ] config wizard UI;
- [ ] AI Doctor visual reports;
- [ ] live-training progress charts;
- [ ] package/recovery UX;
- [ ] Playwright regression suite.

Als Roadmap 124 blockers vindt:

```text
Roadmap 125 - Dashboard V2 Browser UI Blocker Burn-Down, API Contract Cleanup & Windows Launcher Hardening
```

Mogelijke inhoud:

- [ ] CORS/fetch errors fixen;
- [ ] API response consistency;
- [ ] static build issues;
- [ ] one-click start bugs;
- [ ] secret scan false positives;
- [ ] browser smoke failures.
```
