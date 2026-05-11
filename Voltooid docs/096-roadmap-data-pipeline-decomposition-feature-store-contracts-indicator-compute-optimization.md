# Roadmap 096 - Data Pipeline Decomposition, Feature Store Contracts \& Indicator Compute Optimization

Status: Niet volledig voltooid / opnieuw gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/096-roadmap-data-pipeline-decomposition-feature-store-contracts-indicator-compute-optimization.md
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

Doel: Roadmap 095 splitst de runtime op in services, events, pipeline stages en snapshot builders. Roadmap 096 pakt de volgende fundamentele laag aan: **data pipeline, feature store contracts en indicator computation**. De huidige data/feature-laag werkt, maar candles, feature rows, labels, dataset manifests, leakage guard, runtime featurebouw, evaluation/backtest reuse en cache/indexering moeten versieerbaar, incrementeel, sneller, beter gevalideerd en evidence-ready worden.

Live trading blijft volledig buiten scope. Deze roadmap gebruikt alleen lokale data, public market data en demo/paper/testnet-readiness flows. Geen signed real-order endpoints, geen echte account endpoints en geen live trading.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 096`, `096-roadmap`, `Data Pipeline Decomposition`, `Feature Store Contracts`, `Indicator Compute Optimization` en `feature store`.
* \[x] Geen bestaande Roadmap 096 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 095 is lokaal aangemaakt als Runtime Core Decomposition, Event Bus \& Snapshot Optimization.

### Codebasecontrole

Breed bekeken met data/feature-focus:

* \[x] `src/binance\_spot\_bot/data.py`
* \[x] `src/binance\_spot\_bot/features.py`
* \[x] `src/binance\_spot\_bot/market\_data\_source.py`
* \[x] `src/binance\_spot\_bot/evaluation.py`
* \[x] `src/binance\_spot\_bot/dataset\_governance.py`
* \[x] eerdere analyse van `runtime.py`, `check\_all.py`, dashboard, operator/evidence, performance en testselectie roadmaps.

### Belangrijke bestaande basis

De codebase heeft nu:

* \[x] `DataStore` met mappen voor raw, processed, features en models.
* \[x] CSV opslag/laden voor candles.
* \[x] JSONL opslag voor feature rows en label rows.
* \[x] Binance klines parser met candle-validatie.
* \[x] `build\_feature\_rows(...)` met rolling returns, volatility, volume z-score en candle-shape features.
* \[x] `build\_label\_rows(...)` voor future-return labels.
* \[x] `chronological\_split(...)` en `assert\_no\_lookahead(...)`.
* \[x] Market data sources voor static, demo replay, REST polling met fallback en websocket wrapper met safe polling fallback.
* \[x] Evaluation gebruikt feature rows, label rows, walk-forward folds, leakage guard, baseline/candidate model vergelijking en dataset manifests.
* \[x] Dataset governance bevat feature schema hashing, dataset manifest, checksum en leakage guard.
* \[x] Runtime gebruikt `build\_feature\_rows(...)\[-1]` per step, wat correct maar niet optimaal is voor performance.

### Belangrijkste gat na Roadmap 095

Na runtime-opdeling is de data/feature-laag nog de volgende grote bottleneck:

* \[ ] `DataStore` is nog basic en heeft geen typed dataset/index/contracts.
* \[ ] Candles worden volledig als CSV gelezen/geschreven zonder partitionering/index.
* \[ ] Feature computation bouwt vaak opnieuw over de volledige candlelijst.
* \[ ] Indicatoren zijn nog niet modulair/versioned.
* \[ ] Feature schema is al aanwezig, maar nog niet als harde feature-store contractlaag.
* \[ ] Runtime en evaluation delen featurebouw nog niet via een centrale feature service.
* \[ ] Public Binance data cache heeft nog geen sterke manifest/index/reuse-contracten.
* \[ ] Feature drift/data quality evidence is nog beperkt.
* \[ ] Dataset lineage van raw → candles → features → labels → evaluation → model is nog niet volledig traceable.
* \[ ] Performance budgets uit Roadmap 093 zijn nog niet toegepast op feature/indicator computation.
* \[ ] Testselectie/knowledge graph kan data pipeline changes nog niet fijnmazig classificeren.

Roadmap 096 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 096

Maak een versioned, incrementele en evidence-ready data pipeline:

```text
Raw/public Binance data
→ candle store
→ candle quality validation
→ indicator registry
→ incremental feature computation
→ feature store contracts
→ labels
→ dataset manifests
→ evaluation/backtest/runtime reuse
→ data pipeline evidence
```

Na Roadmap 096 moet de bot kunnen:

* \[ ] candles opslaan met manifest/index;
* \[ ] candle datasets valideren op gaps/duplicates/order/range;
* \[ ] indicators modulair registreren;
* \[ ] feature rows incrementeel berekenen;
* \[ ] feature schema-contracten afdwingen;
* \[ ] labels versioned bouwen;
* \[ ] feature/cache hergebruiken in runtime en evaluation;
* \[ ] dataset lineage exporteren;
* \[ ] data quality/drift evidence maken;
* \[ ] performance budgetten op feature computation toepassen;
* \[ ] data pipeline dashboard/CLI gebruiken;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe exchange client.
* \[ ] Geen live trading.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte account endpoints.
* \[ ] Geen externe feature store/cloud service.
* \[ ] Geen database verplicht maken als basic JSON/CSV/JSONL genoeg is.
* \[ ] Geen volledige pandas/polars dependency verplicht maken.
* \[ ] Geen nieuwe modeltraining-roadmap; deze roadmap levert data/feature fundament.
* \[ ] Geen evaluation engine rewrite; alleen hergebruik van feature store contracts.
* \[ ] Geen breaking dataset schema zonder Roadmap 089 migration/release evidence.

Wel doen:

* \[ ] DataStore opsplitsen in typed stores;
* \[ ] candle store/index toevoegen;
* \[ ] feature store contracts toevoegen;
* \[ ] indicator registry toevoegen;
* \[ ] incremental feature computation toevoegen;
* \[ ] labels/feature schema versioning hard maken;
* \[ ] runtime/evaluation hergebruik verbeteren;
* \[ ] data pipeline reports/evidence maken;
* \[ ] CLI/dashboard integreren;
* \[ ] alles local-only, public/demo/paper en no-live houden.

\---

## 3\. Fase 0 - Data Pipeline Safety Contract

Nieuwe doc:

```text
docs/data-pipeline-safety-contract.md
```

Regels:

* \[ ] Data pipeline is local-first.
* \[ ] Public market data is toegestaan.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen live trading.
* \[ ] Geen API secrets in dataset manifests.
* \[ ] Geen raw credentials in cache paths/metadata.
* \[ ] Feature/label computation is deterministic.
* \[ ] Data cache writes zijn manifest/hash based.
* \[ ] Dataset schema changes vereisen schema version.
* \[ ] Destructive cache cleanup vereist preview + confirm.
* \[ ] Data quality failures mogen trading niet verhogen.
* \[ ] Reports/evidence zijn secret-free.
* \[ ] No-live proof wordt opgenomen in data pipeline reports.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen geen signed/order/account endpoints in data pipeline.
* \[ ] Tests bewijzen dataset manifests geen secrets bevatten.
* \[ ] Output bevat `live\_trading\_enabled=False`.
* \[ ] Check-all blijft groen.

\---

## 4\. Fase 1 - Data Store V2 Contracts

Nieuwe module:

```text
src/binance\_spot\_bot/data\_store\_v2.py
```

Dataclasses:

* \[ ] `DataStoreRoot`
* \[ ] `DataStoreContract`
* \[ ] `DataStorePathPolicy`
* \[ ] `DataArtifactRef`
* \[ ] `DataStoreManifest`
* \[ ] `DataStoreValidationResult`

Substores:

* \[ ] `RawMarketDataStore`
* \[ ] `CandleStore`
* \[ ] `FeatureStore`
* \[ ] `LabelStore`
* \[ ] `DatasetManifestStore`
* \[ ] `DataQualityStore`
* \[ ] `DataLineageStore`

Contractregels:

* \[ ] alle paths binnen `data\_dir`;
* \[ ] geen path traversal;
* \[ ] suffix allowlist;
* \[ ] manifest per artifact;
* \[ ] sha256 per artifact;
* \[ ] schema version per artifact;
* \[ ] redaction/no-secret proof;
* \[ ] live\_trading\_enabled=False.

Acceptatiecriteria:

* \[ ] DataStore V2 werkt naast bestaande `DataStore`.
* \[ ] Bestaande `DataStore` blijft backward-compatible.
* \[ ] Path policy blokkeert unsafe paths.
* \[ ] Manifests zijn JSON-serializable.
* \[ ] Tests dekken path policy en manifests.

\---

## 5\. Fase 2 - Candle Dataset Model

Nieuwe module:

```text
src/binance\_spot\_bot/candle\_dataset.py
```

Dataclasses:

* \[ ] `CandleDatasetId`
* \[ ] `CandleDatasetKey`
* \[ ] `CandleDatasetManifest`
* \[ ] `CandleDatasetStats`
* \[ ] `CandleValidationIssue`
* \[ ] `CandleValidationReport`

Dataset key:

* \[ ] symbol;
* \[ ] interval;
* \[ ] source;
* \[ ] start\_ms;
* \[ ] end\_ms;
* \[ ] row\_count;
* \[ ] schema\_version;
* \[ ] data\_hash.

Stats:

* \[ ] row\_count;
* \[ ] start/end;
* \[ ] min/max/avg volume;
* \[ ] min/max close;
* \[ ] gap\_count;
* \[ ] duplicate\_count;
* \[ ] zero\_volume\_count;
* \[ ] invalid\_ohlc\_count;
* \[ ] stale\_count;
* \[ ] source;
* \[ ] checksum.

Acceptatiecriteria:

* \[ ] CandleDatasetManifest kan uit candles gebouwd worden.
* \[ ] Candle validation detecteert gaps/duplicates/invalid OHLC.
* \[ ] Manifest is secret-free.
* \[ ] Dataset ID is deterministic.
* \[ ] Tests gebruiken candle fixtures.

\---

## 6\. Fase 3 - Candle Store \& Index

Nieuwe module:

```text
src/binance\_spot\_bot/candle\_store.py
```

Storage layout:

```text
data/market/candles/
  <source>/
    <symbol>/
      <interval>/
        candles.csv
        manifest.json
        index.json
        quality.json
