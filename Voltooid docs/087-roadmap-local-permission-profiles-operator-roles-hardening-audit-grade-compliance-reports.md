# Roadmap 087 - Local Permission Profiles, Operator Roles Hardening \& Audit-Grade Compliance Reports

Status: Niet volledig voltooid / opnieuw gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/087-roadmap-local-permission-profiles-operator-roles-hardening-audit-grade-compliance-reports.md
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

Doel: Roadmap 086 maakt een Human-in-the-Loop Action Center met approval queue, action proposals, decision journal, safe execution en post-action verification. Roadmap 087 hardent de lokale autorisatielaag daarom verder: permission profiles, operator roles, role-based approval policies, separation of duties, compliance-style evidence packs, audit-grade reports, permission drift detection en role-aware dashboard/CLI. Alles blijft lokaal, paper-only en zonder live trading.

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
* \[x] Geen bestaande Roadmap 087 gevonden via repo-search.
* \[x] Roadmap 086 is lokaal aangemaakt voor Human-in-the-Loop Action Center en decision journal.

### Codebasecontrole

Gecontroleerde relevante modules:

* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] `src/binance\_spot\_bot/security.py`
* \[x] `src/binance\_spot\_bot/redaction.py`

Bestaande basis:

* \[x] `operator\_ops.py` bevat lokale operatorfuncties:

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
* \[x] `security.py` bevat `scan\_for\_secrets(...)` met secret regexes voor Binance/OpenAI-like secrets, signatures, listenKeys en token-achtige strings.
* \[x] `redaction.py` bevat redaction voor strings, JSON secret fields en payloads.
* \[x] Bestaande operator outputs zetten `live\_trading\_enabled=False`.

### Belangrijkste gat na Roadmap 086

Na Roadmap 086 zijn approvals en decisions auditbaar, maar nog niet strak genoeg geregeld:

* \[ ] wie welke actie mag goedkeuren;
* \[ ] wie approval policies mag wijzigen;
* \[ ] wie destructive local actions mag uitvoeren;
* \[ ] wie paper-risk-changing actions mag goedkeuren;
* \[ ] of één persoon zowel proposal als approval als execution mag doen;
* \[ ] of permission changes zelf auditbaar zijn;
* \[ ] of compliance reports aantonen dat live trading disabled bleef;
* \[ ] of forbidden action attempts meetbaar zijn;
* \[ ] of permissions drift detecteerbaar is;
* \[ ] of role profiles exporteerbaar en reproduceerbaar zijn.

Roadmap 087 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 087

Maak een lokale permission en compliance-laag:

```text
Action Center
→ local operator identity
→ permission profiles
→ role-based approval policy
→ separation of duties
→ permission drift detection
→ compliance evidence
→ audit-grade reports
```

Na Roadmap 087 moet de bot kunnen:

* \[ ] lokale operator roles definiëren;
* \[ ] permission profiles per role toepassen;
* \[ ] action approvals role-aware maken;
* \[ ] separation of duties afdwingen;
* \[ ] permission changes journalen;
* \[ ] compliance reports genereren;
* \[ ] forbidden action attempts rapporteren;
* \[ ] decision journal auditen;
* \[ ] no-live evidence bewijzen;
* \[ ] alle reports secret-free exporteren.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen cloud identity provider.
* \[ ] Geen online login-systeem.
* \[ ] Geen external telemetry.
* \[ ] Geen live trading.
* \[ ] Geen signed order endpoints.
* \[ ] Geen Binance account endpoints.
* \[ ] Geen real-money permissions.
* \[ ] Geen remote policy management.
* \[ ] Geen automatisch uitvoeren van AI-acties.
* \[ ] Geen volledige enterprise IAM bouwen.

Wel doen:

* \[ ] lokale permission profiles bouwen;
* \[ ] lokale operator identity hardenen;
* \[ ] role-based approval policies toevoegen;
* \[ ] Action Center integreren met roles;
* \[ ] compliance reports maken;
* \[ ] permission drift detecteren;
* \[ ] audit bundles uitbreiden;
* \[ ] alles local-only, redacted en no-live houden.

\---

## 3\. Fase 0 - Permission \& Compliance Safety Contract

Doel: vastleggen dat permissions nooit live trading kunnen vrijzetten.

### Nieuwe doc

```text
docs/local-permission-compliance-safety-contract.md
```

### Regels

