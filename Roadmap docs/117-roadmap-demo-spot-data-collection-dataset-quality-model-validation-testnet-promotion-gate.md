# Roadmap 117 - Demo Spot Data Collection Sprint, Dataset Quality Burn-Down, Model Validation Improvement \& Testnet Promotion Gate

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/117-roadmap-demo-spot-data-collection-dataset-quality-model-validation-testnet-promotion-gate.md
```

## Samenvatting

Roadmap 116 maakt de bot-app zoals gewenst:

```text
1 klikbaar startbestand
→ alles start samen
→ Dashboard V2 Control Center opent
→ profiel kiezen: backtest / paper / demo spot / testnet / live locked
→ config/API keys invullen
→ Start klikken
→ bot haalt data op en draait in gekozen mode
```

Roadmap 117 is de logische vervolgstap voordat echte live trading ooit veilig kan worden overwogen: **de bot moet eerst genoeg goede demo spot trading data verzamelen, die data schoonmaken, datasetkwaliteit meten, modellen/strategieën valideren, paper/testnet rehearsals draaien en pas daarna een promotion gate naar “live-ready review” halen.**

Deze roadmap focust dus niet op “live direct aanzetten”, maar op het bouwen van de datagedreven brug richting live:

```text
Demo Spot Control Center
→ Demo Spot Data Recorder
→ Dataset Vault
→ Dataset Quality Burn-Down
→ Feature/Label Builder
→ Model/Strategy Validation
→ Backtest + Walk-Forward
→ Paper Replay
→ Testnet Promotion Gate
→ Live Readiness Evidence
```

Belangrijk: live trading blijft standaard locked. De huidige code ondersteunt al `TradingMode.LIVE`, maar de execution layer blokkeert echte live order placement nog bewust met: `live order placement requires a separate manual implementation step`. Roadmap 117 respecteert dat. Het doel is bewijs en validatie opbouwen, niet live orders plaatsen.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 117`, `117-roadmap`, `Live Trading Dry-Run`, `Testnet-to-Live Promotion Gate`, `Minimal Real-Order Execution Safety Layer` en `Demo Spot Data Collection Sprint`.
* \[x] Geen bestaande Roadmap 117 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 116 is lokaal aangemaakt als One-Click Bot Launcher, Unified Control Center, Demo-Data Training Pipeline \& Safe Live Trading Gate.

### Codebasecontrole

Breed bekeken met focus op live gating, Binance adapter, execution, config, modes, demo/testnet/live readiness en safe defaults:

* \[x] `src/binance\_spot\_bot/config.py`
* \[x] `src/binance\_spot\_bot/types.py`
* \[x] `src/binance\_spot\_bot/binance.py`
* \[x] `src/binance\_spot\_bot/execution.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/market\_data\_source.py`
* \[x] `src/binance\_spot\_bot/paper.py`
* \[x] `src/binance\_spot\_bot/paper\_accounting.py`
* \[x] `src/binance\_spot\_bot/risk.py`
* \[x] `src/binance\_spot\_bot/session\_store.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] roadmaplijn 104-116.

### Belangrijke conclusies uit de codebase

* \[x] `TradingMode` bevat al `disabled`, `paper`, `testnet` en `live`.
* \[x] `BotSettings` leest live safety-instellingen uit env:

  * `LIVE\_TRADING\_ENABLED`;
  * `KILL\_SWITCH`;
  * `MANUAL\_LIVE\_APPROVAL`;
  * `MAX\_DAILY\_LOSS\_QUOTE`;
  * `MAX\_POSITION\_QUOTE`;
  * `MAX\_TRADES\_PER\_DAY`;
  * `MIN\_SIGNAL\_CONFIDENCE`;
  * `MAX\_SPREAD\_BPS`.
* \[x] `validate\_live\_readiness()` blokkeert live tenzij app env, live flag, kill switch, manual approval, risk limits en API credentials correct staan.
* \[x] `BinanceSpotAdapter` heeft public market endpoints én signed/account/order endpoints. Roadmap 117 moet data collection toestaan, maar signed live order routes blijven geblokkeerd.
* \[x] `ExecutionEngine` kan paper fills doen en demo/testnet orders guarded uitvoeren, maar live order placement is nog bewust niet geïmplementeerd.
* \[x] De adapter heeft signed routes zoals `place\_order`, `cancel\_order`, `get\_order`, `open\_orders` en `query\_order`; die mogen niet door demo-data/training code gebruikt worden voor live.
* \[x] Roadmap 116 bouwt de one-click app, profielen, demo recorder, training dataset builder en live readiness gate.
* \[x] Roadmap 117 moet daarna zorgen dat die live-readiness gate echte data/evidence krijgt.

### Grootste gat na Roadmap 116

Roadmap 116 bouwt de infrastructuur, maar daarna heb je nog niet automatisch “goede data” of “goede validation”. Wat nog mist:

* \[ ] genoeg demo spot sessies;
* \[ ] sessies met verschillende marktomstandigheden;
* \[ ] genoeg candles, signals, risk decisions, fills en rejected orders;
* \[ ] data quality score;
* \[ ] leakage checks;
* \[ ] feature/label consistency;
* \[ ] model/strategy validation grade;
* \[ ] paper replay bewijs;
* \[ ] testnet promotion bewijs;
* \[ ] live readiness evidence;
* \[ ] dashboard dat exact toont waarom live nog locked is.

Roadmap 117 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 117

Maak een datagedreven live-training en promotion pipeline:

```text
Demo spot data
→ quality gates
→ training/validation dataset
→ model/strategy validation
→ paper replay
→ testnet promotion
→ live readiness evidence
```

Na Roadmap 117 moet de bot:

* \[ ] demo spot trading sessies kunnen verzamelen als training/validatiebron;
* \[ ] datasetkwaliteit kunnen meten;
* \[ ] slechte/missende data kunnen tonen als burn-down backlog;
* \[ ] feature/label datasets kunnen bouwen;
* \[ ] model/strategy validation kunnen scoren;
* \[ ] paper replay kunnen draaien op demo-derived data;
* \[ ] testnet promotion kunnen blokkeren of toestaan;
* \[ ] live readiness evidence kunnen exporteren;
* \[ ] live trading locked houden zolang gates niet groen zijn;
* \[ ] in het dashboard duidelijk tonen wat nog ontbreekt voor live readiness.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen one-click launcher opnieuw bouwen; Roadmap 116 doet dat.
* \[ ] Geen Dashboard V2 foundation opnieuw bouwen.
* \[ ] Geen Strategy/Portfolio Labs opnieuw bouwen.
* \[ ] Geen Binance adapter herschrijven.
* \[ ] Geen live order placement implementeren.
* \[ ] Geen live trading automatisch activeren.
* \[ ] Geen live start vanuit launcher.
* \[ ] Geen signed live order route gebruiken voor training.
* \[ ] Geen API keys opslaan in datasets.
* \[ ] Geen financial advice.
* \[ ] Geen model claimen als “winstgevend” zonder evidence.
* \[ ] Geen testnet promotion zonder demo data quality.

Wel doen:

* \[ ] demo data collection sprint;
* \[ ] dataset quality burn-down;
* \[ ] feature/label builder hardening;
* \[ ] model/strategy validation evidence;
* \[ ] paper replay validation;
* \[ ] testnet promotion gate;
* \[ ] live readiness dashboard;
* \[ ] evidence bundle;
* \[ ] UAT/check-all/browser smoke.

\---

## 3\. Fase 0 - Demo-to-Live Training Safety Contract

Nieuw docbestand:

```text
docs/live-training/demo-to-live-training-safety-contract.md
```

Regels:

* \[ ] Demo-data training is local-only.
* \[ ] Geen live trading.
* \[ ] Geen live order placement.
* \[ ] Geen live auto-start.
* \[ ] Geen account/live signed order routes in dataset builder.
* \[ ] Demo/testnet signed routes alleen binnen demo/testnet profiel en guarded.
* \[ ] Raw API keys/secrets nooit in datasets, logs of evidence.
* \[ ] Training output is geen financieel advies.
* \[ ] Model validation output zegt niet “gegarandeerde winst”.
* \[ ] Live blijft locked tot alle gates pass.
* \[ ] Testnet promotion vereist demo dataset quality pass.
* \[ ] Live readiness vereist demo + paper + testnet evidence.
* \[ ] Elke report bevat:

  * `live\_trading\_enabled=False` tenzij expliciete readiness context;
  * `live\_execution\_enabled=False`;
  * `not\_financial\_advice\_statement`.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen live order routes geblokkeerd blijven.
* \[ ] Tests bewijzen datasets secret-free zijn.
* \[ ] Tests bewijzen live locked blijft zonder evidence.
* \[ ] Tests bewijzen no-advice wording.

\---

## 4\. Fase 1 - Demo Session Target Plan

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/demo\_session\_targets.py
```

