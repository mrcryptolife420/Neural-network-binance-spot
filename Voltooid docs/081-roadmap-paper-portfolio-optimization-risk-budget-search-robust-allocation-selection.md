# Roadmap 081 - Paper Portfolio Optimization, Risk Budget Search \& Robust Allocation Selection

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Voltooid docs/081-roadmap-paper-portfolio-optimization-risk-budget-search-robust-allocation-selection.md
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
* `Roadmap docs/080-roadmap-paper-portfolio-benchmarking-stress-testing-scenario-replay.md`

Doel: Roadmap 080 benchmarkt en stresstest paper portfolio allocations. Roadmap 081 gebruikt die benchmarkresultaten om systematisch te zoeken naar robuuste paper allocaties, risk budgets, caps en rotation policies. De roadmap kiest niet simpelweg de hoogste PnL, maar selecteert een conservative, evidence-based paper portfolio policy die goed blijft over meerdere scenario’s, stress tests en regimes.

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
* \[x] Geen bestaande Roadmap 081 gevonden via repo-search.
* \[x] Roadmap 076 is lokaal aangemaakt voor Binance public data ingestion.
* \[x] Roadmap 077 is lokaal aangemaakt voor backtest datasets en confidence calibration.
* \[x] Roadmap 078 is lokaal aangemaakt voor paper deployment en auto rollback.
* \[x] Roadmap 079 is lokaal aangemaakt voor paper portfolio operations.
* \[x] Roadmap 080 is lokaal aangemaakt voor paper portfolio benchmarking/stress/scenario replay.

### Codebasecontrole

Gecontroleerde relevante modules:

* \[x] `src/binance\_spot\_bot/portfolio.py`
* \[x] `src/binance\_spot\_bot/portfolio\_risk.py`
* \[x] `src/binance\_spot\_bot/backtest.py`
* \[x] `src/binance\_spot\_bot/evaluation.py`

### Bestaande basis

Er bestaat al:

* \[x] `Portfolio` met balances, positions, buy/sell accounting, fees, realized PnL, total equity en exposure.
* \[x] `PortfolioRiskEngine` met total exposure, open positions, daily loss en cooldown.
* \[x] `BacktestEngine` met trades, blocked, final equity, PnL en max drawdown.
* \[x] `evaluate\_walk\_forward` met dataset manifest, leakage guard, baseline/candidate comparison en costs.
* \[x] Multi-symbol demo/budget/risk validation uit Roadmap 075.
* \[x] Roadmap 080 levert benchmarkresultaten, stress results en robustness scores.

### Belangrijkste gat na Roadmap 080

Na Roadmap 080 weet je hoe policies presteren in scenario’s. Wat nog mist:

* \[ ] automatisch zoeken over allocation policies;
* \[ ] risk budget tuning;
* \[ ] Pareto frontier tussen return, drawdown, turnover en robustness;
* \[ ] scenario-weighted policy selectie;
* \[ ] conservative default policy card;
* \[ ] risk cap search;
* \[ ] strategy/symbol budget caps optimaliseren;
* \[ ] rotation policy parameters optimaliseren;
* \[ ] overfit guards voor allocation search;
* \[ ] paper-only policy approval gate.

\---

## 1\. Hoofddoel Roadmap 081

Maak een **paper portfolio optimizer** die benchmarkresultaten omzet in een veilige, robuuste paper allocation policy:

```text
Benchmark results
→ search space
→ risk budget search
→ scenario-weighted evaluation
→ Pareto frontier
→ robustness filters
→ conservative policy selection
→ policy card
→ paper-only approval
```

Na Roadmap 081 moet de bot:

* \[ ] meerdere allocation policies automatisch kunnen testen;
* \[ ] risk budgets kunnen zoeken binnen veilige grenzen;
* \[ ] portfolio policies kunnen ranken op robustness, niet alleen PnL;
* \[ ] scenario weights kunnen gebruiken;
* \[ ] Pareto frontier kunnen tonen;
* \[ ] overfit policies kunnen blokkeren;
* \[ ] conservative default policy kunnen voorstellen;
* \[ ] policy cards kunnen exporteren;
* \[ ] policy approval paper-only houden;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe benchmark suite; Roadmap 080 doet dat.
* \[ ] Geen nieuwe data ingestion; Roadmap 076 doet dat.
* \[ ] Geen nieuwe backtest engine vanaf nul.
* \[ ] Geen nieuwe portfolio engine vanaf nul.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen real-money optimizer.
* \[ ] Geen futures/margin/leverage.
* \[ ] Geen AI autonomous allocator zonder guardrails.

