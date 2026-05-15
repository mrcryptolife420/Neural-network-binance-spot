# Roadmap 102 - Operator Manual, Local Paper OS UX Training \& Support Playbooks

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/102-roadmap-operator-manual-local-paper-os-ux-training-support-playbooks.md
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
* `Roadmap docs/099-roadmap-paper-portfolio-model-ensemble-strategy-allocation-model-rotation-governance.md`
* `Roadmap docs/100-roadmap-end-to-end-paper-trading-operating-system-milestone-system-audit-production-readiness-simulation.md`
* `Roadmap docs/101-roadmap-paper-os-stabilization-sprint-blocker-burn-down-reliability-hardening.md`

Doel: Roadmap 100 maakt een volledige paper-only systeemmijlpaal en Roadmap 101 stabiliseert blockers, flaky checks, evidence gaps en reliability. Roadmap 102 maakt het systeem daarna **veilig bedienbaar en leerbaar**: een volledige operator manual, dashboard walkthroughs, lokale training mode, support bundle interpretatie, troubleshooting playbooks, onboarding checklists, guided paper simulation lessons en operator certification/sign-off.

Live trading blijft volledig buiten scope. Deze roadmap maakt documentatie en training voor paper/demo/testnet-readiness workflows. Geen live mode, geen signed real-order endpoints, geen echte account workflows en geen productieclaim voor echt geld.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 102`, `102-roadmap`, `Operator Manual`, `Local Paper OS UX Training`, `Support Playbooks` en `Paper OS Reliability Sprint 2`.
* \[x] Geen bestaande Roadmap 102 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 101 is lokaal aangemaakt als Paper OS Stabilization Sprint, Blocker Burn-Down \& Reliability Hardening.

### Codebasecontrole

Breed bekeken met operator/training/support-focus:

* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/ui/page\_registry.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] eerdere analyses van dashboard, runtime, support bundles, evidence, paper simulation, model registry, risk, paper accounting, roadmap/milestone/stabilization flows.

### Belangrijke bestaande basis

De codebase heeft nu:

* \[x] Een grote CLI command surface met diagnostics, support bundles, operator reports, evidence, runtime/paper sessions, demo pilot, model/evaluation, dashboard, demo execution en check-all.
* \[x] Een bestaande `check\_all.py` die veilige env vars forceert:

  * `PYTHONPATH=src`
  * `LIVE\_TRADING\_ENABLED=false`
  * `KILL\_SWITCH=true`
* \[x] `Runtime.UI\_MODES` beperkt tot:

  * `demo`
  * `paper`
  * `testnet-readiness`
* \[x] `ui/page\_registry.py` bevat 16 dashboard pages en blokkeert live trading pages.
* \[x] `operator\_ops.py` heeft al artifact catalog, operator health score, rehearsal profiles, support bundle restore preview, evidence chain, environment doctor, diagnostics baseline, report index, redaction self-test, command manifest, evidence manifest, local ops snapshot, retention preview, operator report en operator quality gate.
* \[x] Roadmap 100 plant milestone audit, no-live proof, readiness score, milestone bundle en operator sign-off.
* \[x] Roadmap 101 plant stabilization backlog, workplans, flaky/slow checks, evidence gap detector, waivers en stabilization gate.

### Belangrijkste gat na Roadmap 101

Na Roadmap 101 is het systeem technisch gestabiliseerd, maar nog niet optimaal bedienbaar voor een operator:

* \[ ] Geen volledige operator manual per workflow.
* \[ ] Geen dashboard walkthroughs per page.
* \[ ] Geen lokale training mode met guided lessons.
* \[ ] Geen support bundle interpretatiegids.
* \[ ] Geen troubleshooting decision trees.
* \[ ] Geen onboarding checklist voor nieuwe lokale installatie.
* \[ ] Geen operator certification/checklist.
* \[ ] Geen glossary voor alle statuses, reports, blockers, evidence en safety states.
* \[ ] Geen command cookbook met “wanneer gebruik ik welke CLI command”.
* \[ ] Geen paper simulation training scenario library.
* \[ ] Geen operator-ready “wat doe ik bij X?” playbooks.
* \[ ] Geen manual verification dat docs overeenkomen met actuele CLI/dashboard/runtime.
* \[ ] Geen no-live operator training proof.

Roadmap 102 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 102

Maak een lokale operator enablement-laag:

```text
Paper OS features
→ operator manual
→ dashboard walkthroughs
→ CLI cookbook
→ training lessons
→ troubleshooting playbooks
→ support bundle interpretation
→ operator certification
→ evidence-backed sign-off
```

Na Roadmap 102 moet een operator kunnen:

* \[ ] het systeem lokaal installeren en controleren;
* \[ ] begrijpen wat demo, paper en testnet-readiness betekenen;
* \[ ] het dashboard veilig gebruiken;
* \[ ] weten welke CLI command bij welk probleem hoort;
* \[ ] paper simulation scenario’s oefenen;
* \[ ] support bundles en evidence reports interpreteren;
* \[ ] blockers en warnings oplossen via playbooks;
* \[ ] no-live proof begrijpen en verifiëren;
* \[ ] operator sign-off uitvoeren voor paper-only gebruik;
* \[ ] weten wat expliciet niet mag: live trading, signed real-order endpoints, echte account/order workflows.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe trading features.
* \[ ] Geen nieuwe modeltraining pipeline.
* \[ ] Geen nieuwe runtime refactor.
* \[ ] Geen nieuwe dashboard rewrite.
* \[ ] Geen nieuwe release manager.
* \[ ] Geen nieuwe stabilization engine.
* \[ ] Geen cloud docs portal verplicht maken.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte account workflow.
* \[ ] Geen support bundle upload naar externe service.
* \[ ] Geen trainingslessen die echte orders plaatsen.
* \[ ] Geen operator certification die live approval suggereert.

Wel doen:

* \[ ] docs structureren;
* \[ ] dashboard training mode toevoegen;
* \[ ] CLI cookbook genereren;
* \[ ] troubleshooting playbooks bouwen;
* \[ ] support bundle interpretation toevoegen;
* \[ ] training scenario’s toevoegen;
* \[ ] operator certification en sign-off toevoegen;
* \[ ] docs/tests/evidence integreren;
* \[ ] alles paper-only en local-only houden.

\---

## 3\. Fase 0 - Operator Training Safety Contract

Nieuwe doc:

```text
docs/operator-training-safety-contract.md
```

Regels:

* \[ ] Operator training is local-only.
* \[ ] Training gebruikt alleen demo/paper/testnet-readiness.
* \[ ] Geen live mode in training.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte account workflows.
* \[ ] Training actions mogen geen orders plaatsen buiten bestaande demo/paper guardrails.
* \[ ] Training mode moet altijd no-live banner tonen.
* \[ ] Support bundle interpretation mag geen secrets tonen.
* \[ ] Troubleshooting playbooks mogen safety checks niet omzeilen.
* \[ ] Waivers worden uitgelegd maar P0 no-live/secret findings blijven niet-waivebaar.
* \[ ] Operator certification is paper-only.
* \[ ] Reports/evidence zijn secret-free.
* \[ ] Alle training exports bevatten `live\_trading\_enabled=False`.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen training docs geen live approval claims bevatten.
* \[ ] Tests bewijzen training commands geen signed/order/account commands aanbevelen.
* \[ ] Dashboard toont `OPERATOR TRAINING - NO LIVE TRADING`.
* \[ ] Training evidence is secret-free.

\---

## 4\. Fase 1 - Documentation Information Architecture

Nieuwe docs-map:

```text
docs/operator/
```

Structuur:

```text
docs/operator/
  index.md
  quick-start.md
  install-checklist.md
  safety-model.md
  dashboard-walkthroughs/
  cli-cookbook/
  troubleshooting/
  support-bundles/
  evidence/
  paper-simulation-training/
  model-ops-training/
  portfolio-training/
  release-and-roadmap-ops/
  glossary.md
  certification.md
