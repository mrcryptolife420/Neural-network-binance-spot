# Roadmap 079 - Paper Portfolio Operations, Capital Allocation \& Strategy Rotation

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/079-roadmap-paper-portfolio-operations-capital-allocation-strategy-rotation.md
```

Volgt op:

* `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
* `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
* `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
* `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
* `Voltooid docs/005` t/m `Voltooid docs/075`
* `Roadmap docs/076-roadmap-binance-public-data-ingestion-indicator-warmup-feature-expansion.md`
* `Roadmap docs/077-roadmap-data-driven-strategy-confidence-backtest-dataset-builder-indicator-calibration.md`
* `Roadmap docs/078-roadmap-paper-strategy-deployment-continuous-evaluation-auto-rollback.md`

Doel: Roadmap 078 maakt één paper-approved strategy deployment controleerbaar, met continuous evaluation, drift detection, watchdog, auto-rollback en daily reports. Roadmap 079 breidt dit uit naar **meerdere paper-approved strategies tegelijk** in één paper portfolio. De bot moet paper capital kunnen verdelen, conflicts tussen strategies oplossen, strategy rotation toepassen, portfolio-level risk bewaken en evidence produceren over welke strategy/symbol/allocatie beter werkt.

Live trading blijft volledig buiten scope.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] `Voltooid docs/075-roadmap-simple-demo-multi-symbol-final-validation.md` bestaat.
* \[x] Roadmap 075 heeft status `Voltooid`.
* \[x] Roadmap 075 bevestigt:

  * multi-symbol dashboard helpers;
  * symbol validation guardrails;
  * total demo quote budget;
  * risk summary;
  * budget allocation;
  * evidence export;
  * full pytest;
  * check-all;
  * browser smoke;
  * live trading disabled.
* \[x] Geen bestaande Roadmap 079 gevonden via repo-search.
* \[x] Roadmap 076 is lokaal aangemaakt voor Binance public data ingestion.
* \[x] Roadmap 077 is lokaal aangemaakt voor strategy confidence/backtest/calibration.
* \[x] Roadmap 078 is lokaal aangemaakt voor paper deployment/continuous evaluation/rollback.

### Codebasecontrole

Gecontroleerde relevante modules:

* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/model\_registry.py`
* \[x] `src/binance\_spot\_bot/portfolio.py`
* \[x] `src/binance\_spot\_bot/portfolio\_risk.py`

### Bestaande basis

Er bestaat al:

* \[x] `Portfolio` met balances, positions, buy/sell accounting, fees, realized PnL, total equity en total exposure.
* \[x] `PortfolioRiskEngine` met max total exposure, max open positions, max daily loss en per-symbol cooldown.
* \[x] `BotRuntime` met paper runtime, session store, model registry, risk engine, paper account, alerts, reports, demo pilot en no-live UI modes.
* \[x] Multi-symbol demo helpers en budget allocation zijn in Roadmap 075 gevalideerd.
* \[x] Roadmap 078 introduceert paper deployment plan/store/watchdog/rollback voor één strategy.

### Belangrijkste gat na Roadmap 078

Na Roadmap 078 kun je één paper-approved strategy veilig deployen en terugrollen. Wat dan nog mist:

* \[ ] meerdere paper-approved strategies tegelijk volgen;
* \[ ] paper capital verdelen over strategies;
* \[ ] strategy-level en portfolio-level exposure combineren;
* \[ ] strategy rotation op basis van evidence;
* \[ ] conflict handling als meerdere strategies hetzelfde symbol willen traden;
* \[ ] portfolio-level paper watchdog;
* \[ ] allocation drift monitoring;
* \[ ] daily portfolio report;
* \[ ] strategy attribution;
* \[ ] portfolio evidence bundle.

\---

## 1\. Hoofddoel Roadmap 079

Maak van losse paper deployments een **paper portfolio operating system**:

```text
Paper-approved strategies
→ portfolio allocation plan
→ conflict resolution
→ paper portfolio execution
→ strategy attribution
→ portfolio watchdog
→ strategy rotation
→ portfolio daily report
→ evidence-based allocation updates
```

Na Roadmap 079 moet de bot:

* \[ ] meerdere paper strategies tegelijk kunnen volgen;
* \[ ] total paper quote budget verdelen over strategies en symbols;
* \[ ] strategy conflicts detecteren;
* \[ ] portfolio-wide max loss/drawdown/exposure bewaken;
* \[ ] capital allocation automatisch of semi-automatisch herwegen;
* \[ ] underperforming strategies paper-only demoten of pauzeren;
* \[ ] winners niet onbeperkt opschalen zonder guardrails;
* \[ ] daily portfolio evidence rapporteren;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe paper runtime vanaf nul.
* \[ ] Geen nieuwe StrategyDeployment basis; Roadmap 078 doet deployment.
* \[ ] Geen nieuwe portfolio class vanaf nul; bestaande `Portfolio` uitbreiden.
* \[ ] Geen nieuwe RiskEngine vanaf nul.
* \[ ] Geen live trading.
* \[ ] Geen signed order endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen futures/margin/leverage.
* \[ ] Geen autonomous AI trader.
* \[ ] Geen real-money capital allocation.

Wel doen:

* \[ ] bestaande portfolio uitbreiden naar strategy-aware portfolio;
* \[ ] bestaande deployment store gebruiken als input;
* \[ ] bestaande paper watchdog uitbreiden naar portfolio watchdog;
* \[ ] bestaande daily reports uitbreiden naar portfolio reports;
* \[ ] bestaande dashboard multi-symbol budget UX gebruiken en verdiepen;
* \[ ] alles paper/demo-only houden.

\---

## 3\. Fase 0 - Paper Portfolio Safety Contract

Doel: vastleggen dat portfolio operations paper-only blijven.

### Nieuwe doc

```text
docs/paper-portfolio-operations-safety-contract.md
```

### Regels

* \[ ] Portfolio operations mogen alleen:

  * demo;
  * paper;
  * research;
  * testnet-readiness voor checks zonder deployment.
* \[ ] Live mode verboden.
* \[ ] Signed endpoints verboden.
* \[ ] Real account balance verboden.
* \[ ] Withdrawals/margin/futures verboden.
* \[ ] Allocatie is alleen paper capital.
* \[ ] Rotation mag alleen paper strategies pauzeren/activeren.
* \[ ] Watchdog mag risico verlagen of stoppen, nooit verhogen buiten limieten.
* \[ ] Reports zijn secret-free.

### Acceptatiecriteria

* \[ ] Safety contract staat in docs.
* \[ ] Tests bewijzen dat portfolio operations geen live mode accepteren.
* \[ ] Dashboard toont `PAPER PORTFOLIO ONLY`.
* \[ ] Geen order/account endpoint wordt gebruikt.

\---

## 4\. Fase 1 - Strategy-aware Portfolio V2

Doel: bestaande `Portfolio` uitbreiden zodat positions en PnL per strategy traceerbaar zijn.

### Uitbreiding `portfolio.py`

Nieuwe types:

* \[ ] `StrategyPosition`
* \[ ] `StrategyAllocation`
* \[ ] `PortfolioLedgerEventV2`
* \[ ] `StrategyAttribution`
* \[ ] `PortfolioSnapshotV2`

### Nieuwe velden

Per position:

* \[ ] symbol;
* \[ ] strategy\_id;
* \[ ] deployment\_id;
* \[ ] quantity;
* \[ ] average\_entry;
* \[ ] realized\_pnl;
* \[ ] unrealized\_pnl;
* \[ ] fees\_paid;
* \[ ] slippage\_paid;
* \[ ] opened\_at;
* \[ ] last\_updated\_at.

Per portfolio:

* \[ ] total quote balance;
* \[ ] reserved quote by strategy;
* \[ ] available quote;
* \[ ] strategy allocations;
* \[ ] symbol exposures;
* \[ ] strategy exposures;
* \[ ] portfolio high-watermark;
* \[ ] portfolio drawdown;
* \[ ] portfolio realized/unrealized pnl.

### Acceptatiecriteria

* \[ ] Portfolio kan PnL per strategy tonen.
* \[ ] Portfolio kan exposure per strategy tonen.
* \[ ] Portfolio kan exposure per symbol tonen.
* \[ ] Bestaande single-strategy portfolio tests blijven werken.
* \[ ] Geen secrets in snapshots.

\---

## 5\. Fase 2 - Portfolio Allocation Plan

Doel: paper capital bewust verdelen.

### Nieuwe module

