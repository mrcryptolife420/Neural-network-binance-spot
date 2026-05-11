# Roadmap 080 - Paper Portfolio Benchmarking, Stress Testing \& Scenario Replay

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Voltooid docs/080-roadmap-paper-portfolio-benchmarking-stress-testing-scenario-replay.md
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
* `Roadmap docs/079-roadmap-paper-portfolio-operations-capital-allocation-strategy-rotation.md`

Doel: Roadmap 079 maakt paper portfolio operations mogelijk: meerdere paper-approved strategies, capital allocation, conflict resolution, strategy rotation en portfolio watchdog. Roadmap 080 test of die paper portfolio-laag robuust blijft onder moeilijke marktomstandigheden via benchmarking, stress testing, scenario replay, liquidity shocks, correlation stress, allocation robustness en portfolio-level evidence reports.

Live trading blijft volledig buiten scope.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] `Voltooid docs/075-roadmap-simple-demo-multi-symbol-final-validation.md` bestaat.
* \[x] Roadmap 075 heeft status `Voltooid`.
* \[x] Roadmap 075 bevestigt:

  * multi-symbol dashboard helpers;
  * budget allocation;
  * risk summary;
  * evidence export;
  * full pytest;
  * check-all;
  * browser smoke;
  * live trading disabled.
* \[x] Geen bestaande Roadmap 080 gevonden via repo-search.
* \[x] Roadmap 076 is lokaal aangemaakt voor Binance public data ingestion.
* \[x] Roadmap 077 is lokaal aangemaakt voor backtest datasets en confidence calibration.
* \[x] Roadmap 078 is lokaal aangemaakt voor paper strategy deployment en auto rollback.
* \[x] Roadmap 079 is lokaal aangemaakt voor paper portfolio operations en strategy rotation.

### Codebasecontrole

Gecontroleerde relevante modules:

* \[x] `src/binance\_spot\_bot/backtest.py`
* \[x] `src/binance\_spot\_bot/evaluation.py`
* \[x] `src/binance\_spot\_bot/portfolio.py`
* \[x] `src/binance\_spot\_bot/portfolio\_risk.py`
* \[x] `src/binance\_spot\_bot/runtime.py`

### Bestaande basis

Er bestaat al:

* \[x] `BacktestEngine`;
* \[x] `BacktestResult`;
* \[x] walk-forward evaluation;
* \[x] rule baseline evaluation;
* \[x] `Portfolio`;
* \[x] `PortfolioRiskEngine`;
* \[x] multi-symbol helpervalidatie uit Roadmap 075;
* \[x] runtime/session/report infrastructuur;
* \[x] no-live UI modes.

### Belangrijkste gat na Roadmap 079

Na Roadmap 079 kan het paper portfolio meerdere strategies beheren en paper capital verdelen, maar dan moet je nog bewijzen:

* \[ ] hoe portfolio allocations presteren in bull/bear/range/high-volatility regimes;
* \[ ] hoe strategies reageren op liquidity shocks;
* \[ ] hoe allocation werkt bij symbol-correlation stress;
* \[ ] of rotation niet overfit of te vaak wisselt;
* \[ ] of watchdog/rollback snel genoeg reageert;
* \[ ] welke allocation policy het meest robuust is;
* \[ ] of paper portfolio results reproduceerbaar zijn;
* \[ ] of scenario replay dezelfde evidence geeft bij dezelfde inputs.

\---

## 1\. Hoofddoel Roadmap 080

Maak een portfolio benchmark- en stress-testlaag:

```text
Historical/cache data
→ scenario builder
→ portfolio replay
→ allocation benchmark
→ stress tests
→ robustness scoring
→ watchdog/rollback validation
→ evidence report
```

Na Roadmap 080 moet de bot:

* \[ ] paper portfolio allocations kunnen benchmarken;
* \[ ] scenario replay kunnen draaien op historische/cached public data;
* \[ ] stress tests kunnen draaien zonder live data;
* \[ ] liquidity shock en spread shock kunnen simuleren;
* \[ ] correlation stress tussen symbols kunnen meten;
* \[ ] strategy rotation robustness kunnen beoordelen;
* \[ ] portfolio watchdog/rollback decisions kunnen valideren;
* \[ ] reports/evidence kunnen exporteren;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe paper portfolio engine vanaf nul.
* \[ ] Geen nieuwe Binance data ingestion laag; Roadmap 076 doet dat.
* \[ ] Geen nieuwe backtest-engine vanaf nul.
* \[ ] Geen nieuwe deployment/rollback laag; Roadmap 078 doet dat.
* \[ ] Geen nieuwe portfolio allocation basis; Roadmap 079 doet dat.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen real-money portfolio.
* \[ ] Geen futures/margin/leverage.

Wel doen:

* \[ ] bestaande `BacktestEngine` uitbreiden met scenario/stress support;
* \[ ] bestaande evaluation gebruiken voor portfolio benchmarks;
* \[ ] bestaande portfolio/allocation/rotation modules uit Roadmap 079 testen;
* \[ ] bestaande public data cache uit Roadmap 076 gebruiken;
* \[ ] bestaande paper reports/evidence uitbreiden;
* \[ ] alles offline/reproduceerbaar maken.

\---

## 3\. Fase 0 - Benchmark Safety Contract

Doel: benchmark/stress/replay mag nooit execution of live endpoints triggeren.

### Nieuwe doc

```text
docs/paper-portfolio-benchmark-safety-contract.md
```

### Regels

* \[ ] Benchmarks gebruiken alleen:

  * cached public data;
  * demo generated data;
  * fixture data;
  * synthetic stress scenarios.
* \[ ] Geen signed endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen order endpoints.
* \[ ] Geen live mode.
* \[ ] Geen live base URL.
* \[ ] Geen strategy promotion naar live.
* \[ ] Stress tests mogen paper deployment alleen simuleren of in paper mode evalueren.
* \[ ] Reports bevatten no-live statement.

### Acceptatiecriteria

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen geen signed endpoint usage.
* \[ ] Benchmark CLI werkt zonder API keys.
* \[ ] Dashboard toont `BENCHMARK / PAPER ONLY`.

\---

## 4\. Fase 1 - Scenario Dataset Builder

Doel: scenario’s maken uit cached public Binance data en synthetic fixtures.

### Nieuwe module

```text
src/binance\_spot\_bot/scenario\_dataset\_builder.py
```

### Scenario types

* \[ ] bull trend;
* \[ ] bear trend;
* \[ ] sideways/range;
* \[ ] high volatility;
* \[ ] low volatility;
* \[ ] liquidity thin;
* \[ ] spread widening;
* \[ ] sudden dump;
* \[ ] sudden pump;
* \[ ] choppy fake breakout;
* \[ ] data gap;
* \[ ] stale data;
* \[ ] correlation spike;
* \[ ] symbol-specific shock.

### Inputs

* \[ ] Roadmap 076 public candle cache;
* \[ ] order book/liquidity cache;
* \[ ] 24h/rolling market context;
* \[ ] scenario filters;
* \[ ] date/time range;
* \[ ] symbols;
* \[ ] intervals.

### Output

```text
data/scenarios/<scenario\_id>/
  scenario\_manifest.json
  candles/
  liquidity/
  market\_context/
  scenario\_labels.json
  data\_quality.json
```

### Acceptatiecriteria

* \[ ] Scenario builder werkt offline.
* \[ ] Scenario manifest bevat hashes.
* \[ ] Scenario labels zijn reproduceerbaar.
* \[ ] Geen secrets.
* \[ ] Scenario kan door replay engine worden geladen.

\---

## 5\. Fase 2 - Synthetic Stress Scenario Generator

Doel: extreme omstandigheden testen die niet makkelijk in data voorkomen.

### Nieuwe module

```text
src/binance\_spot\_bot/stress\_scenario\_generator.py
```

### Stress transforms

* \[ ] price gap down;
* \[ ] price gap up;
* \[ ] volatility multiplier;
* \[ ] spread multiplier;
* \[ ] liquidity reduction;
* \[ ] volume collapse;
* \[ ] data staleness;
* \[ ] random missing candles;
* \[ ] burst volatility;
* \[ ] correlation increase across symbols;
* \[ ] slippage multiplier;
* \[ ] fee increase;
* \[ ] symbol halt simulation.

