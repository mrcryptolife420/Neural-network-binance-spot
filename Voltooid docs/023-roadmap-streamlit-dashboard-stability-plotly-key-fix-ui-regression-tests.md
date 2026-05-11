# Roadmap 023 - Streamlit Dashboard Stability, Plotly Key Fix, UI Regression Tests \& Operator UX Hardening

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-10  
Voorgestelde locatie:

```text
Roadmap docs/023-roadmap-streamlit-dashboard-stability-plotly-key-fix-ui-regression-tests.md
```

Volgt op:

* `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
* `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
* `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
* `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
* `Voltooid docs/005` t/m `Voltooid docs/022`

Belangrijk: deze roadmap is bewust genummerd als **023**, omdat er volgens de actuele projectstatus al roadmaps bestaan tot en met Roadmap 022. Deze roadmap mag niets overschrijven. Hij focust op de concrete Streamlit-crash die lokaal optreedt en op bredere dashboard-stabiliteit.

Live trading blijft volledig buiten scope.

Voltooiingsnotitie 2026-05-10:

* Plotly charts renderen via `render_plotly_chart` met stabiele keys uit `ui/chart_registry.py`.
* `streamlit_app.py` bevat geen directe `st.plotly_chart(...)` calls meer.
* Dashboard smoke command toegevoegd: `spot-bot dashboard-smoke --seconds 10`.
* Operator docs toegevoegd voor widget-keys, Streamlit troubleshooting en Python-versieondersteuning.
* Validatie uitgevoerd: `pytest tests/test_roadmap_023_dashboard_stability.py tests/test_roadmap_024_dashboard_architecture.py` en `python -m binance_spot_bot.cli dashboard-smoke --seconds 1`.

\---

## 0\. Aanleiding

Lokale foutmelding:

```text
streamlit.errors.StreamlitDuplicateElementId:
There are multiple plotly\_chart elements with the same auto-generated ID.

To fix this error, please pass a unique key argument to the plotly\_chart element.
```

Lokale stacktrace:

```text
File "src/binance\_spot\_bot/ui/streamlit\_app.py", line 631, in \_render\_demo\_pilot
    st.plotly\_chart(runner\_counters\_figure(telemetry\_rows), use\_container\_width=True)
```

Directe oorzaak:

* \[x] Minstens één `st.plotly\_chart(...)` wordt zonder unieke `key=` aangeroepen.
* \[x] Streamlit genereert dan automatisch een ID op basis van elementtype + parameters.
* \[x] Als dezelfde Plotly-figuur of dezelfde chart-call meerdere keren in dezelfde run voorkomt, ontstaat een duplicate element ID.
* \[x] Nieuwere Streamlit-versies zijn hier strenger in.

Structurele oorzaak:

* \[x] Dashboard heeft geen centrale key-conventie voor UI-elementen.
* \[x] Plotly charts, forms, buttons, tables en download buttons kunnen na uitbreidingen botsende auto-generated IDs krijgen.
* \[x] Sommige dashboardsecties worden dynamisch en meerdere keren gerenderd.
* \[x] Er is nog onvoldoende Streamlit UI-regressietest rond duplicate element IDs.

\---

## 1\. Controle en codebase-analyse

### 1.1 Roadmapcontrole

Uit projectcontext:

* \[x] `Voltooid docs` bevat roadmaps tot en met Roadmap 022.
* \[x] Roadmap 015 is voltooid en bevestigde al:

  * dashboard polish;
  * long-running paper ops;
  * scanner research;
  * replay/compare/evidence;
  * readiness;
  * check-all groen;
  * live trading disabled.
* \[x] Deze roadmap mag geen oude roadmap opnieuw bouwen.
* \[x] Deze roadmap moet aansluiten als stabiliteits- en bugfixroadmap na de bestaande roadmapreeks.

### 1.2 Huidige dashboardbasis

Bestand:

```text
src/binance\_spot\_bot/ui/streamlit\_app.py
```

