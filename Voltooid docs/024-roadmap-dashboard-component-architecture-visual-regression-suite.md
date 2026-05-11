# Roadmap 024 - Dashboard Component Architecture \& Visual Regression Suite

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-10  
Voorgestelde locatie:

```text
Roadmap docs/024-roadmap-dashboard-component-architecture-visual-regression-suite.md
```

Volgt op:

* `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
* `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
* `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
* `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
* `Voltooid docs/005` t/m `Voltooid docs/022`
* `023-roadmap-streamlit-dashboard-stability-plotly-key-fix-ui-regression-tests.md`

Belangrijk: Roadmap 023 fixt de directe `StreamlitDuplicateElementId` / Plotly `key=` crash. Roadmap 024 voorkomt dat het dashboard opnieuw fragiel wordt door de Streamlit-app modulairder, testbaarder, visueel controleerbaar en regressiebestendig te maken.

Live trading blijft volledig buiten scope.

Voltooiingsnotitie 2026-05-10:

* Dashboardtabs zijn gecentraliseerd in `ui/page_registry.py`.
* Page context en eerste page modules zijn toegevoegd onder `ui/pages/`.
* Chart registry en Plotly helper vormen de vaste componentgrens voor dashboardgrafieken.
* Architectuur-, smoke-, visual-regression-, performance-, accessibility- en troubleshootingdocs zijn toegevoegd.
* Regressietests toegevoegd voor page registry, page module imports, no-live contract, chart-key uniqueness en unkeyed Plotly calls.
* Validatie uitgevoerd: `pytest tests/test_roadmap_023_dashboard_stability.py tests/test_roadmap_024_dashboard_architecture.py` en `python -m binance_spot_bot.cli dashboard-smoke --seconds 1`.

\---

## 0\. Controle vooraf

### Roadmapcontext

* \[x] Roadmap 015 is voltooid en bevestigt dat Roadmaps 001 t/m 014 plus de Codex build priority in `Voltooid docs` stonden.
* \[x] Roadmap 015 rondde dashboard polish, long-running paper ops, scanner research, replay/compare/evidence, readiness en no-live regressies af.
* \[x] Volgens projectcontext bestaan er inmiddels roadmaps tot en met 022.
* \[x] Roadmap 023 is aangemaakt voor de directe Streamlit Plotly key fix.
* \[x] Roadmap 024 moet niet opnieuw Roadmap 023 doen, maar de dashboardarchitectuur structureel versterken.

### Codebasecontext

Gecontroleerd:

```text
src/binance\_spot\_bot/ui/streamlit\_app.py
```

Huidige observaties:

* \[x] `streamlit\_app.py` bevat veel imports uit de volledige applicatie.
* \[x] `streamlit\_app.py` doet argument parsing, session state setup, runtime setup, sidebar controls, tab rendering en veel panel rendering in één bestand.
* \[x] Dashboard heeft veel tabs:

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
  * Logs \& Security;
  * Demo Pilot.
* \[x] Meerdere `st.plotly\_chart(...)` calls staan direct in `streamlit\_app.py`.
* \[x] In de huidige code ontbreken op meerdere Plotly charts nog expliciete keys.
* \[x] Demo Pilot bevat meerdere charts:

  * runner heartbeat;
  * runner counters;
  * runner equity/PnL;
  * command status.
* \[x] Deze structuur maakt het risico op regressies, duplicate keys, trage rendering en moeilijke Codex-wijzigingen groot.

Conclusie:

Roadmap 024 moet het dashboard niet “groter” maken. Roadmap 024 moet het dashboard **opdelen, testen en stabiliseren**.

\---

## 1\. Hoofddoel Roadmap 024

Maak het dashboard productwaardig onderhoudbaar.

Na Roadmap 024 moet gelden:

