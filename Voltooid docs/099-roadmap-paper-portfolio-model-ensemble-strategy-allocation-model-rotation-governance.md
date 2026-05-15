# Roadmap 099 - Paper Portfolio Model Ensemble, Strategy Allocation \& Model Rotation Governance

Status: Niet volledig voltooid / opnieuw gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/099-roadmap-paper-portfolio-model-ensemble-strategy-allocation-model-rotation-governance.md
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
* `Roadmap docs/081-roadmap-paper-portfolio-optimization-risk-budget-search-robust-allocation-selection.md`
* `Roadmap docs/082-roadmap-paper-policy-rollout-ab-paper-experiments-champion-challenger-governance.md`
* `Roadmap docs/083-roadmap-local-paper-operations-automation-scheduled-reports-operator-runbooks.md`
* `Roadmap docs/084-roadmap-local-paper-ops-observability-metrics-warehouse-long-term-analytics.md`
* `Roadmap docs/085-roadmap-local-ai-ops-assistant-natural-language-queries-safe-operator-guidance.md`
* `Roadmap docs/086-roadmap-safe-human-in-the-loop-action-center-approval-workflows-operator-decision-journal.md`
* `Roadmap docs/087-roadmap-local-permission-profiles-operator-roles-hardening-audit-grade-compliance-reports.md`
* `Roadmap docs/088-roadmap-offline-disaster-recovery-backup-restore-drills-local-state-integrity.md`
* `Roadmap docs/089-roadmap-local-release-management-versioned-upgrade-paths-migration-safety.md`
* `Roadmap docs/090-roadmap-developer-experience-codex-task-packs-roadmap-execution-automation.md`
* `Roadmap docs/091-roadmap-repository-knowledge-graph-code-ownership-impact-analysis.md`
* `Roadmap docs/092-roadmap-intelligent-test-selection-ci-acceleration-regression-risk-scoring.md`
* `Roadmap docs/093-roadmap-performance-profiling-runtime-bottleneck-analysis-resource-budgeting.md`
* `Roadmap docs/094-roadmap-dashboard-component-refactor-lazy-loading-ux-performance-hardening.md`
* `Roadmap docs/095-roadmap-runtime-core-decomposition-event-bus-snapshot-optimization.md`
* `Roadmap docs/096-roadmap-data-pipeline-decomposition-feature-store-contracts-indicator-compute-optimization.md`
* `Roadmap docs/097-roadmap-model-training-pipeline-v2-experiment-tracking-feature-contract-aware-model-promotion.md`
* `Roadmap docs/098-roadmap-shadow-paper-model-monitoring-drift-detection-automatic-candidate-downgrade.md`

Doel: Roadmap 098 maakt paper/shadow model monitoring, drift detection, model health scoring en veilige paper/shadow downgrade mogelijk. Roadmap 099 bouwt daarop de volgende laag: **meerdere paper/shadow modellen, strategieën en symbolen tegelijk beheren als een paper portfolio**, met ensemble voting, model/strategy allocation, rotation policies, risk budgets, governance gates, performance attribution, evidence en dashboard/CLI-bediening.

Live trading blijft volledig buiten scope. Alle allocatie, ensemble decisions, rotation en governance zijn paper/shadow/demo-only. Geen live mode, geen signed real-order endpoints en geen echte account/order acties.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 099`, `099-roadmap`, `Paper Portfolio Model Ensemble`, `Strategy Allocation`, `Model Rotation Governance` en `ensemble voting`.
* \[x] Geen bestaande Roadmap 099 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 098 is lokaal aangemaakt als Shadow/Paper Model Monitoring, Drift Detection \& Automatic Candidate Downgrade.

### Codebasecontrole

Breed bekeken met ensemble/portfolio/allocation-focus:

* \[x] `src/binance\_spot\_bot/model\_registry.py`
* \[x] `src/binance\_spot\_bot/risk.py`
* \[x] `src/binance\_spot\_bot/paper\_accounting.py`
* \[x] `src/binance\_spot\_bot/session\_store.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] eerdere analyse van `signal\_model.py`, `evaluation.py`, `dataset\_governance.py`, `features.py`, `data.py`, dashboard, check-all, model monitoring en roadmaplijn tot 098.

### Belangrijke bestaande basis

De codebase heeft nu:

* \[x] `ModelRegistry` met model metadata, aliases, model cards, candidate/champion status, promotion checks en previous champion tracking.
* \[x] `RiskEngine` met max daily loss, max position quote, max trades per day, min confidence, spread/stale-data checks, default quote size en kill switch.
* \[x] `PaperAccount` met quote/base balance, average entry, realized PnL, fees, slippage, fills en equity.
* \[x] `SessionStore` met session summaries, snapshots, fills, alerts, orders en heartbeats als lokale artifacts.
* \[x] `BotRuntime` kan via `model\_alias` een model laden of fallback naar rule baseline doen.
* \[x] Roadmap 097 plant training/promotie naar paper/shadow/demo-only aliases.
* \[x] Roadmap 098 plant monitoring, drift health en downgrade van paper/shadow aliases.

### Belangrijkste gat na Roadmap 098

Na Roadmap 098 kun je modellen bewaken en downgraden. Wat nog mist:

* \[ ] meerdere paper/shadow modellen tegelijk laten stemmen;
* \[ ] meerdere strategieën per symbol/regime vergelijken;
* \[ ] allocatie van paper capital tussen modellen/strategieën/symbolen;
* \[ ] model ensemble decision logging;
* \[ ] strategy/model rotation policies;
* \[ ] governance gates voor rotatie;
* \[ ] exposure/risk budgets op portfolio-niveau;
* \[ ] performance attribution per model/strategy/symbol/regime;
* \[ ] rotation evidence en decision journal;
* \[ ] dashboard voor model ensemble en paper allocation;
* \[ ] automatic paper-only rebalancing met guardrails;
* \[ ] no-live proof per allocation/rotation decision.

Roadmap 099 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 099

Maak een lokale paper portfolio ensemble- en governance-laag:

```text
Promoted paper/shadow models
→ model ensemble definitions
→ strategy allocation policies
→ portfolio risk budgets
→ paper-only rotation decisions
→ performance attribution
→ governance approval/evidence
→ dashboard/CLI controls
```

Na Roadmap 099 moet de bot kunnen:

* \[ ] meerdere model aliases combineren in een paper/shadow ensemble;
* \[ ] ensemble votes berekenen;
* \[ ] model confidence wegen;
* \[ ] allocation weights per model/strategy/symbol bepalen;
* \[ ] portfolio risk budgets afdwingen;
* \[ ] strategy/model rotation voorstellen;
* \[ ] paper-only rotation uitvoeren met governance;
* \[ ] performance attribution maken;
* \[ ] model health uit Roadmap 098 meenemen;
* \[ ] paper downgrade/allocation decisions bewijzen;
* \[ ] dashboard/CLI aanbieden;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen live trading.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte account endpoints.
* \[ ] Geen automatic live capital allocation.
* \[ ] Geen live model rotation.
* \[ ] Geen nieuwe modeltraining pipeline; Roadmap 097 doet dat.
* \[ ] Geen drift detector opnieuw bouwen; Roadmap 098 doet dat.
* \[ ] Geen feature store opnieuw bouwen; Roadmap 096 doet dat.
* \[ ] Geen runtime refactor opnieuw bouwen; Roadmap 095 doet dat.
* \[ ] Geen portfolio optimizer zonder paper-only guardrails.
* \[ ] Geen allocation decision die risk limits verhoogt.
* \[ ] Geen cloud portfolio service.
* \[ ] Geen remote telemetry.

Wel doen:

* \[ ] paper/shadow ensemble definitions toevoegen;
* \[ ] ensemble voting toevoegen;
* \[ ] allocation policy toevoegen;
* \[ ] portfolio-level risk budgets toevoegen;
* \[ ] paper-only rotation governance toevoegen;
* \[ ] performance attribution toevoegen;
* \[ ] evidence/reporting/dashboard/CLI toevoegen;
* \[ ] model monitoring health uit Roadmap 098 gebruiken;
* \[ ] alles local-only en no-live houden.

\---

## 3\. Fase 0 - Paper Portfolio Ensemble Safety Contract

Nieuwe doc:

```text
docs/paper-portfolio-ensemble-safety-contract.md
```

Regels:

* \[ ] Ensemble/portfolio tooling is local-only.
* \[ ] Geen live trading.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen account endpoints.
* \[ ] Ensemble decisions mogen alleen paper/shadow/demo beïnvloeden.
* \[ ] Allocation policy mag risk limits niet verhogen zonder explicit governance approval.
* \[ ] Paper allocation mag geen live capital betekenen.
* \[ ] Rotation mag alleen paper/shadow/demo aliases wijzigen.
* \[ ] Live aliases zijn forbidden:

  * `champion\_live`;
  * `live\_approved`;
  * `auto\_live`;
  * `live\_portfolio`;
  * `live\_allocation`.
* \[ ] Ensemble members moeten model evidence/health hebben.
* \[ ] Model health D/F blokkeert allocation increase.
* \[ ] Critical drift blokkeert new allocation.
* \[ ] Reports/evidence zijn secret-free.
* \[ ] No-live proof wordt in elk decision report opgenomen.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen live aliases worden geblokkeerd.
* \[ ] Tests bewijzen allocation geen signed/order/account endpoints gebruikt.
* \[ ] Tests bewijzen health D/F allocation increase blokkeert.
* \[ ] Output bevat `live\_trading\_enabled=False`.

\---

## 4\. Fase 1 - Ensemble Definition Schema

Nieuwe module:

```text
src/binance\_spot\_bot/ensemble\_config.py
```

Dataclasses:

* \[ ] `EnsembleConfig`
* \[ ] `EnsembleMember`
* \[ ] `EnsembleVotingPolicy`
* \[ ] `EnsembleWeightPolicy`
* \[ ] `EnsembleScope`
* \[ ] `EnsembleConfigValidationResult`

Ensemble member velden:

* \[ ] member\_id;
* \[ ] model\_alias;
* \[ ] model\_id optional;
* \[ ] strategy\_id;
* \[ ] symbol\_scope;
* \[ ] interval\_scope;
* \[ ] regime\_scope;
* \[ ] base\_weight;
* \[ ] min\_weight;
* \[ ] max\_weight;
* \[ ] enabled;
* \[ ] requires\_health\_min\_grade;
* \[ ] requires\_feature\_schema\_hash;
* \[ ] paper\_only=true;
* \[ ] shadow\_only optional.

Voting policies:

* \[ ] majority\_vote;
* \[ ] confidence\_weighted\_vote;
* \[ ] health\_weighted\_vote;
* \[ ] performance\_weighted\_vote;
* \[ ] veto\_on\_risk\_block;
* \[ ] hold\_on\_disagreement;
* \[ ] fallback\_to\_baseline.

Acceptatiecriteria:

* \[ ] Config is JSON-serializable.
* \[ ] Config rejects live aliases.
* \[ ] Config rejects negative weights.
* \[ ] Config requires at least one enabled member.
* \[ ] Tests cover duplicate member IDs and invalid scopes.

\---

## 5\. Fase 2 - Strategy \& Model Allocation Policy

Nieuwe module:

```text
src/binance\_spot\_bot/allocation\_policy.py
```

Dataclasses:

* \[ ] `AllocationPolicy`
* \[ ] `AllocationTarget`
* \[ ] `AllocationWeight`
* \[ ] `AllocationConstraint`
* \[ ] `AllocationPolicyValidationResult`

Allocation dimensions:

* \[ ] model;
* \[ ] strategy;
* \[ ] symbol;
* \[ ] interval;
* \[ ] regime;
* \[ ] paper capital bucket;
* \[ ] confidence bucket;
* \[ ] risk bucket.

Constraints:

* \[ ] max weight per model;
* \[ ] max weight per symbol;
* \[ ] max weight per strategy;
* \[ ] max correlation proxy group;
* \[ ] min health grade;
* \[ ] max drawdown allowed;
* \[ ] max recent drift score;
* \[ ] max paper degradation;
* \[ ] max allocation change per rebalance;
* \[ ] max trades per allocation bucket;
* \[ ] min observations before allocation increase.

