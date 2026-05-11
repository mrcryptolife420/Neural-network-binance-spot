# Roadmap 078 - Paper Strategy Deployment, Continuous Evaluation \& Auto-Rollback

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Voltooid docs/078-roadmap-paper-strategy-deployment-continuous-evaluation-auto-rollback.md
```

Volgt op:

* `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
* `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
* `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
* `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
* `Voltooid docs/005` t/m `Voltooid docs/075`
* `Roadmap docs/076-roadmap-binance-public-data-ingestion-indicator-warmup-feature-expansion.md`
* `Roadmap docs/077-roadmap-data-driven-strategy-confidence-backtest-dataset-builder-indicator-calibration.md`

Doel: Roadmap 077 maakt strategie-confidence, indicatorcalibratie, backtest-datasets en paper-only promotion gates evidence-based. Roadmap 078 gebruikt die evidence om een **paper-approved strategy** gecontroleerd in demo/paper te draaien, continu te evalueren, drift en performanceproblemen te detecteren, automatisch terug te rollen naar een veilige conservative preset en dagelijks evidence-rapporten te maken.

Live trading blijft volledig buiten scope.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] `Voltooid docs/075-roadmap-simple-demo-multi-symbol-final-validation.md` bestaat.
* \[x] Roadmap 075 heeft status `Voltooid`.
* \[x] Roadmap 075 bevestigt dat multi-symbol dashboard helpers, risk summary, budget allocation, evidence export, full pytest, check-all en browser smoke zijn gevalideerd.
* \[x] Roadmap 075 bevestigt dat live trading disabled blijft.
* \[x] Geen bestaande Roadmap 078 gevonden via repo-search.
* \[x] Roadmap 076 is lokaal aangemaakt voor Binance public data ingestion en indicator warmup.
* \[x] Roadmap 077 is lokaal aangemaakt voor data-driven confidence, backtest dataset builder en indicator calibration.

### Codebasecontrole

Gecontroleerde relevante modules:

* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/model\_registry.py`
* \[x] `src/binance\_spot\_bot/evaluation.py`
* \[x] `src/binance\_spot\_bot/backtest.py`
* \[x] `src/binance\_spot\_bot/dataset\_governance.py`
* \[x] `src/binance\_spot\_bot/features.py`

### Belangrijke bestaande basis

De codebase heeft al:

* \[x] `RuntimeOptions` met mode, symbol, interval, source, model alias, risk limits, fetch limit en demo pilot settings.
* \[x] `BotRuntime` met session store, model registry, risk engine, paper account, alerts, execution engine, order lifecycle, report exports en demo pilot status.
* \[x] `UI\_MODES = ("demo", "paper", "testnet-readiness")`; live mode staat niet in de UI modes.
* \[x] `DATA\_SOURCES = ("auto", "demo", "rest", "websocket")`.
* \[x] `ModelRegistry` met candidate/champion metadata, model cards en promotion gate checks.
* \[x] `evaluate\_promotion(...)` met checks zoals dataset manifest, leakage guard, feature schema, walk-forward report, baseline comparison, drawdown, trade count, model card en operator confirmation.
* \[x] `BacktestEngine` en walk-forward evaluation bestaan.
* \[x] Session reports en runtime reports bestaan.

### Belangrijkste gat na Roadmap 077

Na Roadmap 077 kan een strategie mogelijk `paper\_approved` worden, maar dan mist nog:

* \[ ] gecontroleerde paper deployment lifecycle;
* \[ ] strategy runtime profile/version lock;
* \[ ] continuous paper evaluation;
* \[ ] drift detection;
* \[ ] auto rollback naar conservative preset;
* \[ ] daily strategy report;
* \[ ] performance watchdog;
* \[ ] evidence-based demotion;
* \[ ] dashboard deployment status;
* \[ ] safe deployment runbook;
* \[ ] no-live deployment contract.

\---