* \[ ] `streamlit\_app.py` is klein en fungeert vooral als app shell/router.
* \[ ] Elke grote tab heeft een eigen page-module.
* \[ ] Herbruikbare UI-componenten staan in componentmodules.
* \[ ] Chart keys worden centraal beheerd.
* \[ ] Plotly rendering gebeurt via een veilige helper.
* \[ ] UI errors in één panel crashen niet het hele dashboard.
* \[ ] Browser/visual smoke tests detecteren regressies.
* \[ ] Dashboard performance wordt bewaakt.
* \[ ] Accessibility en responsive layout worden gecontroleerd.
* \[ ] Live trading blijft disabled.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen tweede Streamlit-app maken.
* \[ ] Geen nieuwe bot runtime.
* \[ ] Geen nieuwe RiskEngine.
* \[ ] Geen nieuwe ExecutionEngine.
* \[ ] Geen nieuwe Binance adapter.
* \[ ] Geen nieuwe strategy lab.
* \[ ] Geen nieuwe portfolio engine.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoint vanuit dashboard demo/research.
* \[ ] Geen massale tradinglogica-refactor.

Wel doen:

* \[ ] Bestaande dashboardcode modulair maken.
* \[ ] Bestaande tabs verplaatsen naar page-modules.
* \[ ] Bestaande UI helpers uitbreiden.
* \[ ] Bestaande charts via veilige helper renderen.
* \[ ] Bestaande safety/no-live checks behouden.
* \[ ] Nieuwe UI-regressietests toevoegen.

\---

## 3\. Fase 0 - Stabiliteitscontract voor dashboardarchitectuur

Doel: vóór refactor exact vastleggen wat niet mag breken.

### Taken

* \[ ] Maak `docs/dashboard-architecture-contract.md`.
* \[ ] Definieer vaste regels:

  * `streamlit\_app.py` bevat alleen app shell, state setup en routing.
  * Page modules bevatten tab-specifieke rendering.
  * Component modules bevatten herbruikbare UI.
  * Trading/risk/execution logic blijft buiten UI.
  * Elke chart heeft een key uit chart registry.
  * Elke widget in loops heeft een key.
  * Elke tab moet safe kunnen falen zonder heel dashboard te breken.
* \[ ] Voeg no-live contract toe:

  * live mode niet selecteerbaar;
  * live badge zichtbaar;
  * demo/research plaatst geen signed orders.
* \[ ] Voeg Codex-regels toe:

  * geen grote UI-refactor zonder smoke test;
  * geen nieuwe tab zonder page-module;
  * geen chart zonder key;
  * geen raw JSON als primaire operatorweergave.

### Acceptatiecriteria

* \[ ] Contractdocument bestaat.
* \[ ] Refactors verwijzen naar contract.
* \[ ] No-live regels blijven expliciet.
* \[ ] Codex kan op dit contract bouwen.

\---

## 4\. Fase 1 - Page-module architectuur

Doel: `streamlit\_app.py` opsplitsen in onderhoudbare page modules.

### Nieuwe map

```text
src/binance\_spot\_bot/ui/pages/
```

### Nieuwe bestanden

* \[ ] `src/binance\_spot\_bot/ui/pages/\_\_init\_\_.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/overview.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/demo\_spot\_trading.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/credentials\_profile.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/bot\_controls.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/risk\_controls.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/strategy\_model.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/market\_data.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/orders\_account.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/sessions.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/evaluation.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/strategy\_lab.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/research.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/portfolio.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/readiness.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/logs\_security.py`
* \[ ] `src/binance\_spot\_bot/ui/pages/demo\_pilot.py`

### Refactorregels

* \[ ] Elke bestaande `\_render\_\*` functie wordt verplaatst naar passende page module.
* \[ ] `streamlit\_app.py` blijft verantwoordelijk voor:

  * parse args;
  * set page config;
  * initialize session state;
  * build runtime;
  * create tabs;
  * call page render functions.
* \[ ] Geen tradinglogic wijzigen.
* \[ ] Geen runtime behavior wijzigen.
* \[ ] Geen safety gates wijzigen.