* \[ ] Roles gelden alleen lokaal.
* \[ ] Roles kunnen forbidden actions niet toestaan.
* \[ ] Geen enkele role kan live trading activeren.
* \[ ] Geen enkele role kan signed order endpoints toestaan.
* \[ ] Geen enkele role kan account endpoints toestaan.
* \[ ] Permission profiles mogen risk alleen binnen paper/governance aanpassen.
* \[ ] Permission changes zijn zelf approval-required.
* \[ ] Policy changes krijgen journal entry.
* \[ ] Destructive local actions vereisen preview + confirm.
* \[ ] Paper-risk-changing actions vereisen governance evidence.
* \[ ] All compliance exports zijn redacted.
* \[ ] Compliance reports bevatten no-live proof.

### Acceptatiecriteria

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen admin\_local kan live niet activeren.
* \[ ] Tests bewijzen forbidden actions blijven forbidden.
* \[ ] Dashboard toont `LOCAL PERMISSIONS ONLY`.
* \[ ] Compliance report toont no-live bewijs.

\---

## 4\. Fase 1 - Local Operator Identity V2

Doel: Roadmap 086 identity uitbreiden tot stabiele lokale operatoridentiteit.

### Nieuwe of uit te breiden module

```text
src/binance\_spot\_bot/local\_operator\_identity.py
```

### Dataclasses

* \[ ] `LocalOperatorIdentity`
* \[ ] `LocalOperatorProfile`
* \[ ] `LocalOperatorSession`
* \[ ] `LocalOperatorDevice`
* \[ ] `LocalOperatorIdentityStore`

### Identity velden

* \[ ] operator\_id;
* \[ ] display\_name;
* \[ ] role\_ids;
* \[ ] local\_machine\_id\_hash;
* \[ ] profile\_hash;
* \[ ] created\_at\_ms;
* \[ ] updated\_at\_ms;
* \[ ] last\_seen\_ms;
* \[ ] disabled;
* \[ ] notes;
* \[ ] live\_trading\_enabled=false.

### Local identity rules

* \[ ] Default operator wordt lokaal aangemaakt.
* \[ ] Geen secrets in identity store.
* \[ ] Machine ID wordt gehasht.
* \[ ] Identity changes worden gejournaled.
* \[ ] Disabled operator kan niet approven.
* \[ ] Unknown operator krijgt viewer permissions.

### Acceptatiecriteria

* \[ ] Identity store werkt local-only.
* \[ ] Geen secrets in identity store.
* \[ ] Disabled operator kan geen action approve.
* \[ ] Unknown operator is viewer.
* \[ ] Tests dekken create/update/disable.

\---

## 5\. Fase 2 - Permission Profile Schema

Doel: rechten declaratief vastleggen.

### Nieuwe module

```text
src/binance\_spot\_bot/permission\_profiles.py
```

### Dataclasses

* \[ ] `PermissionProfile`
* \[ ] `PermissionRule`
* \[ ] `PermissionScope`
* \[ ] `PermissionDecision`
* \[ ] `PermissionProfileManifest`

### Permission scopes

* \[ ] view\_dashboard;
* \[ ] view\_reports;
* \[ ] view\_metrics;
* \[ ] view\_evidence;
* \[ ] ask\_ai\_ops;
* \[ ] create\_action\_proposal;
* \[ ] approve\_read\_only;
* \[ ] approve\_safe\_artifact;
* \[ ] approve\_confirm\_required;
* \[ ] approve\_destructive\_local;
* \[ ] approve\_paper\_risk\_reducing;
* \[ ] approve\_paper\_risk\_changing;
* \[ ] execute\_approved\_action;
* \[ ] verify\_action;
* \[ ] manage\_scheduler;
* \[ ] manage\_runbooks;
* \[ ] manage\_policies;
* \[ ] export\_audit\_bundle;
* \[ ] manage\_permissions;
* \[ ] manage\_retention;
* \[ ] install\_local\_scheduler;
* \[ ] view\_security\_findings.

Forbidden global scopes:

* \[ ] enable\_live\_trading;
* \[ ] signed\_order\_endpoint;
* \[ ] account\_endpoint;
* \[ ] reveal\_secrets;
* \[ ] arbitrary\_shell;
* \[ ] remote\_upload;

### Acceptatiecriteria

* \[ ] Permission profiles zijn JSON-serializable.
* \[ ] Forbidden scopes kunnen niet toegestaan worden.
* \[ ] Profile manifest heeft hash.
* \[ ] Tests dekken invalid permissions.
* \[ ] Profiles zijn secret-free.

\---

## 6\. Fase 3 - Default Role Templates

Doel: veilige standaardrollen aanbieden.

### Nieuwe module

```text
src/binance\_spot\_bot/operator\_roles.py
```

### Default roles

#### Viewer

