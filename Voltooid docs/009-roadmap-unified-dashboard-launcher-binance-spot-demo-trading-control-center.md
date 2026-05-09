# Roadmap 009 - Unified Dashboard Launcher \& Binance Spot Demo Trading Control Center

Status: Concept / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-09  
Voorgestelde bestandsnaam:

```text
Roadmap docs/009-roadmap-unified-dashboard-launcher-binance-spot-demo-trading-control-center.md
```

Volgt op:

* `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
* `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
* `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
* `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
* `Roadmap docs/005-roadmap-long-paper-testnet-alerts-scanner-packaging.md`
* `006-roadmap-multi-symbol-portfolio-testnet-endurance-mlops.md`
* `007-roadmap-live-readiness-audit-shadow-chaos-release-governance.md`
* `008-roadmap-strict-live-readiness-pilot-design.md`

Doel: het dashboard en het starten van de bot veel beter op elkaar aansluiten, zodat de gebruiker vanuit één duidelijke lokale flow de bot kan starten, demo Binance Spot-data kan zien, veilige demo/paper trades kan uitvoeren in het dashboard, fills/orders/sessies kan volgen, en nooit per ongeluk live trading activeert.

Belangrijk: deze roadmap activeert geen live trading. Alles blijft `demo`, `paper`, `binance-demo-spot` of `testnet-readiness` met harde safety gates.

\---

## 0\. Onderzoek en huidige status

### 0.1 Roadmapcontrole

* \[x] Roadmap 001 t/m 004 zijn voltooid.
* \[x] Roadmap 005 staat in `Roadmap docs` en focust op long paper/testnet sessies, alerts, scanner, modeltraining, storage, reports en Windows packaging.
* \[x] Deze Roadmap 009 bouwt niet opnieuw aan long sessions, portfolio risk, shadow mode of live-readiness.
* \[x] Deze Roadmap 009 focust specifiek op:

  * startflow;
  * dashboard UX;
  * bot lifecycle vanuit dashboard;
  * demo Binance Spot trading;
  * handmatige demo trade ticket;
  * zichtbare order/fill lifecycle;
  * first-run setup;
  * operator confidence.

### 0.2 Codebaseonderzoek

Gecontroleerde onderdelen:

* \[x] `src/binance\_spot\_bot/ui/streamlit\_app.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/launcher.py`
* \[x] `scripts/start-dashboard.ps1`
* \[x] `src/binance\_spot\_bot/exchange\_profiles.py`
* \[x] `src/binance\_spot\_bot/execution.py`
* \[x] `Roadmap docs/005-roadmap-long-paper-testnet-alerts-scanner-packaging.md`

Huidige sterktes:

* \[x] Dashboard bestaat al in Streamlit.
* \[x] Dashboard heeft tabs:

  * Overview;
  * Credentials \& Profile;
  * Bot Controls;
  * Risk Controls;
  * Strategy \& Model;
  * Market Data;
  * Orders \& Account;
  * Sessions;
  * Evaluation;
  * Logs \& Security.
* \[x] Dashboard toont `LIVE TRADING DISABLED`.
* \[x] Sidebar heeft controls voor:

  * exchange profile;
  * runtime mode;
  * market data source;
  * symbol;
  * interval;
  * scenario;
  * model alias;
  * replay speed;
  * start/pause/step/reset/emergency stop.
* \[x] CLI heeft commands:

  * `run-local`;
  * `stream-paper`;
  * `dashboard`;
  * `launch-dashboard`;
  * `connectivity-check`;
  * `list-sessions`;
  * `show-session`;
  * `evaluate-model`;
  * `data-quality`.
* \[x] Windows startscript start Streamlit, kiest een vrije poort en zet `LIVE\_TRADING\_ENABLED=false` en `KILL\_SWITCH=true`.
* \[x] Exchange profiles bestaan:

  * `local-demo`;
  * `binance-demo-spot`;
  * `binance-spot-testnet`.
