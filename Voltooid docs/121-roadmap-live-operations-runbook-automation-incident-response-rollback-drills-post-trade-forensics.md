# Roadmap 121 - Live Operations Runbook Automation, Incident Response, Rollback Drills \& Post-Trade Forensics

Status: Voltooid en gevalideerd  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/121-roadmap-live-operations-runbook-automation-incident-response-rollback-drills-post-trade-forensics.md
```

## Samenvatting

Roadmap 116 maakt de bot een one-click lokale app met één Dashboard V2 Control Center.

Roadmap 117 bouwt demo spot data collection, dataset quality, model/strategy validation, paper replay en testnet promotion.

Roadmap 118 bouwt live dry-run, read-only account verification, order preview, sizing guards, safety drills en een tiny capped first-order gate.

Roadmap 119 bouwt controlled live sessions met micro-position budgets, max orders, reconciliation na elke order, monitoring, circuit breakers en automatic disarm rules.

Roadmap 120 bouwt live governance: session reviews, scorecards, execution quality, risk limit calibration, scaling decisions, operator approvals, profile lifecycle en governance evidence.

Roadmap 121 is de beste volgende stap: **operationele live-runbooks, incident response, rollback drills en post-trade forensics**. Als er eenmaal controlled live sessions en governance bestaan, moet de bot niet alleen “kunnen traden”, maar ook veilig kunnen reageren wanneer iets fout gaat: unknown order state, reconciliation mismatch, API failure, stale data, high spread, emergency stop, unexpected open order, evidence writer failure of dashboard disconnect.

De kern:

```text
Live session/governance evidence
→ incident detection
→ incident classification
→ automated runbook suggestions
→ operator action checklist
→ rollback drill
→ post-trade forensic timeline
→ root-cause report
→ prevention backlog
→ governance evidence
```

Dit is nog steeds geen unattended live trading. Roadmap 121 automatiseert runbooks en forensic analyse, maar live orders blijven onder de gecontroleerde live session manager en operator approvals vallen.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 121`, `121-roadmap`, `Live Operations Runbook Automation`, `Incident Response`, `Rollback Drills`, `Post-Trade Forensics` en `Live Governance Blocker Burn-Down`.
* \[x] Geen bestaande Roadmap 121 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 120 is lokaal aangemaakt als Live Session Performance Review, Scaling Governance, Risk Limit Calibration \& Operator Approval Workflow.

### Codebasecontrole

Breed bekeken met focus op sessions, audit, risk, execution, live readiness, evidence en recovery:

