# Roadmap 116 - One-Click Bot Launcher, Unified Control Center, Demo-Data Training Pipeline \& Safe Live Trading Gate

Status: Voltooid / Gevalideerd  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/116-roadmap-one-click-bot-launcher-unified-control-center-demo-data-training-pipeline-safe-live-gate.md
```

## Samenvatting

Deze roadmap corrigeert de productrichting naar wat de bot uiteindelijk moet worden: één lokale bot-app die je met één bestand start, waarna één dashboard opent waar je alles beheert.

Gewenste eindflow:

```text
Dubbelklik Start-Neural-Binance-Bot.cmd
→ local supervisor start backend + runtime + data services + dashboard
→ Dashboard V2 opent automatisch
→ kies profiel: backtest / paper / demo spot Binance / testnet / live locked
→ vul of selecteer config/API keys
→ klik Start
→ bot haalt zelf data op
→ bot draait volgens profiel
→ dashboard toont data, trades, risk, orders, fills, logs en controls
```

Belangrijke toevoeging: **live trading moet eerst “getraind/onderbouwd” worden met goede data uit demo spot trading**. Live is dus geen simpele toggle. De bot moet eerst demo spot data verzamelen, datasets bouwen, data quality checks doen, model/strategie validatie draaien, backtests/walk-forward/paper/testnet bewijs verzamelen en daarna pas via een live-readiness gate naar een live-armed status kunnen.

Live flow:

```text
Demo spot trading data recorder
→ demo session dataset vault
→ feature/training dataset builder
→ data quality + leakage checks
→ model/strategy training or validation
→ backtest/walk-forward validation
→ paper replay validation
→ demo/testnet rehearsal proof
→ live readiness gate
→ manual live arm
→ controlled live execution gate
```

Belangrijk: live trading blijft standaard geblokkeerd. De huidige execution layer blokkeert live order placement bewust. Roadmap 116 bouwt daarom eerst de app, de profielen, de data/training gates en de live-readiness gates. Echte live execution mag pas via een aparte, expliciete live-execution implementation gate.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande Roadmap 116 of unified bot app/live profile roadmaps.
* \[x] Geen bestaande Roadmap 116 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 115 is lokaal aangemaakt als paper portfolio walk-forward/rebalancing robustness roadmap.

### Codebasecontrole

Breed bekeken met focus op dashboard, runtime, config, Binance adapter, execution, paper/demo/testnet/live gating en safety:

* \[x] `src/binance\_spot\_bot/binance.py`
* \[x] `src/binance\_spot\_bot/config.py`
* \[x] `src/binance\_spot\_bot/types.py`
* \[x] `src/binance\_spot\_bot/execution.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/market\_data\_source.py`
* \[x] `src/binance\_spot\_bot/paper.py`
* \[x] `src/binance\_spot\_bot/paper\_accounting.py`
* \[x] `src/binance\_spot\_bot/risk.py`
* \[x] `src/binance\_spot\_bot/session\_store.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] roadmaplijn 104-115.

### Bestaande basis in de codebase

* \[x] `TradingMode` ondersteunt `disabled`, `paper`, `testnet` en `live`.
* \[x] `BotSettings` leest `TRADING\_MODE`, Binance keys, base urls, `LIVE\_TRADING\_ENABLED`, `KILL\_SWITCH`, `MANUAL\_LIVE\_APPROVAL`, max daily loss, max position, max trades, confidence, spread en data paths uit env.
* \[x] `validate\_live\_readiness()` vereist o.a. live env, `LIVE\_TRADING\_ENABLED=true`, `KILL\_SWITCH=false`, manual approval phrase, risk limits en API credentials.
* \[x] `BinanceSpotAdapter` heeft public data endpoints én signed/account/order endpoints.
* \[x] `ExecutionEngine` ondersteunt disabled, paper en testnet/demo flows, maar live order placement is bewust geblokkeerd.
* \[x] `RuntimeSnapshot` bevat candles, signals, fills, equity, market data, data quality, sessions, active model, alerts, paper account, demo account/orders, readiness en report paths.
* \[x] `PaperTrader`, `PaperAccount`, `RiskEngine` en `SessionStore` geven een goede basis voor paper/demo evidence en training/validatie.
* \[x] `check\_all.py` forceert safe env met `LIVE\_TRADING\_ENABLED=false` en `KILL\_SWITCH=true`.

### Belangrijkste gat

De codebase is krachtig, maar nog geen eenvoudige bot-app:

* \[ ] Geen één-klik startbestand.
* \[ ] Geen centrale Control Center flow.
* \[ ] Geen profielkeuze voor backtest/paper/demo/testnet/live.
* \[ ] Geen wizard voor config/API keys.
* \[ ] Geen runtime orchestrator die data + bot + dashboard samen start.
* \[ ] Geen demo spot data recorder als trainingbron.
* \[ ] Geen training dataset vault uit demo spot trading.
* \[ ] Geen live readiness die demo-data/training/paper/testnet bewijs vereist.
* \[ ] Geen duidelijke dashboard flow: profiel kiezen → config invullen → Start.
* \[ ] Geen live-locked/armed lifecycle met evidence.

Roadmap 116 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 116

Maak van het project een lokale bot-app met één ingang:

```text
one-click launcher
→ app supervisor
→ Dashboard V2 Control Center
→ profile selector
→ config/key wizard
→ data bootstrap
→ runtime orchestrator
→ demo data recorder
→ model/training gate
→ safe start/stop/live-readiness
```

Na deze roadmap moet de gebruiker:

* \[ ] één bestand kunnen aanklikken om alles te starten;
* \[ ] automatisch het dashboard in de browser zien;
* \[ ] profielen kunnen kiezen:

  * backtest;
  * paper;
  * Binance demo spot;
  * Binance spot testnet;
  * live locked;
  * live armed later, alleen na gates.
* \[ ] API keys/config veilig kunnen invoeren of selecteren;
* \[ ] symbol, interval, model, strategy en risk preset kunnen instellen;
* \[ ] op Start kunnen klikken;
* \[ ] bot automatisch data laten ophalen;
* \[ ] bot runtime realtime kunnen volgen;
* \[ ] demo spot data kunnen opnemen voor training/validatie;
* \[ ] live pas kunnen armeren na dataset/training/validatie/readiness gates;
* \[ ] Pause/Resume/Stop/Kill Switch kunnen gebruiken;
* \[ ] evidence/support/audit kunnen exporteren.

\---

## 2\. Productprincipe

### Eén klikbare app

Gewenst:

```text
Start-Neural-Binance-Bot.cmd
```

of desktop shortcut:

```text
Start Neural Binance Bot
```

Flow:

```text
1. Launcher checkt Python/venv/project.
2. App Supervisor start lokale backend.
3. Dashboard V2 static/server start.
4. Runtime/data services initialiseren.
5. Browser opent Dashboard V2.
6. Operator kiest profiel.
7. Operator vult config/API keys via wizard.
8. Operator klikt Start.
9. Bot haalt data op.
10. Bot start in gekozen mode.
11. Dashboard toont status, trades, risk, logs, charts en controls.
```

### Eén dashboard voor alles

Dashboard V2 Control Center krijgt:

* \[ ] profiel selector;
* \[ ] config wizard;
* \[ ] API key/secret status;
* \[ ] data bootstrap status;
* \[ ] readiness checklist;
* \[ ] start/pause/resume/stop;
* \[ ] kill switch;
* \[ ] market data panel;
* \[ ] orders/fills/signals;
* \[ ] risk decisions;
* \[ ] demo data recorder;
* \[ ] training/validation gate;
* \[ ] live readiness gate;
* \[ ] evidence/support export.

### Live trading alleen na bewijs

Live mag pas na:

* \[ ] genoeg demo spot sessions;
* \[ ] voldoende kwaliteit van demo data;
* \[ ] training/validation dataset;
* \[ ] model/strategy validation;
* \[ ] backtest/walk-forward;
* \[ ] paper replay;
* \[ ] testnet/demo rehearsal;
* \[ ] live readiness;
* \[ ] manual arm;
* \[ ] dedicated live execution gate.

\---