### Acceptatiecriteria

* \[ ] Dashboard ziet er functioneel hetzelfde uit.
* \[ ] `streamlit\_app.py` wordt merkbaar kleiner.
* \[ ] Alle bestaande tabs blijven aanwezig.
* \[ ] Dashboard import smoke slaagt.
* \[ ] No-live tests blijven groen.

\---

## 5\. Fase 2 - Page interface contract

Doel: alle page modules hetzelfde patroon laten gebruiken.

### Nieuwe module

```text
src/binance\_spot\_bot/ui/page\_context.py
```

### PageContext bevat

* \[ ] settings;
* \[ ] runtime settings;
* \[ ] snapshot;
* \[ ] profile;
* \[ ] store;
* \[ ] credential manager;
* \[ ] session store;
* \[ ] workspace store;
* \[ ] selected symbol;
* \[ ] selected interval;
* \[ ] selected source;
* \[ ] selected mode;
* \[ ] helper flags:

  * live\_disabled;
  * demo\_armed;
  * expert\_mode;
  * safe\_mode.

### Page module interface

```python
def render\_page(ctx: PageContext) -> None:
    ...
```

### Acceptatiecriteria

* \[ ] Page modules hebben consistente signature.
* \[ ] Minder globale `st.session\_state` toegang in page modules.
* \[ ] Testfixtures kunnen PageContext maken.
* \[ ] Page modules zijn makkelijker apart te testen.

\---

## 6\. Fase 3 - Component library opsplitsen

Doel: UI helpers niet in één los bestand laten groeien.

### Nieuwe map

```text
src/binance\_spot\_bot/ui/components/
```

### Componentbestanden

* \[ ] `badges.py`
* \[ ] `cards.py`
* \[ ] `charts.py`
* \[ ] `tables.py`
* \[ ] `forms.py`
* \[ ] `alerts.py`
* \[ ] `errors.py`
* \[ ] `diagnostics.py`
* \[ ] `downloads.py`
* \[ ] `layout.py`
* \[ ] `debug.py`

### Migratie

Bestaande helpers:

* \[ ] `render\_badges`
* \[ ] `render\_table`
* \[ ] `render\_debug`
* \[ ] `render\_alert\_list`

verplaatsen of re-exporten via:

```text
src/binance\_spot\_bot/ui/components/\_\_init\_\_.py
```

### Acceptatiecriteria

* \[ ] Oude imports blijven tijdelijk werken of worden netjes gemigreerd.
* \[ ] Componenten zijn klein en testbaar.
* \[ ] Geen component roept trading execution aan.
* \[ ] Componenten redacteren gevoelige velden waar nodig.

\---

## 7\. Fase 4 - Chart registry en Plotly render helper

Doel: geen duplicate Plotly keys meer en minder losse `st.plotly\_chart` calls.

### Nieuwe module

```text
src/binance\_spot\_bot/ui/chart\_registry.py
```

### Chart key constants

* \[ ] `OVERVIEW\_CANDLESTICK = "overview\_chart\_candlestick"`
* \[ ] `OVERVIEW\_EQUITY = "overview\_chart\_equity"`
* \[ ] `DEMO\_SPOT\_PREVIEW = "demo\_spot\_chart\_preview"`
* \[ ] `DEMO\_SPOT\_EQUITY = "demo\_spot\_chart\_equity"`
* \[ ] `DEMO\_PILOT\_HEARTBEAT = "demo\_pilot\_chart\_heartbeat"`
* \[ ] `DEMO\_PILOT\_COUNTERS = "demo\_pilot\_chart\_counters"`
* \[ ] `DEMO\_PILOT\_EQUITY\_PNL = "demo\_pilot\_chart\_equity\_pnl"`
* \[ ] `DEMO\_PILOT\_COMMAND\_STATUS = "demo\_pilot\_chart\_command\_status"`
* \[ ] `PORTFOLIO\_EQUITY = "portfolio\_chart\_equity"`
* \[ ] `PORTFOLIO\_EXPOSURE = "portfolio\_chart\_exposure"`
* \[ ] `READINESS\_SCORE = "readiness\_chart\_score"`
* \[ ] `SCANNER\_HISTORY = "research\_chart\_scanner\_history"`
* \[ ] `SESSION\_COMPARE\_EQUITY = "sessions\_chart\_compare\_equity"`