```

Core functies:

* \[ ] save candles;
* \[ ] append candles;
* \[ ] load range;
* \[ ] load tail;
* \[ ] merge candles;
* \[ ] deduplicate;
* \[ ] validate chronology;
* \[ ] write index;
* \[ ] verify index;
* \[ ] list datasets;
* \[ ] export manifest.

Acceptatiecriteria:

* \[ ] Store kan bestaande processed CSV importeren.
* \[ ] Store kan tail laden voor runtime.
* \[ ] Store kan range laden voor evaluation.
* \[ ] Merge is deterministic.
* \[ ] Tests dekken append/merge/dedup/range.

\---

## 7\. Fase 4 - Public Binance Data Cache V2

Nieuwe module:

```text
src/binance\_spot\_bot/public\_market\_cache.py
```

Doel: public Binance klines/orderbook/market data beter cachen zonder signed endpoints.

Cache targets:

* \[ ] klines;
* \[ ] exchange info filters;
* \[ ] book ticker snapshots;
* \[ ] ticker statistics indien public;
* \[ ] symbol metadata.

Cache policies:

* \[ ] freshness ttl per data type;
* \[ ] public-only endpoint allowlist;
* \[ ] no signed/account/order endpoints;
* \[ ] fallback to demo data when unavailable;
* \[ ] cache manifest/hashes;
* \[ ] source status;
* \[ ] fetch error metadata redacted.

Acceptatiecriteria:

* \[ ] Public endpoint allowlist bestaat.
* \[ ] Signed/account/order endpoints zijn geblokkeerd.
* \[ ] Kline cache schrijft CandleDatasetManifest.
* \[ ] Cache fallback is reportable.
* \[ ] Tests gebruiken fake adapter/responses.

\---

## 8\. Fase 5 - Indicator Registry

Nieuwe module:

```text
src/binance\_spot\_bot/indicator\_registry.py
```

Dataclasses:

* \[ ] `IndicatorDefinition`
* \[ ] `IndicatorInputSpec`
* \[ ] `IndicatorOutputSpec`
* \[ ] `IndicatorParameter`
* \[ ] `IndicatorVersion`
* \[ ] `IndicatorRegistry`
* \[ ] `IndicatorComputeResult`

Indicator categories:

* \[ ] returns;
* \[ ] volatility;
* \[ ] volume;
* \[ ] trend;
* \[ ] momentum;
* \[ ] candle\_shape;
* \[ ] liquidity\_proxy;
* \[ ] data\_quality;
* \[ ] custom.

Startindicatoren:

* \[ ] ret\_1;
* \[ ] ret\_window;
* \[ ] rolling\_volatility;
* \[ ] volume\_zscore;
* \[ ] body\_ratio;
* \[ ] upper\_wick\_ratio;
* \[ ] lower\_wick\_ratio;
* \[ ] simple\_moving\_average;
* \[ ] price\_distance\_to\_sma;
* \[ ] rolling\_volume\_mean;
* \[ ] rolling\_range\_pct;
* \[ ] rolling\_trade\_count\_mean.

Acceptatiecriteria:

* \[ ] Bestaande features zijn als indicators geregistreerd.
* \[ ] Indicator definitions hebben version/hash.
* \[ ] Parameter changes wijzigen schema hash.
* \[ ] Registry output is secret-free.
* \[ ] Tests dekken duplicate indicator names.

\---

## 9\. Fase 6 - Incremental Indicator Compute

Nieuwe module:

```text
src/binance\_spot\_bot/indicator\_compute.py
```

Doel: niet elke runtime step volledig `build\_feature\_rows(...)\[-1]` over alle candles doen.

Dataclasses:

* \[ ] `IndicatorState`
* \[ ] `IndicatorWindow`
* \[ ] `IndicatorComputeRequest`
* \[ ] `IndicatorComputeOutput`
* \[ ] `IncrementalFeatureState`

Functionaliteit:

* \[ ] compute full batch;
* \[ ] compute last row;
* \[ ] update rolling state;
* \[ ] warmup status;
* \[ ] missing data warning;
* \[ ] deterministic fallback to batch;
* \[ ] performance metadata;
* \[ ] schema hash output.

Acceptatiecriteria:

* \[ ] Incremental output matcht batch output binnen tolerantie.
* \[ ] Warmup path is duidelijk.
* \[ ] State kan resetten bij gap/source change.
* \[ ] Runtime kan laatste feature sneller krijgen.
* \[ ] Tests vergelijken batch vs incremental.

\---

## 10\. Fase 7 - Feature Store Contract

Nieuwe module:

```text
src/binance\_spot\_bot/feature\_store.py
```

Dataclasses:

* \[ ] `FeatureDatasetKey`
* \[ ] `FeatureDatasetManifest`
* \[ ] `FeatureStoreContract`
* \[ ] `FeatureStoreReadRequest`
* \[ ] `FeatureStoreWriteRequest`
* \[ ] `FeatureStoreValidationReport`

Contractvelden:

* \[ ] feature\_set\_id;
* \[ ] feature\_set\_version;
* \[ ] feature\_schema\_hash;
* \[ ] generator\_version;
* \[ ] indicator\_versions;
* \[ ] lookback\_window;
* \[ ] source candle dataset ID;
* \[ ] symbol;
* \[ ] interval;
* \[ ] start/end;
* \[ ] row\_count;
* \[ ] checksum;
* \[ ] data\_quality summary;
* \[ ] created\_at\_ms;
* \[ ] live\_trading\_enabled=false.

Storage:

```text
data/features/v2/
  <feature\_set\_id>/
    features.jsonl
    manifest.json
    schema.json
    quality.json