* \[x] `src/binance\_spot\_bot/session\_store.py`
* \[x] `src/binance\_spot\_bot/audit.py`
* \[x] `src/binance\_spot\_bot/risk.py`
* \[x] `src/binance\_spot\_bot/config.py`
* \[x] `src/binance\_spot\_bot/execution.py`
* \[x] `src/binance\_spot\_bot/binance.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] roadmaplijn 104-120.

### Belangrijke bestaande basis

* \[x] `SessionStore` bewaart summaries, snapshots, fills, alerts, orders en heartbeats, en kan sessies afsluiten met PnL, drawdown, trades, blocks en status.
* \[x] `AuditLog` scrubt secret-like velden zoals API key, secret, signature, authorization en X-MBX-APIKEY.
* \[x] `RiskEngine` blokkeert al op kill switch, HOLD, lage confidence, max trades, max position, max daily loss, stale data, hoge spread en onvoldoende balance.
* \[x] `BotSettings.validate\_live\_readiness()` vereist live env, live flag, kill switch false, manual approval, risk limits en credentials.
* \[x] `ExecutionEngine` houdt live order placement bewust geblokkeerd tot aparte manual implementation, terwijl paper/demo/testnet flows bestaan.
* \[x] Roadmap 118/119/120 voegen live dry-run, first-order gate, controlled live sessions, reconciliation, automatic disarm, live scorecards en governance toe.

### Belangrijkste gat na Roadmap 120

Na live governance weet je of een sessie goed of slecht was. Maar bij echte incidenten wil je sneller en gestructureerder handelen:

* \[ ] Geen incident taxonomy.
* \[ ] Geen automated runbook decision tree.
* \[ ] Geen rollback drill engine.
* \[ ] Geen post-trade forensic timeline builder.
* \[ ] Geen root-cause report generator.
* \[ ] Geen incident evidence bundle.
* \[ ] Geen operator incident command center in Dashboard V2.
* \[ ] Geen “what changed before incident?” diff.
* \[ ] Geen timeline van order → risk → exchange → reconciliation → disarm.
* \[ ] Geen prevention backlog uit incidents.
* \[ ] Geen incident rehearsal/simulation framework.
* \[ ] Geen recovery readiness score.

Roadmap 121 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 121

Maak een operationele veiligheidslaag voor live incidenten:

```text
live session events
→ incident detector
→ incident classifier
→ runbook automation
→ rollback/recovery drill
→ forensic timeline
→ root cause analysis
→ prevention backlog
→ evidence bundle
```

Na Roadmap 121 moet de operator:

* \[ ] incidenten automatisch kunnen herkennen en classificeren;
* \[ ] de juiste runbook stappen in het dashboard zien;
* \[ ] rollback/drill workflows kunnen oefenen met fake adapter/fixtures;
* \[ ] post-trade forensic timelines kunnen genereren;
* \[ ] root-cause reports kunnen exporteren;
* \[ ] prevention backlog items kunnen laten aanmaken;
* \[ ] incident evidence kunnen bundelen;
* \[ ] incident readiness kunnen testen in check-all/UAT;
* \[ ] live trading nog steeds handmatig, capped en gecontroleerd houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen one-click launcher opnieuw bouwen.
* \[ ] Geen Roadmap 117 demo-training pipeline opnieuw bouwen.
* \[ ] Geen Roadmap 118 first-order gate opnieuw bouwen.
* \[ ] Geen Roadmap 119 live session manager opnieuw bouwen.
* \[ ] Geen Roadmap 120 governance opnieuw bouwen.
* \[ ] Geen Binance adapter herschrijven.
* \[ ] Geen unattended live trading.
* \[ ] Geen nieuwe live order execution path.
* \[ ] Geen automatic scale-up.
* \[ ] Geen automatisch verder traden na incident.
* \[ ] Geen raw secrets in incidents, forensics of evidence.
* \[ ] Geen financieel advies.

Wel doen:

* \[ ] incident taxonomy;
* \[ ] incident detector/classifier;
* \[ ] runbook automation;
* \[ ] rollback drills;
* \[ ] post-trade forensic timeline;
* \[ ] root-cause analyzer;
* \[ ] prevention backlog;
* \[ ] incident evidence bundle;
* \[ ] Dashboard V2 incident command center;
* \[ ] CLI/API/check-all/UAT/docs.

\---

## 3\. Fase 0 - Live Operations Safety Contract

Nieuw docbestand:

```text
docs/live-ops/live-operations-safety-contract.md
```

Regels:

* \[ ] Incident tooling mag nooit live orders plaatsen.
* \[ ] Incident tooling mag nooit live sessions starten.
* \[ ] Incident tooling mag altijd emergency stop/disarm aanbevelen of uitvoeren via bestaande safe route.
* \[ ] Incident tooling moet raw secrets redacteren.
* \[ ] Incident reports moeten audit/evidence hashes bevatten.
* \[ ] Incident response mag niet automatisch risk limits verhogen.
* \[ ] Recovery mag niet automatisch live opnieuw armeren.
* \[ ] Post-incident recovery vereist operator review.
* \[ ] Runbook recommendations zijn operationele veiligheid, geen financieel advies.
* \[ ] Forensics mogen alleen bestaande logs/evidence lezen.
* \[ ] Rollback drills gebruiken fake adapter/fixtures tenzij operator expliciet testnet kiest.
* \[ ] Live blijft manually armed only.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen runbook tooling geen order endpoints gebruikt.
* \[ ] Tests bewijzen incident tooling wel emergency stop/disarm kan signaleren.
* \[ ] Tests bewijzen recovery geen auto-arm doet.
* \[ ] Tests bewijzen reports secret-free zijn.

\---

## 4\. Fase 1 - Incident Taxonomy Schema

Nieuwe module:

```text
src/binance\_spot\_bot/live\_ops/incident\_taxonomy.py
```

Incident types:

* \[ ] `unknown\_order\_state`
* \[ ] `reconciliation\_mismatch`
* \[ ] `unexpected\_open\_order`
* \[ ] `balance\_drift`
* \[ ] `order\_rejected`
* \[ ] `partial\_fill\_stuck`
* \[ ] `cancel\_failed`
* \[ ] `api\_connectivity\_loss`
* \[ ] `api\_rate\_limit`
* \[ ] `market\_data\_stale`
* \[ ] `spread\_spike`
* \[ ] `risk\_limit\_breach`
* \[ ] `kill\_switch\_triggered`
* \[ ] `emergency\_stop\_triggered`
* \[ ] `dashboard\_disconnect`
* \[ ] `evidence\_writer\_failure`
* \[ ] `audit\_hash\_mismatch`
* \[ ] `secret\_leak\_detected`
* \[ ] `profile\_config\_drift`
* \[ ] `model\_signal\_anomaly`
* \[ ] `unexpected\_live\_session\_state`

Severity levels:

* \[ ] P0 emergency;
* \[ ] P1 critical;
* \[ ] P2 high;
* \[ ] P3 medium;
* \[ ] P4 low.

Dataclasses:

* \[ ] `LiveOpsIncidentType`
* \[ ] `LiveOpsIncidentSeverity`
* \[ ] `LiveOpsIncident`
* \[ ] `LiveOpsIncidentSignal`
* \[ ] `LiveOpsIncidentClassification`
* \[ ] `LiveOpsIncidentTaxonomyReport`

Acceptatiecriteria:

* \[ ] Taxonomy is JSON-serializable.
* \[ ] Every incident type maps to severity default.
* \[ ] Every P0/P1 maps to immediate disarm/emergency runbook.
* \[ ] Secret leak maps to P0.
* \[ ] Tests cover taxonomy matrix.

\---

## 5\. Fase 2 - Incident Detector

Nieuwe module:

```text
src/binance\_spot\_bot/live\_ops/incident\_detector.py
```

Inputs:

* \[ ] live session store events;
* \[ ] session summaries;
* \[ ] audit log;
* \[ ] order lifecycle logs;
* \[ ] reconciliation reports;
* \[ ] heartbeat reports;
* \[ ] disarm rule reports;
* \[ ] circuit breaker reports;
* \[ ] governance scorecards;
* \[ ] dashboard connectivity events;
* \[ ] evidence writer reports.

Detection rules:

* \[ ] unknown order state -> incident;
* \[ ] reconciliation mismatch -> incident;
* \[ ] unexpected open order -> incident;
* \[ ] emergency stop -> incident;
* \[ ] stale data while live armed -> incident;
* \[ ] high spread while live armed -> incident;
* \[ ] evidence hash mismatch -> incident;
* \[ ] secret leak -> incident;
* \[ ] dashboard disconnect too long while live armed -> incident;
* \[ ] profile/config drift while live armed -> incident.

Acceptatiecriteria:

* \[ ] Detector works from fixture live session evidence.
* \[ ] Detector is read-only.
* \[ ] Detector redacts secrets.
* \[ ] Detector emits deterministic incident ids.
* \[ ] Tests cover every detection rule.

\---

## 6\. Fase 3 - Incident Classifier \& Priority Engine

Nieuwe module:

```text
src/binance\_spot\_bot/live\_ops/incident\_classifier.py
```

Classifier decisions:

* \[ ] severity;
* \[ ] affected session;
* \[ ] affected order;
* \[ ] affected profile;
* \[ ] recommended immediate action;
* \[ ] required runbook;
* \[ ] required evidence;
* \[ ] recovery allowed yes/no;
* \[ ] live re-arm allowed yes/no;
* \[ ] operator escalation required yes/no.

Hard rules:

* \[ ] secret leak = P0.
* \[ ] unknown order state while live = P0/P1.
* \[ ] reconciliation mismatch = P1.
* \[ ] unexpected open order = P1.
* \[ ] emergency stop = P1 unless drill.
* \[ ] evidence hash mismatch = P1/P0 depending context.
* \[ ] dashboard disconnect while live = P1/P2.
* \[ ] stale market data while live = P2/P1 if order pending.

Acceptatiecriteria:

* \[ ] Classifier deterministic.
* \[ ] P0/P1 blocks re-arm.
* \[ ] P0/P1 requires evidence bundle.
* \[ ] Tests cover severity rules.
* \[ ] Reports secret-free.

\---

## 7\. Fase 4 - Runbook Registry

Nieuwe module:

```text
src/binance\_spot\_bot/live\_ops/runbook\_registry.py
```

Runbooks:

* \[ ] `unknown\_order\_state\_runbook`
* \[ ] `reconciliation\_mismatch\_runbook`
* \[ ] `unexpected\_open\_order\_runbook`
* \[ ] `balance\_drift\_runbook`
* \[ ] `api\_connectivity\_loss\_runbook`
* \[ ] `market\_data\_stale\_runbook`
* \[ ] `spread\_spike\_runbook`
* \[ ] `risk\_limit\_breach\_runbook`
* \[ ] `emergency\_stop\_runbook`
* \[ ] `secret\_leak\_runbook`
* \[ ] `evidence\_hash\_mismatch\_runbook`
* \[ ] `dashboard\_disconnect\_runbook`
* \[ ] `profile\_config\_drift\_runbook`
* \[ ] `model\_signal\_anomaly\_runbook`

Per runbook:

* \[ ] runbook\_id;
* \[ ] title;
* \[ ] severity;
* \[ ] immediate actions;
* \[ ] safe automated actions;
* \[ ] manual actions;
* \[ ] required checks;
* \[ ] rollback steps;
* \[ ] recovery criteria;
* \[ ] evidence required;
* \[ ] re-arm blockers;
* \[ ] owner/operator notes.

Acceptatiecriteria:

* \[ ] Every incident type has runbook.
* \[ ] P0/P1 runbooks include disarm/emergency stop.
* \[ ] Runbooks never place orders.
* \[ ] Runbooks secret-free.
* \[ ] Tests cover registry completeness.

\---

## 8\. Fase 5 - Runbook Execution Planner

Nieuwe module:

```text
src/binance\_spot\_bot/live\_ops/runbook\_planner.py
```

Planner output:

* \[ ] recommended immediate safe action;
* \[ ] operator checklist;
* \[ ] automated safe checks;
* \[ ] evidence collection plan;
* \[ ] rollback plan;
* \[ ] recovery criteria;
* \[ ] re-arm blockers;
* \[ ] escalation note;
* \[ ] estimated priority;
* \[ ] dashboard next actions.

Allowed automated actions:

* \[ ] disarm through existing safe route;
* \[ ] emergency stop through existing safe route;
* \[ ] collect evidence;
* \[ ] verify hashes;
* \[ ] query local state;
* \[ ] run fake/testnet drill if explicitly configured;
* \[ ] create incident report.

Forbidden automated actions:

* \[ ] place order;
* \[ ] cancel live order automatically unless existing emergency/cancel gate explicitly requires operator confirmation;
* \[ ] re-arm live;
* \[ ] increase risk limit;
* \[ ] resume live session.

Acceptatiecriteria:

* \[ ] Planner never suggests unsafe auto-order action.
* \[ ] P0/P1 suggests disarm/emergency stop.
* \[ ] Recovery criteria explicit.
* \[ ] Tests cover allowed/forbidden actions.
* \[ ] Reports redacted.

\---

## 9\. Fase 6 - Incident Command Center State

Nieuwe module:

```text
src/binance\_spot\_bot/live\_ops/incident\_command\_center.py
```

States:

* \[ ] normal;
* \[ ] incident\_detected;
* \[ ] classifying;
* \[ ] runbook\_selected;
* \[ ] awaiting\_operator\_action;
* \[ ] safe\_action\_executed;
* \[ ] evidence\_collecting;
* \[ ] rollback\_drill\_running;
* \[ ] recovery\_review;
* \[ ] blocked\_from\_rearm;
* \[ ] resolved;
* \[ ] closed\_with\_followups.

Fields:

* \[ ] active\_incident\_id;
* \[ ] severity;
* \[ ] session\_id;
* \[ ] order\_id optional;
* \[ ] runbook\_id;
* \[ ] current\_step;
* \[ ] completed\_steps;
* \[ ] blockers;
* \[ ] safe\_actions\_taken;
* \[ ] evidence\_paths;
* \[ ] operator\_notes;
* \[ ] rearm\_allowed=false by default.

Acceptatiecriteria:

* \[ ] State machine deterministic.
* \[ ] Re-arm false by default.
* \[ ] Closing P0/P1 requires evidence.
* \[ ] Operator notes stored redacted.
* \[ ] Tests cover transitions.

\---

## 10\. Fase 7 - Rollback Drill Engine

Nieuwe module:

```text
src/binance\_spot\_bot/live\_ops/rollback\_drills.py
```

Drills:

* \[ ] disarm drill;
* \[ ] emergency stop drill;
* \[ ] cancel pending order drill with fake adapter;
* \[ ] reconciliation mismatch drill;
* \[ ] dashboard disconnect drill;
* \[ ] stale data drill;
* \[ ] evidence writer failure drill;
* \[ ] profile rollback drill;
* \[ ] risk preset rollback drill;
* \[ ] live profile demotion drill.

Inputs:

* \[ ] fixture live session;
* \[ ] fake adapter;
* \[ ] session plan;
* \[ ] runbook;
* \[ ] expected safety result.

Outputs:

* \[ ] drill result;
* \[ ] pass/fail;
* \[ ] timing;
* \[ ] actions taken;
* \[ ] evidence paths;
* \[ ] blockers;
* \[ ] recommended fixes.

Acceptatiecriteria:

* \[ ] Drills run offline/fake by default.
* \[ ] Drills never place real orders.
* \[ ] Failed drill creates P1/P2 finding.
* \[ ] Drill reports are secret-free.
* \[ ] Tests cover all drills.

\---

## 11\. Fase 8 - Post-Trade Forensic Timeline Builder

Nieuwe module:

```text
src/binance\_spot\_bot/live\_ops/post\_trade\_forensics.py
```

Timeline sources:

* \[ ] audit log;
* \[ ] session store snapshots;
* \[ ] order lifecycle;
* \[ ] reconciliation reports;
* \[ ] heartbeats;
* \[ ] disarm rules;
* \[ ] circuit breakers;
* \[ ] risk decisions;
* \[ ] order previews;
* \[ ] execution responses;
* \[ ] dashboard/operator actions;
* \[ ] governance approvals;
* \[ ] evidence manifests.

Timeline event categories:

* \[ ] profile/config;
* \[ ] market data;
* \[ ] model signal;
* \[ ] risk decision;
* \[ ] preview;
* \[ ] order submit;
* \[ ] exchange response;
* \[ ] reconciliation;
* \[ ] heartbeat;
* \[ ] disarm/circuit breaker;
* \[ ] operator action;
* \[ ] evidence.

Acceptatiecriteria:

* \[ ] Timeline deterministic.
* \[ ] Events sorted by timestamp.
* \[ ] Missing timestamps flagged.
* \[ ] Secret redaction passes.
* \[ ] Tests cover timeline reconstruction.

\---

## 12\. Fase 9 - Root Cause Analyzer

Nieuwe module:

```text
src/binance\_spot\_bot/live\_ops/root\_cause\_analyzer.py
```

Root cause categories:

* \[ ] market data issue;
* \[ ] exchange/API issue;
* \[ ] risk config issue;
* \[ ] model/signal issue;
* \[ ] profile/config drift;
* \[ ] operator action issue;
* \[ ] reconciliation/order state issue;
* \[ ] evidence/audit issue;
* \[ ] dashboard/connectivity issue;
* \[ ] unknown/needs manual review.

Analyzer outputs:

* \[ ] likely root cause;
* \[ ] contributing factors;
* \[ ] evidence links;
* \[ ] confidence level;
* \[ ] unresolved questions;
* \[ ] recommended prevention items;
* \[ ] required operator review.

Acceptatiecriteria:

* \[ ] Analyzer works from incident fixture.
* \[ ] Unknown stays unknown, no fake certainty.
* \[ ] Evidence links included.
* \[ ] Reports are Markdown + JSON.
* \[ ] Tests cover root cause categories.

\---

## 13\. Fase 10 - Prevention Backlog Generator

Nieuwe module:

```text
src/binance\_spot\_bot/live\_ops/prevention\_backlog.py
```

Backlog item types:

* \[ ] test missing;
* \[ ] runbook missing;
* \[ ] dashboard warning missing;
* \[ ] risk limit too loose;
* \[ ] data quality gap;
* \[ ] reconciliation improvement;
* \[ ] evidence gap;
* \[ ] operator workflow issue;
* \[ ] docs/runbook update;
* \[ ] automation hardening;
* \[ ] profile demotion needed.

Fields:

* \[ ] backlog\_id;
* \[ ] incident\_id;
* \[ ] title;
* \[ ] priority;
* \[ ] owner\_area;
* \[ ] recommended roadmap;
* \[ ] evidence\_refs;
* \[ ] acceptance criteria;
* \[ ] created\_at\_ms;
* \[ ] status.

Acceptatiecriteria:

* \[ ] P0/P1 incidents create backlog items.
* \[ ] Duplicate backlog items merged.
* \[ ] Items are exportable Markdown/JSON.
* \[ ] No secrets.
* \[ ] Tests cover item generation.

\---

## 14\. Fase 11 - Recovery Readiness Gate

Nieuwe module:

```text
src/binance\_spot\_bot/live\_ops/recovery\_readiness\_gate.py
```

Recovery gate requires:

* \[ ] incident classified;
* \[ ] runbook completed;
* \[ ] evidence bundle created;
* \[ ] forensics generated;
* \[ ] root cause reviewed;
* \[ ] P0/P1 blockers resolved or accepted as blocked;
* \[ ] rollback drill passed;
* \[ ] profile state safe;
* \[ ] risk limits not increased automatically;
* \[ ] operator approval for any re-arm;
* \[ ] governance status updated.

Gate states:

* \[ ] recovery\_blocked;
* \[ ] more\_evidence\_required;
* \[ ] rollback\_drill\_required;
* \[ ] root\_cause\_review\_required;
* \[ ] safe\_to\_resume\_paper\_or\_demo;
* \[ ] live\_rearm\_review\_required;
* \[ ] live\_rearm\_blocked;
* \[ ] incident\_closed\_no\_rearm.

Acceptatiecriteria:

* \[ ] Gate never auto-rearms live.
* \[ ] Missing root cause blocks live rearm review.
* \[ ] Failed rollback drill blocks.
* \[ ] Report redacted.
* \[ ] Tests cover states.

\---

## 15\. Fase 12 - Incident Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/live\_ops/incident\_evidence\_bundle.py
```