## 3\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen Dashboard V2 foundation opnieuw bouwen.
* \[ ] Geen scanner/strategy/portfolio labs opnieuw bouwen.
* \[ ] Geen modeltraining pipeline volledig opnieuw bouwen als bestaande componenten herbruikbaar zijn.
* \[ ] Geen exchange adapter volledig herschrijven.
* \[ ] Geen live trading blind activeren.
* \[ ] Geen auto-live-start.
* \[ ] Geen live orders vanuit launcher.
* \[ ] Geen raw API keys in profiles/logs/evidence.
* \[ ] Geen remote/cloud control panel.
* \[ ] Geen externe telemetry.
* \[ ] Geen financieel advies.
* \[ ] Geen unattended live trading.

Wel doen:

* \[ ] one-click launcher;
* \[ ] local app supervisor;
* \[ ] unified profile system;
* \[ ] config/key wizard;
* \[ ] runtime orchestrator;
* \[ ] data bootstrap;
* \[ ] demo spot data recorder;
* \[ ] training dataset builder;
* \[ ] model/strategy validation gate;
* \[ ] live readiness gate;
* \[ ] dashboard control center;
* \[ ] evidence/support/audit.

\---

## 4\. Fase 0 - Unified Bot App Safety Contract

Nieuw docbestand:

```text
docs/unified-bot-app/unified-bot-app-safety-contract.md
```

Regels:

* \[ ] One-click launcher mag nooit automatisch live orders plaatsen.
* \[ ] Live profile start altijd locked.
* \[ ] Live profile mag niet auto-starten.
* \[ ] Live trading vereist explicit manual arm in dashboard.
* \[ ] Live trading vereist demo-data/training/validatie bewijs.
* \[ ] Live trading vereist `validate\_live\_readiness()` pass.
* \[ ] Live trading vereist aparte live-execution implementation gate.
* \[ ] API keys worden nooit in profiles/logs/reports/dashboard JSON/evidence getoond.
* \[ ] Profielen bevatten secret references, geen raw secrets.
* \[ ] Backtest/paper/demo/testnet mogen via Start werken.
* \[ ] Kill Switch is altijd zichtbaar.
* \[ ] Stop button is altijd zichtbaar.
* \[ ] Launcher start standaard safe.
* \[ ] Dashboard opent lokaal op `127.0.0.1`.
* \[ ] Geen remote telemetry.
* \[ ] Geen financieel advies.
* \[ ] Alle reports zijn secret-free.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen launcher nooit live auto-start doet.
* \[ ] Tests bewijzen live locked blijft zonder gates.
* \[ ] Tests bewijzen keys niet lekken.
* \[ ] Tests bewijzen Stop/Kill Switch altijd zichtbaar zijn.

\---

## 5\. Fase 1 - Unified Bot Profile Schema

Nieuwe module:

```text
src/binance\_spot\_bot/app\_control/bot\_profile.py
```

Modes:

* \[ ] `backtest`
* \[ ] `paper`
* \[ ] `demo\_spot`
* \[ ] `testnet`
* \[ ] `live\_locked`
* \[ ] `live\_armed`
* \[ ] `disabled`

Dataclasses:

* \[ ] `BotProfile`
* \[ ] `BotProfileMode`
* \[ ] `BotProfileExchange`
* \[ ] `BotProfileDataSource`
* \[ ] `BotProfileRisk`
* \[ ] `BotProfileModel`
* \[ ] `BotProfileTrainingGate`
* \[ ] `BotProfileSecretsRef`
* \[ ] `BotProfileValidationResult`
* \[ ] `BotProfileReport`

Profile fields:

* \[ ] profile\_id;
* \[ ] name;
* \[ ] description;
* \[ ] mode;
* \[ ] exchange\_profile;
* \[ ] base\_url;
* \[ ] symbol;
* \[ ] watchlist\_id;
* \[ ] interval;
* \[ ] data\_source;
* \[ ] model\_alias;
* \[ ] strategy\_id;
* \[ ] risk\_preset;
* \[ ] max\_daily\_loss\_quote;
* \[ ] max\_position\_quote;
* \[ ] max\_trades\_per\_day;
* \[ ] min\_signal\_confidence;
* \[ ] max\_spread\_bps;
* \[ ] starting\_quote\_balance;
* \[ ] secret\_ref;
* \[ ] dashboard\_workspace\_id;
* \[ ] auto\_open\_dashboard;
* \[ ] auto\_fetch\_data;
* \[ ] auto\_start\_runtime;
* \[ ] live\_trading\_enabled;
* \[ ] kill\_switch;
* \[ ] manual\_live\_approval;
* \[ ] requires\_demo\_training\_evidence;
* \[ ] required\_demo\_sessions;
* \[ ] required\_min\_demo\_fills;
* \[ ] required\_dataset\_quality\_score;
* \[ ] required\_validation\_grade;
* \[ ] created\_at\_ms;
* \[ ] updated\_at\_ms.

Validation blocks:

* \[ ] raw API key/secret in profile JSON;
* \[ ] live mode with `auto\_start\_runtime=true`;
* \[ ] live mode without demo/training evidence requirement;
* \[ ] live mode without risk limits;
* \[ ] live mode without kill-switch/approval controls;
* \[ ] unknown exchange profile;
* \[ ] unsafe base URL;
* \[ ] invalid symbol/interval;
* \[ ] missing risk preset;
* \[ ] secret-like values.

Acceptatiecriteria:

* \[ ] Profiles JSON-serializable.
* \[ ] Backtest/paper/demo/testnet profiles validate.
* \[ ] Live profile defaults to locked.
* \[ ] Live profile requires demo-data/training gate.
* \[ ] Raw secrets blocked/redacted.

\---

## 6\. Fase 2 - Profile Store \& Templates

Nieuwe module:

```text
src/binance\_spot\_bot/app\_control/profile\_store.py
```

Storage:

```text
data/app-control/profiles/
  templates/
  user/
  backups/
  reports/
```

Built-in templates:

* \[ ] `backtest-local-btcusdt`
* \[ ] `paper-btcusdt-safe`
* \[ ] `paper-watchlist-safe`
* \[ ] `binance-demo-spot-safe`
* \[ ] `binance-spot-testnet-safe`
* \[ ] `live-locked-training-required-template`

Functions:

* \[ ] list profiles;
* \[ ] load profile;
* \[ ] save profile;
* \[ ] clone profile;
* \[ ] delete profile with confirm;
* \[ ] set default profile;
* \[ ] export/import profile;
* \[ ] validate all profiles;
* \[ ] backup before edit.

Acceptatiecriteria:

* \[ ] Store local-only.
* \[ ] Path traversal blocked.
* \[ ] Raw secrets blocked.
* \[ ] Built-in templates validate.
* \[ ] Live template requires training gate.

\---

## 7\. Fase 3 - Local Secret Reference Manager

Nieuwe module:

```text
src/binance\_spot\_bot/app\_control/secret\_refs.py
```

Secret reference types:

* \[ ] `.env.local` reference;
* \[ ] OS environment reference;
* \[ ] session-only secret entry;
* \[ ] encrypted local file later optional;
* \[ ] Windows Credential Manager later optional.

Features:

* \[ ] create secret ref;
* \[ ] validate secret presence;
* \[ ] show fingerprint only;
* \[ ] rotate secret ref;
* \[ ] delete secret ref;
* \[ ] detect raw secret in profile;
* \[ ] redact all outputs;
* \[ ] permission checklist.

Acceptatiecriteria:

* \[ ] API keys never printed.
* \[ ] Dashboard sees only fingerprint/status.
* \[ ] Missing key gives helpful error.
* \[ ] Secret refs work with env files.
* \[ ] Evidence redacts secrets.

\---

## 8\. Fase 4 - Config Wizard API

Nieuwe module:

```text
src/binance\_spot\_bot/app\_control/config\_wizard.py
```

Wizard steps:

1. Kies profieltype:

   * backtest;
   * paper;
   * demo spot;
   * testnet;
   * live locked.
2. Kies exchange/base URL.
3. Kies symbol/watchlist.
4. Kies interval.
5. Kies data source.
6. Kies model/strategy.
7. Kies risk preset.
8. Voeg secret ref toe indien nodig.
9. Stel demo-data/training requirements in voor live.
10. Run readiness checks.
11. Save profile.
12. Start profile of keep locked.

