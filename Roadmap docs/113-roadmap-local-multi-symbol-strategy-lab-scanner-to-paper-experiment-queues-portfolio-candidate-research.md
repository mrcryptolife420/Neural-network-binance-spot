# Roadmap 113 - Local Multi-Symbol Strategy Lab, Scanner-to-Paper Experiment Queues \& Portfolio Candidate Research

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/113-roadmap-local-multi-symbol-strategy-lab-scanner-to-paper-experiment-queues-portfolio-candidate-research.md
```

## Samenvatting

Roadmap 112 maakt een lokale Market Intelligence Workbench voor Binance Spot public data: symbol universe, watchlist scanner, market metrics, rankings, scanner presets, multi-symbol paper analytics en Dashboard V2 scanner widgets.

Roadmap 113 is de logische vervolgstap: **scanner-resultaten omzetten naar veilige paper-only research en experiment queues**. De scanner zegt welke symbolen interessant zijn qua volume, spread, volatility, momentum en data quality. Roadmap 113 laat de bot daarna lokaal en paper-only experimenten uitvoeren op die symbolen, zonder live trading, zonder signed order endpoints en zonder financieel advies.

De kern:

```text
Market scanner rankings
→ scanner-to-experiment queue
→ multi-symbol paper experiment runs
→ strategy/model/symbol comparison
→ risk/overfit/data-quality guards
→ portfolio candidate research
→ Dashboard V2 Strategy Lab workspace
→ evidence/reporting
```

Deze roadmap maakt een lokale “strategy lab” laag bovenop de scanner. Niet om live te handelen, maar om lokaal te onderzoeken welke symbolen, strategieën, modellen en risk settings in paper/datasets beter of slechter presteren.

Live trading blijft volledig buiten scope. Geen live mode, geen signed real-order endpoints, geen echte account workflows, geen auto-trading vanuit scanner rankings en geen financieel advies.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 113`, `113-roadmap`, `Local Multi-Symbol Strategy Lab`, `Scanner-to-Paper`, `Experiment Queues` en `Portfolio Candidate Research`.
* \[x] Geen bestaande Roadmap 113 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 112 is lokaal aangemaakt als Dashboard V2 Local Market Intelligence Workbench, Binance Spot Scanner \& Multi-Symbol Paper Analytics.

### Codebasecontrole

Breed bekeken met focus op scanner, public Binance data, runtime, paper analytics, Dashboard V2, CLI, check-all en safety:

* \[x] `src/binance\_spot\_bot/binance.py`
* \[x] `src/binance\_spot\_bot/market\_data\_source.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/ui/page\_registry.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] roadmaplijn 104-112.

### Belangrijke bestaande basis

De codebase heeft nu of krijgt via Roadmap 104-112:

* \[x] Binance public market endpoints voor exchange info, klines, UI klines, order book, 24hr ticker, rolling ticker, avg price, recent trades, agg trades en book ticker.
* \[x] Signed/account/order endpoints bestaan in dezelfde adapter, dus strategy-lab/scanner-to-experiment code moet deze expliciet blijven blokkeren.
* \[x] Market data sources voor static candles, demo replay, REST polling en WebSocket-wrapper met veilige fallback.
* \[x] Runtime modes beperkt tot `demo`, `paper` en `testnet-readiness`.
* \[x] Runtime snapshots bevatten candles, signals, fills, equity, market data, top of book, data quality, sessions, active model, alerts, paper account, readiness, demo info en reconciliation.
* \[x] Dashboard page registry bevat 36 pages en blokkeert live trading pages.
* \[x] Check-all forceert safe env:

  * `LIVE\_TRADING\_ENABLED=false`;
  * `KILL\_SWITCH=true`;
  * `PYTHONPATH=src`.
* \[x] Roadmap 112 plant public endpoint policy, symbol universe, scanner cache, watchlist scanner, metrics, rankings, presets, multi-symbol paper analytics en scanner evidence.
* \[x] Roadmap 110/111 plannen workspaces, widgets, extension packs en analytics presets.

### Belangrijkste gat na Roadmap 112

Roadmap 112 kan markten scannen en rankings maken, maar de volgende research-stap ontbreekt nog:

* \[ ] Geen scanner-to-experiment queue.
* \[ ] Geen batch paper experiment runner per symbol/watchlist.
* \[ ] Geen vergelijking tussen strategie/model/risk settings over meerdere symbolen.
* \[ ] Geen experiment dataset manifest.
* \[ ] Geen overfit/data leakage guard.
* \[ ] Geen ranking van symbol-strategy candidates op paper-only metrics.
* \[ ] Geen portfolio candidate shortlist.
* \[ ] Geen experiment governance.
* \[ ] Geen reproducible seed/config per experiment.
* \[ ] Geen local experiment evidence bundle.
* \[ ] Geen Dashboard V2 Strategy Lab queue/workbench.
* \[ ] Geen duidelijke “not advice / paper-only research” guard.

Roadmap 113 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 113

Maak een lokale multi-symbol strategy lab laag:

```text
Scanner output
→ experiment candidates
→ experiment queue
→ batch paper experiments
→ strategy/model/risk comparison
→ candidate scorecards
→ portfolio research shortlist
→ evidence bundle
```

Na Roadmap 113 moet de operator:

* \[ ] scanner rankings kunnen omzetten naar paper-only experiment candidates;
* \[ ] experiment queues kunnen maken uit watchlists, rankings en presets;
* \[ ] batch paper experiments kunnen draaien zonder live endpoints;
* \[ ] strategieën/modellen/risk presets kunnen vergelijken over symbolen;
* \[ ] resultaten kunnen sorteren op paper PnL, drawdown, blocks, fills, data quality en stability;
* \[ ] portfolio candidate shortlists kunnen maken;
* \[ ] overfit/data-quality/leakage warnings kunnen zien;
* \[ ] experiment reports en evidence kunnen exporteren;
* \[ ] alles local-only, paper-only en no-live houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen Binance scanner opnieuw bouwen; Roadmap 112 doet dat.
* \[ ] Geen Dashboard V2 workspace systeem opnieuw bouwen.
* \[ ] Geen extension pack systeem opnieuw bouwen.
* \[ ] Geen runtime core refactor opnieuw bouwen.
* \[ ] Geen modeltraining pipeline opnieuw bouwen.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed order endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen echte Binance orders.
* \[ ] Geen auto-trading vanuit scanner rankings.
* \[ ] Geen financieel advies.
* \[ ] Geen cloud experiment platform.
* \[ ] Geen remote telemetry.
* \[ ] Geen API keys vereisen.
* \[ ] Geen experiment dat safety gates omzeilt.

Wel doen:

* \[ ] scanner output naar experiment candidates;
* \[ ] experiment queue;
* \[ ] paper-only batch runner;
* \[ ] strategy/model/risk comparison;
* \[ ] candidate scoring;
* \[ ] portfolio research shortlist;
* \[ ] overfit/data-quality guards;
* \[ ] Dashboard V2 Strategy Lab;
* \[ ] CLI/reports/evidence/tests;
* \[ ] no-live/public-only/paper-only proof.

\---

## 3\. Fase 0 - Multi-Symbol Strategy Lab Safety Contract

Nieuw docbestand:

```text
docs/multi-symbol-strategy-lab-safety-contract.md
```

Regels:

* \[ ] Strategy lab is local-only.
* \[ ] Experiments zijn paper-only.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed order endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen echte orders.
* \[ ] Geen API keys vereist.
* \[ ] Scanner rankings worden alleen research inputs.
* \[ ] Output is geen financieel advies.
* \[ ] Candidate scorecards mogen niet “buy/sell” zeggen.
* \[ ] Experiment queues mogen geen action endpoint voor live execution bevatten.
* \[ ] Batch runner gebruikt safe env:

  * `LIVE\_TRADING\_ENABLED=false`;
  * `KILL\_SWITCH=true`.
* \[ ] Reports/evidence zijn secret-free.
* \[ ] Elke run bevat `live\_trading\_enabled=False`.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen live/signed/account/order endpoints geblokkeerd zijn.
* \[ ] Tests bewijzen experiment output geen buy/sell advies bevat.
* \[ ] Tests bewijzen batch runner zonder API keys kan werken.
* \[ ] Tests bewijzen reports secret-free zijn.

\---

## 4\. Fase 1 - Scanner-to-Experiment Candidate Builder

Nieuwe module:

```text
src/binance\_spot\_bot/strategy\_lab/scanner\_candidate\_builder.py
```

Inputs:

* \[ ] Roadmap 112 watchlist scan report.
* \[ ] symbol ranking report.
* \[ ] market metrics report.
* \[ ] scanner preset metadata.
* \[ ] symbol universe metadata.
* \[ ] cached klines availability.
* \[ ] data quality report.

Dataclasses:

* \[ ] `ScannerExperimentCandidate`
* \[ ] `ScannerCandidateSource`
* \[ ] `ScannerCandidateFilter`
* \[ ] `ScannerCandidateBuildReport`

Candidate fields:

* \[ ] candidate\_id;
* \[ ] symbol;
* \[ ] source\_run\_id;
* \[ ] source\_preset;
* \[ ] ranking\_reasons;
* \[ ] metrics\_snapshot;
* \[ ] data\_quality\_status;
* \[ ] available\_intervals;
* \[ ] recommended\_intervals;
* \[ ] warnings;
* \[ ] not\_financial\_advice\_statement;
* \[ ] live\_trading\_enabled=false.

Filters:

* \[ ] max candidates;
* \[ ] min quote volume;
* \[ ] max spread bps;
* \[ ] min data quality score;
* \[ ] quote asset;
* \[ ] include/exclude symbols;
* \[ ] volatility bucket;
* \[ ] momentum bucket;
* \[ ] require cached klines.

Acceptatiecriteria:

* \[ ] Candidate builder werkt op fixture scanner report.
* \[ ] Missing scanner data geeft warnings, geen crash.
* \[ ] Output bevat geen buy/sell advies.
* \[ ] Live mode wordt geblokkeerd.
* \[ ] Tests dekken filters en edge cases.

\---

## 5\. Fase 2 - Experiment Queue Schema

Nieuwe module:

```text
src/binance\_spot\_bot/strategy\_lab/experiment\_queue.py
```

Dataclasses:

* \[ ] `StrategyExperimentQueue`
* \[ ] `StrategyExperimentJob`
* \[ ] `StrategyExperimentJobStatus`
* \[ ] `StrategyExperimentQueueValidation`
* \[ ] `StrategyExperimentQueueManifest`

Job fields:

* \[ ] job\_id;
* \[ ] candidate\_id;
* \[ ] symbol;
* \[ ] interval;
* \[ ] data\_source:

  * cached\_klines;
  * fixture;
  * demo\_replay;
  * public\_rest\_cache;
* \[ ] strategy\_id;
* \[ ] model\_alias;
* \[ ] risk\_preset;
* \[ ] seed;
* \[ ] window;
* \[ ] max\_steps;
* \[ ] starting\_quote;
* \[ ] created\_at\_ms;
* \[ ] status:

  * queued;
  * running;
  * completed;
  * failed;
  * skipped;
  * blocked.
* \[ ] blockers;
* \[ ] expected\_artifacts;
* \[ ] no\_live\_statement;
* \[ ] live\_trading\_enabled=false.

Queue rules:

* \[ ] max jobs per queue;
* \[ ] max symbols;
* \[ ] max intervals;
* \[ ] max model aliases;
* \[ ] max total estimated runtime;
* \[ ] no live mode;
* \[ ] no signed endpoints;
* \[ ] no account endpoints;
* \[ ] no auto execution to real market.

Acceptatiecriteria:

* \[ ] Queue is JSON-serializable.
* \[ ] Duplicate jobs detected.
* \[ ] Unsafe job blocked.
* \[ ] Queue manifest has hashes.
* \[ ] Tests cover valid/invalid queues.

\---

## 6\. Fase 3 - Experiment Queue Store

Nieuwe module:

```text
src/binance\_spot\_bot/strategy\_lab/experiment\_queue\_store.py
```

Storage:

```text
data/strategy-lab/queues/
  queued/
  running/
  completed/
  reports/
  evidence/