Bundle bevat:

* \[ ] safety contract;
* \[ ] incident taxonomy report;
* \[ ] detector output;
* \[ ] classifier output;
* \[ ] selected runbook;
* \[ ] runbook execution plan;
* \[ ] command center state;
* \[ ] rollback drill report;
* \[ ] forensic timeline;
* \[ ] root cause report;
* \[ ] prevention backlog;
* \[ ] recovery readiness gate;
* \[ ] relevant live session evidence refs;
* \[ ] relevant governance evidence refs;
* \[ ] audit hash chain refs;
* \[ ] redaction proof;
* \[ ] no-auto-rearm proof;
* \[ ] hashes.

Output:

```text
data/live-ops/incidents/<incident\_id>/evidence/
  incident\_evidence\_manifest.json
  incident\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Evidence bundle secret-free.
* \[ ] Evidence has manifest/hash.
* \[ ] Evidence can be verified.
* \[ ] Bundle states recovery/rearm status clearly.
* \[ ] Dashboard can download bundle.

\---

## 16\. Fase 13 - Dashboard V2 Live Ops Incident Command Center

Nieuwe routes/pages:

```text
/live-ops
/live-ops/incidents
/live-ops/runbooks
/live-ops/rollback-drills
/live-ops/forensics
/live-ops/root-cause
/live-ops/prevention-backlog
/live-ops/recovery
/live-ops/evidence
```

Panels:

* \[ ] active incident banner;
* \[ ] incident severity;
* \[ ] session/order affected;
* \[ ] selected runbook;
* \[ ] immediate safe action;
* \[ ] operator checklist;
* \[ ] evidence status;
* \[ ] rollback drill launcher;
* \[ ] forensic timeline;
* \[ ] root cause report;
* \[ ] prevention backlog;
* \[ ] recovery readiness gate;
* \[ ] re-arm blocked/allowed review status;
* \[ ] emergency stop/disarm controls;
* \[ ] incident evidence export.

UX rules:

* \[ ] P0/P1 banner always visible.
* \[ ] Emergency stop/disarm easier than recovery.
* \[ ] Re-arm never automatic.
* \[ ] Recovery status explicit.
* \[ ] Operator notes redacted.
* \[ ] No order execute controls here.

Acceptatiecriteria:

* \[ ] Live Ops page loads.
* \[ ] Incident list visible.
* \[ ] Runbook checklist visible.
* \[ ] Forensic timeline visible.
* \[ ] Browser smoke covers fake incident flow.

\---

## 17\. Fase 14 - Live Ops API Routes

Nieuwe API routes:

```text
GET  /api/live-ops/status
POST /api/live-ops/incidents/detect
GET  /api/live-ops/incidents
GET  /api/live-ops/incidents/{incident\_id}
POST /api/live-ops/incidents/{incident\_id}/classify
GET  /api/live-ops/runbooks
GET  /api/live-ops/runbooks/{runbook\_id}
POST /api/live-ops/runbooks/plan
POST /api/live-ops/command-center/update
POST /api/live-ops/rollback-drills/run
POST /api/live-ops/forensics/build-timeline
POST /api/live-ops/root-cause/analyze
POST /api/live-ops/prevention-backlog/generate
POST /api/live-ops/recovery/check
POST /api/live-ops/evidence/export
WS   /ws/live-ops
```

API rules:

* \[ ] no route places orders;
* \[ ] no route starts live session;
* \[ ] emergency stop/disarm only via existing safe route;
* \[ ] all responses redacted;
* \[ ] re-arm never automatic;
* \[ ] runbook actions require operator confirmation where needed.

Acceptatiecriteria:

* \[ ] TestClient covers routes.
* \[ ] Order endpoints never called.
* \[ ] Recovery route never re-arms.
* \[ ] Secrets redacted.
* \[ ] WebSocket emits incident state.

\---

## 18\. Fase 15 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli live-ops-status --json
python -m binance\_spot\_bot.cli live-incident-detect --session <id> --json
python -m binance\_spot\_bot.cli live-incident-classify --incident <id> --json
python -m binance\_spot\_bot.cli live-runbook-plan --incident <id> --json
python -m binance\_spot\_bot.cli live-rollback-drill --drill disarm --json
python -m binance\_spot\_bot.cli live-forensic-timeline --incident <id> --json
python -m binance\_spot\_bot.cli live-root-cause --incident <id> --json
python -m binance\_spot\_bot.cli live-prevention-backlog --incident <id> --json
python -m binance\_spot\_bot.cli live-recovery-check --incident <id> --json
python -m binance\_spot\_bot.cli live-incident-evidence-export --incident <id>
python -m binance\_spot\_bot.cli dashboard-v2-live-ops-smoke --json
```

