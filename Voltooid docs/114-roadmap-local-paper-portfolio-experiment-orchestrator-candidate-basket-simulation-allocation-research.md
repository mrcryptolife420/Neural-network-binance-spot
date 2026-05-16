# Roadmap 114 - Local Paper Portfolio Experiment Orchestrator, Candidate Basket Simulation \& Allocation Research

Status: Voltooid / Gevalideerd  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/114-roadmap-local-paper-portfolio-experiment-orchestrator-candidate-basket-simulation-allocation-research.md
```

## Samenvatting

Roadmap 112 maakt een lokale Market Intelligence Workbench voor Binance Spot public data: symbol universe, watchlist scanner, market metrics, rankings, scanner presets en multi-symbol paper analytics.

Roadmap 113 zet scanner-output om naar paper-only Strategy Lab experimenten: scanner-to-paper candidates, experiment queues, strategy/model/risk comparisons, candidate scorecards en portfolio candidate research.

Roadmap 114 is de logische volgende stap: **maak van losse research candidates een paper-only portfolio research lab**. Niet één symbool of één strategie vergelijken, maar candidate baskets bouwen, allocaties simuleren, portfolio-level drawdown/volatility/risk budget onderzoeken, scenario stress tests draaien en paper-only allocation recommendations als research-output maken.

De kern:

```text
Strategy Lab candidate scorecards
→ candidate basket builder
→ allocation constraint engine
→ paper portfolio experiment orchestrator
→ basket simulation
→ scenario stress tests
→ allocation research scorecards
→ Dashboard V2 Portfolio Lab
→ evidence bundle
```

Live trading blijft volledig buiten scope. Geen live mode, geen signed real-order endpoints, geen echte account workflows, geen echte portfolio allocaties en geen financieel advies. Alle outputs zijn local-only, paper-only research.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 114`, `114-roadmap`, `Local Paper Portfolio Experiment Orchestrator`, `Candidate Basket Simulation`, `Allocation Research` en `portfolio experiment`.
* \[x] Geen bestaande Roadmap 114 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 113 is lokaal aangemaakt als Local Multi-Symbol Strategy Lab, Scanner-to-Paper Experiment Queues \& Portfolio Candidate Research.

### Codebasecontrole

Breed bekeken met focus op Binance/public data, market data, runtime/paper simulation, Strategy Lab vervolg, Dashboard V2, CLI, check-all en safety:

* \[x] `src/binance\_spot\_bot/binance.py`
* \[x] `src/binance\_spot\_bot/market\_data\_source.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/ui/page\_registry.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] roadmaplijn 104-113.

### Belangrijke bestaande basis

De codebase heeft nu of krijgt via Roadmap 112/113:

* \[x] Binance public market endpoints voor exchange info, klines, UI klines, order book, 24hr ticker, rolling ticker, avg price, recent trades, agg trades en book ticker.
* \[x] Signed/account/order endpoints bestaan in dezelfde adapter, dus portfolio research moet deze hard blijven blokkeren.
* \[x] Market data sources voor static candles, demo replay, REST polling en WebSocket-wrapper met veilige fallback.
* \[x] Runtime modes beperkt tot `demo`, `paper` en `testnet-readiness`.
* \[x] Runtime snapshots bevatten candles, signals, fills, equity, market data, top of book, data quality, sessions, active model, alerts, paper account, readiness, demo info en reconciliation.
* \[x] Check-all forceert safe env:

  * `LIVE\_TRADING\_ENABLED=false`;
  * `KILL\_SWITCH=true`;
  * `PYTHONPATH=src`.
* \[x] Roadmap 113 plant Strategy Lab scorecards, experiment queues, comparison reports, portfolio candidate research en research guards.
* \[x] Roadmap 110/111 plannen Dashboard V2 workspaces, widget registry, extension packs, analytics presets en local-only customization.

### Belangrijkste gat na Roadmap 113

Roadmap 113 levert candidate scorecards en portfolio candidate research, maar nog geen echte portfolio-level experimentorchestratie:

* \[ ] Geen candidate basket builder.
* \[ ] Geen portfolio allocation constraints.
* \[ ] Geen paper portfolio basket simulation.
* \[ ] Geen basket-level equity curve.
* \[ ] Geen portfolio-level drawdown/volatility/risk budget analyse.
* \[ ] Geen scenario stress tests op baskets.
* \[ ] Geen candidate overlap/correlation proxy.
* \[ ] Geen allocation search over candidate baskets.
* \[ ] Geen portfolio research scorecard.
* \[ ] Geen paper-only allocation governance.
* \[ ] Geen Portfolio Lab Dashboard V2 workbench.
* \[ ] Geen portfolio experiment evidence bundle.

Roadmap 114 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 114

Maak een lokaal paper-only portfolio experiment lab:

```text
Candidate scorecards
→ candidate baskets
→ allocation constraints
→ paper portfolio simulations
→ scenario stress tests
→ allocation research
→ portfolio scorecards
→ evidence bundle
```

Na Roadmap 114 moet de operator:

* \[ ] candidate baskets kunnen bouwen uit Strategy Lab scorecards;
* \[ ] allocatieconstraints kunnen instellen;
* \[ ] paper portfolio simulations kunnen draaien over meerdere symbolen/strategieën;
* \[ ] basket equity curves kunnen vergelijken;
* \[ ] drawdown, volatility, exposure en risk budget usage kunnen zien;
* \[ ] stress scenarios kunnen draaien;
* \[ ] allocation candidates kunnen scorecarden;
* \[ ] portfolio research reports kunnen exporteren;
* \[ ] no-live/no-advice/no-real-allocation proof kunnen verifiëren;
* \[ ] alles local-only en paper-only houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen Binance scanner opnieuw bouwen.
* \[ ] Geen Strategy Lab experiment runner opnieuw bouwen.
* \[ ] Geen Dashboard V2 workspace systeem opnieuw bouwen.
* \[ ] Geen trading runtime core refactor.
* \[ ] Geen modeltraining pipeline opnieuw bouwen.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed order endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen echte portfolio allocaties.
* \[ ] Geen echte Binance orders.
* \[ ] Geen auto-trading vanuit basket rankings.
* \[ ] Geen financieel advies.
* \[ ] Geen cloud portfolio platform.
* \[ ] Geen remote telemetry.
* \[ ] Geen API keys vereisen.
* \[ ] Geen allocation output met “koop/verkoop” taal.

Wel doen:

* \[ ] candidate basket schema;
* \[ ] allocation constraint engine;
* \[ ] paper portfolio orchestrator;
* \[ ] basket simulation;
* \[ ] portfolio risk analytics;
* \[ ] stress tests;
* \[ ] allocation research scorecards;
* \[ ] Dashboard V2 Portfolio Lab;
* \[ ] CLI/reports/evidence/tests;
* \[ ] no-live/no-advice proof.

\---

## 3\. Fase 0 - Paper Portfolio Research Safety Contract

Nieuw docbestand:

```text
docs/portfolio-lab/paper-portfolio-research-safety-contract.md
```

Regels:

* \[ ] Portfolio Lab is local-only.
* \[ ] Simulaties zijn paper-only.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed order endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen echte orders.
* \[ ] Geen echte portfolio allocatie.
* \[ ] Geen API keys vereist.
* \[ ] Candidate baskets zijn research inputs.
* \[ ] Output is geen financieel advies.
* \[ ] Allocation scorecards mogen geen “buy/sell” of “real allocation” claim bevatten.
* \[ ] Orchestrator gebruikt safe env:

  * `LIVE\_TRADING\_ENABLED=false`;
  * `KILL\_SWITCH=true`.
* \[ ] Reports/evidence zijn secret-free.
* \[ ] Elke run bevat `live\_trading\_enabled=False`.
* \[ ] Elke report bevat `paper\_only\_research\_statement`.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen live/signed/account/order endpoints geblokkeerd zijn.
* \[ ] Tests bewijzen allocation output geen buy/sell advies bevat.
* \[ ] Tests bewijzen runner zonder API keys werkt.
* \[ ] Tests bewijzen reports secret-free zijn.

\---

## 4\. Fase 1 - Portfolio Candidate Basket Schema

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/candidate\_basket.py
```

