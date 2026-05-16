# Roadmap 115 - Local Paper Portfolio Rebalancing Research, Walk-Forward Basket Validation \& Allocation Robustness Lab

Status: Voltooid / Gevalideerd  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/115-roadmap-local-paper-portfolio-rebalancing-research-walk-forward-basket-validation-allocation-robustness-lab.md
```

## Samenvatting

Roadmap 112 bouwt een lokale Binance Spot Market Intelligence Workbench met scanner, symbol rankings, market metrics en multi-symbol paper analytics.

Roadmap 113 bouwt een Strategy Lab dat scanner-output omzet naar paper-only experiment queues, strategy/model/risk comparisons, candidate scorecards en portfolio candidate research.

Roadmap 114 bouwt een Portfolio Lab dat candidate baskets, allocation constraints, paper portfolio simulations, stress tests en allocation scorecards maakt.

Roadmap 115 is de logische volgende stap: **paper portfolio allocations robuust valideren vóór je ze als research-setup vertrouwt**. Niet alleen één basket simulation draaien, maar walk-forward splits, rolling windows, rebalancing schedules, allocation decay, candidate replacement, robustness scoring en paper-only governance toevoegen.

De kern:

```text
Portfolio Lab allocation candidates
→ walk-forward split builder
→ rebalancing schedule research
→ rolling paper portfolio simulations
→ allocation robustness scoring
→ candidate decay monitoring
→ out-of-sample validation
→ governance/sign-off evidence
```

Live trading blijft volledig buiten scope. Geen live mode, geen signed real-order endpoints, geen echte account workflows, geen echte portfolio allocaties en geen financieel advies. Alles is local-only, paper-only research.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 115`, `115-roadmap`, `Paper Portfolio Rebalancing`, `Walk-Forward Basket Validation`, `Allocation Robustness Lab` en `rebalancing research`.
* \[x] Geen bestaande Roadmap 115 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 114 is lokaal aangemaakt als Local Paper Portfolio Experiment Orchestrator, Candidate Basket Simulation \& Allocation Research.

### Codebasecontrole

Breed bekeken met focus op paper runtime, paper accounting, risk, sessions, market data, check-all, Strategy Lab/Portfolio Lab vervolg en safety:

* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/paper.py`
* \[x] `src/binance\_spot\_bot/paper\_accounting.py`
* \[x] `src/binance\_spot\_bot/risk.py`
* \[x] `src/binance\_spot\_bot/session\_store.py`
* \[x] `src/binance\_spot\_bot/market\_data\_source.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] roadmaplijn 104-114.

### Belangrijke bestaande basis

De codebase heeft nu of krijgt via Roadmap 112-114:

* \[x] Runtime modes zijn beperkt tot `demo`, `paper` en `testnet-readiness`.
* \[x] `RuntimeSnapshot` bevat candles, signals, fills, equity points, risk decisions, data quality, session summaries, active model, paper account, alerts en report paths.
* \[x] `PaperTrader` genereert signals, risk decisions en execution results via model, risk engine en execution engine.
* \[x] `PaperAccount` ondersteunt buy/sell, equity, fees, slippage, realized PnL en fills.
* \[x] `RiskEngine` blokkeert op kill switch, HOLD, lage confidence, max trades, max position, max daily loss, stale data, spread, insufficient quote/base balance.
* \[x] `SessionStore` bewaart session summaries, snapshots, fills, alerts, orders en exports.
* \[x] `check\_all.py` forceert safe env:

  * `LIVE\_TRADING\_ENABLED=false`;
  * `KILL\_SWITCH=true`;
  * `PYTHONPATH=src`.
* \[x] Roadmap 114 plant candidate baskets, allocation proposals, paper portfolio simulations, stress tests, risk analytics en evidence.

### Belangrijkste gat na Roadmap 114

Roadmap 114 kan paper portfolio allocations simuleren en scorecards maken. Maar één simulatie of één historische periode is niet genoeg om robuustheid te onderzoeken:

* \[ ] Geen walk-forward split builder.
* \[ ] Geen train/validation/test tijdvensters voor paper research.
* \[ ] Geen rolling basket validation.
* \[ ] Geen rebalancing schedule comparison.
* \[ ] Geen allocation decay monitoring.
* \[ ] Geen candidate replacement rules.
* \[ ] Geen out-of-sample robustness score.
* \[ ] Geen rolling drawdown/volatility stability score.
* \[ ] Geen cross-window consistency report.
* \[ ] Geen governance gate die “niet robuust genoeg” blokkeert.
* \[ ] Geen Dashboard V2 Robustness Lab.
* \[ ] Geen robustness evidence bundle.

Roadmap 115 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 115

Maak een local-only, paper-only robustness lab voor portfolio allocations:

```text
Portfolio Lab allocations
→ walk-forward splits
→ rolling basket simulations
→ rebalancing schedule experiments
→ candidate decay checks
→ out-of-sample robustness scorecards
→ governance gate
→ evidence bundle
```

Na Roadmap 115 moet de operator:

* \[ ] allocation candidates over meerdere tijdvensters kunnen testen;
* \[ ] walk-forward splits kunnen maken uit cached candles/paper results;
* \[ ] rebalance schedules kunnen vergelijken;
* \[ ] candidate decay kunnen meten;
* \[ ] candidate replacement rules kunnen simuleren;
* \[ ] allocation stability kunnen beoordelen;
* \[ ] out-of-sample performance kunnen scheiden van in-sample research;
* \[ ] robustness scorecards kunnen exporteren;
* \[ ] governance gate kunnen gebruiken om zwakke allocations te blokkeren;
* \[ ] alles no-live, paper-only en no-advice houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen scanner opnieuw bouwen.
* \[ ] Geen Strategy Lab opnieuw bouwen.
* \[ ] Geen Portfolio Lab basket simulation opnieuw bouwen.
* \[ ] Geen Dashboard V2 workspace systeem opnieuw bouwen.
* \[ ] Geen trading runtime refactor.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed order endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen echte portfolio allocaties.
* \[ ] Geen echte Binance orders.
* \[ ] Geen financieel advies.
* \[ ] Geen remote telemetry.
* \[ ] Geen cloud research platform.
* \[ ] Geen API keys vereisen.
* \[ ] Geen out-of-sample claim zonder bewijs/evidence.

Wel doen:

* \[ ] walk-forward splits;
* \[ ] rolling validation;
* \[ ] rebalancing schedule research;
* \[ ] allocation decay;
* \[ ] candidate replacement simulation;
* \[ ] robustness metrics;
* \[ ] governance gate;
* \[ ] Dashboard V2 Robustness Lab;
* \[ ] CLI/reports/evidence/tests;
* \[ ] no-live/no-advice proof.

\---

## 3\. Fase 0 - Walk-Forward Robustness Safety Contract

Nieuw docbestand:

```text
docs/portfolio-lab/walk-forward-robustness-safety-contract.md
```

Regels:

* \[ ] Robustness Lab is local-only.
* \[ ] Alle simulations zijn paper-only.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed order endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen echte orders.
* \[ ] Geen echte portfolio allocaties.
* \[ ] Geen API keys vereist.
* \[ ] Output is geen financieel advies.
* \[ ] Geen “koop/verkoop” of “real allocation” wording.
* \[ ] Walk-forward output moet split boundaries tonen.
* \[ ] Out-of-sample claims vereisen split evidence.
* \[ ] Orchestrator gebruikt safe env:

  * `LIVE\_TRADING\_ENABLED=false`;
  * `KILL\_SWITCH=true`.
* \[ ] Reports/evidence zijn secret-free.
* \[ ] Elke run bevat `live\_trading\_enabled=False`.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen live/signed/account/order endpoints geblokkeerd zijn.
* \[ ] Tests bewijzen no-advice/no-real-allocation wording.
* \[ ] Tests bewijzen split evidence verplicht is voor out-of-sample score.
* \[ ] Tests bewijzen reports secret-free zijn.

\---

## 4\. Fase 1 - Walk-Forward Split Schema

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/walk\_forward\_splits.py
```

Dataclasses:

* \[ ] `WalkForwardSplit`
* \[ ] `WalkForwardWindow`
* \[ ] `WalkForwardSplitConfig`
* \[ ] `WalkForwardSplitValidationResult`
* \[ ] `WalkForwardSplitReport`

Split modes:

* \[ ] expanding\_window;
* \[ ] rolling\_window;
* \[ ] anchored\_train\_validation;
* \[ ] fixed\_train\_validation\_test;
* \[ ] session\_based;
* \[ ] custom\_boundaries.

Window fields:

* \[ ] window\_id;
* \[ ] train\_start\_ms;
* \[ ] train\_end\_ms;
* \[ ] validation\_start\_ms;
* \[ ] validation\_end\_ms;
* \[ ] test\_start\_ms;
* \[ ] test\_end\_ms optional;
* \[ ] symbols;
* \[ ] source\_dataset\_ids;
* \[ ] min\_candles\_required;
* \[ ] no\_live\_statement;
* \[ ] paper\_only\_research\_statement.

Validation:

* \[ ] no overlapping invalid windows;
* \[ ] train before validation before test;
* \[ ] minimum candles per symbol;
* \[ ] no future leakage;
* \[ ] no empty validation window;
* \[ ] no live mode.

Acceptatiecriteria:

* \[ ] Split schema is JSON-serializable.
* \[ ] Invalid boundaries blocked.
* \[ ] Missing candle coverage warning/block.
* \[ ] Leakage checks run.
* \[ ] Tests cover split modes.

\---

## 5\. Fase 2 - Dataset Coverage \& Candle Availability Audit

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/dataset\_coverage\_audit.py
```

Inputs:

* \[ ] cached klines from Roadmap 112.
* \[ ] Strategy Lab experiment result stores.
* \[ ] Portfolio Lab result stores.
* \[ ] session store snapshots.
* \[ ] symbol universe metadata.

Audit metrics:

* \[ ] candles per symbol.
* \[ ] first/last timestamp.
* \[ ] missing intervals.
* \[ ] duplicate timestamps.
* \[ ] stale data.
* \[ ] min coverage by split.
* \[ ] symbol coverage alignment.
* \[ ] data gap severity.
* \[ ] cache/source provenance.
* \[ ] public-only proof.

Acceptatiecriteria:

* \[ ] Audit works from fixture candles.
* \[ ] Missing symbols reported.
* \[ ] Data gaps detected.
* \[ ] Report is Markdown + JSON.
* \[ ] Tests cover coverage edge cases.

\---

