# Codex Bouwvolgorde - Prioriteitenplan over Roadmap docs 005 t/m 014

Status: Aanbevolen bouwvolgorde voor Codex  
Project: Neural network Binance spot  
Datum: 2026-05-09  
Bestandsdoel:

```text
Roadmap docs/codex-build-priority-plan-roadmaps-005-014.md
```

Doel: bepalen wat Codex het beste eerst bouwt, in welke volgorde, met kleine veilige PR’s/tasks. Dit plan bouwt voort op Roadmap 005 t/m 014, maar bouwt ze niet blind numeriek. De volgorde is gekozen op basis van afhankelijkheden, veiligheid, ontwikkelsnelheid, testbaarheid en directe waarde voor het dashboard.

\---

## 0\. Hoofdconclusie

De beste Codex-bouwvolgorde is:

1. \[ ] **Safety + check-all + CI basis** uit Roadmap 013.
2. \[ ] **Unified dashboard/control-center startflow** uit Roadmap 009.
3. \[ ] **Dashboard demo Binance Spot trading** uit Roadmap 009.
4. \[ ] **Preflight + alerts + session reports + paper accounting** uit Roadmap 005.
5. \[ ] **Workspace, diagnostics, backup/restore** uit Roadmap 014.
6. \[ ] **Strategy Lab + risk/signal debugging + replay** uit Roadmap 010.
7. \[ ] **Copilot permissions/redaction + strategy templates** uit Roadmap 011.
8. \[ ] **Experiment DB + scanner history + notebook/HTML exports** uit Roadmap 012.
9. \[ ] **Multi-symbol portfolio paper + testnet endurance** uit Roadmap 006.
10. \[ ] **Evidence vault + shadow mode + chaos testing** uit Roadmap 007.
11. \[ ] **Strict live-readiness pilot design only** uit Roadmap 008.

Belangrijk: Roadmap 008 blijft design/audit. Geen live trading activeren.

\---

## 1\. Waarom niet gewoon roadmapnummer-volgorde?

Roadmap 005 is officieel de eerste geplande roadmap na de voltooide roadmaps. Maar daarna zijn er aanvullende roadmaps gemaakt rond dashboard, strategy lab, copilot, research workspace, CI en UX.

Voor Codex is de beste volgorde niet per roadmapnummer, maar per afhankelijkheid:

* \[ ] Eerst check/CI/testbasis, anders kan Codex makkelijk bestaande safety breken.
* \[ ] Daarna dashboard-startflow, want dat is de primaire gebruikservaring.
* \[ ] Daarna demo trading in dashboard, want dat geeft directe feedback.
* \[ ] Daarna paper-session/alerts/reports, zodat elke run meetbaar wordt.
* \[ ] Daarna research/AI/scanner/portfolio, omdat die stabiele sessies en reports nodig hebben.
* \[ ] Live-readiness pas als allerlaatste en alleen als ontwerp/audit.

\---

## 2\. Codex bouwregels

Gebruik Codex niet met één enorme opdracht zoals:

```text
Bouw Roadmap 005 t/m 014 volledig.
```

Dat is te groot en veroorzaakt rommel.

Gebruik in plaats daarvan:

* \[ ] één kleine branch per featuregroep;
* \[ ] één duidelijke acceptatiecheck per PR;
* \[ ] tests in dezelfde PR;
* \[ ] docs in dezelfde PR;
* \[ ] geen live trading;
* \[ ] geen secrets;
* \[ ] geen grote refactor tegelijk met features;
* \[ ] elke PR moet lokaal via `check-all` kunnen draaien.

Aanbevolen branch-stijl:

```text
codex/013-check-all-ci
codex/009-control-center-launcher
codex/009-demo-spot-trading-tab
codex/005-alerts-watchdog
codex/005-session-report-bundle
codex/014-workspaces-backup
codex/010-strategy-lab
```

\---

## 3\. Fase A - Eerst technische veiligheidsbasis bouwen

Bronroadmap: Roadmap 013  
Waarom eerst: alle latere Codex-taken moeten automatisch getest kunnen worden.

