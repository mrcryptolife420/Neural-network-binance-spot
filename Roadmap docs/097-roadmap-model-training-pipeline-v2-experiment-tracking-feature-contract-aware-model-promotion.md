# Roadmap 097 - Model Training Pipeline V2, Experiment Tracking \& Feature Contract-Aware Model Promotion

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/097-roadmap-model-training-pipeline-v2-experiment-tracking-feature-contract-aware-model-promotion.md
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

Doel: Roadmap 096 maakt data pipeline contracts, candle datasets, feature store contracts, labels, data quality en lineage sterker. Roadmap 097 bouwt daarop de volgende kernlaag: **een reproduceerbare modeltraining pipeline met experiment tracking, model artifact manifests, feature-contract-aware evaluation, strict promotion gates, inference compatibility checks, latency budgets en model evidence bundles**.

Live trading blijft volledig buiten scope. Modelpromotie betekent hier alleen: lokaal/paper/shadow/demo gebruik. Geen live trading, geen signed order endpoints en geen echte account/order acties.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 097`, `097-roadmap`, `Model Training Pipeline V2`, `Experiment Tracking`, `Feature Contract-Aware Model Promotion` en `model promotion`.
* \[x] Geen bestaande Roadmap 097 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 096 is lokaal aangemaakt als Data Pipeline Decomposition, Feature Store Contracts \& Indicator Compute Optimization.

### Codebasecontrole

Breed bekeken met model/evaluation/promotie-focus:

* \[x] `src/binance\_spot\_bot/signal\_model.py`
* \[x] `src/binance\_spot\_bot/model\_registry.py`
* \[x] `src/binance\_spot\_bot/evaluation.py`
* \[x] `src/binance\_spot\_bot/dataset\_governance.py`
* \[x] eerdere analyse van `features.py`, `data.py`, runtime, dashboard, check-all, performance, testselectie en data pipeline roadmaps.

### Belangrijke bestaande basis

De codebase heeft nu:

* \[x] `RuleBasedSignalModel` als baseline signal model.
* \[x] `TinyNeuralSignalModel` als compacte pure-Python MLP met `fit`, `predict`, `save` en `load`.
* \[x] `EvaluationReport`, `WalkForwardConfig`, `walk\_forward\_folds`, `evaluate\_rule\_baseline` en `evaluate\_walk\_forward`.
* \[x] Walk-forward evaluation met baseline/candidate vergelijking, costs, leakage guard, candidate summary en confidence buckets.
* \[x] `ModelRegistry` met model metadata, model artifacts, aliases, model cards, champion promotion, previous champion en promotion decisions.
* \[x] Promotion gate met checks voor dataset manifest, leakage guard, feature schema hash, walk-forward report, baseline comparison, drawdown, trade count, model card en operator confirmation.
* \[x] Dataset governance met dataset manifests, feature schema hashing, manifest checksums en leakage guard.
* \[x] Roadmap 096 plant feature store contracts en data lineage, wat modeltraining betrouwbaarder maakt.

### Belangrijkste gat na Roadmap 096

Na Roadmap 096 is de data/feature-laag contract-aware, maar modeltraining en promotie kunnen nog veel sterker:

* \[ ] Geen aparte training job config/schema.
* \[ ] Geen lokale experiment tracker met run history.
* \[ ] Geen model artifact manifest met hashes, inputs, feature schema en metrics.
* \[ ] Geen reproduceerbaarheidsgate voor seed/config/dataset.
* \[ ] Geen strict link tussen FeatureStore V2 en modeltraining.
* \[ ] Geen candidate-vs-baseline-vs-champion evaluation pack.
* \[ ] Geen model drift/stability report over meerdere folds/datasets.
* \[ ] Geen inference compatibility check per feature schema.
* \[ ] Geen inference latency/performance budget.
* \[ ] Geen model rollback/alias history report.
* \[ ] Geen dashboard voor experiments/model training.
* \[ ] Geen model evidence bundle die release/roadmap/compliance kan gebruiken.

Roadmap 097 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 097

Maak een veilige lokale modeltraining- en promotiepipeline:

```text
FeatureStore contract
→ TrainingJobConfig
→ Experiment run
→ Model artifact manifest
→ Walk-forward evaluation
→ Baseline/champion comparison
→ Promotion gate
→ Model evidence bundle
→ Paper/shadow/demo alias
```

Na Roadmap 097 moet de bot kunnen:

* \[ ] training jobs declaratief definiëren;
* \[ ] feature/label contracts verplicht valideren vóór training;
* \[ ] experiment runs lokaal opslaan;
* \[ ] model artifacts met manifest/hashes registreren;
* \[ ] walk-forward evaluation verplicht uitvoeren;
* \[ ] model cards uitbreiden;
* \[ ] candidate vergelijken met baseline en champion;
* \[ ] promotion gates stricter maken;
* \[ ] inference compatibility en latency meten;
* \[ ] model rollback/alias history beheren;
* \[ ] model evidence exporteren;
* \[ ] modeltraining zichtbaar maken in dashboard;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen zware ML framework dependency verplicht maken.
* \[ ] Geen cloud experiment tracker.
* \[ ] Geen remote telemetry.
* \[ ] Geen live trading.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte Binance account endpoints.
* \[ ] Geen model dat automatisch live promoted wordt.
* \[ ] Geen autonomous training agent die zonder operator budgetten wijzigt.
* \[ ] Geen feature store opnieuw bouwen; Roadmap 096 doet dat.
* \[ ] Geen evaluation engine volledig herschrijven.
* \[ ] Geen modelpromotie zonder leakage guard, feature schema hash en operator confirmation.

Wel doen:

* \[ ] Training job schema toevoegen.
* \[ ] Experiment tracking local-only maken.
* \[ ] Model artifact manifests toevoegen.
* \[ ] Feature contract gates koppelen aan training.
* \[ ] Evaluation/promotie uitbreiden.
* \[ ] Model evidence bundle maken.
* \[ ] Inference compatibility/latency checks toevoegen.
* \[ ] CLI/dashboard integreren.
* \[ ] Alles paper/shadow/demo-only houden.

\---

## 3\. Fase 0 - Model Training Safety Contract

Nieuwe doc:

```text
docs/model-training-safety-contract.md
```

Regels:

* \[ ] Modeltraining is local-only.
* \[ ] Geen remote telemetry.
* \[ ] Geen live trading.
* \[ ] Geen signed order endpoints.
* \[ ] Geen account endpoints.
* \[ ] Training gebruikt alleen approved dataset/feature/label manifests.
* \[ ] Training blokkeert op failed leakage guard.
* \[ ] Training blokkeert op incompatible feature schema.
* \[ ] Model artifacts bevatten geen secrets.
* \[ ] Promotion is alleen paper/shadow/demo aliasing.
* \[ ] Champion promotion vereist operator confirmation.
* \[ ] Promotion vereist baseline/champion comparison.
* \[ ] Promotion vereist model card.
* \[ ] Promotion vereist inference compatibility check.
* \[ ] Reports/evidence zijn secret-free.
* \[ ] No-live proof wordt in reports opgenomen.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen modelpromotie geen live mode activeert.
* \[ ] Tests bewijzen failed leakage guard training/promotie blokkeert.
* \[ ] Tests bewijzen model artifacts secret-free zijn.
* \[ ] Output bevat `live\_trading\_enabled=False`.

\---

## 4\. Fase 1 - Training Job Config Schema

Nieuwe module:

```text
src/binance\_spot\_bot/training\_config.py
```

Dataclasses:

* \[ ] `TrainingJobConfig`
* \[ ] `TrainingDataBinding`
* \[ ] `TrainingModelSpec`
* \[ ] `TrainingSplitPolicy`
* \[ ] `TrainingCostAssumptions`
* \[ ] `TrainingRiskAssumptions`
* \[ ] `TrainingValidationPolicy`
* \[ ] `TrainingConfigValidationResult`

Config velden:

* \[ ] job\_id;
* \[ ] experiment\_name;
* \[ ] model\_type:

  * rule\_baseline;
  * tiny\_neural\_signal;
  * future\_optional\_adapter.
* \[ ] feature\_dataset\_id;
* \[ ] label\_dataset\_id;
* \[ ] feature\_schema\_hash;
* \[ ] label\_schema\_hash;
* \[ ] dataset\_manifest\_path;
* \[ ] split policy;
* \[ ] walk-forward config;
* \[ ] fee/slippage/spread assumptions;
* \[ ] risk limits for evaluation;
* \[ ] random seed;
* \[ ] epochs;
* \[ ] learning rate;
* \[ ] hidden size;
* \[ ] min trade count;
* \[ ] max drawdown;
* \[ ] candidate beats baseline required;
* \[ ] no\_live\_required=true.

Acceptatiecriteria:

* \[ ] Config is JSON-serializable.
* \[ ] Config validation blocks missing feature/label manifests.
* \[ ] Config validation blocks incompatible schema.
* \[ ] Config output is secret-free.
* \[ ] Tests cover valid/invalid configs.

\---

## 5\. Fase 2 - Local Experiment Tracker

Nieuwe module:

```text
src/binance\_spot\_bot/experiment\_tracker.py
```

Storage:

```text
data/experiments/
  runs/
  summaries/
  manifests/
  artifacts/