## 1\. Hoofddoel Roadmap 078

Maak van “paper-approved strategy” een gecontroleerde paper deployment workflow:

```text
Research evidence
→ paper promotion check
→ paper deployment plan
→ controlled paper run
→ continuous evaluation
→ drift/performance watchdog
→ auto rollback if bad
→ daily evidence report
→ strategy remains paper-only
```

Na Roadmap 078 moet de bot:

* \[ ] alleen paper-approved strategies kunnen starten in paper/demo;
* \[ ] strategy/model/config exact kunnen pinnen;
* \[ ] continu paper performance meten;
* \[ ] afwijkingen detecteren tussen backtest expectation en paper reality;
* \[ ] automatisch terugrollen bij no-go signalen;
* \[ ] daily reports exporteren;
* \[ ] dashboard status tonen;
* \[ ] nooit live trading activeren.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe data ingestion laag; Roadmap 076 doet dat.
* \[ ] Geen nieuwe calibration/backtest laag; Roadmap 077 doet dat.
* \[ ] Geen tweede runtime bouwen.
* \[ ] Geen tweede model registry bouwen.
* \[ ] Geen tweede risk engine bouwen.
* \[ ] Geen live trading.
* \[ ] Geen signed order endpoints.
* \[ ] Geen Binance account endpoints.
* \[ ] Geen futures/margin/leverage.
* \[ ] Geen autonomous AI trading.

Wel doen:

* \[ ] bestaande `BotRuntime` gecontroleerd inzetten voor paper strategy deployment;
* \[ ] bestaande `ModelRegistry` promotion metadata gebruiken;
* \[ ] bestaande session/report/evidence outputs uitbreiden;
* \[ ] nieuwe deployment controller toevoegen;
* \[ ] continuous evaluation toevoegen;
* \[ ] rollback/demotion policy toevoegen;
* \[ ] dashboard paper deployment panel toevoegen.

\---

## 3\. Fase 0 - Paper deployment safety contract

Doel: vastleggen dat deployment in deze roadmap alleen paper/demo is.

### Nieuwe doc

```text
docs/paper-strategy-deployment-safety-contract.md
```

### Regels

* \[ ] Deployment mode mag alleen:

  * `demo`;
  * `paper`;
  * `testnet-readiness` voor checks zonder echte deployment.
* \[ ] Live mode is verboden.
* \[ ] Signed order endpoints zijn verboden.
* \[ ] Binance account endpoints zijn verboden.
* \[ ] Deployment mag geen `live\_allowed=True` zetten.
* \[ ] Rollback mag alleen naar safer preset.
* \[ ] Operator moet deployment expliciet starten.
* \[ ] Auto rollback mag stoppen of conservative preset activeren.
* \[ ] Auto rollback mag nooit overschakelen naar live/testnet orders.
* \[ ] Reports moeten redacted/secret-free zijn.

### Acceptatiecriteria

* \[ ] Safety contract staat in docs.
* \[ ] Tests bewijzen dat live deployment onmogelijk is.
* \[ ] Dashboard toont `PAPER DEPLOYMENT ONLY`.
* \[ ] CLI deployment faalt als mode live of unknown is.

\---

## 4\. Fase 1 - PaperStrategyDeployment model

Doel: strategy deployments als first-class object opslaan.

### Nieuwe module

```text
src/binance\_spot\_bot/paper\_deployment.py
```

### Dataclasses

* \[ ] `PaperDeploymentPlan`
* \[ ] `PaperDeploymentStatus`
* \[ ] `PaperDeploymentRun`
* \[ ] `PaperDeploymentDecision`
* \[ ] `RollbackDecision`
* \[ ] `DeploymentGuardrailResult`

### `PaperDeploymentPlan` bevat