Inputs:

* \[ ] Strategy Lab candidate scorecards.
* \[ ] Strategy Lab comparison reports.
* \[ ] scanner ranking reports.
* \[ ] data quality/research guard reports.
* \[ ] operator selected symbols.
* \[ ] allow/deny list.

Dataclasses:

* \[ ] `PortfolioCandidateBasket`
* \[ ] `PortfolioBasketItem`
* \[ ] `PortfolioBasketSource`
* \[ ] `PortfolioBasketValidationResult`
* \[ ] `PortfolioBasketBuildReport`

Basket item fields:

* \[ ] item\_id;
* \[ ] symbol;
* \[ ] strategy\_id;
* \[ ] model\_alias;
* \[ ] risk\_preset;
* \[ ] source\_candidate\_id;
* \[ ] source\_scorecard\_id;
* \[ ] paper\_score;
* \[ ] data\_quality\_score;
* \[ ] market\_quality\_score;
* \[ ] warnings;
* \[ ] blocked\_reason optional;
* \[ ] paper\_only=true;
* \[ ] live\_trading\_enabled=false.

Basket fields:

* \[ ] basket\_id;
* \[ ] name;
* \[ ] description;
* \[ ] source\_queue\_id;
* \[ ] source\_scanner\_run\_id;
* \[ ] items;
* \[ ] max\_items;
* \[ ] quote\_asset;
* \[ ] created\_at\_ms;
* \[ ] no\_live\_statement;
* \[ ] no\_financial\_advice\_statement;
* \[ ] paper\_only\_research\_statement.

Acceptatiecriteria:

* \[ ] Basket schema is JSON-serializable.
* \[ ] Duplicate symbol/strategy/model combo detected.
* \[ ] Blocked candidates excluded unless explicitly included as disabled.
* \[ ] Advice wording scan passes.
* \[ ] Tests use fixture scorecards.

\---

## 5\. Fase 2 - Basket Builder \& Filters

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/basket\_builder.py
```

Filters:

* \[ ] max basket size;
* \[ ] min paper score;
* \[ ] min data quality score;
* \[ ] max drawdown;
* \[ ] max spread warning threshold;
* \[ ] max block rate;
* \[ ] min trades;
* \[ ] quote asset;
* \[ ] include/exclude symbols;
* \[ ] include/exclude strategy IDs;
* \[ ] include/exclude model aliases;
* \[ ] volatility bucket;
* \[ ] diversification bucket;
* \[ ] require research guard pass.

Build modes:

* \[ ] top\_score;
* \[ ] diversified;
* \[ ] conservative;
* \[ ] high\_volume;
* \[ ] low\_drawdown;
* \[ ] model\_balanced;
* \[ ] strategy\_balanced;
* \[ ] custom.

Acceptatiecriteria:

* \[ ] Builder werkt op Strategy Lab fixtures.
* \[ ] Filters zijn deterministic.
* \[ ] Unsafe/blocked candidates worden niet actief.
* \[ ] Missing fields geven warnings.
* \[ ] Tests dekken build modes.

\---

## 6\. Fase 3 - Allocation Constraint Engine

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/allocation\_constraints.py
```

Constraints:

* \[ ] total allocation = 100%;
* \[ ] max allocation per symbol;
* \[ ] min allocation per selected item;
* \[ ] max symbols;
* \[ ] max strategies per basket;
* \[ ] max model aliases;
* \[ ] max exposure per quote asset;
* \[ ] max volatility bucket exposure;
* \[ ] max drawdown candidate exposure;
* \[ ] max blocked/warning candidates = 0 by default;
* \[ ] minimum data quality score;
* \[ ] risk budget cap;
* \[ ] rebalance frequency paper-only.

Dataclasses:

* \[ ] `AllocationConstraints`
* \[ ] `AllocationConstraintViolation`
* \[ ] `AllocationConstraintReport`

Acceptatiecriteria:

* \[ ] Valid allocation passes.
* \[ ] Sum not equal 100% fails/warns according tolerance.
* \[ ] Overexposure detected.
* \[ ] Blocked candidates force fail.
* \[ ] Tests cover constraints.

\---

## 7\. Fase 4 - Allocation Proposal Generator

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/allocation\_proposals.py
```

Proposal modes:

* \[ ] equal\_weight;
* \[ ] score\_weighted;
* \[ ] inverse\_drawdown\_weighted;
* \[ ] inverse\_volatility\_weighted;
* \[ ] liquidity\_adjusted;
* \[ ] risk\_budget\_balanced;
* \[ ] conservative\_research;
* \[ ] custom\_manual.

Dataclasses:

* \[ ] `PortfolioAllocationProposal`
* \[ ] `PortfolioAllocationItem`
* \[ ] `PortfolioAllocationProposalReport`

Rules:

* \[ ] proposal is paper-only research;
* \[ ] no real allocation;
* \[ ] no buy/sell wording;
* \[ ] constraints must pass before active simulation;
* \[ ] output contains warnings and assumptions.

Acceptatiecriteria:

* \[ ] Proposal deterministic.
* \[ ] Constraint violations included.
* \[ ] Proposal cannot include blocked candidate.
* \[ ] Advice wording scan passes.
* \[ ] Tests cover all modes.

\---

## 8\. Fase 5 - Paper Portfolio Experiment Orchestrator

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/portfolio\_experiment\_orchestrator.py
```

Doel: meerdere candidate/strategy jobs combineren tot één paper portfolio experiment.

Input:

* \[ ] candidate basket;
* \[ ] allocation proposal;
* \[ ] cached candles/result series;
* \[ ] paper strategy results from Roadmap 113;
* \[ ] scenario config;
* \[ ] rebalance config;
* \[ ] constraints.

Output:

* \[ ] `PortfolioExperimentRun`
* \[ ] `PortfolioExperimentStep`
* \[ ] `PortfolioExperimentResult`
* \[ ] `PortfolioExperimentReport`

Run fields:

* \[ ] run\_id;
* \[ ] basket\_id;
* \[ ] allocation\_id;
* \[ ] start\_ms;
* \[ ] end\_ms;
* \[ ] status;
* \[ ] mode=`paper`;
* \[ ] starting\_quote;
* \[ ] rebalance\_policy;
* \[ ] no\_live\_statement;
* \[ ] paper\_only\_research\_statement;
* \[ ] live\_trading\_enabled=false.

Acceptatiecriteria:

* \[ ] Orchestrator runs on fixture results/candles.
* \[ ] Orchestrator works without API keys.
* \[ ] Orchestrator blocks live/signed/account/order paths.
* \[ ] Orchestrator exports JSON + Markdown report.
* \[ ] Tests cover completed/blocked/failed runs.

\---

## 9\. Fase 6 - Basket Simulation Engine

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/basket\_simulation.py
```

Simulation outputs:

* \[ ] portfolio equity curve;
* \[ ] per-symbol equity contribution;
* \[ ] per-strategy contribution;
* \[ ] allocation over time;
* \[ ] drawdown series;
* \[ ] volatility estimate;
* \[ ] realized paper PnL;
* \[ ] fees estimate;
* \[ ] turnover estimate;
* \[ ] risk budget usage;
* \[ ] blocked action count;
* \[ ] data quality warnings.

Simulation modes:

* \[ ] static allocation;
* \[ ] periodic paper rebalance;
* \[ ] threshold rebalance paper-only;
* \[ ] no-rebalance baseline;
* \[ ] candidate removal scenario.

Acceptatiecriteria:

* \[ ] Simulation deterministic.
* \[ ] Missing series handled.
* \[ ] Allocation constraints enforced.
* \[ ] No real orders/actions.
* \[ ] Tests use synthetic result series.

\---

## 10\. Fase 7 - Portfolio Risk Analytics

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/portfolio\_risk\_analytics.py
```

Metrics:

* \[ ] portfolio max drawdown;
* \[ ] drawdown duration;
* \[ ] volatility proxy;
* \[ ] return/drawdown ratio;
* \[ ] downside deviation;
* \[ ] concentration score;
* \[ ] exposure by symbol;
* \[ ] exposure by strategy;
* \[ ] exposure by model alias;
* \[ ] exposure by volatility bucket;
* \[ ] data quality weighted exposure;
* \[ ] risk block contribution;
* \[ ] fee drag;
* \[ ] turnover proxy.

Dataclasses:

* \[ ] `PortfolioRiskMetricSet`
* \[ ] `PortfolioRiskAnalyticsReport`

Acceptatiecriteria:

* \[ ] Metrics deterministic.
* \[ ] Empty/short series handled.
* \[ ] Concentration warnings correct.
* \[ ] Reports secret-free.
* \[ ] Tests cover edge cases.

\---