* \[x] `ExecutionEngine` ondersteunt:

  * `DISABLED`;
  * `PAPER`;
  * `TESTNET` via `test\_order`;
  * live blijft geblokkeerd.

Belangrijkste huidige gaten:

* \[ ] Bot-start en dashboard-start voelen nog als losse onderdelen.
* \[ ] `launch-dashboard` print alleen URL/poort en start de UI niet volledig vanuit Python.
* \[ ] `dashboard` CLI print een Streamlit command in plaats van een complete launcher-flow.
* \[ ] Dashboard heeft geen duidelijke first-run wizard.
* \[ ] Dashboard heeft geen dedicated “Demo Spot Trading” tab.
* \[ ] Dashboard heeft geen handmatige safe trade ticket voor demo/paper.
* \[ ] Dashboard toont orders/fills vooral als JSON, niet als operatorvriendelijke timeline/tabel.
* \[ ] Dashboard heeft geen duidelijke knop “Start bot engine” versus “Start dashboard”.
* \[ ] Dashboard heeft geen duidelijke state machine voor stopped/starting/running/paused/error.
* \[ ] Dashboard heeft geen “Binance Spot demo explained” flow.
* \[ ] Dashboard kan nog te technisch aanvoelen voor dagelijks gebruik.
* \[ ] De gebruiker ziet niet genoeg waarom een trade wel/niet uitgevoerd werd.
* \[ ] Geen guided setup voor:

  * local demo;
  * Binance public market data;
  * Binance Demo Spot API;
  * Binance Spot Testnet.

### 0.3 Binance Spot public-data onderzoek

Getoetst met public Binance Spot data voor `BTCUSDT`:

* \[x] `BTCUSDT` heeft status `TRADING`.
* \[x] Spot trading is toegestaan.
* \[x] Symbol filters bevatten:

  * `PRICE\_FILTER`;
  * `LOT\_SIZE`;
  * `MARKET\_LOT\_SIZE`;
  * `NOTIONAL`;
  * order count filters.
* \[x] `BTCUSDT` gebruikt onder andere:

  * tick size `0.01000000`;
  * lot step `0.00001000`;
  * min notional `5.00000000`.
* \[x] Public top-of-book bid/ask is beschikbaar.
* \[x] Public UI klines zijn beschikbaar en geschikt voor dashboard candlestick visualisatie.
* \[x] Deze data is genoeg om een veilige demo/paper spot trading UI te bouwen zonder echte orders.

Conclusie:

* \[x] Dashboard kan realistische Binance Spot demo/paper trading tonen met public market data.
* \[x] Voor echte Binance Demo Spot API/testnet acties moeten credentials en testnet guards verplicht blijven.
* \[x] Handmatige “demo trade” in het dashboard moet standaard lokaal/paper blijven.
* \[x] Demo fills moeten zichtbaar en verklaarbaar zijn, maar mogen geen echte orders zijn.

\---

## 1\. Hoofddoel Roadmap 009

Maak van het project een echte lokale **Bot Control Center** ervaring:

```text
Dubbelklik / CLI start
→ preflight
→ dashboard opent
→ gebruiker kiest demo/paper/binance-demo-spot
→ market data zichtbaar
→ bot engine start
→ gebruiker kan safe demo trade uitvoeren
→ chart toont signalen/fills
→ orders/account tab toont lifecycle
→ session report exporteerbaar
→ live trading blijft onmogelijk
```

\---

## 2\. Scope

### In scope

* \[ ] Unified launcher voor dashboard + bot engine.
* \[ ] First-run wizard.
* \[ ] Dashboard start state machine.
* \[ ] Demo Spot Trading tab.
* \[ ] Safe manual demo/paper trade ticket.
* \[ ] Binance public Spot market-data preview.
* \[ ] Binance Demo Spot API profile UX.
* \[ ] Better bot controls.
* \[ ] Better order/fill tables.
* \[ ] Better session visibility.
* \[ ] Better error/preflight UX.
* \[ ] Dashboard health banner.
* \[ ] Operator-friendly labels in Nederlands/Engels.
* \[ ] No-live safety tests.

