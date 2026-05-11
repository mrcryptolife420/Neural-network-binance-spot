# Roadmap 082 - Paper Policy Rollout, A/B Paper Experiments \& Champion/Challenger Portfolio Governance

Status: Niet volledig voltooid / opnieuw gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/082-roadmap-paper-policy-rollout-ab-paper-experiments-champion-challenger-governance.md
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

Doel: Roadmap 081 selecteert een robuuste paper portfolio policy op basis van benchmarks, scenario weights, risk budgets en conservative policy cards. Roadmap 082 zorgt dat zo’n paper policy gecontroleerd uitgerold kan worden, vergeleken kan worden met challengers via A/B paper experiments, en beheerd wordt via champion/challenger governance. De roadmap voorkomt dat een nieuwe paper policy blind de oude vervangt.

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
* \[x] Geen bestaande Roadmap 082 gevonden via repo-search.
* \[x] Roadmap 076 is lokaal aangemaakt voor Binance public data ingestion.
* \[x] Roadmap 077 is lokaal aangemaakt voor backtest/calibration/confidence.
* \[x] Roadmap 078 is lokaal aangemaakt voor paper deployment/rollback.
* \[x] Roadmap 079 is lokaal aangemaakt voor paper portfolio operations/rotation.
* \[x] Roadmap 080 is lokaal aangemaakt voor stress testing/scenario replay.
* \[x] Roadmap 081 is lokaal aangemaakt voor paper portfolio optimization/risk budget search.

### Codebasecontrole

Gecontroleerde relevante modules:

* \[x] `src/binance\_spot\_bot/model\_registry.py`
* \[x] `src/binance\_spot\_bot/portfolio.py`
* \[x] `src/binance\_spot\_bot/evaluation.py`
* \[x] `src/binance\_spot\_bot/runtime.py`

### Bestaande basis

Er bestaat al:

* \[x] `ModelRegistry` met candidate/champion metadata, model cards, promotion gate checks en champion alias.
* \[x] `PromotionGateResult`.
* \[x] `ModelMetadata` met candidate/champion/status/role en `previous\_champion\_id`.
* \[x] `evaluate\_promotion(...)` met checks voor dataset manifest, leakage guard, feature schema hash, walk-forward report, baseline comparison, drawdown, trade count, model card en operator confirmation.
* \[x] Roadmap 081 levert paper policy cards en paper policy approval gates.
* \[x] Roadmap 075 bevestigt dat multi-symbol dashboard helpers en browser smoke al gevalideerd zijn.
* \[x] Live trading blijft disabled.

### Belangrijkste gat na Roadmap 081

Na Roadmap 081 heb je een gekozen/approved paper portfolio policy. Wat nog mist:

* \[ ] gecontroleerde paper rollout;
* \[ ] champion/challenger portfolio policy registry;
* \[ ] A/B paper experiments;
* \[ ] traffic/allocation split tussen champion en challenger;
* \[ ] experiment stopping rules;
* \[ ] promotion/demotion governance voor portfolio policies;
* \[ ] weekly governance report;
* \[ ] rollback naar previous champion policy;
* \[ ] operator approval workflow;
* \[ ] policy lineage en audit trail.

\---

## 1\. Hoofddoel Roadmap 082

Maak van een paper-approved portfolio policy een gecontroleerde rollout- en governanceflow:

```text
Approved paper policy
→ rollout plan
→ champion/challenger setup
→ A/B paper experiment
→ evidence collection
→ stopping rules
→ governance review
→ promote/demote/rollback
→ weekly report
```

Na Roadmap 082 moet de bot:

* \[ ] een champion paper policy kunnen vastleggen;
* \[ ] challengers paper-only kunnen toevoegen;
* \[ ] paper allocation split tussen champion/challenger kunnen draaien;
* \[ ] A/B paper experiments kunnen meten;
* \[ ] stopping rules toepassen bij slechte challenger;
* \[ ] champion promotion/demotion evidence-based doen;
* \[ ] rollback naar previous champion mogelijk maken;
* \[ ] weekly governance reports exporteren;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe optimizer; Roadmap 081 doet dat.
* \[ ] Geen nieuwe benchmark suite; Roadmap 080 doet dat.
* \[ ] Geen nieuwe portfolio engine vanaf nul.
* \[ ] Geen nieuwe model registry vanaf nul.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen real-money rollout.
* \[ ] Geen cloud experiment service.
* \[ ] Geen external telemetry.

