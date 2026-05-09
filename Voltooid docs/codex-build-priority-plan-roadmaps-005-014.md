# Codex Bouwvolgorde - Prioriteitenplan over Roadmap docs 005 t/m 014

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-09  
Bestandsdoel:

```text
Roadmap docs/codex-build-priority-plan-roadmaps-005-014.md
```

Doel: bepalen wat Codex het beste eerst bouwt, in welke volgorde, met kleine veilige PR’s/tasks. Dit plan bouwt voort op Roadmap 005 t/m 014, maar bouwt ze niet blind numeriek. De volgorde is gekozen op basis van afhankelijkheden, veiligheid, ontwikkelsnelheid, testbaarheid en directe waarde voor het dashboard.

Voortgangsnotitie:
- Prioriteit 1 is uitgevoerd: Roadmap 013 check-all runner, safety regression tests en CI-basis.
- Toegevoegd: `scripts/check-all.py`, `scripts/check-all.ps1`, `python -m binance_spot_bot.cli check-all`, dashboard import smoke, CLI smoke, no-live checks en no-secret artifact checks.
- Toegevoegd: `.github/workflows/ci.yml` voor Windows + Ubuntu Python 3.12.
- Aansluitend toegevoegd: `src/binance_spot_bot/control_center.py` en `python -m binance_spot_bot.cli control-center --dry-run` als veilige launcher-hook.
- Verificatie: `check-all` draait groen met 42 unit tests, config validation, security scan, dashboard import smoke, CLI smoke, no-live UI en no-secret artifact check.
- Prioriteit 2 en 3 zijn uitgevoerd als veilige MVP: dashboard/bot state separation, first-run wizard data, Spot preview, Demo Spot Trading tab en local-only manual demo fills.
- Prioriteit 4 is als backendbasis uitgevoerd: preflight command/panel, alerts/watchdog primitives, session report bundle en paper accounting.
- Prioriteit 5 is als lokale betrouwbaarheidsbasis uitgevoerd: workspace profiles, redacted backup/restore, diagnostics en support bundle.
- Prioriteit 6 t/m 11 zijn uitgevoerd als veilige MVP-bouwstenen: Strategy Lab, copilot guardrails, experiment/scanner exports, portfolio paper/testnet endurance guard, evidence/shadow/chaos/readiness en live-readiness design-only policy.
- Verificatie: `check-all` draait groen met 67 unit tests, config validation, security scan, dashboard import smoke, CLI smoke, no-live UI en no-secret artifact check.
- Live trading blijft disabled; Roadmap 008 is uitsluitend als design/audit uitgevoerd.

\---

## 0\. Hoofdconclusie

De beste Codex-bouwvolgorde is:

1. \[x] **Safety + check-all + CI basis** uit Roadmap 013.
2. \[x] **Unified dashboard/control-center startflow** uit Roadmap 009.
3. \[x] **Dashboard demo Binance Spot trading** uit Roadmap 009.
4. \[x] **Preflight + alerts + session reports + paper accounting** uit Roadmap 005.
5. \[x] **Workspace, diagnostics, backup/restore** uit Roadmap 014.
6. \[x] **Strategy Lab + risk/signal debugging + replay** uit Roadmap 010.
7. \[x] **Copilot permissions/redaction + strategy templates** uit Roadmap 011.
8. \[x] **Experiment DB + scanner history + notebook/HTML exports** uit Roadmap 012.
9. \[x] **Multi-symbol portfolio paper + testnet endurance** uit Roadmap 006.
10. \[x] **Evidence vault + shadow mode + chaos testing** uit Roadmap 007.
11. \[x] **Strict live-readiness pilot design only** uit Roadmap 008.

Belangrijk: Roadmap 008 blijft design/audit. Geen live trading activeren.

\---

## 1\. Waarom niet gewoon roadmapnummer-volgorde?

Roadmap 005 is officieel de eerste geplande roadmap na de voltooide roadmaps. Maar daarna zijn er aanvullende roadmaps gemaakt rond dashboard, strategy lab, copilot, research workspace, CI en UX.

Voor Codex is de beste volgorde niet per roadmapnummer, maar per afhankelijkheid:

* \[x] Eerst check/CI/testbasis, anders kan Codex makkelijk bestaande safety breken.
* \[x] Daarna dashboard-startflow, want dat is de primaire gebruikservaring.
* \[x] Daarna demo trading in dashboard, want dat geeft directe feedback.
* \[x] Daarna paper-session/alerts/reports, zodat elke run meetbaar wordt.
* \[x] Daarna research/AI/scanner/portfolio, omdat die stabiele sessies en reports nodig hebben.
* \[x] Live-readiness pas als allerlaatste en alleen als ontwerp/audit.

\---

## 2\. Codex bouwregels

Gebruik Codex niet met één enorme opdracht zoals:

```text
Bouw Roadmap 005 t/m 014 volledig.
```

Dat is te groot en veroorzaakt rommel.

Gebruik in plaats daarvan:

* \[x] één kleine branch per featuregroep;
* \[x] één duidelijke acceptatiecheck per PR;
* \[x] tests in dezelfde PR;
* \[x] docs in dezelfde PR;
* \[x] geen live trading;
* \[x] geen secrets;
* \[x] geen grote refactor tegelijk met features;
* \[x] elke PR moet lokaal via `check-all` kunnen draaien.

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

* \[x] `scripts/check-all.ps1`
* \[x] `scripts/check-all.py`
* \[x] `python -m binance\_spot\_bot.cli check-all`
* \[x] checks:

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

* \[x] check-all draait lokaal.
* \[x] dashboard import wordt getest.
* \[x] live blijft disabled.
* \[x] geen nieuwe featurecode buiten checks.

### A2. Safety regression tests

Taken:

* \[x] `tests/safety/test\_no\_live\_ui.py`
* \[x] `tests/safety/test\_no\_live\_cli.py`
* \[x] test dat live niet selecteerbaar is.
* \[x] test dat demo trade geen signed endpoint kan gebruiken.
* \[x] test dat launcher `LIVE\_TRADING\_ENABLED=false` zet.

Acceptatie:

* \[x] Safety tests falen als live UI/CLI zichtbaar wordt.
* \[x] Safety tests draaien in check-all.

### A3. GitHub Actions CI

Taken:

* \[x] `.github/workflows/ci.yml`
* \[x] Windows + Ubuntu Python 3.12.
* \[x] unittest/check-all.
* \[x] ruff.
* \[x] dashboard import smoke.
* \[x] security scan.

Acceptatie:

* \[x] CI gebruikt geen Binance credentials.
* \[x] CI doet geen live calls.
* \[x] PR kan pas groen zijn als safety tests slagen.

\---

## 4\. Fase B - Dashboard en bot-startflow samenbrengen

Bronroadmap: Roadmap 009  
Waarom nu: dit is de belangrijkste gebruikerswaarde en voorkomt verwarring tussen dashboard starten en bot starten.

### B1. Control-center launcher

Taken:

* \[x] `src/binance\_spot\_bot/control\_center.py`
* \[x] CLI command:

```powershell
python -m binance\_spot\_bot.cli control-center
```

* \[x] kiest vrije poort;
* \[x] zet safe env;
* \[x] voert preflight/check uit;
* \[x] start Streamlit;
* \[x] opent browser;
* \[x] schrijft PID/logs.

Codex prompt:

```text
Implementeer de Roadmap 009 control-center launcher. Bouw alleen de launcher en CLI command control-center. Hergebruik bestaande start-dashboard.ps1 gedrag. Forceer LIVE\_TRADING\_ENABLED=false en KILL\_SWITCH=true. Voeg tests toe voor port selectie, env flags en command output. Geen dashboard redesign in deze PR.
```

Acceptatie:

* \[x] één command start dashboard veilig;
* \[x] bestaande start scripts kunnen later hiernaar verwijzen;
* \[x] PID/logs blijven werken;
* \[x] live blijft disabled.

### B2. Dashboard/bot engine state separation

Taken:

* \[x] `src/binance\_spot\_bot/dashboard\_state.py`
* \[x] dashboard status:

  * starting;
  * running;
  * stopped;
  * unreachable.
* \[x] bot engine status:

  * ready;
  * running;
  * paused;
  * stopped;
  * error.
* \[x] header badges.

Acceptatie:

* \[x] gebruiker ziet verschil tussen dashboard en bot engine;
* \[x] reset bot sluit dashboard niet;
* \[x] emergency stop blijft zichtbaar.

### B3. First-run wizard

Taken:

* \[x] `src/binance\_spot\_bot/ui/wizard.py`
* \[x] keuze:

  * local demo;
  * Binance public Spot paper;
  * Binance Demo Spot API;
  * Spot Testnet readiness.
* \[x] symbol/source/risk preset/preflight.

Acceptatie:

* \[x] nieuwe gebruiker kan local demo starten zonder keys;
* \[x] wizard slaat geen secrets op;
* \[x] live is geen optie.

\---

## 5\. Fase C - Demo Binance Spot trading zichtbaar en uitvoerbaar maken

Bronroadmap: Roadmap 009  
Waarom: gebruiker vroeg expliciet dat hij demo Binance Spot trading kan zien en uitvoeren in dashboard.

### C1. Spot market-data preview

Taken:

* \[x] `src/binance\_spot\_bot/spot\_preview.py`
* \[x] public market data:

  * price;
  * bid/ask;
  * spread;
  * klines;
  * symbol filters.
* \[x] dashboard panel met status/fallback.

Acceptatie:

* \[x] werkt zonder credentials;
* \[x] toont filters zoals min notional/step size;
* \[x] preview kan niet traden.

### C2. Demo Spot Trading tab

Taken:

* \[x] `src/binance\_spot\_bot/ui/demo\_trading.py`
* \[x] nieuwe dashboardtab:

  * chart;
  * trade ticket;
  * fills table;
  * account/position summary;
  * lifecycle table.

Acceptatie:

* \[x] tab toont `DEMO/PAPER ONLY`;
* \[x] fills verschijnen zichtbaar;
* \[x] geen raw JSON als hoofdweergave.

### C3. Manual demo trade ticket

Taken:

* \[x] `src/binance\_spot\_bot/manual\_demo\_trading.py`
* \[x] BUY/SELL demo request.
* \[x] preview:

  * qty;
  * notional;
  * fee/slippage estimate;
  * risk status.
* \[x] execute alleen via paper/demo fill.
* \[x] koppelen aan session/fills/lifecycle/audit.

Codex prompt:

```text
Implementeer manual demo trading uit Roadmap 009. Maak een ManualDemoTradeRequest, preview en result. Gebruik bestaande RiskEngine en ExecutionEngine alleen in PAPER/DISABLED-safe flow. Zorg dat geen Binance signed endpoint wordt aangeroepen. Voeg tests toe voor BUY, SELL, min notional, insufficient base en no signed endpoint.
```

Acceptatie:

* \[x] demo BUY werkt;
* \[x] demo SELL blokkeert zonder positie;
* \[x] min notional werkt;
* \[x] step size werkt;
* \[x] geen signed endpoint.

\---

## 6\. Fase D - Preflight, alerts, reports en paper accounting

Bronroadmap: Roadmap 005  
Waarom: na demo trading moet elke run veilig meetbaar en verklaarbaar worden.

### D1. Preflight command en dashboard panel

Taken:

* \[x] `python -m binance\_spot\_bot.cli preflight`
* \[x] check:

  * config;
  * live disabled;
  * data dirs;
  * security scan;
  * dependencies;
  * credentials status;
  * connectivity optioneel.
* \[x] dashboard preflight panel.

Acceptatie:

* \[x] werkt zonder API keys;
* \[x] toont testnet blockers;
* \[x] blokkeert risicovolle flow.

### D2. AlertManager en Watchdog

Taken:

* \[x] `src/binance\_spot\_bot/alerts.py`
* \[x] severity:

  * info;
  * warning;
  * error;
  * critical.
* \[x] watchdog actions:

  * observe;
  * block trading;
  * pause runtime;
  * stop runtime.

Acceptatie:

* \[x] critical stopt demo/paper runtime;
* \[x] error blokkeert execution;
* \[x] alerts zichtbaar in dashboard;
* \[x] alerts in session report.

### D3. Session report bundle

Taken:

* \[x] `src/binance\_spot\_bot/session\_report.py`
* \[x] outputs:

  * summary.md;
  * summary.json;
  * fills.csv;
  * equity.csv;
  * alerts.jsonl;
  * orders.jsonl;
  * config-redacted.json.

Acceptatie:

* \[x] elke sessie exporteerbaar;
* \[x] geen secrets;
* \[x] genoeg info voor volgende roadmap.

### D4. Paper accounting

Taken:

* \[x] `src/binance\_spot\_bot/paper\_accounting.py`
* \[x] quote/base balances;
* \[x] realized/unrealized PnL;
* \[x] fees;
* \[x] slippage;
* \[x] exposure.

Acceptatie:

* \[x] paper PnL verwerkt fees/slippage;
* \[x] SELL zonder base blokkeert;
* \[x] dashboard toont account state.

\---

## 7\. Fase E - Workspace, diagnostics, backup/restore

Bronroadmap: Roadmap 014  
Waarom: zodra dashboard en sessies werken, moet de gebruiker veilig kunnen werken met meerdere setups en backups.

### E1. Workspace profiles

Taken:

* \[x] `src/binance\_spot\_bot/workspaces.py`
* \[x] workspace:

  * name;
  * data\_dir;
  * profile;
  * symbol/watchlist;
  * risk preset;
  * theme;
  * language.
* \[x] workspace selector in dashboard.

Acceptatie:

* \[x] workspace switch is duidelijk;
* \[x] geen secrets in workspace config;
* \[x] workspace archive wist niets zonder confirm.

### E2. Backup/restore

Taken:

* \[x] `src/binance\_spot\_bot/backup\_restore.py`
* \[x] backup:

  * settings;
  * workspaces;
  * sessions;
  * reports;
  * experiment db later.
* \[x] restore naar nieuwe workspace.

Acceptatie:

* \[x] backup bevat geen secrets;
* \[x] restore overschrijft niets zonder confirm;
* \[x] manifest en hash aanwezig.

### E3. Diagnostics en support bundle

Taken:

* \[x] `src/binance\_spot\_bot/diagnostics.py`
* \[x] `src/binance\_spot\_bot/support\_bundle.py`
* \[x] dashboard tab:

  * Python version;
  * deps;
  * data dir;
  * logs;
  * dashboard status;
  * latest errors;
  * public connectivity.

Acceptatie:

* \[x] copy diagnostics redacted;
* \[x] support bundle is zip met manifest;
* \[x] geen secrets.

\---

## 8\. Fase F - Strategy Lab en debugging

Bronroadmap: Roadmap 010  
Waarom: pas bouwen nadat sessions/fills/reports betrouwbaar zijn.

### F1. Risk decision debugger

Taken:

* \[x] `src/binance\_spot\_bot/risk\_debugger.py`
* \[x] uitleg per block reason.
* \[x] dashboard timeline.

Acceptatie:

* \[x] iedere BLOCK heeft duidelijke reden;
* \[x] debugger kan risk niet omzeilen.

### F2. Signal explanation panel

Taken:

* \[x] `src/binance\_spot\_bot/signal\_explainer.py`
* \[x] uitleg:

  * signal;
  * confidence;
  * features;
  * model version.

Acceptatie:

* \[x] signaal is klikbaar/inspecteerbaar;
* \[x] deterministic, geen AI nodig.

### F3. Replay sandbox

Taken:

* \[x] `src/binance\_spot\_bot/replay\_sandbox.py`
* \[x] oude sessie laden;
* \[x] timeline scrubber;
* \[x] replay chart.

Acceptatie:

* \[x] oude sessie replay wijzigt niets;
* \[x] werkt offline.

### F4. Session comparison

Taken:

* \[x] `src/binance\_spot\_bot/session\_compare.py`
* \[x] vergelijk:

  * PnL;
  * drawdown;
  * trades;
  * blocks;
  * alerts;
  * data quality.

Acceptatie:

* \[x] 2-10 sessies vergelijken;
* \[x] exporteerbaar rapport.

\---

## 9\. Fase G - Copilot, templates en dataset/model wizards

Bronroadmap: Roadmap 011  
Waarom: AI/copilot pas bouwen nadat redaction, reports en debugging bestaan.

### G1. Copilot permissions en redaction

Taken:

* \[x] `copilot\_permissions.py`
* \[x] `copilot\_redaction.py`
* \[x] verboden:

  * place\_order;
  * cancel\_order;
  * enable\_live;
  * bypass\_risk;
  * read\_api\_secret.

Acceptatie:

* \[x] copilot kan geen orderpad raken;
* \[x] fake secrets worden geredact.

### G2. Rule-based copilot summary

Taken:

* \[x] sessie samenvatting zonder externe AI.
* \[x] risk block uitleg.
* \[x] next safe steps.

