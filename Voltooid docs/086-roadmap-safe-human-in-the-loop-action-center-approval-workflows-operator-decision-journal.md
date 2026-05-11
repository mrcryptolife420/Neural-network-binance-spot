# Roadmap 086 - Safe Human-in-the-Loop Action Center, Approval Workflows \& Operator Decision Journal

Status: Niet volledig voltooid / opnieuw gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/086-roadmap-safe-human-in-the-loop-action-center-approval-workflows-operator-decision-journal.md
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

Doel: Roadmap 085 maakt een lokale AI/Ops-assistent die alleen advies, context, runbook aanbevelingen en veilige commandvoorstellen geeft. Roadmap 086 bouwt daarop een **Human-in-the-Loop Action Center**: een veilige lokale approval queue waar operatoren voorgestelde acties kunnen beoordelen, goedkeuren, weigeren, documenteren en uitvoeren binnen strikte allowlists. Elke beslissing wordt opgeslagen in een operator decision journal met evidence, runbook context, command proposal, safety class, confirmation phrase en audit trail.

Live trading blijft volledig buiten scope. Het Action Center mag nooit live trading activeren, real orders plaatsen, signed endpoints gebruiken of risk limits verhogen zonder expliciete, veilige paper-only governance.

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
* \[x] Geen bestaande Roadmap 086 gevonden via repo-search.
* \[x] Roadmap 085 is lokaal aangemaakt voor Local AI Ops Assistant, natural language queries en safe operator guidance.

### Codebasecontrole

Gecontroleerde relevante modules:

* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] bestaande operatorlaag bevat al:

  * artifact catalog;
  * operator health score;
  * evidence chain;
  * environment doctor;
  * data growth budget;
  * diagnostics baseline;
  * report index;
  * support bundle verification;
  * redaction self-test;
  * local ops snapshot;
  * operator quality gate;
  * incident timeline;
  * retention preview;
  * state archive;
  * operator command manifest.
* \[x] Bestaande operator outputs zetten `live\_trading\_enabled=False`.
* \[x] Roadmap 083 definieert lokale jobs, scheduler, runbooks en allowlisted commands.
* \[x] Roadmap 085 definieert AI/Ops command proposals, guidance policy en read-only answers.

### Belangrijkste gat na Roadmap 085

Na Roadmap 085 kan de AI/Ops-assistent uitleggen wat er mis is en veilige commands voorstellen, maar nog niet:

* \[ ] proposals in een lokale approval queue plaatsen;
* \[ ] een operatorbeslissing formeel vastleggen;
* \[ ] command execution pas na bevestiging uitvoeren;
* \[ ] confirm phrases per actie afdwingen;
* \[ ] decision journal exporteren;
* \[ ] action history vergelijken met later resultaat;
* \[ ] runbook steps koppelen aan goedgekeurde acties;
* \[ ] rollback/pause/archive/compact acties onder governance uitvoeren;
* \[ ] multi-step approval workflows bouwen;
* \[ ] evidence verzamelen vóór en na actie;
* \[ ] audit trail met hashes maken.

Roadmap 086 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 086

Maak een veilig lokaal Action Center:

```text
AI/Ops suggestion
→ action proposal
→ safety classification
→ evidence/context review
→ operator approval/rejection
→ optional execution via allowlist
→ post-action verification
→ decision journal
→ audit/evidence bundle
```

Na Roadmap 086 moet de operator kunnen:

* \[ ] AI/Ops command proposals bekijken;
* \[ ] voorgestelde acties veilig classificeren;
* \[ ] required evidence zien voordat een actie wordt uitgevoerd;
* \[ ] acties goedkeuren, weigeren of parkeren;
* \[ ] confirm phrases invoeren voor confirm-required acties;
* \[ ] alleen allowlisted commands uitvoeren;
* \[ ] execution output redacted opslaan;
* \[ ] post-action verification automatisch draaien;
* \[ ] decision journal doorzoeken;
* \[ ] audit bundle exporteren;
* \[ ] nooit live trading activeren.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe AI/Ops-assistent; Roadmap 085 doet dat.
* \[ ] Geen nieuwe scheduler; Roadmap 083 doet dat.
* \[ ] Geen nieuwe governance engine; Roadmap 082 doet dat.
* \[ ] Geen live trading.
* \[ ] Geen signed order endpoints.
* \[ ] Geen Binance account endpoints.
* \[ ] Geen arbitrary shell execution.
* \[ ] Geen external telemetry.
* \[ ] Geen remote upload.
* \[ ] Geen role-based cloud auth.
* \[ ] Geen autonomous agent die acties zelf uitvoert.
* \[ ] Geen risk-verhogende auto-execution.