```text
src/binance\_spot\_bot/portfolio\_allocation.py
```

### Dataclasses

* \[ ] `PortfolioAllocationPlan`
* \[ ] `StrategyAllocationTarget`
* \[ ] `SymbolAllocationTarget`
* \[ ] `AllocationDecision`
* \[ ] `AllocationDriftReport`

### Allocatie-instellingen

* \[ ] total paper quote budget;
* \[ ] max quote per strategy;
* \[ ] min quote per strategy;
* \[ ] max quote per symbol;
* \[ ] max total exposure;
* \[ ] reserve cash percentage;
* \[ ] rebalance threshold;
* \[ ] max allocation change per day;
* \[ ] max strategy count;
* \[ ] max correlated exposure.

### Allocation modes

* \[ ] equal weight;
* \[ ] confidence weighted;
* \[ ] risk adjusted;
* \[ ] performance weighted;
* \[ ] conservative fixed budget;
* \[ ] manual operator weights.

### Acceptatiecriteria

* \[ ] Allocation plan is serializable.
* \[ ] Plan werkt met meerdere strategies en symbols.
* \[ ] Plan kan geen live/real capital bevatten.
* \[ ] Plan weigert allocations boven total budget.
* \[ ] Dashboard kan plan tonen.

\---

## 6\. Fase 3 - Strategy Conflict Resolver

Doel: voorkomen dat meerdere strategies elkaar tegenwerken.

### Nieuwe module

```text
src/binance\_spot\_bot/strategy\_conflict\_resolver.py
```

### Conflicttypes

* \[ ] Strategy A wil BUY BTCUSDT, Strategy B wil SELL BTCUSDT.
* \[ ] Meerdere strategies willen dezelfde quote budget gebruiken.
* \[ ] Symbol exposure limiet wordt overschreden.
* \[ ] Portfolio risk blokkeert nieuwe entries.
* \[ ] Strategy wil entry terwijl portfolio in reduce-only staat.
* \[ ] Strategy confidence is lager dan andere kandidaat.
* \[ ] Data quality/liquidity verschilt per strategy/symbol.

### Resolve policies

* \[ ] highest adjusted confidence wins;
* \[ ] paper-approved priority;
* \[ ] risk-adjusted expected value;
* \[ ] reduce-only always allowed;
* \[ ] conservative tie-breaker;
* \[ ] no-trade if conflict unresolved.

### Output

* \[ ] `ConflictResolutionDecision`
* \[ ] winner strategy;
* \[ ] blocked strategies;
* \[ ] reason codes;
* \[ ] portfolio impact;
* \[ ] evidence links.

### Acceptatiecriteria

* \[ ] Tegengestelde signalen op zelfde symbol worden niet blind allebei uitgevoerd.
* \[ ] Conflict reason is dashboard-ready.
* \[ ] No-trade is default bij onduidelijk conflict.
* \[ ] Reduce-only exit blijft mogelijk.
* \[ ] Geen signed endpoint.

\---

## 7\. Fase 4 - Portfolio RiskEngine V3

Doel: portfolio-level risk voor meerdere strategies.

### Uitbreiding `portfolio\_risk.py`

Nieuwe limits:

* \[ ] max\_total\_portfolio\_exposure;
* \[ ] max\_symbol\_exposure;
* \[ ] max\_strategy\_exposure;
* \[ ] max\_strategy\_daily\_loss;
* \[ ] max\_portfolio\_daily\_loss;
* \[ ] max\_portfolio\_drawdown;
* \[ ] max\_strategy\_drawdown;
* \[ ] max\_correlation\_cluster\_exposure;
* \[ ] max\_open\_positions\_total;
* \[ ] max\_open\_positions\_per\_strategy;
* \[ ] max\_trades\_per\_strategy;
* \[ ] max\_trades\_portfolio;
* \[ ] max\_allocation\_drift;
* \[ ] minimum\_cash\_reserve.

Nieuwe decision:

* \[ ] `PortfolioRiskDecisionV3`
* \[ ] allowed;
* \[ ] reduce\_only\_allowed;
* \[ ] severity;
* \[ ] reason;
* \[ ] strategy\_id;
* \[ ] symbol;
* \[ ] current exposure;
* \[ ] projected exposure;
* \[ ] limit;
* \[ ] recommended action.

### Acceptatiecriteria