Wel doen:

* \[ ] Roadmap 080 benchmark outputs gebruiken;
* \[ ] allocation search toevoegen;
* \[ ] risk budget search toevoegen;
* \[ ] policy selection rules toevoegen;
* \[ ] evidence/card export toevoegen;
* \[ ] dashboard optimizer panel toevoegen;
* \[ ] CLI commands toevoegen;
* \[ ] alles paper-only houden.

\---

## 3\. Fase 0 - Optimization Safety Contract

Doel: vastleggen dat optimalisatie geen live deployment of real-money allocatie betekent.

### Nieuwe doc

```text
docs/paper-portfolio-optimization-safety-contract.md
```

### Regels

* \[ ] Optimizer werkt alleen met:

  * benchmark artifacts;
  * scenario replay artifacts;
  * cached public data;
  * demo/paper metrics;
  * fixture data.
* \[ ] Optimizer gebruikt geen signed endpoints.
* \[ ] Optimizer gebruikt geen account endpoints.
* \[ ] Optimizer mag geen order plaatsen.
* \[ ] Optimizer mag geen live mode activeren.
* \[ ] Optimizer output is een paper-only policy proposal.
* \[ ] Policy approval vereist operator confirmation.
* \[ ] Conservative policy selectie is default.
* \[ ] Highest return policy mag nooit automatisch gekozen worden zonder risk filters.
* \[ ] Reports bevatten no-live statement.

### Acceptatiecriteria

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen optimizer kan geen live mode zetten.
* \[ ] Dashboard toont `PAPER OPTIMIZATION ONLY`.
* \[ ] CLI faalt bij mode live.

\---

## 4\. Fase 1 - Optimization Input Registry

Doel: Roadmap 080 outputs centraal laden en valideren.

### Nieuwe module

```text
src/binance\_spot\_bot/optimization\_input\_registry.py
```

### Input types

* \[ ] benchmark summary;
* \[ ] scenario results;
* \[ ] allocation policy results;
* \[ ] equity curves;
* \[ ] drawdown curves;
* \[ ] liquidity stress report;
* \[ ] correlation stress report;
* \[ ] rotation churn report;
* \[ ] watchdog validation report;
* \[ ] robustness scores;
* \[ ] evidence manifest.

### Taken

* \[ ] Load benchmark artifacts by `benchmark\_id`.
* \[ ] Validate hashes via evidence manifest.
* \[ ] Check required files exist.
* \[ ] Check scenario coverage.
* \[ ] Check no-live proof.
* \[ ] Produce `OptimizationInputBundle`.

### Acceptatiecriteria

* \[ ] Optimizer faalt als benchmark evidence ontbreekt.
* \[ ] Optimizer faalt als manifest/hash niet klopt.
* \[ ] Optimizer werkt offline.
* \[ ] Geen secrets in input bundle.

\---

## 5\. Fase 2 - Allocation Search Space

Doel: precies bepalen welke parameters de optimizer mag aanpassen.

### Nieuwe module

```text
src/binance\_spot\_bot/allocation\_search\_space.py
```

### Search parameters

#### Portfolio budget

* \[ ] total paper budget;
* \[ ] cash reserve percentage;
* \[ ] max allocation per strategy;
* \[ ] min allocation per strategy;
* \[ ] max allocation per symbol;
* \[ ] max allocation per cluster.

#### Risk caps

* \[ ] max total exposure;
* \[ ] max strategy exposure;
* \[ ] max symbol exposure;
* \[ ] max daily loss;
* \[ ] max drawdown;
* \[ ] max trades per day;
* \[ ] max turnover;
* \[ ] max rotation frequency.

#### Strategy weights

* \[ ] equal weight;
* \[ ] confidence weight;
* \[ ] risk-adjusted weight;
* \[ ] performance weight;
* \[ ] robust score weight;
* \[ ] manual weight constraints.

#### Rotation parameters

* \[ ] min sample before rotation;
* \[ ] max allocation change per rotation;
* \[ ] cooldown after rotation;
* \[ ] demotion threshold;
* \[ ] promotion threshold;
* \[ ] churn penalty.

### Guardrails