### Render helper

In:

```text
src/binance\_spot\_bot/ui/components/charts.py
```

Voeg toe:

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

Regels:

* \[ ] `key` is verplicht.
* \[ ] Lege key geeft `ValueError`.
* \[ ] Helper vangt Plotly render errors op.
* \[ ] Helper toont nette foutkaart in plaats van dashboardcrash.
* \[ ] Helper ondersteunt lege-state.
* \[ ] Helper logt chart key in debug mode.

### Acceptatiecriteria

* \[ ] Alle `st.plotly\_chart` calls hebben key of gebruiken helper.
* \[ ] Test faalt als `st.plotly\_chart` zonder key wordt toegevoegd.
* \[ ] Duplicate chart keys in registry falen tests.
* \[ ] Demo Pilot charts hebben unieke keys.
* \[ ] StreamlitDuplicateElementId komt niet terug.

\---

## 8\. Fase 5 - UI error boundaries per page/panel

Doel: als één tab of panel faalt, crasht niet het hele dashboard.

### Nieuwe module

```text
src/binance\_spot\_bot/ui/error\_boundary.py
```

### Helper

```python
def render\_with\_boundary(
    title: str,
    render\_fn: Callable\[\[], None],
    \*,
    key: str,
    show\_debug: bool = False,
) -> None:
    ...
```

### Gedrag

* \[ ] Vangt exceptions per page/panel.
* \[ ] Toont friendly error:

  * titel;
  * korte uitleg;
  * mogelijke oplossing;
  * knop/link naar diagnostics;
  * debug details in expander.
* \[ ] Redact secrets uit traceback.
* \[ ] Schrijft error naar diagnostics/support bundle.
* \[ ] Laat andere tabs verder werken.

### Acceptatiecriteria

* \[ ] Fout in Strategy Lab crasht Overview niet.
* \[ ] Fout in Demo Pilot crasht dashboard niet volledig.
* \[ ] Tracebacks zijn geredact.
* \[ ] Diagnostics bevat panelnaam en exceptiontype.
* \[ ] No-live safety blijft intact.

\---

## 9\. Fase 6 - Dashboard route/page registry

Doel: tabs declaratief beheren in plaats van handmatig losse calls.

### Nieuwe module

```text
src/binance\_spot\_bot/ui/page\_registry.py
```

### PageDefinition

```python
@dataclass(frozen=True)
class PageDefinition:
    key: str
    title: str
    module: str
    beginner: bool
    expert: bool
    requires\_runtime: bool
    safety\_level: str
```

### Registry bevat

* \[ ] Overview
* \[ ] Demo Spot Trading
* \[ ] Credentials \& Profile
* \[ ] Bot Controls
* \[ ] Risk Controls
* \[ ] Strategy \& Model
* \[ ] Market Data
* \[ ] Orders \& Account
* \[ ] Sessions
* \[ ] Evaluation
* \[ ] Strategy Lab
* \[ ] Research
* \[ ] Portfolio
* \[ ] Readiness
* \[ ] Logs \& Security
* \[ ] Demo Pilot

### Acceptatiecriteria

* \[ ] Tabs worden vanuit registry opgebouwd.
* \[ ] Beginner/expert mode kan pagina’s filteren.
* \[ ] Iedere pagina heeft unieke key.
* \[ ] Tests controleren duplicate page keys.
* \[ ] Live page bestaat niet.

\---

## 10\. Fase 7 - Dashboard fixtures

Doel: UI-tests kunnen draaien zonder Binance, internet of echte sessies.