* \[ ] Portfolio risk kan strategy entry blokkeren.
* \[ ] Reduce-only exit blijft toegestaan.
* \[ ] Strategy-level loss blokkeert alleen die strategy waar mogelijk.
* \[ ] Portfolio-level critical blokkeert alle nieuwe entries.
* \[ ] Decision is report-ready.

\---

## 8\. Fase 5 - Paper Portfolio Orchestrator

Doel: meerdere strategy deployments samen laten draaien in paper mode.

### Nieuwe module

```text
src/binance\_spot\_bot/paper\_portfolio\_orchestrator.py
```

### Taken

* \[ ] Laad actieve paper deployments uit Roadmap 078.
* \[ ] Laad allocation plan.
* \[ ] Per tick/symbol:

  * verzamel strategy signals;
  * pas strategy confidence toe;
  * controleer data quality;
  * controleer liquidity;
  * resolve conflicts;
  * controleer portfolio risk;
  * simuleer paper fill;
  * update strategy-aware portfolio.
* \[ ] Events schrijven naar deployment stores en portfolio store.
* \[ ] Alerts sturen naar portfolio watchdog.
* \[ ] Session/report integratie.

### Acceptatiecriteria

* \[ ] Orchestrator werkt met fake strategies.
* \[ ] Orchestrator werkt zonder Binance keys.
* \[ ] Orchestrator stuurt geen live orders.
* \[ ] Orchestrator kan 2-5 paper strategies simuleren.
* \[ ] Conflicts en blocks zijn zichtbaar.

\---

## 9\. Fase 6 - Portfolio Deployment Store

Doel: portfolio operations persistent maken.

### Nieuwe module

```text
src/binance\_spot\_bot/portfolio\_deployment\_store.py
```

### Storage

```text
data/portfolio-deployments/
  portfolio-index.json
  <portfolio\_deployment\_id>/
    allocation-plan.json
    active-strategies.json
    portfolio-events.jsonl
    portfolio-snapshots.jsonl
    conflict-decisions.jsonl
    risk-decisions.jsonl
    rotation-decisions.jsonl
    daily-reports/
```

### Acceptatiecriteria

* \[ ] Store kan portfolio deployment opslaan/laden.
* \[ ] Events zijn append-only.
* \[ ] Active strategies zijn traceerbaar.
* \[ ] Geen secrets.
* \[ ] Bundle export met manifest/hash.

\---

## 10\. Fase 7 - Portfolio-level Continuous Evaluation

Doel: portfolio als geheel evalueren, niet alleen losse strategies.

### Nieuwe module

```text
src/binance\_spot\_bot/portfolio\_continuous\_evaluation.py
```

### Metrics

* \[ ] portfolio equity;
* \[ ] portfolio PnL;
* \[ ] realized/unrealized PnL;
* \[ ] max drawdown;
* \[ ] exposure by symbol;
* \[ ] exposure by strategy;
* \[ ] diversification score;
* \[ ] strategy contribution;
* \[ ] symbol contribution;
* \[ ] conflict rate;
* \[ ] block rate;
* \[ ] allocation drift;
* \[ ] cash reserve;
* \[ ] risk-adjusted return;
* \[ ] turnover;
* \[ ] fees/slippage;
* \[ ] data quality warnings by strategy/symbol.

### Acceptatiecriteria

* \[ ] Portfolio metrics worden periodiek berekend.
* \[ ] Strategy attribution is zichtbaar.
* \[ ] Conflicts/blocks tellen mee.
* \[ ] Evaluation gebruikt geen order endpoints.
* \[ ] Metrics zijn dashboard-ready.

\---

## 11\. Fase 8 - Portfolio Watchdog

Doel: portfolio paper operations beschermen.

### Nieuwe module

```text
src/binance\_spot\_bot/portfolio\_watchdog.py
```

### Checks

* \[ ] portfolio max drawdown;
* \[ ] portfolio daily loss;
* \[ ] strategy daily loss;
* \[ ] symbol exposure limit;
* \[ ] strategy exposure limit;
* \[ ] allocation drift;
* \[ ] too many conflicts;
* \[ ] too many blocked trades;
* \[ ] data quality degraded across portfolio;
* \[ ] liquidity degraded;
* \[ ] repeated strategy rollbacks;
* \[ ] missing daily report;
* \[ ] evidence integrity failure.

