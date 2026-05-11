# Roadmap 025 - Operator-grade Visual E2E Demo Dashboard Validation

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-10  
Locatie:

```text
Roadmap docs/025-roadmap-operator-grade-visual-e2e-demo-dashboard-validation.md
```

Volgt op:

- `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
- `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
- `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
- `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
- `Voltooid docs/005` t/m `Voltooid docs/024`

Live trading blijft volledig buiten scope. Deze roadmap bouwt voort op de bestaande one-click launcher, Streamlit dashboard, Demo Spot flow, pilot runner, telemetry, page registry en chart registry. Er wordt niets dubbel gebouwd.

Voltooiingsnotitie 2026-05-10:

- Launch evidence toegevoegd aan `spot-bot control-center` met `data/checks/dashboard/launch-evidence.json`.
- Browser smoke command toegevoegd: `spot-bot dashboard-browser-smoke --url <url> --seconds 15`.
- Operator evidence toegevoegd via CLI en dashboardknop.
- Dashboard header uitgebreid met mode, source, profile, base URL, live-disabled, kill switch, demo armed en runner state.
- Demo Spot en Demo Pilot tonen duidelijkere operatorstatus.
- Docs toegevoegd/bijgewerkt voor smoke tests, visual regression, operator workflow en dashboard evidence.
- Validatie uitgevoerd: `python -m pytest`, `python -m binance_spot_bot.cli check-all --skip-tests --json` en een echte Playwright browser-smoke tegen een lokaal gestart dashboard op `http://127.0.0.1:8860`.
- Screenshot artifacts aangemaakt onder `data/checks/dashboard/screenshots/`.

---

## 0. Onderzoeksconclusie

### Wat al bestaat

- Windows one-click start:
  - `Start Bot Dashboard.cmd`
  - `scripts/start-dashboard.ps1`
  - `spot-bot control-center`
- Veilig launchpad:
  - `LIVE_TRADING_ENABLED=false`
  - `KILL_SWITCH=true`
  - preflight voor dashboardstart
- Dashboard:
  - Streamlit Control Center
  - Demo Spot Trading tab
  - Demo Pilot tab
  - Runner Mission Control
  - telemetry charts
  - page registry
  - chart registry
- Validatie:
  - `spot-bot dashboard-smoke`
  - `spot-bot check-all`
  - no-live tests
  - static UI architecture tests

### Wat nog ontbreekt

- Geen echte browser-based dashboard smoke test die bewijst dat het dashboard visueel opent.
- Geen screenshot artifacts van Overview, Demo Spot Trading en Demo Pilot.
- Geen automatische controle dat de one-click launcher eindigt in een bruikbare lokale URL.
- Geen operator bewijsbundel die laat zien:
  - welke modus actief is;
  - of live trading disabled is;
  - of Demo Spot connectie/arming zichtbaar is;
  - of runner controls zichtbaar zijn;
  - of charts renderen zonder blank screen.
- `docs/dashboard-visual-regression.md` noemt Playwright als toekomstige stap, maar die stap is nog niet uitgevoerd.

Conclusie: de beste volgende update is geen nieuwe tradinglogica, maar een **operator-grade end-to-end bewijslaag** voor het dashboard en de Windows one-click flow.

---

## 1. Doel

Maak het lokaal aantoonbaar dat de bot en het dashboard met één klik starten, visueel bruikbaar zijn, veilig in demo/paper context blijven en de Demo Spot / runner workflow zichtbaar met elkaar verbonden is.

Na deze roadmap moet een operator kunnen zeggen:

- Ik klik `Start Bot Dashboard.cmd`.
- Het dashboard opent lokaal.
- Ik zie duidelijk de actieve modus.
- Ik zie dat live trading disabled is.
- Ik zie Demo Spot credentials/connectivity/arming status.
- Ik zie runner status, commands, telemetry en charts.
- Ik kan een smoke/evidence report genereren met screenshots en JSON.

---

## 2. Scope

### In scope

- Browser smoke automation voor lokaal Streamlit dashboard.
- Screenshot artifacts voor kritieke tabs.
- Dashboard smoke report uitbreiden met browser/evidence info.
- Windows one-click flow betrouwbaarder maken.
- UI-status verduidelijken voor operator:
  - mode;
  - profile;
  - base URL;
  - live disabled;
  - kill switch;
  - demo armed;
  - runner state.