Acceptatiecriteria:

* \[ ] Commands work offline from evidence/fixtures.
* \[ ] Commands support JSON.
* \[ ] Commands never place orders.
* \[ ] Commands never re-arm live.
* \[ ] Reports redact secrets.

\---

## 19\. Fase 16 - Check-All Integration

Fast profile:

* \[ ] live\_ops modules import;
* \[ ] taxonomy completeness;
* \[ ] runbook registry completeness;
* \[ ] detector fixture;
* \[ ] secret redaction;
* \[ ] no order endpoint call tests;
* \[ ] no auto-rearm tests.

Deep profile:

* \[ ] fake live incident fixture;
* \[ ] incident detection/classification;
* \[ ] runbook plan;
* \[ ] rollback drill fixture;
* \[ ] forensic timeline;
* \[ ] root cause report;
* \[ ] prevention backlog;
* \[ ] recovery readiness gate;
* \[ ] incident evidence export/verify;
* \[ ] Dashboard live ops browser smoke.

Acceptatiecriteria:

* \[ ] Fast check-all stays safe.
* \[ ] Deep profile proves incident workflow.
* \[ ] Any order call hard fails.
* \[ ] Any auto-rearm hard fails.
* \[ ] Secret leak hard fails.

\---

## 20\. Fase 17 - UAT / Operator Workflow