```

Nieuwe module:

```text
src/binance\_spot\_bot/operator\_docs\_index.py
```

Dataclasses:

* \[ ] `OperatorDocPage`
* \[ ] `OperatorDocSection`
* \[ ] `OperatorDocsIndex`
* \[ ] `OperatorDocsValidationResult`

Index velden:

* \[ ] doc\_id;
* \[ ] title;
* \[ ] path;
* \[ ] category;
* \[ ] target\_operator\_level:

  * beginner;
  * normal;
  * advanced;
  * maintainer.
* \[ ] related\_cli\_commands;
* \[ ] related\_dashboard\_pages;
* \[ ] related\_playbooks;
* \[ ] related\_evidence;
* \[ ] no\_live\_statement\_present;
* \[ ] last\_validated\_ms.

Acceptatiecriteria:

* \[ ] Operator docs index wordt gegenereerd.
* \[ ] Ontbrekende docs worden gerapporteerd.
* \[ ] No-live statement wordt per doc gecontroleerd.
* \[ ] Docs index is Markdown + JSON.
* \[ ] Tests gebruiken fixture docs.

\---

## 5\. Fase 2 - Operator Quick Start \& Install Checklist

Nieuwe docs:

```text
docs/operator/quick-start.md
docs/operator/install-checklist.md
docs/operator/safety-model.md
```

Quick start bevat:

* \[ ] projectdoel;
* \[ ] wat is demo mode;
* \[ ] wat is paper mode;
* \[ ] wat is testnet-readiness;
* \[ ] wat is expliciet geen live trading;
* \[ ] basis commands:

  * `validate-config`;
  * `preflight`;
  * `check-all`;
  * `launch-dashboard`;
  * `dashboard-smoke`;
  * `paper-session`;
  * `operator-quality-gate`;
  * `support-bundle`;
* \[ ] eerste dashboard start;
* \[ ] eerste paper simulation;
* \[ ] evidence export;
* \[ ] support bundle maken.

Install checklist bevat:

* \[ ] Python versie;
* \[ ] dependencies;
* \[ ] `.env` uitleg zonder secrets te tonen;
* \[ ] data dir;
* \[ ] audit log path;
* \[ ] safe env vars;
* \[ ] dashboard smoke;
* \[ ] no-live proof;
* \[ ] first support bundle verify.

Acceptatiecriteria:

* \[ ] Beginner kan quick-start volgen zonder live credentials.
* \[ ] Checklist bevat no-live verification.
* \[ ] Commands komen overeen met actuele CLI.
* \[ ] Docs bevatten geen echte secrets.
* \[ ] Docs validation test groen.

\---

## 6\. Fase 3 - CLI Cookbook Generator

Nieuwe module:

```text
src/binance\_spot\_bot/operator\_cli\_cookbook.py
```

Input:

* \[ ] `operator\_command\_manifest()`;
* \[ ] argparse/CLI command inventory;
* \[ ] Roadmap 091 CLI surface map indien beschikbaar;
* \[ ] docs handmatige metadata.

Output docs:

```text
docs/operator/cli-cookbook/
  index.md
  health-checks.md
  dashboard.md
  paper-runtime.md
  demo-pilot.md
  support-bundles.md
  evidence.md
  model-evaluation.md
  security-redaction.md
  roadmap-release.md
