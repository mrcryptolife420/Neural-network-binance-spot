# Roadmap 006 - Multi-Symbol Portfolio Paper Trading, Testnet Endurance \& Research Maturity

Status: Concept / Vervolgroadmap  
Project: Neural network Binance spot  
Volgt op:

* `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
* `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
* `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
* `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
* `Roadmap docs/005-roadmap-long-paper-testnet-alerts-scanner-packaging.md`

Belangrijk: Roadmap 006 mag pas definitief worden gemaakt nadat Roadmap 005 is uitgevoerd of minimaal meetbare resultaten heeft opgeleverd. Deze roadmap is bedoeld als logische vervolgrichting, niet als vervanging van Roadmap 005.

Live trading blijft buiten scope.

\---

## 0\. Output-afspraak voor toekomstige roadmaps

* \[x] Elke nieuwe roadmap moet lokaal downloadbaar zijn in deze chat.
* \[x] Elke nieuwe roadmap moet een afvinkbare Markdown `.md` zijn.
* \[x] Eerst `Voltooid docs` controleren.
* \[x] Eerst `Roadmap docs` controleren.
* \[x] Eerst volledige codebase analyseren.
* \[x] Daarna pas vervolgroadmap maken.
* \[x] Geen overlap plannen met bestaande roadmaps.
* \[x] Nieuwe roadmap moet verder bouwen op de vorige roadmaps.

\---

## 1\. Waarom Roadmap 006 pas na Roadmap 005 komt

Roadmap 005 staat momenteel in `Roadmap docs` en focust op:

* \[ ] lange paper/testnet sessies;
* \[ ] alerts en watchdog;
* \[ ] gated testnet order placement;
* \[ ] durable order lifecycle;
* \[ ] realistischer paper accounting;
* \[ ] multi-symbol watchlist/scanner;
* \[ ] modeltraining met checkpoints;
* \[ ] storage upgrade;
* \[ ] session report bundles;
* \[ ] incident/recovery workflows;
* \[ ] Windows portable packaging.

Roadmap 006 moet dus niet dezelfde dingen opnieuw bouwen. Roadmap 006 moet voortbouwen op de outputs van Roadmap 005:

* \[ ] paper-session reports;
* \[ ] alert/watchdog logs;
* \[ ] testnet orderflow resultaten;
* \[ ] scanner output;
* \[ ] model promotion resultaten;
* \[ ] session report bundles;
* \[ ] incident/recovery resultaten;
* \[ ] portable packaging ervaring.

\---

## 2\. Hoofddoel Roadmap 006

Roadmap 006 brengt het project van single-symbol / scoped paper-validatie naar multi-symbol portfolio-validatie en langere testnet endurance.

Doel:

* \[ ] meerdere symbols tegelijk volgen;
* \[ ] portfolio-wide risk beheren;
* \[ ] meerdaagse testnet endurance valideren;
* \[ ] model research sturen op echte paper/testnet resultaten;
* \[ ] alerts buiten dashboard brengen;
* \[ ] live-readiness audit voorbereiden zonder live trading te activeren.

\---

## 3\. Scope

### In scope

* \[ ] Multi-symbol portfolio paper trading.
* \[ ] Portfolio RiskEngine uitbreiding.
* \[ ] Testnet endurance over meerdere uren/dagen.
* \[ ] Scanner-resultaten gebruiken voor portfolio-kandidaten.
* \[ ] Session report analyse over meerdere runs.
* \[ ] Model research maturity.
* \[ ] Drift en model monitoring over meerdere sessies.
* \[ ] External alert delivery.
* \[ ] Live-readiness audit-documentatie.

### Out of scope

* \[ ] Live trading.
* \[ ] Margin trading.
* \[ ] Futures trading.
* \[ ] Leverage.
* \[ ] Withdrawals.
* \[ ] Autonome LLM trading decisions.
* \[ ] Winstgaranties.
* \[ ] Cloud deployment als verplicht onderdeel.

\---

## 4\. Fase 0 - Roadmap 005 resultaten valideren

Doel: Roadmap 006 alleen starten als Roadmap 005 voldoende bewijs heeft opgeleverd.

### Taken

* \[ ] Controleer of Roadmap 005 volledig of gedeeltelijk uitgevoerd is.
* \[ ] Lees alle Roadmap 005 session report bundles.
* \[ ] Verzamel:

  * \[ ] PnL per sessie;
  * \[ ] max drawdown;
  * \[ ] fees;
  * \[ ] slippage;
  * \[ ] block reasons;
  * \[ ] alerts;
  * \[ ] data-quality issues;
  * \[ ] order lifecycle issues;
  * \[ ] testnet reconciliation issues;
  * \[ ] model status;
  * \[ ] scanner output.