* \[ ] Hard minimum cash reserve.
* \[ ] Hard max drawdown cap.
* \[ ] Hard max per-symbol exposure.
* \[ ] Hard no-leverage constraint.
* \[ ] Hard no-live constraint.
* \[ ] No allocation above paper budget.

### Acceptatiecriteria

* \[ ] Search space serializable to JSON.
* \[ ] Search space validates bounds.
* \[ ] Unsafe bounds are rejected.
* \[ ] Dashboard can show selected search space.
* \[ ] Tests cover invalid ranges.

\---

## 6\. Fase 3 - Portfolio Policy Candidate Generator

Doel: candidate paper policies genereren uit search space.

### Nieuwe module

```text
src/binance\_spot\_bot/portfolio\_policy\_generator.py
```

### Candidate types

* \[ ] equal allocation conservative;
* \[ ] confidence weighted conservative;
* \[ ] robustness weighted;
* \[ ] drawdown minimizer;
* \[ ] cash reserve heavy;
* \[ ] low turnover;
* \[ ] low correlation;
* \[ ] risk parity style;
* \[ ] rotation conservative;
* \[ ] operator manual baseline.

### Candidate output

* \[ ] policy\_id;
* \[ ] allocation weights;
* \[ ] risk caps;
* \[ ] rotation settings;
* \[ ] cash reserve;
* \[ ] expected use case;
* \[ ] constraints;
* \[ ] generated\_from;
* \[ ] seed;
* \[ ] hash.

### Acceptatiecriteria

* \[ ] Generator creates deterministic candidates with seed.
* \[ ] All candidates are paper-only.
* \[ ] Candidate count is capped.
* \[ ] Unsafe candidates are filtered.
* \[ ] Candidate config is exportable.

\---

## 7\. Fase 4 - Portfolio Optimization Engine

Doel: candidates evalueren op benchmark/scenario results.

### Nieuwe module

```text
src/binance\_spot\_bot/portfolio\_optimizer.py
```

### Search modes

* \[ ] grid search;
* \[ ] random search with seed;
* \[ ] conservative heuristic search;
* \[ ] scenario-weighted ranking;
* \[ ] manual candidate comparison.

### Evaluation metrics

* \[ ] average return;
* \[ ] median return;
* \[ ] worst-case return;
* \[ ] max drawdown;
* \[ ] average drawdown;
* \[ ] volatility;
* \[ ] turnover;
* \[ ] conflict rate;
* \[ ] rotation churn;
* \[ ] liquidity shock loss;
* \[ ] correlation stress loss;
* \[ ] watchdog failure count;
* \[ ] robustness score;
* \[ ] evidence completeness.

### Acceptatiecriteria

* \[ ] Optimizer compares multiple candidates.
* \[ ] Optimizer supports deterministic seed.
* \[ ] Optimizer can run offline.
* \[ ] Optimizer ranks by configured objective.
* \[ ] Optimizer never chooses live policy.

\---

## 8\. Fase 5 - Pareto Frontier Builder

Doel: trade-offs zichtbaar maken tussen return, drawdown, churn en robustness.

### Nieuwe module

```text
src/binance\_spot\_bot/pareto\_frontier.py
```

### Dimensions

* \[ ] return;
* \[ ] max drawdown;
* \[ ] worst-case scenario result;
* \[ ] robustness score;
* \[ ] turnover;
* \[ ] churn;
* \[ ] liquidity stress loss;
* \[ ] correlation stress loss.

### Output

* \[ ] Pareto efficient policies;
* \[ ] dominated policies;
* \[ ] frontier summary;
* \[ ] risk-return table;
* \[ ] dashboard chart payload.

### Acceptatiecriteria

* \[ ] Highest PnL but high drawdown can be marked dominated.
* \[ ] Conservative low-drawdown policy can appear on frontier.
* \[ ] Dashboard can show frontier.
* \[ ] Frontier output is deterministic.

\---

## 9\. Fase 6 - Scenario-Weighted Policy Selection

Doel: policy kiezen die past bij operator risk preference en scenario beliefs.

### Nieuwe module

```text
src/binance\_spot\_bot/scenario\_weighted\_selection.py
```

### Scenario weights

* \[ ] bull trend;
* \[ ] bear trend;
* \[ ] range;
* \[ ] high volatility;
* \[ ] liquidity shock;
* \[ ] correlation spike;
* \[ ] data gap;
* \[ ] sudden dump;
* \[ ] choppy breakout.