Wel doen:

* \[ ] action proposal schema toevoegen;
* \[ ] approval queue toevoegen;
* \[ ] decision journal toevoegen;
* \[ ] command execution alleen via bestaande allowlist;
* \[ ] confirm phrases afdwingen;
* \[ ] post-action verification toevoegen;
* \[ ] dashboard action center toevoegen;
* \[ ] CLI action center commands toevoegen;
* \[ ] evidence bundle/audit trail toevoegen.

\---

## 3\. Fase 0 - Human-in-the-Loop Action Safety Contract

Doel: vastleggen dat alle acties operator-goedgekeurd, lokaal en paper/read-only zijn.

### Nieuwe doc

```text
docs/human-in-the-loop-action-safety-contract.md
```

### Regels

* \[ ] Geen actie wordt automatisch uitgevoerd door AI.
* \[ ] Elke actie heeft safety class.
* \[ ] Elke confirm-required actie vereist exacte confirm phrase.
* \[ ] Forbidden acties worden nooit uitgevoerd.
* \[ ] Commands moeten door allowlist validator.
* \[ ] Geen live mode.
* \[ ] Geen signed order endpoint.
* \[ ] Geen account endpoint.
* \[ ] Geen secrets in action args.
* \[ ] Geen arbitrary shell.
* \[ ] Geen remote upload.
* \[ ] Geen external telemetry.
* \[ ] Risk-verlagende paper acties mogen met confirm.
* \[ ] Risk-verhogende acties worden geblokkeerd of vereisen aparte governance.
* \[ ] Elke actie krijgt decision journal entry.
* \[ ] Elke execution krijgt post-action verification.

### Acceptatiecriteria

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen dat AI nooit direct execute path kan aanroepen.
* \[ ] Tests bewijzen live/order/account actions worden geweigerd.
* \[ ] Dashboard toont `HUMAN-IN-THE-LOOP REQUIRED`.
* \[ ] Action Center toont `NO LIVE TRADING`.

\---

## 4\. Fase 1 - Action Proposal Schema

Doel: één schema voor alle voorgestelde acties.

### Nieuwe module

```text
src/binance\_spot\_bot/action\_proposals.py
```

### Dataclasses

* \[ ] `ActionProposal`
* \[ ] `ActionCommand`
* \[ ] `ActionSafetyClass`
* \[ ] `ActionPrecondition`
* \[ ] `ActionExpectedOutcome`
* \[ ] `ActionEvidenceLink`
* \[ ] `ActionRiskAssessment`
* \[ ] `ActionValidationResult`

### ActionProposal velden

* \[ ] proposal\_id;
* \[ ] created\_at\_ms;
* \[ ] source:

  * ai\_ops;
  * runbook;
  * scheduler;
  * dashboard;
  * CLI;
  * governance;
  * anomaly;
  * operator\_manual;
* \[ ] title;
* \[ ] description;
* \[ ] category:

  * diagnostics;
  * support\_bundle;
  * report;
  * evidence;
  * metrics;
  * retention;
  * scheduler;
  * runbook;
  * paper\_policy;
  * paper\_portfolio;
  * dashboard;
  * cleanup;
* \[ ] command;
* \[ ] args;
* \[ ] safety\_class:

  * read\_only;
  * safe\_generate\_artifact;
  * confirm\_required;
  * destructive\_confirm\_required;
  * paper\_risk\_reducing;
  * paper\_risk\_changing;
  * forbidden;
* \[ ] expected\_outputs;
* \[ ] required\_evidence;
* \[ ] preconditions;
* \[ ] confirm\_phrase;
* \[ ] forbidden\_reasons;
* \[ ] related\_runbook\_id;
* \[ ] related\_incident\_id;
* \[ ] related\_evidence\_ids;
* \[ ] no\_auto\_execute=true;
* \[ ] live\_trading\_enabled=false.

### Acceptatiecriteria

* \[ ] Proposal is JSON-serializable.
* \[ ] Proposal bevat geen secrets.
* \[ ] Proposal kan AI/Ops command proposal importeren.
* \[ ] Forbidden proposal kan niet approved worden.
* \[ ] Tests dekken safety classes.

\---

## 5\. Fase 2 - Action Policy \& Validator

Doel: elk voorstel valideren vóór het in de queue mag.

### Nieuwe module

```text
src/binance\_spot\_bot/action\_policy.py
```

### Validator checks