Doel: bepalen hoeveel en welke demo spot data nodig is.

Target metrics:

* \[ ] minimum demo sessions;
* \[ ] minimum total runtime minutes;
* \[ ] minimum candles;
* \[ ] minimum signals;
* \[ ] minimum ALLOW/BLOCK risk decisions;
* \[ ] minimum demo order previews;
* \[ ] minimum test orders;
* \[ ] minimum placed demo orders;
* \[ ] minimum fills;
* \[ ] minimum rejected/cancelled cases;
* \[ ] minimum spread samples;
* \[ ] minimum latency samples;
* \[ ] minimum reconciliation runs;
* \[ ] minimum market regimes:

  * calm;
  * volatile;
  * low volume;
  * high spread;
  * trending;
  * ranging.

Dataclasses:

* \[ ] `DemoSessionTarget`
* \[ ] `DemoSessionTargetProgress`
* \[ ] `DemoSessionTargetReport`

Acceptatiecriteria:

* \[ ] Target plan is configurable.
* \[ ] Target progress works from fixture sessions.
* \[ ] Missing target data creates burn-down items.
* \[ ] Report is JSON + Markdown.
* \[ ] Dashboard can show progress.

\---

## 5\. Fase 2 - Demo Spot Recording Hardening

Uitbreid Roadmap 116 recorder:

```text
src/binance\_spot\_bot/live\_training/demo\_spot\_data\_recorder.py
```

Extra recording requirements:

* \[ ] session manifest per run;
* \[ ] event sequence numbers;
* \[ ] event hash chain;
* \[ ] clock/source timestamps;
* \[ ] profile id;
* \[ ] symbol/interval;
* \[ ] exchange profile;
* \[ ] model alias;
* \[ ] strategy id;
* \[ ] risk preset;
* \[ ] market data source;
* \[ ] order preview events;
* \[ ] risk decision events;
* \[ ] execution result events;
* \[ ] demo order response events;
* \[ ] reconciliation events;
* \[ ] recorder health events;
* \[ ] dropped event counter;
* \[ ] redaction self-test.

Acceptatiecriteria:

* \[ ] Recorder can resume after dashboard reconnect.
* \[ ] Hash chain validates.
* \[ ] Dropped events are reported.
* \[ ] Raw secrets blocked.
* \[ ] Tests cover corrupt/missing event cases.

\---

## 6\. Fase 3 - Demo Dataset Vault

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/demo\_dataset\_vault.py
```

Storage:

```text
data/live-training/demo-vault/
  raw-events/
  normalized/
  manifests/
  quality/
  features/
  labels/
  splits/
  evidence/