- Visual regression baseline MVP.
- Documentatie voor operator-run en troubleshoot.
- Tests die voorkomen dat live trading in deze flow komt.

### Out of scope

- Geen live trading.
- Geen nieuwe ExchangeAdapter.
- Geen nieuwe RiskEngine.
- Geen nieuwe modeltraining.
- Geen nieuwe strategie.
- Geen duplicaat dashboard.
- Geen opslag van echte secrets in repo.

---

## 3. Gewenste architectuur

### Nieuwe/uitgebreide componenten

```text
scripts/start-dashboard.ps1
        |
        v
spot-bot control-center
        |
        v
Streamlit dashboard URL
        |
        v
spot-bot dashboard-browser-smoke
        |
        +--> screenshots/
        +--> browser-smoke.json
        +--> operator-evidence.json
```

### Interne grenzen

- `control_center.py`
  - blijft verantwoordelijk voor veilig starten.
  - geeft URL, PID, logs, live-disabled en kill-switch status terug.
- `dashboard_smoke.py` of CLI-handler
  - voert browser smoke uit.
  - bewaart bewijs onder `data/checks/dashboard/`.
- `ui/page_registry.py`
  - blijft bron voor tab/page namen.
- `ui/chart_registry.py`
  - blijft bron voor chart keys.
- `docs/`
  - beschrijft operator workflow en visual evidence.

---

## 4. Fase 1 - One-click launch evidence

Taken:

- Voeg een launch evidence artifact toe bij `spot-bot control-center`.
- Sla na start op:
  - timestamp;
  - URL;
  - port;
  - PID;
  - logpaden;
  - live trading status;
  - kill switch status;
  - preflight status.
- Voeg een `--evidence` optie toe of maak evidence standaard onderdeel van start.
- Zorg dat `scripts/start-dashboard.ps1` de URL en logpaden duidelijk print.

Acceptatiecriteria:

- `Start Bot Dashboard.cmd` blijft werken.
- `spot-bot control-center --dry-run` blijft werken.
- `data/checks/dashboard/launch-evidence.json` wordt aangemaakt bij echte start of expliciete evidence-run.
- Evidence bevat `live_trading_enabled: false`.
- Evidence bevat `kill_switch: true`.

---

## 5. Fase 2 - Browser smoke MVP

Taken:

- Voeg CLI-command toe:

```powershell
spot-bot dashboard-browser-smoke --url http://127.0.0.1:8503 --seconds 15
```

- Gebruik Playwright of een lichte browser smoke wrapper.
- Controleer minimaal:
  - pagina opent;
  - titel bevat `Neural Network Binance Spot Bot`;
  - tekst `LIVE TRADING DISABLED` is zichtbaar;
  - tab `Overview` bestaat;
  - tab `Demo Spot Trading` bestaat;
  - tab `Demo Pilot` bestaat;
  - geen Streamlit error banner zichtbaar is;
  - geen `StreamlitDuplicateElementId` zichtbaar is.
- Schrijf JSON-resultaat naar:

```text
data/checks/dashboard/browser-smoke.json
```

Acceptatiecriteria:

- Browser smoke faalt hard bij blank page.
- Browser smoke faalt hard bij Streamlit exception.
- Browser smoke faalt hard als live-disabled tekst ontbreekt.
- Browser smoke kan tegen een bestaande lokale dashboard URL draaien.

---

## 6. Fase 3 - Screenshot evidence

Taken:

- Maak screenshots van:
  - Overview;
  - Demo Spot Trading;
  - Demo Pilot;
  - Logs & Security.
- Bewaar artifacts onder:

```text
data/checks/dashboard/screenshots/
```

- Voeg screenshotpaden toe aan `browser-smoke.json`.
- Voeg optionele `--update-baseline` vlag toe voor lokale baseline screenshots.
- Voeg geen grote binary baselines toe aan repo tenzij bewust gekozen; standaard blijven artifacts lokaal in `data/`.

Acceptatiecriteria:

- Elke screenshot bestaat en is groter dan 0 bytes.
- Screenshots tonen geen blank page.
- Screenshots bevatten geen zichtbare secrets.
- Screenshot artifact paden staan in smoke JSON.