* \[ ] command staat op allowlist;
* \[ ] command bevat geen shell injection;
* \[ ] args bevatten geen secrets;
* \[ ] args bevatten geen live mode;
* \[ ] args bevatten geen order/account endpoint;
* \[ ] confirm phrase klopt bij high-risk local action;
* \[ ] required evidence bestaat;
* \[ ] runbook bestaat indien gekoppeld;
* \[ ] action category klopt;
* \[ ] output path zit binnen data dir;
* \[ ] destructive action heeft preview-first evidence;
* \[ ] paper-risk-changing action heeft governance evidence;
* \[ ] safety class is niet forbidden.

### Acceptatiecriteria

* \[ ] Validator blokkeert onbekende commands.
* \[ ] Validator blokkeert live/signed/order/account commands.
* \[ ] Validator blokkeert command injection.
* \[ ] Validator eist preview voor destructive actions.
* \[ ] Validator is testbaar zonder dashboard.

\---

## 6\. Fase 3 - Approval Queue Store

Doel: action proposals lokaal bewaren en volgen.

### Nieuwe module

```text
src/binance\_spot\_bot/approval\_queue.py
```

### Storage

```text
data/action-center/
  proposals/
  approvals/
  executions/
  decisions/
  verification/
  queue-index.json
```

### Statussen

* \[ ] proposed;
* \[ ] needs\_evidence;
* \[ ] needs\_confirmation;
* \[ ] approved;
* \[ ] rejected;
* \[ ] expired;
* \[ ] superseded;
* \[ ] executing;
* \[ ] executed;
* \[ ] verification\_failed;
* \[ ] completed;
* \[ ] archived.

### Taken

* \[ ] Save proposal.
* \[ ] Load proposal.
* \[ ] List queue.
* \[ ] Update status.
* \[ ] Expire old proposals.
* \[ ] Link decision.
* \[ ] Link execution.
* \[ ] Link verification.
* \[ ] Export queue.

### Acceptatiecriteria

* \[ ] Queue is local-only.
* \[ ] Queue bevat geen secrets.
* \[ ] Queue index heeft manifest/hash.
* \[ ] Expired proposals kunnen niet uitgevoerd worden.
* \[ ] Tests dekken status transitions.

\---

## 7\. Fase 4 - Operator Decision Journal

Doel: elke beslissing auditbaar vastleggen.

### Nieuwe module

```text
src/binance\_spot\_bot/decision\_journal.py
```

### Dataclasses

* \[ ] `OperatorDecision`
* \[ ] `DecisionReason`
* \[ ] `DecisionEvidence`
* \[ ] `DecisionOutcome`
* \[ ] `DecisionJournal`
* \[ ] `DecisionJournalExport`

### Decision velden

* \[ ] decision\_id;
* \[ ] proposal\_id;
* \[ ] operator\_id\_local;
* \[ ] decision:

  * approve;
  * reject;
  * defer;
  * request\_more\_evidence;
  * mark\_duplicate;
  * supersede;
* \[ ] reason\_text;
* \[ ] reason\_codes;
* \[ ] evidence\_links;
* \[ ] risk\_acknowledgement;
* \[ ] confirm\_phrase\_used;
* \[ ] created\_at\_ms;
* \[ ] previous\_status;
* \[ ] next\_status;
* \[ ] redacted=true;
* \[ ] live\_trading\_enabled=false.

### Acceptatiecriteria

* \[ ] Elke approval/rejection krijgt journal entry.
* \[ ] Journal is append-only.
* \[ ] Journal is secret-free.
* \[ ] Journal kan Markdown/JSON exporteren.
* \[ ] Journal entries hebben hashes.

\---

## 8\. Fase 5 - Manual Approval Workflow

Doel: veilige menselijke goedkeuring afdwingen.

### Nieuwe module

```text
src/binance\_spot\_bot/approval\_workflow.py
```

### Workflow

* \[ ] proposal submitted;
* \[ ] validation;
* \[ ] evidence check;
* \[ ] safety summary;
* \[ ] operator decision;
* \[ ] confirm phrase check;
* \[ ] queue status update;
* \[ ] journal entry;
* \[ ] execution eligibility check.

### Approval requirements per safety class

Read-only:

* \[ ] operator approval optional;
* \[ ] execution may be one-click in dashboard;
* \[ ] still journaled.

Safe artifact generation:

* \[ ] operator approval required;
* \[ ] no confirm phrase.

Confirm-required:

* \[ ] operator approval;
* \[ ] exact confirm phrase.

Destructive confirm-required:

* \[ ] preview evidence;
* \[ ] exact confirm phrase;
* \[ ] second review recommended.

