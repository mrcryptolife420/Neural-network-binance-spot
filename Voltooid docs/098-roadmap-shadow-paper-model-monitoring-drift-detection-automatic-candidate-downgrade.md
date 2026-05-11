# Roadmap 098 - Shadow/Paper Model Monitoring, Drift Detection \& Automatic Candidate Downgrade

Status: Niet volledig voltooid / opnieuw gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/098-roadmap-shadow-paper-model-monitoring-drift-detection-automatic-candidate-downgrade.md
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

Doel: Roadmap 097 maakt modeltraining, experiment tracking, model artifact manifests, feature-contract-aware promotion en paper/shadow/demo-only promotie sterker. Roadmap 098 bouwt daarop een **model monitoring en drift-laag**: promoted modellen worden continu lokaal bewaakt in shadow/paper/demo, feature drift en prediction drift worden gemeten, performance-degradatie wordt gedetecteerd, model health scores worden berekend, alerts worden aangemaakt, en slechte kandidaten kunnen automatisch alleen naar een veilige paper/shadow/demo fallback worden gedowngraded.

Live trading blijft volledig buiten scope. Monitoring en downgrade mogen nooit live trading activeren, geen signed real-order endpoints gebruiken en geen echte account/order endpoints aanroepen.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 098`, `098-roadmap`, `Shadow/Paper Model Monitoring`, `Drift Detection`, `Automatic Candidate Downgrade` en `model health score`.
* \[x] Geen bestaande Roadmap 098 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 097 is lokaal aangemaakt als Model Training Pipeline V2, Experiment Tracking \& Feature Contract-Aware Model Promotion.

### Codebasecontrole

Breed bekeken met model-monitoring-focus:

* \[x] `src/binance\_spot\_bot/model\_registry.py`
* \[x] `src/binance\_spot\_bot/session\_store.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] eerdere analyse van `signal\_model.py`, `evaluation.py`, `dataset\_governance.py`, `features.py`, `data.py`, runtime, paper sessions, dashboard, check-all, metrics en evidence roadmaps.

### Belangrijke bestaande basis

De codebase heeft nu:

* \[x] Model registry met `ModelMetadata`, aliases, model cards, promotion checks, champion promotion en previous champion tracking.
* \[x] Promotion gates die al kijken naar dataset manifest, leakage guard, feature schema hash, walk-forward report, baseline comparison, drawdown, trade count, model card en operator confirmation.
* \[x] `SessionStore` bewaart session summaries en JSONL events voor snapshots, fills, alerts, orders en heartbeats.
* \[x] `BotRuntime` laadt een model via alias of valt terug naar `RuleBasedSignalModel`.
* \[x] Runtime snapshots bevatten active model metadata, signal/risk/execution info, fills, equity, alerts, order lifecycle, session summary en recent sessions.
* \[x] Roadmap 096 plant feature store contracts, feature schema, labels en data lineage.
* \[x] Roadmap 097 plant training config, experiment tracker, model artifact manifests, promotion gate V2, inference compatibility en latency budgets.

### Belangrijkste gat na Roadmap 097

Na Roadmap 097 kun je modellen veilig trainen en promoten naar paper/shadow/demo aliases. Wat nog mist:

* \[ ] doorlopende monitoring van promoted modellen;
* \[ ] shadow model predictions naast champion predictions;
* \[ ] feature drift detectie tussen training data en runtime/paper data;
* \[ ] prediction drift detectie tussen baseline/champion/candidate;
* \[ ] signal distribution drift;
* \[ ] paper PnL degradation monitoring;
* \[ ] confidence calibration monitoring;
* \[ ] model health score;
* \[ ] automatic downgrade naar veilige paper/shadow/demo fallback;
* \[ ] model monitoring evidence bundle;
* \[ ] dashboard voor model monitoring;
* \[ ] scheduler/reporting integratie;
* \[ ] no-live downgrade safety.

Roadmap 098 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 098

Maak een lokale model monitoring-laag:

```text
Runtime/paper/shadow sessions
→ model predictions
→ feature drift
→ prediction drift
→ paper performance
→ health score
→ alerts
→ paper/shadow downgrade decision
→ evidence bundle
```

Na Roadmap 098 moet de bot kunnen:

* \[ ] promoted modellen volgen in paper/shadow/demo;
* \[ ] champion, candidate en baseline predictions naast elkaar loggen;
* \[ ] feature drift meten ten opzichte van training baseline;
* \[ ] prediction drift meten;
* \[ ] confidence drift meten;
* \[ ] paper performance degradation detecteren;
* \[ ] model health score berekenen;
* \[ ] downgrade recommendations maken;
* \[ ] automatische downgrade uitvoeren alleen binnen paper/shadow/demo aliases;
* \[ ] alerts/evidence/reports exporteren;
* \[ ] dashboard en CLI voor monitoring aanbieden;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe modeltraining pipeline; Roadmap 097 doet dat.
* \[ ] Geen feature store opnieuw bouwen; Roadmap 096 doet dat.
* \[ ] Geen runtime refactor opnieuw bouwen; Roadmap 095 doet dat.
* \[ ] Geen live trading.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte Binance account endpoints.
* \[ ] Geen automatic live model promotion.
* \[ ] Geen automatic live downgrade.
* \[ ] Geen cloud monitoring service.
* \[ ] Geen remote telemetry.
* \[ ] Geen drift detection die order sizing verhoogt.
* \[ ] Geen downgrade zonder evidence/journal/alias history.