### A1. check-all runner

Taken:

* \[ ] `scripts/check-all.ps1`
* \[ ] `scripts/check-all.py`
* \[ ] `python -m binance\_spot\_bot.cli check-all`
* \[ ] checks:

  * unit tests;
  * config validation;
  * security scan;
  * dashboard import smoke;
  * CLI smoke;
  * no-live UI check;
  * no-secret artifact check.

Codex prompt:

```text
Implementeer alleen de check-all runner uit Roadmap 013. Voeg scripts/check-all.ps1, scripts/check-all.py en CLI command check-all toe. Gebruik bestaande unittest/ruff/security-scan/dashboard import checks. Voeg tests toe. Activeer geen live trading.
```

Acceptatie:

* \[ ] check-all draait lokaal.
* \[ ] dashboard import wordt getest.
* \[ ] live blijft disabled.
* \[ ] geen nieuwe featurecode buiten checks.

### A2. Safety regression tests

Taken:

* \[ ] `tests/safety/test\_no\_live\_ui.py`
* \[ ] `tests/safety/test\_no\_live\_cli.py`
* \[ ] test dat live niet selecteerbaar is.
* \[ ] test dat demo trade geen signed endpoint kan gebruiken.
* \[ ] test dat launcher `LIVE\_TRADING\_ENABLED=false` zet.

Acceptatie:

* \[ ] Safety tests falen als live UI/CLI zichtbaar wordt.
* \[ ] Safety tests draaien in check-all.

### A3. GitHub Actions CI

Taken:

* \[ ] `.github/workflows/ci.yml`
* \[ ] Windows + Ubuntu Python 3.12.
* \[ ] pytest.
* \[ ] ruff.
* \[ ] dashboard import smoke.
* \[ ] security scan.

Acceptatie:

* \[ ] CI gebruikt geen Binance credentials.
* \[ ] CI doet geen live calls.
* \[ ] PR kan pas groen zijn als safety tests slagen.

\---

## 4\. Fase B - Dashboard en bot-startflow samenbrengen

Bronroadmap: Roadmap 009  
Waarom nu: dit is de belangrijkste gebruikerswaarde en voorkomt verwarring tussen dashboard starten en bot starten.

### B1. Control-center launcher

Taken:

* \[ ] `src/binance\_spot\_bot/control\_center.py`
* \[ ] CLI command:

```powershell
python -m binance\_spot\_bot.cli control-center
```

* \[ ] kiest vrije poort;
* \[ ] zet safe env;
* \[ ] voert preflight/check uit;
* \[ ] start Streamlit;
* \[ ] opent browser;
* \[ ] schrijft PID/logs.

Codex prompt:

```text
Implementeer de Roadmap 009 control-center launcher. Bouw alleen de launcher en CLI command control-center. Hergebruik bestaande start-dashboard.ps1 gedrag. Forceer LIVE\_TRADING\_ENABLED=false en KILL\_SWITCH=true. Voeg tests toe voor port selectie, env flags en command output. Geen dashboard redesign in deze PR.
```

Acceptatie:

* \[ ] één command start dashboard veilig;
* \[ ] bestaande start scripts kunnen later hiernaar verwijzen;
* \[ ] PID/logs blijven werken;
* \[ ] live blijft disabled.

### B2. Dashboard/bot engine state separation

Taken:

* \[ ] `src/binance\_spot\_bot/dashboard\_state.py`
* \[ ] dashboard status:

  * starting;
  * running;
  * stopped;
  * unreachable.
* \[ ] bot engine status:

  * ready;
  * running;
  * paused;
  * stopped;
  * error.
* \[ ] header badges.

Acceptatie:

* \[ ] gebruiker ziet verschil tussen dashboard en bot engine;
* \[ ] reset bot sluit dashboard niet;
* \[ ] emergency stop blijft zichtbaar.

### B3. First-run wizard

Taken:

* \[ ] `src/binance\_spot\_bot/ui/wizard.py`
* \[ ] keuze:

  * local demo;
  * Binance public Spot paper;
  * Binance Demo Spot API;
  * Spot Testnet readiness.
* \[ ] symbol/source/risk preset/preflight.

Acceptatie:

* \[ ] nieuwe gebruiker kan local demo starten zonder keys;
* \[ ] wizard slaat geen secrets op;
* \[ ] live is geen optie.

\---

## 5\. Fase C - Demo Binance Spot trading zichtbaar en uitvoerbaar maken

Bronroadmap: Roadmap 009  
Waarom: gebruiker vroeg expliciet dat hij demo Binance Spot trading kan zien en uitvoeren in dashboard.

### C1. Spot market-data preview

Taken:

* \[ ] `src/binance\_spot\_bot/spot\_preview.py`
* \[ ] public market data:

  * price;
  * bid/ask;
  * spread;
  * klines;
  * symbol filters.
* \[ ] dashboard panel met status/fallback.

Acceptatie:

* \[ ] werkt zonder credentials;
* \[ ] toont filters zoals min notional/step size;
* \[ ] preview kan niet traden.

### C2. Demo Spot Trading tab

Taken:

* \[ ] `src/binance\_spot\_bot/ui/demo\_trading.py`
* \[ ] nieuwe dashboardtab:

  * chart;
  * trade ticket;
  * fills table;
  * account/position summary;
  * lifecycle table.

Acceptatie:

* \[ ] tab toont `DEMO/PAPER ONLY`;
* \[ ] fills verschijnen zichtbaar;
* \[ ] geen raw JSON als hoofdweergave.

### C3. Manual demo trade ticket

Taken:

* \[ ] `src/binance\_spot\_bot/manual\_demo\_trading.py`
* \[ ] BUY/SELL demo request.
* \[ ] preview:

  * qty;
  * notional;
  * fee/slippage estimate;
  * risk status.
* \[ ] execute alleen via paper/demo fill.
* \[ ] koppelen aan session/fills/lifecycle/audit.

Codex prompt:

```text
Implementeer manual demo trading uit Roadmap 009. Maak een ManualDemoTradeRequest, preview en result. Gebruik bestaande RiskEngine en ExecutionEngine alleen in PAPER/DISABLED-safe flow. Zorg dat geen Binance signed endpoint wordt aangeroepen. Voeg tests toe voor BUY, SELL, min notional, insufficient base en no signed endpoint.
```

Acceptatie:

* \[ ] demo BUY werkt;
* \[ ] demo SELL blokkeert zonder positie;
* \[ ] min notional werkt;
* \[ ] step size werkt;
* \[ ] geen signed endpoint.

\---

## 6\. Fase D - Preflight, alerts, reports en paper accounting

Bronroadmap: Roadmap 005  
Waarom: na demo trading moet elke run veilig meetbaar en verklaarbaar worden.

### D1. Preflight command en dashboard panel

Taken:

* \[ ] `python -m binance\_spot\_bot.cli preflight`
* \[ ] check:

  * config;
  * live disabled;
  * data dirs;
  * security scan;
  * dependencies;
  * credentials status;
  * connectivity optioneel.
* \[ ] dashboard preflight panel.

Acceptatie:

* \[ ] werkt zonder API keys;
* \[ ] toont testnet blockers;
* \[ ] blokkeert risicovolle flow.

### D2. AlertManager en Watchdog

Taken:

* \[ ] `src/binance\_spot\_bot/alerts.py`
* \[ ] severity:

  * info;
  * warning;
  * error;
  * critical.
* \[ ] watchdog actions:

  * observe;
  * block trading;
  * pause runtime;
  * stop runtime.

Acceptatie:

* \[ ] critical stopt demo/paper runtime;
* \[ ] error blokkeert execution;
* \[ ] alerts zichtbaar in dashboard;
* \[ ] alerts in session report.

### D3. Session report bundle

Taken:

* \[ ] `src/binance\_spot\_bot/session\_report.py`
* \[ ] outputs:

  * summary.md;
  * summary.json;
  * fills.csv;
  * equity.csv;
  * alerts.jsonl;
  * orders.jsonl;
  * config-redacted.json.