Paper risk-reducing:

* \[ ] allowed with confirm;
* \[ ] evidence linked.

Paper risk-changing:

* \[ ] governance evidence required;
* \[ ] confirm phrase;
* \[ ] never live.

Forbidden:

* \[ ] no approval possible.

### Acceptatiecriteria

* \[ ] Forbidden proposals cannot be approved.
* \[ ] Confirm phrase mismatch blocks approval.
* \[ ] Missing evidence blocks approval.
* \[ ] Journal records all decisions.
* \[ ] Tests cover every safety class.

\---

## 9\. Fase 6 - Safe Action Executor

Doel: goedgekeurde acties uitvoeren, maar alleen via allowlist.

### Nieuwe module

```text
src/binance\_spot\_bot/action\_executor.py
```

### Execution rules

* \[ ] Execute only approved proposals.
* \[ ] Re-validate immediately before execution.
* \[ ] Use safe env:

  * `LIVE\_TRADING\_ENABLED=false`;
  * `KILL\_SWITCH=true`.
* \[ ] Use command allowlist from Roadmap 083.
* \[ ] No arbitrary shell.
* \[ ] Timeout required.
* \[ ] Capture stdout/stderr.
* \[ ] Redact output.
* \[ ] Store execution result.
* \[ ] Never execute forbidden actions.
* \[ ] Never execute live/order/account commands.

### ExecutionResult velden

* \[ ] execution\_id;
* \[ ] proposal\_id;
* \[ ] started\_at\_ms;
* \[ ] finished\_at\_ms;
* \[ ] status;
* \[ ] exit\_code;
* \[ ] stdout\_path;
* \[ ] stderr\_path;
* \[ ] artifacts;
* \[ ] redacted;
* \[ ] live\_trading\_enabled=false.

### Acceptatiecriteria

* \[ ] Approved safe diagnostics command executes.
* \[ ] Approved support bundle command executes.
* \[ ] Live/order/account command rejected even if approval file is tampered.
* \[ ] Output is redacted.
* \[ ] Tests use fake command runner.

\---

## 10\. Fase 7 - Post-Action Verification

Doel: na elke actie controleren of het verwachte resultaat klopt.

### Nieuwe module

```text
src/binance\_spot\_bot/action\_verification.py
```

### Verification types

* \[ ] file exists;
* \[ ] JSON status ok;
* \[ ] support bundle verify;
* \[ ] redaction self-test;
* \[ ] evidence manifest updated;
* \[ ] metrics ingested;
* \[ ] report index updated;
* \[ ] dashboard smoke result;
* \[ ] runbook step completed;
* \[ ] no-live proof;
* \[ ] no secrets found.

### VerificationResult

* \[ ] verification\_id;
* \[ ] execution\_id;
* \[ ] proposal\_id;
* \[ ] checks;
* \[ ] status:

  * pass;
  * warn;
  * fail;
  * skipped;
* \[ ] blockers;
* \[ ] warnings;
* \[ ] artifacts;
* \[ ] next\_action;
* \[ ] timestamp\_ms.

### Acceptatiecriteria

* \[ ] Verification runs after execution.
* \[ ] Failed verification updates queue status.
* \[ ] Verification can create follow-up proposal.
* \[ ] No-live proof checked.
* \[ ] Output is evidence-linked.

\---

## 11\. Fase 8 - Action Center Dashboard

Doel: operator kan voorstellen veilig bekijken, goedkeuren en uitvoeren.

### Nieuwe dashboardsectie

```text
Action Center
```

### Panels

* \[ ] queue summary;
* \[ ] proposals by status;
* \[ ] safety class badges;
* \[ ] evidence required/missing;
* \[ ] proposal detail;
* \[ ] command preview;
* \[ ] expected output;
* \[ ] related runbook;
* \[ ] related AI/Ops answer;
* \[ ] related anomaly/incident;
* \[ ] decision history;
* \[ ] execution history;
* \[ ] post-action verification;
* \[ ] decision journal;
* \[ ] audit export.

### Actions

* \[ ] approve;
* \[ ] reject;
* \[ ] defer;
* \[ ] request evidence;
* \[ ] execute approved safe action;
* \[ ] verify action;
* \[ ] export decision journal;
* \[ ] export audit bundle.

### Dashboard safeguards

* \[ ] `HUMAN-IN-THE-LOOP REQUIRED` badge.
* \[ ] `NO LIVE TRADING` badge.
* \[ ] Forbidden actions visible as blocked but not executable.
* \[ ] Confirm phrase input required.
* \[ ] Raw JSON only in debug expanders.
* \[ ] No one-click for destructive actions.