Huidige dashboard heeft onder andere:

* \[x] `st.set\_page\_config(page\_title="Spot Bot Control Center", layout="wide")`
* \[x] Sidebar controls:

  * exchange profile;
  * runtime mode;
  * market data source;
  * symbol;
  * interval;
  * scenario;
  * model alias;
  * start/pause/step/reset/emergency stop.
* \[x] Tabs:

  * Overview;
  * Demo Spot Trading;
  * Credentials \& Profile;
  * Bot Controls;
  * Risk Controls;
  * Strategy \& Model;
  * Market Data;
  * Orders \& Account;
  * Sessions;
  * Evaluation;
  * Strategy Lab;
  * Research;
  * Portfolio;
  * Readiness;
  * Logs \& Security.
* \[x] Imports voor gevorderde modules:

  * manual demo trading;
  * spot preview;
  * diagnostics;
  * evidence;
  * experiment DB;
  * notebook export;
  * portfolio;
  * readiness;
  * replay sandbox;
  * risk debugger;
  * scanner history;
  * signal explainer;
  * strategy templates;
  * workspaces.
* \[x] Live trading wordt zichtbaar disabled gehouden.

### 1.3 Gevonden chart-risico in repo

In de huidige repo-versie staan in `\_render\_overview` minimaal deze calls zonder `key=`:

```python
st.plotly\_chart(candlestick\_figure(snapshot.candles, snapshot.signals, snapshot.fills), use\_container\_width=True)
st.plotly\_chart(equity\_figure(snapshot.equity\_points), use\_container\_width=True)
```

In jouw lokale stacktrace staat aanvullend:

```python
st.plotly\_chart(runner\_counters\_figure(telemetry\_rows), use\_container\_width=True)
```

Conclusie:

* \[x] De fix moet niet alleen de lokale regel 631 aanpassen.
* \[x] Elke `st.plotly\_chart` in het volledige dashboard moet een unieke, stabiele key krijgen.
* \[x] Ook toekomstige dashboardcharts moeten via een helper worden gerenderd zodat dit niet terugkomt.

\---

## 2\. Hoofddoel Roadmap 023

Maak het Streamlit dashboard stabieler en regressiebestendig.

Na deze roadmap moet dit gelden:

* \[ ] Geen `StreamlitDuplicateElementId` meer door Plotly charts.
* \[ ] Elke `st.plotly\_chart` heeft een unieke, voorspelbare key.
* \[ ] Elke belangrijke Streamlit widget heeft een key-conventie.
* \[ ] Dashboard smoke tests detecteren duplicate widget risks vroeg.
* \[ ] Demo Pilot / Demo Spot Trading / Overview charts kunnen samen renderen zonder crash.
* \[ ] Dashboard blijft veilig:

  * geen live mode;
  * geen signed endpoint vanuit demo/research;
  * geen secrets in logs/reports/support bundles.
* \[ ] Python/Streamlit compatibility wordt duidelijker gedocumenteerd.
* \[ ] De gebruikerservaring wordt verbeterd met betere foutmeldingen, diagnostics en fallback.

\---

## 3\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen tweede dashboard bouwen.
* \[ ] Geen nieuwe runtime bouwen.
* \[ ] Geen nieuwe RiskEngine bouwen.
* \[ ] Geen nieuwe ExecutionEngine bouwen.
* \[ ] Geen live trading toevoegen.
* \[ ] Geen testnet orderflow aanpassen buiten UI-stabiliteit.
* \[ ] Geen nieuwe strategie/modeltraining bouwen.
* \[ ] Geen grote refactor zonder tests.

Wel doen:

* \[ ] Bestaande dashboard renderlaag stabiliseren.
* \[ ] Keys toevoegen aan charts/widgets.
* \[ ] UI helper toevoegen voor Plotly charts.
* \[ ] Smoke tests toevoegen.
* \[ ] Diagnostics verbeteren.
* \[ ] Streamlit/Python versiecompatibiliteit vastleggen.
* \[ ] Codex-taken klein houden.