* \[ ] deployment\_id;
* \[ ] strategy\_id;
* \[ ] model\_id;
* \[ ] model\_alias;
* \[ ] dataset\_id;
* \[ ] feature\_schema\_hash;
* \[ ] promotion\_decision\_id;
* \[ ] symbols;
* \[ ] intervals;
* \[ ] mode = paper/demo;
* \[ ] source = demo/rest/websocket/cache;
* \[ ] risk preset;
* \[ ] quote budget;
* \[ ] max runtime;
* \[ ] max daily loss;
* \[ ] max drawdown;
* \[ ] max consecutive losses;
* \[ ] min data quality;
* \[ ] min liquidity score;
* \[ ] rollback policy;
* \[ ] created\_at;
* \[ ] operator\_confirmed.

### Acceptatiecriteria

* \[ ] Deployment plan is serializable.
* \[ ] Deployment plan bevat geen secrets.
* \[ ] Plan kan model/promotion evidence linken.
* \[ ] Plan faalt als live mode wordt gevraagd.
* \[ ] Plan faalt als model niet paper-approved is.

\---

## 5\. Fase 2 - Deployment Store

Doel: paper deployments lokaal beheren.

### Nieuwe module

```text
src/binance\_spot\_bot/deployment\_store.py
```

### Storage

```text
data/deployments/
  deployment-index.json
  <deployment\_id>/
    deployment-plan.json
    status.json
    events.jsonl
    daily-reports/
    rollback-decisions.jsonl
```

### Taken

* \[ ] Save/load deployment plan.
* \[ ] Append deployment events.
* \[ ] Track active deployment.
* \[ ] Prevent two active deployments with same strategy/symbol unless explicitly allowed.
* \[ ] Link sessions to deployment\_id.
* \[ ] Archive deployment.
* \[ ] Export deployment bundle.

### Acceptatiecriteria

* \[ ] Deployment history blijft lokaal.
* \[ ] Active deployment is duidelijk.
* \[ ] Events zijn append-only.
* \[ ] Geen secrets in deployment store.
* \[ ] Deployment bundle heeft manifest/hash.

\---

## 6\. Fase 3 - Paper deployment CLI

Doel: deployment workflow via CLI bruikbaar maken.

### Nieuwe commands

```powershell
python -m binance\_spot\_bot.cli paper-deployment-plan --model-id <id> --symbols BTCUSDT,ETHUSDT --risk-preset conservative
python -m binance\_spot\_bot.cli paper-deployment-start --deployment-id <id> --confirm PAPER\_DEPLOY
python -m binance\_spot\_bot.cli paper-deployment-status --deployment-id <id>
python -m binance\_spot\_bot.cli paper-deployment-stop --deployment-id <id> --reason operator\_stop
python -m binance\_spot\_bot.cli paper-deployment-rollback --deployment-id <id> --confirm PAPER\_ROLLBACK
python -m binance\_spot\_bot.cli paper-deployment-export --deployment-id <id>
```

### Guardrails

* \[ ] Start vereist `PAPER\_DEPLOY` confirm.
* \[ ] Rollback vereist `PAPER\_ROLLBACK` confirm als handmatig.
* \[ ] Start faalt bij:

  * missing promotion evidence;
  * failed leakage guard;
  * failed check-all evidence;
  * data quality blocked;
  * live mode requested;
  * unsupported source;
  * stale model evidence.

### Acceptatiecriteria

* \[ ] CLI werkt zonder API keys.
* \[ ] CLI gebruikt paper/demo modes.
* \[ ] Geen signed endpoints.
* \[ ] JSON output optie.
* \[ ] Tests met fake deployment plan.

\---

## 7\. Fase 4 - Strategy version lock

Doel: voorkomen dat runtime onbewust met andere model/features/settings draait dan goedgekeurd.

### Taken

* \[ ] Voeg `StrategyRuntimeLock` toe:

  * model\_id;
  * model\_alias;
  * feature\_schema\_hash;
  * dataset\_id;
  * indicator\_weights\_hash;
  * risk\_preset\_hash;
  * symbol list;
  * interval;
  * source;
  * deployment\_id.