## 6\. Fase 3 - Rebalancing Schedule Schema

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/rebalancing\_schedules.py
```

Schedule types:

* \[ ] no\_rebalance;
* \[ ] fixed\_interval;
* \[ ] threshold\_based;
* \[ ] volatility\_adjusted;
* \[ ] drawdown\_guarded;
* \[ ] candidate\_decay\_guarded;
* \[ ] manual\_research\_checkpoints.

Dataclasses:

* \[ ] `RebalancingSchedule`
* \[ ] `RebalancingRule`
* \[ ] `RebalancingEvent`
* \[ ] `RebalancingScheduleValidationResult`

Fields:

* \[ ] schedule\_id;
* \[ ] schedule\_type;
* \[ ] interval\_steps;
* \[ ] interval\_ms;
* \[ ] allocation\_drift\_threshold\_pct;
* \[ ] drawdown\_threshold\_pct;
* \[ ] volatility\_threshold;
* \[ ] candidate\_decay\_threshold;
* \[ ] max\_rebalances;
* \[ ] min\_steps\_between\_rebalances;
* \[ ] paper\_only=true;
* \[ ] live\_trading\_enabled=false.

Acceptatiecriteria:

* \[ ] Schedule validation blocks unsafe values.
* \[ ] No live/real allocation wording.
* \[ ] Threshold schedules deterministic.
* \[ ] Edge cases handled.
* \[ ] Tests cover all schedule types.

\---

## 7\. Fase 4 - Rebalance Event Simulator

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/rebalance\_event\_simulator.py
```

Doel: in paper-only simulations rebalancing events plannen zonder echte orders.

Inputs:

* \[ ] allocation proposal;
* \[ ] basket simulation timeline;
* \[ ] rebalancing schedule;
* \[ ] candidate decay report;
* \[ ] market data windows;
* \[ ] constraints.

Outputs:

* \[ ] planned rebalance events;
* \[ ] skipped events;
* \[ ] constraint violations;
* \[ ] estimated turnover;
* \[ ] estimated fees;
* \[ ] allocation drift before/after;
* \[ ] paper-only event log.

Rules:

* \[ ] no real orders.
* \[ ] no execution engine real mode.
* \[ ] no signed endpoints.
* \[ ] all events are simulated/research-only.

Acceptatiecriteria:

* \[ ] Event simulator deterministic.
* \[ ] Drift threshold events trigger.
* \[ ] Max rebalances enforced.
* \[ ] Fees/turnover estimated.
* \[ ] Tests use synthetic timeline.

\---

## 8\. Fase 5 - Rolling Portfolio Simulation Orchestrator

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/rolling\_portfolio\_orchestrator.py
```

Doel: Roadmap 114 basket simulations over walk-forward windows en schedules draaien.

Inputs:

* \[ ] candidate basket.
* \[ ] allocation proposal.
* \[ ] walk-forward splits.
* \[ ] rebalancing schedules.
* \[ ] cached results/candles.
* \[ ] constraints.
* \[ ] stress scenarios optional.

Outputs:

* \[ ] `RollingPortfolioRun`
* \[ ] `RollingWindowResult`
* \[ ] `RollingScheduleResult`
* \[ ] `RollingPortfolioReport`

Per window result:

* \[ ] window\_id;
* \[ ] train metrics;
* \[ ] validation metrics;
* \[ ] test metrics optional;
* \[ ] rebalance events;
* \[ ] portfolio equity curve;
* \[ ] drawdown;
* \[ ] turnover;
* \[ ] fees;
* \[ ] guard warnings;
* \[ ] status.

Acceptatiecriteria:

* \[ ] Orchestrator runs on fixture windows.
* \[ ] Can compare at least 2 schedules.
* \[ ] Blocks missing no-live proof.
* \[ ] Works without API keys.
* \[ ] Tests cover completed/blocked/failed windows.

\---

## 9\. Fase 6 - Allocation Decay Monitor

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/allocation\_decay.py
```

Decay signals:

* \[ ] paper score deterioration.
* \[ ] drawdown increase.
* \[ ] block rate increase.
* \[ ] spread deterioration.
* \[ ] data quality deterioration.
* \[ ] signal count collapse.
* \[ ] model confidence degradation.
* \[ ] volatility regime shift.
* \[ ] candidate no longer passes scanner filters.
* \[ ] stress test degradation.

Dataclasses:

* \[ ] `AllocationDecaySignal`
* \[ ] `CandidateDecayReport`
* \[ ] `AllocationDecaySummary`

Statuses:

* \[ ] stable;
* \[ ] watch;
* \[ ] degraded;
* \[ ] remove\_candidate\_research\_only;
* \[ ] blocked.

Acceptatiecriteria:

* \[ ] Decay monitor deterministic.
* \[ ] Does not output live action.
* \[ ] Degraded candidates visible in report.
* \[ ] Tests cover each decay signal.
* \[ ] Advice wording scan passes.

\---

## 10\. Fase 7 - Candidate Replacement Simulator

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/candidate\_replacement.py
```

Replacement policies:

* \[ ] no\_replacement baseline;
* \[ ] replace\_degraded\_with\_next\_candidate;
* \[ ] replace\_if\_data\_quality\_fails;
* \[ ] replace\_if\_drawdown\_threshold;
* \[ ] replace\_if\_scanner\_rank\_decays;
* \[ ] manual\_review\_required.

Inputs:

* \[ ] candidate basket.
* \[ ] candidate scorecards.
* \[ ] decay reports.
* \[ ] replacement candidate pool.
* \[ ] allocation constraints.

Outputs:

* \[ ] replacement events;
* \[ ] before/after basket;
* \[ ] constraint report;
* \[ ] expected risk changes;
* \[ ] paper-only replacement note.

Acceptatiecriteria:

* \[ ] Replacement never auto-orders.
* \[ ] Replacement policy deterministic.
* \[ ] Constraints revalidated after replacement.
* \[ ] Manual review policy blocks auto-replace.
* \[ ] Tests cover policies.

\---

## 11\. Fase 8 - Walk-Forward Performance Analyzer

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/walk\_forward\_performance.py
```