\---

## 4\. Fase 0 - Hotfix: directe Plotly key crash oplossen

Doel: de huidige crash onmiddellijk oplossen.

### Directe fix voor lokale stacktrace

Vervang:

```python
st.plotly\_chart(runner\_counters\_figure(telemetry\_rows), use\_container\_width=True)
```

door:

```python
st.plotly\_chart(
    runner\_counters\_figure(telemetry\_rows),
    use\_container\_width=True,
    key="demo\_pilot\_runner\_counters\_chart",
)
```

### Directe fix voor huidige repo-overview

Vervang:

```python
st.plotly\_chart(candlestick\_figure(snapshot.candles, snapshot.signals, snapshot.fills), use\_container\_width=True)
st.plotly\_chart(equity\_figure(snapshot.equity\_points), use\_container\_width=True)
```

door:

```python
st.plotly\_chart(
    candlestick\_figure(snapshot.candles, snapshot.signals, snapshot.fills),
    use\_container\_width=True,
    key="overview\_candlestick\_chart",
)

st.plotly\_chart(
    equity\_figure(snapshot.equity\_points),
    use\_container\_width=True,
    key="overview\_equity\_chart",
)
```

### Extra chart-keys die direct moeten worden toegevoegd als ze bestaan

Zoek in de volledige codebase naar:

```text
st.plotly\_chart(
```

en geef keys zoals:

```python
key="overview\_candlestick\_chart"
key="overview\_equity\_chart"
key="demo\_spot\_price\_chart"
key="demo\_spot\_equity\_chart"
key="demo\_pilot\_runner\_counters\_chart"
key="demo\_pilot\_runner\_latency\_chart"
key="portfolio\_equity\_chart"
key="portfolio\_exposure\_chart"
key="readiness\_score\_chart"
key="scanner\_rank\_chart"
key="strategy\_lab\_comparison\_chart"
key="session\_compare\_equity\_chart"
key="research\_scanner\_history\_chart"
```

### Acceptatiecriteria

* \[ ] Dashboard start zonder `StreamlitDuplicateElementId`.
* \[ ] `\_render\_demo\_pilot` rendert zonder crash.
* \[ ] Overview rendert zonder duplicate chart ID.
* \[ ] Alle bestaande `st.plotly\_chart` calls hebben een `key`.
* \[ ] Geen trading/risk/execution logic gewijzigd.
* \[ ] Live trading blijft disabled.

\---

## 5\. Fase 1 - Dashboard-wide Streamlit key conventie

Doel: duplicate IDs structureel voorkomen.

### Nieuwe conventie

Gebruik stabiele key-namen:

```text
<section>\_<component>\_<purpose>
```

Voorbeelden:

```text
overview\_chart\_candlestick
overview\_chart\_equity
demo\_spot\_chart\_price
demo\_spot\_form\_manual\_trade
demo\_spot\_button\_refresh\_preview
demo\_pilot\_chart\_runner\_counters
demo\_pilot\_chart\_runner\_latency
portfolio\_chart\_equity
portfolio\_table\_positions
readiness\_table\_blockers
sessions\_download\_current\_summary
logs\_button\_collect\_diagnostics
```

### Taken

* \[ ] Maak `docs/streamlit-widget-key-convention.md`.
* \[ ] Leg key-regels vast voor:

  * charts;
  * buttons;
  * forms;
  * selectboxes;
  * sliders;
  * checkboxes;
  * download buttons;
  * expanders;
  * dataframes/tables.
* \[ ] Keys mogen niet afhangen van onstabiele willekeurige data.
* \[ ] Keys in loops moeten index én stabiele identifier gebruiken:

```python
key=f"session\_compare\_chart\_{session\_id}\_{idx}"
```

* \[ ] Verbied “copy-paste charts zonder key” in docs.
* \[ ] Voeg Codex-regel toe: elke nieuwe Streamlit widget krijgt een key tenzij Streamlit dat technisch niet ondersteunt.