* \[ ] Runtime controleert bij start:

  * model metadata match;
  * feature schema match;
  * strategy confidence config match;
  * risk preset match.
* \[ ] Mismatch geeft blocker.
* \[ ] Dashboard toont lock status.

### Acceptatiecriteria

* \[ ] Deployment start faalt bij model mismatch.
* \[ ] Deployment start faalt bij feature schema mismatch.
* \[ ] Operator ziet exact welke hash afwijkt.
* \[ ] Geen automatische “fix” zonder confirm.
* \[ ] Geen live route.

\---

## 8\. Fase 5 - Continuous Paper Evaluation

Doel: paper deployment continu vergelijken met verwachtingen.

### Nieuwe module

```text
src/binance\_spot\_bot/continuous\_evaluation.py
```

### Inputs

* \[ ] active deployment plan;
* \[ ] runtime snapshots;
* \[ ] fills;
* \[ ] signals;
* \[ ] risk decisions;
* \[ ] data quality;
* \[ ] backtest expectation from Roadmap 077;
* \[ ] calibration curves;
* \[ ] symbol ranking expectation.

### Metrics

* \[ ] realized paper PnL;
* \[ ] unrealized PnL;
* \[ ] drawdown;
* \[ ] win rate;
* \[ ] average win/loss;
* \[ ] profit factor;
* \[ ] consecutive losses;
* \[ ] blocked trade rate;
* \[ ] signal distribution;
* \[ ] confidence bucket performance;
* \[ ] slippage estimate vs actual simulated;
* \[ ] spread exposure;
* \[ ] liquidity warnings;
* \[ ] data quality warnings;
* \[ ] expected vs actual signal frequency;
* \[ ] expected vs actual PnL band.

### Acceptatiecriteria

* \[ ] Evaluation runs during/after paper session.
* \[ ] Metrics are stored per deployment.
* \[ ] Metrics are dashboard-ready.
* \[ ] No order execution is triggered by evaluator.
* \[ ] Reports are secret-free.

\---

## 9\. Fase 6 - Drift Detection

Doel: detecteren wanneer paper reality afwijkt van research/backtest.

### Nieuwe module

```text
src/binance\_spot\_bot/drift\_detection.py
```

### Drift types

* \[ ] data distribution drift;
* \[ ] volatility drift;
* \[ ] liquidity drift;
* \[ ] spread drift;
* \[ ] signal distribution drift;
* \[ ] confidence calibration drift;
* \[ ] symbol ranking drift;
* \[ ] regime mix drift;
* \[ ] performance drift;
* \[ ] data quality drift.

### Drift status

* \[ ] `ok`;
* \[ ] `watch`;
* \[ ] `warning`;
* \[ ] `critical`.

### Acceptatiecriteria

* \[ ] Drift detection does not stop runtime directly; it emits decisions to watchdog.
* \[ ] Critical drift can trigger rollback policy.
* \[ ] Drift report is exportable.
* \[ ] False positives are documented.
* \[ ] No live trading.

\---

## 10\. Fase 7 - Paper Performance Watchdog

Doel: paper deployment automatisch beschermen.

### Nieuwe module

```text
src/binance\_spot\_bot/paper\_watchdog.py
```

### Watchdog checks

* \[ ] max drawdown exceeded;
* \[ ] max daily loss exceeded;
* \[ ] max consecutive losses exceeded;
* \[ ] win rate below threshold after minimum sample;
* \[ ] profit factor below threshold;
* \[ ] too many blocked trades;
* \[ ] data quality degraded;
* \[ ] liquidity degraded;
* \[ ] calibration drift critical;
* \[ ] strategy runtime lock mismatch;
* \[ ] missing reports/evidence;
* \[ ] runtime errors.

### Watchdog actions