### Out of scope

* \[ ] Live trading.
* \[ ] Futures.
* \[ ] Margin.
* \[ ] Withdrawals.
* \[ ] Autonome LLM order placement.
* \[ ] Portfolio multi-symbol auto-trading.
* \[ ] Full production deployment.

\---

## 3\. Fase 0 - UX-first safety contract

Doel: vóór UI-wijzigingen exact vastleggen wat de dashboardervaring veilig moet doen.

### Taken

* \[ ] Maak `docs/dashboard-safety-contract.md`.
* \[ ] Definieer alle dashboard modes:

  * `local-demo`;
  * `paper-public-spot`;
  * `binance-demo-spot-readiness`;
  * `binance-spot-testnet-readiness`.
* \[ ] Definieer wat elke mode wel/niet mag:

  * public market data lezen;
  * local paper fills maken;
  * test order uitvoeren;
  * echte testnet order plaatsen;
  * live order plaatsen.
* \[ ] Live order plaatsen blijft overal `false`.
* \[ ] Maak matrix:

```text
Mode | Requires keys | Uses real market data | Can paper fill | Can test\_order | Can real order
```

* \[ ] Voeg tests toe dat live nergens zichtbaar/selecteerbaar is.
* \[ ] Dashboard toont deze matrix in een help-panel.

### Acceptatiecriteria

* \[ ] Gebruiker ziet exact welke mode actief is.
* \[ ] Gebruiker ziet exact of een knop echte orders kan sturen.
* \[ ] Geen enkele demo-knop stuurt echte live orders.
* \[ ] Safety contract staat in docs en dashboard.

\---

## 4\. Fase 1 - Unified Bot Launcher

Doel: bot en dashboard starten als één duidelijke flow.

### Nieuwe module

```text
src/binance\_spot\_bot/control\_center.py
```

### Nieuwe CLI commands

```powershell
python -m binance\_spot\_bot.cli control-center
python -m binance\_spot\_bot.cli control-center --mode demo
python -m binance\_spot\_bot.cli control-center --mode paper --source rest --symbol BTCUSDT
python -m binance\_spot\_bot.cli control-center --safe-reset
```

### Taken

* \[ ] `control-center` kiest vrije poort.
* \[ ] `control-center` zet safe env:

  * `LIVE\_TRADING\_ENABLED=false`;
  * `KILL\_SWITCH=true`;
  * `PYTHONPATH=src`.
* \[ ] `control-center` voert preflight uit.
* \[ ] `control-center` start Streamlit.
* \[ ] `control-center` wacht tot dashboard bereikbaar is.
* \[ ] `control-center` opent browser.
* \[ ] `control-center` schrijft PID en logs.
* \[ ] `control-center` toont URL, PID, mode, source, symbol.
* \[ ] `control-center --safe-reset` sluit oude dashboardprocessen, wist geen data, maar reset runtime state.
* \[ ] `dashboard` CLI blijft bestaan als legacy/advanced command.
* \[ ] Windows `.cmd` gaat intern naar `control-center`.

### Acceptatiecriteria

* \[ ] Eén command start alles.
* \[ ] Dubbelklik start alles.
* \[ ] Geen terminalkennis nodig.
* \[ ] Oude dashboardprocessen worden gedetecteerd.
* \[ ] Als dashboard al draait, opent de bestaande URL.
* \[ ] Als poort bezet is, wordt nieuwe poort gekozen.
* \[ ] Live env flags blijven hard disabled.

\---

## 5\. Fase 2 - Start/Stop dashboard en bot engine scheiden in de UI

Doel: gebruiker moet begrijpen wat gestart is: dashboard of bot engine.