### Acceptatiecriteria

* \[ ] Browser smoke covers Action Center.
* \[ ] Dashboard cannot execute unapproved proposal.
* \[ ] Dashboard cannot approve forbidden proposal.
* \[ ] Dashboard shows no-live proof.
* \[ ] All forms/buttons have unique keys.

\---

## 12\. Fase 9 - Action Center CLI

Doel: Action Center ook via commandline gebruiken.

### Nieuwe commands

```powershell
python -m binance\_spot\_bot.cli action-propose --from-ai-session <id>
python -m binance\_spot\_bot.cli action-list
python -m binance\_spot\_bot.cli action-show --proposal-id <id>
python -m binance\_spot\_bot.cli action-approve --proposal-id <id> --confirm <PHRASE>
python -m binance\_spot\_bot.cli action-reject --proposal-id <id> --reason "not needed"
python -m binance\_spot\_bot.cli action-execute --proposal-id <id>
python -m binance\_spot\_bot.cli action-verify --proposal-id <id>
python -m binance\_spot\_bot.cli decision-journal --days 7
python -m binance\_spot\_bot.cli action-audit-export --days 30
python -m binance\_spot\_bot.cli action-safety-test
```

### Acceptatiecriteria

* \[ ] CLI commands support JSON output.
* \[ ] CLI cannot execute unapproved action.
* \[ ] CLI requires confirm phrase.
* \[ ] CLI rejects forbidden actions.
* \[ ] CLI never calls live/signed/order/account endpoints.

\---

## 13\. Fase 10 - AI/Ops Integration

Doel: Roadmap 085 proposals naar Action Center sturen.

### Integratiepunten

* \[ ] AI/Ops command proposal kan `ActionProposal` maken.
* \[ ] AI/Ops answer kan “Send to Action Center” aanbieden.
* \[ ] Runbook recommendation kan proposal maken voor eerste veilige command.
* \[ ] Forbidden AI/Ops intent kan geen proposal maken.
* \[ ] Prompt injection suspicious sources worden gemarkeerd in proposal evidence.
* \[ ] Context pack manifest wordt aan proposal gekoppeld.

### Acceptatiecriteria

* \[ ] AI/Ops kan alleen proposal maken, niet uitvoeren.
* \[ ] Proposal behoudt source/session/evidence.
* \[ ] Unsafe AI output wordt door validator geblokkeerd.
* \[ ] Dashboard toont AI/Ops source.
* \[ ] Tests gebruiken fake AI/Ops session.

\---

## 14\. Fase 11 - Runbook Step Approvals

Doel: runbooks kunnen stap voor stap worden afgewerkt via approvals.

### Nieuwe module

```text
src/binance\_spot\_bot/runbook\_action\_workflow.py
```

### Functionaliteit

* \[ ] runbook step → action proposal;
* \[ ] step preconditions;
* \[ ] step approval;
* \[ ] step execution;
* \[ ] step verification;
* \[ ] step completion journal;
* \[ ] runbook completion evidence.

### Acceptatiecriteria

* \[ ] Runbook steps can be proposed as actions.
* \[ ] Steps with destructive commands require confirm.
* \[ ] Completion is journaled.
* \[ ] Runbook evidence can be exported.
* \[ ] No live actions.

\---

## 15\. Fase 12 - Multi-Step Approval Plans

Doel: grotere workflows veilig opdelen.

### Nieuwe module

```text
src/binance\_spot\_bot/approval\_plans.py
```

### Plan types

* \[ ] dashboard recovery plan;
* \[ ] failed scheduled report plan;
* \[ ] support bundle + verify plan;
* \[ ] metrics compaction plan;
* \[ ] evidence rebuild plan;
* \[ ] paper policy rollback plan;
* \[ ] local scheduler install plan;
* \[ ] retention archive plan.

### Plan status

* \[ ] draft;
* \[ ] waiting\_for\_approval;
* \[ ] partially\_approved;
* \[ ] running;
* \[ ] paused;
* \[ ] completed;
* \[ ] failed;
* \[ ] canceled.

### Acceptatiecriteria

* \[ ] Plan consists of ordered proposals.
* \[ ] Each step has its own approval/verification.
* \[ ] Failure pauses remaining steps.
* \[ ] Plan can be exported.
* \[ ] No plan can include forbidden action.

\---

## 16\. Fase 13 - Local Operator Identity \& Roles

Doel: lokale audit trail verbeteren zonder cloud auth.

### Nieuwe module