```

Functions:

* \[ ] create queue.
* \[ ] load queue.
* \[ ] list queues.
* \[ ] clone queue.
* \[ ] update job status.
* \[ ] cancel queued job.
* \[ ] archive queue.
* \[ ] export queue manifest.
* \[ ] verify queue manifest.
* \[ ] cleanup old queues.

Acceptatiecriteria:

* \[ ] Store is local-only.
* \[ ] Store is hash/manifest based.
* \[ ] Store rejects path traversal.
* \[ ] Store redacts secret-like values.
* \[ ] Tests use temp dirs.

\---

## 7\. Fase 4 - Strategy/Risk/Model Experiment Matrix

Nieuwe module:

```text
src/binance\_spot\_bot/strategy\_lab/experiment\_matrix.py
```

Matrix dimensions:

* \[ ] symbols;
* \[ ] intervals;
* \[ ] strategy IDs;
* \[ ] model aliases;
* \[ ] risk presets;
* \[ ] seeds;
* \[ ] window sizes;
* \[ ] data sources.

Presets:

### `small\_safe\_smoke`

* \[ ] max 2 symbols;
* \[ ] 1 interval;
* \[ ] rule-based model;
* \[ ] conservative risk;
* \[ ] fixture/cached data.

### `scanner\_top10\_paper`

* \[ ] top 10 scanner candidates;
* \[ ] 1m/5m optional;
* \[ ] rule-based + selected model alias;
* \[ ] conservative and balanced risk.

### `model\_compare`

* \[ ] same symbols;
* \[ ] same candles;
* \[ ] multiple model aliases;
* \[ ] same risk settings.

### `risk\_compare`

* \[ ] same symbols/model;
* \[ ] conservative/balanced/aggressive paper risk presets;
* \[ ] no live actions.

Acceptatiecriteria:

* \[ ] Matrix expands to queue jobs.
* \[ ] Matrix respects max job budget.
* \[ ] Unsupported model/risk preset blocked.
* \[ ] Deterministic job IDs.
* \[ ] Tests cover matrix expansion.

\---

## 8\. Fase 5 - Paper Experiment Runner

Nieuwe module:

```text
src/binance\_spot\_bot/strategy\_lab/paper\_experiment\_runner.py
```

Runner behavior:

* \[ ] load queue.
* \[ ] validate no-live.
* \[ ] load cached candles.
* \[ ] create paper-only runtime or pure paper simulation.
* \[ ] run deterministic steps.
* \[ ] collect fills/signals/risk blocks/equity.
* \[ ] export per-job result.
* \[ ] update queue status.
* \[ ] stop on critical safety finding.
* \[ ] support resume failed/unfinished queue.
* \[ ] no API keys required.

Dataclasses:

* \[ ] `PaperExperimentRun`
* \[ ] `PaperExperimentJobResult`
* \[ ] `PaperExperimentRunnerConfig`
* \[ ] `PaperExperimentRunnerReport`

Per job result:

* \[ ] job\_id;
* \[ ] symbol;
* \[ ] interval;
* \[ ] strategy\_id;
* \[ ] model\_alias;
* \[ ] risk\_preset;
* \[ ] status;
* \[ ] candle\_count;
* \[ ] signal\_count;
* \[ ] fill\_count;
* \[ ] block\_count;
* \[ ] paper\_pnl;
* \[ ] max\_drawdown;
* \[ ] fees;
* \[ ] exposure\_summary;
* \[ ] data\_quality\_warnings;
* \[ ] runtime\_messages;
* \[ ] report\_paths;
* \[ ] live\_trading\_enabled=false.

Acceptatiecriteria:

* \[ ] Runner works with fixture candles.
* \[ ] Runner works without API keys.
* \[ ] Runner blocks live/signed/account/order endpoints.
* \[ ] Runner can resume.
* \[ ] Tests cover successful/failed/blocked jobs.

\---

## 9\. Fase 6 - Experiment Result Store

Nieuwe module:

```text
src/binance\_spot\_bot/strategy\_lab/experiment\_result\_store.py
```

Storage:

```text
data/strategy-lab/results/
  jobs/
  queues/
  scorecards/
  comparisons/
  exports/