* \[ ] view dashboard;
* \[ ] view reports;
* \[ ] view metrics;
* \[ ] view evidence summaries;
* \[ ] no actions.

#### Operator

* \[ ] create action proposals;
* \[ ] approve read-only actions;
* \[ ] approve safe artifact generation;
* \[ ] execute approved read-only/safe artifact actions;
* \[ ] complete runbook steps.

#### Maintainer

* \[ ] operator permissions;
* \[ ] approve confirm-required local actions;
* \[ ] manage scheduler;
* \[ ] manage runbooks;
* \[ ] manage retention preview/archive;
* \[ ] verify support bundles.

#### Governance Reviewer

* \[ ] view policy governance;
* \[ ] approve paper policy governance actions;
* \[ ] approve paper-risk-reducing actions;
* \[ ] review weekly governance reports;
* \[ ] cannot execute local maintenance unless also maintainer.

#### Admin Local

* \[ ] manage local profiles;
* \[ ] manage permission profiles;
* \[ ] install/uninstall local scheduler;
* \[ ] export audit bundles;
* \[ ] cannot override forbidden actions.

### Acceptatiecriteria

* \[ ] Default roles are conservative.
* \[ ] Admin local cannot enable live.
* \[ ] Role templates have hashes.
* \[ ] Role changes are journaled.
* \[ ] Docs explain each role.

\---

## 7\. Fase 4 - Permission Evaluation Engine

Doel: elke action/approval/exec checken tegen roles.

### Nieuwe module

```text
src/binance\_spot\_bot/permission\_engine.py
```

### Core functies

* \[ ] `evaluate\_permission(operator, scope, resource)`
* \[ ] `can\_view(operator, resource)`
* \[ ] `can\_create\_proposal(operator, proposal)`
* \[ ] `can\_approve(operator, proposal)`
* \[ ] `can\_execute(operator, proposal)`
* \[ ] `can\_verify(operator, execution)`
* \[ ] `can\_manage\_permission(operator, target)`
* \[ ] `explain\_denial(...)`

### Decision output

* \[ ] allowed;
* \[ ] reason;
* \[ ] missing\_scope;
* \[ ] forbidden\_scope;
* \[ ] operator\_id;
* \[ ] role\_ids;
* \[ ] resource\_id;
* \[ ] safety\_class;
* \[ ] live\_trading\_enabled=false.

### Acceptatiecriteria

* \[ ] Permission engine denies by default.
* \[ ] Forbidden scopes always denied.
* \[ ] Denials are explainable.
* \[ ] Decisions are redacted.
* \[ ] Tests cover all default roles.

\---

## 8\. Fase 5 - Separation of Duties

Doel: één operator mag niet alles alleen kunnen bij gevoelige acties.

### Nieuwe module

```text
src/binance\_spot\_bot/separation\_of\_duties.py
```

### Rules

* \[ ] proposer cannot approve own destructive action.
* \[ ] proposer cannot approve own paper-risk-changing action.
* \[ ] approver and executor can be same only for low-risk actions.
* \[ ] permission profile changes require admin\_local plus second confirmation if available.
* \[ ] audit export can be done by admin\_local or maintainer.
* \[ ] forbidden actions cannot be approved by anyone.
* \[ ] emergency local stop/paper risk reduction may allow same operator with journal entry.

### Acceptatiecriteria

* \[ ] SoD rules apply to approval workflow.
* \[ ] Violations are journaled.
* \[ ] Emergency paper risk reduction remains possible.
* \[ ] Tests cover self-approval block.
* \[ ] Dashboard explains SoD blocker.

\---

## 9\. Fase 6 - Approval Policy Templates

Doel: Action Center approvalregels configureren per action type.

### Nieuwe module

```text
src/binance\_spot\_bot/approval\_policy\_templates.py
```

### Templates

* \[ ] default\_strict;
* \[ ] solo\_local\_safe;
* \[ ] maintenance\_mode;
* \[ ] governance\_review;
* \[ ] emergency\_paper\_risk\_reduction;
* \[ ] audit\_only.

### Per template

* \[ ] required role;
* \[ ] required confirm phrase;
* \[ ] required evidence;
* \[ ] separation-of-duties rule;
* \[ ] max action age;
* \[ ] post-action verification required;
* \[ ] audit bundle required;
* \[ ] scheduler allowed yes/no.

### Acceptatiecriteria

* \[ ] Templates are JSON-serializable.
* \[ ] Strict is default.
* \[ ] Templates cannot allow forbidden actions.
* \[ ] Template changes are journaled.
* \[ ] Tests cover template validation.

\---

## 10\. Fase 7 - Permission Change Workflow