Wel doen:

* \[ ] local model monitoring toevoegen;
* \[ ] shadow prediction logging toevoegen;
* \[ ] drift baselines en drift reports maken;
* \[ ] paper model health score maken;
* \[ ] paper/shadow downgrade policy toevoegen;
* \[ ] alias rollback/downgrade integreren met Roadmap 097;
* \[ ] runtime/session/evidence/dashboard/CLI integreren;
* \[ ] alles local-only en no-live houden.

\---

## 3\. Fase 0 - Model Monitoring Safety Contract

Nieuwe doc:

```text
docs/model-monitoring-safety-contract.md
```

Regels:

* \[ ] Monitoring is local-only.
* \[ ] Geen remote telemetry.
* \[ ] Geen live trading.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen account endpoints.
* \[ ] Monitoring mag geen orders plaatsen.
* \[ ] Drift alerts mogen alleen paper/shadow/demo actions voorstellen.
* \[ ] Automatic downgrade mag alleen aliases aanpassen:

  * candidate;
  * paper\_candidate;
  * shadow\_candidate;
  * demo\_candidate;
  * champion\_paper;
  * champion\_shadow.
* \[ ] Forbidden aliases:

  * champion\_live;
  * live\_approved;
  * auto\_live.
* \[ ] Downgrade vereist evidence.
* \[ ] Downgrade schrijft alias history.
* \[ ] Downgrade schrijft decision journal waar beschikbaar.
* \[ ] Downgrade mag nooit risk limits verhogen.
* \[ ] Reports/evidence zijn secret-free.
* \[ ] No-live proof wordt opgenomen in reports.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen automatic downgrade geen live alias kan wijzigen.
* \[ ] Tests bewijzen monitoring geen execution/order calls doet.
* \[ ] Reports bevatten `live\_trading\_enabled=False`.
* \[ ] Dashboard toont `LOCAL MODEL MONITORING ONLY`.

\---

## 4\. Fase 1 - Model Monitoring Config

Nieuwe module:

```text
src/binance\_spot\_bot/model\_monitoring\_config.py
```

Dataclasses:

* \[ ] `ModelMonitoringConfig`
* \[ ] `ModelMonitoringScope`
* \[ ] `DriftThresholds`
* \[ ] `PerformanceThresholds`
* \[ ] `DowngradePolicy`
* \[ ] `MonitoringSchedulePolicy`
* \[ ] `MonitoringConfigValidationResult`

Config velden:

* \[ ] monitored\_aliases;
* \[ ] baseline\_model\_alias;
* \[ ] champion\_alias;
* \[ ] candidate\_aliases;
* \[ ] feature\_dataset\_id;
* \[ ] feature\_schema\_hash;
* \[ ] training\_baseline\_window;
* \[ ] runtime\_monitoring\_window;
* \[ ] min\_observations;
* \[ ] drift thresholds;
* \[ ] performance thresholds;
* \[ ] confidence thresholds;
* \[ ] downgrade mode:

  * disabled;
  * recommend\_only;
  * auto\_paper\_only;
  * auto\_shadow\_only.
* \[ ] no\_live\_required=true.

Acceptatiecriteria:

* \[ ] Config is JSON-serializable.
* \[ ] Unknown alias scope blocked.
* \[ ] Live aliases blocked.
* \[ ] no\_live\_required=False blocked.
* \[ ] Tests cover invalid thresholds.

\---

## 5\. Fase 2 - Model Monitoring Store

Nieuwe module:

```text
src/binance\_spot\_bot/model\_monitoring\_store.py
```

Storage:

```text
data/model-monitoring/
  predictions/
  drift/
  performance/
  health/
  downgrade-decisions/
  reports/
  evidence/
```

Dataclasses:

* \[ ] `MonitoringRun`
* \[ ] `MonitoringObservation`
* \[ ] `MonitoringPredictionRecord`
* \[ ] `MonitoringMetricRecord`
* \[ ] `MonitoringStoreManifest`

Store functies:

* \[ ] save prediction records;
* \[ ] save drift reports;
* \[ ] save health score;
* \[ ] save downgrade decision;
* \[ ] list monitoring runs;
* \[ ] load latest per alias;
* \[ ] write manifest;
* \[ ] verify manifest.

Acceptatiecriteria:

* \[ ] Store is local-only.
* \[ ] Store has manifest/hash.
* \[ ] Store stores no secrets.
* \[ ] Store can load latest monitoring window.
* \[ ] Tests use temp dirs.

\---

## 6\. Fase 3 - Shadow Prediction Logger

Nieuwe module:

```text
src/binance\_spot\_bot/shadow\_prediction\_logger.py
```

Doel: champion, candidate en baseline predictions naast elkaar loggen zonder extra orders.

Records:

* \[ ] timestamp\_ms;
* \[ ] symbol;
* \[ ] interval;
* \[ ] feature\_schema\_hash;
* \[ ] feature\_hash;
* \[ ] champion\_model\_id;
* \[ ] candidate\_model\_id;
* \[ ] baseline\_model\_id;
* \[ ] champion\_signal;
* \[ ] candidate\_signal;
* \[ ] baseline\_signal;
* \[ ] champion\_confidence;
* \[ ] candidate\_confidence;
* \[ ] baseline\_confidence;
* \[ ] prediction\_latency\_ms;
* \[ ] model\_aliases;
* \[ ] no\_order\_side\_effect=true;
* \[ ] live\_trading\_enabled=false.

Regels:

* \[ ] shadow predictions mogen geen execution engine aanroepen;
* \[ ] candidate predictions zijn read-only;
* \[ ] missing candidate geeft warning, geen crash;
* \[ ] incompatible feature schema wordt gelogd;
* \[ ] prediction payload wordt geredact.

Acceptatiecriteria:

* \[ ] Logger kan predictions voor meerdere modellen opslaan.
* \[ ] Logger roept geen order/execution code aan.
* \[ ] Missing model geeft safe warning.
* \[ ] Output is secret-free.
* \[ ] Tests gebruiken fake models.

\---

## 7\. Fase 4 - Feature Drift Baseline

Nieuwe module:

```text
src/binance\_spot\_bot/feature\_drift\_baseline.py
```

Doel: training/evaluation feature baseline opslaan voor drift vergelijking.

Dataclasses:

* \[ ] `FeatureDriftBaseline`
* \[ ] `FeatureDistributionSummary`
* \[ ] `FeatureBaselineManifest`
* \[ ] `FeatureBaselineValidation`

Per feature:

* \[ ] count;
* \[ ] mean;
* \[ ] std;
* \[ ] min;
* \[ ] max;
* \[ ] quantiles;
* \[ ] missing\_count;
* \[ ] zero\_count;
* \[ ] finite\_count;
* \[ ] histogram buckets;
* \[ ] schema hash;
* \[ ] dataset id.

Acceptatiecriteria:

* \[ ] Baseline kan uit FeatureStore dataset worden gemaakt.
* \[ ] Baseline manifest heeft hash.
* \[ ] Baseline schema hash moet overeenkomen.
* \[ ] Baseline bevat geen raw secrets.
* \[ ] Tests gebruiken feature fixtures.

\---

## 8\. Fase 5 - Feature Drift Detector

Nieuwe module:

```text
src/binance\_spot\_bot/feature\_drift.py
```

Drift metrics:

* \[ ] mean shift;
* \[ ] std shift;
* \[ ] min/max out-of-range;
* \[ ] missing rate shift;
* \[ ] zero rate shift;
* \[ ] quantile shift;
* \[ ] histogram distance;
* \[ ] PSI-like score zonder externe dependency;
* \[ ] feature missing from runtime;
* \[ ] new unexpected feature.

Dataclasses:

* \[ ] `FeatureDriftIssue`
* \[ ] `FeatureDriftReport`
* \[ ] `FeatureDriftScore`
* \[ ] `FeatureDriftPolicy`

Severity:

* \[ ] ok;
* \[ ] watch;
* \[ ] warning;
* \[ ] critical.

Acceptatiecriteria:

* \[ ] Drift detector compares runtime window vs baseline.
* \[ ] Schema mismatch creates critical issue.
* \[ ] Missing feature creates blocker/warning per policy.
* \[ ] Report is explainable.
* \[ ] Tests cover no drift, mild drift, critical drift.

\---

## 9\. Fase 6 - Prediction Drift Detector

Nieuwe module:

```text
src/binance\_spot\_bot/prediction\_drift.py
```

Metrics:

* \[ ] signal distribution drift;
* \[ ] confidence distribution drift;
* \[ ] BUY/SELL/HOLD ratio shift;
* \[ ] disagreement rate champion vs candidate;
* \[ ] disagreement rate champion vs baseline;
* \[ ] confidence collapse;
* \[ ] overconfident wrong direction proxy;
* \[ ] no-trade/HOLD dominance;
* \[ ] latency drift;
* \[ ] missing prediction rate.

Dataclasses:

* \[ ] `PredictionDriftReport`
* \[ ] `PredictionDriftIssue`
* \[ ] `ModelDisagreementReport`
* \[ ] `PredictionDistributionSummary`

Acceptatiecriteria:

* \[ ] Detector works from shadow prediction logs.
* \[ ] Detects large signal distribution shift.
* \[ ] Detects candidate/champion disagreement.
* \[ ] Detects confidence collapse.
* \[ ] Report is secret-free.
* \[ ] Tests use synthetic predictions.

\---

## 10\. Fase 7 - Paper Performance Monitor

Nieuwe module:

```text
src/binance\_spot\_bot/paper\_model\_performance.py
```

Doel: paper/session performance per model alias volgen.

Inputs:

* \[ ] SessionStore summaries;
* \[ ] fills.jsonl;
* \[ ] snapshots.jsonl;
* \[ ] orders.jsonl;
* \[ ] runtime active\_model payload;
* \[ ] model alias history;
* \[ ] feature schema hash.

Metrics:

* \[ ] paper pnl;
* \[ ] max drawdown;
* \[ ] trade count;
* \[ ] blocked count;
* \[ ] win/loss proxy;
* \[ ] fees;
* \[ ] exposure;
* \[ ] confidence-weighted outcomes;
* \[ ] risk block reasons;
* \[ ] session completion status;
* \[ ] degradation vs baseline/champion previous window.

Acceptatiecriteria:

* \[ ] Monitor can aggregate sessions by model alias.
* \[ ] Monitor handles missing model metadata.
* \[ ] Degradation vs rolling baseline is calculated.
* \[ ] Report is secret-free.
* \[ ] Tests use fixture session store.

\---

## 11\. Fase 8 - Model Health Score

Nieuwe module:

```text
src/binance\_spot\_bot/model\_health\_score.py
```

Score categories:

* \[ ] feature drift;
* \[ ] prediction drift;
* \[ ] paper performance;
* \[ ] drawdown;
* \[ ] trade quality;
* \[ ] confidence stability;
* \[ ] inference latency;
* \[ ] data quality;
* \[ ] schema compatibility;
* \[ ] artifact integrity;
* \[ ] monitoring freshness.

Grades:

* \[ ] A: healthy;
* \[ ] B: acceptable;
* \[ ] C: watch;
* \[ ] D: degraded;
* \[ ] F: blocked.

Hard blockers:

* \[ ] feature schema incompatible;
* \[ ] model artifact verification failed;
* \[ ] leakage/evidence missing;
* \[ ] critical feature drift;
* \[ ] critical prediction drift;
* \[ ] paper drawdown breach;
* \[ ] live alias detected;
* \[ ] no-live proof missing.

Acceptatiecriteria:

* \[ ] Score explains penalties.
* \[ ] Hard blockers force F/blocked.
* \[ ] Score is deterministic.
* \[ ] Dashboard can show health score.
* \[ ] Tests cover all grades.

\---

## 12\. Fase 9 - Model Degradation Alerts

Nieuwe module:

```text
src/binance\_spot\_bot/model\_monitoring\_alerts.py
```

Alert types:

* \[ ] feature\_drift\_warning;
* \[ ] feature\_drift\_critical;
* \[ ] prediction\_drift\_warning;
* \[ ] prediction\_drift\_critical;
* \[ ] paper\_performance\_degraded;
* \[ ] drawdown\_limit\_breached;
* \[ ] model\_latency\_degraded;
* \[ ] model\_artifact\_invalid;
* \[ ] schema\_incompatible;
* \[ ] monitoring\_stale;
* \[ ] downgrade\_recommended;
* \[ ] downgrade\_executed;
* \[ ] downgrade\_blocked.

Integratie:

* \[ ] Runtime event bus from Roadmap 095;
* \[ ] Action Center from Roadmap 086;
* \[ ] Operator reports;
* \[ ] Model evidence bundle.

Acceptatiecriteria:

* \[ ] Alerts are typed and redacted.
* \[ ] Alerts do not execute trades.
* \[ ] Critical alert can pause paper/demo use.
* \[ ] Alert evidence links to reports.
* \[ ] Tests cover alert severity mapping.

\---

## 13\. Fase 10 - Downgrade Policy Engine

Nieuwe module:

```text
src/binance\_spot\_bot/model\_downgrade\_policy.py
```

Policy modes:

* \[ ] disabled;
* \[ ] recommend\_only;
* \[ ] auto\_shadow\_only;
* \[ ] auto\_paper\_only.

Downgrade targets:

* \[ ] candidate → archived;
* \[ ] paper\_candidate → candidate;
* \[ ] shadow\_candidate → candidate;
* \[ ] demo\_candidate → candidate;
* \[ ] champion\_paper → previous\_champion\_paper;
* \[ ] champion\_shadow → previous\_champion\_shadow;
* \[ ] fallback to rule\_baseline if no safe previous alias.

Forbidden:

* \[ ] any live alias;
* \[ ] any risk increase;
* \[ ] any order placement;
* \[ ] any account endpoint;
* \[ ] any signed endpoint.

Decision requirements:

* \[ ] health score D/F;
* \[ ] evidence report present;
* \[ ] alias history present;
* \[ ] no-live proof;
* \[ ] policy mode allows;
* \[ ] downgrade target verified.

Acceptatiecriteria:

* \[ ] Policy explains recommendation.
* \[ ] Auto mode never touches live aliases.
* \[ ] Missing evidence blocks auto downgrade.
* \[ ] Fallback is safe and explicit.
* \[ ] Tests cover all modes.

\---

## 14\. Fase 11 - Paper/Shadow Alias Downgrade Executor

Nieuwe module:

```text
src/binance\_spot\_bot/model\_downgrade\_executor.py
```

Doel: downgrade veilig uitvoeren via ModelRegistry/alias history, alleen paper/shadow/demo.

Flow:

* \[ ] load downgrade decision;
* \[ ] verify decision;
* \[ ] verify target alias;
* \[ ] verify no-live proof;
* \[ ] write pre-downgrade alias snapshot;
* \[ ] update safe alias;
* \[ ] write alias history;
* \[ ] write downgrade result;
* \[ ] create alert;
* \[ ] create evidence bundle.

Guardrails:

* \[ ] dry-run default;
* \[ ] confirm required unless policy allows auto\_paper\_only/auto\_shadow\_only;
* \[ ] no live aliases;
* \[ ] no order/execution calls;
* \[ ] rollback info stored.