Acceptatiecriteria:

* \[ ] Wizard creates paper profile.
* \[ ] Wizard creates demo spot profile.
* \[ ] Wizard creates testnet profile.
* \[ ] Wizard creates live locked training-required profile.
* \[ ] Wizard never arms live automatically.

\---

## 9\. Fase 5 - App Supervisor

Nieuwe module:

```text
src/binance\_spot\_bot/app\_control/app\_supervisor.py
```

Supervisor responsibilities:

* \[ ] start backend;
* \[ ] start Dashboard V2;
* \[ ] initialize runtime registry;
* \[ ] initialize data services;
* \[ ] initialize WebSocket hub;
* \[ ] open browser when healthy;
* \[ ] write session file;
* \[ ] monitor service health;
* \[ ] graceful shutdown;
* \[ ] crash report;
* \[ ] local URL display.

Acceptatiecriteria:

* \[ ] Supervisor starts local services.
* \[ ] Default host `127.0.0.1`.
* \[ ] Browser opens after health pass.
* \[ ] Crash report redacted.
* \[ ] Tests use fake server.

\---

## 10\. Fase 6 - One-Click Launcher Files

Nieuwe module:

```text
src/binance\_spot\_bot/app\_control/one\_click\_launcher.py
```

Generated files:

```text
Start-Neural-Binance-Bot.cmd
Start-Neural-Binance-Bot.ps1
Stop-Neural-Binance-Bot.cmd
Open-Neural-Binance-Dashboard.cmd
Create-Desktop-Shortcut.ps1
```

Launcher behavior:

* \[ ] find project root;
* \[ ] use `.venv` if present;
* \[ ] verify Python;
* \[ ] verify package import;
* \[ ] run quick dependency check;
* \[ ] start app supervisor;
* \[ ] wait for health;
* \[ ] open dashboard;
* \[ ] show local URL;
* \[ ] show safe startup notice;
* \[ ] never auto-start live.

Acceptatiecriteria:

* \[ ] `.cmd` works on Windows.
* \[ ] `.ps1` works on Windows PowerShell.
* \[ ] No admin privileges required.
* \[ ] Launcher contains no secrets.
* \[ ] Launcher cannot live auto-start.

\---

## 11\. Fase 7 - Unified Runtime Orchestrator

Nieuwe module:

```text
src/binance\_spot\_bot/app\_control/runtime\_orchestrator.py
```

Responsibilities:

* \[ ] load selected profile;
* \[ ] validate profile;
* \[ ] translate profile to BotSettings/env overlay;
* \[ ] create market data source;
* \[ ] run data bootstrap;
* \[ ] create runtime;
* \[ ] start runtime loop;
* \[ ] pause runtime;
* \[ ] resume runtime;
* \[ ] stop runtime;
* \[ ] emergency kill switch;
* \[ ] snapshot status;
* \[ ] collect logs/events;
* \[ ] emit WebSocket events.

Runtime states:

* \[ ] idle;
* \[ ] validating\_profile;
* \[ ] waiting\_for\_keys;
* \[ ] bootstrapping\_data;
* \[ ] recording\_demo\_data;
* \[ ] training\_dataset\_ready;
* \[ ] validating\_model;
* \[ ] ready\_to\_start;
* \[ ] running;
* \[ ] paused;
* \[ ] stopping;
* \[ ] stopped;
* \[ ] blocked;
* \[ ] failed;
* \[ ] live\_locked;
* \[ ] live\_training\_required;
* \[ ] live\_validation\_required;
* \[ ] live\_ready\_to\_arm;
* \[ ] live\_armed;
* \[ ] emergency\_stopped.

Acceptatiecriteria:

* \[ ] Paper profile can start runtime.
* \[ ] Demo spot profile can start after demo readiness.
* \[ ] Testnet profile can run readiness flow.
* \[ ] Live profile remains locked until gates pass.
* \[ ] Tests use fake runtime/data source.

\---

## 12\. Fase 8 - Data Bootstrap Manager

Nieuwe module:

```text
src/binance\_spot\_bot/app\_control/data\_bootstrap.py
```

Bootstrap tasks:

* \[ ] check symbol filters;
* \[ ] fetch exchangeInfo;
* \[ ] fetch initial klines;
* \[ ] fetch bookTicker/top-of-book;
* \[ ] warm market data cache;
* \[ ] validate candle count;
* \[ ] validate data freshness;
* \[ ] validate spread;
* \[ ] load model features;
* \[ ] prepare backtest dataset;
* \[ ] prepare paper runtime feed;
* \[ ] prepare demo/testnet readiness;
* \[ ] prepare live public-data-only readiness until armed.

Acceptatiecriteria:

* \[ ] Bootstrap works offline with fixtures.
* \[ ] Bootstrap works with cached public data.
* \[ ] Bootstrap reports missing data clearly.
* \[ ] Live bootstrap does not place orders.
* \[ ] Tests cover each profile type.

\---

## 13\. Fase 9 - Demo Spot Data Recorder

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/demo\_spot\_data\_recorder.py
```

Doel: alle bruikbare demo spot trading data opnemen als trainings-/validatiebron.

Record types:

* \[ ] public market snapshots;
* \[ ] candles/klines;
* \[ ] top of book;
* \[ ] spreads;
* \[ ] signals;
* \[ ] model predictions/confidence;
* \[ ] risk decisions;
* \[ ] order previews;
* \[ ] demo test orders;
* \[ ] demo placed orders;
* \[ ] fills;
* \[ ] rejected orders;
* \[ ] cancellations;
* \[ ] reconciliation results;
* \[ ] slippage estimates;
* \[ ] latency measurements;
* \[ ] session context;
* \[ ] errors/warnings.

Storage:

```text
data/live-training/demo-spot-recordings/
  sessions/
  market/
  orders/
  fills/
  features/
  manifests/
```

Acceptatiecriteria:

* \[ ] Demo recorder works during demo spot profile.
* \[ ] Records are timestamped and hashed.
* \[ ] Raw secrets are never recorded.
* \[ ] Session manifest generated.
* \[ ] Tests use fixture demo events.

\---

## 14\. Fase 10 - Demo Dataset Quality Gate

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/demo\_dataset\_quality.py
```

Quality checks:

* \[ ] minimum demo sessions;
* \[ ] minimum candles;
* \[ ] minimum demo fills;
* \[ ] minimum signal count;
* \[ ] minimum risk decision count;
* \[ ] no missing critical timestamps;
* \[ ] no duplicate event IDs;
* \[ ] spread data present;
* \[ ] fills reconcile with orders;
* \[ ] latency data present;
* \[ ] symbol/interval consistency;
* \[ ] data freshness;
* \[ ] no raw secrets;
* \[ ] no live events mixed into demo dataset.

Outputs:

* \[ ] dataset quality score;
* \[ ] blockers;
* \[ ] warnings;
* \[ ] missing data recommendations;
* \[ ] live readiness contribution.

Acceptatiecriteria:

* \[ ] Quality gate deterministic.
* \[ ] Low-quality dataset blocks live training gate.
* \[ ] Secret scan hard fails.
* \[ ] Reports Markdown + JSON.
* \[ ] Tests cover pass/fail cases.

\---

## 15\. Fase 11 - Training Dataset Builder

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/training\_dataset\_builder.py
```

Inputs:

* \[ ] demo spot recordings;
* \[ ] market snapshots;
* \[ ] candles;
* \[ ] signals;
* \[ ] risk decisions;
* \[ ] fills;
* \[ ] order outcomes;
* \[ ] reconciliation;
* \[ ] paper session results optional;
* \[ ] scanner/strategy/portfolio lab evidence optional.

Dataset outputs:

* \[ ] features table;
* \[ ] labels/outcomes table;
* \[ ] event alignment table;
* \[ ] train/validation/test split;
* \[ ] leakage report;
* \[ ] data dictionary;
* \[ ] dataset manifest.

Feature examples:

* \[ ] candle returns;
* \[ ] volatility;
* \[ ] spread bps;
* \[ ] volume;
* \[ ] signal confidence;
* \[ ] risk block reason;
* \[ ] order latency;
* \[ ] slippage estimate;
* \[ ] fill outcome;
* \[ ] model prediction context.

Acceptatiecriteria:

* \[ ] Dataset builds from fixture demo sessions.
* \[ ] Train/validation/test split exists.
* \[ ] Leakage checks run.
* \[ ] Dataset manifest has hashes.
* \[ ] Tests cover missing/invalid data.

\---

## 16\. Fase 12 - Model/Strategy Training \& Validation Gate

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/model\_validation\_gate.py
```