```

Functions:

* \[ ] ingest recorder sessions;
* \[ ] normalize events;
* \[ ] deduplicate events;
* \[ ] index by symbol/session/time;
* \[ ] validate hash chains;
* \[ ] store dataset manifests;
* \[ ] export dataset summary;
* \[ ] verify vault integrity;
* \[ ] purge bad/duplicate sessions with confirm;
* \[ ] never store raw secrets.

Acceptatiecriteria:

* \[ ] Vault ingests fixture sessions.
* \[ ] Vault rejects raw secret fields.
* \[ ] Vault detects duplicate sessions.
* \[ ] Vault produces manifest/hashes.
* \[ ] Tests use temp dirs.

\---

## 7\. Fase 4 - Dataset Quality Burn-Down Board

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/dataset\_quality\_burndown.py
```

Quality issue categories:

* \[ ] missing candles;
* \[ ] missing top-of-book;
* \[ ] missing spread samples;
* \[ ] missing risk decisions;
* \[ ] missing fills;
* \[ ] missing rejections;
* \[ ] missing reconciliation;
* \[ ] stale market data;
* \[ ] duplicate timestamps;
* \[ ] out-of-order events;
* \[ ] inconsistent symbol/interval;
* \[ ] too few sessions;
* \[ ] too few market regimes;
* \[ ] leaked secret-like value;
* \[ ] suspicious leakage;
* \[ ] missing model version;
* \[ ] missing strategy id;
* \[ ] insufficient paper replay coverage.

Priorities:

* \[ ] DQ-P0: secret leak/live contamination/leakage/no-live failure;
* \[ ] DQ-P1: missing critical data;
* \[ ] DQ-P2: weak validation coverage;
* \[ ] DQ-P3: quality improvement;
* \[ ] DQ-P4: polish.

Acceptatiecriteria:

* \[ ] Burn-down board generated from vault.
* \[ ] P0 blocks validation.
* \[ ] Board visible in dashboard.
* \[ ] Board export Markdown + JSON.
* \[ ] Tests cover priority mapping.

\---

## 8\. Fase 5 - Demo Dataset Quality Gate v2

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/demo\_dataset\_quality\_v2.py
```

Quality scoring:

* \[ ] completeness score;
* \[ ] freshness score;
* \[ ] coverage score;
* \[ ] event consistency score;
* \[ ] order/fill reconciliation score;
* \[ ] market regime diversity score;
* \[ ] symbol/interval consistency score;
* \[ ] model/strategy metadata score;
* \[ ] secret-free score;
* \[ ] no-live-contamination score;
* \[ ] leakage risk score.

Grades:

* \[ ] A: usable for live-readiness validation;
* \[ ] B: usable with warnings;
* \[ ] C: usable for paper only;
* \[ ] D: collect more demo data;
* \[ ] F: invalid/unsafe.

Hard blockers:

* \[ ] secret leak;
* \[ ] live event contamination;
* \[ ] missing no-live proof;
* \[ ] no fills/orders when required;
* \[ ] unreconciled critical orders;
* \[ ] severe timestamp corruption;
* \[ ] leakage risk high.

Acceptatiecriteria:

* \[ ] Quality gate deterministic.
* \[ ] Grade A/B can feed model validation.
* \[ ] C/D/F block testnet/live promotion.
* \[ ] Report links burn-down issues.
* \[ ] Tests cover all grades.

\---

## 9\. Fase 6 - Feature/Label Dataset Builder v2

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/feature\_label\_dataset.py
```

Feature groups:

* \[ ] candle features;
* \[ ] volume features;
* \[ ] spread features;
* \[ ] top-of-book features;
* \[ ] volatility features;
* \[ ] momentum features;
* \[ ] signal confidence features;
* \[ ] risk decision features;
* \[ ] order preview features;
* \[ ] latency/slippage features;
* \[ ] reconciliation features;
* \[ ] model context features.

Label/outcome groups:

* \[ ] future return labels;
* \[ ] demo fill outcome labels;
* \[ ] risk block labels;
* \[ ] slippage labels;
* \[ ] rejected order labels;
* \[ ] session drawdown labels;
* \[ ] paper replay outcome labels.

Output:

* \[ ] features JSON/CSV/Parquet optional later;
* \[ ] labels JSON/CSV;
* \[ ] data dictionary;
* \[ ] split manifest;
* \[ ] leakage report;
* \[ ] feature coverage report;
* \[ ] hash manifest.

Acceptatiecriteria:

* \[ ] Builds from vault fixture.
* \[ ] Missing optional features create warnings.
* \[ ] Leakage checks run.
* \[ ] Dataset is secret-free.
* \[ ] Tests cover feature alignment.

\---

## 10\. Fase 7 - Train/Validation/Test Split Governance

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/split\_governance.py
```

Split modes:

* \[ ] chronological train/validation/test;
* \[ ] session-based split;
* \[ ] symbol-based holdout;
* \[ ] walk-forward split;
* \[ ] latest-session holdout;
* \[ ] stress-regime holdout.

Rules:

* \[ ] train ends before validation;
* \[ ] validation ends before test;
* \[ ] no event leakage;
* \[ ] no duplicate session across splits;
* \[ ] at least N samples per split;
* \[ ] preserve market regime metadata;
* \[ ] test split is never used for tuning;
* \[ ] split manifest immutable after validation unless versioned.

Acceptatiecriteria:

* \[ ] Split governance report generated.
* \[ ] Leakage blocks validation.
* \[ ] Small datasets warn/block.
* \[ ] Tests cover split edge cases.
* \[ ] Dashboard shows split health.

\---

## 11\. Fase 8 - Model Candidate Registry

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/model\_candidate\_registry.py
```

Registry tracks:

* \[ ] model candidate id;
* \[ ] model alias;
* \[ ] model version;
* \[ ] strategy id;
* \[ ] dataset version;
* \[ ] feature set version;
* \[ ] training config hash;
* \[ ] validation report path;
* \[ ] paper replay report path;
* \[ ] testnet rehearsal report path;
* \[ ] promotion state;
* \[ ] blockers;
* \[ ] created\_at\_ms;
* \[ ] updated\_at\_ms.

Promotion states:

* \[ ] draft;
* \[ ] dataset\_ready;
* \[ ] validation\_running;
* \[ ] validation\_passed;
* \[ ] paper\_replay\_required;
* \[ ] paper\_replay\_passed;
* \[ ] testnet\_required;
* \[ ] testnet\_passed;
* \[ ] live\_readiness\_candidate;
* \[ ] blocked;
* \[ ] rejected;
* \[ ] expired.

Acceptatiecriteria:

* \[ ] Registry stores model candidates.
* \[ ] State transitions validated.
* \[ ] Cannot skip paper/testnet gates.
* \[ ] Reports redacted.
* \[ ] Tests cover state machine.

\---

## 12\. Fase 9 - Model/Strategy Validation Runner

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/model\_strategy\_validation.py
```

Validation checks:

* \[ ] dataset quality grade;
* \[ ] split governance pass;
* \[ ] baseline strategy comparison;
* \[ ] selected model/strategy performance;
* \[ ] precision/recall or signal quality metrics where relevant;
* \[ ] confidence calibration;
* \[ ] risk block compatibility;
* \[ ] drawdown limits;
* \[ ] overfit gap;
* \[ ] rejected order analysis;
* \[ ] slippage/latency assumptions;
* \[ ] session robustness;
* \[ ] market regime coverage.

Grades:

* \[ ] A: promotion eligible;
* \[ ] B: eligible with warnings;
* \[ ] C: paper-only continue testing;
* \[ ] D: blocked;
* \[ ] F: invalid/unsafe.

Acceptatiecriteria:

* \[ ] Runner works on fixture dataset.
* \[ ] Runner compares against baseline.
* \[ ] Overfit/leakage blocks.
* \[ ] No profit guarantee wording.
* \[ ] Tests cover grades.

\---

## 13\. Fase 10 - Paper Replay From Demo Dataset

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/paper\_replay\_from\_demo.py
```

Purpose:

* \[ ] replay demo-derived candles/features through paper runtime;
* \[ ] compare expected signals vs observed demo signals;
* \[ ] compare risk decisions;
* \[ ] estimate paper fills;
* \[ ] compare slippage assumptions;
* \[ ] validate stop/kill-switch logic;
* \[ ] produce paper replay report.

Outputs:

* \[ ] paper replay equity curve;
* \[ ] fills;
* \[ ] risk blocks;
* \[ ] signal agreement;
* \[ ] drawdown;
* \[ ] fee/slippage estimate;
* \[ ] validation status;
* \[ ] blockers/warnings.

Acceptatiecriteria:

* \[ ] Replay works without API keys.
* \[ ] Replay uses demo-derived dataset.
* \[ ] Replay cannot place orders.
* \[ ] Results feed model registry.
* \[ ] Tests use fixture dataset.

\---

## 14\. Fase 11 - Demo-to-Testnet Promotion Gate

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/testnet\_promotion\_gate.py
```

Promotion requires:

* \[ ] demo session targets met minimum progress;
* \[ ] demo dataset quality grade A/B;
* \[ ] feature/label dataset built;
* \[ ] split governance pass;
* \[ ] model/strategy validation grade A/B;
* \[ ] paper replay pass;
* \[ ] risk limits valid;
* \[ ] testnet credentials present;
* \[ ] testnet base URL verified;
* \[ ] symbol filters loaded;
* \[ ] max testnet order size cap;
* \[ ] operator confirmation.

Gate states:

* \[ ] not\_ready;
* \[ ] collect\_more\_demo\_data;
* \[ ] fix\_dataset\_quality;
* \[ ] validation\_required;
* \[ ] paper\_replay\_required;
* \[ ] ready\_for\_testnet\_rehearsal;
* \[ ] testnet\_blocked;
* \[ ] testnet\_promoted.

Acceptatiecriteria:

* \[ ] Gate blocks without demo data.
* \[ ] Gate blocks low dataset grade.
* \[ ] Gate blocks missing paper replay.
* \[ ] Gate can produce promoted state.
* \[ ] Tests cover all states.

\---

## 15\. Fase 12 - Testnet Rehearsal Runner

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/testnet\_rehearsal\_runner.py
```

Purpose:

* \[ ] run controlled testnet rehearsal after promotion gate.
* \[ ] verify signed endpoint readiness.
* \[ ] run test order.
* \[ ] optionally run tiny testnet order if allowed by testnet profile.
* \[ ] reconcile order.
* \[ ] test cancel flow.
* \[ ] test stop/kill-switch flow.
* \[ ] record all results.
* \[ ] never use live base URL.
* \[ ] feed live readiness evidence.

Acceptatiecriteria:

* \[ ] Testnet base URL required.
* \[ ] Live base URL blocked.
* \[ ] Max rehearsal order count enforced.
* \[ ] Reconciliation required.
* \[ ] Tests use fake adapter.

\---