### Actions

* \[ ] observe;
* \[ ] warn;
* \[ ] reduce strategy allocation;
* \[ ] freeze new entries;
* \[ ] switch strategy to observe-only;
* \[ ] rotate out underperformer;
* \[ ] stop portfolio deployment.

### Acceptatiecriteria

* \[ ] Watchdog never increases risk.
* \[ ] Watchdog actions are paper-only.
* \[ ] Actions are evidence-linked.
* \[ ] Dashboard shows current watchdog status.
* \[ ] Tests cover critical actions.

\---

## 12\. Fase 9 - Strategy Rotation Engine

Doel: underperforming strategies pauzeren en betere paper candidates activeren.

### Nieuwe module

```text
src/binance\_spot\_bot/strategy\_rotation.py
```

### Rotation inputs

* \[ ] paper performance;
* \[ ] backtest expectation;
* \[ ] confidence calibration;
* \[ ] drift status;
* \[ ] daily report score;
* \[ ] drawdown;
* \[ ] data quality by strategy;
* \[ ] liquidity suitability;
* \[ ] correlation with active strategies;
* \[ ] operator constraints.

### Rotation actions

* \[ ] keep;
* \[ ] watch;
* \[ ] reduce allocation;
* \[ ] increase allocation within cap;
* \[ ] pause strategy;
* \[ ] replace with candidate;
* \[ ] move to observe-only.

### Guardrails

* \[ ] no rotation without minimum sample count;
* \[ ] max allocation increase per day;
* \[ ] no activation without paper-approved status;
* \[ ] no live mode;
* \[ ] operator confirmation for replacement unless auto policy explicitly allows paper-only replace.

### Acceptatiecriteria

* \[ ] Rotation is evidence-based.
* \[ ] Strategy replacement never enables live.
* \[ ] Allocation increases are capped.
* \[ ] Underperformers can be paused.
* \[ ] Dashboard shows rotation reason.

\---

## 13\. Fase 10 - Capital Rebalancer

Doel: paper capital allocations periodiek corrigeren.

### Nieuwe module

```text
src/binance\_spot\_bot/capital\_rebalancer.py
```

### Rebalance types

* \[ ] scheduled rebalance;
* \[ ] drift-triggered rebalance;
* \[ ] risk-triggered rebalance;
* \[ ] manual rebalance;
* \[ ] stop-loss rebalance.

### Rebalance constraints

* \[ ] preserve cash reserve;
* \[ ] max allocation change;
* \[ ] no increase for strategy in watch/suspended;
* \[ ] reduce-only during critical portfolio risk;
* \[ ] avoid overtrading;
* \[ ] avoid tiny dust allocations.

### Acceptatiecriteria

* \[ ] Rebalancer outputs plan, not hidden action.
* \[ ] Apply requires paper-only confirmation unless auto-reduce.
* \[ ] Auto-reduce is allowed, auto-risk-increase is not.
* \[ ] Rebalance decisions are logged.

\---

## 14\. Fase 11 - Cross-strategy Attribution Report

Doel: begrijpen welke strategy/symbol het portfolio resultaat veroorzaakt.

### Nieuwe module

```text
src/binance\_spot\_bot/portfolio\_attribution.py
```

### Attribution

* \[ ] PnL by strategy;
* \[ ] PnL by symbol;
* \[ ] drawdown by strategy;
* \[ ] drawdown by symbol;
* \[ ] fees by strategy;
* \[ ] slippage by strategy;
* \[ ] blocked trades by strategy;
* \[ ] conflicts by strategy;
* \[ ] contribution to volatility;
* \[ ] contribution to portfolio risk.

### Acceptatiecriteria

* \[ ] Daily portfolio report bevat attribution.
* \[ ] Dashboard kan top/bottom strategy tonen.
* \[ ] Strategy demotion kan attribution gebruiken.
* \[ ] Evidence export bevat attribution.

\---

## 15\. Fase 12 - Daily Portfolio Report

Doel: dagelijks bewijs over het totale paper portfolio.

### Nieuwe module

```text
src/binance\_spot\_bot/daily\_portfolio\_report.py
```

### Output