### UI-state model

```text
Dashboard process:
- not\_started
- starting
- running
- unreachable
- stopped

Bot runtime:
- not\_created
- ready
- running
- paused
- stopped
- completed
- error
```

### Taken

* \[ ] Voeg `DashboardRuntimeState` toe.
* \[ ] Voeg `BotEngineState` toe.
* \[ ] Dashboard header toont:

  * dashboard status;
  * bot engine status;
  * mode;
  * source;
  * profile;
  * live disabled badge.
* \[ ] Sidebar knoppen hernoemen:

  * `Start dashboard` alleen in launcher/landing context.
  * `Start bot engine`.
  * `Pause bot engine`.
  * `Step once`.
  * `Reset bot engine`.
  * `Emergency stop`.
* \[ ] Maak statusbanner:

  * groen: running;
  * geel: paused/degraded;
  * rood: error/emergency stopped;
  * grijs: ready/not started.
* \[ ] Voeg “Wat gebeurt er als ik klik?” uitleg toe per knop.

### Acceptatiecriteria

* \[ ] Gebruiker ziet verschil tussen dashboard en bot.
* \[ ] Start/pause/reset/emergency stop zijn begrijpelijk.
* \[ ] Emergency stop blijft altijd zichtbaar.
* \[ ] Bot reset sluit dashboard niet.
* \[ ] Dashboard refresh herstart bot niet onbedoeld.

\---

## 6\. Fase 3 - First-run wizard

Doel: eerste keer starten eenvoudig maken.

### Wizard stappen

1. \[ ] Kies veilige modus:

   * Local demo replay;
   * Binance public Spot paper;
   * Binance Demo Spot API;
   * Binance Spot Testnet readiness.
2. \[ ] Kies symbol:

   * BTCUSDT;
   * ETHUSDT;
   * BNBUSDT;
   * custom.
3. \[ ] Kies market data:

   * demo;
   * REST public;
   * WebSocket public;
   * fallback auto.
4. \[ ] Kies risk preset:

   * conservative;
   * balanced;
   * aggressive-paper-only.
5. \[ ] Preflight.
6. \[ ] Start bot engine.
7. \[ ] Toon demo trade uitleg.

### Taken

* \[ ] Voeg `ui/wizard.py` toe.
* \[ ] Wizard status opslaan zonder secrets.
* \[ ] Wizard opnieuw openen via Settings.
* \[ ] Wizard blokkeert risicovolle modes zonder credentials/preflight.
* \[ ] Wizard toont “local demo is safest first start”.

### Acceptatiecriteria

* \[ ] Nieuwe gebruiker kan binnen 2 minuten demo draaien.
* \[ ] Geen keys nodig voor local demo.
* \[ ] Binance Demo Spot API vraagt credentials pas in juiste stap.
* \[ ] Wizard schrijft geen secrets naar disk.
* \[ ] Wizard kan worden gereset.

\---

## 7\. Fase 4 - Binance Spot demo market-data preview

Doel: gebruiker ziet echte Spot marktdata vóór trade-simulatie.

### UI panel

* \[ ] Current price.
* \[ ] Bid.
* \[ ] Ask.
* \[ ] Spread bps.
* \[ ] 1m candlestick preview.
* \[ ] Volume.
* \[ ] Symbol filters:

  * tick size;
  * step size;
  * min notional;
  * market lot size;
  * order types.
* \[ ] Data source status.
* \[ ] Last refresh time.
* \[ ] Fallback state.

### Backend

Nieuwe module:

```text
src/binance\_spot\_bot/spot\_preview.py
```

Functies:

* \[ ] `load\_spot\_symbol\_preview(symbol)`
* \[ ] `load\_spot\_order\_book\_preview(symbol)`
* \[ ] `load\_spot\_ui\_klines(symbol, interval, limit)`
* \[ ] `spot\_preview\_to\_dashboard\_payload()`