### Acceptatiecriteria

* \[ ] Conventie bestaat in docs.
* \[ ] Nieuwe UI-code volgt conventie.
* \[ ] Review checklist bevat widget-key check.
* \[ ] Geen nieuwe auto-generated chart IDs in dashboard.

\---

## 6\. Fase 2 - Centrale Plotly render-helper

Doel: voorkomen dat ontwikkelaars `st.plotly\_chart` overal los blijven aanroepen.

### Nieuwe of uit te breiden module

```text
src/binance\_spot\_bot/ui/components.py
```

### Nieuwe helper

```python
def render\_plotly\_chart(
    figure,
    \*,
    key: str,
    use\_container\_width: bool = True,
    title: str | None = None,
    help\_text: str | None = None,
) -> None:
    ...
```

### Regels

* \[ ] `key` is verplicht.
* \[ ] Lege key geeft `ValueError`.
* \[ ] Helper kan debug-info tonen in development mode.
* \[ ] Helper kan chart render errors netjes opvangen.
* \[ ] Helper kan fallback tonen als figure `None` is.
* \[ ] Helper gebruikt altijd `st.plotly\_chart(..., key=key)`.

### Migratie

Vervang:

```python
st.plotly\_chart(fig, use\_container\_width=True, key="...")
```

door:

```python
render\_plotly\_chart(fig, key="overview\_chart\_equity")
```

### Acceptatiecriteria

* \[ ] Alle dashboard Plotly charts gebruiken helper of hebben expliciet key.
* \[ ] Helper faalt duidelijk bij ontbrekende key.
* \[ ] Chart render errors crashen niet heel dashboard.
* \[ ] Unit test dekt ontbrekende key.
* \[ ] Dashboard blijft visueel hetzelfde.

\---

## 7\. Fase 3 - Streamlit widget audit

Doel: niet alleen Plotly, maar alle duplicate-risk widgets nalopen.

### Audit scope

Zoek naar:

```text
st.plotly\_chart
st.button
st.download\_button
st.form
st.selectbox
st.multiselect
st.slider
st.checkbox
st.text\_input
st.number\_input
st.dataframe
st.data\_editor
st.tabs
st.expander
```

### Taken

* \[ ] Voeg keys toe aan buttons met herhaalde labels.
* \[ ] Voeg keys toe aan forms.
* \[ ] Voeg keys toe aan download buttons.
* \[ ] Voeg keys toe aan widgets in loops.
* \[ ] Controleer dat labels zoals “Export”, “Refresh”, “Run”, “Save”, “Reset” niet botsen.
* \[ ] Controleer tabs met vergelijkbare UI-secties.
* \[ ] Maak auditrapport:

```text
docs/streamlit-widget-audit.md
```

### Acceptatiecriteria

* \[ ] Geen widget in loops zonder key.
* \[ ] Geen herhaalde button-labels zonder key.
* \[ ] Forms hebben stabiele keys.
* \[ ] Download buttons hebben stabiele keys.
* \[ ] Auditdocument is aanwezig.

\---

## 8\. Fase 4 - Demo Pilot stability

Doel: de lokale stacktrace rond `\_render\_demo\_pilot` structureel oplossen.

### Taken

* \[ ] Zoek `\_render\_demo\_pilot` in lokale/codebaseversie.
* \[ ] Geef alle charts in `\_render\_demo\_pilot` unieke keys:

  * runner counters;
  * runner latency;
  * telemetry history;
  * run duration;
  * alert counts;
  * fills/equity indien aanwezig.
* \[ ] Geef alle buttons/forms in `\_render\_demo\_pilot` keys.
* \[ ] Voeg guard toe voor lege `telemetry\_rows`.
* \[ ] Voeg fallback toe:

```text
Geen telemetry beschikbaar. Start demo pilot of wacht op eerste heartbeat.
```