Metrics:

* \[ ] train vs validation performance gap.
* \[ ] validation vs test performance gap.
* \[ ] rolling PnL stability.
* \[ ] rolling drawdown stability.
* \[ ] schedule turnover.
* \[ ] fee drag per schedule.
* \[ ] worst window.
* \[ ] best window.
* \[ ] median window.
* \[ ] pass window ratio.
* \[ ] drawdown breach count.
* \[ ] data quality fail count.
* \[ ] rebalance event count.

Acceptatiecriteria:

* \[ ] Analyzer deterministic.
* \[ ] Handles missing test window.
* \[ ] Detects overfit gap.
* \[ ] Reports Markdown + JSON.
* \[ ] Tests cover synthetic windows.

\---

## 12\. Fase 9 - Allocation Robustness Scorecards

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/allocation\_robustness\_scorecards.py
```

Score dimensions:

* \[ ] out-of-sample consistency.
* \[ ] walk-forward pass rate.
* \[ ] worst-window drawdown.
* \[ ] median-window performance.
* \[ ] turnover penalty.
* \[ ] fee drag penalty.
* \[ ] data quality robustness.
* \[ ] candidate decay penalty.
* \[ ] replacement stability.
* \[ ] stress scenario survival.
* \[ ] allocation concentration.
* \[ ] schedule simplicity.
* \[ ] reproducibility.

Grades:

* \[ ] A: robust paper research candidate.
* \[ ] B: usable with warnings.
* \[ ] C: unstable, needs more validation.
* \[ ] D: blocked for paper portfolio research.
* \[ ] F: unsafe/invalid/no-live failure.

Wording:

* \[ ] “paper research candidate”.
* \[ ] “robustness score”.
* \[ ] No buy/sell.
* \[ ] No real allocation.

Acceptatiecriteria:

* \[ ] Scorecard deterministic.
* \[ ] Hard blockers force D/F.
* \[ ] Advice wording scan passes.
* \[ ] Report includes reasons.
* \[ ] Tests cover all grades.

\---

## 13\. Fase 10 - Robustness Governance Gate

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/robustness\_governance\_gate.py
```

Gate states:

* \[ ] draft;
* \[ ] research\_ready;
* \[ ] needs\_more\_data;
* \[ ] blocked\_by\_data\_quality;
* \[ ] blocked\_by\_overfit;
* \[ ] blocked\_by\_drawdown;
* \[ ] blocked\_by\_no\_live\_failure;
* \[ ] rejected.

Hard blockers:

* \[ ] no-live proof missing.
* \[ ] no paper-only statement.
* \[ ] advice wording violation.
* \[ ] validation/test windows missing.
* \[ ] extreme overfit gap.
* \[ ] worst-window drawdown above threshold.
* \[ ] too few pass windows.
* \[ ] data quality fail in critical window.
* \[ ] replacement policy unsafe.
* \[ ] constraints violated.

Acceptatiecriteria:

* \[ ] Gate deterministic.
* \[ ] Hard blockers force blocked/rejected.
* \[ ] Gate never approves live usage.
* \[ ] Gate output Markdown + JSON.
* \[ ] Tests cover gate states.

\---

## 14\. Fase 11 - Walk-Forward Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_lab/walk\_forward\_evidence\_bundle.py
```

Bundle bevat:

* \[ ] safety contract.
* \[ ] walk-forward split report.
* \[ ] dataset coverage audit.
* \[ ] rebalancing schedule report.
* \[ ] rebalance event simulation report.
* \[ ] rolling portfolio run report.
* \[ ] allocation decay report.
* \[ ] candidate replacement report.
* \[ ] walk-forward performance report.
* \[ ] robustness scorecards.
* \[ ] governance gate report.
* \[ ] no-live proof.
* \[ ] no-real-allocation proof.
* \[ ] no-financial-advice proof.
* \[ ] redaction proof.
* \[ ] hashes.

Output:

```text
data/portfolio-lab/walk-forward/evidence/<run\_id>/
  walk\_forward\_evidence\_manifest.json
  walk\_forward\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle links to Roadmap 114 Portfolio Lab evidence.
* \[ ] Dashboard can download bundle.

\---

## 15\. Fase 12 - Dashboard V2 Allocation Robustness Lab

Nieuwe Dashboard V2 routes:

```text
/portfolio-lab/robustness
/portfolio-lab/walk-forward
/portfolio-lab/rebalancing
/portfolio-lab/decay
/portfolio-lab/replacements
/portfolio-lab/governance
```

Panels:

* \[ ] Portfolio Lab run selector.
* \[ ] walk-forward split builder.
* \[ ] dataset coverage audit.
* \[ ] rebalancing schedule selector.
* \[ ] schedule comparison table.
* \[ ] rolling simulation status.
* \[ ] train/validation/test performance chart.
* \[ ] worst-window panel.
* \[ ] allocation decay panel.
* \[ ] candidate replacement simulator.
* \[ ] robustness scorecards.
* \[ ] governance gate.
* \[ ] evidence export.
* \[ ] no-live/no-advice/no-real-allocation banner.

Acceptatiecriteria:

* \[ ] Robustness page loads.
* \[ ] Split preview works.
* \[ ] Schedule comparison visible.
* \[ ] Robustness scorecard visible.
* \[ ] Browser smoke covers happy path.

\---

## 16\. Fase 13 - Dashboard Widgets \& Workspace Packs

Nieuwe widgets:

* \[ ] `WalkForwardSplitWidget`
* \[ ] `DatasetCoverageWidget`
* \[ ] `RebalancingScheduleWidget`
* \[ ] `RebalanceEventTimelineWidget`
* \[ ] `RollingPortfolioStatusWidget`
* \[ ] `WalkForwardPerformanceWidget`
* \[ ] `AllocationDecayWidget`
* \[ ] `CandidateReplacementWidget`
* \[ ] `RobustnessScorecardWidget`
* \[ ] `RobustnessGovernanceGateWidget`
* \[ ] `WalkForwardEvidenceWidget`

Nieuwe Roadmap 111 extension packs:

### `allocation-robustness-lab`

* \[ ] split builder;
* \[ ] schedule comparison;
* \[ ] rolling simulation status;
* \[ ] robustness scorecard;
* \[ ] governance gate;
* \[ ] evidence.

### `conservative-rebalancing-research`

* \[ ] no-rebalance baseline;
* \[ ] fixed schedule;
* \[ ] drawdown guarded schedule;
* \[ ] turnover/fee analysis.

### `candidate-decay-monitoring-desk`

* \[ ] decay signals;
* \[ ] replacement policy;
* \[ ] scanner rank decay;
* \[ ] manual review warnings.

Acceptatiecriteria:

* \[ ] Widgets validate in Dashboard V2 registry.
* \[ ] Packs validate through extension pack schema.
* \[ ] Safety widgets included.
* \[ ] Browser smoke covers one pack.
* \[ ] Pack evidence generated.

\---

## 17\. Fase 14 - Robustness API

Nieuwe Dashboard V2 API routes:

```text
GET  /api/portfolio-lab/robustness/health
POST /api/portfolio-lab/walk-forward/splits/preview
POST /api/portfolio-lab/walk-forward/splits/create
POST /api/portfolio-lab/dataset-coverage/audit
GET  /api/portfolio-lab/rebalancing/schedules
POST /api/portfolio-lab/rebalancing/schedules/validate
POST /api/portfolio-lab/rebalancing/events/simulate
POST /api/portfolio-lab/rolling-simulation/preview
POST /api/portfolio-lab/rolling-simulation/run
POST /api/portfolio-lab/decay/analyze
POST /api/portfolio-lab/replacements/simulate
POST /api/portfolio-lab/walk-forward/performance
POST /api/portfolio-lab/robustness/scorecards
POST /api/portfolio-lab/robustness/governance-gate
POST /api/portfolio-lab/walk-forward/evidence-export
WS   /ws/portfolio-lab/robustness
```

Rules:

* \[ ] All responses include `live\_trading\_enabled=False`.
* \[ ] Rolling simulation requires `RUN\_WALK\_FORWARD\_PAPER\_RESEARCH\_ONLY`.
* \[ ] Large runs require preview first.
* \[ ] No signed/order/account endpoints.
* \[ ] No financial advice wording.
* \[ ] Payload limits enforced.
* \[ ] Reports redacted.

Acceptatiecriteria:

* \[ ] TestClient covers core routes.
* \[ ] Run confirm required.
* \[ ] Unsafe split/allocation blocked.
* \[ ] WebSocket sends rolling status.
* \[ ] Reports redacted.

\---