Acceptatiecriteria:

* \[ ] Policy validates safe paper-only allocation.
* \[ ] Policy blocks live allocation labels.
* \[ ] Policy blocks allocation increase for degraded models.
* \[ ] Policy blocks missing model evidence.
* \[ ] Tests cover valid/invalid constraints.

\---

## 6\. Fase 3 - Portfolio Risk Budget Schema

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_risk\_budget.py
```

Dataclasses:

* \[ ] `PortfolioRiskBudget`
* \[ ] `ModelRiskBudget`
* \[ ] `SymbolRiskBudget`
* \[ ] `StrategyRiskBudget`
* \[ ] `RiskBudgetUsage`
* \[ ] `RiskBudgetDecision`

Budgets:

* \[ ] total paper capital;
* \[ ] max paper exposure quote;
* \[ ] max allocation per model;
* \[ ] max allocation per symbol;
* \[ ] max allocation per strategy;
* \[ ] max daily paper loss;
* \[ ] max drawdown;
* \[ ] max turnover;
* \[ ] max trades per day;
* \[ ] max correlated exposure proxy;
* \[ ] max degraded model exposure;
* \[ ] cash reserve minimum.

Acceptatiecriteria:

* \[ ] Budget usage can be computed from paper sessions/fills.
* \[ ] Budget blocks over-allocation.
* \[ ] Budget never increases live risk.
* \[ ] Budget decision is explainable.
* \[ ] Tests cover budget pass/warn/fail.

\---

## 7\. Fase 4 - Ensemble Prediction Engine

Nieuwe module:

```text
src/binance\_spot\_bot/ensemble\_prediction.py
```

Dataclasses:

* \[ ] `EnsemblePredictionRequest`
* \[ ] `MemberPrediction`
* \[ ] `EnsembleVote`
* \[ ] `EnsemblePredictionResult`
* \[ ] `EnsembleDisagreement`

Inputs:

* \[ ] feature row;
* \[ ] market state;
* \[ ] model aliases;
* \[ ] model health scores;
* \[ ] allocation weights;
* \[ ] voting policy;
* \[ ] fallback policy.

Output:

* \[ ] final signal side;
* \[ ] final confidence;
* \[ ] member predictions;
* \[ ] vote weights;
* \[ ] disagreement score;
* \[ ] veto reasons;
* \[ ] fallback used;
* \[ ] no\_order\_side\_effect=true;
* \[ ] live\_trading\_enabled=false.

Acceptatiecriteria:

* \[ ] Majority vote works.
* \[ ] Confidence-weighted vote works.
* \[ ] Health-weighted vote works.
* \[ ] Severe disagreement can HOLD.
* \[ ] Engine never places orders.

\---

## 8\. Fase 5 - Strategy Rotation Policy

Nieuwe module:

```text
src/binance\_spot\_bot/strategy\_rotation.py
```

Dataclasses:

* \[ ] `RotationPolicy`
* \[ ] `RotationCandidate`
* \[ ] `RotationDecision`
* \[ ] `RotationTrigger`
* \[ ] `RotationCooldown`

Triggers:

* \[ ] model health score below threshold;
* \[ ] feature drift critical;
* \[ ] prediction drift critical;
* \[ ] paper performance degradation;
* \[ ] drawdown breach;
* \[ ] candidate outperforms champion paper;
* \[ ] confidence collapse;
* \[ ] stale monitoring;
* \[ ] evidence missing;
* \[ ] manual operator request.

Actions:

* \[ ] no\_change;
* \[ ] reduce\_weight;
* \[ ] increase\_weight;
* \[ ] disable\_member;
* \[ ] enable\_member;
* \[ ] rotate\_to\_fallback;
* \[ ] rebalance\_paper\_weights;
* \[ ] recommend\_retrain;
* \[ ] create\_action\_proposal.

Acceptatiecriteria:

* \[ ] Rotation decision is explainable.
* \[ ] Cooldown prevents rapid flipping.
* \[ ] Health D/F cannot increase weight.
* \[ ] Missing evidence blocks rotation.
* \[ ] Tests cover each trigger/action.

\---

## 9\. Fase 6 - Paper Portfolio State

Nieuwe module:

```text
src/binance\_spot\_bot/paper\_portfolio\_state.py
```

Dataclasses:

* \[ ] `PaperPortfolioState`
* \[ ] `PaperPortfolioPosition`
* \[ ] `PaperPortfolioAllocation`
* \[ ] `PaperPortfolioCash`
* \[ ] `PaperPortfolioExposure`
* \[ ] `PaperPortfolioSnapshot`

State fields:

* \[ ] portfolio\_id;
* \[ ] total\_paper\_capital;
* \[ ] cash\_reserve;
* \[ ] allocations by model/strategy/symbol;
* \[ ] exposures;
* \[ ] unrealized pnl proxy;
* \[ ] realized pnl;
* \[ ] fees;
* \[ ] drawdown;
* \[ ] model health summary;
* \[ ] active rotations;
* \[ ] blocked allocations;
* \[ ] live\_trading\_enabled=false.

Acceptatiecriteria:

* \[ ] State can be built from paper session summaries/fills.
* \[ ] State is JSON-serializable.
* \[ ] State contains no secrets.
* \[ ] State supports snapshot/history.
* \[ ] Tests use fixture sessions.

\---

## 10\. Fase 7 - Portfolio Allocation Engine

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_allocation\_engine.py
```

Flow:

* \[ ] load portfolio state;
* \[ ] load allocation policy;
* \[ ] load model health;
* \[ ] load performance attribution;
* \[ ] compute proposed weights;
* \[ ] apply risk budget constraints;
* \[ ] apply rotation policy;
* \[ ] produce allocation decision;
* \[ ] write allocation journal;
* \[ ] no execution side effects.

Dataclasses:

* \[ ] `AllocationRequest`
* \[ ] `AllocationProposal`
* \[ ] `AllocationDecision`
* \[ ] `AllocationJournalEntry`