UAT scenarios:

* \[ ] open Live Ops Incident Command Center;
* \[ ] detect fake reconciliation mismatch;
* \[ ] classify incident as P1;
* \[ ] view selected runbook;
* \[ ] execute safe runbook checklist in fake mode;
* \[ ] run rollback drill;
* \[ ] build forensic timeline;
* \[ ] generate root cause report;
* \[ ] generate prevention backlog;
* \[ ] run recovery readiness gate;
* \[ ] verify live re-arm remains blocked;
* \[ ] export incident evidence.

Acceptatiecriteria:

* \[ ] UAT confirms no order placement.
* \[ ] UAT confirms no auto re-arm.
* \[ ] UAT confirms P0/P1 runbook is clear.
* \[ ] UAT confirms evidence secret-free.
* \[ ] UAT evidence attached.

\---

## 21\. Fase 18 - Release / Knowledge / Test / Performance Integration

Roadmap 089:

* \[ ] release notes mention live ops incident command center.
* \[ ] version manifest includes live ops schema version.
* \[ ] migration notes include incident evidence paths.

Roadmap 091:

* \[ ] knowledge graph maps live session → incident → runbook → forensic timeline → root cause → prevention backlog.
* \[ ] impact analysis detects changes affecting live ops.

Roadmap 092:

* \[ ] test selector chooses live ops tests for live\_ops changes.
* \[ ] live\_trading changes select incident regression tests.
* \[ ] dashboard live ops UI changes select browser smoke.

Roadmap 093:

* \[ ] performance budget for incident detection, timeline build, evidence export and dashboard render.

Acceptatiecriteria:

* \[ ] Release evidence includes incident evidence.
* \[ ] Knowledge graph updated.
* \[ ] Test selector protects incident code.
* \[ ] Performance reports include live ops budgets.
* \[ ] No order placement in live ops.

\---

## 22\. Fase 19 - Scheduled Live Ops Reports

Scheduled jobs:

* \[ ] daily live ops status report;
* \[ ] weekly runbook registry validation;
* \[ ] weekly rollback drill in fake mode;
* \[ ] weekly incident detection over latest sessions;
* \[ ] weekly evidence integrity check;
* \[ ] monthly incident readiness report.

Metrics:

* \[ ] open incident count;
* \[ ] P0/P1 incident count;
* \[ ] runbook coverage percent;
* \[ ] rollback drill pass/fail;
* \[ ] evidence integrity failures;
* \[ ] prevention backlog count;
* \[ ] recovery readiness status;
* \[ ] no-auto-rearm proof.

Acceptatiecriteria:

* \[ ] Scheduled jobs never place orders.
* \[ ] Reports are secret-free.
* \[ ] Dashboard can show reports.
* \[ ] Check-all safe env preserved.

\---

## 23\. Tests

### Unit tests

* \[ ] `tests/test\_live\_ops\_safety\_contract.py`
* \[ ] `tests/test\_incident\_taxonomy.py`
* \[ ] `tests/test\_incident\_detector.py`
* \[ ] `tests/test\_incident\_classifier.py`
* \[ ] `tests/test\_runbook\_registry.py`
* \[ ] `tests/test\_runbook\_planner.py`
* \[ ] `tests/test\_incident\_command\_center.py`
* \[ ] `tests/test\_rollback\_drills.py`
* \[ ] `tests/test\_post\_trade\_forensics.py`
* \[ ] `tests/test\_root\_cause\_analyzer.py`
* \[ ] `tests/test\_prevention\_backlog.py`
* \[ ] `tests/test\_recovery\_readiness\_gate.py`
* \[ ] `tests/test\_incident\_evidence\_bundle.py`
* \[ ] `tests/test\_live\_ops\_api.py`

### Integration tests

* \[ ] Detect fake unknown order state.
* \[ ] Detect fake reconciliation mismatch.
* \[ ] Classify P0/P1 incidents.
* \[ ] Select runbook.
* \[ ] Generate runbook plan.
* \[ ] Run rollback drill fake mode.
* \[ ] Build forensic timeline.
* \[ ] Analyze root cause.
* \[ ] Generate prevention backlog.
* \[ ] Run recovery gate.
* \[ ] Export incident evidence.

### Browser smoke

* \[ ] `/live-ops` loads.
* \[ ] incident list visible.
* \[ ] P0/P1 banner visible.
* \[ ] runbook checklist visible.
* \[ ] rollback drill panel visible.
* \[ ] forensic timeline visible.
* \[ ] root cause panel visible.
* \[ ] recovery gate visible.
* \[ ] evidence export visible.
* \[ ] no order execute button visible.