## 16\. Fase 13 - Testnet-to-Live Readiness Candidate Gate

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/live\_candidate\_gate.py
```

Live candidate requires:

* \[ ] demo dataset evidence;
* \[ ] model validation evidence;
* \[ ] paper replay evidence;
* \[ ] testnet rehearsal evidence;
* \[ ] risk config evidence;
* \[ ] live profile validation;
* \[ ] live API key permission check, read-only fingerprint first;
* \[ ] order preview support;
* \[ ] live execution still blocked until separate implementation gate;
* \[ ] operator live checklist.

Gate states:

* \[ ] blocked;
* \[ ] more\_demo\_data\_needed;
* \[ ] more\_validation\_needed;
* \[ ] more\_testnet\_needed;
* \[ ] live\_readiness\_review;
* \[ ] live\_execution\_not\_implemented;
* \[ ] live\_execution\_gate\_required.

Acceptatiecriteria:

* \[ ] Gate never enables live orders.
* \[ ] Gate produces exact blockers.
* \[ ] Gate requires evidence bundle hashes.
* \[ ] Dashboard can show live candidate status.
* \[ ] Tests cover gate states.

\---

## 17\. Fase 14 - Live Training Dashboard

Nieuwe Dashboard V2 route:

```text
/live-training
```

Sections:

* \[ ] demo session target progress;
* \[ ] demo recorder status;
* \[ ] dataset vault status;
* \[ ] dataset quality burn-down;
* \[ ] quality gate grade;
* \[ ] feature/label dataset builder;
* \[ ] split governance;
* \[ ] model candidate registry;
* \[ ] model/strategy validation;
* \[ ] paper replay;
* \[ ] testnet promotion gate;
* \[ ] testnet rehearsal;
* \[ ] live candidate gate;
* \[ ] evidence export;
* \[ ] live locked banner.

Acceptatiecriteria:

* \[ ] Dashboard shows exactly what data is missing.
* \[ ] Dashboard can trigger dataset build.
* \[ ] Dashboard can trigger validation.
* \[ ] Dashboard can show testnet promotion blockers.
* \[ ] Browser smoke covers live-training page.

\---

## 18\. Fase 15 - Control Center Live-Training Integration

Update `/control-center` from Roadmap 116:

* \[ ] live profile card shows training requirements;
* \[ ] demo profile card shows recorder progress;
* \[ ] Start Demo Session button;
* \[ ] Build Dataset button;
* \[ ] Run Quality Gate button;
* \[ ] Run Model Validation button;
* \[ ] Run Paper Replay button;
* \[ ] Run Testnet Promotion Check button;
* \[ ] Live locked reason panel;
* \[ ] next-best-action suggestion;
* \[ ] no live start button.

Acceptatiecriteria:

* \[ ] Operator sees live blockers.
* \[ ] Operator sees next data collection step.
* \[ ] Live cannot be armed from Control Center without gates.
* \[ ] Demo data progress visible.
* \[ ] Browser smoke covers blocker flow.

\---

## 19\. Fase 16 - API Routes

Nieuwe API routes:

```text
GET  /api/live-training/health
GET  /api/live-training/demo-targets
GET  /api/live-training/demo-targets/progress
GET  /api/live-training/recordings
POST /api/live-training/recordings/verify
GET  /api/live-training/vault
POST /api/live-training/vault/ingest
GET  /api/live-training/dataset-quality
GET  /api/live-training/dataset-burndown
POST /api/live-training/dataset/build
POST /api/live-training/splits/build
GET  /api/live-training/model-candidates
POST /api/live-training/model-candidates
POST /api/live-training/model-validation/run
POST /api/live-training/paper-replay/run
POST /api/live-training/testnet-promotion/check
POST /api/live-training/testnet-rehearsal/run
POST /api/live-training/live-candidate/check
POST /api/live-training/evidence/export
WS   /ws/live-training
```

API rules:

* \[ ] raw secrets never returned;
* \[ ] live order routes absent;
* \[ ] testnet rehearsal gated;
* \[ ] dataset build requires quality precheck;
* \[ ] model validation requires split governance;
* \[ ] live candidate check does not enable live;
* \[ ] all reports redacted.

Acceptatiecriteria:

* \[ ] TestClient covers routes.
* \[ ] Unsafe actions blocked.
* \[ ] Missing evidence returns blocker.
* \[ ] Secrets redacted.
* \[ ] WebSocket emits training progress.

\---

## 20\. Fase 17 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli demo-session-targets --json
python -m binance\_spot\_bot.cli demo-session-progress --json
python -m binance\_spot\_bot.cli demo-recordings-verify --json
python -m binance\_spot\_bot.cli demo-vault-ingest --profile <id>
python -m binance\_spot\_bot.cli demo-dataset-quality-v2 --json
python -m binance\_spot\_bot.cli demo-dataset-burndown --json
python -m binance\_spot\_bot.cli demo-feature-label-build --json
python -m binance\_spot\_bot.cli split-governance-check --dataset <id> --json
python -m binance\_spot\_bot.cli model-candidates --json
python -m binance\_spot\_bot.cli model-validation-run --candidate <id> --json
python -m binance\_spot\_bot.cli paper-replay-from-demo --candidate <id> --json
python -m binance\_spot\_bot.cli testnet-promotion-check --candidate <id> --json
python -m binance\_spot\_bot.cli testnet-rehearsal-run --candidate <id> --confirm RUN\_TESTNET\_REHEARSAL\_ONLY
python -m binance\_spot\_bot.cli live-candidate-check --candidate <id> --json
python -m binance\_spot\_bot.cli live-training-evidence-export --candidate <id>
python -m binance\_spot\_bot.cli dashboard-v2-live-training-smoke --json
```

Acceptatiecriteria:

* \[ ] Commands werken lokaal.
* \[ ] Commands ondersteunen JSON.
* \[ ] Testnet rehearsal vereist confirm.
* \[ ] Live candidate check enablet geen live orders.
* \[ ] Reports zijn secret-free.

\---

## 21\. Fase 18 - Check-All Integration

Fast profile:

* \[ ] live\_training imports;
* \[ ] demo target plan fixture;
* \[ ] recorder manifest fixture;
* \[ ] vault validation fixture;
* \[ ] dataset quality fixture;
* \[ ] no-live/no-secret tests;
* \[ ] live candidate gate blocks without evidence.

Deep profile:

* \[ ] dataset vault ingest fixture;
* \[ ] quality burn-down fixture;
* \[ ] feature/label dataset fixture;
* \[ ] split governance fixture;
* \[ ] model validation fixture;
* \[ ] paper replay fixture;
* \[ ] testnet promotion fixture;
* \[ ] testnet rehearsal fake adapter;
* \[ ] live candidate gate fixture;
* \[ ] Dashboard live-training browser smoke;
* \[ ] evidence export/verify.

Acceptatiecriteria:

* \[ ] Fast check-all blijft snel.
* \[ ] Deep check-all dekt demo-to-live pipeline.
* \[ ] Secret leak hard fails.
* \[ ] Live route/order enablement hard fails.
* \[ ] Reports redacted.

\---

## 22\. Fase 19 - UAT / Operator Workflow

Roadmap 102 operator docs:

* \[ ] demo data collection guide;
* \[ ] dataset quality guide;
* \[ ] validation gate guide;
* \[ ] paper replay guide;
* \[ ] testnet promotion guide;
* \[ ] live locked/live candidate guide.

Roadmap 103 UAT scenarios:

* \[ ] start demo profile from Control Center;
* \[ ] record demo data;
* \[ ] verify recording manifest;
* \[ ] ingest demo vault;
* \[ ] run dataset quality gate;
* \[ ] inspect burn-down board;
* \[ ] build feature/label dataset;
* \[ ] run split governance;
* \[ ] run model validation;
* \[ ] run paper replay;
* \[ ] run testnet promotion check;
* \[ ] run fake testnet rehearsal;
* \[ ] run live candidate check;
* \[ ] prove live still locked;
* \[ ] export evidence.

Acceptatiecriteria:

* \[ ] UAT confirms live remains locked.
* \[ ] UAT confirms missing demo data is clear.
* \[ ] UAT confirms no secrets in evidence.
* \[ ] UAT confirms dashboard next actions.
* \[ ] UAT evidence linked.

\---

## 23\. Fase 20 - Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/live\_training/demo\_to\_live\_evidence.py
```

Bundle bevat:

* \[ ] safety contract;
* \[ ] demo target plan;
* \[ ] demo target progress;
* \[ ] recorder manifests;
* \[ ] vault manifest;
* \[ ] dataset quality burn-down;
* \[ ] dataset quality v2 report;
* \[ ] feature/label dataset manifest;
* \[ ] split governance report;
* \[ ] model candidate registry state;
* \[ ] model/strategy validation report;
* \[ ] paper replay report;
* \[ ] testnet promotion report;
* \[ ] testnet rehearsal report;
* \[ ] live candidate gate report;
* \[ ] no-live-order proof;
* \[ ] no-secret proof;
* \[ ] no-financial-advice proof;
* \[ ] hashes.

Output:

```text
data/live-training/demo-to-live/evidence/<run\_id>/
  demo\_to\_live\_evidence\_manifest.json
  demo\_to\_live\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Evidence is secret-free.
* \[ ] Evidence has manifest/hash.
* \[ ] Evidence can be verified.
* \[ ] Evidence required for next live roadmap.
* \[ ] Dashboard can download bundle.

\---

## 24\. Fase 21 - Release / Knowledge / Test / Performance Integration

Roadmap 089:

* \[ ] release notes mention demo-to-live training gate;
* \[ ] version manifest includes live-training schema version;
* \[ ] migration notes include dataset vault path.

Roadmap 091:

* \[ ] knowledge graph maps demo recordings → vault → quality → dataset → validation → promotion.
* \[ ] impact analysis detects changes affecting live readiness.

Roadmap 092:

* \[ ] test selector chooses live-training tests for recorder/dataset/validation changes.
* \[ ] Binance adapter signed route changes select safety tests.
* \[ ] Dashboard live-training UI changes select browser smoke.

Roadmap 093:

* \[ ] performance budgets for vault ingest, dataset build, quality gate, validation, paper replay.
* \[ ] slow dataset build findings.

Acceptatiecriteria:

* \[ ] Release evidence includes demo-to-live evidence.
* \[ ] Knowledge graph updated.
* \[ ] Test selection works.
* \[ ] Performance reports include live-training budgets.
* \[ ] Live remains locked.

\---

## 25\. Fase 22 - Scheduled Demo-to-Live Reports

Scheduled jobs:

* \[ ] daily demo target progress report;
* \[ ] daily vault integrity check;
* \[ ] weekly dataset quality report;
* \[ ] weekly burn-down report;
* \[ ] weekly feature/label build dry-run;
* \[ ] weekly model validation check;
* \[ ] weekly paper replay check;
* \[ ] weekly testnet promotion status;
* \[ ] monthly demo-to-live evidence export;
* \[ ] after each demo session: recorder verify + vault ingest.

Metrics:

* \[ ] demo session count;
* \[ ] total candles;
* \[ ] total signals;
* \[ ] total fills;
* \[ ] total rejected orders;
* \[ ] reconciliation pass rate;
* \[ ] dataset quality grade;
* \[ ] burn-down P0/P1 count;
* \[ ] model validation grade;
* \[ ] paper replay status;
* \[ ] testnet promotion status;
* \[ ] live candidate gate blockers.

Acceptatiecriteria:

* \[ ] Jobs are local-only.
* \[ ] Jobs never enable live orders.
* \[ ] Reports are secret-free.
* \[ ] Dashboard can show reports.
* \[ ] Check-all safe env preserved.

\---

## 26\. Tests

### Unit tests