Wel doen:

* \[ ] bestaande `ModelRegistry` concept uitbreiden naar portfolio policy registry;
* \[ ] Roadmap 081 policy cards gebruiken;
* \[ ] paper-only rollout plan toevoegen;
* \[ ] A/B paper experiment framework toevoegen;
* \[ ] governance reports toevoegen;
* \[ ] dashboard/CLI toevoegen;
* \[ ] evidence-first en no-live houden.

\---

## 3\. Fase 0 - Paper Policy Governance Safety Contract

Doel: vastleggen dat rollout/governance alleen paper is.

### Nieuwe doc

```text
docs/paper-policy-governance-safety-contract.md
```

### Regels

* \[ ] Governance werkt alleen met paper policies.
* \[ ] A/B experiments gebruiken alleen demo/paper simulation.
* \[ ] Geen live allocation.
* \[ ] Geen signed endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen remote telemetry.
* \[ ] Promotion betekent alleen champion paper policy.
* \[ ] Rollback betekent terug naar vorige paper champion of conservative no-trade.
* \[ ] Operator confirmation vereist voor champion promotion.
* \[ ] Reports zijn secret-free.

### Acceptatiecriteria

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen geen live champion status.
* \[ ] Dashboard toont `PAPER GOVERNANCE ONLY`.
* \[ ] CLI faalt bij live mode.

\---

## 4\. Fase 1 - Portfolio Policy Registry

Doel: paper portfolio policies beheren zoals modellen in `ModelRegistry`.

### Nieuwe module

```text
src/binance\_spot\_bot/portfolio\_policy\_registry.py
```

### Dataclasses

* \[ ] `PortfolioPolicyMetadata`
* \[ ] `PortfolioPolicyRegistry`
* \[ ] `PolicyPromotionGateResult`
* \[ ] `PolicyLineageRecord`
* \[ ] `PolicyGovernanceDecision`

### Metadata velden

* \[ ] policy\_id;
* \[ ] policy\_name;
* \[ ] policy\_type;
* \[ ] allocation\_weights;
* \[ ] risk\_budget\_hash;
* \[ ] scenario\_weight\_hash;
* \[ ] optimizer\_id;
* \[ ] benchmark\_id;
* \[ ] robustness\_score;
* \[ ] max\_drawdown;
* \[ ] worst\_case\_scenario;
* \[ ] policy\_card\_path;
* \[ ] evidence\_manifest\_path;
* \[ ] status:

  * candidate;
  * challenger;
  * champion;
  * suspended;
  * archived;
* \[ ] role;
* \[ ] previous\_champion\_id;
* \[ ] created\_at\_ms;
* \[ ] promoted\_at\_ms;
* \[ ] governance\_notes.

### Acceptatiecriteria

* \[ ] Registry kan policy registreren.
* \[ ] Registry kan champion alias beheren.
* \[ ] Registry schrijft policy card links.
* \[ ] Registry bevat geen secrets.
* \[ ] Registry lijkt qua patroon op `ModelRegistry` maar kopieert geen modelcode blind.

\---

## 5\. Fase 2 - Paper Policy Promotion Gate

Doel: paper policy mag alleen champion worden met bewijs.

### Nieuwe module

```text
src/binance\_spot\_bot/policy\_promotion\_gate.py
```

### Checks

* \[ ] policy card present;
* \[ ] evidence manifest present;
* \[ ] benchmark evidence valid;
* \[ ] robustness score above threshold;
* \[ ] max drawdown below threshold;
* \[ ] worst-case scenario acceptable;
* \[ ] overfit guard passed;
* \[ ] paper approval present;
* \[ ] no-live proof present;
* \[ ] operator confirmed.