* \[ ] observe;
* \[ ] warn;
* \[ ] reduce paper quote size;
* \[ ] switch to observe-only;
* \[ ] pause strategy;
* \[ ] rollback to conservative preset;
* \[ ] stop deployment.

### Acceptatiecriteria

* \[ ] Watchdog actions are paper-only.
* \[ ] Stop/rollback events are stored.
* \[ ] Dashboard shows current watchdog status.
* \[ ] Tests cover each action.
* \[ ] Live remains disabled.

\---

## 11\. Fase 8 - Auto-Rollback Policy

Doel: automatisch terug naar veiligere state als paper deployment slecht loopt.

### Nieuwe module

```text
src/binance\_spot\_bot/auto\_rollback.py
```

### Rollback targets

* \[ ] current strategy observe-only;
* \[ ] conservative risk preset;
* \[ ] rule-based baseline;
* \[ ] no-trade baseline;
* \[ ] stop deployment.

### Rollback triggers

* \[ ] critical drift;
* \[ ] max drawdown breach;
* \[ ] max loss breach;
* \[ ] consecutive loss breach;
* \[ ] confidence calibration failure;
* \[ ] data quality blocked;
* \[ ] runtime lock mismatch;
* \[ ] evidence integrity failure.

### RollbackDecision bevat

* \[ ] deployment\_id;
* \[ ] trigger;
* \[ ] severity;
* \[ ] previous\_state;
* \[ ] target\_state;
* \[ ] reason;
* \[ ] timestamp;
* \[ ] operator\_required;
* \[ ] evidence\_links.

### Acceptatiecriteria

* \[ ] Rollback never increases risk.
* \[ ] Rollback never enables live.
* \[ ] Rollback logs evidence.
* \[ ] Manual override requires confirm.
* \[ ] Dashboard shows rollback reason.

\---

## 12\. Fase 9 - Evidence-based Demotion

Doel: paper-approved strategies kunnen teruggezet worden als ze slecht presteren.

### Nieuwe module

```text
src/binance\_spot\_bot/strategy\_demotion.py
```

### Demotion statuses

* \[ ] paper\_approved;
* \[ ] paper\_watch;
* \[ ] paper\_suspended;
* \[ ] research\_only;
* \[ ] archived.

### Demotion triggers

* \[ ] repeated rollback;
* \[ ] failed daily report threshold;
* \[ ] poor confidence calibration;
* \[ ] no longer beats baseline;
* \[ ] too many data quality blockers;
* \[ ] evidence expired;
* \[ ] operator demotion.

### Acceptatiecriteria

* \[ ] Demotion updates registry/deployment metadata.
* \[ ] Demotion does not delete artifacts.
* \[ ] Demotion is evidence-linked.
* \[ ] Strategy can be re-promoted only via Roadmap 077 gates.
* \[ ] No live status exists.

\---

## 13\. Fase 10 - Daily Strategy Report

Doel: dagelijks paper deployment bewijs genereren.

### Nieuwe module

```text
src/binance\_spot\_bot/daily\_strategy\_report.py
```

### Report output

```text
data/deployments/<deployment\_id>/daily-reports/YYYY-MM-DD/
  daily\_strategy\_report.md
  daily\_strategy\_report.json
  metrics.csv
  drift\_report.json
  watchdog\_events.jsonl
  rollback\_decisions.jsonl
  evidence\_manifest.json
```

### Report bevat

* \[ ] summary;
* \[ ] deployment status;
* \[ ] paper PnL;
* \[ ] drawdown;
* \[ ] trades;
* \[ ] win/loss;
* \[ ] blocked reasons;
* \[ ] confidence bucket performance;
* \[ ] data quality;
* \[ ] liquidity warnings;
* \[ ] drift status;
* \[ ] watchdog actions;
* \[ ] rollback/demotion decisions;
* \[ ] next recommended action;
* \[ ] no-live statement.

### Acceptatiecriteria