```

Functions:

* \[ ] save job result.
* \[ ] load job result.
* \[ ] list results by queue.
* \[ ] list results by symbol.
* \[ ] list results by strategy/model/risk.
* \[ ] save queue result summary.
* \[ ] export CSV/JSON/Markdown.
* \[ ] verify result hashes.

Acceptatiecriteria:

* \[ ] Result store is local-only.
* \[ ] Result hashes verify.
* \[ ] Decimal serialization safe.
* \[ ] Reports redacted.
* \[ ] Tests use temp dirs.

\---

## 10\. Fase 7 - Strategy Comparison Engine

Nieuwe module:

```text
src/binance\_spot\_bot/strategy\_lab/strategy\_comparison.py
```

Compare dimensions:

* \[ ] by symbol.
* \[ ] by strategy.
* \[ ] by model alias.
* \[ ] by risk preset.
* \[ ] by interval.
* \[ ] by scanner source preset.
* \[ ] by data quality bucket.

Metrics:

* \[ ] paper PnL.
* \[ ] max drawdown.
* \[ ] return/drawdown ratio.
* \[ ] trade count.
* \[ ] fill rate.
* \[ ] block rate.
* \[ ] risk block reasons.
* \[ ] signal count.
* \[ ] signal confidence average.
* \[ ] data quality warning count.
* \[ ] fees.
* \[ ] stability score.
* \[ ] reproducibility score.

Acceptatiecriteria:

* \[ ] Comparison deterministic.
* \[ ] Missing results handled.
* \[ ] Tables sort correctly.
* \[ ] No financial advice wording.
* \[ ] Tests cover comparison metrics.

\---

## 11\. Fase 8 - Candidate Scorecards

Nieuwe module:

```text
src/binance\_spot\_bot/strategy\_lab/candidate\_scorecards.py
```

Score categories:

* \[ ] market quality score;
* \[ ] data quality score;
* \[ ] paper performance score;
* \[ ] drawdown penalty;
* \[ ] liquidity/spread score;
* \[ ] block penalty;
* \[ ] stability score;
* \[ ] model consistency score;
* \[ ] risk compatibility score;
* \[ ] portfolio diversification fit.

Important wording:

* \[ ] Use “research candidate”.
* \[ ] Use “paper-only score”.
* \[ ] Do not say “buy”, “sell”, “sure win”, “best trade”.
* \[ ] Do not hide risk warnings.

Output:

* \[ ] candidate scorecard JSON;
* \[ ] candidate scorecard Markdown;
* \[ ] top candidates table;
* \[ ] blocked candidates table;
* \[ ] warning reasons.

Acceptatiecriteria:

* \[ ] Scorecard deterministic.
* \[ ] Hard risk/data blockers reduce score.
* \[ ] Advice wording scan passes.
* \[ ] Scorecards are secret-free.
* \[ ] Tests cover scoring.

\---

## 12\. Fase 9 - Portfolio Candidate Research

Nieuwe module:

```text
src/binance\_spot\_bot/strategy\_lab/portfolio\_candidate\_research.py
```

Goal: research-only shortlist for paper portfolio experiments.

Inputs:

* \[ ] candidate scorecards.
* \[ ] strategy comparison report.
* \[ ] symbol ranking report.
* \[ ] risk limits.
* \[ ] diversification constraints.
* \[ ] max candidates.

Research outputs:

* \[ ] candidate basket.
* \[ ] symbol exposure notes.
* \[ ] correlation proxy from candles.
* \[ ] volatility grouping.
* \[ ] quote asset distribution.
* \[ ] strategy/model diversity.
* \[ ] paper-only allocation suggestion.
* \[ ] risk warnings.
* \[ ] experiment follow-up queue.

Rules:

* \[ ] No live allocation.
* \[ ] No real-money recommendation.
* \[ ] No order generation.
* \[ ] Output is research-only.

Acceptatiecriteria:

* \[ ] Shortlist generated from fixtures.
* \[ ] Over-concentrated basket warning.
* \[ ] Missing correlation data handled.
* \[ ] No advice wording.
* \[ ] Tests cover basket constraints.

\---

## 13\. Fase 10 - Overfit, Leakage \& Data Quality Guards

Nieuwe module:

```text
src/binance\_spot\_bot/strategy\_lab/research\_guards.py
```

Guards:

* \[ ] minimum candle count.
* \[ ] stale data.
* \[ ] too few trades.
* \[ ] one-trade result warning.
* \[ ] excessive drawdown.
* \[ ] high spread.
* \[ ] data gaps.
* \[ ] duplicate candle timestamps.
* \[ ] suspicious perfect score.
* \[ ] train/test leakage warning where relevant.
* \[ ] same data used for scanner and score without validation.
* \[ ] insufficient symbols.
* \[ ] insufficient intervals.
* \[ ] model alias missing.
* \[ ] result not reproducible.

Guard statuses:

* \[ ] pass.
* \[ ] warn.
* \[ ] block.
* \[ ] unknown.

Acceptatiecriteria:

* \[ ] Guards run on job and queue results.
* \[ ] Blocked candidate cannot become top candidate.
* \[ ] Warnings shown in scorecards.
* \[ ] Tests cover each guard.
* \[ ] Reports secret-free.

\---

## 14\. Fase 11 - Experiment Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/strategy\_lab/experiment\_evidence\_bundle.py
```

Bundle bevat:

* \[ ] safety contract.
* \[ ] candidate builder report.
* \[ ] queue manifest.
* \[ ] experiment matrix.
* \[ ] runner report.
* \[ ] job result manifests.
* \[ ] strategy comparison report.
* \[ ] candidate scorecards.
* \[ ] portfolio candidate research.
* \[ ] research guard report.
* \[ ] no-live proof.
* \[ ] no-financial-advice proof.
* \[ ] public/safe data source proof.
* \[ ] redaction proof.
* \[ ] hashes.

Output:

```text
data/strategy-lab/evidence/<run\_id>/
  strategy\_lab\_evidence\_manifest.json
  strategy\_lab\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle links to Roadmap 112 scanner evidence.
* \[ ] Dashboard can download bundle.

\---

## 15\. Fase 12 - Dashboard V2 Strategy Lab Workbench

Nieuwe Dashboard V2 routes:

```text
/strategy-lab
/strategy-lab/candidates
/strategy-lab/queues
/strategy-lab/experiments
/strategy-lab/comparisons
/strategy-lab/scorecards
/strategy-lab/portfolio-research
/strategy-lab/evidence
```

Panels:

* \[ ] scanner run selector;
* \[ ] candidate filters;
* \[ ] candidate table;
* \[ ] queue builder;
* \[ ] matrix builder;
* \[ ] queue run status;
* \[ ] experiment result table;
* \[ ] comparison charts;
* \[ ] candidate scorecards;
* \[ ] portfolio shortlist;
* \[ ] research guard warnings;
* \[ ] evidence export;
* \[ ] no-live/no-advice banner.

Acceptatiecriteria:

* \[ ] Strategy Lab page loads.
* \[ ] Candidate builder works from fixture scanner report.
* \[ ] Queue builder preview works.
* \[ ] Result comparison visible.
* \[ ] Browser smoke covers happy path.

\---

## 16\. Fase 13 - Strategy Lab Widgets \& Workspace Packs

Nieuwe widgets:

* \[ ] `ScannerCandidateTableWidget`
* \[ ] `ExperimentQueueWidget`
* \[ ] `ExperimentMatrixWidget`
* \[ ] `ExperimentRunStatusWidget`
* \[ ] `StrategyComparisonWidget`
* \[ ] `CandidateScorecardWidget`
* \[ ] `ResearchGuardWidget`
* \[ ] `PortfolioCandidateWidget`
* \[ ] `ExperimentEvidenceWidget`

Nieuwe Roadmap 111 packs:

### `scanner-to-paper-lab`

* \[ ] candidates;
* \[ ] queue builder;
* \[ ] runner status;
* \[ ] comparison;
* \[ ] evidence.

### `model-compare-lab`

* \[ ] model aliases;
* \[ ] candidate symbols;
* \[ ] result comparison;
* \[ ] scorecards.

### `risk-compare-lab`

* \[ ] risk presets;
* \[ ] drawdown/block analysis;
* \[ ] candidate scorecards.

### `portfolio-candidate-lab`

* \[ ] candidate shortlist;
* \[ ] diversification;
* \[ ] portfolio research;
* \[ ] follow-up queue.

Acceptatiecriteria:

* \[ ] Widgets validate in Dashboard V2 registry.
* \[ ] Packs validate through extension pack schema.
* \[ ] No-live widgets included.
* \[ ] Browser smoke covers one pack.
* \[ ] Pack evidence generated.

\---

## 17\. Fase 14 - Strategy Lab API

Nieuwe Dashboard V2 API routes:

```text
GET  /api/strategy-lab/health
POST /api/strategy-lab/candidates/build
GET  /api/strategy-lab/candidates
POST /api/strategy-lab/queue/preview
POST /api/strategy-lab/queue/create
GET  /api/strategy-lab/queues
GET  /api/strategy-lab/queues/{queue\_id}
POST /api/strategy-lab/queues/{queue\_id}/run
POST /api/strategy-lab/queues/{queue\_id}/cancel
GET  /api/strategy-lab/results
GET  /api/strategy-lab/results/{run\_id}
POST /api/strategy-lab/comparison
POST /api/strategy-lab/scorecards
POST /api/strategy-lab/portfolio-research
POST /api/strategy-lab/evidence-export
WS   /ws/strategy-lab
```

Rules:

* \[ ] All responses include `live\_trading\_enabled=False`.
* \[ ] Run queue requires explicit `RUN\_PAPER\_EXPERIMENTS\_ONLY`.
* \[ ] Large queue requires preview first.
* \[ ] API never calls signed/order/account endpoints.
* \[ ] No advice wording.
* \[ ] Payload limits enforced.

Acceptatiecriteria:

* \[ ] TestClient covers core routes.
* \[ ] Queue run confirm required.
* \[ ] Unsafe queue blocked.
* \[ ] WebSocket sends queue status.
* \[ ] Reports redacted.

\---

## 18\. Fase 15 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli strategy-lab-candidates-build --scanner-run <id> --json
python -m binance\_spot\_bot.cli strategy-lab-queue-preview --candidates latest --preset small\_safe\_smoke --json
python -m binance\_spot\_bot.cli strategy-lab-queue-create --candidates latest --preset small\_safe\_smoke
python -m binance\_spot\_bot.cli strategy-lab-queue-run --queue <id> --confirm RUN\_PAPER\_EXPERIMENTS\_ONLY
python -m binance\_spot\_bot.cli strategy-lab-queue-status --queue <id> --json
python -m binance\_spot\_bot.cli strategy-lab-results --queue <id> --json
python -m binance\_spot\_bot.cli strategy-lab-compare --queue <id> --json
python -m binance\_spot\_bot.cli strategy-lab-scorecards --queue <id> --json
python -m binance\_spot\_bot.cli strategy-lab-portfolio-candidates --queue <id> --json
python -m binance\_spot\_bot.cli strategy-lab-guards --queue <id> --json
python -m binance\_spot\_bot.cli strategy-lab-evidence-export --queue <id>
python -m binance\_spot\_bot.cli dashboard-v2-strategy-lab-smoke --json
```