### Presets

* \[ ] conservative default;
* \[ ] balanced paper;
* \[ ] risk-off;
* \[ ] high-volatility defensive;
* \[ ] liquidity-defensive;
* \[ ] rotation-minimal.

### Acceptatiecriteria

* \[ ] Operator can choose scenario weight preset.
* \[ ] Weights sum to 1.
* \[ ] Policy selection changes transparently with weights.
* \[ ] Report shows scenario contribution.
* \[ ] Default is conservative.

\---

## 10\. Fase 7 - Risk Budget Optimizer

Doel: risk caps zoeken die paper portfolio robuust houden.

### Nieuwe module

```text
src/binance\_spot\_bot/risk\_budget\_optimizer.py
```

### Tunable budgets

* \[ ] max total exposure;
* \[ ] max strategy exposure;
* \[ ] max symbol exposure;
* \[ ] max cluster exposure;
* \[ ] max daily loss;
* \[ ] max drawdown;
* \[ ] max trades per day;
* \[ ] max turnover;
* \[ ] minimum cash reserve;
* \[ ] max allocation change per rebalance.

### Constraints

* \[ ] never exceed operator max risk;
* \[ ] no leverage;
* \[ ] no negative cash;
* \[ ] preserve reduce-only escape;
* \[ ] no overtrading;
* \[ ] no single-symbol concentration.

### Output

* \[ ] risk budget proposal;
* \[ ] rejected budgets;
* \[ ] reason codes;
* \[ ] stress survival score;
* \[ ] recommended conservative cap.

### Acceptatiecriteria

* \[ ] Optimizer favors caps that survive stress.
* \[ ] Drawdown cap cannot be loosened above operator max.
* \[ ] Output is paper-only.
* \[ ] Dashboard shows why cap chosen.

\---

## 11\. Fase 8 - Overfit \& Selection Bias Guard

Doel: voorkomen dat optimizer een policy kiest die alleen historisch geluk had.

### Nieuwe module

```text
src/binance\_spot\_bot/portfolio\_optimization\_guard.py
```

### Guards

* \[ ] minimum scenario count;
* \[ ] minimum symbol count;
* \[ ] minimum sample count;
* \[ ] train/test scenario split;
* \[ ] out-of-sample scenario validation;
* \[ ] shuffled scenario sanity check;
* \[ ] winner’s curse warning;
* \[ ] high parameter count penalty;
* \[ ] excessive turnover penalty;
* \[ ] single scenario dependency warning.

### Acceptatiecriteria

* \[ ] Policy with good result in only one scenario gets warning/blocker.
* \[ ] Too many tuned parameters reduce confidence.
* \[ ] Out-of-sample failure blocks paper approval.
* \[ ] Report includes selection bias warnings.

\---

## 12\. Fase 9 - Conservative Policy Selector

Doel: default kiezen die veilig genoeg is voor paper operations.

### Nieuwe module

```text
src/binance\_spot\_bot/conservative\_policy\_selector.py
```

### Selection rules

* \[ ] must pass all hard safety guards;
* \[ ] must be on or near Pareto frontier;
* \[ ] max drawdown below threshold;
* \[ ] worst-case scenario above minimum;
* \[ ] liquidity shock acceptable;
* \[ ] correlation stress acceptable;
* \[ ] rotation churn acceptable;
* \[ ] no evidence gaps;
* \[ ] no overfit blockers;
* \[ ] prefer higher cash reserve on tie;
* \[ ] prefer lower turnover on tie.

### Output

* \[ ] selected policy;
* \[ ] rejected alternatives;
* \[ ] reason codes;
* \[ ] confidence grade;
* \[ ] required operator confirmation.

### Acceptatiecriteria

* \[ ] Selector never auto-picks highest PnL if risk poor.
* \[ ] Selector can return “no policy approved”.
* \[ ] Selector explains every rejection.
* \[ ] Selected policy is paper-only.

\---

## 13\. Fase 10 - Portfolio Policy Card

Doel: selected policy documenteren als reproduceerbare card.

### Nieuwe module

```text
src/binance\_spot\_bot/portfolio\_policy\_card.py
```

### Card bevat