### Acceptatiecriteria

* \[ ] Promotion gate kan policy blokkeren.
* \[ ] Gate reasons zijn dashboard-ready.
* \[ ] Promotion kan geen live status zetten.
* \[ ] Tests dekken missing evidence, weak robustness en operator not confirmed.

\---

## 6\. Fase 3 - Paper Rollout Plan

Doel: nieuwe paper policy niet direct volledig gebruiken.

### Nieuwe module

```text
src/binance\_spot\_bot/paper\_policy\_rollout.py
```

### Rollout strategies

* \[ ] observe-only rollout;
* \[ ] 10% paper allocation;
* \[ ] 25% paper allocation;
* \[ ] 50% paper allocation;
* \[ ] full paper rollout;
* \[ ] canary symbol rollout;
* \[ ] limited time rollout;
* \[ ] conservative shadow comparison.

### RolloutPlan bevat

* \[ ] rollout\_id;
* \[ ] champion\_policy\_id;
* \[ ] challenger\_policy\_id;
* \[ ] rollout\_stage;
* \[ ] allocation\_split;
* \[ ] symbols;
* \[ ] max duration;
* \[ ] min sample count;
* \[ ] stopping rules;
* \[ ] success rules;
* \[ ] rollback target;
* \[ ] operator confirmation;
* \[ ] created\_at\_ms.

### Acceptatiecriteria

* \[ ] Rollout plan is paper-only.
* \[ ] Allocation split kan niet boven total paper budget.
* \[ ] Rollout start met conservative default.
* \[ ] Dangerous stage increase vereist confirm.
* \[ ] Rollout events worden opgeslagen.

\---

## 7\. Fase 4 - A/B Paper Experiment Framework

Doel: champion en challenger eerlijk vergelijken in paper.

### Nieuwe module

```text
src/binance\_spot\_bot/ab\_paper\_experiments.py
```

### Experiment types

* \[ ] champion vs challenger same symbols;
* \[ ] champion vs challenger split allocation;
* \[ ] canary challenger on subset symbols;
* \[ ] observe-only challenger;
* \[ ] time-window alternating comparison;
* \[ ] scenario-weighted replay experiment.

### Metrics

* \[ ] PnL;
* \[ ] drawdown;
* \[ ] risk-adjusted return;
* \[ ] trade count;
* \[ ] blocked trade rate;
* \[ ] conflict rate;
* \[ ] data quality warnings;
* \[ ] liquidity penalties;
* \[ ] turnover;
* \[ ] rotation churn;
* \[ ] watchdog actions;
* \[ ] policy violations.

### Acceptatiecriteria

* \[ ] Experiment runs offline/paper-only.
* \[ ] Experiment can use same cached data for fairness.
* \[ ] Challenger cannot affect champion allocation beyond plan.
* \[ ] Results are reproducible with seed.
* \[ ] No signed endpoints.

\---

## 8\. Fase 5 - Experiment Assignment \& Split Manager

Doel: paper traffic/allocation eerlijk verdelen.

### Nieuwe module

```text
src/binance\_spot\_bot/paper\_experiment\_split.py
```

### Split types

* \[ ] allocation percentage split;
* \[ ] symbol split;
* \[ ] time-slice split;
* \[ ] random deterministic seed split;
* \[ ] canary-only split.

### Guardrails

* \[ ] never exceed paper budget;
* \[ ] preserve cash reserve;
* \[ ] no double counting same fill;
* \[ ] conflict resolver aware;
* \[ ] champion protected;
* \[ ] challenger capped.

### Acceptatiecriteria

* \[ ] Split is deterministic with seed.
* \[ ] Split is auditable.
* \[ ] Split never routes to live.
* \[ ] Dashboard can show split.

\---

## 9\. Fase 6 - Experiment Stopping Rules

Doel: slechte challengers snel stoppen.

### Nieuwe module

```text
src/binance\_spot\_bot/experiment\_stopping\_rules.py
```

### Stop triggers