```

Dataclasses:

* \[ ] `ExperimentRun`
* \[ ] `ExperimentRunStatus`
* \[ ] `ExperimentMetric`
* \[ ] `ExperimentArtifact`
* \[ ] `ExperimentManifest`
* \[ ] `ExperimentTracker`

Run status:

* \[ ] created;
* \[ ] validating\_data;
* \[ ] training;
* \[ ] evaluating;
* \[ ] failed;
* \[ ] completed;
* \[ ] promotion\_candidate;
* \[ ] archived.

Per run:

* \[ ] run\_id;
* \[ ] experiment\_name;
* \[ ] config\_hash;
* \[ ] feature\_dataset\_id;
* \[ ] label\_dataset\_id;
* \[ ] feature\_schema\_hash;
* \[ ] model\_type;
* \[ ] seed;
* \[ ] started\_at\_ms;
* \[ ] finished\_at\_ms;
* \[ ] metrics;
* \[ ] artifacts;
* \[ ] status;
* \[ ] failure\_reason;
* \[ ] live\_trading\_enabled=false.

Acceptatiecriteria:

* \[ ] Tracker is local-only.
* \[ ] Tracker is append-only where practical.
* \[ ] Run manifest has hashes.
* \[ ] Failed runs are recorded.
* \[ ] No secrets in tracker.

\---

## 6\. Fase 3 - Training Data Contract Gate

Nieuwe module:

```text
src/binance\_spot\_bot/training\_data\_gate.py
```

Doel: training pas starten als data/feature/label contracten kloppen.

Checks:

* \[ ] feature dataset manifest exists;
* \[ ] label dataset manifest exists;
* \[ ] candle dataset manifest exists;
* \[ ] dataset lineage valid;
* \[ ] feature schema hash matches config;
* \[ ] label schema hash matches config;
* \[ ] leakage guard passed;
* \[ ] train/validation/test ranges non-empty;
* \[ ] embargo/gap policy satisfied;
* \[ ] row count enough;
* \[ ] data quality not blocked;
* \[ ] no secrets in manifests;
* \[ ] no-live proof present.

Acceptatiecriteria:

* \[ ] Gate blocks missing feature manifest.
* \[ ] Gate blocks schema mismatch.
* \[ ] Gate blocks failed leakage guard.
* \[ ] Gate blocks insufficient rows.
* \[ ] Gate report is secret-free.

\---

## 7\. Fase 4 - Model Trainer Interface

Nieuwe module:

```text
src/binance\_spot\_bot/model\_training.py
```

Dataclasses:

* \[ ] `TrainingInput`
* \[ ] `TrainingOutput`
* \[ ] `TrainingMetricSet`
* \[ ] `TrainingFailure`
* \[ ] `ModelTrainer`

Trainer adapters:

* \[ ] `RuleBaselineTrainer`
* \[ ] `TinyNeuralTrainer`

Training output:

* \[ ] model object or artifact ref;
* \[ ] model\_type;
* \[ ] feature\_names;
* \[ ] model\_version;
* \[ ] train metrics;
* \[ ] validation metrics;
* \[ ] training duration;
* \[ ] seed;
* \[ ] config hash;
* \[ ] warnings.

Acceptatiecriteria:

* \[ ] Rule baseline trainer creates deterministic baseline artifact.
* \[ ] Tiny neural trainer trains deterministically with seed.
* \[ ] Trainer works from FeatureStore/LabelStore contracts once Roadmap 096 exists.
* \[ ] Trainer fallback can work with existing feature/label rows.
* \[ ] Tests cover empty/mismatched rows.

\---

## 8\. Fase 5 - Model Artifact Manifest

Nieuwe module:

```text
src/binance\_spot\_bot/model\_artifacts.py
```

Dataclasses:

* \[ ] `ModelArtifactManifest`
* \[ ] `ModelArtifactFile`
* \[ ] `ModelArtifactHash`
* \[ ] `ModelArtifactValidationReport`

Manifest bevat:

* \[ ] model\_id;
* \[ ] model\_type;
* \[ ] model\_version;
* \[ ] artifact\_path;
* \[ ] artifact\_sha256;
* \[ ] model\_card\_path;
* \[ ] training\_config\_hash;
* \[ ] feature\_dataset\_id;
* \[ ] label\_dataset\_id;
* \[ ] feature\_schema\_hash;
* \[ ] label\_schema\_hash;
* \[ ] dataset\_lineage\_hash;
* \[ ] training\_run\_id;
* \[ ] evaluation\_report\_path;
* \[ ] created\_at\_ms;
* \[ ] live\_trading\_enabled=false;
* \[ ] forbidden\_use: live trading.

Acceptatiecriteria:

* \[ ] Manifest is written next to model artifact.
* \[ ] Manifest verifies artifact hash.
* \[ ] Manifest contains no secrets.
* \[ ] Registry stores manifest path.
* \[ ] Tests detect tampered artifact.

\---

## 9\. Fase 6 - Training Pipeline Orchestrator

Nieuwe module:

```text
src/binance\_spot\_bot/training\_pipeline.py
```

Flow:

* \[ ] load training config;
* \[ ] validate config;
* \[ ] run data contract gate;
* \[ ] create experiment run;
* \[ ] load feature/label rows;
* \[ ] train model;
* \[ ] save model artifact;
* \[ ] write artifact manifest;
* \[ ] run evaluation;
* \[ ] write model card;
* \[ ] register candidate;
* \[ ] write pipeline report;
* \[ ] mark experiment completed/failed.

Acceptatiecriteria:

* \[ ] Pipeline can train TinyNeuralSignalModel from fixture data.
* \[ ] Failed gate creates failed experiment run.
* \[ ] Successful run creates model artifact + manifest + model card.
* \[ ] Pipeline output is secret-free.
* \[ ] No live trading.

\---

## 10\. Fase 7 - Evaluation Pack V2

Nieuwe module:

```text
src/binance\_spot\_bot/model\_evaluation\_pack.py
```

Evaluation pack bevat:

* \[ ] walk-forward report;
* \[ ] leakage guard report;
* \[ ] baseline metrics;
* \[ ] candidate metrics;
* \[ ] champion metrics if available;
* \[ ] costs assumptions;
* \[ ] risk assumptions;
* \[ ] confidence bucket analysis;
* \[ ] signal distribution;
* \[ ] drawdown analysis;
* \[ ] turnover/trade count;
* \[ ] blocked trade reasons;
* \[ ] fold stability;
* \[ ] feature schema compatibility;
* \[ ] inference latency summary.

Acceptatiecriteria:

* \[ ] Existing `EvaluationReport` remains supported.
* \[ ] Evaluation pack can compare candidate vs baseline.
* \[ ] Evaluation pack can compare candidate vs champion if available.
* \[ ] Fold stability metrics are computed.
* \[ ] Report is JSON/Markdown exportable.

\---

## 11\. Fase 8 - Champion/Challenger Comparison

Nieuwe module:

```text
src/binance\_spot\_bot/champion\_challenger.py
```

Dataclasses:

* \[ ] `ChampionChallengerComparison`
* \[ ] `ModelComparisonMetric`
* \[ ] `ModelComparisonDecision`
* \[ ] `ModelComparisonReport`

Comparison dimensions:

* \[ ] candidate beats baseline after costs;
* \[ ] candidate beats champion after costs;
* \[ ] max drawdown within limit;
* \[ ] trade count sufficient;
* \[ ] fold stability;
* \[ ] confidence distribution acceptable;
* \[ ] no leakage;
* \[ ] same feature schema or compatible schema;
* \[ ] inference latency within budget;
* \[ ] model artifact verified;
* \[ ] model card present.

Acceptatiecriteria:

* \[ ] Candidate can be compared with no current champion.
* \[ ] Candidate can be compared with existing champion.
* \[ ] Decision is explainable.
* \[ ] Failed checks produce reasons.
* \[ ] Tests cover candidate better/worse/equal.

\---

## 12\. Fase 9 - Promotion Gate V2

Uitbreiden:

```text
src/binance\_spot\_bot/model\_registry.py
```

Nieuwe module:

```text
src/binance\_spot\_bot/model\_promotion\_gate.py
```

Extra checks:

* \[ ] model artifact manifest verified;
* \[ ] feature contract gate passed;
* \[ ] label contract gate passed;
* \[ ] dataset lineage present;
* \[ ] leakage guard passed;
* \[ ] evaluation pack present;
* \[ ] champion/challenger comparison passed;
* \[ ] inference compatibility passed;
* \[ ] inference latency budget passed;
* \[ ] model card present;
* \[ ] no-live proof present;
* \[ ] operator confirmed;
* \[ ] promotion scope is paper/shadow/demo only.

Promotion scopes:

* \[ ] candidate;
* \[ ] paper\_candidate;
* \[ ] shadow\_candidate;
* \[ ] demo\_candidate;
* \[ ] champion\_paper;
* \[ ] champion\_shadow;
* \[ ] archived.

Forbidden:

* \[ ] champion\_live;
* \[ ] live\_approved;
* \[ ] auto\_live.

Acceptatiecriteria:

* \[ ] Old promotion flow remains backward-compatible.
* \[ ] Promotion V2 blocks forbidden live scopes.
* \[ ] Promotion V2 blocks missing artifact manifest.
* \[ ] Promotion V2 blocks failed latency/compatibility.
* \[ ] Promotion decision is written to registry and evidence.

\---

## 13\. Fase 10 - Model Card V2

Nieuwe module:

```text
src/binance\_spot\_bot/model\_card\_v2.py
```

Model card secties:

* \[ ] model identity;
* \[ ] intended use;
* \[ ] forbidden use;
* \[ ] training data;
* \[ ] feature schema;
* \[ ] label schema;
* \[ ] leakage guard;
* \[ ] evaluation summary;
* \[ ] cost assumptions;
* \[ ] risk assumptions;
* \[ ] baseline/champion comparison;
* \[ ] known limitations;
* \[ ] failure modes;
* \[ ] inference latency;
* \[ ] promotion decision;
* \[ ] rollback instructions;
* \[ ] no-live statement.

Acceptatiecriteria:

* \[ ] Model card is Markdown + JSON.
* \[ ] Model card contains no secrets.
* \[ ] Model card links to manifests/evidence.
* \[ ] Promotion requires model card.
* \[ ] Tests verify required sections.

\---

## 14\. Fase 11 - Inference Compatibility Check

Nieuwe module:

```text
src/binance\_spot\_bot/inference\_compatibility.py
```

Checks:

* \[ ] model feature names match feature schema;
* \[ ] model can predict on latest feature row;
* \[ ] missing feature behavior deterministic;
* \[ ] extra feature behavior deterministic;
* \[ ] model output side is valid;
* \[ ] model confidence is finite and bounded;
* \[ ] model horizon is valid;
* \[ ] model metadata has version/model\_id;
* \[ ] feature schema compatibility status acceptable;
* \[ ] no raw secrets in prediction payload.

Acceptatiecriteria:

* \[ ] Tiny neural compatibility passes for matching schema.
* \[ ] Missing feature mismatch is blocked or warned based on policy.
* \[ ] Rule baseline compatibility passes.
* \[ ] Invalid prediction output fails.
* \[ ] Report is secret-free.

\---

## 15\. Fase 12 - Inference Latency \& Resource Budget

Nieuwe module:

```text
src/binance\_spot\_bot/model\_performance.py
```

Metrics:

* \[ ] prediction p50/p95/max duration;
* \[ ] batch prediction duration;
* \[ ] model load duration;
* \[ ] artifact size;
* \[ ] model card size;
* \[ ] feature vector build duration;
* \[ ] memory best-effort;
* \[ ] warm/cold prediction difference.

Budgets:

* \[ ] max single prediction ms;
* \[ ] max model load ms;
* \[ ] max artifact bytes;
* \[ ] max batch prediction ms;
* \[ ] max runtime inference overhead.

Acceptatiecriteria:

* \[ ] Latency test works offline.
* \[ ] Budget check is deterministic enough for local use.
* \[ ] Promotion can require budget pass.
* \[ ] Performance report feeds Roadmap 093.
* \[ ] No secrets.

\---

## 16\. Fase 13 - Model Rollback \& Alias History

Nieuwe module:

```text
src/binance\_spot\_bot/model\_alias\_history.py
```

Track:

* \[ ] alias changes;
* \[ ] previous champion;
* \[ ] previous paper champion;
* \[ ] rollback target;
* \[ ] promotion decision;
* \[ ] operator confirmation;
* \[ ] timestamp;
* \[ ] model card path;
* \[ ] artifact manifest path.

Commands/flow:

* \[ ] preview alias change;
* \[ ] promote candidate;
* \[ ] rollback alias;
* \[ ] archive old model;
* \[ ] export alias history.

Acceptatiecriteria:

* \[ ] Alias change is append-only in history.
* \[ ] Rollback requires existing previous champion.
* \[ ] Forbidden live alias is blocked.
* \[ ] History is secret-free.
* \[ ] Tests cover promote/rollback/archive.

\---

## 17\. Fase 14 - Model Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/model\_evidence\_bundle.py
```