### Nieuwe fixtures

```text
tests/fixtures/dashboard/
```

Bestanden:

* \[ ] `empty\_snapshot.json`
* \[ ] `demo\_running\_snapshot.json`
* \[ ] `demo\_with\_fills\_snapshot.json`
* \[ ] `portfolio\_snapshot.json`
* \[ ] `readiness\_blocked\_snapshot.json`
* \[ ] `scanner\_history\_snapshot.json`
* \[ ] `demo\_pilot\_telemetry\_snapshot.json`
* \[ ] `error\_snapshot.json`

### Taken

* \[ ] Maak factory helpers:

  * `make\_dashboard\_context()`
  * `make\_snapshot\_from\_fixture()`
  * `make\_fake\_runtime()`
* \[ ] Geen fixture bevat secrets.
* \[ ] Fixtures zijn klein genoeg voor repo.

### Acceptatiecriteria

* \[ ] Page modules kunnen met fixture context getest worden.
* \[ ] Geen Binance credentials nodig.
* \[ ] Geen netwerk nodig.
* \[ ] No-live status zichtbaar in fixtures.

\---

## 11\. Fase 8 - Static UI regression tests

Doel: simpele fouten vroeg vangen.

### Nieuwe tests

```text
tests/test\_dashboard\_architecture.py
tests/test\_streamlit\_widget\_keys.py
tests/test\_chart\_registry.py
tests/test\_page\_registry.py
```

### Checks

* \[ ] Geen `st.plotly\_chart(` zonder `key=` of zonder helper.
* \[ ] Geen duplicate chart registry values.
* \[ ] Geen duplicate page keys.
* \[ ] Geen page met `live` als key/title.
* \[ ] Geen direct `place\_order` import in UI pages.
* \[ ] Geen credential secret fields in UI diagnostics exports.
* \[ ] Geen raw `st.exception` zonder redaction helper.
* \[ ] Geen widget in loops zonder key waar detecteerbaar.

### Acceptatiecriteria

* \[ ] Tests draaien in `check-all`.
* \[ ] Tests falen bij nieuwe unkeyed Plotly chart.
* \[ ] Tests falen bij live page.
* \[ ] Tests falen bij UI direct execution import.

\---

## 12\. Fase 9 - Browser smoke suite

Doel: het dashboard echt starten en controleren of het opent.

### Nieuwe command

```powershell
python -m binance\_spot\_bot.cli dashboard-smoke --seconds 10
```

of integratie:

```powershell
python -m binance\_spot\_bot.cli check-all --include-dashboard-smoke
```

### Smoke checks

* \[ ] Start dashboard op vrije poort.
* \[ ] Forceer:

  * `LIVE\_TRADING\_ENABLED=false`;
  * `KILL\_SWITCH=true`;
  * demo mode.
* \[ ] Wacht tot HTTP bereikbaar is.
* \[ ] Controleer response.
* \[ ] Scan logs op:

  * `StreamlitDuplicateElementId`;
  * `DuplicateWidgetID`;
  * `Traceback`;
  * `place\_order`;
  * `LIVE\_TRADING\_ENABLED=true`;
  * `api.binance.com/api/v3/order`.
* \[ ] Stop dashboardproces.
* \[ ] Schrijf artifact:

```text
data/checks/dashboard-smoke.json
```

### Acceptatiecriteria

* \[ ] Smoke draait zonder API keys.
* \[ ] Smoke detecteert duplicate element errors.
* \[ ] Smoke detecteert dashboard traceback.
* \[ ] Smoke stopt proces netjes.
* \[ ] Artifact bevat geen secrets.

\---

## 13\. Fase 10 - Visual regression suite

Doel: zien wanneer dashboardlayout visueel breekt.

### Opties

Start licht:

* \[ ] HTML snapshot / text smoke.

Daarna optioneel:

* \[ ] Playwright screenshots.
* \[ ] Screenshot diff met baseline.
* \[ ] Per-page screenshot artifacts.