---

## 7. Fase 4 - Operator dashboard polish

Taken:

- Voeg bovenaan het dashboard een compacte operator status bar toe met:
  - mode;
  - profile;
  - source;
  - base URL;
  - live disabled;
  - kill switch;
  - demo armed;
  - runner state.
- Gebruik bestaande `render_badges` of een kleine shared helper.
- Voeg duidelijke status toe aan Demo Spot Trading:
  - selected Binance profile;
  - Demo Spot base URL;
  - credential status zonder secrets;
  - armed/not armed;
  - next safe action.
- Voeg duidelijke status toe aan Demo Pilot:
  - runner alive/stale;
  - current command queue;
  - last heartbeat age;
  - evidence export action.

Acceptatiecriteria:

- Operator ziet direct of hij in demo/paper/testnet-readiness zit.
- Operator ziet direct dat live trading disabled is.
- Demo Spot en Demo Pilot voelen verbonden via gedeelde status.
- Geen secrets worden getoond.

---

## 8. Fase 5 - Evidence export in dashboard

Taken:

- Voeg dashboardknop toe: `Export operator evidence`.
- Export bevat:
  - runtime snapshot summary;
  - selected mode/profile/source;
  - connectivity status;
  - pilot runner status;
  - recent telemetry summary;
  - chart key registry summary;
  - page registry summary;
  - live-disabled proof.
- Bewaar als JSON in:

```text
data/evidence/dashboard/
```

Acceptatiecriteria:

- Export werkt zonder actieve Binance keys.
- Export bevat geen secrets.
- Export bevat `live_trading_enabled: false`.
- Export bevat runner/dashboard status.

---

## 9. Fase 6 - Tests en regressieblokkades

Nieuwe tests:

- `tests/test_roadmap_025_dashboard_browser_smoke.py`
- `tests/test_roadmap_025_operator_evidence.py`

Testdoelen:

- CLI-command import en argument parsing werkt.
- Browser smoke payload schema is stabiel.
- Smoke faalt bij ontbrekende live-disabled marker.
- Evidence export bevat geen secret-like velden.
- One-click dry-run blijft safe:
  - live disabled;
  - kill switch true;
  - localhost URL.
- Page registry en chart registry worden meegenomen in evidence.

Acceptatiecriteria:

- `python -m pytest tests/test_roadmap_025_dashboard_browser_smoke.py tests/test_roadmap_025_operator_evidence.py` slaagt.
- `python -m pytest` slaagt.
- `spot-bot check-all --skip-tests --json` blijft `ok`.

---

## 10. Documentatie

Aanpassen/toevoegen:

- `docs/dashboard-visual-regression.md`
  - concrete browser smoke workflow toevoegen.
- `docs/dashboard-smoke-tests.md`
  - browser smoke command toevoegen.
- `docs/operator-workflow.md`
  - one-click start -> visual check -> demo pilot evidence.
- Nieuw:
  - `docs/dashboard-operator-evidence.md`

Acceptatiecriteria:

- Operator kan zonder codekennis dashboard starten en evidence vinden.
- Docs noemen expliciet dat live trading disabled blijft.
- Docs beschrijven waar screenshots en JSON-artifacts staan.

---

## 11. Definition of Done

- Windows one-click flow is aantoonbaar via launch evidence.
- Dashboard browser smoke opent lokaal dashboard en controleert kritieke UI-markers.
- Screenshots worden lokaal als evidence opgeslagen.
- Operator status bar maakt mode/profile/live-disabled/runner-status direct zichtbaar.
- Demo Spot en Demo Pilot status zijn visueel met elkaar verbonden.
- Evidence export bestaat en lekt geen secrets.
- Nieuwe roadmap 025 tests slagen.
- Volledige pytest-suite slaagt op Python 3.12+.
- `check-all --skip-tests --json` blijft groen.
- Live trading blijft uitgeschakeld.

---

## 12. Verplaatsregel

Wanneer deze roadmap volledig is uitgevoerd en gevalideerd:

```text
Roadmap docs/025-roadmap-operator-grade-visual-e2e-demo-dashboard-validation.md
```

verplaatsen naar:

```text
Voltooid docs/025-roadmap-operator-grade-visual-e2e-demo-dashboard-validation.md
```