Bundle bevat:

* \[ ] training config;
* \[ ] data contract gate report;
* \[ ] feature dataset manifest;
* \[ ] label dataset manifest;
* \[ ] dataset lineage;
* \[ ] experiment manifest;
* \[ ] model artifact manifest;
* \[ ] evaluation pack;
* \[ ] champion/challenger comparison;
* \[ ] inference compatibility report;
* \[ ] latency budget report;
* \[ ] model card;
* \[ ] promotion decision;
* \[ ] alias history;
* \[ ] no-live proof;
* \[ ] redaction proof;
* \[ ] hashes.

Output:

```text
data/model-evidence/<model\_id>/
  model\_evidence\_manifest.json
  model\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle links to data pipeline evidence.
* \[ ] Bundle links to release/roadmap evidence.

\---

## 18\. Fase 15 - Model Training CLI

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli training-config-validate --config config/training/demo-tiny.json
python -m binance\_spot\_bot.cli training-data-gate --config config/training/demo-tiny.json
python -m binance\_spot\_bot.cli train-model --config config/training/demo-tiny.json
python -m binance\_spot\_bot.cli experiment-list
python -m binance\_spot\_bot.cli experiment-show --run-id <id>
python -m binance\_spot\_bot.cli model-artifact-verify --model-id <id>
python -m binance\_spot\_bot.cli model-evaluation-pack --model-id <id>
python -m binance\_spot\_bot.cli champion-challenger-compare --candidate <id>
python -m binance\_spot\_bot.cli model-promotion-check --model-id <id>
python -m binance\_spot\_bot.cli model-promote-paper --model-id <id> --confirm PROMOTE\_MODEL\_PAPER
python -m binance\_spot\_bot.cli model-rollback-preview
python -m binance\_spot\_bot.cli model-card --model-id <id>
python -m binance\_spot\_bot.cli inference-compatibility --model-id <id>
python -m binance\_spot\_bot.cli model-latency-check --model-id <id>
python -m binance\_spot\_bot.cli model-evidence-export --model-id <id>
```