* \[ ] Voorkom dat dezelfde chart twee keer in dezelfde tab wordt gerenderd met dezelfde key.
* \[ ] Als dezelfde figure bewust op twee plekken staat, gebruik verschillende keys:

  * `demo\_pilot\_runner\_counters\_main`
  * `demo\_pilot\_runner\_counters\_sidebar`

### Acceptatiecriteria

* \[ ] `\_render\_demo\_pilot` crasht niet met duplicate element IDs.
* \[ ] Lege telemetry crasht niet.
* \[ ] Meerdere refreshes/reruns crashen niet.
* \[ ] Start/pause/step flows blijven werken.
* \[ ] Geen live route toegevoegd.

\---

## 9\. Fase 5 - Dashboard smoke test voor Streamlit element IDs

Doel: de bug automatisch vangen vóór je dashboard handmatig start.

### Nieuwe testmodule

```text
tests/test\_streamlit\_dashboard\_keys.py
```

### Tests

* \[ ] Static test: elke `st.plotly\_chart(` call bevat `key=`.
* \[ ] Static test: elke `render\_plotly\_chart(` call bevat `key=`.
* \[ ] Static test: bekende duplicate labels in buttons/forms hebben keys.
* \[ ] Snapshot test: `\_render\_overview` kan met fake snapshot renderen.
* \[ ] Snapshot test: Demo Spot Trading tab kan met fake snapshot renderen.
* \[ ] Snapshot test: Demo Pilot kan met lege telemetry renderen.
* \[ ] No-live test: dashboard smoke maakt live niet selecteerbaar.

### Mogelijke aanpak

Eerste versie mag simpel zijn:

* \[ ] AST of tekstscan over `src/binance\_spot\_bot/ui`.
* \[ ] Fail als `st.plotly\_chart(` voorkomt zonder `key=`.
* \[ ] Fail als `plotly\_chart` in `streamlit\_app.py` rechtstreeks wordt gebruikt buiten helper.

### Acceptatiecriteria

* \[ ] Test faalt vóór fix.
* \[ ] Test slaagt na fix.
* \[ ] Check-all draait deze test.
* \[ ] Geen externe browser nodig voor basis smoke.
* \[ ] Geen Binance credentials nodig.

\---

## 10\. Fase 6 - Optional browser smoke test

Doel: dashboard echt starten en HTTP/render smoke testen.

### Nieuwe scriptoptie

```powershell
python -m binance\_spot\_bot.cli dashboard-smoke --seconds 10
```

of:

```powershell
python -m binance\_spot\_bot.cli check-all --include-dashboard-smoke
```

### Taken

* \[ ] Start dashboard op vrije poort.
* \[ ] Forceer:

  * `LIVE\_TRADING\_ENABLED=false`;
  * `KILL\_SWITCH=true`;
  * demo mode.
* \[ ] Wacht tot HTTP bereikbaar is.
* \[ ] Controleer statuscode.
* \[ ] Check logs op:

  * `StreamlitDuplicateElementId`;
  * `DuplicateWidgetID`;
  * `Traceback`;
  * `place\_order`;
  * `LIVE\_TRADING\_ENABLED=true`.
* \[ ] Stop dashboardproces.
* \[ ] Schrijf smoke artifact:

```text
data/checks/dashboard-smoke.json
```

### Acceptatiecriteria

* \[ ] Dashboard smoke detecteert duplicate element errors.
* \[ ] Smoke draait zonder API keys.
* \[ ] Smoke stopt proces netjes.
* \[ ] Smoke artifact bevat geen secrets.
* \[ ] Smoke kan optioneel in CI draaien.

\---

## 11\. Fase 7 - Dashboard diagnostics voor UI errors

Doel: als de UI crasht, krijgt gebruiker nuttige hulp.

### Taken

* \[ ] Voeg friendly diagnostic toe voor:

  * `StreamlitDuplicateElementId`;
  * `DuplicateWidgetID`;
  * Plotly figure render errors;
  * missing optional dependency;
  * invalid Python version;
  * stale Streamlit cache;
  * port conflict.