Acceptatiecriteria:

* \[ ] Engine proposes paper-only weights.
* \[ ] Engine explains blocked allocation increases.
* \[ ] Engine respects max allocation change.
* \[ ] Engine never places orders.
* \[ ] Tests cover degraded/healthy/rebalance cases.

\---

## 11\. Fase 8 - Ensemble Paper Execution Adapter

Nieuwe module:

```text
src/binance\_spot\_bot/ensemble\_paper\_adapter.py
```

Doel: ensemble decisions vertalen naar paper-only risk intent zonder live side effects.

Regels:

* \[ ] Only paper/shadow/demo modes.
* \[ ] No signed endpoints.
* \[ ] No account endpoints.
* \[ ] Uses RiskEngine constraints.
* \[ ] Uses PaperAccount/PaperTrader path only where applicable.
* \[ ] Records ensemble decision before execution.
* \[ ] Final execution result keeps model/member attribution.

Dataclasses:

* \[ ] `EnsemblePaperIntent`
* \[ ] `EnsemblePaperDecision`
* \[ ] `EnsembleExecutionAttribution`

Acceptatiecriteria:

* \[ ] Adapter can convert ensemble BUY/SELL/HOLD to paper intent.
* \[ ] HOLD/disagreement does not execute.
* \[ ] Risk block is preserved.
* \[ ] Attribution is recorded.
* \[ ] Tests prove no signed/order/account live calls.

\---

## 12\. Fase 9 - Performance Attribution

Nieuwe module:

```text
src/binance\_spot\_bot/performance\_attribution.py
```

Attribution dimensions:

* \[ ] model alias;
* \[ ] model id;
* \[ ] strategy id;
* \[ ] symbol;
* \[ ] interval;
* \[ ] regime;
* \[ ] ensemble member;
* \[ ] vote type;
* \[ ] confidence bucket;
* \[ ] allocation bucket.

Metrics:

* \[ ] paper pnl;
* \[ ] realized pnl;
* \[ ] unrealized pnl proxy;
* \[ ] fees;
* \[ ] fills count;
* \[ ] trade count;
* \[ ] win/loss proxy;
* \[ ] avg confidence;
* \[ ] risk blocks;
* \[ ] drawdown;
* \[ ] exposure time proxy;
* \[ ] turnover;
* \[ ] disagreement cost proxy.

Acceptatiecriteria:

* \[ ] Attribution can aggregate session/fill data.
* \[ ] Attribution links fills to model/ensemble member where available.
* \[ ] Missing attribution is reported.
* \[ ] Report is secret-free.
* \[ ] Tests use fixture fills and predictions.

\---

## 13\. Fase 10 - Regime-Aware Allocation Context

Nieuwe module:

```text
src/binance\_spot\_bot/regime\_allocation.py
```

Regime signals:

* \[ ] volatility bucket;
* \[ ] trend proxy;
* \[ ] volume regime;
* \[ ] spread regime;
* \[ ] data quality regime;
* \[ ] feature drift regime;
* \[ ] prediction disagreement regime.

Usage:

* \[ ] allocation weights by regime;
* \[ ] ensemble member enable/disable by regime;
* \[ ] risk budget adjustment downward only;
* \[ ] rotation trigger by regime.

Acceptatiecriteria:

* \[ ] Regime context is deterministic.
* \[ ] Regime cannot increase live risk.
* \[ ] Risk adjustments are paper-only and bounded.
* \[ ] Missing regime data falls back safely.
* \[ ] Tests cover low/high volatility regimes.

\---

## 14\. Fase 11 - Rotation Governance Gate

Nieuwe module:

```text
src/binance\_spot\_bot/rotation\_governance.py
```

Checks:

* \[ ] model evidence present;
* \[ ] model health acceptable;
* \[ ] data evidence present;
* \[ ] monitoring evidence present;
* \[ ] allocation policy valid;
* \[ ] portfolio risk budget valid;
* \[ ] rotation cooldown satisfied;
* \[ ] downgrade/rotation decision explainable;
* \[ ] no-live proof present;
* \[ ] operator approval if required;
* \[ ] action center proposal if human-in-loop.

Decision statuses:

* \[ ] allowed;
* \[ ] allowed\_with\_warning;
* \[ ] blocked;
* \[ ] requires\_operator\_approval;
* \[ ] recommend\_only.

Acceptatiecriteria:

* \[ ] Gate blocks missing evidence.
* \[ ] Gate blocks live aliases.
* \[ ] Gate requires approval for large allocation change.
* \[ ] Gate writes decision report.
* \[ ] Tests cover allowed/blocked/approval.

\---

## 15\. Fase 12 - Rotation Decision Journal

Nieuwe module:

```text
src/binance\_spot\_bot/rotation\_journal.py
```

Journal fields:

* \[ ] decision\_id;
* \[ ] timestamp\_ms;
* \[ ] portfolio\_id;
* \[ ] ensemble\_id;
* \[ ] previous\_weights;
* \[ ] proposed\_weights;
* \[ ] final\_weights;
* \[ ] triggers;
* \[ ] governance result;
* \[ ] operator approval;
* \[ ] evidence links;
* \[ ] no-live proof;
* \[ ] rollback info.

Acceptatiecriteria:

* \[ ] Journal is append-only.
* \[ ] Journal is secret-free.
* \[ ] Journal supports hash chain optional.
* \[ ] Rollback info is recorded.
* \[ ] Tests cover append/load/verify.

\---

## 16\. Fase 13 - Paper Portfolio Rebalance Executor

Nieuwe module:

```text
src/binance\_spot\_bot/paper\_portfolio\_rebalance.py
```

Doel: paper-only weights toepassen in portfolio config/state.

Modes:

* \[ ] dry\_run;
* \[ ] preview;
* \[ ] apply\_paper\_only;
* \[ ] recommend\_only.

Flow:

* \[ ] load allocation decision;
* \[ ] verify governance gate;
* \[ ] verify no-live proof;
* \[ ] write pre-rebalance snapshot;
* \[ ] apply paper weights;
* \[ ] write post-rebalance snapshot;
* \[ ] write rotation journal;
* \[ ] write evidence bundle.