Doel: role/profile wijzigingen zelf veilig goedkeuren.

### Nieuwe module

```text
src/binance\_spot\_bot/permission\_change\_workflow.py
```

### Workflow

* \[ ] propose permission change;
* \[ ] diff current vs proposed;
* \[ ] validate forbidden scopes absent;
* \[ ] require admin\_local approval;
* \[ ] require confirm phrase;
* \[ ] journal decision;
* \[ ] write new profile;
* \[ ] verify profile manifest;
* \[ ] create audit event.

### Output

* \[ ] permission change proposal;
* \[ ] permission diff;
* \[ ] validation result;
* \[ ] decision journal entry;
* \[ ] updated manifest;
* \[ ] rollback file.

### Acceptatiecriteria

* \[ ] Permission changes require approval.
* \[ ] Forbidden scopes blocked.
* \[ ] Rollback possible.
* \[ ] Diff is human-readable.
* \[ ] Tests cover malicious profile.

\---

## 11\. Fase 8 - Permission Drift Detection

Doel: detecteren als permissions onverwacht veranderen.

### Nieuwe module

```text
src/binance\_spot\_bot/permission\_drift.py
```

### Drift checks

* \[ ] profile hash changed;
* \[ ] role template changed;
* \[ ] forbidden scope appears;
* \[ ] operator role added;
* \[ ] disabled operator re-enabled;
* \[ ] approval policy changed;
* \[ ] local identity changed;
* \[ ] missing permission manifest;
* \[ ] stale permission review.

### Status

* \[ ] ok;
* \[ ] warning;
* \[ ] critical;
* \[ ] blocked.

### Acceptatiecriteria

* \[ ] Drift report can run offline.
* \[ ] Critical drift blocks sensitive approvals.
* \[ ] Drift is dashboard-ready.
* \[ ] Drift report is evidence-linked.
* \[ ] Tests cover tampered profile.

\---

## 12\. Fase 9 - Role-Aware Action Center Integration

Doel: Roadmap 086 Action Center roles laten afdwingen.

### Integratie

* \[ ] Proposal list filtered by view permission.
* \[ ] Approval button disabled without permission.
* \[ ] Execute button disabled without permission.
* \[ ] Verify button disabled without permission.
* \[ ] Destructive actions show required role.
* \[ ] SoD blocker shown.
* \[ ] Permission decision shown in detail panel.
* \[ ] Journal records operator role/profile hash.

### Acceptatiecriteria

* \[ ] Viewer cannot approve.
* \[ ] Operator cannot approve destructive local action.
* \[ ] Maintainer can approve local maintenance if policy permits.
* \[ ] Governance reviewer can approve paper governance action.
* \[ ] Admin cannot override forbidden action.
* \[ ] Browser smoke covers role-aware panel.

\---

## 13\. Fase 10 - Compliance Evidence Model

Doel: audit-grade reports baseren op vaste evidence types.

### Nieuwe module

```text
src/binance\_spot\_bot/compliance\_evidence.py
```

### Evidence types

* \[ ] no\_live\_proof;
* \[ ] check\_all\_result;
* \[ ] browser\_smoke\_result;
* \[ ] redaction\_self\_test;
* \[ ] secret\_scan\_result;
* \[ ] permission\_manifest;
* \[ ] role\_manifest;
* \[ ] approval\_policy\_manifest;
* \[ ] decision\_journal;
* \[ ] action\_audit\_bundle;
* \[ ] support\_bundle\_verify;
* \[ ] evidence\_chain;
* \[ ] operator\_health\_score;
* \[ ] permission\_drift\_report;
* \[ ] forbidden\_action\_attempts;
* \[ ] compliance\_report\_hash.

### Acceptatiecriteria

* \[ ] Evidence model is typed.
* \[ ] Required evidence can be checked.
* \[ ] Missing evidence creates blocker.
* \[ ] Evidence links are hashed.
* \[ ] Evidence is secret-free.

\---

## 14\. Fase 11 - Audit-Grade Compliance Report

Doel: een sterk rapport maken over local ops, permissions en no-live.

### Nieuwe module

```text
src/binance\_spot\_bot/compliance\_report.py
```

### Reports

Daily/weekly/monthly optional:

```text
data/compliance/
  YYYY-MM-DD/
    compliance\_report.md
    compliance\_report.json
    compliance\_evidence\_manifest.json
```

### Report secties