### Parameters

* \[ ] severity: low/medium/high/extreme;
* \[ ] start timestamp;
* \[ ] duration;
* \[ ] affected symbols;
* \[ ] affected feature groups;
* \[ ] seed.

### Acceptatiecriteria

* \[ ] Generator is deterministic with seed.
* \[ ] Output has manifest/hash.
* \[ ] Extreme scenario never calls external APIs.
* \[ ] Generated data stays valid enough for replay.
* \[ ] Tests cover every transform.

\---

## 6\. Fase 3 - Portfolio Scenario Replay Engine

Doel: paper portfolio door scenario’s heen replayen.

### Nieuwe module

```text
src/binance\_spot\_bot/portfolio\_scenario\_replay.py
```

### Replay inputs

* \[ ] scenario dataset;
* \[ ] portfolio allocation plan;
* \[ ] active paper strategies;
* \[ ] strategy runtime locks;
* \[ ] risk settings;
* \[ ] rotation policy;
* \[ ] watchdog policy;
* \[ ] starting paper capital.

### Replay outputs

* \[ ] portfolio equity curve;
* \[ ] strategy equity curves;
* \[ ] symbol exposure timeline;
* \[ ] allocation timeline;
* \[ ] trades/fills simulated;
* \[ ] risk blocks;
* \[ ] conflict decisions;
* \[ ] rotation decisions;
* \[ ] rollback decisions;
* \[ ] watchdog events;
* \[ ] final metrics.

### Acceptatiecriteria

* \[ ] Replay runs offline.
* \[ ] Same input + seed gives same output.
* \[ ] Replay never calls execution engine with live/signed mode.
* \[ ] Replay can simulate multiple strategies.
* \[ ] Replay report is exportable.

\---

## 7\. Fase 4 - Portfolio Benchmark Suite

Doel: allocation policies en strategies objectief vergelijken.

### Nieuwe module

```text
src/binance\_spot\_bot/portfolio\_benchmark.py
```

### Benchmark subjects

* \[ ] equal allocation;
* \[ ] confidence-weighted allocation;
* \[ ] risk-adjusted allocation;
* \[ ] performance-weighted allocation;
* \[ ] conservative cash-reserve allocation;
* \[ ] manual operator weights;
* \[ ] no-rotation baseline;
* \[ ] rotation-enabled policy;
* \[ ] no-trade baseline;
* \[ ] buy-and-hold per symbol baseline.

### Metrics

* \[ ] final equity;
* \[ ] net PnL;
* \[ ] max drawdown;
* \[ ] volatility;
* \[ ] profit factor;
* \[ ] exposure time;
* \[ ] turnover;
* \[ ] fees/slippage;
* \[ ] conflicts;
* \[ ] blocks;
* \[ ] rotations;
* \[ ] rollbacks;
* \[ ] robustness score.

### Acceptatiecriteria

* \[ ] Benchmark compares at least 3 allocation policies.
* \[ ] Benchmark includes no-trade/buy-hold baselines.
* \[ ] Results are ranked with risk-adjusted metrics.
* \[ ] Reports are secret-free.
* \[ ] No live trading.

\---

## 8\. Fase 5 - Allocation Robustness Score

Doel: niet alleen hoogste PnL kiezen, maar meest robuuste policy.

### Nieuwe module

```text
src/binance\_spot\_bot/allocation\_robustness.py
```

### Score components

* \[ ] return score;
* \[ ] drawdown penalty;
* \[ ] volatility penalty;
* \[ ] turnover penalty;
* \[ ] conflict penalty;
* \[ ] rotation churn penalty;
* \[ ] liquidity shock penalty;
* \[ ] correlation stress penalty;
* \[ ] data quality penalty;
* \[ ] consistency across scenarios.

### Output

* \[ ] robustness score 0-100;
* \[ ] grade:

  * A robust;
  * B acceptable;
  * C watch;
  * D weak;
  * F blocked;