Acceptatiecriteria:

* \[ ] Commands werken offline met fixtures/cache.
* \[ ] Commands ondersteunen JSON.
* \[ ] Queue run vereist confirm.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Reports zijn secret-free.

\---

## 19\. Fase 16 - Check-All Integration

Fast profile:

* \[ ] strategy lab module imports.
* \[ ] safety contract/no-live checks.
* \[ ] queue schema validation.
* \[ ] candidate builder fixture.
* \[ ] no-advice wording scan.

Deep profile:

* \[ ] experiment queue fixture.
* \[ ] paper experiment runner fixture.
* \[ ] comparison fixture.
* \[ ] scorecard fixture.
* \[ ] portfolio candidate fixture.
* \[ ] research guard fixture.
* \[ ] strategy lab API smoke.
* \[ ] dashboard browser smoke.
* \[ ] evidence bundle verify.

Acceptatiecriteria:

* \[ ] Fast check-all blijft snel.
* \[ ] Deep check-all dekt end-to-end paper experiment.
* \[ ] No-live failure hard fail.
* \[ ] Advice wording failure hard fail.
* \[ ] Reports secret-free.

\---

## 20\. Fase 17 - Operator/UAT Integration

Roadmap 102:

* \[ ] Operator manual krijgt Strategy Lab guide.
* \[ ] CLI cookbook krijgt strategy-lab commands.
* \[ ] Troubleshooting krijgt experiment queue/playbook.
* \[ ] Evidence guide krijgt Strategy Lab evidence uitleg.

Roadmap 103:

* \[ ] UAT scenario: scanner results naar candidates.
* \[ ] UAT scenario: queue preview maken.
* \[ ] UAT scenario: small paper experiment queue draaien.
* \[ ] UAT scenario: scorecards bekijken.
* \[ ] UAT scenario: portfolio candidate shortlist bekijken.
* \[ ] UAT scenario: no-live/no-advice proof controleren.
* \[ ] UAT scenario: evidence exporteren.

Acceptatiecriteria:

* \[ ] UAT scenarios pass.
* \[ ] Docs link valid.
* \[ ] No-live/no-advice proof included.
* \[ ] UAT feedback can create strategy-lab backlog items.
* \[ ] Browser smoke/UAT evidence linked.

\---

## 21\. Fase 18 - Release/Knowledge/Test/Performance Integration

Roadmap 089:

* \[ ] Release notes include Strategy Lab.
* \[ ] Version manifest includes strategy-lab schema version.
* \[ ] Migration notes include experiment queue/result paths.

Roadmap 091:

* \[ ] Knowledge graph maps scanner → candidates → queue → runner → scorecards.
* \[ ] Impact analysis detects scanner/strategy/model/risk changes affecting Strategy Lab.
* \[ ] Ownership map includes Strategy Lab modules.

Roadmap 092:

* \[ ] Test selector chooses strategy-lab tests for queue/runner/comparison changes.
* \[ ] Scanner changes select candidate builder tests.
* \[ ] Risk/model changes select paper experiment tests.
* \[ ] Dashboard Strategy Lab UI changes select browser smoke.

Roadmap 093:

* \[ ] Performance budgets for queue size, run time, result payload, report size.
* \[ ] Heavy queues produce warnings/findings.
* \[ ] Experiment runtime trends stored locally.

Acceptatiecriteria:

* \[ ] Release evidence includes Strategy Lab evidence.
* \[ ] Knowledge graph updated.
* \[ ] Test selection works.
* \[ ] Performance reports include experiment budgets.
* \[ ] No-live proof preserved.

\---

## 22\. Fase 19 - Scheduled Strategy Lab Reports

Scheduled jobs:

* \[ ] weekly candidate refresh from latest scanner evidence.
* \[ ] weekly small safe paper experiment queue.
* \[ ] weekly scorecard summary.
* \[ ] weekly research guard report.
* \[ ] monthly portfolio candidate research report.
* \[ ] post-scanner-change candidate validation.
* \[ ] post-model-change model comparison smoke.
* \[ ] post-risk-change risk comparison smoke.

Metrics:

* \[ ] queue count.
* \[ ] completed job count.
* \[ ] failed/blocked job count.
* \[ ] average paper PnL.
* \[ ] max drawdown distribution.
* \[ ] block rate.
* \[ ] top research candidates.
* \[ ] rejected candidates.
* \[ ] guard warnings.
* \[ ] evidence export status.
* \[ ] no-live/no-advice proof status.

Acceptatiecriteria:

* \[ ] Jobs are local-only.
* \[ ] Jobs use cached/fixture data unless configured public cache.
* \[ ] Jobs never call signed/order/account endpoints.
* \[ ] Reports are secret-free.
* \[ ] No live trading.

\---

## 23\. Tests

### Unit tests