### Acceptatiecriteria

* \[ ] BTCUSDT preview werkt met public endpoints.
* \[ ] Als Binance niet bereikbaar is, toont dashboard duidelijke fallback.
* \[ ] Preview kan niet traden.
* \[ ] Filters worden gebruikt in demo trade ticket validatie.
* \[ ] Geen credentials nodig.

\---

## 8\. Fase 5 - Dedicated “Demo Spot Trading” tab

Doel: één duidelijke plek waar gebruiker demo trades kan zien en uitvoeren.

### Nieuwe tab

```text
Demo Spot Trading
```

### Layout

* \[ ] Bovenste rij:

  * mode badge;
  * symbol;
  * current price;
  * spread;
  * session id;
  * live disabled.
* \[ ] Linkerkant:

  * candlestick chart;
  * signal markers;
  * manual demo fills;
  * bot demo fills.
* \[ ] Rechterkant:

  * demo trade ticket;
  * risk check preview;
  * estimated quantity;
  * estimated notional;
  * estimated fees/slippage;
  * validation status.
* \[ ] Onderkant:

  * open demo position;
  * fills table;
  * order lifecycle;
  * account balances;
  * audit tail.

### Acceptatiecriteria

* \[ ] Demo trading heeft eigen tab.
* \[ ] Trade ticket is niet verstopt in JSON.
* \[ ] Gebruiker ziet “DEMO/PAPER ONLY”.
* \[ ] Fills verschijnen direct op chart.
* \[ ] Orders/fills zijn begrijpelijk.

\---

## 9\. Fase 6 - Safe manual demo trade ticket

Doel: gebruiker kan in dashboard demo BUY/SELL uitvoeren zonder echte orders.

### Trade ticket velden

* \[ ] Side: BUY / SELL.
* \[ ] Symbol.
* \[ ] Quote amount.
* \[ ] Quantity preview.
* \[ ] Order type:

  * market simulation;
  * limit simulation later.
* \[ ] Price source:

  * last candle close;
  * mid price;
  * bid/ask.
* \[ ] Fee/slippage estimate.
* \[ ] Risk preset.
* \[ ] Confirm checkbox:

  * `I understand this is DEMO/PAPER only`.

### Backend

Nieuwe module:

```text
src/binance\_spot\_bot/manual\_demo\_trading.py
```

Types:

```text
ManualDemoTradeRequest
ManualDemoTradePreview
ManualDemoTradeResult
```

Flow:

1. \[ ] User vult ticket in.
2. \[ ] Preview berekent quantity/notional.
3. \[ ] Symbol filters worden toegepast.
4. \[ ] RiskEngine checkt.
5. \[ ] ExecutionEngine paper fillt.
6. \[ ] OrderLifecycleStore krijgt intent/fill.
7. \[ ] SessionStore schrijft fill.
8. \[ ] AuditLog schrijft event.
9. \[ ] Dashboard toont fill.

### Acceptatiecriteria

* \[ ] BUY demo fill werkt.
* \[ ] SELL demo fill werkt alleen als demo balance/position genoeg is.
* \[ ] Min notional wordt gerespecteerd.
* \[ ] Step size wordt gerespecteerd.
* \[ ] Risk blocks worden zichtbaar uitgelegd.
* \[ ] Geen echte order endpoint wordt aangeroepen.
* \[ ] Tests bewijzen dat Binance signed endpoints niet worden gebruikt.

\---

## 10\. Fase 7 - Bot-generated demo trades zichtbaar maken

Doel: automatische paper fills van de bot duidelijk onderscheiden van handmatige demo trades.

### Taken

* \[ ] Voeg `trade\_origin` toe:

  * `bot\_signal`;
  * `manual\_demo`;
  * `testnet\_test\_order`;
  * `imported\_session`.
* \[ ] Chart markers:

  * manual demo BUY/SELL;
  * bot BUY/SELL;
  * blocked signal.