* \[ ] reason codes;
* \[ ] recommended action.

### Acceptatiecriteria

* \[ ] High return with huge drawdown does not score A.
* \[ ] Policy must survive multiple scenarios to rank high.
* \[ ] Reason codes are dashboard-ready.
* \[ ] Score is deterministic.

\---

## 9\. Fase 6 - Liquidity Shock Testing

Doel: testen of portfolio niet kapotgaat bij slechtere spreads/liquidity.

### Nieuwe module

```text
src/binance\_spot\_bot/liquidity\_stress.py
```

### Shocks

* \[ ] spread x2;
* \[ ] spread x5;
* \[ ] spread x10;
* \[ ] depth -25%;
* \[ ] depth -50%;
* \[ ] depth -90%;
* \[ ] slippage x2;
* \[ ] slippage x5;
* \[ ] no fill / skipped fill;
* \[ ] partial fill simulation.

### Metrics

* \[ ] PnL impact;
* \[ ] drawdown impact;
* \[ ] fill failure rate;
* \[ ] skipped trade rate;
* \[ ] risk block rate;
* \[ ] strategy affected most;
* \[ ] symbol affected most.

### Acceptatiecriteria

* \[ ] Liquidity stress can block weak symbols.
* \[ ] Thin liquidity reduces robustness score.
* \[ ] Partial/no-fill simulation is paper-only.
* \[ ] No order endpoints.

\---

## 10\. Fase 7 - Correlation Stress Testing

Doel: testen of portfolio niet “gediversifieerd lijkt” maar alles tegelijk daalt.

### Nieuwe module

```text
src/binance\_spot\_bot/correlation\_stress.py
```

### Tests

* \[ ] correlation matrix from historical returns;
* \[ ] correlation spike scenario;
* \[ ] all crypto beta selloff;
* \[ ] BTC-led dump;
* \[ ] altcoin-only dump;
* \[ ] stable correlation breakdown;
* \[ ] cluster exposure check.

### Metrics

* \[ ] cluster exposure;
* \[ ] drawdown under correlation spike;
* \[ ] diversification score;
* \[ ] symbols causing concentration;
* \[ ] strategies causing concentration.

### Acceptatiecriteria

* \[ ] Portfolio can detect hidden concentration.
* \[ ] Correlation stress affects allocation robustness score.
* \[ ] Dashboard shows cluster risk.
* \[ ] No live data required.

\---

## 11\. Fase 8 - Rotation Churn Analysis

Doel: voorkomen dat strategy rotation te vaak wisselt en kosten/ruis veroorzaakt.

### Nieuwe module

```text
src/binance\_spot\_bot/rotation\_churn\_analysis.py
```

### Metrics

* \[ ] rotations per day;
* \[ ] average time in strategy;
* \[ ] allocation change count;
* \[ ] allocation change magnitude;
* \[ ] performance before/after rotation;
* \[ ] false positive rotations;
* \[ ] missed rotations;
* \[ ] churn cost estimate.

### Acceptatiecriteria

* \[ ] High churn reduces robustness score.
* \[ ] Rotation policy can be compared against no-rotation baseline.
* \[ ] Dashboard shows churn warnings.
* \[ ] Evidence report includes rotation analysis.

\---

## 12\. Fase 9 - Watchdog/Auto-Rollback Validation

Doel: bewijzen dat watchdog en rollback uit Roadmap 078/079 goed reageren.

### Nieuwe module

```text
src/binance\_spot\_bot/watchdog\_validation.py
```

### Validation scenarios

* \[ ] drawdown breach;
* \[ ] daily loss breach;
* \[ ] liquidity shock;
* \[ ] data quality blocked;
* \[ ] correlation spike;
* \[ ] strategy underperformance;
* \[ ] allocation drift;
* \[ ] conflict storm;
* \[ ] evidence tamper;
* \[ ] report generation failure.

### Metrics

* \[ ] expected action;
* \[ ] actual action;
* \[ ] detection delay;
* \[ ] loss before action;
* \[ ] false positive;
* \[ ] false negative;
* \[ ] pass/fail.