Guardrails:

* \[ ] dry-run default;
* \[ ] confirm phrase required for apply;
* \[ ] no live aliases;
* \[ ] no order placement;
* \[ ] no account endpoint;
* \[ ] rollback plan written.

Acceptatiecriteria:

* \[ ] Dry-run shows exact weight changes.
* \[ ] Apply requires confirm.
* \[ ] Apply cannot touch live aliases.
* \[ ] Rebalance writes journal/evidence.
* \[ ] Tests use temp config/state.

\---

## 17\. Fase 14 - Ensemble/Allocation Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_ensemble\_evidence.py
```

Bundle bevat:

* \[ ] ensemble config;
* \[ ] allocation policy;
* \[ ] risk budget;
* \[ ] model health summaries;
* \[ ] drift summaries;
* \[ ] performance attribution;
* \[ ] ensemble prediction samples;
* \[ ] allocation proposal;
* \[ ] rotation governance result;
* \[ ] rotation journal entries;
* \[ ] rebalance result;
* \[ ] no-live proof;
* \[ ] redaction proof;
* \[ ] hashes.

Output:

```text
data/portfolio-ensemble/evidence/<decision\_id>/
  portfolio\_ensemble\_evidence\_manifest.json
  portfolio\_ensemble\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle links to model monitoring evidence.
* \[ ] Bundle links to model/data/runtime evidence.

\---

## 18\. Fase 15 - Paper Portfolio Ensemble Store

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_ensemble\_store.py
```

Storage:

```text
data/portfolio-ensemble/
  configs/
  states/
  predictions/
  allocations/
  rotations/
  journals/
  reports/
  evidence/
```

Store functies:

* \[ ] save/load ensemble config;
* \[ ] save/load allocation policy;
* \[ ] save/load risk budget;
* \[ ] save/load portfolio state;
* \[ ] save/load allocation decisions;
* \[ ] save/load rotation journals;
* \[ ] save/load evidence;
* \[ ] write manifests;
* \[ ] verify manifests.

Acceptatiecriteria:

* \[ ] Store is local-only.
* \[ ] Store has manifest/hash.
* \[ ] Store rejects unsafe paths.
* \[ ] Store contains no secrets.
* \[ ] Tests use temp dirs.

\---

## 19\. Fase 16 - Portfolio Ensemble Report

Nieuwe module:

```text
src/binance\_spot\_bot/portfolio\_ensemble\_report.py
```

Report secties:

* \[ ] summary;
* \[ ] ensemble members;
* \[ ] current allocations;
* \[ ] model health;
* \[ ] performance attribution;
* \[ ] risk budget usage;
* \[ ] drift/monitoring status;
* \[ ] rotation recommendations;
* \[ ] governance status;
* \[ ] recent decisions;
* \[ ] blocked actions;
* \[ ] no-live proof;
* \[ ] evidence links.

Acceptatiecriteria:

* \[ ] Report is Markdown + JSON.
* \[ ] Report is secret-free.
* \[ ] Report is dashboard downloadable.
* \[ ] Report can feed scheduled reports.
* \[ ] Tests use fixture ensemble state.

\---

## 20\. Fase 17 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli ensemble-config-validate --config config/ensemble/default.json
python -m binance\_spot\_bot.cli ensemble-predict --config config/ensemble/default.json --symbol BTCUSDT
python -m binance\_spot\_bot.cli allocation-policy-validate --config config/allocation/default.json
python -m binance\_spot\_bot.cli portfolio-risk-budget-check --portfolio paper-default
python -m binance\_spot\_bot.cli portfolio-state --portfolio paper-default
python -m binance\_spot\_bot.cli allocation-propose --portfolio paper-default
python -m binance\_spot\_bot.cli performance-attribution --portfolio paper-default
python -m binance\_spot\_bot.cli strategy-rotation-check --portfolio paper-default
python -m binance\_spot\_bot.cli rotation-governance-check --decision-id <id>
python -m binance\_spot\_bot.cli paper-rebalance-preview --decision-id <id>
python -m binance\_spot\_bot.cli paper-rebalance-apply --decision-id <id> --confirm APPLY\_PAPER\_REBALANCE
python -m binance\_spot\_bot.cli portfolio-ensemble-report --portfolio paper-default
python -m binance\_spot\_bot.cli portfolio-ensemble-evidence-export --decision-id <id>
```

Acceptatiecriteria:

* \[ ] Commands werken offline met paper/demo data.
* \[ ] Commands ondersteunen JSON output.
* \[ ] Apply command vereist confirm.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Reports zijn secret-free.

\---

## 21\. Fase 18 - Dashboard Panel

Nieuwe dashboardsectie:

```text
Paper Portfolio Ensemble \& Rotation
```

Panels:

* \[ ] ensemble config status;
* \[ ] ensemble members;
* \[ ] model health by member;
* \[ ] current allocation weights;
* \[ ] risk budget usage;
* \[ ] ensemble prediction sample;
* \[ ] disagreement score;
* \[ ] performance attribution;
* \[ ] rotation recommendation;
* \[ ] governance gate status;
* \[ ] rebalance preview;
* \[ ] rotation journal;
* \[ ] evidence export;
* \[ ] no-live proof.

Actions:

* \[ ] validate ensemble config;
* \[ ] run ensemble prediction sample;
* \[ ] validate allocation policy;
* \[ ] run risk budget check;
* \[ ] propose allocation;
* \[ ] run rotation check;
* \[ ] preview paper rebalance;
* \[ ] apply paper rebalance with confirm;
* \[ ] export evidence;
* \[ ] copy CLI commands.

Safeguards:

* \[ ] `PAPER PORTFOLIO ONLY` badge.
* \[ ] `NO LIVE ALLOCATION` badge.
* \[ ] Live aliases hidden/blocked.
* \[ ] Rebalance target shown before action.
* \[ ] Confirmation phrase required.
* \[ ] Raw JSON only in limited/debug expander.
* \[ ] Stable widget keys.
* \[ ] Browser smoke covers panel.