* \[ ] summary;
* \[ ] no-live proof;
* \[ ] operator roles;
* \[ ] permission profiles;
* \[ ] permission changes;
* \[ ] approval statistics;
* \[ ] action execution statistics;
* \[ ] forbidden action attempts;
* \[ ] redaction test status;
* \[ ] secret scan status;
* \[ ] check-all status;
* \[ ] browser smoke status;
* \[ ] evidence chain status;
* \[ ] support bundle verification;
* \[ ] permission drift status;
* \[ ] open blockers;
* \[ ] recommended actions;
* \[ ] compliance grade.

### Acceptatiecriteria

* \[ ] Report is secret-free.
* \[ ] Report links to evidence.
* \[ ] Report includes no-live proof.
* \[ ] Report can be verified by manifest.
* \[ ] Dashboard can download report.

\---

## 15\. Fase 12 - Compliance Scoring

Doel: snel zien of operator governance gezond is.

### Nieuwe module

```text
src/binance\_spot\_bot/compliance\_score.py
```

### Score categories

* \[ ] live safety;
* \[ ] permission integrity;
* \[ ] approval discipline;
* \[ ] evidence completeness;
* \[ ] redaction/security;
* \[ ] operator health;
* \[ ] report freshness;
* \[ ] action verification;
* \[ ] drift status.

### Grades

* \[ ] A: strong;
* \[ ] B: acceptable;
* \[ ] C: watch;
* \[ ] D: weak;
* \[ ] F: blocked.

### Hard blockers

* \[ ] live enabled;
* \[ ] forbidden scope allowed;
* \[ ] secret scan finding;
* \[ ] redaction self-test failed;
* \[ ] action executed without approval;
* \[ ] decision journal missing;
* \[ ] permission drift critical;
* \[ ] support bundle not redacted.

### Acceptatiecriteria

* \[ ] Score explains penalties.
* \[ ] Hard blockers force F/blocked.
* \[ ] Score is dashboard-ready.
* \[ ] Tests cover hard blockers.
* \[ ] No-live proof included.

\---

## 16\. Fase 13 - Compliance Dashboard Panel

Doel: compliance en permissions begrijpelijk zichtbaar maken.

### Nieuwe dashboardsectie

```text
Permissions \& Compliance
```

### Panels

* \[ ] current operator;
* \[ ] role/profile;
* \[ ] permission summary;
* \[ ] pending permission changes;
* \[ ] permission drift status;
* \[ ] approval policy template;
* \[ ] separation of duties status;
* \[ ] compliance score;
* \[ ] no-live proof;
* \[ ] secret scan status;
* \[ ] redaction self-test;
* \[ ] decision journal summary;
* \[ ] action audit status;
* \[ ] compliance report downloads.

### Actions

* \[ ] view role profile;
* \[ ] propose permission change;
* \[ ] approve permission change if allowed;
* \[ ] run permission drift check;
* \[ ] run compliance report;
* \[ ] export compliance bundle;
* \[ ] run redaction self-test;
* \[ ] run secret scan.

### Acceptatiecriteria

* \[ ] Dashboard shows `LOCAL PERMISSIONS ONLY`.
* \[ ] Dashboard shows `NO LIVE TRADING`.
* \[ ] Viewer cannot see secret-like raw fields.
* \[ ] Browser smoke covers panel.
* \[ ] All widgets have stable keys.

\---

## 17\. Fase 14 - Permission \& Compliance CLI

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli operator-identity
python -m binance\_spot\_bot.cli permission-profiles
python -m binance\_spot\_bot.cli permission-check --scope approve\_confirm\_required
python -m binance\_spot\_bot.cli permission-change-propose --file proposed-profile.json
python -m binance\_spot\_bot.cli permission-change-approve --change-id <id> --confirm PERMISSION\_CHANGE
python -m binance\_spot\_bot.cli permission-drift-check
python -m binance\_spot\_bot.cli compliance-evidence-check
python -m binance\_spot\_bot.cli compliance-report
python -m binance\_spot\_bot.cli compliance-score
python -m binance\_spot\_bot.cli compliance-bundle-export
```

### Acceptatiecriteria

* \[ ] Commands support JSON.
* \[ ] Commands are local-only.
* \[ ] Commands require confirm for permission changes.
* \[ ] Commands cannot enable live.
* \[ ] Commands output secret-free reports.

\---

## 18\. Fase 15 - Compliance Bundle Export

Doel: alles in één verifieerbare auditbundel.

### Nieuwe module

```text
src/binance\_spot\_bot/compliance\_bundle.py
```

### Bundle bevat

* \[ ] compliance report;
* \[ ] compliance score;
* \[ ] permission profiles;
* \[ ] role templates;
* \[ ] permission manifests;
* \[ ] permission drift reports;
* \[ ] decision journal exports;
* \[ ] action audit bundles;
* \[ ] redaction self-test;
* \[ ] secret scan result;
* \[ ] check-all result;
* \[ ] browser smoke result;
* \[ ] evidence chain;
* \[ ] support bundle verify summary;
* \[ ] no-live proof;
* \[ ] hashes.

### Output

```text
data/compliance/bundles/<bundle\_id>/
  compliance\_bundle\_manifest.json
  compliance\_bundle\_summary.md
  files/