Acceptatiecriteria:

* \[ ] Dry-run shows exact alias changes.
* \[ ] Executor refuses live alias.
* \[ ] Executor refuses missing evidence.
* \[ ] Alias history updated.
* \[ ] Tests use temp registry.

\---

## 15\. Fase 12 - Model Monitoring Runbook Recommendations

Nieuwe module:

```text
src/binance\_spot\_bot/model\_monitoring\_runbooks.py
```

Runbook recommendations:

* \[ ] feature drift investigation;
* \[ ] prediction drift investigation;
* \[ ] paper performance degradation;
* \[ ] latency degradation;
* \[ ] schema incompatibility;
* \[ ] model artifact verification failure;
* \[ ] downgrade review;
* \[ ] rollback review;
* \[ ] retrain candidate.

Output:

* \[ ] suggested runbook id;
* \[ ] reason;
* \[ ] linked evidence;
* \[ ] recommended CLI commands;
* \[ ] Action Center proposal optional;
* \[ ] no-live statement.

Acceptatiecriteria:

* \[ ] Runbook recommendation is explainable.
* \[ ] No direct execution.
* \[ ] Can create Action Center proposal where available.
* \[ ] Reports are secret-free.
* \[ ] Tests cover mapping.

\---

## 16\. Fase 13 - Model Monitoring Report

Nieuwe module:

```text
src/binance\_spot\_bot/model\_monitoring\_report.py
```

Reports:

```text
data/model-monitoring/reports/
  daily/
  weekly/
  model-<id>/
```

Report secties:

* \[ ] summary;
* \[ ] monitored aliases;
* \[ ] model health score;
* \[ ] feature drift;
* \[ ] prediction drift;
* \[ ] paper performance;
* \[ ] latency;
* \[ ] artifact integrity;
* \[ ] alerts;
* \[ ] downgrade recommendation;
* \[ ] runbook recommendations;
* \[ ] no-live proof;
* \[ ] evidence links.

Acceptatiecriteria:

* \[ ] Report is Markdown + JSON.
* \[ ] Report is secret-free.
* \[ ] Report links to model/data/runtime evidence.
* \[ ] Dashboard can download report.
* \[ ] Scheduled reports possible.

\---

## 17\. Fase 14 - Model Monitoring Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/model\_monitoring\_evidence.py
```

Bundle bevat:

* \[ ] monitoring config;
* \[ ] monitored model metadata;
* \[ ] feature drift baseline;
* \[ ] feature drift report;
* \[ ] prediction drift report;
* \[ ] paper performance report;
* \[ ] model health score;
* \[ ] alerts;
* \[ ] downgrade decision;
* \[ ] alias snapshot before/after if executed;
* \[ ] runbook recommendations;
* \[ ] no-live proof;
* \[ ] redaction proof;
* \[ ] hashes.

Output:

```text
data/model-monitoring/evidence/<run\_id>/
  model\_monitoring\_evidence\_manifest.json
  model\_monitoring\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle links to model evidence from Roadmap 097.
* \[ ] Bundle links to data pipeline evidence from Roadmap 096.

\---

## 18\. Fase 15 - Runtime Shadow Monitoring Integration

Uitbreiding op Roadmap 095/097:

* \[ ] runtime loads monitored aliases read-only;
* \[ ] runtime records shadow predictions;
* \[ ] runtime snapshot includes model monitoring summary;
* \[ ] runtime event bus emits prediction drift observation events;
* \[ ] incompatible shadow model is skipped safely;
* \[ ] shadow monitoring does not change execution result;
* \[ ] fallback to baseline is explicit if selected paper alias invalid.

Acceptatiecriteria:

* \[ ] Shadow prediction logging does not alter paper fills/orders.
* \[ ] Runtime still works if candidate missing.
* \[ ] Monitoring can be disabled.
* \[ ] Snapshot is secret-free.
* \[ ] Tests prove execution result unchanged with monitoring on/off.

\---