* \[ ] Fills table kolommen:

  * time;
  * origin;
  * side;
  * quantity;
  * price;
  * notional;
  * fee estimate;
  * model;
  * risk decision;
  * status.
* \[ ] Toggle:

  * show manual;
  * show bot;
  * show blocked;
  * show all.

### Acceptatiecriteria

* \[ ] Gebruiker ziet of trade door bot of handmatig kwam.
* \[ ] Bot signals zonder fill zijn zichtbaar als blocked/hold.
* \[ ] Fills blijven in session export.
* \[ ] Chart blijft leesbaar.

\---

## 11\. Fase 8 - Operator-friendly order lifecycle

Doel: JSON vervangen door duidelijke order/fill timeline.

### UI

* \[ ] Orders table.
* \[ ] Fills table.
* \[ ] Lifecycle timeline per order.
* \[ ] Status badges:

  * INTENT;
  * RISK\_BLOCKED;
  * PAPER\_FILLED;
  * TEST\_ORDER\_ACCEPTED;
  * UNKNOWN;
  * RECONCILE\_NEEDED.
* \[ ] Filter per session.
* \[ ] Export current table.

### Backend

* \[ ] `OrderLifecycleStore.list\_recent()` uitbreiden met human-friendly payload.
* \[ ] Manual demo fills koppelen aan lifecycle.
* \[ ] Bot paper fills koppelen aan lifecycle.
* \[ ] Testnet test-order accept koppelen aan lifecycle.

### Acceptatiecriteria

* \[ ] Orders tab is leesbaar zonder JSON.
* \[ ] Unknown/reconcile states zijn opvallend.
* \[ ] Demo fills krijgen lifecycle.
* \[ ] Export bevat geen secrets.

\---

## 12\. Fase 9 - Bot Control Center landing page

Doel: dashboard opent met een nuttige operator startpagina, niet direct een technische tab.

### Landing page blokken

* \[ ] Start bot engine.
* \[ ] Resume last session.
* \[ ] Start local demo.
* \[ ] Start Binance public Spot paper.
* \[ ] Open Demo Spot Trading.
* \[ ] Check credentials.
* \[ ] View last session report.
* \[ ] Open logs/security.
* \[ ] Safety summary.

### Acceptatiecriteria

* \[ ] Eerste scherm helpt gebruiker kiezen.
* \[ ] Gevaarlijke acties zijn niet prominent.
* \[ ] Local demo is aanbevolen eerste actie.
* \[ ] Live blijft onzichtbaar/disabled.

\---

## 13\. Fase 10 - Session resume en dashboard continuity

Doel: dashboard refresh of herstart mag niet verwarrend zijn.

### Taken

* \[ ] Dashboard detecteert recente running/stopped sessions.
* \[ ] Gebruiker kan:

  * resume visual session;
  * clone settings into new runtime;
  * export old session;
  * archive old session.
* \[ ] Runtime state wordt duidelijk:

  * current in-memory runtime;
  * historical session;
  * imported session.
* \[ ] Laatste gekozen mode/symbol/source wordt onthouden zonder secrets.

### Acceptatiecriteria

* \[ ] Dashboard refresh reset bot niet onverwacht.
* \[ ] Oude sessions zijn makkelijk te bekijken.
* \[ ] Nieuwe runtime wordt expliciet gestart.
* \[ ] Geen secrets in settings.

\---

## 14\. Fase 11 - Better dashboard performance

Doel: dashboard sneller en stabieler maken.

### Taken

* \[ ] Gebruik caching voor public symbol filters.
* \[ ] Gebruik caching voor static profile/settings data.
* \[ ] Candlestick chart niet volledig herbouwen als alleen metrics wijzigen.
* \[ ] Beperk audit tail render.
* \[ ] Beperk fills table render bij grote sessions.
* \[ ] Voeg pagination toe voor sessions/orders/fills.
* \[ ] Voeg refresh interval selector toe:

  * manual;
  * 1s;
  * 2s;
  * 5s.