Purpose: live kan pas als gekozen model/strategy voldoende gevalideerd is op demo-derived data en paper/testnet evidence.

Checks:

* \[ ] training dataset quality pass;
* \[ ] minimum train/validation samples;
* \[ ] no leakage;
* \[ ] backtest result exists;
* \[ ] walk-forward result exists;
* \[ ] paper result exists;
* \[ ] demo/testnet rehearsal result exists;
* \[ ] risk limits compatible;
* \[ ] max drawdown below threshold;
* \[ ] excessive overfit gap blocked;
* \[ ] signal confidence calibration acceptable;
* \[ ] rejected orders understood;
* \[ ] slippage/fees assumptions included;
* \[ ] model version pinned;
* \[ ] strategy version pinned.

Grades:

* \[ ] A: eligible for live readiness review;
* \[ ] B: eligible with warnings;
* \[ ] C: more demo/paper validation needed;
* \[ ] D: blocked;
* \[ ] F: unsafe/invalid.

Acceptatiecriteria:

* \[ ] Gate uses demo dataset report.
* \[ ] Gate can block live.
* \[ ] Gate explains blockers.
* \[ ] No financial advice wording.
* \[ ] Tests cover all grades.

\---

## 17\. Fase 13 - Live Training Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/live\_training\_evidence.py
```

Bundle bevat:

* \[ ] demo recording manifests;
* \[ ] demo dataset quality report;
* \[ ] training dataset manifest;
* \[ ] leakage report;
* \[ ] train/validation/test split report;
* \[ ] model/strategy validation report;
* \[ ] backtest/walk-forward report links;
* \[ ] paper validation report links;
* \[ ] demo/testnet rehearsal links;
* \[ ] risk compatibility report;
* \[ ] live readiness contribution;
* \[ ] no-secret proof;
* \[ ] no-live-order proof;
* \[ ] hashes.

Output:

```text
data/live-training/evidence/<run\_id>/
  live\_training\_evidence\_manifest.json
  live\_training\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle required by live readiness gate.
* \[ ] Dashboard can download bundle.

\---

## 18\. Fase 14 - Backtest Profile Integration

Nieuwe module:

```text
src/binance\_spot\_bot/app\_control/backtest\_profile\_runner.py
```

Features:

* \[ ] select dataset;
* \[ ] select symbol/interval/window;
* \[ ] select strategy/model;
* \[ ] select risk preset;
* \[ ] run backtest;
* \[ ] show progress;
* \[ ] show equity/fills/signals/risk blocks;
* \[ ] export report;
* \[ ] feed validation gate.

Acceptatiecriteria:

* \[ ] Backtest profile appears in Control Center.
* \[ ] Backtest does not need API keys.
* \[ ] Backtest output shown in dashboard.
* \[ ] Backtest cannot place orders.
* \[ ] Tests use fixture candles.

\---

## 19\. Fase 15 - Paper Profile Integration

Paper mode as daily safe default.

Features:

* \[ ] paper profile wizard;
* \[ ] starting quote balance;
* \[ ] risk preset selection;
* \[ ] market data source selection;
* \[ ] Start/Pause/Resume/Stop;
* \[ ] paper account panel;
* \[ ] fills/orders panel;
* \[ ] risk decisions panel;
* \[ ] session report;
* \[ ] feed validation gate.

Acceptatiecriteria:

* \[ ] Paper can start from one dashboard.
* \[ ] Paper fetches data automatically.
* \[ ] Paper account updates visible.
* \[ ] Stop always works.
* \[ ] Browser smoke covers paper start/stop.

\---

## 20\. Fase 16 - Binance Demo Spot Profile Integration

Demo spot is the safe bridge before live.

Features:

* \[ ] demo spot profile wizard;
* \[ ] demo base URL validation;
* \[ ] credentials fingerprint;
* \[ ] connection check;
* \[ ] filters check;
* \[ ] test order gate;
* \[ ] armed/unarmed state;
* \[ ] max demo orders per session;
* \[ ] demo order preview;
* \[ ] demo order status;
* \[ ] reconciliation panel;
* \[ ] demo data recorder;
* \[ ] live-training dataset contribution;
* \[ ] evidence report.

Acceptatiecriteria:

* \[ ] Demo profile does not use live base URL.
* \[ ] Demo credentials checked without printing secrets.
* \[ ] Demo order flow requires arming.
* \[ ] Demo max orders enforced.
* \[ ] Demo data recorder captures events.

\---

## 21\. Fase 17 - Binance Spot Testnet Profile Integration

Testnet profile for signed endpoint rehearsal.

Features:

* \[ ] testnet profile wizard;
* \[ ] testnet base URL validation;
* \[ ] credential fingerprint;
* \[ ] account/readiness check;
* \[ ] order test endpoint check;
* \[ ] filters check;
* \[ ] test order only by default;
* \[ ] evidence report;
* \[ ] live-training validation contribution.

Acceptatiecriteria:

* \[ ] Testnet requires credentials.
* \[ ] Testnet base URL must be testnet.
* \[ ] Testnet does not use live base URL.
* \[ ] Test order path visible.
* \[ ] Browser smoke covers testnet readiness.

\---

## 22\. Fase 18 - Live Locked Profile \& Readiness Gate

Nieuwe module:

```text
src/binance\_spot\_bot/app\_control/live\_readiness\_gate.py
```

Live readiness requires:

* \[ ] `APP\_ENV=live`;
* \[ ] `TRADING\_MODE=live`;
* \[ ] `LIVE\_TRADING\_ENABLED=true`;
* \[ ] `KILL\_SWITCH=false`;
* \[ ] manual approval phrase exact;
* \[ ] API credentials present;
* \[ ] API key permission report;
* \[ ] max daily loss > 0;
* \[ ] max position > 0;
* \[ ] max trades per day > 0;
* \[ ] min confidence configured;
* \[ ] max spread configured;
* \[ ] symbol filters loaded;
* \[ ] data freshness OK;
* \[ ] spread OK;
* \[ ] demo dataset quality gate pass;
* \[ ] training dataset manifest exists;
* \[ ] model/strategy validation grade A/B;
* \[ ] paper validation report pass;
* \[ ] demo/testnet rehearsal pass;
* \[ ] live training evidence bundle verified;
* \[ ] final operator confirmation.

Acceptatiecriteria:

* \[ ] Live profile locked by default.
* \[ ] Missing demo training evidence blocks live.
* \[ ] Low model validation grade blocks live.
* \[ ] Readiness report lists every blocker.
* \[ ] Live arming requires exact confirmation.

\---

## 23\. Fase 19 - Live Execution Implementation Gate

Nieuw doc:

```text
docs/live-trading/live-execution-implementation-gate.md
```

Before implementing live order placement:

* \[ ] demo spot flow stable;
* \[ ] demo data recorder stable;
* \[ ] dataset quality gate pass;
* \[ ] model/strategy validation gate pass;
* \[ ] paper validation pass;
* \[ ] testnet pass;
* \[ ] live readiness gate pass;
* \[ ] risk engine hard limits verified;
* \[ ] account/balance read-only check implemented;
* \[ ] order preview implemented;
* \[ ] order size calculator tested;
* \[ ] cancel/emergency stop tested;
* \[ ] audit log/evidence ready;
* \[ ] UAT live-dry-run pass;
* \[ ] explicit operator approval.

Implementation rules:

* \[ ] live execution cannot be added in same PR as UI controls.
* \[ ] live execution requires dedicated PR.
* \[ ] live starts with tiny capped order size.
* \[ ] market and limit orders have separate gates.
* \[ ] emergency kill switch tested before live.