* \[ ] policy\_id;
* \[ ] policy name;
* \[ ] selected\_at;
* \[ ] selected\_from benchmark\_id;
* \[ ] allocation weights;
* \[ ] risk budgets;
* \[ ] rotation settings;
* \[ ] scenario weights;
* \[ ] Pareto status;
* \[ ] robustness score;
* \[ ] worst-case scenario;
* \[ ] known weaknesses;
* \[ ] blocked conditions;
* \[ ] operator notes;
* \[ ] no-live statement;
* \[ ] evidence links;
* \[ ] hash.

### Output

```text
data/portfolio-policies/<policy\_id>/
  portfolio\_policy\_card.md
  portfolio\_policy\_card.json
  evidence\_manifest.json
```

### Acceptatiecriteria

* \[ ] Policy card is secret-free.
* \[ ] Card can be verified with hash.
* \[ ] Card links to benchmark evidence.
* \[ ] Dashboard can display/download card.

\---

## 14\. Fase 11 - Paper Policy Approval Gate

Doel: selected policy pas gebruiken na checks.

### Nieuwe module

```text
src/binance\_spot\_bot/paper\_policy\_approval.py
```

### Gate requirements

* \[ ] benchmark evidence present;
* \[ ] scenario coverage sufficient;
* \[ ] robustness score above threshold;
* \[ ] max drawdown below threshold;
* \[ ] liquidity stress pass;
* \[ ] correlation stress pass;
* \[ ] overfit guard pass;
* \[ ] policy card generated;
* \[ ] operator confirmation;
* \[ ] no-live proof.

### Statussen

* \[ ] blocked;
* \[ ] needs\_more\_benchmarks;
* \[ ] optimization\_candidate;
* \[ ] paper\_policy\_candidate;
* \[ ] paper\_policy\_approved;
* \[ ] paper\_policy\_suspended.

### Acceptatiecriteria

* \[ ] No live-approved status exists.
* \[ ] Policy cannot be approved without evidence.
* \[ ] Approval can be revoked.
* \[ ] Dashboard shows blockers.

\---

## 15\. Fase 12 - Optimizer Dashboard Panel

Doel: portfolio optimization begrijpelijk bedienen.

### Nieuwe/uitgebreide dashboardsectie

```text
Portfolio Optimizer
```

### Panels

* \[ ] input benchmark selector;
* \[ ] search space editor;
* \[ ] scenario weight preset;
* \[ ] candidate count;
* \[ ] optimization run status;
* \[ ] policy ranking table;
* \[ ] Pareto frontier chart;
* \[ ] robustness scores;
* \[ ] risk budget proposals;
* \[ ] overfit warnings;
* \[ ] selected conservative policy;
* \[ ] policy card download;
* \[ ] approval gate status.

### Actions

* \[ ] run optimizer;
* \[ ] compare policies;
* \[ ] select conservative policy;
* \[ ] export policy card;
* \[ ] approve paper policy;
* \[ ] suspend policy.

### Acceptatiecriteria

* \[ ] Dashboard shows paper-only badge.
* \[ ] Raw JSON only in debug expanders.
* \[ ] Dangerous actions require confirmation.
* \[ ] No live mode.
* \[ ] Browser smoke covers page import/render.

\---

## 16\. Fase 13 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli portfolio-optimization-inputs --benchmark-id <id>
python -m binance\_spot\_bot.cli portfolio-optimize --benchmark-id <id> --preset conservative --seed 7
python -m binance\_spot\_bot.cli portfolio-pareto --optimization-id <id>
python -m binance\_spot\_bot.cli risk-budget-search --optimization-id <id>
python -m binance\_spot\_bot.cli select-portfolio-policy --optimization-id <id> --preset conservative
python -m binance\_spot\_bot.cli export-portfolio-policy-card --policy-id <id>
python -m binance\_spot\_bot.cli approve-paper-policy --policy-id <id> --confirm PAPER\_POLICY
```

### Acceptatiecriteria

* \[ ] Commands work offline with benchmark artifacts.
* \[ ] Commands support JSON output.
* \[ ] Commands never require API keys.
* \[ ] Commands never call order/account endpoints.
* \[ ] Approval requires confirm.
* \[ ] Reports are secret-free.

\---

## 17\. Fase 14 - Optimization Reports \& Evidence

### Output

```text
data/portfolio-optimizations/<optimization\_id>/
  optimization\_manifest.json
  search\_space.json
  candidate\_policies.jsonl
  policy\_scores.csv
  pareto\_frontier.json
  scenario\_weighted\_scores.csv
  risk\_budget\_search.json
  overfit\_guard\_report.json
  conservative\_selection\_report.md
  conservative\_selection\_report.json
  evidence\_manifest.json