* \[ ] Maak een `docs/roadmap-005-results-summary.md`.
* \[ ] Bepaal welke onderdelen stabiel genoeg zijn voor multi-symbol portfolio paper.

### Acceptatiecriteria

* \[ ] Er is bewijs uit Roadmap 005, niet alleen aannames.
* \[ ] Roadmap 006 start niet zonder minimaal demo/paper session reports.
* \[ ] Bekende failures uit Roadmap 005 worden meegenomen als blockers.
* \[ ] Live trading blijft buiten scope.

\---

## 5\. Fase 1 - Portfolio state model

Doel: meerdere symbols samen beheren in één portfolio state.

### Nieuwe module

```text
src/binance\_spot\_bot/portfolio.py
```

### Taken

* \[ ] Voeg `PortfolioState` toe:

  * \[ ] quote balance;
  * \[ ] balances per asset;
  * \[ ] positions per symbol;
  * \[ ] average entry per symbol;
  * \[ ] realized PnL per symbol;
  * \[ ] unrealized PnL per symbol;
  * \[ ] total equity;
  * \[ ] total exposure;
  * \[ ] fees paid.
* \[ ] Voeg `PortfolioPosition` toe.
* \[ ] Koppel `PaperAccount` uit Roadmap 005 aan portfolio-level state.
* \[ ] Maak portfolio snapshots per tick/session.
* \[ ] Voeg export toe:

  * \[ ] `portfolio\_snapshots.jsonl`;
  * \[ ] `portfolio\_equity.csv`.

### Acceptatiecriteria

* \[ ] Eén portfolio kan BTCUSDT, ETHUSDT en BNBUSDT tegelijk volgen.
* \[ ] Equity klopt over alle positions.
* \[ ] Fees en slippage worden per symbol én totaal bijgehouden.
* \[ ] Portfolio state bevat geen secrets.
* \[ ] Tests dekken multi-symbol accounting.

\---

## 6\. Fase 2 - Portfolio RiskEngine uitbreiding

Doel: bestaande `RiskEngine` uitbreiden zonder een tweede risk engine te bouwen.

### Taken

* \[ ] Voeg `PortfolioRiskLimits` toe:

  * \[ ] max total exposure quote;
  * \[ ] max exposure per symbol;
  * \[ ] max open positions;
  * \[ ] max correlated exposure;
  * \[ ] max daily portfolio loss;
  * \[ ] max daily symbol loss;
  * \[ ] max trades per symbol;
  * \[ ] max trades portfolio-wide.
* \[ ] Voeg `PortfolioRiskState` toe:

  * \[ ] trades per symbol;
  * \[ ] loss streak per symbol;
  * \[ ] cooldown per symbol;
  * \[ ] current exposure per symbol;
  * \[ ] current total exposure.
* \[ ] Laat de bestaande `RiskEngine` per-symbol decisions blijven maken.
* \[ ] Voeg daarna portfolio-level gate toe:

  * \[ ] allow;
  * \[ ] block;
  * \[ ] reduce-only;
  * \[ ] cooldown.
* \[ ] Dashboard toont:

  * \[ ] total exposure;
  * \[ ] per-symbol exposure;
  * \[ ] portfolio block reasons.

### Acceptatiecriteria

* \[ ] Portfolio risk voorkomt dat alle symbols tegelijk maximale positie nemen.
* \[ ] Per-symbol risk blijft werken.
* \[ ] Portfolio-wide max loss blokkeert alle nieuwe entries.
* \[ ] Reduce/exit logic blijft mogelijk zonder nieuwe BUY entries.
* \[ ] Tests dekken portfolio exposure en max open positions.

\---

## 7\. Fase 3 - Multi-symbol paper runtime

Doel: paper-session runner uitbreiden naar meerdere symbols.

### Nieuwe command

```powershell
python -m binance\_spot\_bot.cli portfolio-paper-session --symbols BTCUSDT,ETHUSDT,BNBUSDT --interval 1m --duration-minutes 120 --source websocket
```

### Taken

* \[ ] Voeg `PortfolioPaperRuntime` toe.
* \[ ] Reuse bestaande:

  * \[ ] `BotRuntime`;
  * \[ ] `MarketDataSource`;
  * \[ ] `SignalModel`;
  * \[ ] `RiskEngine`;
  * \[ ] `PaperAccount`;
  * \[ ] `SessionStore`;
  * \[ ] `AlertManager`.
* \[ ] Per symbol:

  * \[ ] candles;
  * \[ ] features;
  * \[ ] signal;
  * \[ ] risk precheck;
  * \[ ] paper execution.
* \[ ] Portfolio-level:

  * \[ ] exposure check;
  * \[ ] drawdown check;
  * \[ ] cooldown check;
  * \[ ] equity curve.
* \[ ] Session report uitbreiden met portfolio-sectie.

### Acceptatiecriteria