Acceptatiecriteria:

* \[ ] Gate doc exists.
* \[ ] Tests prove live execution still blocked until gate.
* \[ ] Dashboard shows “live execution not implemented” where relevant.
* \[ ] No accidental live path.
* \[ ] Evidence required.

\---

## 24\. Fase 20 - Unified Bot Control Center Dashboard

Nieuwe Dashboard V2 route:

```text
/control-center
```

Main sections:

* \[ ] profile selector;
* \[ ] profile status;
* \[ ] config wizard;
* \[ ] secret/key status;
* \[ ] data bootstrap status;
* \[ ] readiness checklist;
* \[ ] demo data recorder status;
* \[ ] training dataset status;
* \[ ] model/strategy validation gate;
* \[ ] Start button;
* \[ ] Pause button;
* \[ ] Resume button;
* \[ ] Stop button;
* \[ ] Emergency Kill Switch;
* \[ ] runtime state;
* \[ ] market data status;
* \[ ] orders/fills/signals;
* \[ ] risk decisions;
* \[ ] logs/events;
* \[ ] evidence/support export;
* \[ ] live locked/readiness panel.

Acceptatiecriteria:

* \[ ] Control Center can create/select profile.
* \[ ] Control Center can start paper profile.
* \[ ] Control Center shows demo data recording status.
* \[ ] Control Center shows live training/readiness blockers.
* \[ ] Browser smoke covers full paper happy path.

\---

## 25\. Fase 21 - Dashboard Start UX

Rules:

* \[ ] Start button disabled until readiness pass.
* \[ ] Disabled reason always visible.
* \[ ] Live Start button never appears as normal Start.
* \[ ] Live uses separate “Arm Live Session” and confirmation flow.
* \[ ] Paper/demo/testnet clearly labeled.
* \[ ] Config changes while running require restart/safe apply.
* \[ ] Stop button always active when running.
* \[ ] Kill Switch always visible.
* \[ ] Demo recorder visible during demo spot sessions.
* \[ ] Training gate visible for live profiles.

Acceptatiecriteria:

* \[ ] Operator sees clear next action.
* \[ ] Profile validation visible.
* \[ ] Live UX clearly different from paper/demo.
* \[ ] Stop/Kill Switch always visible.
* \[ ] Accessibility basic checks pass.

\---

## 26\. Fase 22 - Unified App API

Nieuwe API routes:

```text
GET  /api/app/health
GET  /api/app/session
POST /api/app/shutdown
GET  /api/profiles
POST /api/profiles
GET  /api/profiles/{profile\_id}
PUT  /api/profiles/{profile\_id}
DELETE /api/profiles/{profile\_id}
POST /api/profiles/{profile\_id}/clone
POST /api/profiles/{profile\_id}/validate
POST /api/profiles/{profile\_id}/set-default
GET  /api/secrets/refs
POST /api/secrets/refs
POST /api/secrets/refs/{secret\_ref\_id}/validate
POST /api/runtime/bootstrap
POST /api/runtime/start
POST /api/runtime/pause
POST /api/runtime/resume
POST /api/runtime/stop
POST /api/runtime/kill-switch
GET  /api/runtime/orchestrator-state
GET  /api/demo-training/status
POST /api/demo-training/dataset/build
GET  /api/demo-training/quality
POST /api/demo-training/validate-model
GET  /api/live/readiness
POST /api/live/arm
POST /api/live/disarm
WS   /ws/app-control
```

API rules:

* \[ ] raw secrets never returned;
* \[ ] live start blocked by default;
* \[ ] launcher cannot call live arm automatically;
* \[ ] runtime start requires profile validation;
* \[ ] live arm requires demo/training evidence;
* \[ ] all mutations audited;
* \[ ] all responses redacted.

Acceptatiecriteria:

* \[ ] TestClient covers routes.
* \[ ] Start paper route works with fixture.
* \[ ] Live arm blocked without demo/training evidence.
* \[ ] Raw secrets not returned.
* \[ ] WebSocket emits app state.

\---

## 27\. Fase 23 - Unified CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli app-start
python -m binance\_spot\_bot.cli app-stop
python -m binance\_spot\_bot.cli app-status --json
python -m binance\_spot\_bot.cli app-create-launchers
python -m binance\_spot\_bot.cli app-open-dashboard
python -m binance\_spot\_bot.cli profiles --json
python -m binance\_spot\_bot.cli profile-create --template paper-btcusdt-safe --name "My Paper Bot"
python -m binance\_spot\_bot.cli profile-validate --profile <id> --json
python -m binance\_spot\_bot.cli profile-set-default --profile <id>
python -m binance\_spot\_bot.cli secret-ref-create --provider env\_file --name "binance-demo"
python -m binance\_spot\_bot.cli secret-ref-validate --secret-ref <id> --json
python -m binance\_spot\_bot.cli runtime-bootstrap --profile <id> --json
python -m binance\_spot\_bot.cli runtime-start --profile <id>
python -m binance\_spot\_bot.cli runtime-stop
python -m binance\_spot\_bot.cli demo-training-quality --profile <id> --json
python -m binance\_spot\_bot.cli demo-training-dataset-build --profile <id>
python -m binance\_spot\_bot.cli model-validation-gate --profile <id> --json
python -m binance\_spot\_bot.cli live-training-evidence-export --profile <id>
python -m binance\_spot\_bot.cli live-readiness --profile <id> --json
python -m binance\_spot\_bot.cli live-arm --profile <id> --confirm I\_UNDERSTAND\_LIVE\_SPOT\_TRADING\_RISK
```

Acceptatiecriteria:

* \[ ] Commands werken lokaal.
* \[ ] Launcher generation werkt.
* \[ ] Profile commands werken.
* \[ ] Demo training commands werken.
* \[ ] Live arm requires confirm and training evidence.
* \[ ] Commands redacteren secrets.

\---

## 28\. Fase 24 - Startup Health \& Error Recovery

Nieuwe module:

```text
src/binance\_spot\_bot/app\_control/startup\_health.py
```

Checks:

* \[ ] Python version;
* \[ ] package import;
* \[ ] dependencies;
* \[ ] data dir writable;
* \[ ] profile store writable;
* \[ ] dashboard static build exists;
* \[ ] backend port available;
* \[ ] browser open possible;
* \[ ] WebSocket health;
* \[ ] default profile exists;
* \[ ] secret refs valid only if needed;
* \[ ] Binance public connectivity optional;
* \[ ] safe env.

Recovery:

* \[ ] missing venv instructions;
* \[ ] port busy → find free port;
* \[ ] missing frontend build → clear message;
* \[ ] invalid profile → open wizard;
* \[ ] missing keys → open key wizard;
* \[ ] missing demo training data → open demo recorder flow;
* \[ ] backend crash → local crash report;
* \[ ] dashboard fail → log + CLI URL.

Acceptatiecriteria:

* \[ ] Startup health report exists.
* \[ ] Launcher shows useful errors.
* \[ ] Dashboard opens wizard if no profile.
* \[ ] Crash reports redacted.
* \[ ] Tests cover failure modes.

\---

## 29\. Fase 25 - Audit, Evidence \& Support Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/app\_control/app\_evidence.py
```

Evidence includes:

* \[ ] launcher session;
* \[ ] app supervisor health;
* \[ ] selected profile redacted;
* \[ ] profile validation report;
* \[ ] secret ref status fingerprint only;
* \[ ] data bootstrap report;
* \[ ] runtime orchestrator state;
* \[ ] dashboard control center state;
* \[ ] demo training status;
* \[ ] dataset quality report;
* \[ ] model validation gate;
* \[ ] live readiness report if relevant;
* \[ ] start/stop/pause/resume actions;
* \[ ] kill switch actions;
* \[ ] errors/crashes;
* \[ ] audit log hashes;
* \[ ] no auto-live-start proof;
* \[ ] no raw secret proof.

Output:

```text
data/app-control/evidence/<run\_id>/
  app\_control\_evidence\_manifest.json
  app\_control\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Evidence secret-free.
* \[ ] Evidence has manifest/hash.
* \[ ] Support bundle includes app-control artifacts.
* \[ ] Live readiness blockers visible.
* \[ ] Tests cover redaction.

\---

## 30\. Fase 26 - Live Trading UX Guardrails

Guardrails:

* \[ ] live profile hidden behind advanced setting by default;
* \[ ] live profile always starts locked;
* \[ ] no “Start Live” from launcher;
* \[ ] live status shows blocked/not implemented/not armed;
* \[ ] demo training evidence required;
* \[ ] model validation gate required;
* \[ ] order preview required before future live execution;
* \[ ] max first order cap;
* \[ ] session max loss;
* \[ ] session max orders;
* \[ ] session timeout;
* \[ ] emergency stop;
* \[ ] disarm on restart;
* \[ ] disarm on config change;
* \[ ] disarm on risk warning;
* \[ ] disarm on connectivity loss;
* \[ ] disarm on stale data.

Acceptatiecriteria:

* \[ ] Live disarms on restart.
* \[ ] Live disarms on profile edit.
* \[ ] Live disarms on kill switch.
* \[ ] Live cannot start from one-click file.
* \[ ] Tests cover disarm triggers.

\---

## 31\. Fase 27 - Dashboard Workspace Integration

Integrations:

* \[ ] workspace selector per profile;
* \[ ] backtest opens backtest workspace;
* \[ ] paper opens paper workspace;
* \[ ] demo spot opens demo control + recorder workspace;
* \[ ] testnet opens readiness workspace;
* \[ ] live locked opens live readiness + training gate workspace;
* \[ ] scanner/strategy/portfolio labs remain available as advanced tabs;
* \[ ] all workspaces show global runtime controls.

Acceptatiecriteria:

* \[ ] Profile can set workspace.
* \[ ] Workspace loads after start.
* \[ ] Runtime state global across dashboard.
* \[ ] Stop/Kill Switch visible everywhere.
* \[ ] Browser smoke covers workspace routing.

\---

## 32\. Fase 28 - Profile Matrix

Matrix report:

```text
data/app-control/profile-matrix/profile\_matrix.md
```

Expected profile matrix:

|Profile|API keys|Data|Orders|Auto-start|Live training gate|Status|
|-|-:|-|-|-:|-:|-|
|Backtest|No|fixture/cache|No|Yes|No|Safe|
|Paper|No|public/cache/demo|Paper only|Yes|Optional|Safe|
|Demo Spot|Yes|public + demo signed|Demo/test orders only|Guarded|Data source|Safe with arm|
|Testnet|Yes|public + testnet signed|Testnet/test only|Guarded|Validation source|Safe with arm|
|Live Locked|Yes|public + live readiness|Real possible later|Never|Required|Locked|
|Live Armed|Yes|live|Real|Never from launcher|Required/pass|Separate gate|

Acceptatiecriteria:

* \[ ] Matrix generated.
* \[ ] Matrix shown in dashboard docs.
* \[ ] Tests ensure live auto-start never allowed.
* \[ ] Live training gate visible.
* \[ ] Profile support status clear.

\---

## 33\. Fase 29 - Check-All Integration

Fast profile:

* \[ ] app\_control imports;
* \[ ] live\_training imports;
* \[ ] profile schema tests;
* \[ ] profile templates validate;
* \[ ] launcher script generation smoke;
* \[ ] startup health fixture;
* \[ ] secret redaction;
* \[ ] demo dataset quality fixture;
* \[ ] live auto-start blocker.

Deep profile:

* \[ ] app supervisor fake server;
* \[ ] runtime orchestrator fixture;
* \[ ] data bootstrap fixture;
* \[ ] demo recorder fixture;
* \[ ] training dataset builder fixture;
* \[ ] model validation gate fixture;
* \[ ] Dashboard Control Center browser smoke;
* \[ ] profile wizard smoke;
* \[ ] paper start/stop smoke;
* \[ ] demo readiness/recording smoke;
* \[ ] testnet readiness smoke;
* \[ ] live readiness gate smoke;
* \[ ] app evidence export/verify.

Acceptatiecriteria:

* \[ ] Normal check-all remains usable.
* \[ ] Deep app-control profile covers one-click flow.
* \[ ] Live auto-start failure hard fails.
* \[ ] Secret leak hard fails.
* \[ ] Reports redacted.

\---

## 34\. Fase 30 - Operator/UAT Integration

Roadmap 102:

* \[ ] Operator manual gets one-click app guide.
* \[ ] CLI cookbook gets app-start/app-stop.
* \[ ] Troubleshooting gets launcher errors.
* \[ ] Key/config guide gets secret refs.
* \[ ] Demo data/training guide.
* \[ ] Live readiness guide gets blockers.

Roadmap 103 UAT:

* \[ ] double-click launcher;
* \[ ] dashboard opens automatically;
* \[ ] create paper profile;
* \[ ] start paper bot;
* \[ ] stop bot;
* \[ ] create demo spot profile;
* \[ ] run demo data recorder;
* \[ ] dataset quality report;
* \[ ] training dataset build;
* \[ ] model validation gate;
* \[ ] missing key shows helpful error;
* \[ ] live profile remains locked without evidence;
* \[ ] evidence export.

Acceptatiecriteria:

* \[ ] UAT one-click flow passes.
* \[ ] UAT paper start/stop passes.
* \[ ] UAT demo recorder/training gate passes.
* \[ ] UAT live locked proof passes.
* \[ ] Evidence attached.

\---

## 35\. Fase 31 - Release/Knowledge/Test/Performance Integration

Roadmap 089:

* \[ ] Release notes include one-click launcher.
* \[ ] Version manifest includes app-control and live-training schema.
* \[ ] Installer/packaging notes include launcher files.
* \[ ] Migration notes explain profiles and demo training data.

Roadmap 091:

* \[ ] Knowledge graph maps profile → settings → data bootstrap → runtime → dashboard.
* \[ ] Knowledge graph maps demo data → dataset → validation gate → live readiness.
* \[ ] Impact analysis detects profile/schema/runtime/training changes.

Roadmap 092:

* \[ ] Test selector chooses app-control tests for launcher/profile/runtime changes.
* \[ ] Test selector chooses live-training tests for demo recorder/dataset/gate changes.
* \[ ] Dashboard control center changes select browser smoke.

Roadmap 093:

* \[ ] Startup time budget.
* \[ ] Dashboard open time budget.
* \[ ] Runtime start time budget.
* \[ ] Data bootstrap time budget.
* \[ ] Demo recorder overhead budget.
* \[ ] Dataset build time budget.
* \[ ] Error recovery metrics.

Acceptatiecriteria:

* \[ ] Release evidence includes one-click app evidence.
* \[ ] Release evidence includes live-training evidence if live profiles exist.
* \[ ] Knowledge graph updated.
* \[ ] Test selection works.
* \[ ] Secret/live-gate proof preserved.

\---

## 36\. Fase 32 - Scheduled App Health Reports

Scheduled jobs:

* \[ ] daily profile validation.
* \[ ] daily secret ref status check, fingerprint only.
* \[ ] daily launcher script validation.
* \[ ] weekly app startup smoke.
* \[ ] weekly paper start/stop smoke.
* \[ ] weekly demo recorder smoke.
* \[ ] weekly dataset quality check.
* \[ ] weekly model validation gate report.
* \[ ] weekly demo/testnet readiness check if configured.
* \[ ] weekly live readiness blocked/ready report if live profile exists.
* \[ ] monthly app evidence export.

Metrics:

* \[ ] startup success/failure;
* \[ ] dashboard open time;
* \[ ] default profile validity;
* \[ ] data bootstrap failures;
* \[ ] runtime start failures;
* \[ ] demo recording count;
* \[ ] dataset quality score;
* \[ ] validation gate grade;
* \[ ] secret ref missing count;
* \[ ] live readiness blockers;
* \[ ] emergency stop tests;
* \[ ] evidence export status.

Acceptatiecriteria:

* \[ ] Jobs are local-only.
* \[ ] Jobs never start live trading.
* \[ ] Reports are secret-free.
* \[ ] Dashboard can show reports.
* \[ ] Check-all safe env preserved.

\---

## 37\. Tests

### Unit tests

* \[ ] `tests/test\_unified\_bot\_app\_safety\_contract.py`
* \[ ] `tests/test\_bot\_profile.py`
* \[ ] `tests/test\_profile\_store.py`
* \[ ] `tests/test\_secret\_refs.py`
* \[ ] `tests/test\_config\_wizard.py`
* \[ ] `tests/test\_app\_supervisor.py`
* \[ ] `tests/test\_one\_click\_launcher.py`
* \[ ] `tests/test\_runtime\_orchestrator.py`
* \[ ] `tests/test\_data\_bootstrap.py`
* \[ ] `tests/test\_demo\_spot\_data\_recorder.py`
* \[ ] `tests/test\_demo\_dataset\_quality.py`
* \[ ] `tests/test\_training\_dataset\_builder.py`
* \[ ] `tests/test\_model\_validation\_gate.py`
* \[ ] `tests/test\_live\_training\_evidence.py`
* \[ ] `tests/test\_backtest\_profile\_runner.py`
* \[ ] `tests/test\_live\_readiness\_gate.py`
* \[ ] `tests/test\_app\_control\_api.py`
* \[ ] `tests/test\_startup\_health.py`
* \[ ] `tests/test\_app\_evidence.py`
* \[ ] `tests/test\_profile\_matrix.py`

### Integration tests

* \[ ] Generate launcher files.
* \[ ] Start fake supervisor.
* \[ ] Create paper profile.
* \[ ] Bootstrap fixture data.
* \[ ] Start fake paper runtime.
* \[ ] Stop fake runtime.
* \[ ] Create demo profile with missing key.
* \[ ] Record demo fixture events.
* \[ ] Build demo training dataset fixture.
* \[ ] Run model validation gate fixture.
* \[ ] Validate live locked profile.
* \[ ] Export app/live-training evidence.
* \[ ] Verify no raw secrets.

### Browser smoke

* \[ ] `/control-center` loads.
* \[ ] profile selector visible.
* \[ ] config wizard visible.
* \[ ] create paper profile.
* \[ ] start paper bot.
* \[ ] pause/resume/stop.
* \[ ] demo recorder panel visible.
* \[ ] dataset quality panel visible.
* \[ ] training validation panel visible.
* \[ ] demo/testnet readiness panel visible.
* \[ ] live profile locked visible.
* \[ ] kill switch visible.
* \[ ] evidence export visible.

### Safety tests

* \[ ] Launcher cannot auto-start live.
* \[ ] Live profile locked by default.
* \[ ] Live requires explicit confirm.
* \[ ] Live requires demo/training evidence.
* \[ ] Raw API key in profile blocked.
* \[ ] Secrets redacted from logs/evidence/API.
* \[ ] Stop/Kill Switch always visible.
* \[ ] Live disarms on restart.
* \[ ] Live disarms on profile edit.
* \[ ] Current live execution remains blocked until live-execution gate PR.
* \[ ] Check-all safe env preserved.

\---

## 38\. Docs

Nieuwe docs:

```text
docs/unified-bot-app/unified-bot-app-safety-contract.md
docs/unified-bot-app/one-click-launcher.md
docs/unified-bot-app/bot-profiles.md
docs/unified-bot-app/profile-store.md
docs/unified-bot-app/secret-refs.md
docs/unified-bot-app/config-wizard.md
docs/unified-bot-app/app-supervisor.md
docs/unified-bot-app/runtime-orchestrator.md
docs/unified-bot-app/data-bootstrap.md
docs/unified-bot-app/control-center.md
docs/unified-bot-app/profile-matrix.md
docs/unified-bot-app/startup-health.md
docs/unified-bot-app/app-evidence.md
docs/live-training/demo-spot-data-recorder.md
docs/live-training/demo-dataset-quality.md
docs/live-training/training-dataset-builder.md
docs/live-training/model-validation-gate.md
docs/live-training/live-training-evidence.md
docs/live-trading/live-readiness-gate.md
docs/live-trading/live-execution-implementation-gate.md
docs/live-trading/live-operator-checklist.md
```

README updates:

* \[ ] “Start with one click”.
* \[ ] Windows launcher guide.
* \[ ] Dashboard Control Center guide.
* \[ ] Profile guide.
* \[ ] API key/secret ref guide.
* \[ ] Demo spot data training guide.
* \[ ] Backtest/paper/demo/testnet/live profile matrix.
* \[ ] Live trading warning and readiness gates.
* \[ ] Troubleshooting.

\---

## 39\. Codex bouwvolgorde

### PR 1 - Safety Contract + Bot Profile Schema

* \[ ] `docs/unified-bot-app/unified-bot-app-safety-contract.md`
* \[ ] `app\_control/bot\_profile.py`
* \[ ] profile validation tests.
* \[ ] live auto-start blocker tests.
* \[ ] training gate requirement tests.
* \[ ] secret redaction tests.

### PR 2 - Profile Store + Templates

* \[ ] `profile\_store.py`
* \[ ] built-in profile templates.
* \[ ] live locked training-required template.
* \[ ] import/export/migration tests.

### PR 3 - Secret Refs + Config Wizard

* \[ ] `secret\_refs.py`
* \[ ] `config\_wizard.py`
* \[ ] redaction and wizard tests.

### PR 4 - App Supervisor + One-Click Launcher

* \[ ] `app\_supervisor.py`
* \[ ] `one\_click\_launcher.py`
* \[ ] Windows `.cmd`/`.ps1` generation.
* \[ ] fake server tests.

### PR 5 - Runtime Orchestrator + Data Bootstrap

* \[ ] `runtime\_orchestrator.py`
* \[ ] `data\_bootstrap.py`
* \[ ] profile-to-runtime tests.

### PR 6 - Demo Spot Data Recorder

* \[ ] `live\_training/demo\_spot\_data\_recorder.py`
* \[ ] demo event manifest.
* \[ ] no-secret tests.

### PR 7 - Dataset Quality + Training Dataset Builder

* \[ ] `live\_training/demo\_dataset\_quality.py`
* \[ ] `live\_training/training\_dataset\_builder.py`
* \[ ] quality/leakage/manifest tests.

### PR 8 - Model Validation Gate + Live Training Evidence

* \[ ] `live\_training/model\_validation\_gate.py`
* \[ ] `live\_training/live\_training\_evidence.py`
* \[ ] validation grade tests.
* \[ ] evidence verify tests.

### PR 9 - Backtest/Paper/Demo/Testnet Profile Integration

* \[ ] backtest runner.
* \[ ] paper start/stop.
* \[ ] demo readiness/recorder.
* \[ ] testnet readiness.
* \[ ] browser/API tests.

### PR 10 - Live Readiness Gate + Live Execution Gate Docs

* \[ ] `live\_readiness\_gate.py`
* \[ ] live execution implementation gate doc.
* \[ ] tests proving live remains locked until gate.

### PR 11 - Control Center Dashboard + App API

* \[ ] `/control-center`.
* \[ ] profile wizard UI.
* \[ ] runtime controls UI.
* \[ ] training gate UI.
* \[ ] App Control API routes.
* \[ ] browser smoke.

### PR 12 - Evidence, Startup Health, Profile Matrix \& Check-All

* \[ ] `startup\_health.py`
* \[ ] `app\_evidence.py`
* \[ ] profile matrix.
* \[ ] check-all integration.

### PR 13 - Docs, UAT, Release/Knowledge/Test/Performance Integration

* \[ ] docs.
* \[ ] UAT one-click + demo-training scenarios.
* \[ ] release notes.
* \[ ] knowledge/test/performance integration.
* \[ ] scheduled reports.

\---

## 40\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 116 PR 1: Unified Bot App Safety Contract + Bot Profile Schema.

Maak docs/unified-bot-app/unified-bot-app-safety-contract.md.

Maak src/binance\_spot\_bot/app\_control/\_\_init\_\_.py.
Maak src/binance\_spot\_bot/app\_control/bot\_profile.py met:
- BotProfile
- BotProfileMode
- BotProfileExchange
- BotProfileDataSource
- BotProfileRisk
- BotProfileModel
- BotProfileTrainingGate
- BotProfileSecretsRef
- BotProfileValidationResult
- BotProfileReport
- validate\_bot\_profile(profile: BotProfile)
- bot\_profile\_to\_dict(...)
- write\_bot\_profile\_report(...)

Modes:
- backtest
- paper
- demo\_spot
- testnet
- live\_locked
- live\_armed
- disabled

BotProfile moet minimaal ondersteunen:
- profile\_id
- name
- description
- mode
- exchange\_profile
- base\_url
- symbol
- watchlist\_id
- interval
- data\_source
- model\_alias
- strategy\_id
- risk\_preset
- max\_daily\_loss\_quote
- max\_position\_quote
- max\_trades\_per\_day
- min\_signal\_confidence
- max\_spread\_bps
- starting\_quote\_balance
- secret\_ref
- dashboard\_workspace\_id
- auto\_open\_dashboard
- auto\_fetch\_data
- auto\_start\_runtime
- live\_trading\_enabled
- kill\_switch
- manual\_live\_approval
- requires\_demo\_training\_evidence
- required\_demo\_sessions
- required\_min\_demo\_fills
- required\_dataset\_quality\_score
- required\_validation\_grade
- no\_live\_auto\_start\_statement
- created\_at\_ms
- updated\_at\_ms

Validatie moet blokkeren op:
- raw API key/secret in profile JSON
- live mode with auto\_start\_runtime=True
- live mode without requires\_demo\_training\_evidence=True
- live mode without required\_demo\_sessions > 0
- live mode without required\_min\_demo\_fills > 0
- live mode without required\_dataset\_quality\_score > 0
- live mode without required\_validation\_grade
- live mode without risk limits
- live mode with missing kill\_switch/manual approval controls
- unknown exchange profile
- unsafe base\_url
- invalid symbol/interval
- missing risk preset
- secret-like values
- buy/sell/guaranteed profit wording

Gebruik alleen stdlib.
Geen command execution.
Geen API calls.
Geen runtime execution.
Geen frontend execution.
Geen Streamlit wijzigen.
Geen signed endpoints.
Geen account/order endpoints.
Geen live trading.

Voeg tests toe voor:
- valid paper profile
- valid demo\_spot profile
- valid live\_locked profile with demo training requirements
- live auto\_start\_runtime blocked
- live without demo training evidence blocked
- live without dataset quality threshold blocked
- live without validation grade blocked
- raw API key blocked
- unsafe base\_url blocked
- invalid symbol blocked
- advice/profit wording blocked
- JSON serialization
- secret-like values worden geredact
```