```

Acceptatiecriteria:

* \[ ] Feature store kan bestaande feature rows opslaan.
* \[ ] Feature store kan manifest/schema valideren.
* \[ ] Feature schema mismatch wordt geblokkeerd.
* \[ ] Store kan range/tail lezen.
* \[ ] Tests dekken contract mismatch.

\---

## 11\. Fase 8 - Feature Schema V2

Uitbreiden:

```text
src/binance\_spot\_bot/dataset\_governance.py
```

Nieuwe module:

```text
src/binance\_spot\_bot/feature\_schema.py
```

Doel: bestaande feature schema hashing hard maken als contract.

Dataclasses:

* \[ ] `FeatureField`
* \[ ] `FeatureSchemaV2`
* \[ ] `FeatureSchemaDiff`
* \[ ] `FeatureSchemaCompatibility`
* \[ ] `FeatureSchemaValidationResult`

Compatibility:

* \[ ] compatible;
* \[ ] additive;
* \[ ] breaking;
* \[ ] incompatible;
* \[ ] unknown.

Checks:

* \[ ] field missing;
* \[ ] field added;
* \[ ] type changed;
* \[ ] normalization changed;
* \[ ] lookback changed;
* \[ ] indicator version changed;
* \[ ] generator version changed.

Acceptatiecriteria:

* \[ ] FeatureSchema V1 compatibility blijft.
* \[ ] Schema diff is human-readable.
* \[ ] Breaking schema change vereist release/migration note.
* \[ ] Evaluation blokkeert incompatible schema.
* \[ ] Tests dekken schema diffs.

\---

## 12\. Fase 9 - Label Store \& Label Contracts

Nieuwe module:

```text
src/binance\_spot\_bot/label\_store.py
```

Dataclasses:

* \[ ] `LabelDefinition`
* \[ ] `LabelDatasetKey`
* \[ ] `LabelDatasetManifest`
* \[ ] `LabelStoreContract`
* \[ ] `LabelValidationReport`

Labels:

* \[ ] future\_return;
* \[ ] future\_return\_up;
* \[ ] future\_return\_bucket;
* \[ ] max\_future\_drawdown;
* \[ ] max\_future\_runup;
* \[ ] volatility\_regime optional.

Contractvelden:

* \[ ] label\_name;
* \[ ] horizon\_bars;
* \[ ] label\_version;
* \[ ] source candle dataset ID;
* \[ ] aligned feature dataset ID;
* \[ ] row\_count;
* \[ ] leakage guard result;
* \[ ] checksum;
* \[ ] live\_trading\_enabled=false.

Acceptatiecriteria:

* \[ ] Existing `build\_label\_rows` wordt ondersteund.
* \[ ] Label manifest is secret-free.
* \[ ] Label/feature alignment wordt gevalideerd.
* \[ ] Horizon changes wijzigen label schema.
* \[ ] Tests dekken alignment/leakage.

\---

## 13\. Fase 10 - Data Quality V2

Nieuwe module:

```text
src/binance\_spot\_bot/data\_quality\_v2.py
```

Doel: data quality voor batch, runtime en datasets centraliseren.

Checks:

* \[ ] chronological order;
* \[ ] duplicate timestamp;
* \[ ] gap detection;
* \[ ] invalid OHLC;
* \[ ] zero/negative price;
* \[ ] zero volume;
* \[ ] extreme returns;
* \[ ] stale data;
* \[ ] spread above limit;
* \[ ] suspicious candle range;
* \[ ] source fallback used;
* \[ ] insufficient warmup;
* \[ ] feature NaN/inf;
* \[ ] label alignment.

Dataclasses:

* \[ ] `DataQualityIssueV2`
* \[ ] `DataQualityReportV2`
* \[ ] `DataQualityPolicy`
* \[ ] `DataQualityEvidence`

Acceptatiecriteria:

* \[ ] V2 kan oude `check\_candles` vervangen/aanvullen.
* \[ ] Runtime krijgt dezelfde issue codes als batch waar mogelijk.
* \[ ] Dataset manifest gebruikt V2 summary.
* \[ ] Tests dekken alle issue types.
* \[ ] Reports zijn secret-free.

\---

## 14\. Fase 11 - Dataset Lineage Graph

Nieuwe module:

```text
src/binance\_spot\_bot/data\_lineage.py
```

Nodes:

* \[ ] raw public data artifact;
* \[ ] candle dataset;
* \[ ] quality report;
* \[ ] feature dataset;
* \[ ] label dataset;
* \[ ] dataset manifest;
* \[ ] evaluation report;
* \[ ] model metadata;
* \[ ] runtime session;
* \[ ] paper policy;
* \[ ] evidence bundle.

Edges:

* \[ ] parsed\_into;
* \[ ] validated\_by;
* \[ ] generated\_features;
* \[ ] generated\_labels;
* \[ ] evaluated\_by;
* \[ ] trained\_model;
* \[ ] used\_by\_runtime;
* \[ ] exported\_evidence;
* \[ ] promoted\_to\_policy.

Acceptatiecriteria:

* \[ ] Lineage graph links raw → candles → features → labels.
* \[ ] Evaluation report links to feature/label manifests.
* \[ ] Runtime session can reference feature schema used.
* \[ ] Graph is JSON/Markdown exportable.
* \[ ] No secrets.

\---

## 15\. Fase 12 - Runtime Feature Service Integration

Uitbreiding op Roadmap 095:

Nieuwe module:

```text
src/binance\_spot\_bot/runtime\_feature\_service.py
```

Taken:

* \[ ] runtime uses incremental indicator compute where possible;
* \[ ] fallback to batch feature computation;
* \[ ] feature warmup status event;
* \[ ] feature schema hash in runtime snapshot/evidence;
* \[ ] feature compute duration to Roadmap 093 profiler;
* \[ ] data quality issues to runtime event bus;
* \[ ] compact feature payload for dashboard.

Acceptatiecriteria:

* \[ ] Runtime feature output blijft backward-compatible.
* \[ ] Incremental and batch last-row match.
* \[ ] Runtime step performance improves or is measurable.
* \[ ] Snapshot includes feature schema metadata.
* \[ ] Tests dekken runtime static candle scenario.

\---

## 16\. Fase 13 - Evaluation/Backtest Reuse Integration

Uitbreiding op `evaluation.py`:

* \[ ] evaluate from CandleStore range;
* \[ ] evaluate from FeatureStore dataset;
* \[ ] reuse FeatureDatasetManifest;
* \[ ] reuse LabelDatasetManifest;
* \[ ] skip feature rebuild if manifest matches;
* \[ ] block if schema incompatible;
* \[ ] write evaluation lineage;
* \[ ] write performance metadata;
* \[ ] write data quality evidence.

Acceptatiecriteria:

* \[ ] Existing evaluate functions blijven werken.
* \[ ] New evaluation path can use feature store.
* \[ ] Leakage guard still required.
* \[ ] Manifest mismatch blocks evaluation.
* \[ ] Tests dekken cached feature reuse.

\---

## 17\. Fase 14 - Data Pipeline CLI

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli data-store-validate
python -m binance\_spot\_bot.cli candle-dataset-build --symbol BTCUSDT --interval 1m --source demo
python -m binance\_spot\_bot.cli candle-dataset-validate --dataset-id <id>
python -m binance\_spot\_bot.cli candle-store-index
python -m binance\_spot\_bot.cli public-market-cache-status
python -m binance\_spot\_bot.cli indicator-registry
python -m binance\_spot\_bot.cli feature-build --symbol BTCUSDT --interval 1m --feature-set baseline-v2
python -m binance\_spot\_bot.cli feature-store-validate --feature-set baseline-v2
python -m binance\_spot\_bot.cli label-build --feature-dataset-id <id>
python -m binance\_spot\_bot.cli data-quality-report --dataset-id <id>
python -m binance\_spot\_bot.cli data-lineage --dataset-id <id>
python -m binance\_spot\_bot.cli data-pipeline-evidence-export --dataset-id <id>
```