* \[ ] `tests/test\_demo\_to\_live\_training\_safety\_contract.py`
* \[ ] `tests/test\_demo\_session\_targets.py`
* \[ ] `tests/test\_demo\_spot\_data\_recorder\_hardening.py`
* \[ ] `tests/test\_demo\_dataset\_vault.py`
* \[ ] `tests/test\_dataset\_quality\_burndown.py`
* \[ ] `tests/test\_demo\_dataset\_quality\_v2.py`
* \[ ] `tests/test\_feature\_label\_dataset.py`
* \[ ] `tests/test\_split\_governance.py`
* \[ ] `tests/test\_model\_candidate\_registry.py`
* \[ ] `tests/test\_model\_strategy\_validation.py`
* \[ ] `tests/test\_paper\_replay\_from\_demo.py`
* \[ ] `tests/test\_testnet\_promotion\_gate.py`
* \[ ] `tests/test\_testnet\_rehearsal\_runner.py`
* \[ ] `tests/test\_live\_candidate\_gate.py`
* \[ ] `tests/test\_demo\_to\_live\_evidence.py`

### Integration tests

* \[ ] Create demo target fixture.
* \[ ] Record demo event fixture.
* \[ ] Ingest vault.
* \[ ] Generate burn-down board.
* \[ ] Run dataset quality v2.
* \[ ] Build feature/label dataset.
* \[ ] Run split governance.
* \[ ] Register model candidate.
* \[ ] Run validation fixture.
* \[ ] Run paper replay fixture.
* \[ ] Run testnet promotion fixture.
* \[ ] Run fake testnet rehearsal.
* \[ ] Run live candidate gate.
* \[ ] Export evidence.

### Browser smoke

* \[ ] `/live-training` loads.
* \[ ] demo target progress visible.
* \[ ] recorder status visible.
* \[ ] dataset quality grade visible.
* \[ ] burn-down board visible.
* \[ ] model candidate registry visible.
* \[ ] validation gate visible.
* \[ ] testnet promotion visible.
* \[ ] live candidate gate visible.
* \[ ] live locked banner visible.
* \[ ] no live start button visible.

### Safety tests

* \[ ] Live orders remain blocked.
* \[ ] Live auto-start absent.
* \[ ] Signed live order routes not used by training pipeline.
* \[ ] Raw API keys blocked from vault/evidence.
* \[ ] Dataset with secret-like values hard fails.
* \[ ] Low dataset quality blocks testnet promotion.
* \[ ] Missing paper replay blocks live candidate.
* \[ ] Missing testnet rehearsal blocks live candidate.
* \[ ] Profit guarantee wording blocked.
* \[ ] Check-all safe env preserved.

\---

## 27\. Docs

Nieuwe docs:

```text
docs/live-training/demo-to-live-training-safety-contract.md
docs/live-training/demo-session-targets.md
docs/live-training/demo-spot-recording-hardening.md
docs/live-training/demo-dataset-vault.md
docs/live-training/dataset-quality-burndown.md
docs/live-training/demo-dataset-quality-v2.md
docs/live-training/feature-label-dataset.md
docs/live-training/split-governance.md
docs/live-training/model-candidate-registry.md
docs/live-training/model-strategy-validation.md
docs/live-training/paper-replay-from-demo.md
docs/live-training/testnet-promotion-gate.md
docs/live-training/testnet-rehearsal-runner.md
docs/live-training/live-candidate-gate.md
docs/live-training/demo-to-live-evidence.md
```

README updates:

* \[ ] “How live training works”.
* \[ ] Demo spot data collection guide.
* \[ ] Dataset quality requirements.
* \[ ] Model validation requirements.
* \[ ] Paper replay requirements.
* \[ ] Testnet promotion requirements.
* \[ ] Why live remains locked.
* \[ ] Evidence export.

\---

## 28\. Codex bouwvolgorde

### PR 1 - Safety Contract + Demo Session Targets

* \[ ] `docs/live-training/demo-to-live-training-safety-contract.md`
* \[ ] `live\_training/demo\_session\_targets.py`
* \[ ] target progress tests.
* \[ ] no-live/no-secret tests.

### PR 2 - Demo Recorder Hardening + Vault

* \[ ] recorder event hash chain.
* \[ ] `demo\_dataset\_vault.py`
* \[ ] vault ingest/verify tests.

### PR 3 - Dataset Quality Burn-Down + Quality Gate v2

* \[ ] `dataset\_quality\_burndown.py`
* \[ ] `demo\_dataset\_quality\_v2.py`
* \[ ] quality grade tests.

### PR 4 - Feature/Label Dataset + Split Governance

* \[ ] `feature\_label\_dataset.py`
* \[ ] `split\_governance.py`
* \[ ] leakage/split tests.

### PR 5 - Model Candidate Registry + Validation Runner

* \[ ] `model\_candidate\_registry.py`
* \[ ] `model\_strategy\_validation.py`
* \[ ] validation grade tests.

### PR 6 - Paper Replay from Demo

* \[ ] `paper\_replay\_from\_demo.py`
* \[ ] paper-only replay tests.

### PR 7 - Testnet Promotion + Testnet Rehearsal

* \[ ] `testnet\_promotion\_gate.py`
* \[ ] `testnet\_rehearsal\_runner.py`
* \[ ] fake adapter tests.

### PR 8 - Live Candidate Gate + Evidence

* \[ ] `live\_candidate\_gate.py`
* \[ ] `demo\_to\_live\_evidence.py`
* \[ ] live remains locked tests.

### PR 9 - API + Dashboard Live-Training Page

* \[ ] live-training API routes.
* \[ ] `/live-training` Dashboard V2 page.
* \[ ] Control Center integration.
* \[ ] browser smoke.

### PR 10 - CLI + Check-All + Docs + UAT + Integrations