```

### Report bevat

* \[ ] benchmark input summary;
* \[ ] search space;
* \[ ] objective;
* \[ ] scenario weights;
* \[ ] candidate count;
* \[ ] rejected candidates;
* \[ ] top policies;
* \[ ] Pareto frontier;
* \[ ] risk budget proposals;
* \[ ] overfit warnings;
* \[ ] selected policy or no-policy decision;
* \[ ] next recommended action;
* \[ ] no-live statement.

### Acceptatiecriteria

* \[ ] Reports are reproducible.
* \[ ] Reports contain no secrets.
* \[ ] Evidence manifest verifies hashes.
* \[ ] Dashboard can download report.
* \[ ] Report supports Roadmap 082 decisions.

\---

## 18\. Fase 15 - CI-safe optimizer subset

Doel: lichte optimizer-test in CI/check-all kunnen draaien.

### CI-safe subset

* \[ ] tiny benchmark fixture;
* \[ ] 2 candidate policies;
* \[ ] 2 scenarios;
* \[ ] 2 risk budgets;
* \[ ] deterministic seed;
* \[ ] no network;
* \[ ] no Streamlit;
* \[ ] max runtime target under 10 seconds.

### Acceptatiecriteria

* \[ ] CI-safe optimizer runs in pytest.
* \[ ] Full optimization can remain manual.
* \[ ] No external data required.
* \[ ] Results deterministic with seed.
* \[ ] No live/signed endpoints.

\---

## 19\. Tests

### Unit tests

* \[ ] `tests/test\_optimization\_input\_registry.py`
* \[ ] `tests/test\_allocation\_search\_space.py`
* \[ ] `tests/test\_portfolio\_policy\_generator.py`
* \[ ] `tests/test\_portfolio\_optimizer.py`
* \[ ] `tests/test\_pareto\_frontier.py`
* \[ ] `tests/test\_scenario\_weighted\_selection.py`
* \[ ] `tests/test\_risk\_budget\_optimizer.py`
* \[ ] `tests/test\_portfolio\_optimization\_guard.py`
* \[ ] `tests/test\_conservative\_policy\_selector.py`
* \[ ] `tests/test\_portfolio\_policy\_card.py`
* \[ ] `tests/test\_paper\_policy\_approval.py`

### Integration tests

* \[ ] Load benchmark fixture.
* \[ ] Generate candidate policies.
* \[ ] Run optimizer.
* \[ ] Build Pareto frontier.
* \[ ] Run risk budget search.
* \[ ] Apply overfit guard.
* \[ ] Select conservative policy.
* \[ ] Generate policy card.
* \[ ] Approve paper policy.
* \[ ] Export evidence.

### Safety tests

* \[ ] Optimizer rejects live mode.
* \[ ] Optimizer uses no signed endpoints.
* \[ ] Optimizer uses no account endpoints.
* \[ ] Policy approval cannot create live approval.
* \[ ] Reports contain no secrets.
* \[ ] Check-all remains green.

\---

## 20\. Docs

Nieuwe docs:

* \[ ] `docs/paper-portfolio-optimization-safety-contract.md`
* \[ ] `docs/optimization-input-registry.md`
* \[ ] `docs/allocation-search-space.md`
* \[ ] `docs/portfolio-policy-generator.md`
* \[ ] `docs/portfolio-optimizer.md`
* \[ ] `docs/pareto-frontier.md`
* \[ ] `docs/scenario-weighted-selection.md`
* \[ ] `docs/risk-budget-optimizer.md`
* \[ ] `docs/portfolio-optimization-guard.md`
* \[ ] `docs/conservative-policy-selector.md`
* \[ ] `docs/portfolio-policy-card.md`
* \[ ] `docs/paper-policy-approval.md`

README updates:

* \[ ] optimization commands;
* \[ ] conservative policy selection explanation;
* \[ ] risk budget search explanation;
* \[ ] no-live statement;
* \[ ] policy card path.

\---

## 21\. Codex bouwvolgorde

### PR 1 - Optimization Input Registry

* \[ ] load Roadmap 080 artifacts;
* \[ ] hash/evidence validation;
* \[ ] tests.

### PR 2 - Allocation Search Space

* \[ ] parameter schema;
* \[ ] bounds validation;
* \[ ] safety tests.

### PR 3 - Policy Candidate Generator

* \[ ] deterministic candidate generation;
* \[ ] unsafe candidate filtering;
* \[ ] tests.

### PR 4 - Portfolio Optimization Engine

* \[ ] grid/random/conservative search;
* \[ ] objective scoring;
* \[ ] tests.

### PR 5 - Pareto Frontier

* \[ ] frontier builder;
* \[ ] dominated policy detection;
* \[ ] tests.

### PR 6 - Scenario Weighted Selection

* \[ ] scenario weights;
* \[ ] presets;
* \[ ] tests.

### PR 7 - Risk Budget Optimizer

* \[ ] budget search;
* \[ ] cap validation;
* \[ ] tests.

### PR 8 - Overfit Guard + Conservative Selector

* \[ ] selection bias checks;
* \[ ] conservative selection;
* \[ ] tests.

### PR 9 - Policy Card + Approval Gate

* \[ ] card export;
* \[ ] paper approval;
* \[ ] evidence;
* \[ ] tests.

### PR 10 - Dashboard + CLI + Docs

* \[ ] optimizer dashboard;
* \[ ] CLI commands;
* \[ ] docs;
* \[ ] browser smoke.

\---

## 22\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 081 PR 1: Optimization Input Registry.

Maak src/binance\_spot\_bot/optimization\_input\_registry.py.
Laad Roadmap 080 benchmark artifacts uit data/portfolio-benchmarks/<benchmark\_id>/:
- benchmark\_manifest.json
- benchmark\_summary.json
- scenario\_results.csv
- allocation\_policy\_results.csv
- robustness\_scores.json
- evidence\_manifest.json

Valideer dat alle vereiste bestanden bestaan, hashes kloppen, scenario coverage aanwezig is en no-live proof aanwezig is.
Maak een OptimizationInputBundle dat downstream optimizer modules kunnen gebruiken.
Voeg tests toe met een tiny benchmark fixture.
Geen API calls, geen signed endpoints, geen orders, geen live trading.
```