## 18\. Fase 15 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli portfolio-lab-walk-forward-splits-preview --run <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-dataset-coverage-audit --basket <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-rebalancing-schedules --json
python -m binance\_spot\_bot.cli portfolio-lab-rebalance-events-preview --allocation <id> --schedule fixed\_interval --json
python -m binance\_spot\_bot.cli portfolio-lab-rolling-simulation-preview --allocation <id> --splits <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-rolling-simulation-run --allocation <id> --splits <id> --confirm RUN\_WALK\_FORWARD\_PAPER\_RESEARCH\_ONLY
python -m binance\_spot\_bot.cli portfolio-lab-allocation-decay --run <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-candidate-replacements --run <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-walk-forward-performance --run <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-robustness-scorecards --run <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-robustness-governance-gate --run <id> --json
python -m binance\_spot\_bot.cli portfolio-lab-walk-forward-evidence-export --run <id>
python -m binance\_spot\_bot.cli dashboard-v2-portfolio-robustness-smoke --json
```

Acceptatiecriteria:

* \[ ] Commands werken offline met fixtures/cache.
* \[ ] Commands ondersteunen JSON.
* \[ ] Rolling simulation run vereist confirm.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Reports zijn secret-free.

\---

## 19\. Fase 16 - Check-All Integration

Fast profile:

* \[ ] robustness lab module imports.
* \[ ] safety contract/no-live checks.
* \[ ] walk-forward split fixture.
* \[ ] rebalancing schedule fixture.
* \[ ] no-advice/no-real-allocation wording scan.

Deep profile:

* \[ ] dataset coverage audit fixture.
* \[ ] rebalance event simulation fixture.
* \[ ] rolling portfolio simulation fixture.
* \[ ] allocation decay fixture.
* \[ ] candidate replacement fixture.
* \[ ] robustness scorecard fixture.
* \[ ] governance gate fixture.
* \[ ] Robustness API smoke.
* \[ ] dashboard browser smoke.
* \[ ] evidence bundle verify.

Acceptatiecriteria:

* \[ ] Fast check-all blijft snel.
* \[ ] Deep check-all dekt walk-forward/rebalancing end-to-end.
* \[ ] No-live failure hard fail.
* \[ ] Advice wording failure hard fail.
* \[ ] Reports secret-free.

\---

## 20\. Fase 17 - Operator/UAT Integration

Roadmap 102:

* \[ ] Operator manual krijgt Allocation Robustness Lab guide.
* \[ ] CLI cookbook krijgt walk-forward/rebalancing commands.
* \[ ] Troubleshooting krijgt data coverage/split/rebalance playbooks.
* \[ ] Evidence guide krijgt walk-forward evidence uitleg.

Roadmap 103:

* \[ ] UAT scenario: walk-forward split preview.
* \[ ] UAT scenario: dataset coverage audit.
* \[ ] UAT scenario: rebalancing schedule comparison.
* \[ ] UAT scenario: rolling simulation run op fixture.
* \[ ] UAT scenario: robustness scorecard bekijken.
* \[ ] UAT scenario: governance gate bekijken.
* \[ ] UAT scenario: no-live/no-advice/no-real-allocation proof controleren.
* \[ ] UAT scenario: evidence exporteren.

Acceptatiecriteria:

* \[ ] UAT scenarios pass.
* \[ ] Docs link valid.
* \[ ] No-live/no-advice proof included.
* \[ ] UAT feedback can create robustness-lab backlog items.
* \[ ] Browser smoke/UAT evidence linked.

\---

## 21\. Fase 18 - Release/Knowledge/Test/Performance Integration

Roadmap 089:

* \[ ] Release notes include Allocation Robustness Lab.
* \[ ] Version manifest includes walk-forward schema version.
* \[ ] Migration notes include walk-forward evidence path.

Roadmap 091:

* \[ ] Knowledge graph maps Portfolio Lab → Robustness Lab.
* \[ ] Impact analysis detects Portfolio Lab changes affecting Robustness Lab.
* \[ ] Ownership map includes robustness modules.

Roadmap 092:

* \[ ] Test selector chooses robustness tests for split/rebalance/scorecard changes.
* \[ ] Portfolio Lab changes select robustness integration tests.
* \[ ] Dashboard robustness UI changes select browser smoke.

Roadmap 093:

* \[ ] Performance budgets for window count, schedule count, simulation runtime, result payload and report size.
* \[ ] Heavy walk-forward simulations produce warnings/findings.
* \[ ] Rolling runtime trends stored locally.

Acceptatiecriteria:

* \[ ] Release evidence includes walk-forward evidence.
* \[ ] Knowledge graph updated.
* \[ ] Test selection works.
* \[ ] Performance reports include robustness budgets.
* \[ ] No-live proof preserved.

\---

## 22\. Fase 19 - Scheduled Robustness Reports

Scheduled jobs:

* \[ ] weekly dataset coverage audit.
* \[ ] weekly walk-forward smoke on latest paper portfolio research allocation.
* \[ ] weekly rebalancing schedule comparison.
* \[ ] weekly allocation decay monitor.
* \[ ] monthly robustness scorecard.
* \[ ] post-Portfolio-Lab-change robustness validation.
* \[ ] post-market-scanner-change candidate decay validation.
* \[ ] post-dashboard-change Robustness Lab smoke.

Metrics:

* \[ ] split count.
* \[ ] pass window ratio.
* \[ ] worst-window drawdown.
* \[ ] overfit gap.
* \[ ] schedule turnover.
* \[ ] fee drag.
* \[ ] decayed candidate count.
* \[ ] replacement event count.
* \[ ] robustness grade distribution.
* \[ ] governance gate status.
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

* \[ ] `tests/test\_walk\_forward\_robustness\_safety\_contract.py`
* \[ ] `tests/test\_walk\_forward\_splits.py`
* \[ ] `tests/test\_dataset\_coverage\_audit.py`
* \[ ] `tests/test\_rebalancing\_schedules.py`
* \[ ] `tests/test\_rebalance\_event\_simulator.py`
* \[ ] `tests/test\_rolling\_portfolio\_orchestrator.py`
* \[ ] `tests/test\_allocation\_decay.py`
* \[ ] `tests/test\_candidate\_replacement.py`
* \[ ] `tests/test\_walk\_forward\_performance.py`
* \[ ] `tests/test\_allocation\_robustness\_scorecards.py`
* \[ ] `tests/test\_robustness\_governance\_gate.py`
* \[ ] `tests/test\_walk\_forward\_evidence\_bundle.py`
* \[ ] `tests/test\_portfolio\_robustness\_api.py`
* \[ ] `tests/test\_portfolio\_robustness\_widgets.py`

### Integration tests

* \[ ] Build walk-forward splits from fixture basket.
* \[ ] Audit dataset coverage from fixture candles.
* \[ ] Validate rebalancing schedules.
* \[ ] Simulate rebalance events.
* \[ ] Run rolling portfolio simulation fixture.
* \[ ] Analyze allocation decay.
* \[ ] Simulate candidate replacement.
* \[ ] Generate walk-forward performance report.
* \[ ] Generate robustness scorecards.
* \[ ] Run governance gate.
* \[ ] Export evidence bundle.
* \[ ] Dashboard API TestClient smoke.

### Browser smoke

* \[ ] `/portfolio-lab/robustness` loads.
* \[ ] split builder visible.
* \[ ] dataset coverage panel visible.
* \[ ] rebalancing schedule selector visible.
* \[ ] rolling simulation preview works.
* \[ ] robustness scorecard visible.
* \[ ] governance gate visible.
* \[ ] evidence export visible.
* \[ ] no-live/no-advice/no-real-allocation banner visible.
* \[ ] no live controls visible.

### Safety tests

* \[ ] Live mode blocked.
* \[ ] Signed endpoint blocked.
* \[ ] Account endpoint blocked.
* \[ ] Order endpoint blocked.
* \[ ] Rolling simulation run requires paper-only confirm.
* \[ ] Runner works without API keys.
* \[ ] Advice wording blocked.
* \[ ] Real allocation wording blocked.
* \[ ] Out-of-sample claim blocked without split evidence.
* \[ ] Evidence secret-free.
* \[ ] Check-all safe env preserved.

\---

## 24\. Docs

Nieuwe docs:

```text
docs/portfolio-lab/walk-forward-robustness-safety-contract.md
docs/portfolio-lab/walk-forward-splits.md
docs/portfolio-lab/dataset-coverage-audit.md
docs/portfolio-lab/rebalancing-schedules.md
docs/portfolio-lab/rebalance-event-simulator.md
docs/portfolio-lab/rolling-portfolio-orchestrator.md
docs/portfolio-lab/allocation-decay.md
docs/portfolio-lab/candidate-replacement.md
docs/portfolio-lab/walk-forward-performance.md
docs/portfolio-lab/allocation-robustness-scorecards.md
docs/portfolio-lab/robustness-governance-gate.md
docs/portfolio-lab/walk-forward-evidence-bundle.md
docs/portfolio-lab/dashboard-v2-robustness-lab.md
docs/portfolio-lab/troubleshooting-robustness.md
```

README updates:

* \[ ] Allocation Robustness Lab overview.
* \[ ] Walk-forward validation workflow.
* \[ ] Paper-only/no-live statement.
* \[ ] No financial advice/no real allocation statement.
* \[ ] CLI examples.
* \[ ] Dashboard V2 route.
* \[ ] Evidence export.

Operator docs updates:

* \[ ] Robustness Lab quick start.
* \[ ] Split builder guide.
* \[ ] Rebalancing schedule interpretation.
* \[ ] Allocation decay interpretation.
* \[ ] Candidate replacement interpretation.
* \[ ] Governance gate troubleshooting.
* \[ ] No-live/no-advice proof.

\---

## 25\. Codex bouwvolgorde

### PR 1 - Safety Contract + Walk-Forward Split Schema

* \[ ] `docs/portfolio-lab/walk-forward-robustness-safety-contract.md`
* \[ ] `portfolio\_lab/walk\_forward\_splits.py`
* \[ ] split validation tests.
* \[ ] no-live/no-advice tests.

### PR 2 - Dataset Coverage Audit

* \[ ] `dataset\_coverage\_audit.py`
* \[ ] fixture candle coverage tests.
* \[ ] data gap tests.

### PR 3 - Rebalancing Schedules + Event Simulator

* \[ ] `rebalancing\_schedules.py`
* \[ ] `rebalance\_event\_simulator.py`
* \[ ] schedule/event tests.

### PR 4 - Rolling Portfolio Orchestrator

* \[ ] `rolling\_portfolio\_orchestrator.py`
* \[ ] fixture rolling simulation tests.
* \[ ] no signed/account/order tests.

### PR 5 - Allocation Decay + Candidate Replacement

* \[ ] `allocation\_decay.py`
* \[ ] `candidate\_replacement.py`
* \[ ] decay/replacement tests.

### PR 6 - Walk-Forward Performance + Robustness Scorecards

* \[ ] `walk\_forward\_performance.py`
* \[ ] `allocation\_robustness\_scorecards.py`
* \[ ] performance/score tests.

### PR 7 - Robustness Governance Gate

* \[ ] `robustness\_governance\_gate.py`
* \[ ] gate state tests.
* \[ ] out-of-sample proof tests.

### PR 8 - API + Dashboard Widgets

* \[ ] robustness API routes.
* \[ ] Dashboard widgets.
* \[ ] TestClient/frontend tests.

### PR 9 - Dashboard Workbench + Packs

* \[ ] Dashboard V2 robustness pages.
* \[ ] workspace/template packs.
* \[ ] browser smoke.

### PR 10 - Evidence, CLI, Check-All, Docs \& Integrations

* \[ ] `walk\_forward\_evidence\_bundle.py`
* \[ ] CLI commands.
* \[ ] check-all integration.
* \[ ] docs.
* \[ ] UAT scenarios.
* \[ ] release/knowledge/test/performance integration.
* \[ ] scheduled reports.

\---

## 26\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 115 PR 1: Walk-Forward Robustness Safety Contract + Walk-Forward Split Schema.

Maak docs/portfolio-lab/walk-forward-robustness-safety-contract.md.

Maak src/binance\_spot\_bot/portfolio\_lab/walk\_forward\_splits.py met:
- WalkForwardWindow
- WalkForwardSplit
- WalkForwardSplitConfig
- WalkForwardSplitValidationResult
- WalkForwardSplitReport
- validate\_walk\_forward\_split(split: WalkForwardSplit)
- walk\_forward\_split\_to\_dict(...)
- write\_walk\_forward\_split\_report(...)

WalkForwardWindow moet minimaal bevatten:
- window\_id
- train\_start\_ms
- train\_end\_ms
- validation\_start\_ms
- validation\_end\_ms
- test\_start\_ms optional
- test\_end\_ms optional
- symbols
- source\_dataset\_ids
- min\_candles\_required
- no\_live\_statement
- paper\_only\_research\_statement
- live\_trading\_enabled=False

WalkForwardSplit moet minimaal bevatten:
- split\_id
- mode
- windows
- created\_at\_ms
- symbols
- no\_live\_statement
- no\_financial\_advice\_statement
- paper\_only\_research\_statement
- live\_trading\_enabled=False

Validatie moet blokkeren op:
- live mode of live\_trading\_enabled=True
- ontbrekende no\_live\_statement
- ontbrekende no\_financial\_advice\_statement
- ontbrekende paper\_only\_research\_statement
- lege windows
- duplicate window\_id
- train\_end\_ms > validation\_start\_ms
- validation\_end\_ms > test\_start\_ms wanneer test bestaat
- end <= start in elk venster
- lege symbols
- min\_candles\_required <= 0
- buy/sell/financial advice wording
- real allocation wording
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
- valid split
- live\_trading\_enabled True blocked
- missing no\_live\_statement blocked
- missing no\_financial\_advice\_statement blocked
- missing paper\_only\_research\_statement blocked
- duplicate window\_id blocked
- invalid time order blocked
- empty symbols blocked
- invalid min\_candles\_required blocked
- advice wording blocked
- real allocation wording blocked
- JSON serialization
- secret-like values worden geredact
- live\_trading\_enabled=False
```