## 11\. Fase 8 - Correlation \& Overlap Proxy

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/correlation\_proxy.py
```

Research-only proxies:

* \[ ] return correlation from cached candles;
* \[ ] co-movement score;
* \[ ] same quote asset overlap;
* \[ ] same base-sector tag optional/local;
* \[ ] shared model/strategy overlap;
* \[ ] simultaneous drawdown overlap;
* \[ ] data gap overlap.

Rules:

* \[ ] Proxy, not statistical guarantee.
* \[ ] Missing data gives unknown/warning.
* \[ ] No financial advice.

Acceptatiecriteria:

* \[ ] Correlation proxy works on fixture candles.
* \[ ] Missing data handled.
* \[ ] Overlap warnings emitted.
* \[ ] Advice wording scan passes.
* \[ ] Tests cover correlated/uncorrelated fixtures.

\---

## 12\. Fase 9 - Scenario Stress Test Engine

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/stress\_tests.py
```

Scenarios:

* \[ ] market drop shock;
* \[ ] high spread shock;
* \[ ] stale data shock;
* \[ ] volatility spike;
* \[ ] top candidate removed;
* \[ ] worst symbol drawdown;
* \[ ] fees doubled;
* \[ ] signal confidence degradation;
* \[ ] risk blocks increase;
* \[ ] liquidity proxy drop;
* \[ ] missing candles for one symbol;
* \[ ] rebalance delay.

Dataclasses:

* \[ ] `PortfolioStressScenario`
* \[ ] `PortfolioStressResult`
* \[ ] `PortfolioStressTestReport`

Acceptatiecriteria:

* \[ ] Stress tests deterministic.
* \[ ] Stress tests do not mutate original results.
* \[ ] Hard scenario warnings included.
* \[ ] Reports are paper-only.
* \[ ] Tests cover scenario application.

\---

## 13\. Fase 10 - Allocation Research Scorecards

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/allocation\_scorecards.py
```

Score dimensions:

* \[ ] paper performance;
* \[ ] drawdown control;
* \[ ] volatility control;
* \[ ] diversification proxy;
* \[ ] concentration penalty;
* \[ ] data quality exposure;
* \[ ] risk block exposure;
* \[ ] stability under stress;
* \[ ] fee/turnover penalty;
* \[ ] reproducibility;
* \[ ] research guard status.

Output:

* \[ ] allocation scorecard JSON;
* \[ ] Markdown summary;
* \[ ] allocation ranking table;
* \[ ] rejected allocations;
* \[ ] warnings and blockers.

Wording rules:

* \[ ] “paper research allocation”.
* \[ ] “candidate allocation”.
* \[ ] No “buy/sell”.
* \[ ] No “real-money allocation”.

Acceptatiecriteria:

* \[ ] Scorecards deterministic.
* \[ ] Stress failures reduce score.
* \[ ] Advice wording scan passes.
* \[ ] Blocked allocation cannot rank first.
* \[ ] Tests cover score computation.

\---

## 14\. Fase 11 - Portfolio Experiment Store

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/portfolio\_experiment\_store.py
```

Storage:

```text
data/portfolio-lab/
  baskets/
  allocations/
  runs/
  simulations/
  stress-tests/
  scorecards/
  reports/
  evidence/
```

Functions:

* \[ ] save basket.
* \[ ] save allocation.
* \[ ] save run.
* \[ ] save simulation.
* \[ ] save stress result.
* \[ ] save scorecard.
* \[ ] list by basket/allocation/date.
* \[ ] export CSV/JSON/Markdown.
* \[ ] verify manifests/hashes.
* \[ ] cleanup old results.

Acceptatiecriteria:

* \[ ] Store is local-only.
* \[ ] Path traversal blocked.
* \[ ] Hash verification works.
* \[ ] Secret redaction works.
* \[ ] Tests use temp dirs.

\---

## 15\. Fase 12 - Portfolio Research Guards

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/portfolio\_research\_guards.py
```

Guards:

* \[ ] too few candidates;
* \[ ] overconcentration;
* \[ ] too many warning candidates;
* \[ ] too much stale data exposure;
* \[ ] high drawdown allocation;
* \[ ] high volatility allocation;
* \[ ] high spread exposure;
* \[ ] insufficient paper trades;
* \[ ] one-symbol dominates score;
* \[ ] one-strategy dominates basket;
* \[ ] correlation proxy too high;
* \[ ] stress test failure;
* \[ ] missing no-live proof;
* \[ ] advice wording violation.

Statuses:

* \[ ] pass;
* \[ ] warn;
* \[ ] block;
* \[ ] unknown.

Acceptatiecriteria:

* \[ ] Guards run on every scorecard.
* \[ ] Missing no-live proof blocks.
* \[ ] Advice wording violation blocks.
* \[ ] Warnings visible in Dashboard V2.
* \[ ] Tests cover each guard.

\---

## 16\. Fase 13 - Portfolio Lab Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/evidence\_bundle.py
```

Bundle bevat:

* \[ ] safety contract.
* \[ ] candidate basket report.
* \[ ] allocation constraints report.
* \[ ] allocation proposal report.
* \[ ] orchestrator report.
* \[ ] basket simulation report.
* \[ ] portfolio risk analytics.
* \[ ] correlation/overlap proxy report.
* \[ ] stress test report.
* \[ ] allocation scorecards.
* \[ ] portfolio research guards.
* \[ ] store manifest.
* \[ ] no-live proof.
* \[ ] no-real-allocation proof.
* \[ ] no-financial-advice proof.
* \[ ] redaction proof.
* \[ ] hashes.

Output:

```text
data/portfolio-lab/evidence/<run\_id>/
  portfolio\_lab\_evidence\_manifest.json
  portfolio\_lab\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle links to Roadmap 113 Strategy Lab evidence.
* \[ ] Dashboard can download bundle.

\---

## 17\. Fase 14 - Dashboard V2 Portfolio Lab Workbench

Nieuwe Dashboard V2 routes:

```text
/portfolio-lab
/portfolio-lab/baskets
/portfolio-lab/allocations
/portfolio-lab/simulations
/portfolio-lab/stress-tests
/portfolio-lab/scorecards
/portfolio-lab/research-guards
/portfolio-lab/evidence
```

Panels:

* \[ ] Strategy Lab result selector.
* \[ ] candidate basket builder.
* \[ ] basket table.
* \[ ] allocation proposal builder.
* \[ ] constraint validation.
* \[ ] simulation run preview.
* \[ ] portfolio equity curve.
* \[ ] drawdown/risk analytics.
* \[ ] correlation/overlap matrix.
* \[ ] stress test panel.
* \[ ] allocation scorecards.
* \[ ] research guard warnings.
* \[ ] evidence export.
* \[ ] no-live/no-advice/no-real-allocation banner.

Acceptatiecriteria:

* \[ ] Portfolio Lab page loads.
* \[ ] Basket builder works from fixture Strategy Lab results.
* \[ ] Allocation preview works.
* \[ ] Simulation results visible.
* \[ ] Browser smoke covers happy path.

\---

## 18\. Fase 15 - Portfolio Lab Widgets \& Workspace Packs

Nieuwe widgets:

* \[ ] `PortfolioBasketBuilderWidget`
* \[ ] `CandidateBasketTableWidget`
* \[ ] `AllocationProposalWidget`
* \[ ] `AllocationConstraintWidget`
* \[ ] `PortfolioSimulationStatusWidget`
* \[ ] `PortfolioEquityCurveWidget`
* \[ ] `PortfolioDrawdownWidget`
* \[ ] `PortfolioRiskAnalyticsWidget`
* \[ ] `CorrelationProxyWidget`
* \[ ] `StressTestWidget`
* \[ ] `AllocationScorecardWidget`
* \[ ] `PortfolioResearchGuardWidget`
* \[ ] `PortfolioEvidenceWidget`

Nieuwe Roadmap 111 extension packs:

### `portfolio-basket-lab`

* \[ ] basket builder;
* \[ ] allocation proposal;
* \[ ] simulation preview;
* \[ ] scorecard;
* \[ ] evidence.

### `conservative-allocation-research`

* \[ ] conservative constraints;
* \[ ] drawdown-focused scoring;
* \[ ] stress tests;
* \[ ] no-advice banner.

### `diversification-research-desk`

* \[ ] correlation proxy;
* \[ ] exposure breakdown;
* \[ ] model/strategy diversity;
* \[ ] basket scorecards.

Acceptatiecriteria:

* \[ ] Widgets validate in registry.
* \[ ] Packs validate through extension pack schema.
* \[ ] Safety widgets included.
* \[ ] Browser smoke covers one pack.
* \[ ] Pack evidence generated.

\---

## 19\. Fase 16 - Portfolio Lab API

Nieuwe Dashboard V2 API routes:

```text
GET  /api/portfolio-lab/health
POST /api/portfolio-lab/baskets/build
GET  /api/portfolio-lab/baskets
GET  /api/portfolio-lab/baskets/{basket\_id}
POST /api/portfolio-lab/allocations/propose
POST /api/portfolio-lab/allocations/validate
GET  /api/portfolio-lab/allocations
POST /api/portfolio-lab/simulations/preview
POST /api/portfolio-lab/simulations/run
GET  /api/portfolio-lab/simulations
GET  /api/portfolio-lab/simulations/{run\_id}
POST /api/portfolio-lab/stress-tests/run
POST /api/portfolio-lab/scorecards
POST /api/portfolio-lab/research-guards
POST /api/portfolio-lab/evidence-export
WS   /ws/portfolio-lab
```

Rules:

* \[ ] All responses include `live\_trading\_enabled=False`.
* \[ ] Simulation run requires `RUN\_PAPER\_PORTFOLIO\_RESEARCH\_ONLY`.
* \[ ] Large simulation requires preview first.
* \[ ] No signed/order/account endpoints.
* \[ ] No financial advice wording.
* \[ ] Payload limits enforced.
* \[ ] Reports redacted.

Acceptatiecriteria:

* \[ ] TestClient covers core routes.
* \[ ] Simulation confirm required.
* \[ ] Unsafe allocation blocked.
* \[ ] WebSocket sends simulation status.
* \[ ] Reports redacted.

\---

## 20\. Fase 17 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli portfolio-lab-basket-build --strategy-lab-run <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-allocation-propose --basket <id> --mode equal\_weight --json
python -m binance\_spot\_bot.cli portfolio-lab-allocation-validate --allocation <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-simulation-preview --basket <id> --allocation <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-simulation-run --basket <id> --allocation <id> --confirm RUN\_PAPER\_PORTFOLIO\_RESEARCH\_ONLY
python -m binance\_spot\_bot.cli portfolio-lab-risk-analytics --run <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-correlation-proxy --basket <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-stress-tests --run <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-scorecards --run <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-guards --run <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-evidence-export --run <id>
python -m binance\_spot\_bot.cli dashboard-v2-portfolio-lab-smoke --json
```

Acceptatiecriteria:

* \[ ] Commands werken offline met fixtures/cache.
* \[ ] Commands ondersteunen JSON.
* \[ ] Simulation run vereist confirm.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Reports zijn secret-free.

\---

## 21\. Fase 18 - Check-All Integration

Fast profile:

* \[ ] portfolio lab module imports.
* \[ ] safety contract/no-live checks.
* \[ ] basket schema validation.
* \[ ] allocation constraint fixture.
* \[ ] no-advice/no-real-allocation wording scan.

Deep profile:

* \[ ] basket builder fixture.
* \[ ] allocation proposal fixture.
* \[ ] paper portfolio simulation fixture.
* \[ ] risk analytics fixture.
* \[ ] stress test fixture.
* \[ ] scorecard fixture.
* \[ ] research guard fixture.
* \[ ] portfolio lab API smoke.
* \[ ] dashboard browser smoke.
* \[ ] evidence bundle verify.

