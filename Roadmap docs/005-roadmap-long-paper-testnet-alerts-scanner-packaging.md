# Roadmap 005 - Lange Paper/Testnet Sessies, Alerts, Scanner, Modeltraining en Windows Packaging

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-09  
Volgt op:

* `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
* `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
* `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
* `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`

Doel: verder bouwen op de afgeronde Roadmaps 001 t/m 004. Roadmap 005 focust op langdurige paper/testnet-validatie, operator alerts, expliciet gated testnet order placement, multi-symbol watchlist/scanner, sterkere modeltraining met checkpoints, betere lokale opslag en Windows packaging. Live trading blijft volledig buiten scope.

\---

## 0\. Correctie en controle vooraf

### Gevonden afgeronde roadmaps

* \[x] Roadmap 001 - veilige Binance Spot AI trading bot basis.
* \[x] Roadmap 002 - lokale visuele paper bot dashboard.
* \[x] Roadmap 003 - realtime market data, ModelOps en dashboard verdieping.
* \[x] Roadmap 004 - Windows one-click secure bot control center.

### Conclusie

* \[x] Er bestaat al een Roadmap 003 in `Voltooid docs`.
* \[x] Er bestaat ook al een Roadmap 004 in `Voltooid docs`.
* \[x] Nieuwe roadmap moet dus **Roadmap 005** zijn.
* \[x] Geen overlap plannen met afgeronde Roadmap 003/004.
* \[x] Eerst volledige codebase-analyse uitvoeren vóór nieuwe features gepland worden.

\---

## 1\. Samenvatting bestaande basis

### Roadmap 001 leverde / beschreef

* \[x] Paper/testnet-first Binance Spot bot.
* \[x] Neural network alleen als signaalgenerator.
* \[x] Deterministische `RiskEngine` als enige trade gate.
* \[x] Binance REST adapter.
* \[x] Datastore, features, labels.
* \[x] Baseline model en tiny neural model.
* \[x] Backtest engine.
* \[x] Paper trader.
* \[x] Audit logging.
* \[x] Monitoring.
* \[x] Live-readiness checklist.
* \[x] Live standaard geblokkeerd.

### Roadmap 002 leverde / beschreef

* \[x] Streamlit + Plotly dashboard.
* \[x] Lokale demo replay zonder API keys.
* \[x] Paper mode met bestaande risk/execution modules.
* \[x] Runtime supervisor.
* \[x] Dashboard controls.
* \[x] Testnet-readiness panel.
* \[x] Windows startcommando’s.
* \[x] Live niet selecteerbaar.

### Roadmap 003 leverde / beschreef

* \[x] Realtime stream parsers.
* \[x] WebSocket URL builders.
* \[x] Reconnect policy.
* \[x] Top-of-book/orderbook skeleton.
* \[x] Spread/staleness risk input.
* \[x] Data source abstraction voor demo, REST en WebSocket-degraded paper mode.
* \[x] Paper sessions, fills, snapshots en exports.
* \[x] Model registry met aliases.
* \[x] Chronologische evaluation workflow.
* \[x] Data-quality checks.
* \[x] Dashboard microstructure, data quality, sessions en ModelOps.

### Roadmap 004 leverde / beschreef

* \[x] Windows one-click launcher.
* \[x] Stop launcher.
* \[x] Local environment check scripts.
* \[x] Exchange profiles.
* \[x] Session-only credentials.
* \[x] Windows SecretManagement adapter.
* \[x] Connectivity checks.
* \[x] Settings persistence zonder secrets.
* \[x] User-data parsers.
* \[x] Order lifecycle store.
* \[x] Control center dashboard met:

  * profile/mode badges;
  * credentials;
  * bot controls;
  * risk controls;
  * model/evaluation;
  * market data;
  * orders/account;
  * sessions;
  * security tabs.
* \[x] Secret redaction en security scan uitgebreid.
* \[x] Live trading buiten scope.

\---

## 2\. Volledige codebase-analyse vóór Roadmap 005

### 2.1 Projectstructuur en packaging

Geanalyseerde onderdelen:

* `README.md`
* `pyproject.toml`
* `Start Bot Dashboard.cmd`
* `Stop Bot Dashboard.cmd`
* `scripts/start-dashboard.ps1`
* `scripts/stop-dashboard.ps1`
* `docs/local-dashboard.md`

Huidige status:

* \[x] Python 3.12+ project.
* \[x] Optional dependency groups bestaan:

  * `research`;
  * `dev`;
  * `ui`;
  * `realtime`;
  * `mlops`.
* \[x] CLI entrypoint bestaat.
* \[x] Windows one-click start bestaat.
* \[x] Dashboard draait lokaal via Streamlit.
* \[x] README documenteert safe demo, paper en dashboard start.

Gaten voor Roadmap 005:

* \[ ] Geen echte packaged Windows app of tray utility.
* \[ ] Geen installer/build script.
* \[ ] Geen duidelijke update-flow voor dependencies.
* \[ ] Geen “portable release folder” met start/stop/check scripts gebundeld.
* \[ ] Geen health check vóór unattended lange paper-sessie.

\---

### 2.2 Config, safety en modes

Geanalyseerde onderdelen:

* `BotSettings`
* `TradingMode`
* live-readiness guards
* exchange profiles
* dashboard-safe runtime creation

Huidige status:

* \[x] Default is fail-closed.
* \[x] Live vereist meerdere expliciete gates.
* \[x] Dashboard forceert live disabled.
* \[x] Exchange profiles bestaan voor local demo, Binance Demo Spot en Binance Spot Testnet.
* \[x] Session-only credentials zijn default.

Gaten voor Roadmap 005:

* \[ ] Geen aparte `PaperSessionPolicy`.
* \[ ] Geen unattended-session limieten:

  * max runtime;
  * max reconnects;
  * max alerts;
  * max degraded duration.
* \[ ] Geen aparte `TestnetOrderPolicy`.
* \[ ] Geen risk-policy versie/hash zichtbaar genoeg in alle exports.
* \[ ] Geen operator “preflight summary” vóór lange sessie.

\---

### 2.3 Binance REST en connectivity

Geanalyseerde onderdelen:

* `BinanceSpotAdapter`
* `connectivity.py`
* signed account checks
* exchange info parsing
* order/test-order endpoints

Huidige status:

* \[x] REST adapter ondersteunt public en signed endpoints.
* \[x] HMAC signing bestaat.
* \[x] Connectivity checks bestaan.
* \[x] Server time check bestaat.
* \[x] Exchange filters kunnen geladen worden.
* \[x] Test-order capability check bestaat.
* \[x] Live route blijft geblokkeerd.

Gaten voor Roadmap 005:

* \[ ] Geen echte guarded testnet place-order flow met expliciete confirm.
* \[ ] Geen volledige post-order reconciliation via REST query + user-data events.
* \[ ] Geen cancel-open-testnet-order workflow.
* \[ ] Geen “testnet only” hard URL/mode validator per command.
* \[ ] Geen structured rate-limit/circuit-breaker policy per lange sessie.

\---

### 2.4 Market data, WebSocket en orderbook

Geanalyseerde onderdelen:

* `market\_stream.py`
* `market\_data\_source.py`
* `orderbook.py`
* stream parser dataclasses
* reconnect policy
* top-of-book feed

Huidige status:

* \[x] Stream URL builders bestaan.
* \[x] Kline/bookTicker/trade/miniTicker parsers bestaan.
* \[x] ReconnectPolicy bestaat.
* \[x] TopOfBook en spreadberekening bestaan.
* \[x] WebSocket data source bestaat maar gebruikt veilige fallback/degraded mode.
* \[x] Runtime kan data source kiezen.

Gaten voor Roadmap 005:

* \[ ] Geen volledige echte WebSocket event loop voor lange sessies.
* \[ ] Geen durable event queue.
* \[ ] Geen stream latency histogram.
* \[ ] Geen reconnect-limit policy voor unattended runs.
* \[ ] Geen multi-symbol stream multiplexing.
* \[ ] Geen scanner over meerdere symbols.
* \[ ] Geen persistent market microstructure snapshots voor latere analyse.

\---

### 2.5 Runtime, sessions en dashboard

Geanalyseerde onderdelen:

* `runtime.py`
* `session\_store.py`
* `monitoring.py`
* `ui/streamlit\_app.py`
* `ui/state.py`
* `settings\_store.py`

Huidige status:

* \[x] `BotRuntime` beheert demo/paper/testnet-readiness.
* \[x] Runtime snapshots bevatten candles, signals, fills, equity, data quality, model, profile en lifecycle info.
* \[x] Sessions worden lokaal opgeslagen.
* \[x] Dashboard heeft tabs voor controls, credentials, risk, model, market data, sessions en security.
* \[x] Emergency stop bestaat.
* \[x] Dashboard toont live disabled.

Gaten voor Roadmap 005:

* \[ ] Geen echte foreground long-running paper-session CLI met duration.
* \[ ] Geen automatische checkpoint/resume van sessies.
* \[ ] Geen alert manager/watchdog die runtime stopt bij kritieke condities.
* \[ ] Geen complete Markdown/HTML report bundle per sessie.
* \[ ] Geen session compare met meerdere sessies tegelijk.
* \[ ] Geen watchlist/scanner dashboard.
* \[ ] Geen unattended-mode UX.

\---

### 2.6 Risk, execution en order lifecycle

Geanalyseerde onderdelen:

* `risk.py`
* `execution.py`
* `paper.py`
* `order\_lifecycle.py`
* `user\_data\_stream.py`

Huidige status:

* \[x] RiskEngine blokkeert op kill switch, HOLD, lage confidence, max trades, max loss, stale data en spread.
* \[x] ExecutionEngine bouwt orders met Decimal en filterchecks.
* \[x] Paper fills bestaan.
* \[x] Testnet test-order route bestaat.
* \[x] OrderLifecycleStore bestaat.
* \[x] User-data event parsers bestaan.

Gaten voor Roadmap 005:

* \[ ] Lifecycle store is nog niet overal durable/persistent.
* \[ ] Paper accounting mist realistischere fees/slippage/partial fills.
* \[ ] SELL risk moet bestaande base exposure strakker controleren.
* \[ ] Geen cooldown/loss-streak state.
* \[ ] Geen per-symbol risk state voor scanner/watchlist.
* \[ ] Geen gated echte testnet order placement.
* \[ ] Geen order cancel/reconcile dashboard action.

\---

### 2.7 ModelOps, training en evaluation

Geanalyseerde onderdelen:

* `signal\_model.py`
* `model\_registry.py`
* `evaluation.py`
* `features.py`
* `data\_quality.py`

Huidige status:

* \[x] Rule baseline bestaat.
* \[x] Tiny neural model bestaat.
* \[x] Model registry light bestaat.
* \[x] Evaluation gebruikt chronologische folds.
* \[x] Data quality en feature shift checks bestaan.

Gaten voor Roadmap 005:

* \[ ] Geen echte PyTorch checkpoint pipeline.
* \[ ] Geen sklearn baseline suite uitgebreid genoeg.
* \[ ] Geen model promotion policy:

  * candidate;
  * rejected;
  * paper-approved;
  * champion.
* \[ ] Geen artifact hash + dataset hash verplicht.
* \[ ] Geen model drift gate vóór lange paper sessie.
* \[ ] Geen multi-symbol training/evaluation.
* \[ ] Geen MLflow/DuckDB integratie.

\---

### 2.8 Security en secrets

Geanalyseerde onderdelen:

* `security.py`
* `redaction.py`
* `audit.py`
* `credentials.py`
* settings persistence

Huidige status:

* \[x] Secret scan bestaat.
* \[x] Redaction helpers bestaan.
* \[x] AuditLog scrubt payloads.
* \[x] Credentials default session-only.
* \[x] Windows SecretStore adapter bestaat als veilige optionele richting.
* \[x] SettingsStore stripte secretachtige keys.

Gaten voor Roadmap 005:

* \[ ] Geen automatische security preflight vóór long-run.
* \[ ] Geen incident bundle export.
* \[ ] Geen audit rotation/retention.
* \[ ] Geen check of session reports secrets bevatten.
* \[ ] Geen “panic package” instructies:

  * stop bot;
  * revoke testnet keys;
  * cancel testnet orders;
  * export logs.

\---

## 3\. Roadmap 005 scope

In scope:

* \[ ] Lange paper/testnet sessies in foreground CLI.
* \[ ] Alert manager en watchdog.
* \[ ] Gated testnet place-order en cancel/reconcile flow.
* \[ ] Multi-symbol watchlist en scanner.
* \[ ] Realistischere paper accounting.
* \[ ] PyTorch checkpoint training pipeline.
* \[ ] Model promotion policy.
* \[ ] Dataset/model/report storage via DuckDB of structured local store.
* \[ ] Session report bundles.
* \[ ] Windows portable packaging.

Out of scope:

* \[ ] Live trading.
* \[ ] Margin/futures/leverage.
* \[ ] Withdrawals.
* \[ ] Autonome LLM orderbeslissingen.
* \[ ] Cloud deployment.
* \[ ] Echte winstclaims.

\---

## 4\. Fase 0 - Preflight quality gate voor Roadmap 005

Doel: vóór nieuwe functionaliteit een harde check-flow afdwingen.

### Taken

* \[ ] Voeg `scripts/check-all.ps1` toe.
* \[ ] Voeg `scripts/check-all.py` toe voor cross-platform checks.
* \[ ] Checks:

  * unit tests;
  * config validation;
  * security scan;
  * dashboard import smoke;
  * CLI smoke;
  * no-live-ui check;
  * no-secret-in-settings/session check.
* \[ ] Voeg `python -m binance\_spot\_bot.cli preflight` command toe.
* \[ ] Preflight output:

  * Python version;
  * dependency groups aanwezig;
  * config mode;
  * live disabled;
  * selected profile;
  * credentials status;
  * connectivity status;
  * writable data dirs;
  * security scan summary.
* \[ ] Dashboard krijgt Preflight tab/panel.

### Acceptatiecriteria

* \[ ] Eén command kan lokaal alle checks draaien.
* \[ ] Preflight werkt zonder API keys in demo mode.
* \[ ] Testnet preflight toont exact welke vereisten ontbreken.
* \[ ] Geen nieuwe fase start voordat preflight groen is.

\---

## 5\. Fase 1 - Long-running paper-session CLI

Doel: langere paper-sessies kunnen draaien als foreground proces met duidelijke stop en rapportage.

### Nieuwe command

```powershell
python -m binance\_spot\_bot.cli paper-session --symbol BTCUSDT --interval 1m --duration-minutes 60 --source websocket
```

### Taken

* \[ ] Voeg `PaperSessionRunner` toe.
* \[ ] Foreground loop:

  * start runtime;
  * verwerkt ticks/events;
  * schrijft snapshots;
  * schrijft heartbeats;
  * stopt netjes bij Ctrl+C.
* \[ ] Runtime policies:

  * max duration;
  * max degraded seconds;
  * max reconnects;
  * max consecutive data-quality warnings;
  * max critical alerts.
* \[ ] Session checkpoints:

  * current equity;
  * position;
  * open lifecycle orders;
  * alerts;
  * source status;
  * model version.
* \[ ] CLI toont periodiek compacte status:

  * elapsed;
  * source status;
  * equity;
  * PnL;
  * trades;
  * blocks;
  * alerts.
* \[ ] Dashboard kan actieve long session volgen.

### Acceptatiecriteria

* \[ ] 60 minuten demo paper-session kan zonder internet draaien.
* \[ ] WebSocket/paper mode degradeert veilig als internet ontbreekt.
* \[ ] Ctrl+C sluit sessie netjes af en schrijft final summary.
* \[ ] Session krijgt status:

  * completed;
  * stopped;
  * failed;
  * watchdog\_stopped.
* \[ ] Geen live mode mogelijk.

\---

## 6\. Fase 2 - AlertManager en Watchdog

Doel: runtime problemen zichtbaar maken en automatisch blokkeren/stoppen wanneer nodig.

### Nieuwe module

```text
src/binance\_spot\_bot/alerts.py
```

### Alert dataclass

```text
Alert
- alert\_id
- timestamp\_ms
- severity: info | warning | error | critical
- component
- code
- message
- action
- session\_id
- correlation\_id
```

### Taken

* \[ ] Voeg `AlertManager` toe.
* \[ ] Voeg `WatchdogPolicy` toe.
* \[ ] Alertbronnen:

  * stale market data;
  * WebSocket disconnected;
  * fallback active te lang;
  * high spread;
  * data quality unhealthy;
  * rate-limit warning;
  * circuit breaker open;
  * unknown order status;
  * reconciliation failed;
  * secret scan finding;
  * unexpected signed mode;
  * testnet credentials missing;
  * model drift warning.
* \[ ] Watchdog acties:

  * `observe`;
  * `block\_trading`;
  * `pause\_runtime`;
  * `stop\_runtime`.
* \[ ] Dashboard toont:

  * active alerts;
  * severity badges;
  * alert history;
  * watchdog action.
* \[ ] AuditLog krijgt alert events.
* \[ ] Session reports nemen alerts op.

### Acceptatiecriteria

* \[ ] Critical alert stopt long-running paper/testnet session.
* \[ ] Error alert blokkeert execution maar laat dashboard draaien.
* \[ ] Warning alert is zichtbaar maar stopt niet automatisch.
* \[ ] Alerts zijn exporteerbaar per sessie.
* \[ ] Tests dekken severity/action mapping.

\---

## 7\. Fase 3 - Gated Spot Testnet order placement

Doel: technische testnet order placement valideren zonder live risico.

### Nieuwe commands

```powershell
python -m binance\_spot\_bot.cli testnet-check --symbol BTCUSDT
python -m binance\_spot\_bot.cli testnet-test-order --symbol BTCUSDT --side BUY --quote-size 10
python -m binance\_spot\_bot.cli testnet-place-small-order --symbol BTCUSDT --side BUY --quote-size 10 --confirm TESTNET\_ONLY
python -m binance\_spot\_bot.cli testnet-cancel-open --symbol BTCUSDT --confirm TESTNET\_CANCEL
```

### Guardrails

* \[ ] Alleen profile `binance-demo-spot` of `binance-spot-testnet`.
* \[ ] Live base URL hard geblokkeerd.
* \[ ] `TradingMode.LIVE` hard geblokkeerd.
* \[ ] `LIVE\_TRADING\_ENABLED` moet false zijn.
* \[ ] Manual confirm exact vereist.
* \[ ] Quote size max via `TESTNET\_MAX\_ORDER\_QUOTE`.
* \[ ] Exchange filters verplicht geladen.
* \[ ] Connectivity check verplicht ok.
* \[ ] User-data/lifecycle store actief of REST reconciliation fallback actief.
* \[ ] Geen retry zonder reconciliation.

### Taken

* \[ ] Voeg `TestnetOrderPolicy` toe.
* \[ ] Voeg `TestnetOrderService` toe.
* \[ ] Plaats kleine testnet order alleen na policy approval.
* \[ ] Query order status na plaatsing.
* \[ ] Update `OrderLifecycleStore`.
* \[ ] Cancel open testnet order optioneel.
* \[ ] Dashboard Orders tab krijgt guarded testnet actions.
* \[ ] Elke action schrijft audit event.

### Acceptatiecriteria

* \[ ] Zonder credentials blokkeert alles netjes.
* \[ ] Met verkeerde profile blokkeert alles.
* \[ ] Met live URL blokkeert alles.
* \[ ] Test order endpoint werkt apart van echte testnet place order.
* \[ ] Echte testnet order kan alleen met `TESTNET\_ONLY`.
* \[ ] Unknown status leidt tot reconciliation.
* \[ ] Geen live order path toegevoegd.

\---

## 8\. Fase 4 - Durable order lifecycle en reconciliation

Doel: paper/testnet orderstatussen duurzaam volgen over runtime en dashboard heen.

### Taken

* \[ ] Maak `OrderLifecycleStore` persistent:

  * JSONL of DuckDB.
* \[ ] Voeg lifecycle events toe:

  * INTENT;
  * BUILT;
  * SUBMITTED;
  * ACK;
  * NEW;
  * PARTIALLY\_FILLED;
  * FILLED;
  * CANCELED;
  * REJECTED;
  * EXPIRED;
  * UNKNOWN;
  * RECONCILED.
* \[ ] Koppel `ExecutionEngine` aan lifecycle store.
* \[ ] Koppel `PaperTrader` aan lifecycle store.
* \[ ] Koppel user-data execution reports aan lifecycle store.
* \[ ] Voeg `OrderReconciler` toe:

  * query via REST;
  * update lifecycle;
  * mark unresolved na max attempts.
* \[ ] Dashboard timeline per order.
* \[ ] Session report order lifecycle summary.

### Acceptatiecriteria

* \[ ] Elke paper fill heeft lifecycle.
* \[ ] Elke testnet order heeft lifecycle.
* \[ ] Runtime restart kan laatste lifecycle events tonen.
* \[ ] Unknown orders zijn zichtbaar en blokkerend tot reconcile.
* \[ ] Tests dekken alle lifecycle transitions.

\---

## 9\. Fase 5 - Realistischer paper accounting

Doel: paperresultaten minder misleidend maken.

### Nieuwe module

```text
src/binance\_spot\_bot/paper\_accounting.py
```

### Taken

* \[ ] Voeg `PaperAccount` toe:

  * quote balance;
  * base balances per symbol;
  * average entry;
  * realized PnL;
  * unrealized PnL;
  * fees paid;
  * exposure quote;
  * equity.
* \[ ] Voeg fill model toe:

  * fixed fee bps;
  * fixed slippage bps;
  * spread-aware price;
  * optional partial fill simulation.
* \[ ] Simuleer rejections:

  * min notional;
  * lot size;
  * stale data;
  * high spread;
  * insufficient quote;
  * insufficient base.
* \[ ] RiskEngine krijgt actuele account state uit PaperAccount.
* \[ ] Dashboard toont:

  * realized PnL;
  * unrealized PnL;
  * fees;
  * average entry;
  * exposure;
  * max drawdown.
* \[ ] Session report bevat accounting breakdown.

### Acceptatiecriteria

* \[ ] Paper PnL verwerkt fees/slippage.
* \[ ] SELL zonder base wordt geblokkeerd.
* \[ ] Exposure klopt per symbol.
* \[ ] Daily loss gate gebruikt correcte PnL policy.
* \[ ] Tests dekken BUY/SELL/accounting edge cases.

\---

## 10\. Fase 6 - Multi-symbol watchlist en scanner

Doel: meerdere symbolen volgen zonder meteen multi-symbol trading volledig te automatiseren.

### Taken

* \[ ] Voeg `WatchlistConfig` toe:

  * symbols;
  * intervals;
  * enabled data source;
  * max symbols.
* \[ ] Voeg `ScannerEngine` toe:

  * haalt features per symbol;
  * berekent signalen;
  * berekent risk precheck;
  * maakt ranking.
* \[ ] Scanner output:

  * symbol;
  * last price;
  * spread bps;
  * data quality;
  * signal side;
  * confidence;
  * risk block reason;
  * model version.
* \[ ] Dashboard Watchlist tab:

  * table;
  * sort by confidence;
  * filter by data quality;
  * show block reason;
  * no auto-trade toggle.
* \[ ] CLI:

  * `python -m binance\_spot\_bot.cli scan-watchlist --symbols BTCUSDT,ETHUSDT,BNBUSDT --interval 1m`
* \[ ] Rate-limit policy voor multi-symbol REST/WebSocket.

### Acceptatiecriteria

* \[ ] Scanner plaatst geen orders.
* \[ ] Scanner gebruikt bestaande SignalModel en RiskEngine.
* \[ ] Dashboard toont top candidates, maar execution blijft handmatig/paper-session scoped.
* \[ ] Rate-limit warning zichtbaar bij te veel symbols.
* \[ ] Tests gebruiken fake data source.

\---

## 11\. Fase 7 - Modeltraining met checkpoints en promotiebeleid

Doel: van “tiny demo model” naar reproduceerbare modeltraining zonder live risico.

### Nieuwe modules

```text
src/binance\_spot\_bot/training.py
src/binance\_spot\_bot/model\_promotion.py
```

### Taken

* \[ ] Voeg baselines toe:

  * no-trade;
  * buy-and-hold;
  * momentum;
  * mean reversion;
  * rule-based.
* \[ ] Voeg sklearn baseline toe als `\[mlops]` geïnstalleerd is.
* \[ ] Voeg PyTorch model toe als `\[research]` geïnstalleerd is.
* \[ ] Save PyTorch checkpoints:

  * state\_dict;
  * config;
  * feature schema;
  * dataset hash;
  * metrics;
  * seed.
* \[ ] Model status:

  * candidate;
  * rejected;
  * paper-approved;
  * champion;
  * archived.
* \[ ] Promotiecriteria:

  * out-of-sample beter dan baselines;
  * max drawdown onder limiet;
  * turnover niet extreem;
  * calibration acceptabel;
  * data quality ok;
  * no leakage checks ok.
* \[ ] Runtime laadt standaard alleen:

  * baseline;
  * paper-approved;
  * champion.
* \[ ] Dashboard ModelOps tab toont promotion status.

### Acceptatiecriteria

* \[ ] Model kan niet gepromoot worden op train metrics alleen.
* \[ ] Slecht model wordt rejected.
* \[ ] Artifact hash en dataset hash verplicht.
* \[ ] Paper-session report vermeldt model status.
* \[ ] Tests dekken promotion/rejection rules.

\---

## 12\. Fase 8 - Dataset en lokale storage upgrade

Doel: betere analyse en rapportage met gestructureerde opslag.

### Opties

* JSONL blijft basis.
* DuckDB optioneel voor query’s.
* Parquet optioneel voor candles/features.

### Taken

* \[ ] Voeg `StorageBackend` interface toe:

  * jsonl;
  * duckdb optional;
  * parquet optional.
* \[ ] Voeg dataset manifest toe:

  * dataset\_id;
  * symbols;
  * interval;
  * source;
  * time range;
  * row count;
  * feature version;
  * hash.
* \[ ] Voeg session index toe:

  * sessions querybaar op symbol/model/date/status.
* \[ ] Voeg model index toe:

  * models querybaar op alias/status/metric.
* \[ ] Dashboard Sessions tab krijgt filters.
* \[ ] CLI:

  * `list-sessions --symbol BTCUSDT --status completed`
  * `list-models --status paper-approved`

### Acceptatiecriteria

* \[ ] JSONL blijft fallback.
* \[ ] Geen zware dependency verplicht voor demo.
* \[ ] DuckDB/Parquet alleen gebruikt als dependency aanwezig is.
* \[ ] Session/model listing sneller en betrouwbaarder.
* \[ ] Tests dekken fallbackgedrag.

\---

## 13\. Fase 9 - Session report bundle

Doel: elke lange sessie eindigt met bruikbare analyse.

### Nieuwe module

```text
src/binance\_spot\_bot/session\_report.py
```

### Report outputs

* \[ ] `summary.md`
* \[ ] `summary.json`
* \[ ] `fills.csv`
* \[ ] `equity.csv`
* \[ ] `alerts.jsonl`
* \[ ] `orders.jsonl`
* \[ ] `config-redacted.json`
* \[ ] `model-metadata.json`
* \[ ] `data-quality.json`

### Report inhoud

* \[ ] Session metadata.
* \[ ] Runtime mode/source/profile.
* \[ ] Config hash.
* \[ ] Risk policy.
* \[ ] Model version/status.
* \[ ] PnL:

  * realized;
  * unrealized;
  * total;
  * fees;
  * slippage.
* \[ ] Drawdown.
* \[ ] Trades/fills.
* \[ ] Block reasons.
* \[ ] Alerts.
* \[ ] Data-quality summary.
* \[ ] Order lifecycle summary.
* \[ ] Known limitations.
* \[ ] “Geen financieel advies / paper is geen live garantie” disclaimer.

### Acceptatiecriteria

* \[ ] Report bundle wordt automatisch geschreven aan einde paper-session.
* \[ ] Dashboard kan bundle downloaden.
* \[ ] Report bevat geen secrets.
* \[ ] Report is voldoende om Roadmap 006 te plannen.

\---

## 14\. Fase 10 - Incident en recovery workflows

Doel: operator kan veilig reageren op problemen.

### Taken

* \[ ] Voeg `panic-stop` CLI toe:

  * stopt local runtime;
  * markeert sessie stopped;
  * exporteert incident bundle.
* \[ ] Voeg `testnet-cancel-open` flow toe.
* \[ ] Voeg incident docs toe:

  * `docs/incident-runbook.md`.
* \[ ] Incident bundle:

  * redacted config;
  * latest alerts;
  * order lifecycle;
  * connectivity status;
  * audit tail;
  * user instructions.
* \[ ] Dashboard Security tab krijgt:

  * Panic stop;
  * Export incident bundle;
  * Testnet cancel checklist.

### Acceptatiecriteria

* \[ ] Panic stop werkt zonder credentials.
* \[ ] Testnet cancel vereist confirm.
* \[ ] Incident bundle bevat geen secrets.
* \[ ] Critical watchdog event kan incident bundle triggeren.

\---

## 15\. Fase 11 - Windows portable packaging

Doel: eenvoudiger starten zonder telkens terminalkennis.

### Taken

* \[ ] Voeg `scripts/build-portable.ps1` toe.
* \[ ] Output:

  * `dist/NeuralNetworkBinanceSpot/`
  * start/stop/check scripts;
  * README shortcut;
  * requirements lock/export;
  * local data dirs;
  * no secrets.
* \[ ] Optioneel:

  * tray utility research;
  * `.lnk` shortcut generator.
* \[ ] Package preflight:

  * Python aanwezig;
  * dependencies aanwezig;
  * streamlit import;
  * project path ok.
* \[ ] Dashboard link opent default browser.
* \[ ] Packaging docs:

  * `docs/windows-portable.md`.

### Acceptatiecriteria

* \[ ] Portable folder start dashboard via dubbelklik.
* \[ ] Geen secrets in dist.
* \[ ] Update-instructies zijn duidelijk.
* \[ ] Stop script sluit alleen eigen processen.
* \[ ] Path met spaties blijft werken.

\---

## 16\. Documentatie-update

Nieuwe of aangepaste docs:

* \[ ] `docs/preflight.md`
* \[ ] `docs/long-paper-sessions.md`
* \[ ] `docs/alerts-watchdog.md`
* \[ ] `docs/testnet-order-placement.md`
* \[ ] `docs/order-reconciliation.md`
* \[ ] `docs/watchlist-scanner.md`
* \[ ] `docs/model-training-promotion.md`
* \[ ] `docs/session-reports.md`
* \[ ] `docs/incident-runbook.md`
* \[ ] `docs/windows-portable.md`

README updates:

* \[ ] paper-session command.
* \[ ] scan-watchlist command.
* \[ ] testnet-check commands.
* \[ ] preflight command.
* \[ ] packaging command.
* \[ ] safety statement: live trading blijft disabled.

\---

## 17\. Testplan Roadmap 005

### Unit tests

* \[ ] Preflight.
* \[ ] PaperSessionRunner.
* \[ ] AlertManager.
* \[ ] WatchdogPolicy.
* \[ ] TestnetOrderPolicy.
* \[ ] TestnetOrderService with fake adapter.
* \[ ] OrderReconciler.
* \[ ] Durable OrderLifecycleStore.
* \[ ] PaperAccount.
* \[ ] ScannerEngine.
* \[ ] ModelPromotionPolicy.
* \[ ] Dataset manifest/storage fallback.
* \[ ] SessionReport.
* \[ ] Incident bundle.
* \[ ] Windows packaging scripts smoke.

### Integration/smoke tests

* \[ ] Demo paper-session 5 minuten simulated.
* \[ ] WebSocket unavailable fallback.
* \[ ] Dashboard import.
* \[ ] Dashboard no-live mode list.
* \[ ] CLI scan-watchlist with fake data.
* \[ ] Testnet commands blocked without credentials.
* \[ ] Security scan over generated reports/settings.

### Manual checks

* \[ ] Start dashboard via `.cmd`.
* \[ ] Run preflight.
* \[ ] Run demo paper-session.
* \[ ] Export report.
* \[ ] Trigger fake alert.
* \[ ] Panic stop.
* \[ ] Build portable folder.

\---

## 18\. Prioriteiten

### Eerst

1. \[ ] Fase 0 - Preflight quality gate.
2. \[ ] Fase 1 - Long-running paper-session CLI.
3. \[ ] Fase 2 - AlertManager en Watchdog.
4. \[ ] Fase 9 - Session report bundle.

### Daarna

5. \[ ] Fase 3 - Gated Spot Testnet order placement.
6. \[ ] Fase 4 - Durable order lifecycle en reconciliation.
7. \[ ] Fase 5 - Realistischer paper accounting.
8. \[ ] Fase 10 - Incident en recovery workflows.

### Daarna pas

9. \[ ] Fase 6 - Multi-symbol watchlist en scanner.
10. \[ ] Fase 7 - Modeltraining met checkpoints en promotiebeleid.
11. \[ ] Fase 8 - Dataset en lokale storage upgrade.
12. \[ ] Fase 11 - Windows portable packaging.

\---

## 19\. Definition of Done

Roadmap 005 is pas klaar als:

* \[ ] Preflight command bestaat en werkt.
* \[ ] Long-running paper-session werkt in demo mode zonder internet.
* \[ ] Long-running paper-session kan WebSocket/REST veilig gebruiken of netjes degraderen.
* \[ ] AlertManager en Watchdog blokkeren/stoppen bij kritieke condities.
* \[ ] Session report bundle wordt automatisch geëxporteerd.
* \[ ] Testnet order placement is expliciet gated en live-hard-blocked.
* \[ ] Order lifecycle is persistent en reconcilebaar.
* \[ ] Paper accounting gebruikt fees/slippage en correcte exposure.
* \[ ] Watchlist scanner plaatst geen orders en gebruikt bestaande model/risk modules.
* \[ ] Model promotion policy voorkomt promotie op train-only metrics.
* \[ ] Storage fallback werkt zonder zware dependencies.
* \[ ] Incident bundle bevat geen secrets.
* \[ ] Windows portable packaging werkt via dubbelklik.
* \[ ] Alle tests en security scan slagen.
* \[ ] README en docs zijn bijgewerkt.
* \[ ] Roadmap 005 kan naar `Voltooid docs/`.

\---

## 20\. Verwachte Roadmap 006 daarna

Alleen plannen na meetbare output van Roadmap 005:

* \[ ] Multi-symbol portfolio paper trading.
* \[ ] Betere strategy research op basis van lange sessierapporten.
* \[ ] MLflow integratie als lokale registry te beperkt wordt.
* \[ ] Geavanceerde alert delivery buiten dashboard.
* \[ ] Testnet endurance testing over meerdere dagen.
* \[ ] Live-readiness audit roadmap, nog steeds zonder live default.