Waarom eerst:

* De hele one-click app moet rond veilige profielen gebouwd worden.
* Live mag niet verder komen zonder demo-data/training/validatie requirements.
* Dit is read-only en raakt runtime/trading/frontend niet.
* Het is klein genoeg voor Codex.
* Daarna kunnen profile store, launcher, orchestrator en dashboard veilig volgen.

\---

## 41\. Definition of Done

Roadmap 116 is klaar als:

* \[ ] Unified Bot App Safety Contract bestaat.
* \[ ] Bot Profile Schema werkt.
* \[ ] Profile Store \& Templates werken.
* \[ ] Local Secret Reference Manager werkt.
* \[ ] Config Wizard API werkt.
* \[ ] App Supervisor werkt.
* \[ ] One-Click Launcher Files werken.
* \[ ] Unified Runtime Orchestrator werkt.
* \[ ] Data Bootstrap Manager werkt.
* \[ ] Demo Spot Data Recorder werkt.
* \[ ] Demo Dataset Quality Gate werkt.
* \[ ] Training Dataset Builder werkt.
* \[ ] Model/Strategy Training \& Validation Gate werkt.
* \[ ] Live Training Evidence Bundle werkt.
* \[ ] Backtest Profile Integration werkt.
* \[ ] Paper Profile Integration werkt.
* \[ ] Binance Demo Spot Profile Integration werkt.
* \[ ] Binance Spot Testnet Profile Integration werkt.
* \[ ] Live Locked Profile \& Readiness Gate werkt.
* \[ ] Live Execution Implementation Gate doc bestaat.
* \[ ] Unified Bot Control Center Dashboard werkt.
* \[ ] Dashboard Start UX werkt.
* \[ ] Unified App API werkt.
* \[ ] Unified CLI Commands werken.
* \[ ] Startup Health \& Error Recovery werkt.
* \[ ] Audit, Evidence \& Support Bundle werkt.
* \[ ] Live Trading UX Guardrails werken.
* \[ ] Dashboard Workspace Integration werkt.
* \[ ] Profile Matrix werkt.
* \[ ] Check-All Integration werkt.
* \[ ] Operator/UAT Integration werkt.
* \[ ] Release/Knowledge/Test/Performance Integration werkt.
* \[ ] Scheduled App Health Reports werken.
* \[ ] Tests bewijzen launcher nooit live auto-start.
* \[ ] Tests bewijzen live training/demo evidence vereist is.
* \[ ] Tests bewijzen secrets nooit lekken.
* \[ ] Tests bewijzen live execution geblokkeerd blijft tot aparte gate.
* \[ ] Browser smoke toont one-click Control Center flow.
* \[ ] Check-all blijft groen.
* \[ ] Roadmap 116 kan na uitvoering naar `Voltooid docs`.