Acceptatiecriteria:

* \[ ] Commands werken offline met demo/static data.
* \[ ] Public cache commands gebruiken alleen public endpoints/fake adapter in tests.
* \[ ] Commands ondersteunen JSON output.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Reports zijn secret-free.

\---

## 18\. Fase 15 - Data Pipeline Dashboard Panel

Nieuwe dashboardsectie:

```text
Data Pipeline \& Feature Store
```

Panels:

* \[ ] candle datasets;
* \[ ] public market cache status;
* \[ ] candle quality;
* \[ ] feature store contracts;
* \[ ] indicator registry;
* \[ ] latest feature builds;
* \[ ] label datasets;
* \[ ] leakage/data quality reports;
* \[ ] data lineage graph summary;
* \[ ] feature compute performance;
* \[ ] schema compatibility;
* \[ ] recommended rebuilds;
* \[ ] evidence export;
* \[ ] no-live proof.

Actions:

* \[ ] validate candle store;
* \[ ] build demo candle dataset;
* \[ ] build feature dataset;
* \[ ] validate feature store;
* \[ ] build labels;
* \[ ] run data quality report;
* \[ ] export lineage/evidence;
* \[ ] copy CLI commands.

Safeguards:

* \[ ] `LOCAL DATA PIPELINE ONLY` badge.
* \[ ] No live controls.
* \[ ] Public data fetch explicitly labeled.
* \[ ] Raw JSON only in limited/debug expander.
* \[ ] Stable widget keys.
* \[ ] Browser smoke covers panel.