* \[ ] `tests/test\_multi\_symbol\_strategy\_lab\_safety\_contract.py`
* \[ ] `tests/test\_scanner\_candidate\_builder.py`
* \[ ] `tests/test\_strategy\_experiment\_queue.py`
* \[ ] `tests/test\_experiment\_queue\_store.py`
* \[ ] `tests/test\_experiment\_matrix.py`
* \[ ] `tests/test\_paper\_experiment\_runner.py`
* \[ ] `tests/test\_experiment\_result\_store.py`
* \[ ] `tests/test\_strategy\_comparison.py`
* \[ ] `tests/test\_candidate\_scorecards.py`
* \[ ] `tests/test\_portfolio\_candidate\_research.py`
* \[ ] `tests/test\_research\_guards.py`
* \[ ] `tests/test\_strategy\_lab\_evidence\_bundle.py`
* \[ ] `tests/test\_strategy\_lab\_api.py`
* \[ ] `tests/test\_strategy\_lab\_widgets.py`

### Integration tests

* \[ ] Build candidates from scanner fixture.
* \[ ] Build queue from candidates.
* \[ ] Expand matrix to jobs.
* \[ ] Run small paper experiment fixture.
* \[ ] Store and load job results.
* \[ ] Generate comparison report.
* \[ ] Generate scorecards.
* \[ ] Generate portfolio candidate research.
* \[ ] Run research guards.
* \[ ] Export evidence bundle.
* \[ ] Dashboard API TestClient smoke.

### Browser smoke

* \[ ] `/strategy-lab` loads.
* \[ ] candidate table visible.
* \[ ] queue builder preview works.
* \[ ] experiment results table visible.
* \[ ] comparison chart visible.
* \[ ] scorecards visible.
* \[ ] portfolio research page visible.
* \[ ] no-live/no-advice banner visible.
* \[ ] no live controls visible.

### Safety tests

* \[ ] Live mode blocked.
* \[ ] Signed endpoint blocked.
* \[ ] Account endpoint blocked.
* \[ ] Order endpoint blocked.
* \[ ] Queue run requires paper-only confirm.
* \[ ] Runner works without API keys.
* \[ ] Advice wording blocked.
* \[ ] No auto-order action present.
* \[ ] Evidence secret-free.
* \[ ] Check-all safe env preserved.

\---

## 24\. Docs

Nieuwe docs:

```text
docs/strategy-lab/multi-symbol-strategy-lab-safety-contract.md
docs/strategy-lab/scanner-candidate-builder.md
docs/strategy-lab/experiment-queue.md
docs/strategy-lab/experiment-matrix.md
docs/strategy-lab/paper-experiment-runner.md
docs/strategy-lab/strategy-comparison.md
docs/strategy-lab/candidate-scorecards.md
docs/strategy-lab/portfolio-candidate-research.md
docs/strategy-lab/research-guards.md
docs/strategy-lab/evidence-bundle.md
docs/strategy-lab/dashboard-v2-workbench.md
docs/strategy-lab/troubleshooting.md
```

README updates:

* \[ ] Strategy Lab overview.
* \[ ] Scanner-to-paper workflow.
* \[ ] Paper-only/no-live statement.
* \[ ] No financial advice statement.
* \[ ] CLI examples.
* \[ ] Dashboard V2 route.
* \[ ] Evidence export.

Operator docs updates:

* \[ ] Strategy Lab quick start.
* \[ ] Queue preview/run guide.
* \[ ] Scorecard interpretation.
* \[ ] Portfolio research interpretation.
* \[ ] Research guard troubleshooting.
* \[ ] No-live/no-advice proof.

\---

## 25\. Codex bouwvolgorde

### PR 1 - Safety Contract + Candidate Builder

* \[ ] `docs/strategy-lab/multi-symbol-strategy-lab-safety-contract.md`
* \[ ] `strategy\_lab/scanner\_candidate\_builder.py`
* \[ ] scanner fixture tests.
* \[ ] no-advice tests.

### PR 2 - Experiment Queue Schema + Store

* \[ ] `experiment\_queue.py`
* \[ ] `experiment\_queue\_store.py`
* \[ ] manifest/hash tests.

### PR 3 - Experiment Matrix

* \[ ] `experiment\_matrix.py`
* \[ ] matrix expansion presets.
* \[ ] job budget tests.

### PR 4 - Paper Experiment Runner

* \[ ] `paper\_experiment\_runner.py`
* \[ ] paper-only fixture runner.
* \[ ] no signed/account/order tests.

### PR 5 - Result Store + Strategy Comparison

* \[ ] `experiment\_result\_store.py`
* \[ ] `strategy\_comparison.py`
* \[ ] comparison report tests.

### PR 6 - Scorecards + Portfolio Research + Guards

* \[ ] `candidate\_scorecards.py`
* \[ ] `portfolio\_candidate\_research.py`
* \[ ] `research\_guards.py`
* \[ ] advice wording/guard tests.

### PR 7 - API + Dashboard Widgets

* \[ ] strategy lab API routes.
* \[ ] Strategy Lab widgets.
* \[ ] TestClient/frontend tests.

### PR 8 - Dashboard Workbench + Packs

* \[ ] Dashboard V2 Strategy Lab pages.
* \[ ] workspace/template packs.
* \[ ] browser smoke.

### PR 9 - Evidence + CLI + Check-All

* \[ ] `experiment\_evidence\_bundle.py`
* \[ ] CLI commands.
* \[ ] check-all integration.

### PR 10 - Docs, UAT, Release/Knowledge/Test/Performance Integration

* \[ ] docs.
* \[ ] UAT scenarios.
* \[ ] release notes.
* \[ ] knowledge/test/performance integration.
* \[ ] scheduled reports.