\---

## 42\. Verwachte Roadmap 117 daarna

Als Roadmap 116 groen is:

```text
Roadmap 117 - Live Trading Dry-Run, Testnet-to-Live Promotion Gate \& Minimal Real-Order Execution Safety Layer
```

Mogelijke inhoud:

* \[ ] live dry-run mode;
* \[ ] read-only live account checks;
* \[ ] order preview;
* \[ ] tiny capped first live order gate;
* \[ ] live cancel/emergency stop;
* \[ ] live audit/evidence;
* \[ ] live kill-switch drills;
* \[ ] still gated, no unattended live.

```

Als Roadmap 116 nog te weinig demo data heeft:

```text
Roadmap 117 - Demo Spot Data Collection Sprint, Dataset Quality Burn-Down \& Model Validation Improvement
```

Mogelijke inhoud:

* \[ ] meer demo sessions opnemen;
* \[ ] dataset quality verbeteren;
* \[ ] feature alignment;
* \[ ] validation grade verbeteren;
* \[ ] paper/testnet rehearsal uitbreiden;
* \[ ] live blijft locked.

```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: One-click launcher with demo/data/training safe live gate.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.

## Uitvoering 2026-05-15

Status: Voltooid / Gevalideerd.

Gebouwd:

- `app_control` package met bot profiles, profile store/templates, secret refs, config wizard, supervisor plan, one-click launcher generation, runtime orchestrator, data bootstrap, startup health, profile matrix en app evidence.
- `live_training` package met demo recorder, dataset quality gate, training dataset builder, model validation gate, live training evidence en live readiness gate.
- Dashboard V2 `/control-center` pagina en app-control/live-training API routes.
- CLI commands voor profiles, launcher, startup health, data bootstrap, runtime start/stop, demo training, model validation, live readiness en live arm.
- Check-all integratie voor app-control en demo-training gates.
- Docs voor unified bot app, live training en live readiness.
- Acceptance tests voor roadmap 116.

Validatie:

- `python -m compileall -q src tests`
- `python -m pytest -q tests/test_roadmap_116_unified_bot_app_acceptance.py` -> 5 passed.
- CLI smokes voor profiles/startup/demo-training/control-center/live-arm.
- `npm install; npm run build`
- `python -m binance_spot_bot.cli security-scan` -> geen findings.
- `python -m binance_spot_bot.cli dashboard-v2-smoke --json` -> ok.
- `python -m binance_spot_bot.cli check-all --skip-tests --json` -> ok.
- Browser render `/control-center` screenshot: `%TEMP%/control-center-116.png`.
- `python -m pytest -q` -> 447 passed, 1 warning.

Safety:

- One-click launcher start nooit live trading.
- Live profile blijft locked en live-arm blijft geblokkeerd door aparte live-execution implementation gate.
- API keys blijven secret refs/fingerprints en worden niet in profiles/evidence getoond.
- Alle app-control/live-training responses houden `live_trading_enabled=false`.