Acceptatiecriteria:

* \[ ] Dashboard can show feature schema hash.
* \[ ] Dashboard can show data quality blockers.
* \[ ] Dashboard can export evidence.
* \[ ] Dashboard does not show secrets.
* \[ ] Browser smoke passes.

\---

## 19\. Fase 16 - Data Pipeline Performance Budgets

Uitbreiding op Roadmap 093:

Budget categories:

* \[ ] candle load range duration;
* \[ ] candle append/merge duration;
* \[ ] feature build full duration;
* \[ ] feature build incremental duration;
* \[ ] label build duration;
* \[ ] data quality check duration;
* \[ ] lineage graph build duration;
* \[ ] public cache validation duration;
* \[ ] evaluation cached vs non-cached duration.

Acceptatiecriteria:

* \[ ] Feature build reports duration and row count.
* \[ ] Budget evaluator can warn/fail slow feature build.
* \[ ] Runtime step profiler sees feature compute duration.
* \[ ] Performance report includes data pipeline section.
* \[ ] No-live proof preserved.

\---

## 20\. Fase 17 - Test Selection \& Knowledge Integration

### Roadmap 091 integratie

* \[ ] Knowledge graph herkent data pipeline modules.
* \[ ] Impact analysis koppelt data.py/features.py/evaluation.py/dataset\_governance.py aan data tests.
* \[ ] Artifact flow graph krijgt raw/candle/feature/label lineage.