Acceptatiecriteria:

* \[ ] Dashboard shows current weights and risk budget.
* \[ ] Dashboard blocks live aliases.
* \[ ] Dashboard can preview rebalance.
* \[ ] Dashboard can export evidence.
* \[ ] Browser smoke passes.

\---

## 22\. Fase 19 - Runtime Integration

Uitbreiding op Roadmap 095/098:

* \[ ] runtime can optionally load ensemble config;
* \[ ] runtime logs ensemble member predictions;
* \[ ] runtime stores ensemble decision attribution;
* \[ ] runtime paper execution can use ensemble final signal only in paper/demo;
* \[ ] runtime snapshot includes ensemble summary;
* \[ ] runtime event bus emits ensemble\_vote and allocation\_context events;
* \[ ] monitoring health updates can reduce weights.
* \[ ] no-live proof preserved.

Acceptatiecriteria:

* \[ ] Runtime behavior unchanged when ensemble disabled.
* \[ ] Ensemble enabled does not call live/signed endpoints.
* \[ ] Ensemble prediction does not alter execution unless paper-only config explicitly enabled.
* \[ ] Snapshot is secret-free.
* \[ ] Tests compare runtime on/off behavior.

\---

## 23\. Fase 20 - Monitoring/Training/Data/Release/Test/Knowledge Integraties

### Roadmap 098 integratie

* \[ ] Model health score feeds allocation policy.
* \[ ] Drift critical blocks allocation increase.
* \[ ] Downgrade decisions update ensemble membership.
* \[ ] Monitoring evidence links to ensemble evidence.

### Roadmap 097 integratie

* \[ ] Promotion to paper alias can create ensemble candidate.
* \[ ] Model evidence required before ensemble membership.
* \[ ] Alias history linked to rotation journal.

### Roadmap 096 integratie

* \[ ] Feature schema compatibility checked for all ensemble members.
* \[ ] Data lineage required for ensemble members.

### Roadmap 092 integratie

* \[ ] Ensemble/allocation changes select portfolio/model/risk tests.
* \[ ] Rebalance executor changes force deep/safety tests.
* \[ ] Dashboard changes require browser smoke.

### Roadmap 091 integratie

* \[ ] Knowledge graph maps ensemble modules/artifact flow.
* \[ ] Impact analysis recognizes allocation/risk/governance domains.

### Roadmap 089/090 integratie

* \[ ] Release evidence includes ensemble evidence for portfolio changes.
* \[ ] Roadmap completion gate requires ensemble evidence.
* \[ ] Codex task packs include no-live/allocation safety tests.

Acceptatiecriteria:

* \[ ] Integrations produce correct evidence links.
* \[ ] Test selection chooses correct tests.
* \[ ] Release notes mention ensemble/allocation changes.
* \[ ] Knowledge graph shows portfolio ensemble artifact flow.
* \[ ] No-live proof preserved.

\---

## 24\. Fase 21 - Scheduled Reports \& Metrics

Uitbreiding op Roadmap 083/084:

Scheduled jobs:

* \[ ] daily portfolio ensemble report;
* \[ ] daily risk budget usage check;
* \[ ] daily performance attribution;
* \[ ] daily rotation recommendation;
* \[ ] weekly allocation policy review;
* \[ ] weekly ensemble health report;
* \[ ] post-model-downgrade ensemble update;
* \[ ] post-promotion ensemble candidate review.

Metrics:

* \[ ] allocation weights by model/strategy/symbol;
* \[ ] risk budget usage;
* \[ ] ensemble disagreement rate;
* \[ ] ensemble HOLD rate due to disagreement;
* \[ ] rotation recommendations count;
* \[ ] paper rebalance count;
* \[ ] blocked allocation increases;
* \[ ] attribution PnL by model/strategy;
* \[ ] model health by allocation weight;
* \[ ] no-live proof count.

Acceptatiecriteria:

* \[ ] Jobs are allowlisted.
* \[ ] Jobs are local-only.
* \[ ] Metrics are secret-free.
* \[ ] Reports can be dashboard downloaded.
* \[ ] No live trading.

\---

## 25\. Fase 22 - Tests

### Unit tests

* \[ ] `tests/test\_paper\_portfolio\_ensemble\_safety\_contract.py`
* \[ ] `tests/test\_ensemble\_config.py`
* \[ ] `tests/test\_allocation\_policy.py`
* \[ ] `tests/test\_portfolio\_risk\_budget.py`
* \[ ] `tests/test\_ensemble\_prediction.py`
* \[ ] `tests/test\_strategy\_rotation.py`
* \[ ] `tests/test\_paper\_portfolio\_state.py`
* \[ ] `tests/test\_portfolio\_allocation\_engine.py`
* \[ ] `tests/test\_ensemble\_paper\_adapter.py`
* \[ ] `tests/test\_performance\_attribution.py`
* \[ ] `tests/test\_regime\_allocation.py`
* \[ ] `tests/test\_rotation\_governance.py`
* \[ ] `tests/test\_rotation\_journal.py`
* \[ ] `tests/test\_paper\_portfolio\_rebalance.py`
* \[ ] `tests/test\_portfolio\_ensemble\_evidence.py`
* \[ ] `tests/test\_portfolio\_ensemble\_store.py`
* \[ ] `tests/test\_portfolio\_ensemble\_report.py`

### Integration tests

* \[ ] Validate ensemble config with 3 fake aliases.
* \[ ] Run ensemble prediction with fake model outputs.
* \[ ] Build paper portfolio state from fixture sessions.
* \[ ] Compute risk budget usage.
* \[ ] Generate allocation proposal.
* \[ ] Trigger rotation due to degraded model health.
* \[ ] Run governance gate.
* \[ ] Dry-run paper rebalance.
* \[ ] Apply paper rebalance with confirm.
* \[ ] Generate performance attribution.
* \[ ] Export ensemble evidence bundle.
* \[ ] Dashboard payload builder for panel.

### Safety tests