Acceptatiecriteria:

* \[ ] Fast check-all blijft snel.
* \[ ] Deep check-all dekt end-to-end paper portfolio research.
* \[ ] No-live failure hard fail.
* \[ ] Advice wording failure hard fail.
* \[ ] Reports secret-free.

\---

## 22\. Fase 19 - Operator/UAT Integration

Roadmap 102:

* \[ ] Operator manual krijgt Portfolio Lab guide.
* \[ ] CLI cookbook krijgt portfolio-lab commands.
* \[ ] Troubleshooting krijgt allocation/constraint/stress-test playbook.
* \[ ] Evidence guide krijgt Portfolio Lab evidence uitleg.

Roadmap 103:

* \[ ] UAT scenario: Strategy Lab results naar basket.
* \[ ] UAT scenario: allocation proposal preview.
* \[ ] UAT scenario: paper portfolio simulation run.
* \[ ] UAT scenario: stress tests bekijken.
* \[ ] UAT scenario: allocation scorecards bekijken.
* \[ ] UAT scenario: no-live/no-advice/no-real-allocation proof controleren.
* \[ ] UAT scenario: evidence exporteren.

Acceptatiecriteria:

* \[ ] UAT scenarios pass.
* \[ ] Docs link valid.
* \[ ] No-live/no-advice proof included.
* \[ ] UAT feedback can create portfolio-lab backlog items.
* \[ ] Browser smoke/UAT evidence linked.

\---

## 23\. Fase 20 - Release/Knowledge/Test/Performance Integration

Roadmap 089:

* \[ ] Release notes include Portfolio Lab.
* \[ ] Version manifest includes portfolio-lab schema version.
* \[ ] Migration notes include basket/allocation/result paths.

Roadmap 091:

* \[ ] Knowledge graph maps Strategy Lab → Portfolio Lab.
* \[ ] Impact analysis detects Strategy Lab changes affecting Portfolio Lab.
* \[ ] Ownership map includes Portfolio Lab modules.

Roadmap 092:

* \[ ] Test selector chooses portfolio-lab tests for basket/allocation/simulation changes.
* \[ ] Strategy Lab changes select Portfolio Lab integration tests.
* \[ ] Dashboard Portfolio Lab UI changes select browser smoke.

Roadmap 093:

* \[ ] Performance budgets for basket size, allocation search count, simulation runtime, result payload, report size.
* \[ ] Heavy simulations produce warnings/findings.
* \[ ] Simulation runtime trends stored locally.

Acceptatiecriteria:

* \[ ] Release evidence includes Portfolio Lab evidence.
* \[ ] Knowledge graph updated.
* \[ ] Test selection works.
* \[ ] Performance reports include portfolio budgets.
* \[ ] No-live proof preserved.

\---

## 24\. Fase 21 - Scheduled Portfolio Lab Reports

Scheduled jobs:

* \[ ] weekly candidate basket refresh from latest Strategy Lab evidence.
* \[ ] weekly conservative allocation simulation.
* \[ ] weekly stress test summary.
* \[ ] weekly allocation scorecard summary.
* \[ ] monthly portfolio research report.
* \[ ] post-Strategy-Lab-change basket validation.
* \[ ] post-risk-change allocation constraint smoke.
* \[ ] post-dashboard-change Portfolio Lab smoke.

Metrics:

* \[ ] basket count.
* \[ ] allocation count.
* \[ ] completed simulation count.
* \[ ] blocked simulation count.
* \[ ] max drawdown distribution.
* \[ ] concentration warnings.
* \[ ] stress test failures.
* \[ ] top paper research allocations.
* \[ ] rejected allocations.
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

## 25\. Tests

### Unit tests

* \[ ] `tests/test\_portfolio\_lab\_safety\_contract.py`
* \[ ] `tests/test\_portfolio\_candidate\_basket.py`
* \[ ] `tests/test\_portfolio\_basket\_builder.py`
* \[ ] `tests/test\_allocation\_constraints.py`
* \[ ] `tests/test\_allocation\_proposals.py`
* \[ ] `tests/test\_portfolio\_experiment\_orchestrator.py`
* \[ ] `tests/test\_basket\_simulation.py`
* \[ ] `tests/test\_portfolio\_risk\_analytics.py`
* \[ ] `tests/test\_correlation\_proxy.py`
* \[ ] `tests/test\_portfolio\_stress\_tests.py`
* \[ ] `tests/test\_allocation\_scorecards.py`
* \[ ] `tests/test\_portfolio\_experiment\_store.py`
* \[ ] `tests/test\_portfolio\_research\_guards.py`
* \[ ] `tests/test\_portfolio\_lab\_evidence\_bundle.py`
* \[ ] `tests/test\_portfolio\_lab\_api.py`
* \[ ] `tests/test\_portfolio\_lab\_widgets.py`

### Integration tests

* \[ ] Build basket from Strategy Lab fixture.
* \[ ] Build allocation proposal.
* \[ ] Validate constraints.
* \[ ] Run paper portfolio simulation fixture.
* \[ ] Generate risk analytics.
* \[ ] Generate correlation proxy.
* \[ ] Run stress tests.
* \[ ] Generate allocation scorecards.
* \[ ] Run portfolio research guards.
* \[ ] Export evidence bundle.
* \[ ] Dashboard API TestClient smoke.

### Browser smoke

* \[ ] `/portfolio-lab` loads.
* \[ ] basket builder visible.
* \[ ] allocation preview works.
* \[ ] simulation results table visible.
* \[ ] portfolio equity chart visible.
* \[ ] stress test panel visible.
* \[ ] scorecards visible.
* \[ ] research guards visible.
* \[ ] no-live/no-advice/no-real-allocation banner visible.
* \[ ] no live controls visible.