```

### Acceptatiecriteria

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle can be archived.
* \[ ] Dashboard/CLI export works.

\---

## 19\. Fase 16 - Permission Review Workflow

Doel: periodieke review van operator roles en permissions.

### Nieuwe module

```text
src/binance\_spot\_bot/permission\_review.py
```

### Review types

* \[ ] daily critical drift review;
* \[ ] weekly role review;
* \[ ] monthly permission baseline review;
* \[ ] after permission change review;
* \[ ] after failed action review.

### Review output

* \[ ] reviewed profiles;
* \[ ] stale profiles;
* \[ ] overprivileged operators;
* \[ ] unused permissions;
* \[ ] forbidden attempts;
* \[ ] recommendations;
* \[ ] approval decision;
* \[ ] evidence links.

### Acceptatiecriteria

* \[ ] Review can be scheduled by local ops.
* \[ ] Review is secret-free.
* \[ ] Review creates reminder if stale.
* \[ ] Review feeds compliance score.
* \[ ] No live controls.

\---

## 20\. Fase 17 - Tests

### Unit tests

* \[ ] `tests/test\_local\_operator\_identity.py`
* \[ ] `tests/test\_permission\_profiles.py`
* \[ ] `tests/test\_operator\_roles.py`
* \[ ] `tests/test\_permission\_engine.py`
* \[ ] `tests/test\_separation\_of\_duties.py`
* \[ ] `tests/test\_approval\_policy\_templates.py`
* \[ ] `tests/test\_permission\_change\_workflow.py`
* \[ ] `tests/test\_permission\_drift.py`
* \[ ] `tests/test\_role\_aware\_action\_center.py`
* \[ ] `tests/test\_compliance\_evidence.py`
* \[ ] `tests/test\_compliance\_report.py`
* \[ ] `tests/test\_compliance\_score.py`
* \[ ] `tests/test\_compliance\_bundle.py`
* \[ ] `tests/test\_permission\_review.py`

### Integration tests

* \[ ] Create default operator identity.
* \[ ] Load default role templates.
* \[ ] Evaluate permissions for viewer/operator/maintainer/admin.
* \[ ] Block viewer approval.
* \[ ] Block self-approval destructive action.
* \[ ] Propose permission change.
* \[ ] Approve permission change.
* \[ ] Detect permission drift.
* \[ ] Generate compliance report.
* \[ ] Export compliance bundle.
* \[ ] Verify compliance bundle.

### Safety tests

* \[ ] Admin cannot enable live.
* \[ ] Forbidden scope cannot be granted.
* \[ ] Live proposal remains rejected.
* \[ ] Signed/order/account scope remains rejected.
* \[ ] Secret scan finding blocks strong compliance grade.
* \[ ] Redaction failure blocks compliance.
* \[ ] Unapproved execution blocks compliance.
* \[ ] Reports contain no secrets.
* \[ ] No-live proof remains true.

\---

## 21\. Docs

Nieuwe docs:

* \[ ] `docs/local-permission-compliance-safety-contract.md`
* \[ ] `docs/local-operator-identity-v2.md`
* \[ ] `docs/permission-profile-schema.md`
* \[ ] `docs/operator-role-templates.md`
* \[ ] `docs/permission-engine.md`
* \[ ] `docs/separation-of-duties.md`
* \[ ] `docs/approval-policy-templates.md`
* \[ ] `docs/permission-change-workflow.md`
* \[ ] `docs/permission-drift-detection.md`
* \[ ] `docs/role-aware-action-center.md`
* \[ ] `docs/compliance-evidence-model.md`
* \[ ] `docs/audit-grade-compliance-report.md`
* \[ ] `docs/compliance-score.md`
* \[ ] `docs/compliance-dashboard.md`
* \[ ] `docs/compliance-bundle-export.md`
* \[ ] `docs/permission-review-workflow.md`

README updates:

* \[ ] local roles overview;
* \[ ] permission profiles;
* \[ ] action approval permissions;
* \[ ] compliance report command;
* \[ ] compliance bundle command;
* \[ ] no-live statement.

\---

## 22\. CLI command examples

### Check current operator

```powershell
python -m binance\_spot\_bot.cli operator-identity --json
```

### Check a permission

```powershell
python -m binance\_spot\_bot.cli permission-check --scope approve\_confirm\_required --json
```

### Run drift check

```powershell
python -m binance\_spot\_bot.cli permission-drift-check --json
```

### Generate compliance report

```powershell
python -m binance\_spot\_bot.cli compliance-report --json
```

### Export compliance bundle

```powershell
python -m binance\_spot\_bot.cli compliance-bundle-export
```

\---

## 23\. Codex bouwvolgorde

### PR 1 - Operator Identity V2 + Permission Profiles

* \[ ] `local\_operator\_identity.py`
* \[ ] `permission\_profiles.py`
* \[ ] default local identity
* \[ ] profile manifests
* \[ ] tests.

### PR 2 - Role Templates

* \[ ] `operator\_roles.py`
* \[ ] viewer/operator/maintainer/governance/admin\_local
* \[ ] tests.

### PR 3 - Permission Engine

* \[ ] permission decisions
* \[ ] explain denial
* \[ ] forbidden scopes
* \[ ] tests.

### PR 4 - Separation of Duties

* \[ ] SoD rules
* \[ ] action center integration base
* \[ ] tests.

### PR 5 - Approval Policy Templates

* \[ ] templates
* \[ ] validation
* \[ ] tests.

### PR 6 - Permission Change Workflow

* \[ ] propose/diff/approve
* \[ ] rollback file
* \[ ] journal integration
* \[ ] tests.

### PR 7 - Permission Drift

* \[ ] drift detection
* \[ ] critical blockers
* \[ ] tests.

### PR 8 - Compliance Evidence + Report

* \[ ] evidence model
* \[ ] compliance report
* \[ ] no-live proof
* \[ ] tests.

### PR 9 - Compliance Score + Bundle

* \[ ] score
* \[ ] bundle export
* \[ ] verification
* \[ ] tests.

### PR 10 - Dashboard + CLI + Docs

* \[ ] permissions/compliance dashboard
* \[ ] CLI commands
* \[ ] browser smoke
* \[ ] docs.

\---

## 24\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 087 PR 1: Operator Identity V2 + Permission Profiles.

Maak src/binance\_spot\_bot/local\_operator\_identity.py met:
- LocalOperatorIdentity
- LocalOperatorProfile
- LocalOperatorSession
- LocalOperatorDevice
- LocalOperatorIdentityStore

Maak src/binance\_spot\_bot/permission\_profiles.py met:
- PermissionProfile
- PermissionRule
- PermissionScope
- PermissionDecision
- PermissionProfileManifest

Gebruik local-only JSON storage onder data/permissions/.
Maak een default operator met viewer permissions als er nog geen identity bestaat.
Zorg dat forbidden scopes nooit toegestaan kunnen worden:
- enable\_live\_trading
- signed\_order\_endpoint
- account\_endpoint
- reveal\_secrets
- arbitrary\_shell
- remote\_upload

Gebruik bestaande redaction helpers.
Voeg tests toe voor:
- default identity creation
- profile serialization
- forbidden scope rejected
- disabled operator cannot approve
- identity/profile store contains no secrets
- live\_trading\_enabled=False in outputs

Geen dashboard bouwen in deze PR.
Geen executor bouwen.
Geen API calls.
Geen signed endpoints.
Geen orders.
Geen live trading.
```