Acceptatie:

* \[ ] elke sessie exporteerbaar;
* \[ ] geen secrets;
* \[ ] genoeg info voor volgende roadmap.

### D4. Paper accounting

Taken:

* \[ ] `src/binance\_spot\_bot/paper\_accounting.py`
* \[ ] quote/base balances;
* \[ ] realized/unrealized PnL;
* \[ ] fees;
* \[ ] slippage;
* \[ ] exposure.

Acceptatie:

* \[ ] paper PnL verwerkt fees/slippage;
* \[ ] SELL zonder base blokkeert;
* \[ ] dashboard toont account state.

\---

## 7\. Fase E - Workspace, diagnostics, backup/restore

Bronroadmap: Roadmap 014  
Waarom: zodra dashboard en sessies werken, moet de gebruiker veilig kunnen werken met meerdere setups en backups.

### E1. Workspace profiles

Taken:

* \[ ] `src/binance\_spot\_bot/workspaces.py`
* \[ ] workspace:

  * name;
  * data\_dir;
  * profile;
  * symbol/watchlist;
  * risk preset;
  * theme;
  * language.
* \[ ] workspace selector in dashboard.

Acceptatie:

* \[ ] workspace switch is duidelijk;
* \[ ] geen secrets in workspace config;
* \[ ] workspace archive wist niets zonder confirm.

### E2. Backup/restore

Taken:

* \[ ] `src/binance\_spot\_bot/backup\_restore.py`
* \[ ] backup:

  * settings;
  * workspaces;
  * sessions;
  * reports;
  * experiment db later.
* \[ ] restore naar nieuwe workspace.

Acceptatie:

* \[ ] backup bevat geen secrets;
* \[ ] restore overschrijft niets zonder confirm;
* \[ ] manifest en hash aanwezig.

### E3. Diagnostics en support bundle

Taken:

* \[ ] `src/binance\_spot\_bot/diagnostics.py`
* \[ ] `src/binance\_spot\_bot/support\_bundle.py`
* \[ ] dashboard tab:

  * Python version;
  * deps;
  * data dir;
  * logs;
  * dashboard status;
  * latest errors;
  * public connectivity.

Acceptatie:

* \[ ] copy diagnostics redacted;
* \[ ] support bundle is zip met manifest;
* \[ ] geen secrets.

\---

## 8\. Fase F - Strategy Lab en debugging

Bronroadmap: Roadmap 010  
Waarom: pas bouwen nadat sessions/fills/reports betrouwbaar zijn.

### F1. Risk decision debugger

Taken:

* \[ ] `src/binance\_spot\_bot/risk\_debugger.py`
* \[ ] uitleg per block reason.
* \[ ] dashboard timeline.

Acceptatie:

* \[ ] iedere BLOCK heeft duidelijke reden;
* \[ ] debugger kan risk niet omzeilen.

### F2. Signal explanation panel

Taken:

* \[ ] `src/binance\_spot\_bot/signal\_explainer.py`
* \[ ] uitleg:

  * signal;
  * confidence;
  * features;
  * model version.

Acceptatie:

* \[ ] signaal is klikbaar/inspecteerbaar;
* \[ ] deterministic, geen AI nodig.

### F3. Replay sandbox

Taken:

* \[ ] `src/binance\_spot\_bot/replay\_sandbox.py`
* \[ ] oude sessie laden;
* \[ ] timeline scrubber;
* \[ ] replay chart.

Acceptatie:

* \[ ] oude sessie replay wijzigt niets;
* \[ ] werkt offline.

### F4. Session comparison

Taken:

* \[ ] `src/binance\_spot\_bot/session\_compare.py`
* \[ ] vergelijk:

  * PnL;
  * drawdown;
  * trades;
  * blocks;
  * alerts;
  * data quality.

Acceptatie:

* \[ ] 2-10 sessies vergelijken;
* \[ ] exporteerbaar rapport.

\---