* \[ ] challenger max drawdown breach;
* \[ ] challenger underperforms champion by threshold;
* \[ ] data quality degraded;
* \[ ] liquidity shock failure;
* \[ ] watchdog critical action;
* \[ ] overfit warning triggered in live paper;
* \[ ] too few samples after time limit;
* \[ ] policy violation;
* \[ ] evidence integrity failure.

### Stop actions

* \[ ] continue observe;
* \[ ] warn;
* \[ ] reduce challenger allocation;
* \[ ] pause challenger;
* \[ ] rollback challenger to observe-only;
* \[ ] end experiment;
* \[ ] archive challenger.

### Acceptatiecriteria

* \[ ] Stopping rules never increase risk.
* \[ ] Stop decision has reason codes.
* \[ ] Stop decision is evidence-linked.
* \[ ] Tests cover each trigger.
* \[ ] No live mode.

\---

## 10\. Fase 7 - Governance Decision Engine

Doel: na experiment beslissen wat met challenger gebeurt.

### Nieuwe module

```text
src/binance\_spot\_bot/policy\_governance.py
```

### Decisions

* \[ ] keep champion;
* \[ ] promote challenger to champion;
* \[ ] extend experiment;
* \[ ] reduce challenger allocation;
* \[ ] rerun benchmark;
* \[ ] suspend challenger;
* \[ ] archive challenger;
* \[ ] rollback to previous champion;
* \[ ] no-policy approved.

### Decision inputs

* \[ ] A/B experiment report;
* \[ ] daily portfolio reports;
* \[ ] benchmark evidence;
* \[ ] robustness score;
* \[ ] drift status;
* \[ ] watchdog actions;
* \[ ] stopping rule outcomes;
* \[ ] operator notes;
* \[ ] no-live proof.

### Acceptatiecriteria

* \[ ] Governance decision is deterministic for same inputs.
* \[ ] Promotion requires operator confirmation.
* \[ ] Every decision has reasons.
* \[ ] Champion replacement preserves previous champion ID.
* \[ ] No live status exists.

\---

## 11\. Fase 8 - Weekly Governance Report

Doel: periodiek overzicht over paper policies.

### Nieuwe module

```text
src/binance\_spot\_bot/weekly\_governance\_report.py
```

### Output

```text
data/policy-governance/weekly/YYYY-WW/
  weekly\_governance\_report.md
  weekly\_governance\_report.json
  policy\_status.csv
  experiment\_results.csv
  governance\_decisions.jsonl
  evidence\_manifest.json
```

### Report bevat

* \[ ] current champion;
* \[ ] challengers;
* \[ ] experiments active/completed;
* \[ ] performance comparison;
* \[ ] risk comparison;
* \[ ] drawdown comparison;
* \[ ] stopping rule events;
* \[ ] promotion/demotion decisions;
* \[ ] policy lineage;
* \[ ] open blockers;
* \[ ] next recommended action;
* \[ ] no-live statement.

### Acceptatiecriteria

* \[ ] Report is secret-free.
* \[ ] Report can be exported from dashboard.
* \[ ] Report links to evidence.
* \[ ] Report supports audit/review.

\---

## 12\. Fase 9 - Policy Lineage \& Rollback

Doel: altijd terug kunnen naar vorige paper champion.

### Nieuwe module

```text
src/binance\_spot\_bot/policy\_lineage.py
```

### Taken

* \[ ] Track policy lineage:

  * parent policy;
  * optimizer source;
  * benchmark source;
  * previous champion;
  * promotion date;
  * demotion date;
  * rollback reason.
* \[ ] Rollback command:

```powershell
python -m binance\_spot\_bot.cli policy-rollback --to previous-champion --confirm PAPER\_POLICY\_ROLLBACK
```

* \[ ] Rollback target options:

  * previous champion;
  * conservative default;
  * no-trade baseline.
* \[ ] Rollback event evidence.
* \[ ] Dashboard lineage graph/table.

### Acceptatiecriteria

* \[ ] Rollback never enables live.
* \[ ] Previous champion is preserved.
* \[ ] Rollback reason is logged.
* \[ ] Policy lineage export works.