Acceptatiecriteria:

* \[ ] Commands werken offline met demo/fixture data.
* \[ ] Commands ondersteunen JSON output.
* \[ ] Promotion command vereist confirm.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Reports zijn secret-free.

\---

## 19\. Fase 16 - Model Training Dashboard Panel

Nieuwe dashboardsectie:

```text
Model Training \& Experiments
```

Panels:

* \[ ] training configs;
* \[ ] data contract gate status;
* \[ ] experiments list;
* \[ ] experiment detail;
* \[ ] candidate models;
* \[ ] baseline/champion comparison;
* \[ ] model card preview;
* \[ ] promotion gate status;
* \[ ] inference compatibility;
* \[ ] latency budgets;
* \[ ] alias history;
* \[ ] model evidence export;
* \[ ] no-live proof.

Actions:

* \[ ] validate training config;
* \[ ] run data gate;
* \[ ] launch local training job with confirm;
* \[ ] view experiment report;
* \[ ] run promotion check;
* \[ ] promote to paper/shadow/demo with confirm;
* \[ ] rollback alias with confirm;
* \[ ] export model evidence;
* \[ ] copy CLI commands.

Safeguards:

* \[ ] `LOCAL MODEL TRAINING ONLY` badge.
* \[ ] `NO LIVE PROMOTION` badge.
* \[ ] Live alias scopes blocked.
* \[ ] Training command visible before execution.
* \[ ] Raw JSON only in limited/debug expander.
* \[ ] Stable widget keys.
* \[ ] Browser smoke covers panel.