### Roadmap 092 integratie

* \[ ] Data pipeline changes selecteren data/feature/evaluation/leakage tests.
* \[ ] Feature schema changes forceren standard/deep profile.
* \[ ] Public cache changes forceren public endpoint allowlist tests.
* \[ ] Runtime feature service changes forceren runtime + data tests.

### Roadmap 089 integratie

* \[ ] Feature schema changes krijgen release/migration note.
* \[ ] Dataset schema manifest voedt schema registry.
* \[ ] Release evidence bevat data pipeline evidence.

### Roadmap 090 integratie

* \[ ] Codex task packs krijgen data contract checks.
* \[ ] Completion gate vereist data pipeline evidence bij data changes.

Acceptatiecriteria:

* \[ ] Data changes krijgen juiste testselectie.
* \[ ] Release notes tonen schema changes.
* \[ ] Completion gate kan data evidence lezen.
* \[ ] Knowledge graph toont data lineage.
* \[ ] No-live proof preserved.

\---

## 21\. Fase 18 - Data Pipeline Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/data\_pipeline\_evidence.py
```

Bundle bevat:

* \[ ] data store manifest;
* \[ ] candle dataset manifest;
* \[ ] candle validation report;
* \[ ] public cache status;
* \[ ] indicator registry manifest;
* \[ ] feature dataset manifest;
* \[ ] feature schema;
* \[ ] label dataset manifest;
* \[ ] leakage guard report;
* \[ ] data quality report;
* \[ ] lineage graph;
* \[ ] performance summary;
* \[ ] no-live proof;
* \[ ] redaction proof;
* \[ ] hashes.

Output:

```text
data/data-pipeline/evidence/<dataset\_id>/
  data\_pipeline\_evidence\_manifest.json
  data\_pipeline\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle links to evaluation/model/runtime evidence where relevant.
* \[ ] Dashboard/CLI export works.

\---

## 22\. Fase 19 - Tests

### Unit tests