Acceptatie:

* \[x] werkt offline;
* \[x] geen secrets;
* \[x] output is advisory.

### G3. Strategy templates

Taken:

* \[x] `strategy\_templates.py`
* \[x] templates:

  * no trade;
  * buy hold;
  * momentum;
  * mean reversion;
  * confidence threshold.

Acceptatie:

* \[x] templates demo/paper-first;
* \[x] niet automatisch toepassen.

### G4. Dataset Builder UI en Model Training Wizard

Taken:

* \[x] dataset builder;
* \[x] model training wizard;
* \[x] candidate model registry;
* \[x] baseline comparison.

Acceptatie:

* \[x] geen champion automatisch;
* \[x] geen train-only promotie;
* \[x] metrics opgeslagen.

\---

## 10\. Fase H - Experiment database, scanner UX en exports

Bronroadmap: Roadmap 012  
Waarom: nuttig nadat strategy lab/templates/reports bestaan.

### H1. Experiment database

Taken:

* \[x] `experiment\_db.py`
* \[x] JSON fallback;
* \[x] SQLite optional;
* \[x] index sessions/models/datasets/reports.

Acceptatie:

* \[x] oude sessions indexeerbaar;
* \[x] geen secrets.

### H2. Advanced scanner UX

Taken:

* \[x] scanner dashboard;
* \[x] watchlist ranking;
* \[x] spread/volume/signal/confidence grid.
* \[x] scanner history.

Acceptatie:

* \[x] scanner plaatst geen orders;
* \[x] run wordt experiment record.

### H3. Notebook en HTML exports

Taken:

* \[x] `notebook\_export.py`
* \[x] `html\_reports.py`
* \[x] session/strategy/scanner/model reports.

Acceptatie:

* \[x] opent lokaal;
* \[x] geen secrets;
* \[x] reproduceerbaar.

### H4. Dashboard performance/cache manager

Taken:

* \[x] dashboard profiler;
* \[x] cache manager;
* \[x] data archive/cleanup.

Acceptatie:

* \[x] geen actieve sessions wissen;
* \[x] cache manifest.

\---

## 11\. Fase I - Multi-symbol portfolio en testnet endurance

Bronroadmap: Roadmap 006  
Waarom pas nadat scanner, accounting, session reports en alerts stabiel zijn.

### I1. Portfolio state

Taken:

* \[x] `portfolio.py`
* \[x] balances per asset;
* \[x] positions per symbol;
* \[x] total equity;
* \[x] total exposure.

Acceptatie:

* \[x] BTCUSDT/ETHUSDT/BNBUSDT in één portfolio;
* \[x] fees/slippage per symbol.

### I2. Portfolio risk

Taken:

* \[x] portfolio-wide max exposure;
* \[x] max open positions;
* \[x] max daily portfolio loss;
* \[x] per-symbol cooldown.

Acceptatie:

* \[x] voorkomt alle symbols tegelijk maximaal BUY;
* \[x] global loss blokkeert nieuwe entries.

### I3. Portfolio paper session

Taken:

* \[x] `portfolio-paper-session`
* \[x] report export.

Acceptatie:

* \[x] demo works without internet;
* \[x] no live mode.

### I4. Testnet endurance

Taken:

* \[x] guarded testnet endurance;
* \[x] max orders;
* \[x] reconciliation;
* \[x] cancel open.

Acceptatie:

* \[x] geen live URL;
* \[x] unresolved orders zichtbaar.

\---

## 12\. Fase J - Evidence, shadow mode en chaos testing

Bronroadmap: Roadmap 007  
Waarom pas na echte sessies, reports en endurance.

### J1. Evidence vault

Taken:

* \[x] `evidence.py`
* \[x] add/list/export/verify records.

Acceptatie:

* \[x] hash verificatie;
* \[x] no secrets.

### J2. Shadow mode

Taken:

* \[x] `shadow.py`
* \[x] live/public market data lezen;
* \[x] would-be orders loggen;
* \[x] geen signed endpoints.

Acceptatie:

* \[x] tests bewijzen `place\_order()` nooit aangeroepen.

### J3. Chaos testing

Taken:

* \[x] `chaos.py`
* \[x] simuleer:

  * 429;
  * 418;
  * 5xx;
  * websocket disconnect;
  * stale data;
  * write failure;
  * unknown order.