Acceptatiecriteria:

* \[ ] Dashboard can show experiment/model status.
* \[ ] Dashboard blocks live promotion.
* \[ ] Dashboard promotion requires confirm.
* \[ ] Dashboard can export evidence.
* \[ ] Browser smoke passes.

\---

## 20\. Fase 17 - Runtime/Inference Integration

Uitbreiding op Roadmap 095:

* \[ ] runtime loads champion\_paper or selected paper alias only.
* \[ ] runtime checks feature schema compatibility before using model.
* \[ ] runtime emits event on model incompatibility.
* \[ ] runtime fallback to rule baseline if model missing/incompatible.
* \[ ] runtime snapshot includes model\_id, feature\_schema\_hash and alias.
* \[ ] inference latency recorded to Roadmap 093 performance store.
* \[ ] no-live proof included in runtime model payload.

Acceptatiecriteria:

* \[ ] Runtime does not crash on missing model.
* \[ ] Runtime blocks incompatible model and falls back safely.
* \[ ] Runtime does not use forbidden live alias.
* \[ ] Snapshot model metadata is secret-free.
* \[ ] Tests cover candidate/champion/fallback paths.

\---

## 21\. Fase 18 - Data Pipeline Integration

Uitbreiding op Roadmap 096:

* \[ ] training uses FeatureStore contracts.
* \[ ] training uses LabelStore contracts.
* \[ ] feature schema diff is shown before training.
* \[ ] dataset lineage included in model artifact manifest.
* \[ ] data quality blockers prevent training.
* \[ ] feature drift report can be attached to evaluation pack.
* \[ ] data pipeline evidence linked in model evidence.