\---

## 26\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 113 PR 1: Multi-Symbol Strategy Lab Safety Contract + Scanner-to-Experiment Candidate Builder.

Maak docs/strategy-lab/multi-symbol-strategy-lab-safety-contract.md.

Maak src/binance\_spot\_bot/strategy\_lab/\_\_init\_\_.py.
Maak src/binance\_spot\_bot/strategy\_lab/scanner\_candidate\_builder.py met:
- ScannerExperimentCandidate
- ScannerCandidateSource
- ScannerCandidateFilter
- ScannerCandidateBuildReport
- build\_scanner\_experiment\_candidates(scanner\_report: dict, filters: ScannerCandidateFilter)
- scanner\_candidate\_build\_report\_to\_dict(...)
- write\_scanner\_candidate\_build\_report(...)

Candidate moet minimaal bevatten:
- candidate\_id
- symbol
- source\_run\_id
- source\_preset
- ranking\_reasons
- metrics\_snapshot
- data\_quality\_status
- available\_intervals
- recommended\_intervals
- warnings
- not\_financial\_advice\_statement
- no\_live\_statement
- live\_trading\_enabled=False

Filters moeten minimaal ondersteunen:
- max\_candidates
- min\_quote\_volume
- max\_spread\_bps
- min\_data\_quality\_score
- quote\_asset
- include\_symbols
- exclude\_symbols
- volatility\_bucket
- momentum\_bucket
- require\_cached\_klines

Gedrag:
- werkt op Roadmap 112 scanner/ranking fixture dictionaries
- ontbrekende velden worden warnings, geen crash
- live mode of live\_trading\_enabled=True blokkeert
- output bevat geen buy/sell/advice wording
- candidate\_id is deterministic
- secret-like values worden geredact
- report bevat no\_live\_statement
- report bevat not\_financial\_advice\_statement
- geen command execution
- geen API calls
- geen signed endpoints
- geen account/order endpoints
- geen live trading

Voeg tests toe voor:
- valid scanner report creates candidates
- filters max\_candidates/min\_quote\_volume/max\_spread\_bps
- missing fields produce warnings
- live\_trading\_enabled True blocked
- deterministic candidate\_id
- advice wording blocked
- JSON serialization
- secret-like values worden geredact
- live\_trading\_enabled=False
- no\_live\_statement aanwezig
- not\_financial\_advice\_statement aanwezig
```

Waarom eerst:

* Roadmap 113 begint bij het veilig omzetten van scanner-output naar paper-only experiment candidates.
* Het is read-only en raakt runtime/trading/frontend niet.
* Het is klein genoeg voor Codex.
* No-live en no-financial-advice regels worden meteen testbaar.
* Daarna kunnen queue schema, matrix en paper runner veilig op deze candidates bouwen.

\---

## 27\. Definition of Done

Roadmap 113 is klaar als:

* \[ ] Multi-Symbol Strategy Lab Safety Contract bestaat.
* \[ ] Scanner-to-Experiment Candidate Builder werkt.
* \[ ] Experiment Queue Schema werkt.
* \[ ] Experiment Queue Store werkt.
* \[ ] Strategy/Risk/Model Experiment Matrix werkt.
* \[ ] Paper Experiment Runner werkt.
* \[ ] Experiment Result Store werkt.
* \[ ] Strategy Comparison Engine werkt.
* \[ ] Candidate Scorecards werken.
* \[ ] Portfolio Candidate Research werkt.
* \[ ] Overfit, Leakage \& Data Quality Guards werken.
* \[ ] Experiment Evidence Bundle werkt.
* \[ ] Dashboard V2 Strategy Lab Workbench werkt.
* \[ ] Strategy Lab Widgets \& Workspace Packs werken.
* \[ ] Strategy Lab API werkt.
* \[ ] CLI commands werken.
* \[ ] Check-All Integration werkt.
* \[ ] Operator/UAT Integration werkt.
* \[ ] Release/Knowledge/Test/Performance Integration werkt.
* \[ ] Scheduled Strategy Lab Reports werken.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen runner zonder API keys werkt.
* \[ ] Tests bewijzen geen financieel advies wording.
* \[ ] Tests bewijzen evidence secret-free is.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Strategy Lab is local-only en paper-only.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 113 kan na uitvoering naar `Voltooid docs`.

\---

## 28\. Verwachte Roadmap 114 daarna

Als Roadmap 113 groen is:

```text
Roadmap 114 - Local Paper Portfolio Experiment Orchestrator, Candidate Basket Simulation \& Allocation Research
```

Mogelijke inhoud:

* \[ ] portfolio candidate baskets uit Strategy Lab;
* \[ ] multi-symbol portfolio paper simulation;
* \[ ] allocation constraints;
* \[ ] basket drawdown/volatility research;
* \[ ] scenario stress tests;
* \[ ] no-live portfolio evidence;
* \[ ] still no live trading.

```

Als Roadmap 113 performanceproblemen vindt:

```text
Roadmap 114 - Strategy Lab Experiment Performance Burn-Down, Queue Scheduling \& Result Cache Optimization
```

Mogelijke inhoud:

* \[ ] queue scheduler optimaliseren;
* \[ ] fixture/candle cache verbeteren;
* \[ ] result cache;
* \[ ] batch runner parallelisme local-safe;
* \[ ] heavy queue warnings;
* \[ ] still no live trading.

```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Strategy lab scanner queue to paper experiment research.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.