## 19\. Fase 16 - Model Monitoring CLI

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli model-monitoring-config-validate --config config/model-monitoring/default.json
python -m binance\_spot\_bot.cli model-monitoring-baseline --alias champion\_paper
python -m binance\_spot\_bot.cli shadow-prediction-log --session-id <id>
python -m binance\_spot\_bot.cli feature-drift-check --alias champion\_paper
python -m binance\_spot\_bot.cli prediction-drift-check --alias champion\_paper
python -m binance\_spot\_bot.cli paper-model-performance --alias champion\_paper
python -m binance\_spot\_bot.cli model-health-score --alias champion\_paper
python -m binance\_spot\_bot.cli model-monitoring-report --alias champion\_paper
python -m binance\_spot\_bot.cli model-downgrade-preview --alias champion\_paper
python -m binance\_spot\_bot.cli model-downgrade-execute --alias champion\_paper --confirm DOWNGRADE\_MODEL\_PAPER
python -m binance\_spot\_bot.cli model-monitoring-evidence-export --alias champion\_paper
```

Acceptatiecriteria:

* \[ ] Commands werken offline met fixture/demo/paper data.
* \[ ] Commands ondersteunen JSON output.
* \[ ] Downgrade execute vereist confirm tenzij policy auto safe is.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Reports zijn secret-free.

\---

## 20\. Fase 17 - Model Monitoring Dashboard Panel

Nieuwe dashboardsectie:

```text
Model Monitoring \& Drift
```

Panels:

* \[ ] monitored aliases;
* \[ ] champion/candidate status;
* \[ ] model health score;
* \[ ] feature drift summary;
* \[ ] prediction drift summary;
* \[ ] paper performance trend;
* \[ ] confidence distribution;
* \[ ] disagreement rate;
* \[ ] latency trend;
* \[ ] alerts;
* \[ ] downgrade recommendation;
* \[ ] runbook recommendations;
* \[ ] evidence export;
* \[ ] no-live proof.

Actions:

* \[ ] validate monitoring config;
* \[ ] run feature drift check;
* \[ ] run prediction drift check;
* \[ ] run health score;
* \[ ] generate report;
* \[ ] preview downgrade;
* \[ ] execute paper/shadow downgrade with confirm;
* \[ ] export evidence;
* \[ ] copy CLI commands.

Safeguards:

* \[ ] `LOCAL MODEL MONITORING ONLY` badge.
* \[ ] `NO LIVE DOWNGRADE` badge.
* \[ ] Live aliases hidden/blocked.
* \[ ] Downgrade target shown before action.
* \[ ] Confirmation phrase required.
* \[ ] Raw JSON only in limited/debug expander.
* \[ ] Stable widget keys.
* \[ ] Browser smoke covers panel.

Acceptatiecriteria:

* \[ ] Dashboard shows model health score.
* \[ ] Dashboard blocks live alias downgrade.
* \[ ] Dashboard can preview downgrade.
* \[ ] Dashboard can export evidence.
* \[ ] Browser smoke passes.

\---

## 21\. Fase 18 - Scheduler \& Reports Integration

Uitbreiding op Roadmap 083/084:

Scheduled jobs:

* \[ ] daily model monitoring report;
* \[ ] daily feature drift check;
* \[ ] daily prediction drift check;
* \[ ] daily paper model performance check;
* \[ ] weekly health score report;
* \[ ] weekly downgrade recommendation report;
* \[ ] post-training monitoring baseline creation;
* \[ ] post-promotion monitoring check.

Metrics naar Roadmap 084:

* \[ ] model health score trend;
* \[ ] feature drift score;
* \[ ] prediction drift score;
* \[ ] paper pnl degradation;
* \[ ] candidate/champion disagreement;
* \[ ] downgrade recommendations;
* \[ ] downgrade executions;
* \[ ] monitoring stale count;
* \[ ] model latency drift.

Acceptatiecriteria:

* \[ ] Scheduled jobs are allowlisted.
* \[ ] Jobs are local-only.
* \[ ] Failed monitoring job creates report/support evidence.
* \[ ] Metrics are secret-free.
* \[ ] No live trading.

\---

## 22\. Fase 19 - Training/Data/Release/Test/Knowledge Integraties

### Roadmap 097 integratie

* \[ ] Model evidence bundle links to monitoring baseline.
* \[ ] Promotion V2 creates initial monitoring baseline.
* \[ ] Alias history includes downgrade decisions.
* \[ ] Model card includes monitoring status.

### Roadmap 096 integratie

* \[ ] Feature drift baseline uses feature store manifest.
* \[ ] Data quality issues influence model health.
* \[ ] Data lineage links monitoring runtime windows.

### Roadmap 095 integratie

* \[ ] Runtime event bus emits shadow prediction events.
* \[ ] Snapshot profiles include monitoring summary.
* \[ ] Session store records model monitoring metadata.

### Roadmap 092 integratie

* \[ ] Model monitoring changes select drift/model/paper tests.
* \[ ] Downgrade executor changes force deep/safety tests.
* \[ ] Dashboard monitoring changes require browser smoke.

### Roadmap 089/090/091 integratie

* \[ ] Release evidence includes monitoring evidence for model changes.
* \[ ] Roadmap completion gate requires monitoring evidence.
* \[ ] Knowledge graph maps model monitoring modules and artifact flow.

Acceptatiecriteria:

* \[ ] Model monitoring evidence links all upstream evidence.
* \[ ] Test selection chooses correct tests.
* \[ ] Release notes include monitoring/downgrade changes.
* \[ ] Knowledge graph shows model monitoring flow.
* \[ ] No-live proof preserved.

\---

## 23\. Fase 20 - Tests

### Unit tests

* \[ ] `tests/test\_model\_monitoring\_safety\_contract.py`
* \[ ] `tests/test\_model\_monitoring\_config.py`
* \[ ] `tests/test\_model\_monitoring\_store.py`
* \[ ] `tests/test\_shadow\_prediction\_logger.py`
* \[ ] `tests/test\_feature\_drift\_baseline.py`
* \[ ] `tests/test\_feature\_drift.py`
* \[ ] `tests/test\_prediction\_drift.py`
* \[ ] `tests/test\_paper\_model\_performance.py`
* \[ ] `tests/test\_model\_health\_score.py`
* \[ ] `tests/test\_model\_monitoring\_alerts.py`
* \[ ] `tests/test\_model\_downgrade\_policy.py`
* \[ ] `tests/test\_model\_downgrade\_executor.py`
* \[ ] `tests/test\_model\_monitoring\_runbooks.py`
* \[ ] `tests/test\_model\_monitoring\_report.py`
* \[ ] `tests/test\_model\_monitoring\_evidence.py`

### Integration tests

* \[ ] Build feature drift baseline from fixture features.
* \[ ] Log shadow predictions for champion/candidate/baseline.
* \[ ] Run feature drift check with no drift.
* \[ ] Run feature drift check with critical drift.
* \[ ] Run prediction drift check.
* \[ ] Aggregate paper session performance by model alias.
* \[ ] Compute health score.
* \[ ] Generate downgrade recommendation.
* \[ ] Dry-run downgrade.
* \[ ] Execute paper-only downgrade with confirm.
* \[ ] Export model monitoring evidence bundle.
* \[ ] Runtime monitoring on/off does not change execution result.

### Safety tests

* \[ ] Monitoring does not place orders.
* \[ ] Monitoring does not call signed/account endpoints.
* \[ ] Live aliases are blocked.
* \[ ] Automatic downgrade cannot touch live aliases.
* \[ ] Downgrade missing evidence is blocked.
* \[ ] Downgrade writes alias history.
* \[ ] Feature schema mismatch forces blocked health score.
* \[ ] Reports/evidence are secret-free.
* \[ ] No-live proof remains true.
* \[ ] Check-all safe env still forced.

\---

## 24\. Docs

Nieuwe docs:

* \[ ] `docs/model-monitoring-safety-contract.md`
* \[ ] `docs/model-monitoring-config.md`
* \[ ] `docs/model-monitoring-store.md`
* \[ ] `docs/shadow-prediction-logging.md`
* \[ ] `docs/feature-drift-baseline.md`
* \[ ] `docs/feature-drift-detection.md`
* \[ ] `docs/prediction-drift-detection.md`
* \[ ] `docs/paper-model-performance-monitor.md`
* \[ ] `docs/model-health-score.md`
* \[ ] `docs/model-monitoring-alerts.md`
* \[ ] `docs/model-downgrade-policy.md`
* \[ ] `docs/model-downgrade-executor.md`
* \[ ] `docs/model-monitoring-runbooks.md`
* \[ ] `docs/model-monitoring-report.md`
* \[ ] `docs/model-monitoring-evidence.md`
* \[ ] `docs/model-monitoring-dashboard.md`

README updates:

* \[ ] model monitoring workflow;
* \[ ] shadow prediction logging;
* \[ ] feature drift check;
* \[ ] prediction drift check;
* \[ ] paper model health;
* \[ ] downgrade preview/execute;
* \[ ] no-live statement.

\---

## 25\. CLI command examples

### Monitoring config valideren

```powershell
python -m binance\_spot\_bot.cli model-monitoring-config-validate --config config/model-monitoring/default.json --json
```

### Feature drift check

```powershell
python -m binance\_spot\_bot.cli feature-drift-check --alias champion\_paper --json
```

### Prediction drift check

```powershell
python -m binance\_spot\_bot.cli prediction-drift-check --alias champion\_paper --json
```

### Model health score

```powershell
python -m binance\_spot\_bot.cli model-health-score --alias champion\_paper --json
```

### Downgrade preview

```powershell
python -m binance\_spot\_bot.cli model-downgrade-preview --alias champion\_paper --json
```

### Paper-only downgrade uitvoeren

```powershell
python -m binance\_spot\_bot.cli model-downgrade-execute --alias champion\_paper --confirm DOWNGRADE\_MODEL\_PAPER
```

### Evidence export

```powershell
python -m binance\_spot\_bot.cli model-monitoring-evidence-export --alias champion\_paper
```

\---

## 26\. Codex bouwvolgorde

### PR 1 - Model Monitoring Safety Contract + Config

* \[ ] `docs/model-monitoring-safety-contract.md`
* \[ ] `model\_monitoring\_config.py`
* \[ ] config validation tests.

### PR 2 - Monitoring Store

* \[ ] `model\_monitoring\_store.py`
* \[ ] manifests/hashes.
* \[ ] tests.

### PR 3 - Shadow Prediction Logger

* \[ ] `shadow\_prediction\_logger.py`
* \[ ] fake model predictions.
* \[ ] no-order-side-effect tests.

### PR 4 - Feature Drift Baseline + Detector

* \[ ] `feature\_drift\_baseline.py`
* \[ ] `feature\_drift.py`
* \[ ] drift tests.

### PR 5 - Prediction Drift Detector

* \[ ] `prediction\_drift.py`
* \[ ] distribution/disagreement/confidence tests.

### PR 6 - Paper Performance + Health Score

* \[ ] `paper\_model\_performance.py`
* \[ ] `model\_health\_score.py`
* \[ ] fixture session tests.

### PR 7 - Alerts + Downgrade Policy

* \[ ] `model\_monitoring\_alerts.py`
* \[ ] `model\_downgrade\_policy.py`
* \[ ] safety tests.

### PR 8 - Downgrade Executor + Runbooks

* \[ ] `model\_downgrade\_executor.py`
* \[ ] `model\_monitoring\_runbooks.py`
* \[ ] alias history integration.

### PR 9 - Reports + Evidence + CLI

* \[ ] `model\_monitoring\_report.py`
* \[ ] `model\_monitoring\_evidence.py`
* \[ ] CLI commands.
* \[ ] tests.

### PR 10 - Runtime + Dashboard + Scheduler + Integrations

* \[ ] runtime shadow monitoring integration;
* \[ ] dashboard panel;
* \[ ] scheduled jobs;
* \[ ] metrics/release/roadmap/knowledge integration;
* \[ ] browser smoke;
* \[ ] docs.

\---

## 27\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 098 PR 1: Model Monitoring Safety Contract + Monitoring Config.

Maak docs/model-monitoring-safety-contract.md.

Maak src/binance\_spot\_bot/model\_monitoring\_config.py met:
- ModelMonitoringConfig
- ModelMonitoringScope
- DriftThresholds
- PerformanceThresholds
- DowngradePolicy
- MonitoringSchedulePolicy
- MonitoringConfigValidationResult
- load\_model\_monitoring\_config(path: Path)
- validate\_model\_monitoring\_config(config: ModelMonitoringConfig)

Config moet minimaal ondersteunen:
- monitored\_aliases
- baseline\_model\_alias
- champion\_alias
- candidate\_aliases
- feature\_dataset\_id
- feature\_schema\_hash
- training\_baseline\_window
- runtime\_monitoring\_window
- min\_observations
- drift thresholds
- performance thresholds
- confidence thresholds
- downgrade mode: disabled, recommend\_only, auto\_paper\_only, auto\_shadow\_only
- no\_live\_required=True

Validatie moet blokkeren op:
- live aliases zoals champion\_live, live\_approved, auto\_live
- no\_live\_required=False
- min\_observations < 1
- negatieve thresholds
- auto modes zonder safe paper/shadow target
- lege monitored\_aliases
- duplicate aliases

Output moet:
- JSON serializable zijn
- secret-free zijn
- live\_trading\_enabled=False bevatten
- no\_live\_statement bevatten

Voeg tests toe voor:
- valid recommend\_only config
- valid auto\_paper\_only config
- live alias blocked
- no\_live\_required False blocked
- invalid thresholds blocked
- duplicate aliases blocked
- empty aliases blocked
- JSON serialization
- secret-like values worden geredact
- live\_trading\_enabled=False

Geen drift detector bouwen in deze PR.
Geen downgrade executor bouwen in deze PR.
Geen model registry wijzigen in deze PR.
Geen dashboard.
Geen signed endpoints.
Geen account/order endpoints.
Geen live trading.
```