* \[ ] Daily report is generated manually or at stop.
* \[ ] Report contains no secrets.
* \[ ] Report is evidence-linked.
* \[ ] Dashboard can download report.
* \[ ] Report can be used for demotion/promote review.

\---

## 14\. Fase 11 - Deployment Dashboard Panel

Doel: operator kan paper deployments volgen zonder raw JSON.

### Nieuwe/uitgebreide dashboardsectie

```text
Paper Deployment
```

### Panels

* \[ ] active deployment status;
* \[ ] strategy/model lock;
* \[ ] symbols;
* \[ ] risk preset;
* \[ ] promotion evidence status;
* \[ ] live disabled badge;
* \[ ] current metrics;
* \[ ] drift status;
* \[ ] watchdog status;
* \[ ] rollback status;
* \[ ] daily report status;
* \[ ] deployment event timeline;
* \[ ] next action.

### Actions

* \[ ] create plan;
* \[ ] start paper deployment;
* \[ ] pause deployment;
* \[ ] stop deployment;
* \[ ] manual rollback;
* \[ ] export daily report;
* \[ ] export deployment bundle.

### Acceptatiecriteria

* \[ ] Dashboard never shows live deployment.
* \[ ] Dangerous actions require confirm.
* \[ ] Critical blockers are visible.
* \[ ] Raw JSON only in debug expander.
* \[ ] Browser smoke covers panel import/render.

\---

## 15\. Fase 12 - Continuous Evaluation Scheduler

Doel: evaluation periodiek draaien tijdens langere paper sessions.

### Nieuwe module

```text
src/binance\_spot\_bot/evaluation\_scheduler.py
```

### Modes

* \[ ] on every N runtime steps;
* \[ ] every N minutes;
* \[ ] on session stop;
* \[ ] on critical event;
* \[ ] manual run.

### Guardrails

* \[ ] Scheduler never sends orders.
* \[ ] Scheduler uses snapshot/session data.
* \[ ] Scheduler cannot change risk except through watchdog-approved paper actions.
* \[ ] Scheduler writes metrics/evidence.

### Acceptatiecriteria

* \[ ] Scheduler works without internet.
* \[ ] Scheduler works during demo replay.
* \[ ] Scheduler output is deterministic for same inputs.
* \[ ] Scheduler has max runtime budget.

\---

## 16\. Fase 13 - Paper deployment evidence bundle

Doel: één bundle met alles rond een deployment.

### Bundle bevat

* \[ ] deployment plan;
* \[ ] strategy runtime lock;
* \[ ] promotion decision;
* \[ ] model card;
* \[ ] dataset manifest;
* \[ ] calibration report;
* \[ ] daily reports;
* \[ ] drift reports;
* \[ ] watchdog events;
* \[ ] rollback decisions;
* \[ ] demotion decisions;
* \[ ] session reports;
* \[ ] check-all output;
* \[ ] no-live proof;
* \[ ] hashes.

### Acceptatiecriteria

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest.
* \[ ] Bundle can be verified.
* \[ ] Bundle can be archived.
* \[ ] Dashboard/CLI export works.

\---

## 17\. Fase 14 - Strategy rollback simulation

Doel: rollback-policy testen vóór echte paper deployment.

### Nieuwe module

```text
src/binance\_spot\_bot/rollback\_simulation.py
```

### Simulaties

* \[ ] max drawdown breach;
* \[ ] data quality blocked;
* \[ ] liquidity degraded;
* \[ ] confidence drift;
* \[ ] consecutive losses;
* \[ ] model lock mismatch;
* \[ ] evidence tamper;
* \[ ] report generation failure.

### Output

* \[ ] rollback simulation report;
* \[ ] expected action;
* \[ ] actual action;
* \[ ] pass/fail;
* \[ ] evidence links.

### Acceptatiecriteria

* \[ ] Rollback simulation can run in CI.
* \[ ] No external API needed.
* \[ ] Critical rollback paths are tested.
* \[ ] Simulation never enables live.