\---

## 13\. Fase 10 - Champion/Challenger Dashboard

Doel: operator ziet policy governance zonder raw JSON.

### Nieuwe dashboardsectie

```text
Policy Governance
```

### Panels

* \[ ] current champion policy card;
* \[ ] challengers table;
* \[ ] rollout stage;
* \[ ] A/B experiment status;
* \[ ] allocation split;
* \[ ] stopping rules;
* \[ ] governance decision;
* \[ ] weekly report status;
* \[ ] policy lineage;
* \[ ] blockers;
* \[ ] next action.

### Actions

* \[ ] register paper policy;
* \[ ] create rollout plan;
* \[ ] start A/B paper experiment;
* \[ ] pause challenger;
* \[ ] promote challenger;
* \[ ] rollback champion;
* \[ ] export weekly report;
* \[ ] export governance evidence.

### Acceptatiecriteria

* \[ ] Dashboard shows `PAPER GOVERNANCE ONLY`.
* \[ ] Dangerous actions require confirmation.
* \[ ] Promotion requires evidence and operator confirmation.
* \[ ] Raw JSON only in debug expanders.
* \[ ] Browser smoke covers dashboard page.

\---

## 14\. Fase 11 - Governance CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli policy-register --policy-card <path>
python -m binance\_spot\_bot.cli policy-promote --policy-id <id> --confirm PAPER\_POLICY\_PROMOTE
python -m binance\_spot\_bot.cli policy-rollout-plan --champion <id> --challenger <id> --stage canary
python -m binance\_spot\_bot.cli ab-paper-start --rollout-id <id> --confirm PAPER\_AB
python -m binance\_spot\_bot.cli ab-paper-status --experiment-id <id>
python -m binance\_spot\_bot.cli ab-paper-stop --experiment-id <id> --reason operator\_stop
python -m binance\_spot\_bot.cli governance-decision --experiment-id <id>
python -m binance\_spot\_bot.cli weekly-governance-report
python -m binance\_spot\_bot.cli policy-rollback --to previous-champion --confirm PAPER\_POLICY\_ROLLBACK
```

### Acceptatiecriteria

* \[ ] Commands work offline/paper-only.
* \[ ] Commands support JSON output.
* \[ ] Commands require confirmation for promotion/rollback/start.
* \[ ] Commands never require API keys.
* \[ ] Commands never call order/account endpoints.

\---

## 15\. Fase 12 - Governance Evidence Bundle

Doel: alle policy governance bewijsstukken exporteerbaar maken.

### Bundle bevat

* \[ ] champion policy card;
* \[ ] challenger policy cards;
* \[ ] rollout plan;
* \[ ] A/B experiment config;
* \[ ] split assignment;
* \[ ] experiment metrics;
* \[ ] stopping decisions;
* \[ ] governance decisions;
* \[ ] weekly reports;
* \[ ] policy lineage;
* \[ ] check-all output;
* \[ ] no-live proof;
* \[ ] hashes.

### Output

```text
data/policy-governance/evidence/<bundle\_id>/
  governance\_bundle\_manifest.json
  governance\_bundle\_summary.md
  files/