## 9\. Fase G - Copilot, templates en dataset/model wizards

Bronroadmap: Roadmap 011  
Waarom: AI/copilot pas bouwen nadat redaction, reports en debugging bestaan.

### G1. Copilot permissions en redaction

Taken:

* \[ ] `copilot\_permissions.py`
* \[ ] `copilot\_redaction.py`
* \[ ] verboden:

  * place\_order;
  * cancel\_order;
  * enable\_live;
  * bypass\_risk;
  * read\_api\_secret.

Acceptatie:

* \[ ] copilot kan geen orderpad raken;
* \[ ] fake secrets worden geredact.

### G2. Rule-based copilot summary

Taken:

* \[ ] sessie samenvatting zonder externe AI.
* \[ ] risk block uitleg.
* \[ ] next safe steps.

Acceptatie:

* \[ ] werkt offline;
* \[ ] geen secrets;
* \[ ] output is advisory.

### G3. Strategy templates

Taken:

* \[ ] `strategy\_templates.py`
* \[ ] templates:

  * no trade;
  * buy hold;
  * momentum;
  * mean reversion;
  * confidence threshold.

Acceptatie:

* \[ ] templates demo/paper-first;
* \[ ] niet automatisch toepassen.

### G4. Dataset Builder UI en Model Training Wizard

Taken:

* \[ ] dataset builder;
* \[ ] model training wizard;
* \[ ] candidate model registry;
* \[ ] baseline comparison.

Acceptatie:

* \[ ] geen champion automatisch;
* \[ ] geen train-only promotie;
* \[ ] metrics opgeslagen.

\---

## 10\. Fase H - Experiment database, scanner UX en exports

Bronroadmap: Roadmap 012  
Waarom: nuttig nadat strategy lab/templates/reports bestaan.

### H1. Experiment database

Taken:

* \[ ] `experiment\_db.py`
* \[ ] JSON fallback;
* \[ ] SQLite optional;
* \[ ] index sessions/models/datasets/reports.

Acceptatie:

* \[ ] oude sessions indexeerbaar;
* \[ ] geen secrets.

### H2. Advanced scanner UX

Taken:

* \[ ] scanner dashboard;
* \[ ] watchlist ranking;
* \[ ] spread/volume/signal/confidence grid.
* \[ ] scanner history.

Acceptatie:

* \[ ] scanner plaatst geen orders;
* \[ ] run wordt experiment record.

### H3. Notebook en HTML exports

Taken:

* \[ ] `notebook\_export.py`
* \[ ] `html\_reports.py`
* \[ ] session/strategy/scanner/model reports.

Acceptatie:

* \[ ] opent lokaal;
* \[ ] geen secrets;
* \[ ] reproduceerbaar.

### H4. Dashboard performance/cache manager

Taken:

* \[ ] dashboard profiler;
* \[ ] cache manager;
* \[ ] data archive/cleanup.

Acceptatie:

* \[ ] geen actieve sessions wissen;
* \[ ] cache manifest.

\---

## 11\. Fase I - Multi-symbol portfolio en testnet endurance

Bronroadmap: Roadmap 006  
Waarom pas nadat scanner, accounting, session reports en alerts stabiel zijn.

### I1. Portfolio state

Taken:

* \[ ] `portfolio.py`
* \[ ] balances per asset;
* \[ ] positions per symbol;
* \[ ] total equity;
* \[ ] total exposure.

Acceptatie:

* \[ ] BTCUSDT/ETHUSDT/BNBUSDT in één portfolio;
* \[ ] fees/slippage per symbol.

### I2. Portfolio risk

Taken:

* \[ ] portfolio-wide max exposure;
* \[ ] max open positions;
* \[ ] max daily portfolio loss;
* \[ ] per-symbol cooldown.

Acceptatie:

* \[ ] voorkomt alle symbols tegelijk maximaal BUY;
* \[ ] global loss blokkeert nieuwe entries.

### I3. Portfolio paper session

Taken:

* \[ ] `portfolio-paper-session`
* \[ ] report export.