* \[ ] Voeg docs toe:

```text
docs/dashboard-troubleshooting-streamlit.md
```

* \[ ] Voeg “Reset Streamlit cache / safe reset dashboard” instructie toe.
* \[ ] Voeg “Run diagnostics” knop of CLI-link toe.
* \[ ] Support bundle neemt recente Streamlit traceback mee, geredact.

### Acceptatiecriteria

* \[ ] Gebruiker ziet oplossing in docs.
* \[ ] Support bundle bevat geredacte traceback.
* \[ ] Diagnostics zeggen welke file/functie waarschijnlijk faalt.
* \[ ] Geen secrets in diagnostics.

\---

## 12\. Fase 8 - Python en dependency compatibility hardening

Aanleiding: lokale stacktrace gebruikt:

```text
C:\\Python314\\Lib\\site-packages\\streamlit\\...
```

Project gebruikt Python `>=3.12`, maar Python 3.14 kan met sommige packages nieuwer/strenger gedrag geven.

### Taken

* \[ ] Documenteer aanbevolen Python-versie:

  * Python 3.12 als primaire ondersteunde versie;
  * Python 3.13 optioneel;
  * Python 3.14 experimenteel totdat dependencies officieel stabiel zijn.
* \[ ] Voeg `python-version` check toe in diagnostics.
* \[ ] Voeg warning toe bij Python 3.14:

```text
Python 3.14 detected. If Streamlit or dependency issues occur, test with Python 3.12.
```

* \[ ] Pin of documenteer minimaal geteste Streamlit-versie.
* \[ ] Voeg `pip freeze`/dependency snapshot toe in support bundle.
* \[ ] Voeg `docs/python-version-support.md` toe.

### Acceptatiecriteria

* \[ ] Diagnostics tonen Python-versie.
* \[ ] Support bundle bevat dependency snapshot.
* \[ ] Docs adviseren Python 3.12 voor stabiele runs.
* \[ ] Geen harde blokkade op Python 3.14, maar duidelijke waarschuwing.

\---

## 13\. Fase 9 - Streamlit session\_state schema hardening

Doel: reruns mogen geen rare widget/key/runtime-botsingen veroorzaken.

### Taken

* \[ ] Definieer session\_state keys in één module:

```text
src/binance\_spot\_bot/ui/session\_state\_keys.py
```

* \[ ] Centrale constants:

  * `runtime`;
  * `runtime\_key`;
  * `running`;
  * `dashboard\_settings`;
  * `manual\_demo\_fills`;
  * `spot\_preview`;
  * `scanner\_exports`;
  * `readiness\_evidence`;
  * telemetry/demo pilot keys.
* \[ ] Voeg helper toe:

```python
def get\_or\_init\_session\_state(...)
```

* \[ ] Geen verspreide string keys meer voor nieuwe code.
* \[ ] Documenteer session\_state schema.

### Acceptatiecriteria

* \[ ] Nieuwe UI-code gebruikt constants.
* \[ ] Reruns resetten runtime niet onverwacht.
* \[ ] Session state reset/safe-reset is duidelijk.
* \[ ] Geen duplicate widget key door session\_state misuse.

\---

## 14\. Fase 10 - Chart registry

Doel: alle dashboardcharts centraal registreren.

### Nieuwe module

```text
src/binance\_spot\_bot/ui/chart\_registry.py
```

### Registry

```python
OVERVIEW\_CANDLESTICK = "overview\_chart\_candlestick"
OVERVIEW\_EQUITY = "overview\_chart\_equity"
DEMO\_PILOT\_RUNNER\_COUNTERS = "demo\_pilot\_chart\_runner\_counters"
DEMO\_PILOT\_RUNNER\_LATENCY = "demo\_pilot\_chart\_runner\_latency"
PORTFOLIO\_EQUITY = "portfolio\_chart\_equity"
READINESS\_SCORE = "readiness\_chart\_score"
SCANNER\_HISTORY = "research\_chart\_scanner\_history"
SESSION\_COMPARE\_EQUITY = "sessions\_chart\_compare\_equity"
```