```

Per command:

* \[ ] command;
* \[ ] purpose;
* \[ ] when to use;
* \[ ] safe mode;
* \[ ] examples;
* \[ ] expected output;
* \[ ] common failures;
* \[ ] related playbooks;
* \[ ] no-live statement;
* \[ ] forbidden variants.

Acceptatiecriteria:

* \[ ] Cookbook genereert docs uit command manifest.
* \[ ] Alle operator commands hebben minimaal korte uitleg.
* \[ ] Deprecated/unknown command references worden gerapporteerd.
* \[ ] Commands bevatten geen live/signed/order/account instructies.
* \[ ] Tests vergelijken manifest met cookbook.

\---

## 7\. Fase 4 - Dashboard Walkthroughs

Nieuwe docs:

```text
docs/operator/dashboard-walkthroughs/
```

Per bestaande dashboard page:

* \[ ] `overview.md`
* \[ ] `demo-spot-trading.md`
* \[ ] `credentials-profile.md`
* \[ ] `bot-controls.md`
* \[ ] `risk-controls.md`
* \[ ] `strategy-model.md`
* \[ ] `market-data.md`
* \[ ] `orders-account.md`
* \[ ] `sessions.md`
* \[ ] `evaluation.md`
* \[ ] `strategy-lab.md`
* \[ ] `research.md`
* \[ ] `portfolio.md`
* \[ ] `readiness.md`
* \[ ] `logs-security.md`
* \[ ] `demo-pilot.md`

Per walkthrough:

* \[ ] doel van page;
* \[ ] wanneer gebruiken;
* \[ ] belangrijkste widgets;
* \[ ] veilige acties;
* \[ ] acties die confirm nodig hebben;
* \[ ] wat nooit live is;
* \[ ] interpretatie van statuses;
* \[ ] common warnings;
* \[ ] gerelateerde CLI commands;
* \[ ] evidence die page kan maken;
* \[ ] troubleshooting.

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_walkthroughs.py
```

Acceptatiecriteria:

* \[ ] Walkthroughs worden gekoppeld aan `page\_registry.py`.
* \[ ] Elke registry page heeft doc.
* \[ ] Missing walkthrough wordt gerapporteerd.
* \[ ] Docs bevatten stable no-live statement.
* \[ ] Browser smoke kan training links checken.

\---

## 8\. Fase 5 - Local Training Mode

Nieuwe module:

```text
src/binance\_spot\_bot/operator\_training.py
```

Dashboardsectie:

```text
Operator Training
```

Training modes:

* \[ ] beginner;
* \[ ] normal operator;
* \[ ] advanced operator;
* \[ ] maintainer.

Lesson types:

* \[ ] read-only lesson;
* \[ ] command walkthrough;
* \[ ] dashboard walkthrough;
* \[ ] paper simulation exercise;
* \[ ] evidence interpretation exercise;
* \[ ] troubleshooting exercise;
* \[ ] sign-off exercise.

Dataclasses:

* \[ ] `TrainingLesson`
* \[ ] `TrainingStep`
* \[ ] `TrainingProgress`
* \[ ] `TrainingAssessment`
* \[ ] `TrainingEvidence`

Acceptatiecriteria:

* \[ ] Training mode werkt local-only.
* \[ ] Training mode toont no-live banner.
* \[ ] Training steps zijn JSON-serializable.
* \[ ] Progress kan lokaal opgeslagen worden.
* \[ ] Tests bewijzen training actions geen live endpoints aanraden.

\---

## 9\. Fase 6 - Training Scenario Library

Nieuwe map:

```text
docs/operator/paper-simulation-training/
```

Scenario’s:

* \[ ] `scenario-001-first-health-check.md`
* \[ ] `scenario-002-first-dashboard-launch.md`
* \[ ] `scenario-003-paper-session-smoke.md`
* \[ ] `scenario-004-risk-block-expected.md`
* \[ ] `scenario-005-data-quality-warning.md`
* \[ ] `scenario-006-support-bundle-create-and-verify.md`
* \[ ] `scenario-007-evidence-manifest-review.md`
* \[ ] `scenario-008-operator-quality-gate.md`
* \[ ] `scenario-009-dashboard-smoke.md`
* \[ ] `scenario-010-roadmap-100-milestone-review.md`
* \[ ] `scenario-011-stabilization-backlog-review.md`
* \[ ] `scenario-012-no-live-proof-review.md`

Nieuwe module:

```text
src/binance\_spot\_bot/training\_scenarios.py
```

Per scenario:

* \[ ] scenario\_id;
* \[ ] title;
* \[ ] difficulty;
* \[ ] preconditions;
* \[ ] commands;
* \[ ] expected outputs;
* \[ ] pass criteria;
* \[ ] failure hints;
* \[ ] evidence artifacts;
* \[ ] no-live proof.

Acceptatiecriteria:

* \[ ] Scenario library kan worden gelist via CLI.
* \[ ] Scenario can be validated against known commands.
* \[ ] Scenario output is dashboard-ready.
* \[ ] Scenario docs contain no live instructions.
* \[ ] Tests cover scenario validation.

\---

## 10\. Fase 7 - Troubleshooting Playbook Library

Nieuwe docs:

```text
docs/operator/troubleshooting/
```

Playbooks:

* \[ ] `config-validation-failed.md`
* \[ ] `preflight-failed.md`
* \[ ] `security-scan-finding.md`
* \[ ] `redaction-self-test-failed.md`
* \[ ] `check-all-failed.md`
* \[ ] `dashboard-import-failed.md`
* \[ ] `dashboard-browser-smoke-failed.md`
* \[ ] `paper-session-failed.md`
* \[ ] `paper-simulation-no-fill.md`
* \[ ] `risk-block-why.md`
* \[ ] `data-quality-warning.md`
* \[ ] `support-bundle-verify-failed.md`
* \[ ] `operator-quality-gate-failed.md`
* \[ ] `evidence-gap-found.md`
* \[ ] `roadmap-traceability-gap.md`
* \[ ] `milestone-bundle-verify-failed.md`
* \[ ] `stabilization-gate-failed.md`
* \[ ] `model-promotion-blocked.md`
* \[ ] `model-drift-warning.md`
* \[ ] `portfolio-allocation-blocked.md`
* \[ ] `no-live-proof-failed.md`

Nieuwe module:

```text
src/binance\_spot\_bot/troubleshooting\_playbooks.py
```

Per playbook:

* \[ ] symptom;
* \[ ] likely causes;
* \[ ] diagnostic commands;
* \[ ] safe remediation steps;
* \[ ] evidence to collect;
* \[ ] when to stop;
* \[ ] escalation path;
* \[ ] related docs;
* \[ ] no-live constraints.

Acceptatiecriteria:

* \[ ] Playbooks zijn indexeerbaar.
* \[ ] Playbooks linken naar geldige commands/docs.
* \[ ] P0 playbooks bevatten stop/blocked guidance.
* \[ ] Geen playbook suggereert live trading.
* \[ ] Tests valideren command references.

\---

## 11\. Fase 8 - Support Bundle Interpretation Guide

Nieuwe docs:

```text
docs/operator/support-bundles/
  support-bundle-overview.md
  support-bundle-manifest.md
  support-bundle-verify.md
  support-bundle-restore-preview.md
  support-bundle-redaction.md
  support-bundle-troubleshooting.md
```

Nieuwe module:

```text
src/binance\_spot\_bot/support\_bundle\_interpreter.py
```

Dataclasses:

* \[ ] `SupportBundleInterpretation`
* \[ ] `SupportBundleSection`
* \[ ] `SupportBundleFinding`
* \[ ] `SupportBundleRecommendation`

Functionaliteit:

* \[ ] support bundle manifest lezen;
* \[ ] verify output uitleggen;
* \[ ] missing files detecteren;
* \[ ] redaction status uitleggen;
* \[ ] common problems koppelen aan playbooks;
* \[ ] no-live proof samenvatten;
* \[ ] recommended next commands geven.

Acceptatiecriteria:

* \[ ] Interpreter werkt op bestaande support bundle manifests.
* \[ ] Interpreter toont geen raw secrets.
* \[ ] Interpreter kan Markdown + JSON exporteren.
* \[ ] Dashboard kan interpretation tonen.
* \[ ] Tests gebruiken fixture bundle.

\---

## 12\. Fase 9 - Evidence Interpretation Guide

Nieuwe docs:

```text
docs/operator/evidence/
  evidence-overview.md
  evidence-manifest.md
  evidence-chain.md
  local-ops-snapshot.md
  operator-quality-gate.md
  no-live-proof.md
  milestone-bundle.md
  stabilization-evidence.md
```

Nieuwe module:

```text
src/binance\_spot\_bot/evidence\_interpreter.py
```

Interpreteert:

* \[ ] evidence manifest;
* \[ ] evidence chain;
* \[ ] local ops snapshot;
* \[ ] operator quality gate output;
* \[ ] redaction self-test output;
* \[ ] system audit output;
* \[ ] milestone bundle output;
* \[ ] stabilization evidence output.

Output:

* \[ ] status summary;
* \[ ] blockers;
* \[ ] warnings;
* \[ ] next action;
* \[ ] related playbooks;
* \[ ] no-live proof;
* \[ ] verification status.

Acceptatiecriteria:

* \[ ] Interpreter werkt met missing artifacts.
* \[ ] Missing artifacts worden warnings.
* \[ ] P0 findings highlighted.
* \[ ] Output is secret-free.
* \[ ] Tests use fixture evidence.

\---

## 13\. Fase 10 - Operator Glossary \& Status Dictionary

Nieuwe docs:

```text
docs/operator/glossary.md
docs/operator/status-dictionary.md
```

Begrippen:

* \[ ] demo mode;
* \[ ] paper mode;
* \[ ] testnet-readiness;
* \[ ] live disabled;
* \[ ] kill switch;
* \[ ] support bundle;
* \[ ] evidence manifest;
* \[ ] evidence chain;
* \[ ] operator quality gate;
* \[ ] no-live proof;
* \[ ] safety invariant;
* \[ ] milestone bundle;
* \[ ] stabilization backlog;
* \[ ] waiver;
* \[ ] P0/P1/P2/P3/P4;
* \[ ] model candidate;
* \[ ] champion paper;
* \[ ] drift;
* \[ ] paper portfolio;
* \[ ] allocation;
* \[ ] dashboard smoke;
* \[ ] browser smoke.

Nieuwe module:

```text
src/binance\_spot\_bot/operator\_glossary.py
```

Acceptatiecriteria:

* \[ ] Glossary is searchable via CLI/dashboard.
* \[ ] Status dictionary maps known statuses to explanation.
* \[ ] Unknown status produces fallback explanation.
* \[ ] No live approval language.
* \[ ] Tests cover common terms.

\---

## 14\. Fase 11 - Guided No-Live Verification Lesson

Nieuwe module:

```text
src/binance\_spot\_bot/no\_live\_training.py
```

Lesson teaches:

* \[ ] why live trading is disabled;
* \[ ] how to verify `UI\_MODES`;
* \[ ] how to verify dashboard modes;
* \[ ] how to verify check-all safe env;
* \[ ] how to run no-live proof pack;
* \[ ] how to interpret no-live failure;
* \[ ] what to do if live appears anywhere;
* \[ ] what not to do.

CLI:

```powershell
python -m binance\_spot\_bot.cli no-live-training
python -m binance\_spot\_bot.cli no-live-training --json
```

Acceptatiecriteria:

* \[ ] Lesson runs offline.
* \[ ] Lesson outputs step-by-step verification.
* \[ ] Failure examples are safe fixtures.
* \[ ] Report includes no-live proof.
* \[ ] Tests cover pass/fail examples.

\---

## 15\. Fase 12 - Operator Certification Checklist

Nieuwe docs:

```text
docs/operator/certification.md
```

Nieuwe module:

```text
src/binance\_spot\_bot/operator\_certification.py
```

Certification levels:

* \[ ] read-only observer;
* \[ ] paper operator;
* \[ ] advanced paper operator;
* \[ ] maintainer.

Checklist items:

* \[ ] can run validate-config;
* \[ ] can run preflight;
* \[ ] can run check-all;
* \[ ] can open dashboard safely;
* \[ ] can explain demo/paper/testnet-readiness;
* \[ ] can create and verify support bundle;
* \[ ] can read operator quality gate;
* \[ ] can interpret no-live proof;
* \[ ] can run paper session smoke;
* \[ ] can export evidence manifest;
* \[ ] can use troubleshooting playbook;
* \[ ] understands forbidden live actions.

Certification output:

* \[ ] local certificate JSON;
* \[ ] Markdown summary;
* \[ ] evidence links;
* \[ ] expiry date;
* \[ ] paper-only statement.

Acceptatiecriteria:

* \[ ] Certification cannot approve live trading.
* \[ ] Certification requires no-live lesson.
* \[ ] Certification stores local evidence.
* \[ ] Expired certification is reported.
* \[ ] Tests cover certification levels.

\---

## 16\. Fase 13 - Operator Training Dashboard Panel

Nieuwe dashboardsectie:

```text
Operator Training \& Playbooks
```

Panels:

* \[ ] training overview;
* \[ ] beginner quick start;
* \[ ] dashboard walkthrough selector;
* \[ ] CLI cookbook browser;
* \[ ] training scenario library;
* \[ ] troubleshooting playbooks;
* \[ ] support bundle interpreter;
* \[ ] evidence interpreter;
* \[ ] glossary search;
* \[ ] no-live verification lesson;
* \[ ] certification checklist;
* \[ ] training progress;
* \[ ] export training evidence.

Actions:

* \[ ] start lesson;
* \[ ] mark step complete;
* \[ ] run safe command copy;
* \[ ] interpret support bundle;
* \[ ] interpret evidence folder;
* \[ ] generate certification draft;
* \[ ] export training evidence.

Safeguards:

* \[ ] `OPERATOR TRAINING - NO LIVE TRADING` badge.
* \[ ] No live controls.
* \[ ] Commands are copy-first, execute only if existing safe runner supports it.
* \[ ] Raw JSON limited/debug only.
* \[ ] Stable widget keys.
* \[ ] Browser smoke covers panel.

Acceptatiecriteria:

* \[ ] Dashboard shows training lessons.
* \[ ] Dashboard can open playbooks.
* \[ ] Dashboard can interpret support/evidence artifacts.
* \[ ] Dashboard blocks live approval wording.
* \[ ] Browser smoke passes.

\---

## 17\. Fase 14 - Operator Training CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli operator-docs-index
python -m binance\_spot\_bot.cli operator-docs-validate
python -m binance\_spot\_bot.cli operator-cli-cookbook
python -m binance\_spot\_bot.cli dashboard-walkthroughs
python -m binance\_spot\_bot.cli training-scenarios
python -m binance\_spot\_bot.cli training-scenario-run --scenario scenario-003-paper-session-smoke
python -m binance\_spot\_bot.cli troubleshooting-playbooks
python -m binance\_spot\_bot.cli support-bundle-interpret --bundle data/support/support-bundle.zip
python -m binance\_spot\_bot.cli evidence-interpret --path data/evidence/manifest/latest-evidence-manifest.json
python -m binance\_spot\_bot.cli operator-glossary --term "kill switch"
python -m binance\_spot\_bot.cli no-live-training
python -m binance\_spot\_bot.cli operator-certification-draft --level paper-operator
python -m binance\_spot\_bot.cli operator-certification-complete --level paper-operator --confirm PAPER\_ONLY\_CERTIFICATION
python -m binance\_spot\_bot.cli operator-training-evidence-export
```

Acceptatiecriteria:

* \[ ] Commands werken offline.
* \[ ] Commands ondersteunen JSON output.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Certification command kan live approval niet claimen.
* \[ ] Reports zijn secret-free.

\---

## 18\. Fase 15 - Training Progress Store

Nieuwe module:

```text
src/binance\_spot\_bot/operator\_training\_store.py
```

Storage:

```text
data/operator-training/
  progress/
  assessments/
  certifications/
  reports/
  evidence/
```

Dataclasses:

* \[ ] `TrainingProgressRecord`
* \[ ] `TrainingAssessmentRecord`
* \[ ] `OperatorCertificationRecord`
* \[ ] `TrainingEvidenceManifest`

Functionaliteit:

* \[ ] progress save/load;
* \[ ] lesson completion;
* \[ ] assessment result;
* \[ ] certification status;
* \[ ] expiry tracking;
* \[ ] evidence links;
* \[ ] manifest verify.

Acceptatiecriteria:

* \[ ] Store is local-only.
* \[ ] Store is manifest/hash based.
* \[ ] Store contains no secrets.
* \[ ] Expired certifications are reported.
* \[ ] Tests use temp dirs.

\---

## 19\. Fase 16 - Training Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/operator\_training\_evidence.py
```

Bundle bevat:

* \[ ] docs index validation;
* \[ ] CLI cookbook validation;
* \[ ] dashboard walkthrough validation;
* \[ ] training scenario validation;
* \[ ] playbook validation;
* \[ ] support bundle interpretation sample;
* \[ ] evidence interpretation sample;
* \[ ] no-live training result;
* \[ ] certification checklist result;
* \[ ] training progress;
* \[ ] no-live proof;
* \[ ] redaction proof;
* \[ ] hashes.

Output:

```text
data/operator-training/evidence/<run\_id>/
  operator\_training\_evidence\_manifest.json
  operator\_training\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle links to Roadmap 100/101 evidence where available.
* \[ ] Dashboard/CLI export works.

\---

## 20\. Fase 17 - Docs Consistency \& Drift Checks

Nieuwe module:

```text
src/binance\_spot\_bot/operator\_docs\_consistency.py
```

Checks:

* \[ ] docs command exists in CLI;
* \[ ] dashboard page docs exist for every page registry item;
* \[ ] no-live statement present;
* \[ ] no forbidden live phrase;
* \[ ] support bundle docs match command output fields;
* \[ ] evidence docs match evidence manifest fields;
* \[ ] troubleshooting playbooks link valid docs/commands;
* \[ ] certification checklist links valid commands;
* \[ ] roadmap references valid files;
* \[ ] outdated commands detected.

Forbidden phrases:

* \[ ] `enable live trading`;
* \[ ] `live approved`;
* \[ ] `real funds`;
* \[ ] `production live`;
* \[ ] `place real order`;
* \[ ] `account balance required` unless explicitly explaining forbidden/blocked.

Acceptatiecriteria:

* \[ ] Drift checker finds missing page doc.
* \[ ] Drift checker finds stale command.
* \[ ] Drift checker flags forbidden live approval language.
* \[ ] Report is Markdown + JSON.
* \[ ] Tests use fixture docs.

\---

## 21\. Fase 18 - Roadmap 100/101 Integration

Roadmap 100 integration:

* \[ ] Operator manual links system inventory.
* \[ ] Operator manual explains readiness score.
* \[ ] Milestone dashboard links to training docs.
* \[ ] No-live proof pack has training explanation.
* \[ ] Operator sign-off requires certification checklist where configured.

Roadmap 101 integration:

* \[ ] Stabilization backlog items link to troubleshooting playbooks.
* \[ ] Workplans link to CLI cookbook and playbooks.
* \[ ] Flaky/slow reports link to playbooks.
* \[ ] Evidence gap detector links evidence interpretation docs.
* \[ ] Waiver docs explain waiver rules and expiry.

Acceptatiecriteria:

* \[ ] Roadmap 100 reports can link operator docs.
* \[ ] Roadmap 101 reports can link playbooks.
* \[ ] Training evidence can be included in milestone/stabilization bundles.
* \[ ] No-live proof preserved.
* \[ ] Tests use fixture links.

\---

## 22\. Fase 19 - Knowledge/Test/Release Integration

Roadmap 091 integration:

* \[ ] Knowledge graph maps operator docs to modules/commands/pages.
* \[ ] Impact analysis flags docs that need updating when CLI/dashboard changes.
* \[ ] Docs ownership map includes operator docs.

Roadmap 092 integration:

* \[ ] Operator docs changes select docs consistency tests.
* \[ ] CLI cookbook changes select command manifest tests.
* \[ ] Dashboard walkthrough changes select page registry tests.

Roadmap 089/090 integration:

* \[ ] Release notes include operator docs changes.
* \[ ] Codex task packs include docs update requirements.
* \[ ] Roadmap completion gate requires docs consistency pass.

Roadmap 094 integration:

* \[ ] Dashboard training page uses stable widget keys.
* \[ ] Browser smoke includes training panel.

Acceptatiecriteria:

* \[ ] Docs drift triggers correct tests.
* \[ ] Release evidence includes docs validation.
* \[ ] Completion gate can require operator training evidence.
* \[ ] Browser smoke covers training UI.
* \[ ] No-live proof preserved.

\---

## 23\. Fase 20 - Scheduled Operator Training Reports

Uitbreiding op Roadmap 083/084:

Scheduled jobs:

* \[ ] weekly operator docs validation;
* \[ ] weekly command cookbook drift check;
* \[ ] weekly dashboard walkthrough drift check;
* \[ ] weekly expired certification check;
* \[ ] monthly operator training evidence export;
* \[ ] post-release docs consistency check;
* \[ ] post-roadmap completion docs drift check.

Metrics:

* \[ ] docs coverage percent;
* \[ ] dashboard page doc coverage;
* \[ ] CLI cookbook coverage;
* \[ ] playbook count;
* \[ ] broken docs links;
* \[ ] forbidden phrase findings;
* \[ ] certification count;
* \[ ] expired certification count;
* \[ ] training scenario pass count.

Acceptatiecriteria:

* \[ ] Jobs are local-only.
* \[ ] Reports are secret-free.
* \[ ] No-live proof included.
* \[ ] Dashboard can show metrics.
* \[ ] No live trading.

\---

## 24\. Fase 21 - Tests

### Unit tests

* \[ ] `tests/test\_operator\_training\_safety\_contract.py`
* \[ ] `tests/test\_operator\_docs\_index.py`
* \[ ] `tests/test\_operator\_cli\_cookbook.py`
* \[ ] `tests/test\_dashboard\_walkthroughs.py`
* \[ ] `tests/test\_operator\_training.py`
* \[ ] `tests/test\_training\_scenarios.py`
* \[ ] `tests/test\_troubleshooting\_playbooks.py`
* \[ ] `tests/test\_support\_bundle\_interpreter.py`
* \[ ] `tests/test\_evidence\_interpreter.py`
* \[ ] `tests/test\_operator\_glossary.py`
* \[ ] `tests/test\_no\_live\_training.py`
* \[ ] `tests/test\_operator\_certification.py`
* \[ ] `tests/test\_operator\_training\_store.py`
* \[ ] `tests/test\_operator\_training\_evidence.py`
* \[ ] `tests/test\_operator\_docs\_consistency.py`

### Integration tests

* \[ ] Build operator docs index.
* \[ ] Validate quick-start commands against CLI.
* \[ ] Generate CLI cookbook from command manifest.
* \[ ] Validate dashboard walkthrough coverage against page registry.
* \[ ] Load training scenarios.
* \[ ] Validate troubleshooting playbooks.
* \[ ] Interpret fixture support bundle.
* \[ ] Interpret fixture evidence manifest.
* \[ ] Run no-live training lesson.
* \[ ] Create certification draft.
* \[ ] Complete paper-only certification with confirm.
* \[ ] Export training evidence bundle.

### Safety tests

* \[ ] Training docs cannot contain live approval language.
* \[ ] CLI cookbook cannot suggest signed/order/account commands.
* \[ ] Training scenario cannot run live command.
* \[ ] Certification cannot approve live trading.
* \[ ] Support bundle interpretation redacts secrets.
* \[ ] Evidence interpretation redacts secrets.
* \[ ] No-live training failure is blocking.
* \[ ] Dashboard training panel has no live controls.
* \[ ] Reports/evidence are secret-free.
* \[ ] Check-all safe env remains `LIVE\_TRADING\_ENABLED=false` and `KILL\_SWITCH=true`.

\---

## 25\. Docs

Nieuwe docs:

* \[ ] `docs/operator-training-safety-contract.md`
* \[ ] `docs/operator/index.md`
* \[ ] `docs/operator/quick-start.md`
* \[ ] `docs/operator/install-checklist.md`
* \[ ] `docs/operator/safety-model.md`
* \[ ] `docs/operator/glossary.md`
* \[ ] `docs/operator/status-dictionary.md`
* \[ ] `docs/operator/certification.md`
* \[ ] `docs/operator/cli-cookbook/index.md`
* \[ ] `docs/operator/dashboard-walkthroughs/index.md`
* \[ ] `docs/operator/troubleshooting/index.md`
* \[ ] `docs/operator/support-bundles/support-bundle-overview.md`
* \[ ] `docs/operator/evidence/evidence-overview.md`
* \[ ] `docs/operator/paper-simulation-training/index.md`
* \[ ] `docs/operator/model-ops-training/index.md`
* \[ ] `docs/operator/portfolio-training/index.md`
* \[ ] `docs/operator/release-and-roadmap-ops/index.md`

README updates:

* \[ ] link to operator quick start;
* \[ ] link to no-live safety model;
* \[ ] link to CLI cookbook;
* \[ ] link to dashboard walkthroughs;
* \[ ] link to troubleshooting playbooks;
* \[ ] link to support bundle guide;
* \[ ] link to operator certification;
* \[ ] no-live statement.

\---

## 26\. CLI command examples

### Operator docs index

```powershell
python -m binance\_spot\_bot.cli operator-docs-index --json
```

### Docs consistency

```powershell
python -m binance\_spot\_bot.cli operator-docs-validate --json
```

### CLI cookbook genereren

```powershell
python -m binance\_spot\_bot.cli operator-cli-cookbook --json
```

### Training scenario’s tonen

```powershell
python -m binance\_spot\_bot.cli training-scenarios --json
```

### Paper session training scenario

```powershell
python -m binance\_spot\_bot.cli training-scenario-run --scenario scenario-003-paper-session-smoke --json
```

### Support bundle interpreteren

```powershell
python -m binance\_spot\_bot.cli support-bundle-interpret --bundle data/support/support-bundle.zip --json
```

### Evidence interpreteren

```powershell
python -m binance\_spot\_bot.cli evidence-interpret --path data/evidence/manifest/latest-evidence-manifest.json --json
```

### No-live training

```powershell
python -m binance\_spot\_bot.cli no-live-training --json
```

### Paper-only certification

```powershell
python -m binance\_spot\_bot.cli operator-certification-complete --level paper-operator --confirm PAPER\_ONLY\_CERTIFICATION
```

\---

## 27\. Codex bouwvolgorde

### PR 1 - Safety Contract + Operator Docs Index

* \[ ] `docs/operator-training-safety-contract.md`
* \[ ] `docs/operator/index.md`
* \[ ] `operator\_docs\_index.py`
* \[ ] docs index tests.

### PR 2 - Quick Start + Install Checklist + Safety Model

* \[ ] quick start docs.
* \[ ] install checklist.
* \[ ] safety model.
* \[ ] docs validation tests.

### PR 3 - CLI Cookbook Generator

* \[ ] `operator\_cli\_cookbook.py`
* \[ ] CLI cookbook docs.
* \[ ] command reference validation tests.

### PR 4 - Dashboard Walkthroughs

* \[ ] `dashboard\_walkthroughs.py`
* \[ ] docs for 16 pages.
* \[ ] page registry coverage tests.

### PR 5 - Training Mode + Scenario Library

* \[ ] `operator\_training.py`
* \[ ] `training\_scenarios.py`
* \[ ] training scenario docs.
* \[ ] tests.

### PR 6 - Troubleshooting Playbooks

* \[ ] `troubleshooting\_playbooks.py`
* \[ ] P0/P1/P2 playbooks.
* \[ ] command/doc link tests.

### PR 7 - Support/Evidence Interpreters

* \[ ] `support\_bundle\_interpreter.py`
* \[ ] `evidence\_interpreter.py`
* \[ ] fixture artifact tests.

### PR 8 - Glossary + No-Live Training + Certification

* \[ ] `operator\_glossary.py`
* \[ ] `no\_live\_training.py`
* \[ ] `operator\_certification.py`
* \[ ] certification tests.

### PR 9 - Training Store + Evidence + Docs Consistency

* \[ ] `operator\_training\_store.py`
* \[ ] `operator\_training\_evidence.py`
* \[ ] `operator\_docs\_consistency.py`
* \[ ] evidence/drift tests.

### PR 10 - CLI + Dashboard + Integrations + Scheduled Reports

* \[ ] CLI commands.
* \[ ] Operator Training dashboard panel.
* \[ ] Roadmap 100/101 integrations.
* \[ ] release/test/knowledge integrations.
* \[ ] browser smoke.
* \[ ] README updates.

\---

## 28\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 102 PR 1: Operator Training Safety Contract + Operator Docs Index.

Maak docs/operator-training-safety-contract.md.
Maak docs/operator/index.md.

Maak src/binance\_spot\_bot/operator\_docs\_index.py met:
- OperatorDocPage
- OperatorDocSection
- OperatorDocsIndex
- OperatorDocsValidationResult
- build\_operator\_docs\_index(root: Path)
- validate\_operator\_docs\_index(index: OperatorDocsIndex)
- operator\_docs\_index\_to\_dict(...)
- write\_operator\_docs\_index(...)

Docs index moet minimaal scannen:
- docs/operator/
- docs/operator/dashboard-walkthroughs/
- docs/operator/cli-cookbook/
- docs/operator/troubleshooting/
- docs/operator/support-bundles/
- docs/operator/evidence/

Per doc:
- doc\_id
- title
- path
- category
- target\_operator\_level
- related\_cli\_commands
- related\_dashboard\_pages
- related\_playbooks
- no\_live\_statement\_present
- missing\_or\_empty
- live\_trading\_enabled=False

Validatie moet:
- missing docs/operator/index.md blokkeren
- empty docs waarschuwen
- ontbrekende no-live statement waarschuwen
- forbidden live approval phrases blokkeren
- output secret-free maken

Gebruik alleen stdlib.
Geen command execution.
Geen dashboard execution.
Geen runtime execution.
Geen GitHub API calls.
Geen signed endpoints.
Geen account/order endpoints.
Geen live trading.

Voeg tests toe voor:
- docs index fixture
- missing index doc
- empty doc warning
- no-live statement detection
- forbidden live phrase blocked
- JSON serialization
- secret-like values worden geredact
- live\_trading\_enabled=False
- no\_live\_statement aanwezig
```