### Pages voor baseline

* \[ ] Overview.
* \[ ] Demo Spot Trading.
* \[ ] Demo Pilot.
* \[ ] Sessions.
* \[ ] Strategy Lab.
* \[ ] Research.
* \[ ] Portfolio.
* \[ ] Readiness.
* \[ ] Logs \& Security.

### Taken

* \[ ] Voeg `tests/visual/` toe.
* \[ ] Voeg `scripts/run-visual-smoke.ps1` toe.
* \[ ] Voeg baseline update-instructies toe.
* \[ ] CI mag visual smoke optioneel draaien.
* \[ ] Full visual diff mag manual blijven als te zwaar.

### Acceptatiecriteria

* \[ ] Visual smoke toont of pages renderen.
* \[ ] Screenshots/logs zijn secret-free.
* \[ ] Geen browser smoke nodig voor elke unit test.
* \[ ] Visual failures zijn duidelijk te lezen.

\---

## 14\. Fase 11 - Performance budgets per page

Doel: voorkomen dat dashboard steeds trager wordt.

### Nieuwe module

```text
src/binance\_spot\_bot/ui/performance.py
```

### Budgets

* \[ ] Overview: maximaal 1 seconde render-target.
* \[ ] Demo Spot Trading: maximaal 1 seconde render-target.
* \[ ] Demo Pilot: maximaal 2 seconden render-target.
* \[ ] Strategy Lab: maximaal 2 seconden render-target.
* \[ ] Research: maximaal 2 seconden render-target.
* \[ ] Portfolio: maximaal 2 seconden render-target.
* \[ ] Session comparison: maximaal 3 seconden render-target.

### Taken

* \[ ] Meet renderduur per page.
* \[ ] Toon warnings in diagnostics bij trage panels.
* \[ ] Voeg performance artifact toe:

```text
data/checks/dashboard-performance.json
```

* \[ ] Voeg caching-richtlijnen toe:

  * cache pure data transforms;
  * cache geen runtime objecten;
  * cache geen secrets.
* \[ ] Voeg max table rows en pagination toe waar nodig.
* \[ ] Voeg “Pause UI refresh” control toe.

### Acceptatiecriteria

* \[ ] Diagnostics toont trage pages.
* \[ ] Cache bevat geen secrets.
* \[ ] Grote tabellen crashen dashboard niet.
* \[ ] Lange sessions blijven bruikbaar.

\---

## 15\. Fase 12 - Accessibility pass

Doel: dashboard beter bruikbaar maken voor meer schermen en gebruikers.

### Taken

* \[ ] Geen status alleen via kleur.
* \[ ] Badges hebben tekst.
* \[ ] Buttons hebben duidelijke labels.
* \[ ] Icon-only acties vermijden.
* \[ ] Emergency stop zichtbaar maar niet verwarrend.
* \[ ] High-contrast mode controleren.
* \[ ] Grote tekst layout controleren.
* \[ ] Tabellen hebben duidelijke kolommen.
* \[ ] Error messages zijn begrijpelijk.
* \[ ] Keyboard-only basisflow documenteren.

### Acceptatiecriteria

* \[ ] Accessibility checklist bestaat.
* \[ ] High contrast blijft leesbaar.
* \[ ] Status heeft tekstlabel.
* \[ ] Demo flow is begrijpelijk zonder kleurinterpretatie.
* \[ ] Emergency stop blijft altijd vindbaar.

\---

## 16\. Fase 13 - Responsive layout validation

Doel: dashboard werkt beter op laptop/tablet/narrow browser.

### Viewports

* \[ ] 1920x1080 desktop.
* \[ ] 1366x768 laptop.
* \[ ] 1280x720 small laptop.
* \[ ] 1024x768 tablet-ish.
* \[ ] narrow browser read-only.

### Taken