### Taken

* \[ ] Voeg registry constants toe.
* \[ ] Gebruik constants in dashboard.
* \[ ] Voeg test toe op duplicate chart keys in registry.
* \[ ] Voeg test toe dat elke chart-key uniek is.
* \[ ] Voeg docs toe.

### Acceptatiecriteria

* \[ ] Chart keys zijn uniek.
* \[ ] Nieuwe chart moet registry gebruiken.
* \[ ] Duplicate registry key faalt in test.
* \[ ] Dashboard code wordt leesbaarder.

\---

## 15\. Fase 11 - Plotly figure stability

Doel: charts zelf betrouwbaarder maken.

### Taken

* \[ ] Zorg dat chart functies altijd een figuur teruggeven, ook bij lege data.
* \[ ] `candlestick\_figure(...)` toont lege-state boodschap bij geen candles.
* \[ ] `equity\_figure(...)` toont lege-state boodschap bij geen equity points.
* \[ ] `runner\_counters\_figure(...)` toont lege-state boodschap bij geen telemetry.
* \[ ] Voeg tests toe voor lege data.
* \[ ] Voeg max-points/downsampling toe voor lange sessies.
* \[ ] Voeg timezone/label consistency toe.

### Acceptatiecriteria

* \[ ] Geen chart crasht bij lege data.
* \[ ] Lange sessies maken dashboard niet traag.
* \[ ] Plotly chart tests slagen.
* \[ ] Chart output is consistent.

\---

## 16\. Fase 12 - Dashboard performance guard

Doel: voorkomen dat meer charts de UI traag maken.

### Taken

* \[ ] Voeg render timing toe voor zware chartsecties.
* \[ ] Voeg max rows aan tabellen toe.
* \[ ] Voeg pagination toe voor:

  * fills;
  * alerts;
  * orders;
  * sessions.
* \[ ] Voeg “pause UI refresh” toe.
* \[ ] Voeg waarschuwing toe bij grote session.
* \[ ] Cache zware pure data transforms met `st.cache\_data`, niet runtime objecten.
* \[ ] Vermijd caching van credentials/secrets.

### Acceptatiecriteria

* \[ ] Dashboard blijft bruikbaar bij lange sessies.
* \[ ] Cache bevat geen secrets.
* \[ ] Grote tabellen renderen niet alles tegelijk.
* \[ ] UI refresh kan gepauzeerd worden zonder bot stop.

\---

## 17\. Fase 13 - UI safety/no-live regression

Doel: dashboardfix mag geen safety regressie introduceren.

### Tests

* \[ ] `SELECTABLE\_MODES` bevat geen live.
* \[ ] Dashboard toont `LIVE TRADING DISABLED`.
* \[ ] Demo Spot Trading gebruikt alleen local paper fill.
* \[ ] Demo Pilot gebruikt geen signed endpoint.
* \[ ] Research/Strategy Lab kan geen execution triggeren.
* \[ ] Shadow/Readiness kan geen live\_allowed true zetten.
* \[ ] Support bundle en diagnostics bevatten geen secrets.

### Acceptatiecriteria

* \[ ] Check-all blijft groen.
* \[ ] No-live tests blijven groen.
* \[ ] Geen signed endpoint in dashboard smoke.
* \[ ] Geen live URL in dashboard mode.

\---

## 18\. Fase 14 - Codex bouwvolgorde

### Codex PR 1 - Directe Plotly key hotfix

Scope:

* \[ ] Voeg `key=` toe aan alle bestaande `st.plotly\_chart`.
* \[ ] Voeg fix toe voor `\_render\_demo\_pilot`.
* \[ ] Geen helper/refactor in deze PR als dat te groot wordt.
* \[ ] Voeg kleine static test toe.

Prompt:

```text
Fix StreamlitDuplicateElementId in the dashboard.
Search all src/binance\_spot\_bot/ui files for st.plotly\_chart.
Add unique stable key= arguments to every plotly\_chart call.
In \_render\_demo\_pilot, set key="demo\_pilot\_runner\_counters\_chart" for runner\_counters\_figure and unique keys for every other chart.
Do not change trading, risk, execution, credentials, or live-readiness logic.
Add a test that fails if st.plotly\_chart appears without key=.
```

### Codex PR 2 - Render helper + chart registry

Scope:

* \[ ] `render\_plotly\_chart`.
* \[ ] `chart\_registry.py`.
* \[ ] migrate chart calls.
* \[ ] tests for duplicate registry keys.

### Codex PR 3 - Widget audit

Scope:

* \[ ] add keys to forms/buttons/downloads in high-risk areas.
* \[ ] docs.
* \[ ] tests.

### Codex PR 4 - Dashboard smoke command

Scope:

* \[ ] dashboard-smoke CLI.
* \[ ] log scan.
* \[ ] process cleanup.
* \[ ] optional check-all integration.

### Codex PR 5 - Diagnostics/docs

Scope:

* \[ ] troubleshooting docs.
* \[ ] Python version warning.
* \[ ] support bundle traceback snapshot.
* \[ ] dependency snapshot.

### Codex PR 6 - Performance/chart stability

Scope:

* \[ ] empty-state figures.
* \[ ] downsampling.
* \[ ] table pagination.
* \[ ] UI refresh pause.

\---

## 19\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 023 Fase 0 en Fase 5.

Los de StreamlitDuplicateElementId bug op door elke st.plotly\_chart call in src/binance\_spot\_bot/ui een unieke stabiele key te geven.

Minimaal:
- overview candlestick chart: key="overview\_chart\_candlestick"
- overview equity chart: key="overview\_chart\_equity"
- demo pilot runner counters chart: key="demo\_pilot\_chart\_runner\_counters"
- demo pilot runner latency chart: key="demo\_pilot\_chart\_runner\_latency" als die bestaat

Voeg een test toe tests/test\_streamlit\_dashboard\_keys.py die faalt als st.plotly\_chart voorkomt zonder key=.

Geen trading/risk/execution/live logic aanpassen.
Live trading moet disabled blijven.
```

\---

## 20\. Definition of Done

Roadmap 023 is klaar als:

* \[ ] De lokale `StreamlitDuplicateElementId` crash is opgelost.
* \[ ] Alle `st.plotly\_chart` calls hebben unieke keys.
* \[ ] `\_render\_demo\_pilot` charts hebben unieke keys.
* \[ ] Er is een Streamlit widget-key conventie.
* \[ ] Er is een chart registry of render helper.
* \[ ] Static test detecteert `plotly\_chart` zonder key.
* \[ ] Dashboard smoke detecteert duplicate element errors.
* \[ ] Charts tonen lege-state in plaats van crash.
* \[ ] Diagnostics helpen bij Streamlit UI errors.
* \[ ] Python 3.12/3.14 compatibility is gedocumenteerd.
* \[ ] Dashboard blijft veilig en live-disabled.
* \[ ] Check-all blijft groen.
* \[ ] Security scan blijft groen.
* \[ ] Roadmap 023 kan na uitvoering naar `Voltooid docs`.

\---

## 21\. Verwachte Roadmap 024 daarna

Na Roadmap 023 zou Roadmap 024 logisch focussen op:

```text
Roadmap 024 - Dashboard Component Architecture \& Visual Regression Suite
```

Mogelijke inhoud:

* \[ ] dashboard component registry;
* \[ ] visual regression screenshots;
* \[ ] Playwright smoke suite;
* \[ ] Streamlit tab isolation;
* \[ ] UI plugin sandbox;
* \[ ] dashboard performance budgets;
* \[ ] accessibility checks;
* \[ ] responsive layout validation;
* \[ ] user-facing error boundary system.