Waarom eerst:

* De operator manual heeft eerst een index en safety contract nodig.
* Het is read-only en raakt runtime/trading niet.
* Het is klein genoeg voor Codex.
* No-live en forbidden phrase checks kunnen meteen getest worden.
* Daarna kunnen CLI cookbook, dashboard walkthroughs, playbooks en training mode veilig op deze index bouwen.

\---

## 29\. Definition of Done

Roadmap 102 is klaar als:

* \[ ] Operator Training Safety Contract bestaat.
* \[ ] Documentation Information Architecture bestaat.
* \[ ] Operator Quick Start \& Install Checklist bestaan.
* \[ ] CLI Cookbook Generator werkt.
* \[ ] Dashboard Walkthroughs bestaan voor alle registry pages.
* \[ ] Local Training Mode werkt.
* \[ ] Training Scenario Library werkt.
* \[ ] Troubleshooting Playbook Library werkt.
* \[ ] Support Bundle Interpretation Guide werkt.
* \[ ] Evidence Interpretation Guide werkt.
* \[ ] Operator Glossary \& Status Dictionary werken.
* \[ ] Guided No-Live Verification Lesson werkt.
* \[ ] Operator Certification Checklist werkt.
* \[ ] Operator Training Dashboard Panel werkt.
* \[ ] Operator Training CLI Commands werken.
* \[ ] Training Progress Store werkt.
* \[ ] Training Evidence Bundle werkt.
* \[ ] Docs Consistency \& Drift Checks werken.
* \[ ] Roadmap 100/101 integraties werken.
* \[ ] Knowledge/Test/Release integraties werken.
* \[ ] Scheduled Operator Training Reports werken.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen docs/training geen live approval language bevatten.
* \[ ] Tests bewijzen support/evidence interpretation secret-free is.
* \[ ] Dashboard browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 102 kan na uitvoering naar `Voltooid docs`.