Waarom eerst:

* Rollen en permissions zijn de basis voor alle compliance-hardening.
* Het bouwt voort op Roadmap 086 Action Center.
* Het raakt geen trading runtime.
* Het is klein genoeg voor Codex.
* Forbidden/no-live safety kan meteen hard getest worden.

\---

## 25\. Definition of Done

Roadmap 087 is klaar als:

* \[ ] Permission \& Compliance Safety Contract bestaat.
* \[ ] Local Operator Identity V2 werkt.
* \[ ] Permission Profile Schema werkt.
* \[ ] Default Role Templates werken.
* \[ ] Permission Evaluation Engine werkt.
* \[ ] Separation of Duties werkt.
* \[ ] Approval Policy Templates werken.
* \[ ] Permission Change Workflow werkt.
* \[ ] Permission Drift Detection werkt.
* \[ ] Role-Aware Action Center Integration werkt.
* \[ ] Compliance Evidence Model werkt.
* \[ ] Audit-Grade Compliance Report werkt.
* \[ ] Compliance Scoring werkt.
* \[ ] Compliance Dashboard Panel werkt.
* \[ ] Permission \& Compliance CLI werkt.
* \[ ] Compliance Bundle Export werkt.
* \[ ] Permission Review Workflow werkt.
* \[ ] Tests bewijzen geen live/signed/account/order permissions.
* \[ ] Tests bewijzen admin forbidden actions niet kan toestaan.
* \[ ] Reports/bundles zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 087 kan na uitvoering naar `Voltooid docs`.