```text
src/binance\_spot\_bot/local\_operator\_identity.py
```

### Identity fields

* \[ ] operator\_id;
* \[ ] display\_name;
* \[ ] local\_machine\_id hash;
* \[ ] role:

  * viewer;
  * operator;
  * maintainer;
  * admin\_local;
* \[ ] created\_at\_ms;
* \[ ] last\_seen\_ms.

### Role permissions

Viewer:

* \[ ] view queue;
* \[ ] view journal.

Operator:

* \[ ] approve read-only/safe artifact actions.
* \[ ] reject/defer proposals.

Maintainer:

* \[ ] approve confirm-required local maintenance.
* \[ ] execute approved local jobs.

Admin local:

* \[ ] install scheduler tasks.
* \[ ] destructive confirm-required local archive/compact actions.

Forbidden for all:

* \[ ] live trading;
* \[ ] signed orders;
* \[ ] account endpoints;
* \[ ] secrets reveal.

### Acceptatiecriteria

* \[ ] Roles are local-only.
* \[ ] No cloud auth.
* \[ ] Role cannot override forbidden actions.
* \[ ] Decision journal records operator\_id.
* \[ ] Tests cover permission boundaries.

\---

## 17\. Fase 14 - Action Audit Bundle

Doel: alle actiegeschiedenis exporteerbaar en verifieerbaar maken.

### Nieuwe module

```text
src/binance\_spot\_bot/action\_audit\_bundle.py
```

### Bundle bevat

* \[ ] proposals;
* \[ ] validation results;
* \[ ] approvals/rejections;
* \[ ] decision journal;
* \[ ] executions;
* \[ ] stdout/stderr redacted;
* \[ ] verification results;
* \[ ] related runbooks;
* \[ ] AI/Ops sessions;
* \[ ] evidence manifests;
* \[ ] no-live proof;
* \[ ] redaction proof;
* \[ ] hashes.

### Output

```text
data/action-center/audit-bundles/<bundle\_id>/
  action\_audit\_manifest.json
  action\_audit\_summary.md
  files/
```

### Acceptatiecriteria

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Dashboard/CLI export works.
* \[ ] Bundle supports incident review.

\---

## 18\. Fase 15 - Decision Outcome Analytics

Doel: meten of goedgekeurde acties echt hielpen.

### Nieuwe module

```text
src/binance\_spot\_bot/decision\_outcome\_analytics.py
```

### Metrics

* \[ ] proposals created;
* \[ ] approvals;
* \[ ] rejections;
* \[ ] average time to approve;
* \[ ] execution success rate;
* \[ ] verification pass rate;
* \[ ] repeated failed proposals;
* \[ ] actions by category;
* \[ ] actions by source;
* \[ ] runbook completion rate;
* \[ ] safety blocks;
* \[ ] forbidden action attempts;
* \[ ] unresolved proposals;
* \[ ] stale approvals.

### Acceptatiecriteria

* \[ ] Metrics export to Roadmap 084 metrics warehouse.
* \[ ] Dashboard shows outcome analytics.
* \[ ] Failed verification triggers follow-up proposal.
* \[ ] Safety blocks are counted.
* \[ ] No secrets in metrics.

\---

## 19\. Fase 16 - Action Center Reports

Doel: periodieke rapporten over operatorbeslissingen.

### Nieuwe module

```text
src/binance\_spot\_bot/action\_center\_report.py
```

### Reports

Daily:

* \[ ] proposals opened;
* \[ ] decisions made;
* \[ ] executions run;
* \[ ] failed verifications;
* \[ ] forbidden requests blocked;
* \[ ] unresolved proposals;
* \[ ] top next actions.

Weekly:

* \[ ] operator decision summary;
* \[ ] action effectiveness;
* \[ ] runbook usage;
* \[ ] recurring problems;
* \[ ] audit gaps;
* \[ ] suggested process improvements.

### Acceptatiecriteria

* \[ ] Reports are secret-free.
* \[ ] Reports link to journal/audit bundle.
* \[ ] Reports can be scheduled by Roadmap 083 scheduler.
* \[ ] Reports feed Roadmap 084 metrics.

\---

## 20\. Fase 17 - Tests

### Unit tests