### Safety tests

* \[ ] Live ops routes never place orders.
* \[ ] Live ops routes never start live session.
* \[ ] Recovery never auto-rearms live.
* \[ ] P0/P1 blocks re-arm.
* \[ ] Secret redaction works.
* \[ ] Evidence hash mismatch blocks recovery.
* \[ ] Financial advice wording blocked.
* \[ ] Check-all safe env preserved.

\---

## 24\. Docs

Nieuwe docs:

```text
docs/live-ops/live-operations-safety-contract.md
docs/live-ops/incident-taxonomy.md
docs/live-ops/incident-detector.md
docs/live-ops/incident-classifier.md
docs/live-ops/runbook-registry.md
docs/live-ops/runbook-planner.md
docs/live-ops/incident-command-center.md
docs/live-ops/rollback-drills.md
docs/live-ops/post-trade-forensics.md
docs/live-ops/root-cause-analyzer.md
docs/live-ops/prevention-backlog.md
docs/live-ops/recovery-readiness-gate.md
docs/live-ops/incident-evidence-bundle.md
docs/live-ops/dashboard-live-ops-command-center.md
```

README updates:

* \[ ] Live Ops overview.
* \[ ] Incident taxonomy.
* \[ ] Runbook automation.
* \[ ] Rollback drills.
* \[ ] Post-trade forensics.
* \[ ] Recovery readiness.
* \[ ] Incident evidence export.
* \[ ] No auto-rearm statement.

\---

## 25\. Codex bouwvolgorde

### PR 1 - Safety Contract + Incident Taxonomy

* \[ ] `docs/live-ops/live-operations-safety-contract.md`
* \[ ] `live\_ops/incident\_taxonomy.py`
* \[ ] taxonomy matrix tests.
* \[ ] no-order/no-auto-rearm tests.

### PR 2 - Incident Detector + Classifier

* \[ ] `incident\_detector.py`
* \[ ] `incident\_classifier.py`
* \[ ] fixture incident tests.

### PR 3 - Runbook Registry

* \[ ] `runbook\_registry.py`
* \[ ] runbook completeness tests.
* \[ ] P0/P1 safe action tests.

### PR 4 - Runbook Planner + Command Center State

* \[ ] `runbook\_planner.py`
* \[ ] `incident\_command\_center.py`
* \[ ] state/checklist tests.

### PR 5 - Rollback Drill Engine

* \[ ] `rollback\_drills.py`
* \[ ] fake drill tests.

### PR 6 - Post-Trade Forensics + Root Cause

* \[ ] `post\_trade\_forensics.py`
* \[ ] `root\_cause\_analyzer.py`
* \[ ] timeline/root cause tests.

### PR 7 - Prevention Backlog + Recovery Gate

* \[ ] `prevention\_backlog.py`
* \[ ] `recovery\_readiness\_gate.py`
* \[ ] recovery no-auto-rearm tests.

### PR 8 - Incident Evidence Bundle

* \[ ] `incident\_evidence\_bundle.py`
* \[ ] evidence export/verify tests.

### PR 9 - Dashboard Live Ops + API

* \[ ] API routes.
* \[ ] Dashboard V2 live ops pages.
* \[ ] browser smoke.

### PR 10 - CLI + Check-All + Docs + UAT + Integrations

* \[ ] CLI commands.
* \[ ] check-all profiles.
* \[ ] docs.
* \[ ] UAT scenarios.
* \[ ] release/knowledge/test/performance integration.
* \[ ] scheduled reports.

\---

## 26\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 121 PR 1: Live Operations Safety Contract + Incident Taxonomy.

Maak docs/live-ops/live-operations-safety-contract.md.

Maak src/binance\_spot\_bot/live\_ops/\_\_init\_\_.py.
Maak src/binance\_spot\_bot/live\_ops/incident\_taxonomy.py met:
- LiveOpsIncidentType
- LiveOpsIncidentSeverity
- LiveOpsIncident
- LiveOpsIncidentSignal
- LiveOpsIncidentClassification
- LiveOpsIncidentTaxonomyReport
- default\_live\_ops\_incident\_taxonomy()
- classify\_default\_severity(incident\_type: str)
- incident\_requires\_immediate\_disarm(incident\_type: str, severity: str)
- incident\_blocks\_rearm(incident\_type: str, severity: str)
- live\_ops\_incident\_taxonomy\_report\_to\_dict(...)
- write\_live\_ops\_incident\_taxonomy\_report(...)

Incident types minimaal:
- unknown\_order\_state
- reconciliation\_mismatch
- unexpected\_open\_order
- balance\_drift
- order\_rejected
- partial\_fill\_stuck
- cancel\_failed
- api\_connectivity\_loss
- api\_rate\_limit
- market\_data\_stale
- spread\_spike
- risk\_limit\_breach
- kill\_switch\_triggered
- emergency\_stop\_triggered
- dashboard\_disconnect
- evidence\_writer\_failure
- audit\_hash\_mismatch
- secret\_leak\_detected
- profile\_config\_drift
- model\_signal\_anomaly
- unexpected\_live\_session\_state

Severity levels:
- P0
- P1
- P2
- P3
- P4

Gedrag:
- secret\_leak\_detected = P0
- unknown\_order\_state = P0/P1 default P1
- reconciliation\_mismatch = P1
- unexpected\_open\_order = P1
- emergency\_stop\_triggered = P1 behalve drill metadata
- evidence/audit hash mismatch = P1
- P0/P1 require immediate disarm by default
- P0/P1 block re-arm by default
- output bevat no\_order\_placement\_statement
- output bevat no\_auto\_rearm\_statement
- output bevat not\_financial\_advice\_statement
- secret-like values worden geredact