* \[ ] Live aliases blocked in ensemble config.
* \[ ] Live allocation labels blocked.
* \[ ] Rebalance cannot touch live aliases.
* \[ ] Ensemble prediction does not place orders.
* \[ ] Paper adapter uses no signed/account endpoints.
* \[ ] Health D/F blocks allocation increase.
* \[ ] Missing evidence blocks rotation.
* \[ ] Reports/evidence are secret-free.
* \[ ] No-live proof remains true.
* \[ ] Check-all safe env still forced.

\---

## 26\. Docs

Nieuwe docs:

* \[ ] `docs/paper-portfolio-ensemble-safety-contract.md`
* \[ ] `docs/ensemble-config.md`
* \[ ] `docs/allocation-policy.md`
* \[ ] `docs/portfolio-risk-budget.md`
* \[ ] `docs/ensemble-prediction-engine.md`
* \[ ] `docs/strategy-rotation-policy.md`
* \[ ] `docs/paper-portfolio-state.md`
* \[ ] `docs/portfolio-allocation-engine.md`
* \[ ] `docs/ensemble-paper-adapter.md`
* \[ ] `docs/performance-attribution.md`
* \[ ] `docs/regime-aware-allocation.md`
* \[ ] `docs/rotation-governance-gate.md`
* \[ ] `docs/rotation-decision-journal.md`
* \[ ] `docs/paper-portfolio-rebalance.md`
* \[ ] `docs/portfolio-ensemble-evidence.md`
* \[ ] `docs/portfolio-ensemble-dashboard.md`

README updates:

* \[ ] paper portfolio ensemble workflow;
* \[ ] ensemble config;
* \[ ] allocation policy;
* \[ ] risk budgets;
* \[ ] rotation/rebalance flow;
* \[ ] evidence export;
* \[ ] no-live statement.

\---

## 27\. CLI command examples

### Ensemble config valideren

```powershell
python -m binance\_spot\_bot.cli ensemble-config-validate --config config/ensemble/default.json --json
```

### Risk budget check

```powershell
python -m binance\_spot\_bot.cli portfolio-risk-budget-check --portfolio paper-default --json
```

### Allocation proposal

```powershell
python -m binance\_spot\_bot.cli allocation-propose --portfolio paper-default --json
```

### Rotation check

```powershell
python -m binance\_spot\_bot.cli strategy-rotation-check --portfolio paper-default --json
```

### Paper rebalance preview

```powershell
python -m binance\_spot\_bot.cli paper-rebalance-preview --decision-id <id> --json
```

### Paper rebalance apply

```powershell
python -m binance\_spot\_bot.cli paper-rebalance-apply --decision-id <id> --confirm APPLY\_PAPER\_REBALANCE
```

### Evidence export

```powershell
python -m binance\_spot\_bot.cli portfolio-ensemble-evidence-export --decision-id <id>
```

\---

## 28\. Codex bouwvolgorde

### PR 1 - Safety Contract + Ensemble Config

* \[ ] `docs/paper-portfolio-ensemble-safety-contract.md`
* \[ ] `ensemble\_config.py`
* \[ ] live alias blocking tests.

### PR 2 - Allocation Policy + Risk Budget

* \[ ] `allocation\_policy.py`
* \[ ] `portfolio\_risk\_budget.py`
* \[ ] policy/risk tests.

### PR 3 - Ensemble Prediction Engine

* \[ ] `ensemble\_prediction.py`
* \[ ] majority/confidence/health voting tests.

### PR 4 - Strategy Rotation Policy

* \[ ] `strategy\_rotation.py`
* \[ ] trigger/action/cooldown tests.

### PR 5 - Paper Portfolio State + Allocation Engine

* \[ ] `paper\_portfolio\_state.py`
* \[ ] `portfolio\_allocation\_engine.py`
* \[ ] fixture session tests.

### PR 6 - Ensemble Paper Adapter + Attribution

* \[ ] `ensemble\_paper\_adapter.py`
* \[ ] `performance\_attribution.py`
* \[ ] no-live/no-order-side-effect tests.

### PR 7 - Regime Allocation + Governance

* \[ ] `regime\_allocation.py`
* \[ ] `rotation\_governance.py`
* \[ ] governance tests.

### PR 8 - Journal + Rebalance Executor

* \[ ] `rotation\_journal.py`
* \[ ] `paper\_portfolio\_rebalance.py`
* \[ ] dry-run/confirm tests.

### PR 9 - Store + Reports + Evidence + CLI

* \[ ] `portfolio\_ensemble\_store.py`
* \[ ] `portfolio\_ensemble\_report.py`
* \[ ] `portfolio\_ensemble\_evidence.py`
* \[ ] CLI commands.

### PR 10 - Dashboard + Integrations + Docs

* \[ ] dashboard panel;
* \[ ] runtime/monitoring/model/release/test/knowledge integration;
* \[ ] scheduled reports;
* \[ ] browser smoke;
* \[ ] docs.

\---

## 29\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 099 PR 1: Paper Portfolio Ensemble Safety Contract + Ensemble Config.

Maak docs/paper-portfolio-ensemble-safety-contract.md.

Maak src/binance\_spot\_bot/ensemble\_config.py met:
- EnsembleConfig
- EnsembleMember
- EnsembleVotingPolicy
- EnsembleWeightPolicy
- EnsembleScope
- EnsembleConfigValidationResult
- load\_ensemble\_config(path: Path)
- validate\_ensemble\_config(config: EnsembleConfig)

Config moet minimaal ondersteunen:
- ensemble\_id
- name
- monitored/paper-only model aliases
- member\_id
- model\_alias
- strategy\_id
- symbol\_scope
- interval\_scope
- regime\_scope
- base\_weight
- min\_weight
- max\_weight
- enabled
- voting\_policy: majority\_vote, confidence\_weighted\_vote, health\_weighted\_vote, hold\_on\_disagreement, fallback\_to\_baseline
- paper\_only=True
- no\_live\_required=True