* \[ ] CLI commands.
* \[ ] check-all integration.
* \[ ] docs.
* \[ ] UAT scenarios.
* \[ ] release/knowledge/test/performance integration.
* \[ ] scheduled reports.

\---

## 29\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 117 PR 1: Demo-to-Live Training Safety Contract + Demo Session Target Plan.

Maak docs/live-training/demo-to-live-training-safety-contract.md.

Maak src/binance\_spot\_bot/live\_training/demo\_session\_targets.py met:
- DemoSessionTarget
- DemoSessionTargetProgress
- DemoSessionTargetReport
- default\_demo\_session\_target()
- calculate\_demo\_session\_target\_progress(target: DemoSessionTarget, session\_summaries: list\[dict])
- demo\_session\_target\_report\_to\_dict(...)
- write\_demo\_session\_target\_report(...)

Target metrics:
- minimum\_demo\_sessions
- minimum\_total\_runtime\_minutes
- minimum\_candles
- minimum\_signals
- minimum\_allow\_risk\_decisions
- minimum\_block\_risk\_decisions
- minimum\_order\_previews
- minimum\_test\_orders
- minimum\_demo\_orders
- minimum\_fills
- minimum\_rejections\_or\_cancellations
- minimum\_spread\_samples
- minimum\_latency\_samples
- minimum\_reconciliation\_runs
- required\_market\_regimes

Report moet bevatten:
- live\_trading\_enabled=False
- live\_execution\_enabled=False
- no\_live\_statement
- public\_or\_demo\_data\_only\_statement
- not\_financial\_advice\_statement
- progress\_percent
- missing\_targets
- blockers
- warnings
- next\_recommended\_collection\_steps

Gedrag:
- werkt op fixture session summaries
- ontbrekende velden worden warnings, geen crash
- raw secrets worden geredact
- live events in session summaries worden blocker
- report zegt nooit buy/sell/profit guaranteed
- geen command execution
- geen API calls
- geen runtime execution
- geen frontend execution
- geen signed endpoints
- geen account/order endpoints
- geen live trading

Voeg tests toe voor:
- empty sessions produce missing targets
- complete sessions pass
- partial sessions produce progress and missing targets
- live event contamination blocks
- missing fields create warnings
- secret-like values worden geredact
- JSON serialization
- live\_trading\_enabled=False
- live\_execution\_enabled=False
- no\_live\_statement aanwezig
- not\_financial\_advice\_statement aanwezig
```

Waarom eerst:

* Jij wilt dat live getraind wordt op goede demo spot data.
* Daarom moet eerst duidelijk zijn hoeveel demo data “genoeg” is.
* Dit raakt nog geen trading/runtime/frontend.
* Het is klein genoeg voor Codex.
* Daarna kunnen recorder, vault, dataset quality en model validation hierop bouwen.

\---

## 30\. Definition of Done

Roadmap 117 is klaar als:

* \[ ] Demo-to-Live Training Safety Contract bestaat.
* \[ ] Demo Session Target Plan werkt.
* \[ ] Demo Spot Recording Hardening werkt.
* \[ ] Demo Dataset Vault werkt.
* \[ ] Dataset Quality Burn-Down Board werkt.
* \[ ] Demo Dataset Quality Gate v2 werkt.
* \[ ] Feature/Label Dataset Builder v2 werkt.
* \[ ] Train/Validation/Test Split Governance werkt.
* \[ ] Model Candidate Registry werkt.
* \[ ] Model/Strategy Validation Runner werkt.
* \[ ] Paper Replay From Demo Dataset werkt.
* \[ ] Demo-to-Testnet Promotion Gate werkt.
* \[ ] Testnet Rehearsal Runner werkt.
* \[ ] Testnet-to-Live Readiness Candidate Gate werkt.
* \[ ] Live Training Dashboard werkt.
* \[ ] Control Center Live-Training Integration werkt.
* \[ ] API routes werken.
* \[ ] CLI commands werken.
* \[ ] Check-All Integration werkt.
* \[ ] UAT/Operator workflow werkt.
* \[ ] Evidence Bundle werkt.
* \[ ] Release/Knowledge/Test/Performance integration werkt.
* \[ ] Scheduled Demo-to-Live Reports werken.
* \[ ] Tests bewijzen live orders blijven geblokkeerd.
* \[ ] Tests bewijzen live candidate gate zonder evidence blokkeert.
* \[ ] Tests bewijzen datasets/evidence secret-free zijn.
* \[ ] Tests bewijzen low-quality demo data testnet/live blokkeert.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Roadmap 117 kan na uitvoering naar `Voltooid docs`.

\---

## 31\. Verwachte Roadmap 118 daarna

Als Roadmap 117 groen is en er genoeg demo/testnet evidence bestaat:

```text
Roadmap 118 - Live Trading Dry-Run, Order Preview, Read-Only Account Verification \& Minimal Real-Order Safety Layer
```

Mogelijke inhoud:

* \[ ] live dry-run mode;
* \[ ] read-only live account checks;
* \[ ] live order preview;
* \[ ] tiny capped first order gate;
* \[ ] live kill-switch drills;
* \[ ] cancel/emergency stop;
* \[ ] live audit/evidence;
* \[ ] no unattended live.

```

Als Roadmap 117 onvoldoende data vindt:

```text
Roadmap 118 - Demo Spot Data Collection Burn-Down Sprint, More Market Regime Coverage \& Validation Dataset Improvement
```

Mogelijke inhoud:

* \[ ] meer demo sessions;
* \[ ] meer fills/rejections;
* \[ ] meer volatile/high-spread scenarios;
* \[ ] dataset quality P0/P1 burn-down;
* \[ ] model validation opnieuw draaien;
* \[ ] live blijft locked.

```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Demo spot data collection validation and testnet promotion gate.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.