\---

## 26\. Verwachte Roadmap 088 daarna

Na Roadmap 087 zou Roadmap 088 logisch focussen op:

```text
Roadmap 088 - Offline Disaster Recovery, Backup/Restore Drills \& Local State Integrity
```

Mogelijke inhoud:

* \[ ] offline backup profiles;
* \[ ] restore previews;
* \[ ] state integrity checks;
* \[ ] disaster recovery runbooks;
* \[ ] corrupt data recovery;
* \[ ] permission/audit restore validation;
* \[ ] evidence continuity after restore;
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

Gebouwd: local operator identity, permission profiles, operator roles, permission engine, separation of duties, approval policy templates, permission change workflow, permission drift, compliance evidence/report/score/bundle, permission review, dashboardtab `Permissions`, CLI smoke via `permission-report` en `permission-check`.

Validatie: `tests/test_roadmaps_083_088_full_surface.py`, `tests/test_roadmaps_082_088_ops_governance.py`, dashboard-smoke en CLI smoke.

Safety: permissions cannot enable live trading; live-trade action remains blocked.

---

## Finale afwerking 2026-05-11

Status: Voltooid en verplaatsbaar naar `Voltooid docs/`.

Gebouwd en herbouwd zonder facade-only implementatie:

* `src/binance_spot_bot/local_operator_identity.py`
* `src/binance_spot_bot/permission_profiles.py`
* `src/binance_spot_bot/operator_roles.py`
* `src/binance_spot_bot/permission_engine.py`
* `src/binance_spot_bot/separation_of_duties.py`
* `src/binance_spot_bot/approval_policy_templates.py`
* `src/binance_spot_bot/permission_change_workflow.py`
* `src/binance_spot_bot/permission_drift.py`
* `src/binance_spot_bot/compliance_evidence.py`
* `src/binance_spot_bot/compliance_report.py`
* `src/binance_spot_bot/compliance_score.py`
* `src/binance_spot_bot/compliance_bundle.py`
* `src/binance_spot_bot/permission_review.py`
* `src/binance_spot_bot/ui/streamlit_app.py` Permissions & Compliance panel
* `src/binance_spot_bot/cli.py` permission/compliance CLI
* `tests/test_roadmap_087_permissions_compliance_acceptance.py`

Docs toegevoegd:

* `docs/local-permission-compliance-safety-contract.md`
* `docs/local-operator-identity-v2.md`
* `docs/permission-profile-schema.md`
* `docs/operator-role-templates.md`
* `docs/permission-engine.md`
* `docs/separation-of-duties.md`
* `docs/approval-policy-templates.md`
* `docs/permission-change-workflow.md`
* `docs/permission-drift-detection.md`
* `docs/role-aware-action-center.md`
* `docs/compliance-evidence-model.md`
* `docs/audit-grade-compliance-report.md`
* `docs/compliance-score.md`
* `docs/compliance-dashboard.md`
* `docs/compliance-bundle-export.md`
* `docs/permission-review-workflow.md`

Validatie uitgevoerd:

* `python -m pytest tests/test_roadmap_087_permissions_compliance_acceptance.py tests/test_roadmap_086_action_center_acceptance.py tests/test_roadmaps_083_088_full_surface.py tests/test_roadmaps_082_088_ops_governance.py -q` -> groen.
* Permission/compliance CLI flow: operator identity, profiles, permission check, permission change propose/approve, drift, evidence, report, score, bundle export -> groen.
* `python -m pytest -q` -> `324 passed, 1 warning`.
* `python -m binance_spot_bot.cli check-all --skip-tests --json` -> groen.
* `python -m binance_spot_bot.cli dashboard-smoke --seconds 1` -> groen.
* `python -m binance_spot_bot.cli dashboard-browser-smoke --url http://127.0.0.1:8506/ --seconds 10` -> groen.

Safety evidence:

* `admin_local` kan forbidden scopes niet toestaan.
* Live/signed/account/secrets/arbitrary shell/remote upload scopes blijven globaal geblokkeerd.
* Disabled operators kunnen niet approven/executen.
* Sensitive self-approval wordt geblokkeerd door separation of duties.
* Compliance reports en bundles bevatten no-live proof en redaction proof.
* `live_trading_enabled=false` blijft expliciet in outputs.