### Safety tests

* \[ ] Live mode blocked.
* \[ ] Signed endpoint blocked.
* \[ ] Account endpoint blocked.
* \[ ] Order endpoint blocked.
* \[ ] Simulation run requires paper-only confirm.
* \[ ] Runner works without API keys.
* \[ ] Advice wording blocked.
* \[ ] Real allocation wording blocked.
* \[ ] No auto-order action present.
* \[ ] Evidence secret-free.
* \[ ] Check-all safe env preserved.

\---

## 26\. Docs

Nieuwe docs:

```text
docs/portfolio-lab/paper-portfolio-research-safety-contract.md
docs/portfolio-lab/candidate-basket.md
docs/portfolio-lab/basket-builder.md
docs/portfolio-lab/allocation-constraints.md
docs/portfolio-lab/allocation-proposals.md
docs/portfolio-lab/portfolio-experiment-orchestrator.md
docs/portfolio-lab/basket-simulation.md
docs/portfolio-lab/portfolio-risk-analytics.md
docs/portfolio-lab/correlation-proxy.md
docs/portfolio-lab/stress-tests.md
docs/portfolio-lab/allocation-scorecards.md
docs/portfolio-lab/research-guards.md
docs/portfolio-lab/evidence-bundle.md
docs/portfolio-lab/dashboard-v2-workbench.md
docs/portfolio-lab/troubleshooting.md
```

README updates:

* \[ ] Portfolio Lab overview.
* \[ ] Strategy Lab to Portfolio Lab workflow.
* \[ ] Paper-only/no-live statement.
* \[ ] No financial advice/no real allocation statement.
* \[ ] CLI examples.
* \[ ] Dashboard V2 route.
* \[ ] Evidence export.

Operator docs updates:

* \[ ] Portfolio Lab quick start.
* \[ ] Basket builder guide.
* \[ ] Allocation proposal interpretation.
* \[ ] Stress test interpretation.
* \[ ] Scorecard interpretation.
* \[ ] Research guard troubleshooting.
* \[ ] No-live/no-advice proof.

\---

## 27\. Codex bouwvolgorde

### PR 1 - Safety Contract + Candidate Basket Schema

* \[ ] `docs/portfolio-lab/paper-portfolio-research-safety-contract.md`
* \[ ] `portfolio\_lab/candidate\_basket.py`
* \[ ] fixture scorecard tests.
* \[ ] no-advice tests.

### PR 2 - Basket Builder + Allocation Constraints

* \[ ] `basket\_builder.py`
* \[ ] `allocation\_constraints.py`
* \[ ] filter/constraint tests.

### PR 3 - Allocation Proposals

* \[ ] `allocation\_proposals.py`
* \[ ] equal/score/inverse-drawdown/inverse-volatility proposals.
* \[ ] constraint integration tests.

### PR 4 - Portfolio Experiment Orchestrator

* \[ ] `portfolio\_experiment\_orchestrator.py`
* \[ ] paper-only orchestration fixture.
* \[ ] no signed/account/order tests.

### PR 5 - Basket Simulation + Result Store

* \[ ] `basket\_simulation.py`
* \[ ] `portfolio\_experiment\_store.py`
* \[ ] simulation/store tests.

### PR 6 - Risk Analytics + Correlation Proxy + Stress Tests

* \[ ] `portfolio\_risk\_analytics.py`
* \[ ] `correlation\_proxy.py`
* \[ ] `stress\_tests.py`
* \[ ] fixture tests.

### PR 7 - Scorecards + Research Guards

* \[ ] `allocation\_scorecards.py`
* \[ ] `portfolio\_research\_guards.py`
* \[ ] advice wording/guard tests.

### PR 8 - API + Dashboard Widgets

* \[ ] portfolio lab API routes.
* \[ ] Portfolio Lab widgets.
* \[ ] TestClient/frontend tests.

### PR 9 - Dashboard Workbench + Packs

* \[ ] Dashboard V2 Portfolio Lab pages.
* \[ ] workspace/template packs.
* \[ ] browser smoke.

### PR 10 - Evidence, CLI, Check-All, Docs \& Integrations

* \[ ] `evidence\_bundle.py`
* \[ ] CLI commands.
* \[ ] check-all integration.
* \[ ] docs.
* \[ ] UAT scenarios.
* \[ ] release/knowledge/test/performance integration.
* \[ ] scheduled reports.

\---

## 28\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 114 PR 1: Paper Portfolio Research Safety Contract + Portfolio Candidate Basket Schema.

Maak docs/portfolio-lab/paper-portfolio-research-safety-contract.md.

Maak src/binance\_spot\_bot/portfolio\_lab/\_\_init\_\_.py.
Maak src/binance\_spot\_bot/portfolio\_lab/candidate\_basket.py met:
- PortfolioBasketItem
- PortfolioCandidateBasket
- PortfolioBasketSource
- PortfolioBasketValidationResult
- PortfolioBasketBuildReport
- validate\_portfolio\_candidate\_basket(basket: PortfolioCandidateBasket)
- portfolio\_candidate\_basket\_to\_dict(...)
- write\_portfolio\_candidate\_basket(...)

Basket item moet minimaal bevatten:
- item\_id
- symbol
- strategy\_id
- model\_alias
- risk\_preset
- source\_candidate\_id
- source\_scorecard\_id
- paper\_score
- data\_quality\_score
- market\_quality\_score
- warnings
- blocked\_reason optional
- paper\_only=True
- live\_trading\_enabled=False

Basket moet minimaal bevatten:
- basket\_id
- name
- description
- source\_queue\_id
- source\_scanner\_run\_id
- items
- max\_items
- quote\_asset
- created\_at\_ms
- no\_live\_statement
- no\_financial\_advice\_statement
- paper\_only\_research\_statement
- live\_trading\_enabled=False