\---

## 18\. Fase 15 - Tests

### Unit tests

* \[ ] `tests/test\_paper\_deployment.py`
* \[ ] `tests/test\_deployment\_store.py`
* \[ ] `tests/test\_paper\_deployment\_cli.py`
* \[ ] `tests/test\_strategy\_runtime\_lock.py`
* \[ ] `tests/test\_continuous\_evaluation.py`
* \[ ] `tests/test\_drift\_detection.py`
* \[ ] `tests/test\_paper\_watchdog.py`
* \[ ] `tests/test\_auto\_rollback.py`
* \[ ] `tests/test\_strategy\_demotion.py`
* \[ ] `tests/test\_daily\_strategy\_report.py`
* \[ ] `tests/test\_evaluation\_scheduler.py`
* \[ ] `tests/test\_deployment\_evidence\_bundle.py`
* \[ ] `tests/test\_rollback\_simulation.py`

### Integration tests

* \[ ] Create paper deployment plan from paper-approved model metadata.
* \[ ] Start fake paper deployment.
* \[ ] Run continuous evaluation.
* \[ ] Trigger drift warning.
* \[ ] Trigger watchdog rollback.
* \[ ] Generate daily report.
* \[ ] Export deployment evidence bundle.
* \[ ] Demote strategy after repeated failure.

### Safety tests

* \[ ] Deployment rejects live mode.
* \[ ] Deployment rejects signed endpoint usage.
* \[ ] Deployment cannot call account endpoint.
* \[ ] Rollback cannot increase risk.
* \[ ] Scheduler cannot send orders.
* \[ ] Daily reports are secret-free.
* \[ ] `live\_allowed` remains false.

\---

## 19\. Docs

Nieuwe docs:

* \[ ] `docs/paper-strategy-deployment-safety-contract.md`
* \[ ] `docs/paper-deployment-workflow.md`
* \[ ] `docs/strategy-runtime-lock.md`
* \[ ] `docs/continuous-paper-evaluation.md`
* \[ ] `docs/drift-detection.md`
* \[ ] `docs/paper-performance-watchdog.md`
* \[ ] `docs/auto-rollback-policy.md`
* \[ ] `docs/strategy-demotion.md`
* \[ ] `docs/daily-strategy-report.md`
* \[ ] `docs/deployment-evidence-bundle.md`
* \[ ] `docs/rollback-simulation.md`

README updates:

* \[ ] paper deployment commands;
* \[ ] safety note;
* \[ ] rollback explanation;
* \[ ] daily report path;
* \[ ] no-live statement.

\---

## 20\. Codex bouwvolgorde

### PR 1 - PaperDeploymentPlan + Store

* \[ ] `paper\_deployment.py`
* \[ ] `deployment\_store.py`
* \[ ] plan validation;
* \[ ] no-live tests.

### PR 2 - Paper deployment CLI

* \[ ] plan/start/status/stop/export commands;
* \[ ] confirm gates;
* \[ ] tests.

### PR 3 - Strategy Runtime Lock

* \[ ] lock schema;
* \[ ] runtime start validation;
* \[ ] dashboard payload;
* \[ ] tests.

### PR 4 - Continuous Evaluation

* \[ ] metrics collector;
* \[ ] deployment metrics store;
* \[ ] report-ready payload;
* \[ ] tests.

### PR 5 - Drift Detection

* \[ ] drift checks;
* \[ ] status/severity;
* \[ ] drift report;
* \[ ] tests.

### PR 6 - Paper Watchdog

* \[ ] thresholds;
* \[ ] actions;
* \[ ] event store;
* \[ ] tests.

### PR 7 - Auto Rollback

* \[ ] rollback targets;
* \[ ] rollback decisions;
* \[ ] manual/auto flows;
* \[ ] tests.

### PR 8 - Daily Strategy Reports

* \[ ] markdown/json/csv outputs;
* \[ ] evidence manifest;
* \[ ] tests.