Waarom eerst:

* Walk-forward robustness kan pas veilig bouwen als split boundaries, no-live, paper-only en no-advice regels machine-testbaar zijn.
* Het is read-only en raakt runtime/trading/frontend niet.
* Het is klein genoeg voor Codex.
* Out-of-sample research krijgt direct een veilige basis.
* Daarna kunnen dataset coverage, rebalancing schedules en rolling simulations veilig op deze splits bouwen.

\---

## 27\. Definition of Done

Roadmap 115 is klaar als:

* \[ ] Walk-Forward Robustness Safety Contract bestaat.
* \[ ] Walk-Forward Split Schema werkt.
* \[ ] Dataset Coverage \& Candle Availability Audit werkt.
* \[ ] Rebalancing Schedule Schema werkt.
* \[ ] Rebalance Event Simulator werkt.
* \[ ] Rolling Portfolio Simulation Orchestrator werkt.
* \[ ] Allocation Decay Monitor werkt.
* \[ ] Candidate Replacement Simulator werkt.
* \[ ] Walk-Forward Performance Analyzer werkt.
* \[ ] Allocation Robustness Scorecards werken.
* \[ ] Robustness Governance Gate werkt.
* \[ ] Walk-Forward Evidence Bundle werkt.
* \[ ] Dashboard V2 Allocation Robustness Lab werkt.
* \[ ] Dashboard Widgets \& Workspace Packs werken.
* \[ ] Robustness API werkt.
* \[ ] CLI commands werken.
* \[ ] Check-All Integration werkt.
* \[ ] Operator/UAT Integration werkt.
* \[ ] Release/Knowledge/Test/Performance Integration werkt.
* \[ ] Scheduled Robustness Reports werken.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen runner zonder API keys werkt.
* \[ ] Tests bewijzen geen financieel advies of real allocation wording.
* \[ ] Tests bewijzen out-of-sample claims split evidence vereisen.
* \[ ] Tests bewijzen evidence secret-free is.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Robustness Lab is local-only en paper-only.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 115 kan na uitvoering naar `Voltooid docs`.