```text
data/portfolio-deployments/<id>/daily-reports/YYYY-MM-DD/
  daily\_portfolio\_report.md
  daily\_portfolio\_report.json
  portfolio\_metrics.csv
  strategy\_attribution.csv
  symbol\_attribution.csv
  conflict\_decisions.jsonl
  rotation\_decisions.jsonl
  allocation\_changes.jsonl
  evidence\_manifest.json
```

### Report bevat

* \[ ] portfolio summary;
* \[ ] active strategies;
* \[ ] allocation table;
* \[ ] PnL/drawdown;
* \[ ] exposure;
* \[ ] strategy attribution;
* \[ ] symbol attribution;
* \[ ] conflicts;
* \[ ] watchdog actions;
* \[ ] rotation decisions;
* \[ ] risk blockers;
* \[ ] next recommended action;
* \[ ] no-live statement.

### Acceptatiecriteria

* \[ ] Report is secret-free.
* \[ ] Report is evidence-linked.
* \[ ] Dashboard can download report.
* \[ ] Report can support rotation/demotion decisions.

\---

## 16\. Fase 13 - Portfolio Dashboard Panel

Doel: operator kan paper portfolio beheren zonder raw JSON.

### Nieuwe/uitgebreide dashboardsectie

```text
Paper Portfolio Operations
```

### Panels

* \[ ] portfolio deployment status;
* \[ ] paper-only badge;
* \[ ] total paper budget;
* \[ ] cash reserve;
* \[ ] active strategies;
* \[ ] strategy allocations;
* \[ ] symbol exposure;
* \[ ] portfolio risk status;
* \[ ] watchdog status;
* \[ ] conflict timeline;
* \[ ] rotation recommendations;
* \[ ] daily report status;
* \[ ] attribution table;
* \[ ] next action.

### Actions

* \[ ] create portfolio allocation plan;
* \[ ] start paper portfolio;
* \[ ] pause strategy;
* \[ ] stop strategy;
* \[ ] rebalance paper capital;
* \[ ] rotate strategy;
* \[ ] export portfolio report;
* \[ ] export evidence bundle.

### Acceptatiecriteria

* \[ ] Dashboard never shows live portfolio mode.
* \[ ] Dangerous paper actions require confirmation.
* \[ ] Critical blockers are visible.
* \[ ] Raw JSON only in debug expanders.
* \[ ] Browser smoke covers panel.

\---

## 17\. Fase 14 - Portfolio Evidence Bundle

Doel: één bundel voor alle portfolio-operations evidence.

### Bundle bevat

* \[ ] allocation plan;
* \[ ] active strategies;
* \[ ] strategy deployment evidence;
* \[ ] portfolio snapshots;
* \[ ] risk decisions;
* \[ ] conflict decisions;
* \[ ] watchdog events;
* \[ ] rotation decisions;
* \[ ] capital rebalance decisions;
* \[ ] daily reports;
* \[ ] attribution reports;
* \[ ] check-all output;
* \[ ] no-live proof;
* \[ ] hashes.

### Acceptatiecriteria

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest.
* \[ ] Bundle can be verified.
* \[ ] Bundle can be archived.
* \[ ] Dashboard/CLI export works.

\---

## 18\. Fase 15 - Portfolio Simulation Suite

Doel: portfolio allocation/rotation testen vóór echte paper runs.

### Nieuwe module

```text
src/binance\_spot\_bot/portfolio\_simulation.py
```

### Scenarios

* \[ ] two strategies same symbol same direction;
* \[ ] two strategies same symbol opposite direction;
* \[ ] one strategy underperforms;
* \[ ] portfolio drawdown breach;
* \[ ] allocation drift;
* \[ ] liquidity degradation;
* \[ ] correlation cluster overexposure;
* \[ ] high conflict rate;
* \[ ] repeated strategy rollback;
* \[ ] missing data for one strategy.

### Acceptatiecriteria

* \[ ] Simulation runs offline.
* \[ ] Critical scenarios trigger expected watchdog actions.
* \[ ] Rotation decisions are deterministic.
* \[ ] No live mode.
* \[ ] CI-safe subset exists.

\---