Acceptatiecriteria:

* \[ ] Training from feature store works.
* \[ ] Training blocks missing label contract.
* \[ ] Training blocks failed data quality gate.
* \[ ] Model evidence links to data evidence.
* \[ ] Tests use feature store fixtures.

\---

## 22\. Fase 19 - Test/Knowledge/Release Integration

### Roadmap 091 integratie

* \[ ] Knowledge graph herkent training/model modules.
* \[ ] Impact analysis koppelt model changes aan evaluation/promotie tests.
* \[ ] Ownership map krijgt model\_training domein.
* \[ ] Artifact flow graph toont model evidence.

### Roadmap 092 integratie

* \[ ] Model/training changes selecteren model/evaluation/promotion tests.
* \[ ] Promotion gate changes forceren deep profile.
* \[ ] Runtime inference changes forceren runtime + model tests.

### Roadmap 089 integratie

* \[ ] Model artifact schema changes krijgen release notes.
* \[ ] Promotion gate changes krijgen release quality gate.
* \[ ] Release evidence bevat model evidence bij model changes.

### Roadmap 090 integratie

* \[ ] Codex task packs krijgen model evidence requirements.
* \[ ] Roadmap completion gate vereist model evidence bij model-roadmaps.

Acceptatiecriteria:

* \[ ] Model changes krijgen juiste testselectie.
* \[ ] Release notes tonen model/promotion changes.
* \[ ] Completion gate kan model evidence lezen.
* \[ ] Knowledge graph toont model artifact flow.
* \[ ] No-live proof preserved.

\---

## 23\. Fase 20 - Metrics/Observability Integration

Uitbreiding op Roadmap 084:

Metrics:

* \[ ] experiment count;
* \[ ] training success/failure count;
* \[ ] average training duration;
* \[ ] evaluation fold count;
* \[ ] candidate beats baseline ratio;
* \[ ] promotion pass/fail count;
* \[ ] model latency p50/p95;
* \[ ] model artifact size;
* \[ ] rollback count;
* \[ ] model incompatibility count;
* \[ ] feature schema mismatch count.

Acceptatiecriteria:

* \[ ] Metrics exportable to local metrics warehouse.
* \[ ] Weekly model ops report possible.
* \[ ] Dashboard can show model ops trends.
* \[ ] No secrets in metrics.
* \[ ] No-live proof preserved.

\---

## 24\. Fase 21 - Tests

### Unit tests