* \[ ] `tests/test\_action\_proposals.py`
* \[ ] `tests/test\_action\_policy.py`
* \[ ] `tests/test\_approval\_queue.py`
* \[ ] `tests/test\_decision\_journal.py`
* \[ ] `tests/test\_approval\_workflow.py`
* \[ ] `tests/test\_action\_executor.py`
* \[ ] `tests/test\_action\_verification.py`
* \[ ] `tests/test\_action\_center\_cli.py`
* \[ ] `tests/test\_ai\_ops\_action\_integration.py`
* \[ ] `tests/test\_runbook\_action\_workflow.py`
* \[ ] `tests/test\_approval\_plans.py`
* \[ ] `tests/test\_local\_operator\_identity.py`
* \[ ] `tests/test\_action\_audit\_bundle.py`
* \[ ] `tests/test\_decision\_outcome\_analytics.py`
* \[ ] `tests/test\_action\_center\_report.py`

### Integration tests

* \[ ] AI/Ops creates safe diagnostics proposal.
* \[ ] Operator approves proposal.
* \[ ] Action executes with fake runner.
* \[ ] Verification passes.
* \[ ] Decision journal export works.
* \[ ] Runbook step creates proposal.
* \[ ] Multi-step plan pauses on failure.
* \[ ] Audit bundle export verifies.
* \[ ] Outcome metrics are generated.

### Safety tests

* \[ ] Live proposal rejected.
* \[ ] Order proposal rejected.
* \[ ] Account query proposal rejected.
* \[ ] Secret reveal proposal rejected.
* \[ ] Shell injection rejected.
* \[ ] Unapproved proposal cannot execute.
* \[ ] Tampered approved proposal re-validates and fails.
* \[ ] Destructive action requires preview + confirm.
* \[ ] Output is redacted.
* \[ ] No-live proof remains true.

\---

## 21\. Docs

Nieuwe docs:

* \[ ] `docs/human-in-the-loop-action-safety-contract.md`
* \[ ] `docs/action-proposal-schema.md`
* \[ ] `docs/action-policy-validator.md`
* \[ ] `docs/approval-queue.md`
* \[ ] `docs/operator-decision-journal.md`
* \[ ] `docs/manual-approval-workflow.md`
* \[ ] `docs/safe-action-executor.md`
* \[ ] `docs/post-action-verification.md`
* \[ ] `docs/action-center-dashboard.md`
* \[ ] `docs/action-center-cli.md`
* \[ ] `docs/ai-ops-action-center-integration.md`
* \[ ] `docs/runbook-step-approvals.md`
* \[ ] `docs/multi-step-approval-plans.md`
* \[ ] `docs/local-operator-identity-roles.md`
* \[ ] `docs/action-audit-bundle.md`
* \[ ] `docs/decision-outcome-analytics.md`

README updates:

* \[ ] Action Center overview.
* \[ ] Approval queue commands.
* \[ ] Decision journal.
* \[ ] Safe execution rules.
* \[ ] No-live statement.
* \[ ] Examples of allowed/confirm/forbidden actions.

\---

## 22\. CLI command examples

### Propose action from AI/Ops

```powershell
python -m binance\_spot\_bot.cli action-propose --from-ai-session latest
```

### Show queue

```powershell
python -m binance\_spot\_bot.cli action-list --json
```

### Approve action

```powershell
python -m binance\_spot\_bot.cli action-approve --proposal-id abc123 --confirm CREATE\_SUPPORT\_BUNDLE
```

### Execute approved action

```powershell
python -m binance\_spot\_bot.cli action-execute --proposal-id abc123
```

### Verify action

```powershell
python -m binance\_spot\_bot.cli action-verify --proposal-id abc123
```

### Export decision journal

```powershell
python -m binance\_spot\_bot.cli decision-journal --days 7
```

### Export audit bundle

```powershell
python -m binance\_spot\_bot.cli action-audit-export --days 30
```

\---

## 23\. Codex bouwvolgorde

### PR 1 - Action Proposal Schema + Policy Validator

* \[ ] `action\_proposals.py`
* \[ ] `action\_policy.py`
* \[ ] safety classes
* \[ ] tests for forbidden/live/shell injection

### PR 2 - Approval Queue Store

* \[ ] `approval\_queue.py`
* \[ ] status transitions
* \[ ] queue index
* \[ ] tests

### PR 3 - Decision Journal

* \[ ] `decision\_journal.py`
* \[ ] append-only journal
* \[ ] Markdown/JSON export
* \[ ] tests

### PR 4 - Manual Approval Workflow

* \[ ] approval rules by safety class
* \[ ] confirm phrase checks
* \[ ] evidence checks
* \[ ] tests

### PR 5 - Safe Action Executor

* \[ ] allowlist command runner
* \[ ] safe env
* \[ ] redacted output
* \[ ] fake runner tests

### PR 6 - Post-Action Verification