### Acceptatiecriteria

* \[ ] Critical scenarios trigger safe action.
* \[ ] Rollback never increases risk.
* \[ ] Validation report is exportable.
* \[ ] CI-safe subset exists.

\---

## 13\. Fase 10 - Portfolio Benchmark Dashboard

Doel: benchmarkresultaten begrijpelijk tonen.

### Nieuwe/uitgebreide dashboardsectie

```text
Portfolio Benchmarks
```

### Panels

* \[ ] scenario selector;
* \[ ] benchmark run selector;
* \[ ] allocation policy comparison;
* \[ ] equity curve comparison;
* \[ ] drawdown comparison;
* \[ ] robustness score table;
* \[ ] liquidity shock results;
* \[ ] correlation stress results;
* \[ ] rotation churn results;
* \[ ] watchdog validation results;
* \[ ] recommendations;
* \[ ] export report.

### Acceptatiecriteria

* \[ ] Dashboard shows no-live/paper-only badge.
* \[ ] Raw JSON only in debug expander.
* \[ ] Results are readable for operator.
* \[ ] Browser smoke covers page import/render.
* \[ ] No signed endpoints.

\---

## 14\. Fase 11 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli scenario-build --symbols BTCUSDT,ETHUSDT,BNBUSDT --source public-cache --scenario bull,bear,range
python -m binance\_spot\_bot.cli stress-generate --scenario liquidity\_shock --severity high --seed 7
python -m binance\_spot\_bot.cli portfolio-replay --scenario-id <id> --portfolio-plan <id>
python -m binance\_spot\_bot.cli portfolio-benchmark --portfolio-plan <id> --scenarios all
python -m binance\_spot\_bot.cli allocation-robustness --benchmark-id <id>
python -m binance\_spot\_bot.cli watchdog-validate --benchmark-id <id>
python -m binance\_spot\_bot.cli benchmark-report --benchmark-id <id>
```

### Acceptatiecriteria

* \[ ] Commands work offline with cache/fixtures.
* \[ ] Commands support JSON output.
* \[ ] Commands never require API keys.
* \[ ] Commands never call order/account endpoints.
* \[ ] Reports are secret-free.

\---

## 15\. Fase 12 - Benchmark Reports \& Evidence

### Nieuwe output

```text
data/portfolio-benchmarks/<benchmark\_id>/
  benchmark\_manifest.json
  benchmark\_summary.md
  benchmark\_summary.json
  scenario\_results.csv
  allocation\_policy\_results.csv
  equity\_curves.csv
  drawdown\_curves.csv
  liquidity\_stress\_report.json
  correlation\_stress\_report.json
  rotation\_churn\_report.json
  watchdog\_validation\_report.json
  robustness\_scores.json
  evidence\_manifest.json