* \[ ] `tests/test\_model\_training\_safety\_contract.py`
* \[ ] `tests/test\_training\_config.py`
* \[ ] `tests/test\_experiment\_tracker.py`
* \[ ] `tests/test\_training\_data\_gate.py`
* \[ ] `tests/test\_model\_training.py`
* \[ ] `tests/test\_model\_artifacts.py`
* \[ ] `tests/test\_training\_pipeline.py`
* \[ ] `tests/test\_model\_evaluation\_pack.py`
* \[ ] `tests/test\_champion\_challenger.py`
* \[ ] `tests/test\_model\_promotion\_gate.py`
* \[ ] `tests/test\_model\_card\_v2.py`
* \[ ] `tests/test\_inference\_compatibility.py`
* \[ ] `tests/test\_model\_performance.py`
* \[ ] `tests/test\_model\_alias\_history.py`
* \[ ] `tests/test\_model\_evidence\_bundle.py`

### Integration tests

* \[ ] Build fixture feature/label dataset.
* \[ ] Validate training config.
* \[ ] Run training data gate.
* \[ ] Train tiny neural model.
* \[ ] Save model artifact manifest.
* \[ ] Register candidate model.
* \[ ] Build evaluation pack.
* \[ ] Compare candidate vs baseline.
* \[ ] Run promotion gate.
* \[ ] Promote to paper alias with confirm.
* \[ ] Rollback alias preview.
* \[ ] Export model evidence bundle.
* \[ ] Runtime loads promoted paper alias.

### Safety tests

* \[ ] Live promotion scope blocked.
* \[ ] Signed/order/account endpoints absent.
* \[ ] Failed leakage guard blocks training/promotie.
* \[ ] Feature schema mismatch blocks training/promotie.
* \[ ] Model artifact tampering detected.
* \[ ] Model card required for promotion.
* \[ ] Operator confirmation required for promotion.
* \[ ] Model evidence contains no secrets.
* \[ ] Runtime fallback on incompatible model.
* \[ ] No-live proof remains true.

\---

## 25\. Docs

Nieuwe docs:

* \[ ] `docs/model-training-safety-contract.md`
* \[ ] `docs/training-job-config.md`
* \[ ] `docs/local-experiment-tracker.md`
* \[ ] `docs/training-data-contract-gate.md`
* \[ ] `docs/model-trainer-interface.md`
* \[ ] `docs/model-artifact-manifest.md`
* \[ ] `docs/training-pipeline-v2.md`
* \[ ] `docs/model-evaluation-pack-v2.md`
* \[ ] `docs/champion-challenger-comparison.md`
* \[ ] `docs/model-promotion-gate-v2.md`
* \[ ] `docs/model-card-v2.md`
* \[ ] `docs/inference-compatibility.md`
* \[ ] `docs/model-latency-budgets.md`
* \[ ] `docs/model-alias-history.md`
* \[ ] `docs/model-evidence-bundle.md`
* \[ ] `docs/model-training-dashboard.md`

README updates:

* \[ ] model training workflow;
* \[ ] experiment tracking;
* \[ ] feature contract gate;
* \[ ] model promotion flow;
* \[ ] paper/shadow/demo aliases;
* \[ ] no-live statement.

\---

## 26\. CLI command examples

### Training config valideren

```powershell
python -m binance\_spot\_bot.cli training-config-validate --config config/training/demo-tiny.json --json
```

### Data gate draaien

```powershell
python -m binance\_spot\_bot.cli training-data-gate --config config/training/demo-tiny.json --json
```

### Model trainen

```powershell
python -m binance\_spot\_bot.cli train-model --config config/training/demo-tiny.json --json
```

### Promotie check

```powershell
python -m binance\_spot\_bot.cli model-promotion-check --model-id <id> --json
```

### Paper promotie

```powershell
python -m binance\_spot\_bot.cli model-promote-paper --model-id <id> --confirm PROMOTE\_MODEL\_PAPER
```

### Evidence export

```powershell
python -m binance\_spot\_bot.cli model-evidence-export --model-id <id>
```

\---

## 27\. Codex bouwvolgorde

### PR 1 - Model Training Safety Contract + Training Config

* \[ ] `docs/model-training-safety-contract.md`
* \[ ] `training\_config.py`
* \[ ] config validation tests.

### PR 2 - Experiment Tracker

* \[ ] `experiment\_tracker.py`
* \[ ] local run storage.
* \[ ] failure/success tests.

### PR 3 - Training Data Contract Gate

* \[ ] `training\_data\_gate.py`
* \[ ] feature/label/leakage/schema checks.
* \[ ] tests.

### PR 4 - Model Trainer Interface

* \[ ] `model\_training.py`
* \[ ] baseline/tiny trainers.
* \[ ] deterministic training tests.

### PR 5 - Model Artifact Manifest

* \[ ] `model\_artifacts.py`
* \[ ] artifact hashing/verify.
* \[ ] registry integration base.

### PR 6 - Training Pipeline Orchestrator

* \[ ] `training\_pipeline.py`
* \[ ] config → gate → train → artifact → registry.
* \[ ] tests.

### PR 7 - Evaluation Pack + Champion/Challenger

* \[ ] `model\_evaluation\_pack.py`
* \[ ] `champion\_challenger.py`
* \[ ] tests.

### PR 8 - Promotion Gate V2 + Model Card V2

* \[ ] `model\_promotion\_gate.py`
* \[ ] `model\_card\_v2.py`
* \[ ] registry integration.
* \[ ] no-live tests.