* \[ ] verification checks
* \[ ] no-live proof
* \[ ] support bundle verify
* \[ ] tests

### PR 7 - Action Center CLI

* \[ ] propose/list/show/approve/reject/execute/verify/journal/export
* \[ ] JSON output
* \[ ] safety tests

### PR 8 - Dashboard Action Center

* \[ ] queue UI
* \[ ] approval form
* \[ ] execution/verification view
* \[ ] browser smoke

### PR 9 - AI/Ops + Runbook Integration

* \[ ] AI/Ops proposals
* \[ ] runbook step workflows
* \[ ] multi-step approval plans
* \[ ] tests

### PR 10 - Identity + Audit + Analytics + Docs

* \[ ] local operator identity
* \[ ] audit bundle
* \[ ] outcome analytics
* \[ ] reports
* \[ ] docs

\---

## 24\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 086 PR 1: Action Proposal Schema + Policy Validator.

Maak src/binance\_spot\_bot/action\_proposals.py met:
- ActionProposal
- ActionCommand
- ActionSafetyClass
- ActionPrecondition
- ActionExpectedOutcome
- ActionEvidenceLink
- ActionRiskAssessment
- ActionValidationResult

Maak src/binance\_spot\_bot/action\_policy.py met een validator die proposals controleert op:
- allowlisted command
- geen live mode
- geen signed/order/account endpoint
- geen shell injection
- geen secrets in args
- output path binnen data dir
- destructive actions vereisen preview evidence
- forbidden actions kunnen nooit approved worden

Gebruik bestaande redaction helpers.
Gebruik de command allowlist uit Roadmap 083 als concept.
Voeg tests toe voor:
- safe diagnostics proposal
- safe support bundle proposal
- reject live trading proposal
- reject order/account proposal
- reject shell injection
- reject secret args
- reject forbidden safety class
- proposal serialization is secret-free

Geen executor bouwen in deze PR.
Geen dashboard bouwen in deze PR.
Geen API calls.
Geen signed endpoints.
Geen orders.
Geen live trading.
```

Waarom eerst:

* Zonder action proposal schema en validator is approval/execution onveilig.
* Het bouwt direct verder op Roadmap 085 command proposals.
* Het raakt geen trading runtime.
* Het is klein genoeg voor Codex.
* Safety kan meteen hard getest worden.

\---

## 25\. Definition of Done

Roadmap 086 is klaar als:

* \[ ] Human-in-the-Loop Action Safety Contract bestaat.
* \[ ] Action Proposal Schema werkt.
* \[ ] Action Policy \& Validator werkt.
* \[ ] Approval Queue Store werkt.
* \[ ] Operator Decision Journal werkt.
* \[ ] Manual Approval Workflow werkt.
* \[ ] Safe Action Executor werkt.
* \[ ] Post-Action Verification werkt.
* \[ ] Action Center Dashboard werkt.
* \[ ] Action Center CLI werkt.
* \[ ] AI/Ops Integration werkt.
* \[ ] Runbook Step Approvals werken.
* \[ ] Multi-Step Approval Plans werken.
* \[ ] Local Operator Identity \& Roles werken.
* \[ ] Action Audit Bundle werkt.
* \[ ] Decision Outcome Analytics werkt.
* \[ ] Action Center Reports werken.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen unapproved actions niet kunnen uitvoeren.
* \[ ] Tests bewijzen forbidden actions niet approved kunnen worden.
* \[ ] Outputs/reports/bundles zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 086 kan na uitvoering naar `Voltooid docs`.

\---

## 26\. Verwachte Roadmap 087 daarna

Na Roadmap 086 zou Roadmap 087 logisch focussen op:

```text
Roadmap 087 - Local Permission Profiles, Operator Roles Hardening \& Audit-Grade Compliance Reports
```

Mogelijke inhoud:

* \[ ] local permission profiles;
* \[ ] stronger role boundaries;
* \[ ] audit-grade compliance reports;
* \[ ] separation between viewer/operator/maintainer/admin;
* \[ ] approval policy templates;
* \[ ] decision retention policies;
* \[ ] compliance evidence packs;
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

Gebouwd: action proposals, action policy, approval queue, decision journal, approval workflow, action executor, action verification, runbook action workflow, approval plans, local operator identity, audit bundle, outcome analytics, action center report, dashboardtab `Action Center`, CLI smoke via `action-center-propose`.

Validatie: `tests/test_roadmaps_083_088_full_surface.py`, `tests/test_roadmaps_082_088_ops_governance.py`, dashboard-smoke en CLI smoke.

Safety: human approval required, local safe actions only, no live trading.