* \[ ] Multi-symbol demo paper-session werkt zonder internet.
* \[ ] WebSocket/REST source degradeert veilig.
* \[ ] Portfolio report wordt geëxporteerd.
* \[ ] Live blijft onmogelijk.
* \[ ] Tests gebruiken fake data sources.

\---

## 8\. Fase 4 - Testnet endurance suite

Doel: testnet orderflow langer valideren zonder live risico.

### Nieuwe commands

```powershell
python -m binance\_spot\_bot.cli testnet-endurance --symbol BTCUSDT --duration-minutes 240 --max-orders 10 --confirm TESTNET\_ENDURANCE
python -m binance\_spot\_bot.cli testnet-reconcile-report --session-id <id>
```

### Taken

* \[ ] Endurance policy toevoegen:

  * \[ ] max duration;
  * \[ ] max orders;
  * \[ ] max quote per order;
  * \[ ] max unresolved orders;
  * \[ ] max reconnects;
  * \[ ] max rate-limit warnings.
* \[ ] Testnet orders:

  * \[ ] place small order;
  * \[ ] query order;
  * \[ ] cancel if open;
  * \[ ] reconcile lifecycle.
* \[ ] User-data stream monitor:

  * \[ ] executionReport latency;
  * \[ ] missed reports;
  * \[ ] reconnect count;
  * \[ ] listenKey keepalive status.
* \[ ] Endurance report:

  * \[ ] orders placed;
  * \[ ] orders filled/canceled/rejected;
  * \[ ] unknown statuses;
  * \[ ] reconciliation success rate;
  * \[ ] API errors;
  * \[ ] rate-limit events.

### Acceptatiecriteria

* \[ ] Testnet endurance kan meerdere uren draaien met hard limits.
* \[ ] Geen live URL mogelijk.
* \[ ] Geen unresolved order blijft verborgen.
* \[ ] Cancel/reconcile werkt aantoonbaar.
* \[ ] Endurance report is downloadbaar.

\---

## 9\. Fase 5 - Research maturity op basis van sessieresultaten

Doel: strategie-ontwikkeling baseren op echte logs en rapporten.

### Taken

* \[ ] Voeg `ResearchDatasetBuilder` toe:

  * \[ ] leest paper/testnet reports;
  * \[ ] maakt research table;
  * \[ ] koppelt signals aan outcomes;
  * \[ ] koppelt block reasons aan performance.
* \[ ] Analyseer per symbol:

  * \[ ] PnL;
  * \[ ] drawdown;
  * \[ ] fees;
  * \[ ] slippage;
  * \[ ] spread;
  * \[ ] data quality;
  * \[ ] signal confidence;
  * \[ ] risk blocks.
* \[ ] Maak `research\_summary.md`.
* \[ ] Dashboard Research tab:

  * \[ ] session comparison;
  * \[ ] symbol comparison;
  * \[ ] model comparison;
  * \[ ] block reason analysis.

### Acceptatiecriteria

* \[ ] Nieuwe strategieën worden niet blind toegevoegd.
* \[ ] Research gebruikt session reports als bron.
* \[ ] Slechte symbols/models worden zichtbaar.
* \[ ] Tests dekken report ingestion.

\---

## 10\. Fase 6 - MLOps verdieping

Doel: modeltraining en modelselectie sterker maken na Roadmap 005.

### Taken

* \[ ] Voeg experiment tracking toe:

  * \[ ] local JSONL;
  * \[ ] optioneel MLflow.
* \[ ] Voeg model comparison toe:

  * \[ ] baseline vs candidate;
  * \[ ] champion vs new candidate;
  * \[ ] per-symbol performance;
  * \[ ] per-regime performance.
* \[ ] Voeg drift over meerdere sessies toe:

  * \[ ] feature drift;
  * \[ ] confidence drift;
  * \[ ] signal distribution drift;
  * \[ ] performance drift.
* \[ ] Voeg auto-rejection toe:

  * \[ ] model wordt rejected bij slechte paper performance;
  * \[ ] champion blijft actief tot candidate bewezen beter is.
* \[ ] Dashboard ModelOps:

  * \[ ] experiment list;
  * \[ ] model lineage;
  * \[ ] promotion history;
  * \[ ] rejection reason.

### Acceptatiecriteria

* \[ ] Geen modelpromotie zonder out-of-sample en paper bewijs.
* \[ ] Drift is zichtbaar over meerdere sessies.
* \[ ] Model lineage is traceerbaar.
* \[ ] MLflow blijft optioneel, niet verplicht voor demo.

\---

## 11\. Fase 7 - External alert delivery

Doel: alerts buiten het dashboard kunnen ontvangen.

### Kanalen

* \[ ] Windows toast notification.
* \[ ] Telegram webhook.
* \[ ] Discord webhook.
* \[ ] Email summary.
* \[ ] Local sound/desktop notification.

### Taken