\---

## 28\. Verwachte Roadmap 116 daarna

Als Roadmap 115 groen is:

```text
Roadmap 116 - Local Paper Portfolio Governance, Research Approval Workflows \& Candidate Lifecycle Management
```

Mogelijke inhoud:

* \[ ] lifecycle van candidates;
* \[ ] research approvals;
* \[ ] review notes;
* \[ ] expiration/decay policies;
* \[ ] promotion/demotion binnen paper-only research;
* \[ ] governance evidence;
* \[ ] still no live trading.

```

Als Roadmap 115 performanceproblemen vindt:

```text
Roadmap 116 - Walk-Forward Simulation Performance Burn-Down, Rolling Cache \& Large Window Optimization
```

Mogelijke inhoud:

* \[ ] rolling simulation cache;
* \[ ] split scheduling optimalisatie;
* \[ ] result reuse;
* \[ ] heavy window warnings;
* \[ ] dashboard chart virtualization;
* \[ ] still no live trading.

```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Walk-forward rebalance research and allocation robustness lab.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.

## Uitvoering 2026-05-15

Status: Voltooid / Gevalideerd.

Gebouwd:

- Walk-forward split schema en validatie.
- Dataset coverage audit.
- Rebalancing schedules en rebalance event simulator.
- Rolling portfolio orchestrator bovenop Portfolio Lab simulatie.
- Allocation decay monitor en candidate replacement simulator.
- Walk-forward performance analyzer.
- Allocation robustness scorecards en governance gate.
- Walk-forward evidence bundle.
- Dashboard V2 Robustness Lab API routes en `/portfolio-lab/robustness` UI.
- Robustness widgets, CLI commands en check-all integratie.
- Robustness docs en acceptance tests.

Validatie:

- `python -m compileall -q src tests`
- `python -m pytest -q tests/test_roadmap_115_portfolio_robustness_acceptance.py` -> 5 passed.
- CLI smokes inclusief rolling-simulation confirm-gate.
- `npm install; npm run build`
- `python -m binance_spot_bot.cli security-scan` -> geen findings.
- `python -m binance_spot_bot.cli dashboard-v2-smoke --json` -> ok.
- `python -m binance_spot_bot.cli check-all --skip-tests --json` -> ok.
- Browser render `/portfolio-lab/robustness` screenshot: `%TEMP%/portfolio-robustness-115.png`.
- `python -m pytest -q` -> 442 passed, 1 warning.

Safety:

- Geen API keys nodig.
- Geen signed/account/order endpoints.
- Rolling simulation vereist `RUN_WALK_FORWARD_PAPER_RESEARCH_ONLY`.
- Alle Robustness Lab responses houden `live_trading_enabled=false`.