## 19\. Fase 16 - CLI commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli portfolio-plan --strategies stratA,stratB --budget 1000 --mode paper
python -m binance\_spot\_bot.cli portfolio-start --portfolio-id <id> --confirm PAPER\_PORTFOLIO
python -m binance\_spot\_bot.cli portfolio-status --portfolio-id <id>
python -m binance\_spot\_bot.cli portfolio-rebalance --portfolio-id <id> --confirm PAPER\_REBALANCE
python -m binance\_spot\_bot.cli portfolio-rotate --portfolio-id <id> --confirm PAPER\_ROTATE
python -m binance\_spot\_bot.cli portfolio-stop --portfolio-id <id> --reason operator\_stop
python -m binance\_spot\_bot.cli portfolio-report --portfolio-id <id>
python -m binance\_spot\_bot.cli portfolio-export-evidence --portfolio-id <id>
```

### Acceptatiecriteria

* \[ ] Commands work without API keys.
* \[ ] Commands accept JSON output.
* \[ ] Commands cannot use live mode.
* \[ ] Confirm required for start/rebalance/rotate.
* \[ ] Reports are secret-free.

\---

## 20\. Fase 17 - Tests

### Unit tests

* \[ ] `tests/test\_strategy\_aware\_portfolio.py`
* \[ ] `tests/test\_portfolio\_allocation.py`
* \[ ] `tests/test\_strategy\_conflict\_resolver.py`
* \[ ] `tests/test\_portfolio\_risk\_v3.py`
* \[ ] `tests/test\_paper\_portfolio\_orchestrator.py`
* \[ ] `tests/test\_portfolio\_deployment\_store.py`
* \[ ] `tests/test\_portfolio\_continuous\_evaluation.py`
* \[ ] `tests/test\_portfolio\_watchdog.py`
* \[ ] `tests/test\_strategy\_rotation.py`
* \[ ] `tests/test\_capital\_rebalancer.py`
* \[ ] `tests/test\_portfolio\_attribution.py`
* \[ ] `tests/test\_daily\_portfolio\_report.py`
* \[ ] `tests/test\_portfolio\_evidence\_bundle.py`
* \[ ] `tests/test\_portfolio\_simulation.py`

### Integration tests

* \[ ] Create portfolio plan with two paper-approved strategies.
* \[ ] Start fake paper portfolio deployment.
* \[ ] Resolve same-symbol conflict.
* \[ ] Trigger portfolio exposure block.
* \[ ] Trigger strategy-level loss block.
* \[ ] Run portfolio evaluation.
* \[ ] Trigger rotation recommendation.
* \[ ] Generate daily portfolio report.
* \[ ] Export evidence bundle.

### Safety tests

* \[ ] Portfolio rejects live mode.
* \[ ] Portfolio rejects real account endpoint.
* \[ ] Rebalancer cannot increase risk during critical state.
* \[ ] Rotation cannot activate non-paper-approved strategy.
* \[ ] Orchestrator cannot call signed endpoints.
* \[ ] Reports/evidence contain no secrets.
* \[ ] Live disabled remains true.

\---

## 21\. Docs

Nieuwe docs:

* \[ ] `docs/paper-portfolio-operations-safety-contract.md`
* \[ ] `docs/paper-portfolio-workflow.md`
* \[ ] `docs/portfolio-allocation-plan.md`
* \[ ] `docs/strategy-conflict-resolution.md`
* \[ ] `docs/portfolio-risk-v3.md`
* \[ ] `docs/paper-portfolio-orchestrator.md`
* \[ ] `docs/portfolio-watchdog.md`
* \[ ] `docs/strategy-rotation.md`
* \[ ] `docs/capital-rebalancer.md`
* \[ ] `docs/portfolio-attribution.md`
* \[ ] `docs/daily-portfolio-report.md`
* \[ ] `docs/portfolio-evidence-bundle.md`
* \[ ] `docs/portfolio-simulation-suite.md`

README updates:

* \[ ] paper portfolio commands;
* \[ ] safety note;
* \[ ] allocation explanation;
* \[ ] conflict resolution explanation;
* \[ ] no-live statement.

\---

## 22\. Codex bouwvolgorde

### PR 1 - Strategy-aware Portfolio V2

* \[ ] Extend existing portfolio types.
* \[ ] Add strategy attribution fields.
* \[ ] Add snapshots/ledger.
* \[ ] Tests.

### PR 2 - Portfolio Allocation Plan

* \[ ] Allocation dataclasses.
* \[ ] Equal/confidence/risk adjusted modes.
* \[ ] Budget validation.
* \[ ] Tests.

### PR 3 - Strategy Conflict Resolver

* \[ ] Conflict decision types.
* \[ ] Resolve policies.
* \[ ] Tests.

### PR 4 - Portfolio RiskEngine V3

* \[ ] New limits/decisions.
* \[ ] Reduce-only behavior.
* \[ ] Tests.

### PR 5 - Paper Portfolio Orchestrator

* \[ ] Multi-strategy paper orchestration.
* \[ ] Store integration.
* \[ ] Tests.

### PR 6 - Portfolio Store + CLI

* \[ ] Store.
* \[ ] CLI commands.
* \[ ] Confirm gates.
* \[ ] Tests.

### PR 7 - Portfolio Evaluation + Watchdog

* \[ ] Metrics.
* \[ ] Watchdog actions.
* \[ ] Tests.

### PR 8 - Strategy Rotation + Capital Rebalancer

* \[ ] Rotation engine.
* \[ ] Rebalancer.
* \[ ] Tests.

### PR 9 - Reports + Attribution + Evidence

* \[ ] Daily report.
* \[ ] Attribution.
* \[ ] Evidence bundle.
* \[ ] Tests.

### PR 10 - Dashboard + Simulation

* \[ ] Dashboard panel.
* \[ ] Simulation suite.
* \[ ] Browser smoke.
* \[ ] Docs.

\---

## 23\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 079 PR 1: Strategy-aware Portfolio V2.

Breid de bestaande src/binance\_spot\_bot/portfolio.py uit zonder een tweede portfolio systeem te maken.
Voeg strategy\_id en deployment\_id tracking toe aan positions/fills/ledger events.
Voeg StrategyPosition, StrategyAllocation, PortfolioLedgerEventV2, StrategyAttribution en PortfolioSnapshotV2 toe.
Zorg dat total equity, total exposure, realized/unrealized PnL, fees en drawdown per strategy en per symbol berekend kunnen worden.
Behoud backward compatibility met bestaande Portfolio.buy/sell waar mogelijk.
Voeg tests toe voor:
- twee strategies op verschillende symbols
- twee strategies op hetzelfde symbol
- PnL per strategy
- exposure per strategy
- fees per strategy
- total portfolio equity
- no secrets in snapshots

Geen live trading, geen signed endpoints, geen risk/execution refactor.
```