* \[ ] Voeg `AlertSink` interface toe.
* \[ ] Voeg sinks toe:

  * \[ ] console;
  * \[ ] local file;
  * \[ ] Windows toast;
  * \[ ] webhook.
* \[ ] Redaction verplicht op alle alert payloads.
* \[ ] Dashboard settings voor alert channels.
* \[ ] Test alert button.
* \[ ] Rate-limit alert spam.

### Acceptatiecriteria

* \[ ] Critical alerts komen buiten dashboard aan.
* \[ ] Alerts bevatten geen secrets.
* \[ ] Webhooks zijn optioneel.
* \[ ] Misconfigured webhook breekt runtime niet.
* \[ ] Tests mocken alert delivery.

\---

## 12\. Fase 8 - Live-readiness audit voorbereiding zonder live trading

Doel: bewijs verzamelen voor een latere aparte live-readiness roadmap.

### Taken

* \[ ] Maak `docs/live-readiness-audit-prep.md`.
* \[ ] Verzamel bewijs:

  * \[ ] paper sessions;
  * \[ ] testnet endurance;
  * \[ ] reconciliation success;
  * \[ ] max drawdown;
  * \[ ] incident drills;
  * \[ ] security scans;
  * \[ ] model promotion history;
  * \[ ] risk policy.
* \[ ] Maak checklist:

  * \[ ] secrets veilig;
  * \[ ] withdrawal permissions uit;
  * \[ ] IP allowlist;
  * \[ ] kill switch getest;
  * \[ ] max loss getest;
  * \[ ] order reconcile getest;
  * \[ ] alerts getest.
* \[ ] Geen live implementatie in deze roadmap.

### Acceptatiecriteria

* \[ ] Audit prep document bestaat.
* \[ ] Er is een bewijsmap met reports.
* \[ ] Live trading blijft disabled.
* \[ ] Volgende roadmap kan beslissen of live-readiness audit zinvol is.

\---

## 13\. Documentatie

Nieuwe docs:

* \[ ] `docs/portfolio-paper-trading.md`
* \[ ] `docs/portfolio-risk.md`
* \[ ] `docs/testnet-endurance.md`
* \[ ] `docs/research-from-session-reports.md`
* \[ ] `docs/modelops-lineage.md`
* \[ ] `docs/external-alerts.md`
* \[ ] `docs/live-readiness-audit-prep.md`

README updates:

* \[ ] portfolio paper command;
* \[ ] testnet endurance command;
* \[ ] research summary command;
* \[ ] alert settings;
* \[ ] safety statement.

\---

## 14\. Testplan

### Unit tests

* \[ ] `tests/test\_portfolio.py`
* \[ ] `tests/test\_portfolio\_risk.py`
* \[ ] `tests/test\_portfolio\_paper\_runtime.py`
* \[ ] `tests/test\_testnet\_endurance.py`
* \[ ] `tests/test\_research\_dataset\_builder.py`
* \[ ] `tests/test\_modelops\_lineage.py`
* \[ ] `tests/test\_alert\_sinks.py`
* \[ ] `tests/test\_live\_readiness\_audit\_prep.py`

### Integration tests

* \[ ] Multi-symbol demo paper session.
* \[ ] Portfolio risk block.
* \[ ] Testnet endurance blocked without credentials.
* \[ ] Alert delivery mock.
* \[ ] Session report ingestion.
* \[ ] Model auto-rejection.

### Security tests

* \[ ] No secrets in reports.
* \[ ] No secrets in alerts.
* \[ ] No live mode in dashboard.
* \[ ] Live URL blocked in testnet endurance.

\---

## 15\. Definition of Done

Roadmap 006 is klaar als:

* \[ ] Portfolio state werkt voor meerdere symbols.
* \[ ] Portfolio risk werkt bovenop bestaande RiskEngine.
* \[ ] Multi-symbol paper-session werkt in demo mode.
* \[ ] Testnet endurance suite is guarded en live-hard-blocked.
* \[ ] Research summaries worden gemaakt uit session reports.
* \[ ] MLOps lineage en model comparison werken.
* \[ ] External alerts werken zonder secret leakage.
* \[ ] Live-readiness audit prep bestaat zonder live trading te activeren.
* \[ ] Alle tests slagen.
* \[ ] Security scan is groen.
* \[ ] README en docs zijn bijgewerkt.
* \[ ] Roadmap 006 kan na uitvoering naar `Voltooid docs`.

\---

## 16\. Verwachte Roadmap 007 daarna

Alleen plannen na Roadmap 006 resultaten:

* \[ ] Echte live-readiness audit roadmap.
* \[ ] Productie-deploy research.
* \[ ] Multi-day testnet operations.
* \[ ] Advanced portfolio optimization.
* \[ ] Optional cloud monitoring.
* \[ ] Nog steeds geen live default.