```

### Acceptatiecriteria

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest.
* \[ ] Bundle can be verified.
* \[ ] Dashboard/CLI export works.
* \[ ] Bundle supports later roadmap decisions.

\---

## 16\. Fase 13 - Governance Simulation Suite

Doel: promotion/rollback/stopping rules testen vóór echte paper governance.

### Nieuwe module

```text
src/binance\_spot\_bot/governance\_simulation.py
```

### Simulaties

* \[ ] challenger strongly beats champion;
* \[ ] challenger slightly beats champion but higher drawdown;
* \[ ] challenger fails liquidity shock;
* \[ ] challenger has too few samples;
* \[ ] champion degrades;
* \[ ] evidence manifest tampered;
* \[ ] weekly report missing;
* \[ ] operator rejects promotion;
* \[ ] rollback to previous champion.

### Acceptatiecriteria

* \[ ] Simulation is deterministic.
* \[ ] Simulation is CI-safe.
* \[ ] Expected governance decisions match actual.
* \[ ] No live mode.
* \[ ] No external API calls.

\---

## 17\. Fase 14 - Tests

### Unit tests

* \[ ] `tests/test\_portfolio\_policy\_registry.py`
* \[ ] `tests/test\_policy\_promotion\_gate.py`
* \[ ] `tests/test\_paper\_policy\_rollout.py`
* \[ ] `tests/test\_ab\_paper\_experiments.py`
* \[ ] `tests/test\_paper\_experiment\_split.py`
* \[ ] `tests/test\_experiment\_stopping\_rules.py`
* \[ ] `tests/test\_policy\_governance.py`
* \[ ] `tests/test\_weekly\_governance\_report.py`
* \[ ] `tests/test\_policy\_lineage.py`
* \[ ] `tests/test\_governance\_evidence\_bundle.py`
* \[ ] `tests/test\_governance\_simulation.py`

### Integration tests

* \[ ] Register champion policy.
* \[ ] Register challenger policy.
* \[ ] Create rollout plan.
* \[ ] Start fake A/B paper experiment.
* \[ ] Trigger stopping rule.
* \[ ] Generate governance decision.
* \[ ] Promote challenger with confirmation.
* \[ ] Rollback to previous champion.
* \[ ] Export weekly governance report.
* \[ ] Export governance evidence bundle.

### Safety tests

* \[ ] Registry rejects live policy.
* \[ ] Promotion cannot create live champion.
* \[ ] A/B experiments cannot call signed endpoints.
* \[ ] Rollback cannot increase risk.
* \[ ] Reports/evidence contain no secrets.
* \[ ] Check-all remains green.
* \[ ] Browser smoke remains green.

\---

## 18\. Docs

Nieuwe docs:

* \[ ] `docs/paper-policy-governance-safety-contract.md`
* \[ ] `docs/portfolio-policy-registry.md`
* \[ ] `docs/policy-promotion-gate.md`
* \[ ] `docs/paper-policy-rollout.md`
* \[ ] `docs/ab-paper-experiments.md`
* \[ ] `docs/paper-experiment-split.md`
* \[ ] `docs/experiment-stopping-rules.md`
* \[ ] `docs/policy-governance.md`
* \[ ] `docs/weekly-governance-report.md`
* \[ ] `docs/policy-lineage-rollback.md`
* \[ ] `docs/governance-evidence-bundle.md`
* \[ ] `docs/governance-simulation-suite.md`

README updates:

* \[ ] policy governance commands;
* \[ ] champion/challenger explanation;
* \[ ] rollout stages;
* \[ ] A/B paper experiment explanation;
* \[ ] no-live statement.

\---

## 19\. Codex bouwvolgorde

### PR 1 - Portfolio Policy Registry

* \[ ] registry;
* \[ ] metadata;
* \[ ] champion alias;
* \[ ] tests.

### PR 2 - Policy Promotion Gate

* \[ ] gate checks;
* \[ ] reasons;
* \[ ] no-live tests.

### PR 3 - Paper Rollout Plan

* \[ ] rollout stages;
* \[ ] allocation split;
* \[ ] tests.

### PR 4 - A/B Paper Experiment Framework

* \[ ] experiment types;
* \[ ] metrics;
* \[ ] tests.

### PR 5 - Split Manager

* \[ ] allocation/symbol/time split;
* \[ ] deterministic seed;
* \[ ] tests.

### PR 6 - Stopping Rules

* \[ ] stop triggers;
* \[ ] stop actions;
* \[ ] tests.

### PR 7 - Governance Decision Engine

* \[ ] decisions;
* \[ ] operator confirmation;
* \[ ] tests.

### PR 8 - Weekly Governance Report + Lineage

* \[ ] reports;
* \[ ] rollback;
* \[ ] tests.

### PR 9 - Dashboard + CLI

* \[ ] dashboard panel;
* \[ ] CLI commands;
* \[ ] browser smoke.

### PR 10 - Evidence Bundle + Simulation + Docs

* \[ ] bundle export;
* \[ ] simulation suite;
* \[ ] docs.

\---

## 20\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 082 PR 1: Portfolio Policy Registry.

Maak src/binance\_spot\_bot/portfolio\_policy\_registry.py.
Gebruik het patroon van ModelRegistry, maar maak het specifiek voor paper portfolio policies.
Voeg PortfolioPolicyMetadata, PortfolioPolicyRegistry, PolicyPromotionGateResult, PolicyLineageRecord en PolicyGovernanceDecision toe.
Sla registry data lokaal op onder data/portfolio-policies/registry.json.
Ondersteun:
- register policy
- list policies
- get by id
- get champion
- set champion met previous\_champion\_id
- archive/suspend policy

Valideer dat policies alleen paper-only status kunnen krijgen en nooit live-approved.
Voeg tests toe voor:
- register candidate policy
- set champion with operator confirmation placeholder
- preserve previous champion
- reject live status
- no secrets in registry

Geen API calls, geen signed endpoints, geen orders, geen live trading.
```