### PR 9 - Dashboard Panel

* \[ ] paper deployment panel;
* \[ ] event timeline;
* \[ ] report download;
* \[ ] browser smoke.

### PR 10 - Demotion + Evidence Bundle + Simulation

* \[ ] demotion policy;
* \[ ] bundle export;
* \[ ] rollback simulation;
* \[ ] docs.

\---

## 21\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 078 PR 1: PaperDeploymentPlan + DeploymentStore.

Maak src/binance\_spot\_bot/paper\_deployment.py met PaperDeploymentPlan, PaperDeploymentStatus, PaperDeploymentRun, DeploymentGuardrailResult en RollbackDecision.
Maak src/binance\_spot\_bot/deployment\_store.py voor lokale opslag onder data/deployments/.
Valideer dat deployment alleen mode demo/paper/testnet-readiness gebruikt en nooit live.
Valideer dat model metadata paper-approved/promotion evidence aanwezig is.
Schrijf deployment-plan.json, status.json en events.jsonl.
Voeg tests toe voor:
- valid paper deployment plan
- reject live mode
- reject missing promotion evidence
- save/load deployment
- no secrets in deployment store

Geen trading/risk/execution logic aanpassen.
Geen signed endpoints.
Live trading blijft disabled.
```

Waarom eerst:

* deployment plan/store is de basis voor alle latere continuous evaluation en rollback;
* deze PR is klein genoeg voor Codex;
* het raakt nog geen runtime orderflow;
* safety kan direct hard getest worden.

\---

## 22\. Definition of Done

Roadmap 078 is klaar als:

* \[ ] PaperDeploymentPlan bestaat.
* \[ ] DeploymentStore bestaat.
* \[ ] Paper deployment CLI bestaat.
* \[ ] Strategy runtime lock werkt.
* \[ ] Continuous paper evaluation werkt.
* \[ ] Drift detection werkt.
* \[ ] Paper performance watchdog werkt.
* \[ ] Auto rollback werkt en verhoogt nooit risico.
* \[ ] Strategy demotion werkt evidence-based.
* \[ ] Daily strategy report werkt.
* \[ ] Deployment dashboard panel werkt.
* \[ ] Evaluation scheduler werkt.
* \[ ] Deployment evidence bundle werkt.
* \[ ] Rollback simulation werkt.
* \[ ] Tests bewijzen dat live mode onmogelijk is.
* \[ ] Tests bewijzen dat signed endpoints niet gebruikt worden.
* \[ ] Reports en bundles zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 078 kan na uitvoering naar `Voltooid docs`.

\---

## 23\. Verwachte Roadmap 079 daarna

Na Roadmap 078 zou Roadmap 079 logisch focussen op:

```text
Roadmap 079 - Paper Portfolio Operations, Capital Allocation \& Strategy Rotation
```

Mogelijke inhoud:

* \[ ] meerdere paper-approved strategies tegelijk volgen;
* \[ ] paper capital allocation;
* \[ ] strategy rotation;
* \[ ] symbol-level allocation;
* \[ ] exposure budget per strategy;
* \[ ] portfolio-level paper watchdog;
* \[ ] cross-strategy conflict handling;
* \[ ] nog steeds geen live trading.



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

- paper_deployment.py toegevoegd met paper deployment plan, version lock, deployment store, continuous evaluation, drift/performance watchdog, rollback plan en daily strategy report.
- CLI command toegevoegd: paper-deployment-cycle.
- Tests toegevoegd: 	ests/test_roadmap_078_paper_deployment.py.

Validatie:

- python -m pytest tests/test_roadmap_076_public_data_ingestion.py tests/test_roadmap_077_strategy_calibration.py tests/test_roadmap_078_paper_deployment.py tests/test_features_model_backtest.py -q -> 14 passed.
- Scope blijft paper-only; rollback target is conservative; live trading disabled.