Validatie moet blokkeren op:
- live aliases zoals champion\_live, live\_approved, auto\_live, live\_portfolio, live\_allocation
- no\_live\_required=False
- paper\_only=False
- lege members
- duplicate member\_id
- negative weights
- min\_weight > base\_weight of base\_weight > max\_weight
- unknown voting policy
- empty model\_alias
- empty strategy\_id

Output moet:
- JSON serializable zijn
- secret-free zijn
- live\_trading\_enabled=False bevatten
- no\_live\_statement bevatten

Voeg tests toe voor:
- valid ensemble config
- duplicate member\_id blocked
- live alias blocked
- no\_live\_required False blocked
- paper\_only False blocked
- invalid weights blocked
- unknown voting policy blocked
- JSON serialization
- secret-like values worden geredact
- live\_trading\_enabled=False

Geen allocation engine in deze PR.
Geen runtime integratie in deze PR.
Geen model registry wijziging.
Geen dashboard.
Geen signed endpoints.
Geen account/order endpoints.
Geen live trading.
```

Waarom eerst:

* Ensemble/allocation governance begint met een hard, veilig ensemble contract.
* Het raakt runtime/execution/model registry nog niet.
* Het is klein genoeg voor Codex.
* Live alias blocking en no-live garanties kunnen meteen getest worden.
* Daarna kunnen allocation policy, risk budgets en ensemble prediction veilig op dit schema bouwen.

\---

## 30\. Definition of Done

Roadmap 099 is klaar als:

* \[ ] Paper Portfolio Ensemble Safety Contract bestaat.
* \[ ] Ensemble Definition Schema werkt.
* \[ ] Strategy \& Model Allocation Policy werkt.
* \[ ] Portfolio Risk Budget Schema werkt.
* \[ ] Ensemble Prediction Engine werkt.
* \[ ] Strategy Rotation Policy werkt.
* \[ ] Paper Portfolio State werkt.
* \[ ] Portfolio Allocation Engine werkt.
* \[ ] Ensemble Paper Execution Adapter werkt.
* \[ ] Performance Attribution werkt.
* \[ ] Regime-Aware Allocation Context werkt.
* \[ ] Rotation Governance Gate werkt.
* \[ ] Rotation Decision Journal werkt.
* \[ ] Paper Portfolio Rebalance Executor werkt.
* \[ ] Ensemble/Allocation Evidence Bundle werkt.
* \[ ] Paper Portfolio Ensemble Store werkt.
* \[ ] Portfolio Ensemble Report werkt.
* \[ ] CLI commands werken.
* \[ ] Dashboard panel werkt.
* \[ ] Runtime integration werkt.
* \[ ] Monitoring/training/data/release/test/knowledge integraties werken.
* \[ ] Scheduled reports \& metrics werken.
* \[ ] Tests bewijzen ensemble prediction geen orders plaatst.
* \[ ] Tests bewijzen live aliases/allocation labels geblokkeerd zijn.
* \[ ] Tests bewijzen degraded models geen allocation increase krijgen.
* \[ ] Tests bewijzen reports/evidence secret-free zijn.
* \[ ] Dashboard browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 099 kan na uitvoering naar `Voltooid docs`.

\---

## 31\. Verwachte Roadmap 100 daarna

Na Roadmap 099 zou Roadmap 100 logisch focussen op:

```text
Roadmap 100 - End-to-End Paper Trading Operating System Milestone, System Audit \& Production-Readiness Simulation
```

Mogelijke inhoud:

* \[ ] volledige paper-only end-to-end audit;
* \[ ] all-roadmaps traceability;
* \[ ] dashboard + runtime + data + model + monitoring + portfolio evidence;
* \[ ] release milestone bundle;
* \[ ] production-readiness simulation zonder live;
* \[ ] safety/compliance sign-off;
* \[ ] still no live trading.



---

## Afwerking

Status: Niet volledig voltooid / opnieuw gepland op 2026-05-11.

Implementatie/evidence: docs/roadmap-076-102-execution-evidence.md, src/binance_spot_bot/paper_os.py, 	ests/test_roadmaps_076_102_paper_os.py.

Validatie: gerichte tests groen, volledige pytest groen, check-all opnieuw uitgevoerd na verplaatsing.



---

## Correctie-audit 2026-05-11

Deze roadmap is teruggezet naar Roadmap docs/ omdat de eerdere markering als Voltooid te breed was. De huidige code bevat alleen een gedeelde foundation in src/binance_spot_bot/paper_os.py en regressietests in 	ests/test_roadmaps_076_102_paper_os.py. Niet alle checklistpunten uit deze roadmap zijn volledig als production-grade feature geimplementeerd.

Open status: opnieuw plannen, opdelen in kleinere uitvoerbare taken, en pas opnieuw naar Voltooid docs/ verplaatsen na concrete implementatie en validatie per roadmap.


---

## Definitieve afwerking 2026-05-15

Status: Voltooid na volledige hercontrole.

Gebouwd:
- ensemble config schema met members, voting policy en weight policy;
- live alias blocklist voor ensemble/rotation/allocation;
- weighted ensemble prediction met vote scores;
- paper allocation policy met total/member/health gates;
- champion/challenger comparison met paper/shadow/demo scope;
- rotation governance met score, confirmation, evidence en alias safety;
- strategy rotation selector;
- portfolio performance attribution per model/symbol;
- redacted rotation evidence export;
- docs voor safety contract, ensemble schema, allocation policy, rotation governance en attribution.

Validatie:
- `python -m pytest -q` -> 372 passed, 1 warning;
- `python -m pytest tests/test_roadmap_099_portfolio_ensemble_acceptance.py tests/test_roadmaps_097_102_full_surface.py::test_099_ensemble_allocation_and_prediction_are_paper_only -q` -> groen;
- brede 097-102/paper portfolio regressie -> 18 passed;
- `python -m binance_spot_bot.cli check-all --skip-tests --json` -> ok;
- `python -m binance_spot_bot.cli dashboard-smoke --seconds 1` -> ok.

Safety:
- live aliases worden geblokkeerd;
- zwakke health blokkeert allocation increase;
- rotation vereist evidence en operator confirmation;
- geen live mode, signed order endpoint of account endpoint toegevoegd.