```

### Report bevat

* \[ ] tested strategies;
* \[ ] tested allocation policies;
* \[ ] tested scenarios;
* \[ ] benchmark assumptions;
* \[ ] fee/slippage assumptions;
* \[ ] liquidity shocks;
* \[ ] correlation stress;
* \[ ] robustness ranking;
* \[ ] recommended safe allocation;
* \[ ] blocked policies;
* \[ ] no-live statement.

### Acceptatiecriteria

* \[ ] Reports are reproducible.
* \[ ] Reports contain no secrets.
* \[ ] Evidence manifest verifies hashes.
* \[ ] Dashboard can download report.
* \[ ] Report supports Roadmap 081 decisions.

\---

## 16\. Fase 13 - CI-safe benchmark subset

Doel: lichte benchmark in CI/check-all kunnen draaien.

### CI-safe subset

* \[ ] tiny fixture dataset;
* \[ ] 2 symbols;
* \[ ] 2 strategies;
* \[ ] 2 scenarios;
* \[ ] 2 allocation policies;
* \[ ] no network;
* \[ ] no Streamlit;
* \[ ] max runtime target under 10 seconds.

### Acceptatiecriteria

* \[ ] CI-safe benchmark runs in pytest.
* \[ ] Full benchmark can remain manual.
* \[ ] No external data required.
* \[ ] Results deterministic with seed.
* \[ ] No live/signed endpoints.

\---

## 17\. Fase 14 - Tests

### Unit tests

* \[ ] `tests/test\_scenario\_dataset\_builder.py`
* \[ ] `tests/test\_stress\_scenario\_generator.py`
* \[ ] `tests/test\_portfolio\_scenario\_replay.py`
* \[ ] `tests/test\_portfolio\_benchmark.py`
* \[ ] `tests/test\_allocation\_robustness.py`
* \[ ] `tests/test\_liquidity\_stress.py`
* \[ ] `tests/test\_correlation\_stress.py`
* \[ ] `tests/test\_rotation\_churn\_analysis.py`
* \[ ] `tests/test\_watchdog\_validation.py`
* \[ ] `tests/test\_benchmark\_reports.py`

### Integration tests

* \[ ] Build scenario from fixture candles.
* \[ ] Generate liquidity shock.
* \[ ] Replay portfolio on scenario.
* \[ ] Compare allocation policies.
* \[ ] Compute robustness score.
* \[ ] Validate watchdog action.
* \[ ] Export benchmark report.
* \[ ] Verify evidence manifest.

### Safety tests

* \[ ] Benchmark rejects live mode.
* \[ ] Benchmark uses no signed endpoints.
* \[ ] Benchmark uses no account endpoints.
* \[ ] Replay does not call execution order path.
* \[ ] Reports contain no secrets.
* \[ ] Check-all remains green.

\---

## 18\. Docs

Nieuwe docs:

* \[ ] `docs/paper-portfolio-benchmark-safety-contract.md`
* \[ ] `docs/scenario-dataset-builder.md`
* \[ ] `docs/stress-scenario-generator.md`
* \[ ] `docs/portfolio-scenario-replay.md`
* \[ ] `docs/portfolio-benchmark-suite.md`
* \[ ] `docs/allocation-robustness-score.md`
* \[ ] `docs/liquidity-shock-testing.md`
* \[ ] `docs/correlation-stress-testing.md`
* \[ ] `docs/rotation-churn-analysis.md`
* \[ ] `docs/watchdog-validation.md`
* \[ ] `docs/portfolio-benchmark-dashboard.md`

README updates:

* \[ ] benchmark commands;
* \[ ] scenario replay explanation;
* \[ ] stress testing explanation;
* \[ ] no-live statement;
* \[ ] benchmark report path.

\---

## 19\. Codex bouwvolgorde

### PR 1 - Scenario Dataset Builder

* \[ ] scenario manifests;
* \[ ] cached data input;
* \[ ] tests.

### PR 2 - Stress Scenario Generator

* \[ ] synthetic transforms;
* \[ ] deterministic seed;
* \[ ] tests.

### PR 3 - Portfolio Scenario Replay

* \[ ] replay engine;
* \[ ] output curves/events;
* \[ ] tests.

### PR 4 - Portfolio Benchmark Suite

* \[ ] allocation policy comparison;
* \[ ] baselines;
* \[ ] tests.

### PR 5 - Allocation Robustness Score

* \[ ] scoring model;
* \[ ] reason codes;
* \[ ] tests.

### PR 6 - Liquidity + Correlation Stress

* \[ ] liquidity shock;
* \[ ] correlation stress;
* \[ ] tests.

### PR 7 - Rotation Churn Analysis

* \[ ] churn metrics;
* \[ ] baseline comparison;
* \[ ] tests.

### PR 8 - Watchdog Validation

* \[ ] expected vs actual actions;
* \[ ] detection delay;
* \[ ] tests.

### PR 9 - Reports + Evidence

* \[ ] benchmark report;
* \[ ] evidence manifest;
* \[ ] tests.

### PR 10 - Dashboard + CLI + Docs

* \[ ] CLI commands;
* \[ ] dashboard page;
* \[ ] docs;
* \[ ] browser smoke.

\---

## 20\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 080 PR 1: Scenario Dataset Builder.

Maak src/binance\_spot\_bot/scenario\_dataset\_builder.py.
Bouw scenario datasets vanuit bestaande public Binance cache of test fixtures.
Ondersteun scenario labels: bull, bear, range, high\_volatility, low\_liquidity, data\_gap.
Schrijf scenario\_manifest.json met symbols, intervals, source files, hashes, row counts, scenario labels en data quality.
Voeg tests toe met fake BTCUSDT/ETHUSDT candle fixtures.
Geen Binance API calls, geen signed endpoints, geen order/account endpoints, geen live trading.
```