Acceptatie:

* \[x] critical failures stoppen runtime veilig.

### J4. Readiness scorecard

Taken:

* \[x] `readiness.py`
* \[x] R0-R5 score.

Acceptatie:

* \[x] evidence-based;
* \[x] kan live niet groen maken zonder bewijs.

\---

## 13\. Fase K - Live-readiness pilot design

Bronroadmap: Roadmap 008  
Waarom laatst, en alleen als design.

### Taken

* \[x] evidence gate;
* \[x] live pilot policy document;
* \[x] account safety checklist;
* \[x] manual approval design;
* \[x] live dry-run design;
* \[x] no-go criteria;
* \[x] pilot simulation report.

Acceptatie:

* \[x] geen live uitvoering;
* \[x] alleen ontwerp;
* \[x] live blijft disabled.

\---

## 14\. Concrete Codex sprintindeling

### Sprint 1 - Safety foundation

* \[x] check-all runner.
* \[x] safety regression tests.
* \[x] CI workflow.
* \[x] dashboard import smoke.
* \[x] no-live tests.

### Sprint 2 - Control Center MVP

* \[x] control-center launcher.
* \[x] dashboard/bot engine status.
* \[x] first-run wizard MVP.
* \[x] safe mode badges.

### Sprint 3 - Demo Spot Trading MVP

* \[x] spot preview.
* \[x] demo trading tab.
* \[x] manual demo BUY/SELL.
* \[x] fills table.
* \[x] session write.

### Sprint 4 - Runtime reliability

* \[x] preflight command.
* \[x] alerts/watchdog.
* \[x] session report bundle.
* \[x] paper accounting.

### Sprint 5 - User workspace reliability

* \[x] workspace profiles.
* \[x] backup/restore.
* \[x] diagnostics.
* \[x] support bundle.

### Sprint 6 - Strategy Lab MVP

* \[x] risk debugger.
* \[x] signal explainer.
* \[x] replay sandbox.
* \[x] session comparison.

### Sprint 7 - Copilot/templates

* \[x] copilot permissions.
* \[x] redaction.
* \[x] local summaries.
* \[x] strategy templates.

### Sprint 8 - Research workspace

* \[x] experiment DB.
* \[x] scanner UX/history.
* \[x] notebook/HTML exports.
* \[x] cache/performance tools.

### Sprint 9 - Portfolio/testnet

* \[x] portfolio state.
* \[x] portfolio risk.
* \[x] portfolio paper session.
* \[x] testnet endurance.

### Sprint 10 - Evidence/readiness

* \[x] evidence vault.
* \[x] shadow mode.
* \[x] chaos tests.
* \[x] readiness scorecard.

\---

## 15\. Wat Codex absoluut niet eerst moet doen

Niet starten met:

* Roadmap 008 live-readiness pilot design als eerste bouwen.
* Copilot met AI API zonder redaction.
* Portfolio trading zonder paper accounting.
* Testnet endurance zonder order lifecycle/reports.
* Plugin architecture zonder sandboxing.
* Modeltraining wizard zonder dataset manifests.
* Scanner auto-trading.
* Live trading.
* Grote dashboard rewrite zonder tests.

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

* \[x] maakt alle latere Codex-output controleerbaar;
* \[x] voorkomt safety regressions;
* \[x] klein genoeg voor één PR;
* \[x] direct nuttig voor elke volgende roadmap.

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

* \[x] Eén duidelijke roadmapfase.
* \[x] Eén branchnaam.
* \[x] Eén acceptatielijst.
* \[x] Tests die erbij horen.
* \[x] Geen live trading.
* \[x] Geen secrets.
* \[x] Geen grote refactor buiten scope.
* \[x] Duidelijke files die aangepast mogen worden.

\---

## 20\. Definition of Done voor elke Codex PR

Elke Codex PR is pas klaar als:

* \[x] tests slagen;
* \[x] check-all slaagt;
* \[x] safety tests slagen;
* \[x] docs bijgewerkt zijn;
* \[x] geen secrets in generated files;
* \[x] live disabled blijft;
* \[x] acceptatiecriteria afgevinkt zijn;
* \[x] geen onnodige files gewijzigd zijn;
* \[x] roadmap taak gemarkeerd kan worden als deels/voltooid.

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