Waarom eerst:

* Strategy-aware portfolio is de fundering voor allocation, conflict resolution, portfolio risk en rotation.
* Het bouwt voort op bestaande `Portfolio`.
* Het raakt nog geen orderflow.
* Het is klein genoeg voor Codex met duidelijke tests.

\---

## 24\. Definition of Done

Roadmap 079 is klaar als:

* \[ ] Strategy-aware Portfolio V2 werkt.
* \[ ] Portfolio allocation plan werkt.
* \[ ] Strategy conflict resolver werkt.
* \[ ] Portfolio RiskEngine V3 werkt.
* \[ ] Paper Portfolio Orchestrator werkt.
* \[ ] Portfolio deployment store werkt.
* \[ ] Portfolio-level continuous evaluation werkt.
* \[ ] Portfolio watchdog werkt.
* \[ ] Strategy rotation werkt.
* \[ ] Capital rebalancer werkt.
* \[ ] Portfolio attribution report werkt.
* \[ ] Daily portfolio report werkt.
* \[ ] Portfolio dashboard panel werkt.
* \[ ] Portfolio evidence bundle werkt.
* \[ ] Portfolio simulation suite werkt.
* \[ ] CLI commands werken.
* \[ ] Tests bewijzen geen live/signed endpoints.
* \[ ] Reports/evidence zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 079 kan na uitvoering naar `Voltooid docs`.

\---

## 25\. Verwachte Roadmap 080 daarna

Na Roadmap 079 zou Roadmap 080 logisch focussen op:

```text
Roadmap 080 - Paper Portfolio Benchmarking, Stress Testing \& Scenario Replay
```

Mogelijke inhoud:

* \[ ] stress testing van portfolio allocations;
* \[ ] scenario replay over historische market regimes;
* \[ ] symbol correlation stress;
* \[ ] liquidity shock simulation;
* \[ ] multi-strategy drawdown analysis;
* \[ ] portfolio benchmark suite;
* \[ ] allocation robustness scoring;
* \[ ] nog steeds geen live trading.