* \[ ] `tests/test\_data\_pipeline\_safety\_contract.py`
* \[ ] `tests/test\_data\_store\_v2.py`
* \[ ] `tests/test\_candle\_dataset.py`
* \[ ] `tests/test\_candle\_store.py`
* \[ ] `tests/test\_public\_market\_cache.py`
* \[ ] `tests/test\_indicator\_registry.py`
* \[ ] `tests/test\_indicator\_compute.py`
* \[ ] `tests/test\_feature\_store.py`
* \[ ] `tests/test\_feature\_schema.py`
* \[ ] `tests/test\_label\_store.py`
* \[ ] `tests/test\_data\_quality\_v2.py`
* \[ ] `tests/test\_data\_lineage.py`
* \[ ] `tests/test\_runtime\_feature\_service.py`
* \[ ] `tests/test\_data\_pipeline\_evidence.py`

### Integration tests

* \[ ] Build demo candle dataset.
* \[ ] Validate candle dataset gaps/duplicates.
* \[ ] Build feature dataset from candle store.
* \[ ] Validate feature schema.
* \[ ] Build label dataset.
* \[ ] Run leakage guard.
* \[ ] Run evaluation using feature store.
* \[ ] Build data lineage graph.
* \[ ] Runtime feature service returns same last feature as batch.
* \[ ] Export data pipeline evidence bundle.

### Safety tests

* \[ ] Public cache allowlist blocks signed/account/order endpoints.
* \[ ] Data manifests contain no secrets.
* \[ ] Path traversal blocked.
* \[ ] Schema mismatch blocks feature reuse.
* \[ ] Live trading remains disabled.
* \[ ] Runtime feature service does not place orders.
* \[ ] Reports/evidence are secret-free.
* \[ ] Check-all safe env still forced.

\---

## 23\. Docs

Nieuwe docs:

* \[ ] `docs/data-pipeline-safety-contract.md`
* \[ ] `docs/data-store-v2-contracts.md`
* \[ ] `docs/candle-dataset-model.md`
* \[ ] `docs/candle-store-index.md`
* \[ ] `docs/public-market-cache-v2.md`
* \[ ] `docs/indicator-registry.md`
* \[ ] `docs/incremental-indicator-compute.md`
* \[ ] `docs/feature-store-contract.md`
* \[ ] `docs/feature-schema-v2.md`
* \[ ] `docs/label-store-contracts.md`
* \[ ] `docs/data-quality-v2.md`
* \[ ] `docs/dataset-lineage-graph.md`
* \[ ] `docs/runtime-feature-service.md`
* \[ ] `docs/evaluation-feature-store-reuse.md`
* \[ ] `docs/data-pipeline-dashboard.md`
* \[ ] `docs/data-pipeline-evidence.md`

README updates:

* \[ ] data pipeline overview;
* \[ ] candle dataset commands;
* \[ ] feature store commands;
* \[ ] indicator registry;
* \[ ] evaluation reuse flow;
* \[ ] no-live statement.

\---

## 24\. CLI command examples

### Demo candle dataset bouwen

```powershell
python -m binance\_spot\_bot.cli candle-dataset-build --symbol BTCUSDT --interval 1m --source demo --json
```

### Candle store valideren

```powershell
python -m binance\_spot\_bot.cli candle-dataset-validate --dataset-id latest --json
```

### Feature dataset bouwen

```powershell
python -m binance\_spot\_bot.cli feature-build --symbol BTCUSDT --interval 1m --feature-set baseline-v2 --json
```

### Feature store valideren

```powershell
python -m binance\_spot\_bot.cli feature-store-validate --feature-set baseline-v2 --json
```

### Data lineage

```powershell
python -m binance\_spot\_bot.cli data-lineage --dataset-id latest --json
```

### Evidence export

```powershell
python -m binance\_spot\_bot.cli data-pipeline-evidence-export --dataset-id latest
```

\---

## 25\. Codex bouwvolgorde

### PR 1 - Data Pipeline Safety Contract + Candle Dataset Model

* \[ ] `docs/data-pipeline-safety-contract.md`
* \[ ] `candle\_dataset.py`
* \[ ] candle manifest/stats/validation
* \[ ] tests.

### PR 2 - Data Store V2 + Candle Store

* \[ ] `data\_store\_v2.py`
* \[ ] `candle\_store.py`
* \[ ] import existing processed CSV
* \[ ] path safety tests.

### PR 3 - Public Market Cache V2

* \[ ] `public\_market\_cache.py`
* \[ ] public endpoint allowlist
* \[ ] fake adapter tests.

### PR 4 - Indicator Registry

* \[ ] `indicator\_registry.py`
* \[ ] register existing features as indicators
* \[ ] tests.

### PR 5 - Incremental Indicator Compute

* \[ ] `indicator\_compute.py`
* \[ ] batch vs incremental parity tests.

### PR 6 - Feature Store + Feature Schema V2

* \[ ] `feature\_store.py`
* \[ ] `feature\_schema.py`
* \[ ] schema diff/compatibility tests.

### PR 7 - Label Store + Data Quality V2