Acceptatie:

* \[ ] demo works without internet;
* \[ ] no live mode.

### I4. Testnet endurance

Taken:

* \[ ] guarded testnet endurance;
* \[ ] max orders;
* \[ ] reconciliation;
* \[ ] cancel open.

Acceptatie:

* \[ ] geen live URL;
* \[ ] unresolved orders zichtbaar.

\---

## 12\. Fase J - Evidence, shadow mode en chaos testing

Bronroadmap: Roadmap 007  
Waarom pas na echte sessies, reports en endurance.

### J1. Evidence vault

Taken:

* \[ ] `evidence.py`
* \[ ] add/list/export/verify records.

Acceptatie:

* \[ ] hash verificatie;
* \[ ] no secrets.

### J2. Shadow mode

Taken:

* \[ ] `shadow.py`
* \[ ] live/public market data lezen;
* \[ ] would-be orders loggen;
* \[ ] geen signed endpoints.

Acceptatie:

* \[ ] tests bewijzen `place\_order()` nooit aangeroepen.

### J3. Chaos testing

Taken:

* \[ ] `chaos.py`
* \[ ] simuleer:

  * 429;
  * 418;
  * 5xx;
  * websocket disconnect;
  * stale data;
  * write failure;
  * unknown order.

Acceptatie:

* \[ ] critical failures stoppen runtime veilig.

### J4. Readiness scorecard

Taken:

* \[ ] `readiness.py`
* \[ ] R0-R5 score.

Acceptatie:

* \[ ] evidence-based;
* \[ ] kan live niet groen maken zonder bewijs.

\---

## 13\. Fase K - Live-readiness pilot design

Bronroadmap: Roadmap 008  
Waarom laatst, en alleen als design.

### Taken

* \[ ] evidence gate;
* \[ ] live pilot policy document;
* \[ ] account safety checklist;
* \[ ] manual approval design;
* \[ ] live dry-run design;
* \[ ] no-go criteria;
* \[ ] pilot simulation report.

Acceptatie:

* \[ ] geen live uitvoering;
* \[ ] alleen ontwerp;
* \[ ] live blijft disabled.

\---

## 14\. Concrete Codex sprintindeling

### Sprint 1 - Safety foundation

* \[ ] check-all runner.
* \[ ] safety regression tests.
* \[ ] CI workflow.
* \[ ] dashboard import smoke.
* \[ ] no-live tests.

### Sprint 2 - Control Center MVP

* \[ ] control-center launcher.
* \[ ] dashboard/bot engine status.
* \[ ] first-run wizard MVP.
* \[ ] safe mode badges.

### Sprint 3 - Demo Spot Trading MVP

* \[ ] spot preview.
* \[ ] demo trading tab.
* \[ ] manual demo BUY/SELL.
* \[ ] fills table.
* \[ ] session write.

### Sprint 4 - Runtime reliability

* \[ ] preflight command.
* \[ ] alerts/watchdog.
* \[ ] session report bundle.
* \[ ] paper accounting.

### Sprint 5 - User workspace reliability

* \[ ] workspace profiles.
* \[ ] backup/restore.
* \[ ] diagnostics.
* \[ ] support bundle.

### Sprint 6 - Strategy Lab MVP

* \[ ] risk debugger.
* \[ ] signal explainer.
* \[ ] replay sandbox.
* \[ ] session comparison.

### Sprint 7 - Copilot/templates

* \[ ] copilot permissions.
* \[ ] redaction.
* \[ ] local summaries.
* \[ ] strategy templates.

### Sprint 8 - Research workspace

* \[ ] experiment DB.
* \[ ] scanner UX/history.
* \[ ] notebook/HTML exports.
* \[ ] cache/performance tools.

### Sprint 9 - Portfolio/testnet

* \[ ] portfolio state.
* \[ ] portfolio risk.
* \[ ] portfolio paper session.
* \[ ] testnet endurance.

### Sprint 10 - Evidence/readiness

* \[ ] evidence vault.
* \[ ] shadow mode.
* \[ ] chaos tests.
* \[ ] readiness scorecard.