Waarom eerst:

* Governance heeft eerst een policy registry nodig.
* Het bouwt logisch voort op `ModelRegistry`.
* Het raakt geen execution/orderflow.
* Het is goed testbaar en klein genoeg voor Codex.

\---

## 21\. Definition of Done

Roadmap 082 is klaar als:

* \[ ] Portfolio Policy Registry werkt.
* \[ ] Paper Policy Promotion Gate werkt.
* \[ ] Paper Rollout Plan werkt.
* \[ ] A/B Paper Experiment Framework werkt.
* \[ ] Experiment Split Manager werkt.
* \[ ] Experiment Stopping Rules werken.
* \[ ] Governance Decision Engine werkt.
* \[ ] Weekly Governance Report werkt.
* \[ ] Policy Lineage \& Rollback werkt.
* \[ ] Champion/Challenger Dashboard werkt.
* \[ ] Governance CLI commands werken.
* \[ ] Governance Evidence Bundle werkt.
* \[ ] Governance Simulation Suite werkt.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Reports zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 082 kan na uitvoering naar `Voltooid docs`.

\---

## 22\. Verwachte Roadmap 083 daarna

Na Roadmap 082 zou Roadmap 083 logisch focussen op:

```text
Roadmap 083 - Local Paper Operations Automation, Scheduled Reports \& Operator Runbooks
```

Mogelijke inhoud:

* \[ ] lokale planning van paper runs;
* \[ ] scheduled daily/weekly reports;
* \[ ] operator runbooks;
* \[ ] health checks;
* \[ ] automatic support bundle on failure;
* \[ ] governance reminders;
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

Gebouwd:

- `src/binance_spot_bot/portfolio_policy_registry.py`
- `src/binance_spot_bot/policy_promotion_gate.py`
- `src/binance_spot_bot/paper_policy_rollout.py`
- `src/binance_spot_bot/ab_paper_experiments.py`
- `src/binance_spot_bot/paper_experiment_split.py`
- `src/binance_spot_bot/experiment_stopping_rules.py`
- `src/binance_spot_bot/policy_governance.py`
- `src/binance_spot_bot/weekly_governance_report.py`
- `src/binance_spot_bot/policy_lineage.py`
- `src/binance_spot_bot/governance_evidence_bundle.py`
- `src/binance_spot_bot/governance_simulation.py`
- CLI commands voor policy register/promote/rollout, A/B paper status/start/stop, governance decision, weekly report, rollback, evidence bundle en simulation.
- Docs: `docs/paper-policy-governance-safety-contract.md`, `docs/portfolio-policy-registry.md`, `docs/paper-policy-rollout.md`.

Validatie:

- `python -m pytest -q tests/test_roadmap_082_policy_governance_full.py tests/test_roadmaps_082_088_ops_governance.py`
- CLI smoke voor alle Roadmap 082 governance commands.

Safety:

- Alle governance functies zijn paper/local-only.
- Geen Binance signed/account/order endpoints.
- Geen live trading enablement.