\---

## 30\. Verwachte Roadmap 103 daarna

Na Roadmap 102 is de meest logische opvolger:

```text
Roadmap 103 - Local Paper OS User Acceptance Testing, Guided Rehearsals \& Operator Feedback Loop
```

Mogelijke inhoud:

* \[ ] UAT scenario runner;
* \[ ] guided operator rehearsals;
* \[ ] feedback collection local-only;
* \[ ] usability scorecards;
* \[ ] training completion analytics;
* \[ ] dashboard UX improvement backlog;
* \[ ] support playbook improvements;
* \[ ] still no live trading.

```

Alternatief als Roadmap 101 nog veel blockers open laat:

```text
Roadmap 103 - Paper OS Reliability Sprint 2, Remaining Blockers \& Regression Cleanup
```



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

## Implementatie-evidence 2026-05-15

Status: Volledig afgewerkt en gevalideerd.

Gebouwd:

* [x] Operator training safety contract.
* [x] Operator docs information architecture.
* [x] Quick start, install checklist en safety model docs.
* [x] CLI cookbook generator.
* [x] Dashboard walkthroughs.
* [x] Local training lessons.
* [x] Training scenario library.
* [x] Troubleshooting playbook library.
* [x] Support bundle interpreter.
* [x] Evidence interpreter.
* [x] Operator glossary en status uitleg.
* [x] Guided no-live training lesson.
* [x] Paper-only operator certification flow.
* [x] Operator training dashboard panel update.
* [x] Operator training CLI commands.
* [x] Training progress store.
* [x] Operator training evidence bundle.
* [x] Docs consistency checks.

Belangrijke bestanden:

* `src/binance_spot_bot/operator_docs_index.py`
* `src/binance_spot_bot/operator_cli_cookbook.py`
* `src/binance_spot_bot/dashboard_walkthroughs.py`
* `src/binance_spot_bot/operator_training.py`
* `src/binance_spot_bot/training_scenarios.py`
* `src/binance_spot_bot/troubleshooting_playbooks.py`
* `src/binance_spot_bot/support_bundle_interpreter.py`
* `src/binance_spot_bot/evidence_interpreter.py`
* `src/binance_spot_bot/operator_glossary.py`
* `src/binance_spot_bot/no_live_training.py`
* `src/binance_spot_bot/operator_certification.py`
* `src/binance_spot_bot/operator_training_store.py`
* `src/binance_spot_bot/operator_training_evidence.py`
* `src/binance_spot_bot/operator_docs_consistency.py`
* `tests/test_roadmap_102_operator_training_acceptance.py`

Validatie:

* [x] `python -m pytest tests/test_roadmap_102_operator_training_acceptance.py tests/test_roadmaps_097_102_full_surface.py::test_102_operator_training_and_manual_surfaces -q` -> 5 passed.
* [x] Roadmap 102 CLI command flow uitgevoerd en support bundle zip-interpretatie gefixt.
* [x] `python -m pytest tests/test_roadmaps_097_102_full_surface.py tests/test_roadmap_100_paper_os_milestone_acceptance.py tests/test_roadmap_101_stabilization_acceptance.py tests/test_roadmap_102_operator_training_acceptance.py tests/test_roadmaps_076_102_paper_os.py -q` -> 25 passed.
* [x] `python -m binance_spot_bot.cli check-all --skip-tests --json` -> ok.
* [x] `python -m binance_spot_bot.cli dashboard-smoke --seconds 1` -> ok.
* [x] `python -m pytest -q` -> 387 passed, 1 warning.

Safety-resultaat:

* [x] Live trading blijft disabled.
* [x] Certification kan geen live approval claimen.
* [x] Training docs en scenario's blijven paper-only.
* [x] Support/evidence interpretatie is secret-redacted.