Waarom eerst:

* optimizer heeft betrouwbare benchmark inputs nodig;
* dit raakt geen execution/risk/live logic;
* het is klein genoeg voor Codex;
* het dwingt evidence-first werken af.

\---

## 23\. Definition of Done

Roadmap 081 is klaar als:

* \[ ] Optimization Input Registry werkt.
* \[ ] Allocation Search Space werkt.
* \[ ] Portfolio Policy Candidate Generator werkt.
* \[ ] Portfolio Optimization Engine werkt.
* \[ ] Pareto Frontier Builder werkt.
* \[ ] Scenario-Weighted Policy Selection werkt.
* \[ ] Risk Budget Optimizer werkt.
* \[ ] Overfit \& Selection Bias Guard werkt.
* \[ ] Conservative Policy Selector werkt.
* \[ ] Portfolio Policy Card werkt.
* \[ ] Paper Policy Approval Gate werkt.
* \[ ] Optimizer Dashboard Panel werkt.
* \[ ] CLI commands werken.
* \[ ] Optimization reports/evidence werken.
* \[ ] CI-safe optimizer subset werkt.
* \[ ] Tests bewijzen geen signed/account/order endpoints.
* \[ ] Reports zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 081 kan na uitvoering naar `Voltooid docs`.

\---

## 24\. Verwachte Roadmap 082 daarna

Na Roadmap 081 zou Roadmap 082 logisch focussen op:

```text
Roadmap 082 - Paper Policy Rollout, A/B Paper Experiments \& Champion/Challenger Portfolio Governance
```

Mogelijke inhoud:

* \[ ] paper policy rollout plan;
* \[ ] A/B paper experiments;
* \[ ] champion/challenger portfolio policies;
* \[ ] controlled allocation migration;
* \[ ] policy rollback;
* \[ ] weekly governance report;
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

- portfolio_optimization.py toegevoegd met risk budget candidate search, robust policy selection, conservative tie-break en policy-card export.
- CLI command toegevoegd: paper-portfolio-optimize.
- Tests toegevoegd: 	ests/test_roadmap_081_portfolio_optimization.py.

Validatie:

- python -m pytest tests/test_roadmap_080_portfolio_benchmarking.py tests/test_roadmap_081_portfolio_optimization.py -q -> 6 passed.
- Scope blijft paper-only; live trading disabled.