Gebruik alleen stdlib.
Geen command execution.
Geen API calls.
Geen runtime execution.
Geen frontend execution.
Geen Streamlit wijzigen.
Geen signed endpoints.
Geen account/order endpoints.
Geen live trading.

Voeg tests toe voor:
- taxonomy contains all incident types
- default severity mapping
- P0/P1 immediate disarm
- P0/P1 block re-arm
- secret leak maps to P0
- emergency stop drill exception
- report JSON serialization
- secret-like values worden geredact
- no\_order\_placement\_statement aanwezig
- no\_auto\_rearm\_statement aanwezig
```

Waarom eerst:

* Live incident response kan pas veilig gebouwd worden als incident types, severity, disarm en re-arm blockers machine-testbaar zijn.
* Het is read-only en raakt execution/runtime/frontend niet.
* Het voorkomt dat recovery of runbooks ooit automatisch live opnieuw armeren.
* Daarna kunnen detector, classifier, runbooks en forensics veilig op deze taxonomy bouwen.

\---

## 27\. Definition of Done

Roadmap 121 is klaar als:

* \[ ] Live Operations Safety Contract bestaat.
* \[ ] Incident Taxonomy Schema werkt.
* \[ ] Incident Detector werkt.
* \[ ] Incident Classifier \& Priority Engine werkt.
* \[ ] Runbook Registry werkt.
* \[ ] Runbook Execution Planner werkt.
* \[ ] Incident Command Center State werkt.
* \[ ] Rollback Drill Engine werkt.
* \[ ] Post-Trade Forensic Timeline Builder werkt.
* \[ ] Root Cause Analyzer werkt.
* \[ ] Prevention Backlog Generator werkt.
* \[ ] Recovery Readiness Gate werkt.
* \[ ] Incident Evidence Bundle werkt.
* \[ ] Dashboard V2 Live Ops Incident Command Center werkt.
* \[ ] Live Ops API Routes werken.
* \[ ] CLI commands werken.
* \[ ] Check-All Integration werkt.
* \[ ] UAT/Operator Workflow werkt.
* \[ ] Release/Knowledge/Test/Performance integration werkt.
* \[ ] Scheduled Live Ops Reports werken.
* \[ ] Tests bewijzen live ops nooit orders plaatst.
* \[ ] Tests bewijzen recovery nooit auto-rearm doet.
* \[ ] Tests bewijzen P0/P1 re-arm blokkeert.
* \[ ] Tests bewijzen incident evidence secret-free is.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Roadmap 121 kan na uitvoering naar `Voltooid docs`.

\---

## 28\. Verwachte Roadmap 122 daarna

Als Roadmap 121 groen is:

```text
Roadmap 122 - Production-Grade Local Packaging, Installer, Desktop Shortcut, Auto-Update Guard \& Offline Recovery Kit
```

Mogelijke inhoud:

* \[ ] lokale installer/portable package;
* \[ ] desktop shortcut;
* \[ ] offline recovery kit;
* \[ ] preflight checks;
* \[ ] backup/restore;
* \[ ] safe auto-update guard;
* \[ ] still no unattended live.

```

Als Roadmap 121 incident blockers vindt:

```text
Roadmap 122 - Live Ops Incident Blocker Burn-Down, Runbook Hardening \& Forensic Coverage Improvement
```

Mogelijke inhoud:

* \[ ] ontbrekende runbooks oplossen;
* \[ ] forensic timeline gaps oplossen;
* \[ ] recovery gates verbeteren;
* \[ ] dashboard incident UX verbeteren;
* \[ ] rollback drills verbeteren;
* \[ ] live blijft capped/locked.

```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Live ops incident response and post-trade forensics safety surface.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.

---

## Voltooiingsbewijs 2026-05-16

Status: Voltooid en verplaatst naar `Voltooid docs` na implementatie en verificatie.

Gebouwd:

* Nieuwe `live_ops` package met incident taxonomy, detector, classifier, runbook registry, runbook planner, incident command center, rollback drills, post-trade forensics, root-cause analyzer, prevention backlog, recovery gate, incident evidence bundle en pipeline.
* Live Ops safety contract en docs onder `docs/live-ops/`.
* CLI-oppervlak voor status, incident detect/classify, runbook plan, rollback drill, forensic timeline, root cause, prevention backlog, recovery check, evidence export en Dashboard V2 smoke.
* Dashboard V2 Live Ops pagina op `/live-ops`.
* API-routes onder `/api/live-ops/*`.
* Check-all entries voor live ops status, rollback drill en dashboard smoke.
* Acceptatietests in `tests/test_roadmap_121_live_ops_acceptance.py`.

Validatie:

* `python -m compileall -q src tests`
* `pytest -q tests/test_roadmap_121_live_ops_acceptance.py` -> 4 passed
* CLI smokes voor `live-ops-status`, `live-incident-detect`, `live-rollback-drill`, `dashboard-v2-live-ops-smoke`
* `python -m binance_spot_bot.cli dashboard-v2-smoke --json`
* `python -m binance_spot_bot.check_all --skip-tests`
* `npm install` en `npm run build`
* `python -m binance_spot_bot.cli security-scan` -> geen findings
* Playwright screenshot smoke voor `/live-ops`

Safety:

* Live ops plaatst geen orders en start geen live sessies.
* Recovery en command center re-armen live nooit automatisch.
* P0/P1 incidenten blokkeren live re-arm tot operator review.
* Rollback drills draaien offline/fake by default.
* Evidence en reports bevatten no-order/no-auto-rearm proofs.