* \[ ] Voeg “pause UI refresh” toe zonder bot te stoppen.

### Acceptatiecriteria

* \[ ] UI blijft bruikbaar bij lange demo sessies.
* \[ ] Geen onnodige runtime reset door rerun.
* \[ ] Grote fills table blijft snel.
* \[ ] Chart update voelt stabiel.

\---

## 15\. Fase 12 - Error UX en troubleshooting

Doel: fouten begrijpelijk maken.

### Dashboard errors

* \[ ] Binance unreachable.
* \[ ] Invalid symbol.
* \[ ] Min notional too low.
* \[ ] Quantity below min qty.
* \[ ] Spread too high.
* \[ ] Data stale.
* \[ ] Missing credentials.
* \[ ] Testnet profile mismatch.
* \[ ] Streamlit rerun/runtime error.
* \[ ] Port already used.
* \[ ] Python/dependency missing.

### Taken

* \[ ] Voeg `ui/errors.py` toe.
* \[ ] Voeg error catalog toe.
* \[ ] Elk probleem krijgt:

  * friendly title;
  * technical detail collapsed;
  * action button;
  * docs link.
* \[ ] Logs tab krijgt “copy diagnostics” knop zonder secrets.

### Acceptatiecriteria

* \[ ] Gebruiker begrijpt waarom trade geblokkeerd is.
* \[ ] Technical stack traces zijn niet hoofdweergave.
* \[ ] Diagnostics zijn redacted.
* \[ ] Troubleshooting docs zijn gelinkt.

\---

## 16\. Fase 13 - Nederlandse UX labels optie

Doel: gebruiker kan dashboard makkelijker begrijpen.

### Taken

* \[ ] Voeg `DashboardLanguage` toe:

  * `nl`;
  * `en`.
* \[ ] Belangrijkste labels vertalen:

  * Start bot engine;
  * Pause;
  * Emergency stop;
  * Demo Spot Trading;
  * Risk blocked;
  * Paper fill;
  * Live disabled;
  * Credentials;
  * Market data.
* \[ ] SettingsStore onthoudt taal.
* \[ ] Docs blijven technisch in Engels/Nederlands waar handig.

### Acceptatiecriteria

* \[ ] Nederlands is beschikbaar voor hoofdflow.
* \[ ] Engels blijft beschikbaar.
* \[ ] Technische values blijven exact.
* \[ ] Taalwissel reset runtime niet.

\---

## 17\. Fase 14 - Tests

### Unit tests

* \[ ] `tests/test\_control\_center.py`
* \[ ] `tests/test\_dashboard\_state.py`
* \[ ] `tests/test\_first\_run\_wizard.py`
* \[ ] `tests/test\_spot\_preview.py`
* \[ ] `tests/test\_manual\_demo\_trading.py`
* \[ ] `tests/test\_trade\_origin.py`
* \[ ] `tests/test\_dashboard\_errors.py`
* \[ ] `tests/test\_no\_live\_dashboard\_actions.py`

### Integration tests

* \[ ] Control center starts safe env.
* \[ ] Dashboard imports.
* \[ ] Demo trade BUY.
* \[ ] Demo trade SELL.
* \[ ] Min notional block.
* \[ ] Step size quantization.
* \[ ] Risk block shown in UI payload.
* \[ ] Session export contains manual demo fill.
* \[ ] No signed Binance endpoint called in demo trade.

### Browser/smoke tests

* \[ ] Start dashboard via `.cmd`.
* \[ ] First-run wizard visible.
* \[ ] Demo Spot Trading tab visible.
* \[ ] Start bot engine.
* \[ ] Execute demo BUY.
* \[ ] Fill appears on chart/table.
* \[ ] Emergency stop visible.
* \[ ] Live disabled visible.
* \[ ] No console errors.