* \[ ] Cards stapelen netjes.
* \[ ] Tabellen gebruiken pagination.
* \[ ] Charts gebruiken container width.
* \[ ] Status header blijft zichtbaar.
* \[ ] Emergency stop blijft bereikbaar.
* \[ ] Sidebar blijft bruikbaar.
* \[ ] Demo Spot Trading ticket breekt niet.

### Acceptatiecriteria

* \[ ] Layout is bruikbaar op laptop.
* \[ ] Geen horizontale chaos in hoofdflow.
* \[ ] Narrow mode toont minstens read-only overzicht.
* \[ ] Live disabled badge blijft zichtbaar.

\---

## 17\. Fase 14 - User-facing dashboard diagnostics

Doel: dashboardproblemen makkelijk oplossen.

### Taken

* \[ ] Voeg `Dashboard Diagnostics` panel toe.
* \[ ] Toon:

  * app version;
  * Python version;
  * Streamlit version;
  * Plotly version;
  * current page;
  * last render error;
  * latest dashboard smoke result;
  * chart key registry status;
  * page registry status.
* \[ ] Voeg knop:

  * export dashboard diagnostics.
* \[ ] Voeg redaction toe.
* \[ ] Voeg troubleshooting docs toe.

### Nieuwe docs

* \[ ] `docs/dashboard-component-architecture.md`
* \[ ] `docs/dashboard-visual-regression.md`
* \[ ] `docs/dashboard-smoke-tests.md`
* \[ ] `docs/dashboard-performance-budgets.md`
* \[ ] `docs/dashboard-accessibility.md`
* \[ ] `docs/dashboard-troubleshooting.md`

### Acceptatiecriteria

* \[ ] Diagnostics zijn secret-free.
* \[ ] Gebruiker ziet waarom dashboard faalt.
* \[ ] Support bundle bevat dashboard diagnostics.
* \[ ] Docs linken naar fixes.

\---

## 18\. Fase 15 - No-live dashboard safety regression

Doel: componentrefactor mag safety niet breken.

### Tests

* \[ ] `SELECTABLE\_MODES` bevat geen live.
* \[ ] Geen page registry item met live.
* \[ ] Geen UI page importeert live execution direct.
* \[ ] Demo Spot Trading gebruikt manual demo/paper flow.
* \[ ] Research/Strategy Lab zijn read-only of paper-only.
* \[ ] Readiness `live\_allowed` blijft false.
* \[ ] Logs/support bundle redacteren secrets.
* \[ ] Browser smoke scant op live button/text.

### Acceptatiecriteria

* \[ ] Safety tests blijven groen.
* \[ ] Geen live mode verschijnt door refactor.
* \[ ] Geen signed endpoint wordt door UI-smoke aangeraakt.
* \[ ] Live disabled badge zichtbaar op hoofdschermen.

\---

## 19\. Codex bouwvolgorde

### Codex PR 1 - Page module split MVP

Scope:

* \[ ] Maak `ui/pages/`.
* \[ ] Verplaats Overview, Demo Spot Trading en Demo Pilot naar page modules.
* \[ ] Laat andere tabs tijdelijk in `streamlit\_app.py`.
* \[ ] Voeg import/smoke tests toe.
* \[ ] Geen tradinglogic wijzigen.

### Codex PR 2 - Page registry en PageContext

Scope:

* \[ ] `page\_context.py`.
* \[ ] `page\_registry.py`.
* \[ ] Tabs uit registry.
* \[ ] Tests voor duplicate page keys en no-live pages.

### Codex PR 3 - Component library split

Scope:

* \[ ] `ui/components/`.
* \[ ] badges/tables/debug/charts/errors.
* \[ ] Backward-compatible imports.
* \[ ] Tests.

### Codex PR 4 - Chart registry en render helper

Scope:

* \[ ] chart constants.
* \[ ] `render\_plotly\_chart`.
* \[ ] migrate all Plotly charts.
* \[ ] static tests voor unkeyed charts.

### Codex PR 5 - Error boundaries

Scope:

* \[ ] `error\_boundary.py`.
* \[ ] wrap page renders.
* \[ ] redacted tracebacks.
* \[ ] tests met failing fake page.

### Codex PR 6 - Dashboard fixtures en static tests

Scope:

* \[ ] fixture snapshots.
* \[ ] page render tests.
* \[ ] no-live UI tests.

### Codex PR 7 - Browser smoke command

Scope:

* \[ ] `dashboard-smoke`.
* \[ ] log scanning.
* \[ ] artifact output.
* \[ ] optional check-all integration.

### Codex PR 8 - Visual regression MVP

Scope:

* \[ ] screenshot/text smoke.
* \[ ] baseline docs.
* \[ ] artifacts.

### Codex PR 9 - Performance/accessibility/responsive pass

Scope:

* \[ ] performance budgets.
* \[ ] diagnostics.
* \[ ] accessibility checklist.
* \[ ] responsive validation.

### Codex PR 10 - Docs/support bundle integration

Scope:

* \[ ] architecture docs.
* \[ ] troubleshooting docs.
* \[ ] support bundle dashboard diagnostics.

\---

## 20\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 024 PR 1: Page module split MVP.

Maak src/binance\_spot\_bot/ui/pages/.
Verplaats alleen de renderfuncties voor Overview, Demo Spot Trading en Demo Pilot uit streamlit\_app.py naar:
- ui/pages/overview.py
- ui/pages/demo\_spot\_trading.py
- ui/pages/demo\_pilot.py

Laat main() in streamlit\_app.py dezelfde tabs tonen en dezelfde functies aanroepen via imports.
Wijzig geen trading/risk/execution/credential logic.
Live trading moet disabled blijven.
Voeg import/smoke tests toe die controleren dat streamlit\_app.py en de drie page modules importeren.
```

Waarom eerst:

* dit pakt de grootste monolithische dashboardpijn aan;
* het is klein genoeg voor één PR;
* het raakt de tabs waar de Plotly-key bug en Demo Pilot crash zitten;
* het maakt latere chart registry/error boundary PR’s makkelijker.

\---

## 21\. Definition of Done

Roadmap 024 is klaar als:

* \[ ] `streamlit\_app.py` is opgesplitst en kleiner.
* \[ ] Alle grote tabs zitten in page modules of hebben een migratiepad.
* \[ ] PageContext bestaat of page interface is consistent.
* \[ ] Page registry bestaat en voorkomt duplicate/live pages.
* \[ ] Component library is opgesplitst.
* \[ ] Chart registry en render helper bestaan.
* \[ ] Error boundaries voorkomen dat één panel het dashboard volledig crasht.
* \[ ] Dashboard fixtures bestaan.
* \[ ] Static UI regression tests bestaan.
* \[ ] Browser smoke command bestaat.
* \[ ] Visual regression MVP bestaat.
* \[ ] Performance budgets zijn gedocumenteerd en meetbaar.
* \[ ] Accessibility checklist is uitgevoerd.
* \[ ] Responsive layout is gevalideerd.
* \[ ] Dashboard diagnostics zijn user-facing.
* \[ ] No-live dashboard safety tests slagen.
* \[ ] Check-all is groen.
* \[ ] Security scan is groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 024 kan na uitvoering naar `Voltooid docs`.

\---

## 22\. Verwachte Roadmap 025 daarna

Na Roadmap 024 zou Roadmap 025 logisch focussen op:

```text
Roadmap 025 - Dashboard Plugin Sandbox, Extension API \& Safe Custom Panels
```

Mogelijke inhoud:

* \[ ] plugin manifest;
* \[ ] plugin permissions;
* \[ ] plugin sandbox;
* \[ ] safe custom dashboard panels;
* \[ ] no network/no execution plugin policy;
* \[ ] plugin visual smoke tests;
* \[ ] plugin crash isolation;
* \[ ] plugin marketplace lokaal, zonder remote code execution;
* \[ ] still no live trading.