Waarom eerst:

* Monitoring en downgrade hebben eerst een hard safety/config contract nodig.
* Het raakt runtime, model registry en execution nog niet.
* Het is klein genoeg voor Codex.
* Live alias blocking en no-live garanties kunnen meteen getest worden.
* Daarna kunnen store, shadow logging, drift detection en downgrade veilig op dit schema bouwen.

\---

## 28\. Definition of Done

Roadmap 098 is klaar als:

* \[ ] Model Monitoring Safety Contract bestaat.
* \[ ] Model Monitoring Config werkt.
* \[ ] Model Monitoring Store werkt.
* \[ ] Shadow Prediction Logger werkt.
* \[ ] Feature Drift Baseline werkt.
* \[ ] Feature Drift Detector werkt.
* \[ ] Prediction Drift Detector werkt.
* \[ ] Paper Performance Monitor werkt.
* \[ ] Model Health Score werkt.
* \[ ] Model Degradation Alerts werken.
* \[ ] Downgrade Policy Engine werkt.
* \[ ] Paper/Shadow Alias Downgrade Executor werkt.
* \[ ] Model Monitoring Runbook Recommendations werken.
* \[ ] Model Monitoring Report werkt.
* \[ ] Model Monitoring Evidence Bundle werkt.
* \[ ] Runtime Shadow Monitoring Integration werkt.
* \[ ] Model Monitoring CLI werkt.
* \[ ] Model Monitoring Dashboard Panel werkt.
* \[ ] Scheduler \& Reports Integration werkt.
* \[ ] Training/Data/Release/Test/Knowledge integraties werken.
* \[ ] Tests bewijzen monitoring geen orders plaatst.
* \[ ] Tests bewijzen automatic downgrade geen live alias raakt.
* \[ ] Tests bewijzen reports/evidence secret-free zijn.
* \[ ] Tests bewijzen feature/prediction drift health score beïnvloedt.
* \[ ] Dashboard browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 098 kan na uitvoering naar `Voltooid docs`.

\---

## 29\. Verwachte Roadmap 099 daarna

Na Roadmap 098 zou Roadmap 099 logisch focussen op:

```text
Roadmap 099 - Paper Portfolio Model Ensemble, Strategy Allocation \& Model Rotation Governance
```

Mogelijke inhoud:

* \[ ] meerdere paper/shadow modellen tegelijk monitoren;
* \[ ] ensemble voting;
* \[ ] model allocation per symbol/regime;
* \[ ] strategy/model rotation;
* \[ ] paper-only capital allocation;
* \[ ] governance gates voor rotation;
* \[ ] ensemble evidence reports;
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