\---

## 18\. Nieuwe bestanden

### Source

* \[ ] `src/binance\_spot\_bot/control\_center.py`
* \[ ] `src/binance\_spot\_bot/spot\_preview.py`
* \[ ] `src/binance\_spot\_bot/manual\_demo\_trading.py`
* \[ ] `src/binance\_spot\_bot/dashboard\_state.py`
* \[ ] `src/binance\_spot\_bot/ui/wizard.py`
* \[ ] `src/binance\_spot\_bot/ui/demo\_trading.py`
* \[ ] `src/binance\_spot\_bot/ui/order\_tables.py`
* \[ ] `src/binance\_spot\_bot/ui/errors.py`
* \[ ] `src/binance\_spot\_bot/ui/i18n.py`

### Docs

* \[ ] `docs/dashboard-safety-contract.md`
* \[ ] `docs/control-center-startflow.md`
* \[ ] `docs/first-run-wizard.md`
* \[ ] `docs/demo-spot-trading-dashboard.md`
* \[ ] `docs/manual-demo-trade-ticket.md`
* \[ ] `docs/dashboard-troubleshooting.md`

### Scripts

* \[ ] Update `Start Bot Dashboard.cmd`
* \[ ] Update `scripts/start-dashboard.ps1`
* \[ ] Update `scripts/stop-dashboard.ps1`
* \[ ] Optional: `scripts/open-control-center.ps1`

\---

## 19\. Prioriteiten

### Eerst bouwen

1. \[ ] Safety contract.
2. \[ ] Unified `control-center` launcher.
3. \[ ] Dashboard/bot engine state separation.
4. \[ ] First-run wizard.
5. \[ ] Demo Spot Trading tab.

### Daarna

6. \[ ] Spot market-data preview.
7. \[ ] Manual demo trade ticket.
8. \[ ] Human-friendly order lifecycle tables.
9. \[ ] Trade origin markers.
10. \[ ] Session resume/continuity.

### Als laatste

11. \[ ] Performance improvements.
12. \[ ] Error UX/troubleshooting.
13. \[ ] Nederlandse labels.
14. \[ ] Browser/smoke tests.

\---

## 20\. Definition of Done

Roadmap 009 is klaar als:

* \[ ] Eén command of dubbelklik start dashboard + control center veilig.
* \[ ] Dashboard maakt onderscheid tussen dashboard process en bot engine.
* \[ ] First-run wizard werkt.
* \[ ] Gebruiker kan local demo starten zonder keys.
* \[ ] Gebruiker kan Binance public Spot market data zien.
* \[ ] Gebruiker kan safe demo BUY/SELL uitvoeren in dashboard.
* \[ ] Demo fills verschijnen op chart en in fills table.
* \[ ] Bot-generated en manual demo trades zijn verschillend zichtbaar.
* \[ ] Risk blocks zijn duidelijk uitgelegd.
* \[ ] Orders/fills/lifecycle zijn leesbaar zonder raw JSON.
* \[ ] Session export bevat demo fills en lifecycle.
* \[ ] Geen demo trade roept signed/live Binance endpoints aan.
* \[ ] Live trading blijft onzichtbaar/disabled.
* \[ ] Tests en security scan slagen.
* \[ ] Docs zijn bijgewerkt.
* \[ ] Roadmap 009 kan na uitvoering naar `Voltooid docs`.

\---

## 21\. Verwachte Roadmap 010 daarna

Als Roadmap 009 klaar is, zou Roadmap 010 logisch gaan over:

* \[ ] mobile-friendly dashboard layout;
* \[ ] advanced charting;
* \[ ] strategy lab in dashboard;
* \[ ] drag-and-drop risk presets;
* \[ ] session comparison dashboards;
* \[ ] guided testnet order rehearsal;
* \[ ] dashboard plugin architecture.

Nog steeds zonder live trading standaard te activeren.