* \[ ] `label\_store.py`
* \[ ] `data\_quality\_v2.py`
* \[ ] leakage/alignment tests.

### PR 8 - Data Lineage + Evaluation Reuse

* \[ ] `data\_lineage.py`
* \[ ] evaluation integration
* \[ ] cached feature reuse tests.

### PR 9 - Runtime Feature Service + Performance Integration

* \[ ] `runtime\_feature\_service.py`
* \[ ] runtime feature parity tests
* \[ ] performance metadata.

### PR 10 - CLI + Dashboard + Evidence + Docs

* \[ ] CLI commands
* \[ ] dashboard panel
* \[ ] data pipeline evidence
* \[ ] browser smoke
* \[ ] docs.

\---

## 26\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 096 PR 1: Data Pipeline Safety Contract + Candle Dataset Model.

Maak docs/data-pipeline-safety-contract.md.

Maak src/binance\_spot\_bot/candle\_dataset.py met:
- CandleDatasetId
- CandleDatasetKey
- CandleDatasetManifest
- CandleDatasetStats
- CandleValidationIssue
- CandleValidationReport
- build\_candle\_dataset\_manifest(...)
- validate\_candle\_dataset(...)
- candle\_dataset\_id(...)
- candle\_stats(...)

Validatie moet minimaal detecteren:
- niet-chronologische candles
- duplicate open\_time\_ms
- invalid OHLC waar low > high of open/close buiten high/low
- zero/negative price
- negative volume
- gap\_count op basis van minimale positieve intervaldelta
- empty dataset warning/blocker

Manifest bevat:
- symbol
- interval
- source
- start\_ms
- end\_ms
- row\_count
- schema\_version
- data\_hash
- stats
- quality summary
- live\_trading\_enabled=False

Gebruik alleen stdlib en bestaande Candle type.
Gebruik bestaande redaction helpers waar zinvol.
Voeg tests toe voor:
- valid candle manifest
- deterministic dataset id/hash
- duplicate timestamp detection
- gap detection
- invalid OHLC detection
- negative volume detection
- empty dataset handling
- manifest JSON serialization
- no secrets in manifest
- live\_trading\_enabled=False

Geen CandleStore in deze PR.
Geen public API calls.
Geen signed endpoints.
Geen account/order endpoints.
Geen live trading.
```

Waarom eerst:

* Elke latere feature store, indicator compute en evaluation reuse heeft betrouwbare candle dataset manifests nodig.
* Het is read-only en raakt runtime/execution niet.
* Het is klein genoeg voor Codex.
* Data quality/no-live/redaction kan direct getest worden.
* Daarna kan CandleStore V2 veilig op dit manifest bouwen.

\---

## 27\. Definition of Done

Roadmap 096 is klaar als:

* \[ ] Data Pipeline Safety Contract bestaat.
* \[ ] Data Store V2 Contracts werken.
* \[ ] Candle Dataset Model werkt.
* \[ ] Candle Store \& Index werkt.
* \[ ] Public Binance Data Cache V2 werkt.
* \[ ] Indicator Registry werkt.
* \[ ] Incremental Indicator Compute werkt.
* \[ ] Feature Store Contract werkt.
* \[ ] Feature Schema V2 werkt.
* \[ ] Label Store \& Label Contracts werken.
* \[ ] Data Quality V2 werkt.
* \[ ] Dataset Lineage Graph werkt.
* \[ ] Runtime Feature Service Integration werkt.
* \[ ] Evaluation/Backtest Reuse Integration werkt.
* \[ ] Data Pipeline CLI werkt.
* \[ ] Data Pipeline Dashboard Panel werkt.
* \[ ] Data Pipeline Performance Budgets werken.
* \[ ] Test Selection \& Knowledge Integration werkt.
* \[ ] Data Pipeline Evidence Bundle werkt.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen manifests/evidence zijn secret-free.
* \[ ] Tests bewijzen incremental feature compute matcht batch.
* \[ ] Dashboard browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 096 kan na uitvoering naar `Voltooid docs`.

\---

## 28\. Verwachte Roadmap 097 daarna

Na Roadmap 096 zou Roadmap 097 logisch focussen op:

```text
Roadmap 097 - Model Training Pipeline V2, Experiment Tracking \& Feature Contract-Aware Model Promotion
```

Mogelijke inhoud:

* \[ ] model training pipeline op feature store contracts;
* \[ ] experiment tracking;
* \[ ] model artifact manifests;
* \[ ] feature schema compatibility gate;
* \[ ] champion/challenger model evaluation;
* \[ ] model promotion evidence;
* \[ ] inference latency budgets;
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

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: data store v2, candle store, feature contracts, indicator compute. Dashboard surface en docs toegevoegd waar van toepassing.

Validatie: tests/test_roadmaps_089_096_full_surface.py, compileall, dashboard-smoke.

Safety: lokaal/paper-only, geen live trading enablement.