\---

## 15\. Wat Codex absoluut niet eerst moet doen

Niet starten met:

* \[ ] Roadmap 008 live-readiness pilot design.
* \[ ] Copilot met AI API zonder redaction.
* \[ ] Portfolio trading zonder paper accounting.
* \[ ] Testnet endurance zonder order lifecycle/reports.
* \[ ] Plugin architecture zonder sandboxing.
* \[ ] Modeltraining wizard zonder dataset manifests.
* \[ ] Scanner auto-trading.
* \[ ] Live trading.
* \[ ] Grote dashboard rewrite zonder tests.

\---

## 16\. Beste eerste Codex-opdracht

De allerbeste eerste opdracht:

```text
Implementeer Roadmap 013 Fase 1 + Fase 5: local check-all runner en safety regression tests.
Maak scripts/check-all.ps1, scripts/check-all.py en CLI command check-all.
Laat check-all unit tests, config validation, security scan, dashboard import smoke en no-live checks draaien.
Voeg tests toe die bewijzen dat live niet in dashboard/CLI safe commands selecteerbaar is.
Geen featurewijzigingen, geen live trading.
```

Waarom:

* \[ ] maakt alle latere Codex-output controleerbaar;
* \[ ] voorkomt safety regressions;
* \[ ] klein genoeg voor één PR;
* \[ ] direct nuttig voor elke volgende roadmap.

\---

## 17\. Tweede Codex-opdracht

```text
Implementeer Roadmap 009 Control Center launcher.
Maak src/binance\_spot\_bot/control\_center.py en CLI command control-center.
Herbruik de bestaande dashboard startflow, kies vrije poort, forceer LIVE\_TRADING\_ENABLED=false en KILL\_SWITCH=true, schrijf PID/logs en open browser.
Voeg tests toe voor env flags, port selectie en command output.
```

\---

## 18\. Derde Codex-opdracht

```text
Implementeer Roadmap 009 Demo Spot Trading MVP.
Maak spot\_preview.py, manual\_demo\_trading.py en een eenvoudige Demo Spot Trading tab.
Toon BTCUSDT public/demo price, bid/ask, spread en symbol filters.
Voeg een safe manual demo BUY/SELL ticket toe dat alleen paper fills maakt.
Voeg tests toe voor BUY, SELL, min notional, insufficient base en geen signed endpoint.
```

\---

## 19\. Definition of Ready voor elke Codex taak

Elke taak moet vóór start hebben:

* \[ ] Eén duidelijke roadmapfase.
* \[ ] Eén branchnaam.
* \[ ] Eén acceptatielijst.
* \[ ] Tests die erbij horen.
* \[ ] Geen live trading.
* \[ ] Geen secrets.
* \[ ] Geen grote refactor buiten scope.
* \[ ] Duidelijke files die aangepast mogen worden.

\---

## 20\. Definition of Done voor elke Codex PR

Elke Codex PR is pas klaar als:

* \[ ] tests slagen;
* \[ ] check-all slaagt;
* \[ ] safety tests slagen;
* \[ ] docs bijgewerkt zijn;
* \[ ] geen secrets in generated files;
* \[ ] live disabled blijft;
* \[ ] acceptatiecriteria afgevinkt zijn;
* \[ ] geen onnodige files gewijzigd zijn;
* \[ ] roadmap taak gemarkeerd kan worden als deels/voltooid.

\---

## 21\. Samenvatting voor Codex

Kortste bouwvolgorde:

```text
013 safety/checks
→ 009 launcher/dashboard/demo trading
→ 005 preflight/alerts/reports/accounting
→ 014 workspaces/backup/diagnostics
→ 010 strategy lab/debug/replay
→ 011 copilot/templates/wizards
→ 012 experiment DB/scanner/exports/performance
→ 006 portfolio/testnet endurance
→ 007 evidence/shadow/chaos
→ 008 live-readiness design only
```

Dit is de veiligste en meest efficiënte bouwvolgorde.