Validatie moet blokkeren op:
- live mode of live\_trading\_enabled=True
- ontbrekende no\_live\_statement
- ontbrekende no\_financial\_advice\_statement
- ontbrekende paper\_only\_research\_statement
- duplicate item\_id
- duplicate active symbol/strategy/model/risk combo
- item met paper\_only=False
- blocked item zonder disabled/blocked status
- negatieve scores
- max\_items overschreden
- buy/sell/financial advice wording
- secret-like values

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
- valid basket
- live\_trading\_enabled True blocked
- missing no\_live\_statement blocked
- missing no\_financial\_advice\_statement blocked
- missing paper\_only\_research\_statement blocked
- duplicate item\_id blocked
- duplicate active combo blocked
- blocked candidate handling
- negative score blocked
- max\_items exceeded blocked
- advice wording blocked
- JSON serialization
- secret-like values worden geredact
- live\_trading\_enabled=False
```

Waarom eerst:

* Portfolio Lab moet beginnen met een veilig, testbaar basket-schema.
* Het is read-only en raakt runtime/trading/frontend niet.
* Het is klein genoeg voor Codex.
* No-live, no-advice en paper-only regels worden meteen machine-testbaar.
* Daarna kunnen allocation constraints, proposals en simulations veilig op dit schema bouwen.

\---

## 29\. Definition of Done

Roadmap 114 is klaar als:

* \[ ] Paper Portfolio Research Safety Contract bestaat.
* \[ ] Portfolio Candidate Basket Schema werkt.
* \[ ] Basket Builder \& Filters werken.
* \[ ] Allocation Constraint Engine werkt.
* \[ ] Allocation Proposal Generator werkt.
* \[ ] Paper Portfolio Experiment Orchestrator werkt.
* \[ ] Basket Simulation Engine werkt.
* \[ ] Portfolio Risk Analytics werkt.
* \[ ] Correlation \& Overlap Proxy werkt.
* \[ ] Scenario Stress Test Engine werkt.
* \[ ] Allocation Research Scorecards werken.
* \[ ] Portfolio Experiment Store werkt.
* \[ ] Portfolio Research Guards werken.
* \[ ] Portfolio Lab Evidence Bundle werkt.
* \[ ] Dashboard V2 Portfolio Lab Workbench werkt.
* \[ ] Portfolio Lab Widgets \& Workspace Packs werken.
* \[ ] Portfolio Lab API werkt.
* \[ ] CLI commands werken.
* \[ ] Check-All Integration werkt.
* \[ ] Operator/UAT Integration werkt.
* \[ ] Release/Knowledge/Test/Performance Integration werkt.
* \[ ] Scheduled Portfolio Lab Reports werken.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen runner zonder API keys werkt.
* \[ ] Tests bewijzen geen financieel advies of real allocation wording.
* \[ ] Tests bewijzen evidence secret-free is.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Portfolio Lab is local-only en paper-only.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 114 kan na uitvoering naar `Voltooid docs`.

\---

## 30\. Verwachte Roadmap 115 daarna

Als Roadmap 114 groen is:

```text
Roadmap 115 - Local Paper Portfolio Rebalancing Research, Walk-Forward Basket Validation \& Allocation Robustness Lab
```

Mogelijke inhoud:

* \[ ] walk-forward basket validation;
* \[ ] allocation robustness tests;
* \[ ] rebalancing schedule research;
* \[ ] out-of-sample scenario splits;
* \[ ] candidate decay monitoring;
* \[ ] paper-only governance;
* \[ ] still no live trading.

```

Als Roadmap 114 performanceproblemen vindt:

```text
Roadmap 115 - Portfolio Lab Performance Burn-Down, Simulation Cache \& Large Basket Optimization
```

Mogelijke inhoud:

* \[ ] simulation result cache;
* \[ ] basket simulation batching;
* \[ ] large basket warnings;
* \[ ] stress test optimization;
* \[ ] Dashboard V2 chart virtualization;
* \[ ] still no live trading.

```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Paper portfolio experiment orchestrator and basket simulation.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.

## Uitvoering 2026-05-15

Status: Voltooid / Gevalideerd.

Gebouwd:

- `src/binance_spot_bot/portfolio_lab/` met basket schema, builder, allocation constraints/proposals, orchestrator, simulation, risk analytics, correlation proxy, stress tests, scorecards, store, guards, evidence en scheduled report surface.
- Dashboard V2 API routes voor `/api/portfolio-lab/*`.
- Dashboard V2 `/portfolio-lab` React workbench met basket, allocation, stress, scorecards, guards en equity preview.
- Portfolio Lab widget registry entries.
- Portfolio Lab CLI commands en `check-all` integratie.
- Portfolio Lab docs en safety contract.
- Roadmap 114 acceptance tests.

Validatie:

- `python -m compileall -q src tests`
- `python -m pytest -q tests/test_roadmap_114_portfolio_lab_acceptance.py` -> 6 passed.
- Portfolio Lab CLI smokes inclusief confirm-gate.
- `npm install; npm run build`
- `python -m binance_spot_bot.cli security-scan` -> geen findings.
- `python -m binance_spot_bot.cli dashboard-v2-smoke --json` -> ok.
- `python -m binance_spot_bot.cli check-all --skip-tests --json` -> ok.
- Browser render `/portfolio-lab` screenshot: `%TEMP%/portfolio-lab-114.png`.
- `python -m pytest -q` -> 437 passed, 1 warning.

Safety:

- Geen API keys nodig.
- Geen signed/account/order endpoints.
- Simulation run vereist `RUN_PAPER_PORTFOLIO_RESEARCH_ONLY`.
- Alle Portfolio Lab responses houden `live_trading_enabled=false`.