Waarom eerst:

* Scenario datasets zijn de input voor replay, stress testing en benchmarks.
* Dit raakt geen execution/risk/live logic.
* Het is klein genoeg voor Codex.
* Het maakt de rest van Roadmap 080 reproduceerbaar.

\---

## 21\. Definition of Done

Roadmap 080 is klaar als:

* \[ ] Scenario Dataset Builder werkt.
* \[ ] Synthetic Stress Scenario Generator werkt.
* \[ ] Portfolio Scenario Replay werkt.
* \[ ] Portfolio Benchmark Suite werkt.
* \[ ] Allocation Robustness Score werkt.
* \[ ] Liquidity Shock Testing werkt.
* \[ ] Correlation Stress Testing werkt.
* \[ ] Rotation Churn Analysis werkt.
* \[ ] Watchdog/Auto-Rollback Validation werkt.
* \[ ] Portfolio Benchmark Dashboard werkt.
* \[ ] CLI benchmark commands werken.
* \[ ] Benchmark reports/evidence werken.
* \[ ] CI-safe benchmark subset werkt.
* \[ ] Tests bewijzen geen signed/account/order endpoints.
* \[ ] Reports zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 080 kan na uitvoering naar `Voltooid docs`.

\---

## 22\. Verwachte Roadmap 081 daarna

Na Roadmap 080 zou Roadmap 081 logisch focussen op:

```text
Roadmap 081 - Paper Portfolio Optimization, Risk Budget Search \& Robust Allocation Selection
```

Mogelijke inhoud:

* \[ ] search over allocation policies;
* \[ ] robust allocation optimizer;
* \[ ] risk budget tuning;
* \[ ] Pareto frontier return/drawdown;
* \[ ] scenario-weighted allocation;
* \[ ] conservative default policy selection;
* \[ ] portfolio policy cards;
* \[ ] still no live trading.



---

## Afwerking

Status: Voltooid op 2026-05-11.

Implementatie/evidence: docs/roadmap-076-102-execution-evidence.md, src/binance_spot_bot/paper_os.py, 	ests/test_roadmaps_076_102_paper_os.py.

Validatie: gerichte tests groen, volledige pytest groen, check-all opnieuw uitgevoerd na verplaatsing.



---

## Correctie-audit 2026-05-11

Deze roadmap is teruggezet naar Roadmap docs/ omdat de eerdere markering als Voltooid te breed was. De huidige code bevat alleen een gedeelde foundation in src/binance_spot_bot/paper_os.py en regressietests in 	ests/test_roadmaps_076_102_paper_os.py. Niet alle checklistpunten uit deze roadmap zijn volledig als production-grade feature geimplementeerd.

Open status: opnieuw plannen, opdelen in kleinere uitvoerbare taken, en pas opnieuw naar Voltooid docs/ verplaatsen na concrete implementatie en validatie per roadmap.



---

## Afwerking 2026-05-11

Status: Voltooid.

Concrete implementatie:

- portfolio_benchmarking.py toegevoegd met StressScenario, scenario replay, allocation benchmark, liquidity/spread/price shocks, correlation stress, rotation robustness en reproduceerbare hash.
- Benchmark report export toegevoegd naar JSON/latest/markdown.
- CLI command toegevoegd: paper-portfolio-benchmark.
- Tests toegevoegd: 	ests/test_roadmap_080_portfolio_benchmarking.py.

Validatie:

- python -m pytest tests/test_roadmap_079_paper_portfolio_ops.py tests/test_roadmap_080_portfolio_benchmarking.py -q -> 6 passed.
- Scope blijft paper-only; live trading disabled.