### PR 9 - Inference Compatibility + Performance + Alias History

* \[ ] `inference\_compatibility.py`
* \[ ] `model\_performance.py`
* \[ ] `model\_alias\_history.py`
* \[ ] runtime integration tests.

### PR 10 - CLI + Dashboard + Evidence + Docs

* \[ ] model CLI commands;
* \[ ] model training dashboard;
* \[ ] model evidence bundle;
* \[ ] metrics/release/roadmap integration;
* \[ ] browser smoke;
* \[ ] docs.

\---

## 28\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 097 PR 1: Model Training Safety Contract + Training Job Config Schema.

Maak docs/model-training-safety-contract.md.

Maak src/binance\_spot\_bot/training\_config.py met:
- TrainingJobConfig
- TrainingDataBinding
- TrainingModelSpec
- TrainingSplitPolicy
- TrainingCostAssumptions
- TrainingRiskAssumptions
- TrainingValidationPolicy
- TrainingConfigValidationResult
- load\_training\_config(path: Path)
- validate\_training\_config(config: TrainingJobConfig)

Config moet minimaal ondersteunen:
- job\_id
- experiment\_name
- model\_type: rule\_baseline of tiny\_neural\_signal
- feature\_dataset\_id
- label\_dataset\_id
- feature\_schema\_hash
- label\_schema\_hash
- dataset\_manifest\_path
- walk-forward config velden
- fee/slippage/spread assumptions
- random seed
- epochs
- learning\_rate
- hidden\_size
- promotion thresholds zoals min\_trade\_count, max\_drawdown, candidate\_beats\_baseline\_required
- no\_live\_required=True

Validatie moet blokkeren op:
- ontbrekende feature\_dataset\_id
- ontbrekende label\_dataset\_id
- onbekend model\_type
- epochs < 1 voor tiny\_neural\_signal
- learning\_rate <= 0 voor tiny\_neural\_signal
- ontbrekende feature\_schema\_hash
- no\_live\_required=False

Output moet:
- JSON serializable zijn
- secret-free zijn
- live\_trading\_enabled=False bevatten
- no\_live\_statement bevatten

Voeg tests toe voor:
- valid tiny neural config
- valid rule baseline config
- missing feature/label dataset blocked
- unknown model type blocked
- invalid epochs/lr blocked
- no\_live\_required False blocked
- JSON serialization
- secret-like values worden geredact
- live\_trading\_enabled=False

Geen trainer bouwen in deze PR.
Geen model registry wijzigen in deze PR.
Geen dashboard.
Geen signed endpoints.
Geen account/order endpoints.
Geen live trading.
```

Waarom eerst:

* Elke training pipeline heeft een hard config contract nodig.
* Het raakt runtime en registry nog niet.
* Het is klein genoeg voor Codex.
* Safety/no-live/promotiegrenzen kunnen meteen getest worden.
* Daarna kunnen experiment tracker, data gate en trainer veilig op dit schema bouwen.

\---

## 29\. Definition of Done

Roadmap 097 is klaar als:

* \[ ] Model Training Safety Contract bestaat.
* \[ ] Training Job Config Schema werkt.
* \[ ] Local Experiment Tracker werkt.
* \[ ] Training Data Contract Gate werkt.
* \[ ] Model Trainer Interface werkt.
* \[ ] Model Artifact Manifest werkt.
* \[ ] Training Pipeline Orchestrator werkt.
* \[ ] Evaluation Pack V2 werkt.
* \[ ] Champion/Challenger Comparison werkt.
* \[ ] Promotion Gate V2 werkt.
* \[ ] Model Card V2 werkt.
* \[ ] Inference Compatibility Check werkt.
* \[ ] Inference Latency \& Resource Budget werkt.
* \[ ] Model Rollback \& Alias History werkt.
* \[ ] Model Evidence Bundle werkt.
* \[ ] Model Training CLI werkt.
* \[ ] Model Training Dashboard Panel werkt.
* \[ ] Runtime/Inference Integration werkt.
* \[ ] Data Pipeline Integration werkt.
* \[ ] Test/Knowledge/Release Integration werkt.
* \[ ] Metrics/Observability Integration werkt.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen failed leakage/schema gates training/promotie blokkeren.
* \[ ] Tests bewijzen model artifacts/evidence secret-free zijn.
* \[ ] Tests bewijzen live promotion scopes geblokkeerd zijn.
* \[ ] Dashboard browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 097 kan na uitvoering naar `Voltooid docs`.

\---

## 30\. Verwachte Roadmap 098 daarna

Na Roadmap 097 zou Roadmap 098 logisch focussen op:

```text
Roadmap 098 - Shadow/Paper Model Monitoring, Drift Detection \& Automatic Candidate Downgrade
```

Mogelijke inhoud:

* \[ ] shadow model monitoring;
* \[ ] feature drift detection;
* \[ ] prediction drift;
* \[ ] paper performance degradation;
* \[ ] automatic paper-only downgrade;
* \[ ] model health score;
* \[ ] model monitoring dashboard;
* \[ ] still no live trading.

