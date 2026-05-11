# Roadmap 120 - Live Session Performance Review, Scaling Governance, Risk Limit Calibration \& Operator Approval Workflow

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/120-roadmap-live-session-performance-review-scaling-governance-risk-limit-calibration-operator-approval-workflow.md
```

## Samenvatting

Roadmap 116 maakt de bot een one-click lokale app met één Dashboard V2 Control Center.  
Roadmap 117 bouwt demo spot data collection, dataset quality, model/strategy validation, paper replay en testnet promotion.  
Roadmap 118 bouwt live dry-run, read-only account verification, order preview, sizing guards, safety drills en een tiny capped first-order gate.  
Roadmap 119 bouwt controlled live sessions: micro-position budgets, max orders, reconciliation na elke order, monitoring, circuit breakers en automatic disarm rules.

Roadmap 120 is de beste volgende stap: **niet verder opschalen naar meer live trading voordat elke controlled live session objectief beoordeeld wordt**. Deze roadmap maakt live session scorecards, performance review, risk-limit calibration, scaling governance, operator approval workflows, rollback rules en promotion/demotion policies.

De kern:

```text
Controlled live session evidence
→ session performance scorecard
→ risk limit calibration report
→ slippage/fee/spread analysis
→ disarm/reconciliation review
→ operator approval workflow
→ scaling governance decision
→ profile/risk preset update proposal
→ staged scale-up or rollback
```

Belangrijk: dit is nog steeds geen unattended live trading. Roadmap 120 beslist niet automatisch dat de bot groter mag traden. Het maakt een governance laag zodat de operator pas na evidence, review, scorecards en expliciete approval naar een volgende micro-scaling level kan.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 120`, `120-roadmap`, `Live Session Performance Review`, `Scaling Governance`, `Risk Limit Calibration` en `Operator Approval Workflow`.
* \[x] Geen bestaande Roadmap 120 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 119 is lokaal aangemaakt als Controlled Live Session Manager, Micro-Position Scaling, Live Monitoring \& Automatic Disarm Rules.

### Codebasecontrole

Breed bekeken met focus op live readiness, execution blocking, risk limits, sessions, audit, evidence en live safety:

* \[x] `src/binance\_spot\_bot/config.py`
* \[x] `src/binance\_spot\_bot/execution.py`
* \[x] `src/binance\_spot\_bot/risk.py`
* \[x] `src/binance\_spot\_bot/session\_store.py`
* \[x] `src/binance\_spot\_bot/audit.py`
* \[x] `src/binance\_spot\_bot/binance.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] roadmaplijn 104-119.

### Belangrijke bestaande basis

* \[x] `BotSettings.validate\_live\_readiness()` heeft live safety voorwaarden voor live env, live flag, kill switch, manual approval, risk limits en credentials.
* \[x] `ExecutionEngine` blokkeert live order placement tot een aparte manual implementation step, terwijl paper/demo/testnet flows al bestaan.
* \[x] `RiskEngine` bevat risk limits voor daily loss, max position, max trades, confidence, spread, stale data, quote size en slippage.
* \[x] `SessionStore` kan session summaries, snapshots, fills, alerts, orders en heartbeats opslaan.
* \[x] `AuditLog` redigeert secret-like velden.
* \[x] Roadmap 119 plant controlled live session evidence met budget, lifecycle, reconciliation, monitoring, disarm rules en session evidence.

### Belangrijkste gat na Roadmap 119

Na Roadmap 119 kan een gecontroleerde micro-live sessie veilig draaien, maar er is nog geen governance om te bepalen:

* \[ ] was deze live sessie goed genoeg?
* \[ ] waren slippage, fees en spread binnen verwachting?
* \[ ] werkte reconciliation foutloos?
* \[ ] waren er disarm triggers of circuit breaker warnings?
* \[ ] mag de bot naar een hoger micro-position level?
* \[ ] moeten risk limits juist omlaag?
* \[ ] moet het model/strategy/risk preset terug naar demo/paper?
* \[ ] welke operator heeft wat goedgekeurd?
* \[ ] welke evidence ondersteunt die beslissing?
* \[ ] hoe wordt een profiel veilig gepromote, gedemote of expired?

Roadmap 120 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 120

Maak een governance- en reviewlaag bovenop controlled live sessions:

```text
live session evidence
→ performance review
→ risk calibration
→ operator approval
→ scaling decision
→ profile update proposal
→ promotion/demotion/rollback
```

Na Roadmap 120 moet de operator:

* \[ ] elke live session kunnen reviewen;
* \[ ] live session scorecards kunnen genereren;
* \[ ] slippage/fees/spread/reconciliation kunnen beoordelen;
* \[ ] risk limits kunnen kalibreren op basis van evidence;
* \[ ] scaling decisions kunnen maken met approval workflow;
* \[ ] live profiles kunnen promoveren/demoveren/expiren;
* \[ ] rollback naar lagere live level kunnen uitvoeren;
* \[ ] operator notes en approvals kunnen vastleggen;
* \[ ] audit/evidence kunnen exporteren;
* \[ ] zeker weten dat geen scaling automatisch gebeurt zonder explicit approval.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen one-click launcher opnieuw bouwen.
* \[ ] Geen Roadmap 117 demo training pipeline opnieuw bouwen.
* \[ ] Geen Roadmap 118 first-order gate opnieuw bouwen.
* \[ ] Geen Roadmap 119 live session manager opnieuw bouwen.
* \[ ] Geen Binance adapter herschrijven.
* \[ ] Geen unattended live trading.
* \[ ] Geen automatische scale-up.
* \[ ] Geen live auto-start.
* \[ ] Geen order execution toevoegen buiten de controlled live session manager.
* \[ ] Geen financial advice.
* \[ ] Geen raw secrets in reports/evidence/dashboard.
* \[ ] Geen risk limits automatisch verhogen zonder approval.

Wel doen:

* \[ ] live session scorecards;
* \[ ] performance review;
* \[ ] slippage/fee/spread analysis;
* \[ ] reconciliation quality review;
* \[ ] disarm/circuit breaker review;
* \[ ] risk limit calibration;
* \[ ] scaling governance;
* \[ ] operator approval workflow;
* \[ ] profile promotion/demotion lifecycle;
* \[ ] dashboard governance cockpit;
* \[ ] evidence bundle;
* \[ ] docs/tests/check-all/UAT.

\---

## 3\. Fase 0 - Live Scaling Governance Safety Contract

Nieuw docbestand:

```text
docs/live-trading/live-scaling-governance-safety-contract.md
```

Regels:

* \[ ] Geen automatische live scale-up.
* \[ ] Geen unattended live trading.
* \[ ] Geen risk-limit verhoging zonder operator approval.
* \[ ] Geen profile promotion zonder live session evidence.
* \[ ] Geen promotion als reconciliation mismatch bestaat.
* \[ ] Geen promotion als emergency stop gebeurde zonder review.
* \[ ] Geen promotion als disarm trigger P0/P1 is.
* \[ ] Geen promotion als slippage/spread/fees buiten thresholds vallen.
* \[ ] Geen promotion als session loss threshold geraakt is.
* \[ ] Geen promotion als evidence manifest/hash faalt.
* \[ ] Approval moet expliciet, timestamped en auditbaar zijn.
* \[ ] Approval mag geen raw secrets bevatten.
* \[ ] Scaling decisions zijn research/governance, geen financieel advies.
* \[ ] Rollback/demotion moet altijd mogelijk zijn.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen automatische scale-up onmogelijk is.
* \[ ] Tests bewijzen approval vereist is.
* \[ ] Tests bewijzen evidence/hash failure promotion blokkeert.
* \[ ] Tests bewijzen reports secret-free zijn.

\---

## 4\. Fase 1 - Live Session Review Schema

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_session\_review.py
```

Dataclasses:

* \[ ] `LiveSessionReview`
* \[ ] `LiveSessionReviewInput`
* \[ ] `LiveSessionReviewFinding`
* \[ ] `LiveSessionReviewScore`
* \[ ] `LiveSessionReviewReport`

Review input:

* \[ ] live session evidence manifest;
* \[ ] session plan;
* \[ ] order lifecycle logs;
* \[ ] reconciliation reports;
* \[ ] heartbeat reports;
* \[ ] disarm events;
* \[ ] circuit breaker events;
* \[ ] account verification refs;
* \[ ] audit hash chain;
* \[ ] risk limits used;
* \[ ] scaling level used.

Finding categories:

* \[ ] performance;
* \[ ] risk;
* \[ ] reconciliation;
* \[ ] execution;
* \[ ] monitoring;
* \[ ] data quality;
* \[ ] evidence;
* \[ ] operator;
* \[ ] safety;
* \[ ] secret redaction.

Acceptatiecriteria:

* \[ ] Review schema is JSON-serializable.
* \[ ] Missing evidence creates blocker.
* \[ ] Unknown order state creates blocker.
* \[ ] Secret-like values redacted.
* \[ ] Tests cover valid/invalid review inputs.

\---

## 5\. Fase 2 - Live Session Scorecard Engine

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_session\_scorecards.py
```

Score dimensions:

* \[ ] evidence integrity score;
* \[ ] reconciliation score;
* \[ ] order lifecycle score;
* \[ ] risk compliance score;
* \[ ] slippage score;
* \[ ] fee impact score;
* \[ ] spread compliance score;
* \[ ] data freshness score;
* \[ ] heartbeat reliability score;
* \[ ] disarm/circuit breaker score;
* \[ ] operator control score;
* \[ ] emergency readiness score.

Grades:

* \[ ] A: eligible for scaling review.
* \[ ] B: keep same level with warnings.
* \[ ] C: repeat current level.
* \[ ] D: demote/rollback recommended.
* \[ ] F: block live until issue fixed.

Hard blockers:

* \[ ] missing evidence;
* \[ ] secret leak;
* \[ ] unreconciled order;
* \[ ] unknown exchange order state;
* \[ ] unexpected open order;
* \[ ] balance drift;
* \[ ] emergency stop without review;
* \[ ] risk limit breach;
* \[ ] order outside preview hash;
* \[ ] order outside session budget.

Acceptatiecriteria:

* \[ ] Scorecard deterministic.
* \[ ] Hard blockers force D/F.
* \[ ] Report explains reasons.
* \[ ] No financial advice wording.
* \[ ] Tests cover all grades.

\---

## 6\. Fase 3 - Live Execution Quality Analytics

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_execution\_quality.py
```

Analytics:

* \[ ] intended vs executed quantity;
* \[ ] intended quote vs actual quote;
* \[ ] preview price vs execution price;
* \[ ] estimated slippage vs actual slippage;
* \[ ] spread before/after order;
* \[ ] fee estimate vs actual fee;
* \[ ] order latency;
* \[ ] time to fill;
* \[ ] partial fill behavior;
* \[ ] rejection reasons;
* \[ ] cancel latency;
* \[ ] order query consistency;
* \[ ] top-of-book freshness.

Acceptatiecriteria:

* \[ ] Analytics work from fake/session evidence.
* \[ ] Missing data produces warnings.
* \[ ] Large slippage becomes blocker/warning.
* \[ ] Reports are JSON + Markdown.
* \[ ] Tests cover execution edge cases.

\---

## 7\. Fase 4 - Live Risk Limit Calibration

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/risk\_limit\_calibration.py
```

Calibration inputs:

* \[ ] live session scorecards;
* \[ ] risk decisions;
* \[ ] session budgets;
* \[ ] realized/unrealized PnL;
* \[ ] max drawdown;
* \[ ] slippage/fees;
* \[ ] spread samples;
* \[ ] stale data samples;
* \[ ] disarm triggers;
* \[ ] paper/demo/testnet comparison.

Calibration outputs:

* \[ ] recommended max single order quote;
* \[ ] recommended max session exposure;
* \[ ] recommended max session orders;
* \[ ] recommended max session loss;
* \[ ] recommended max daily loss;
* \[ ] recommended max spread bps;
* \[ ] recommended max data age;
* \[ ] recommended slippage cap;
* \[ ] recommended scaling level;
* \[ ] keep/demote/block decision;
* \[ ] explanation and evidence refs.

Rules:

* \[ ] Calibration can reduce limits automatically as proposal.
* \[ ] Calibration cannot increase limits without approval.
* \[ ] Calibration cannot bypass governance.
* \[ ] Calibration cannot write active profile directly.
* \[ ] Output is proposal only.

Acceptatiecriteria:

* \[ ] Calibration deterministic.
* \[ ] Risk increases require approval.
* \[ ] Risk reductions can be proposed safely.
* \[ ] Hard blockers prevent increase.
* \[ ] Tests cover calibration scenarios.

\---

## 8\. Fase 5 - Scaling Governance Decision Engine

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/scaling\_governance.py
```

Decision inputs:

* \[ ] current scaling level;
* \[ ] live session scorecards;
* \[ ] calibration report;
* \[ ] operator approval state;
* \[ ] unresolved findings;
* \[ ] recent emergency stops;
* \[ ] recent disarm triggers;
* \[ ] evidence integrity;
* \[ ] minimum successful sessions per level.

Decision outputs:

* \[ ] keep\_level;
* \[ ] eligible\_for\_next\_level\_review;
* \[ ] approved\_for\_next\_level;
* \[ ] repeat\_current\_level;
* \[ ] demote\_level;
* \[ ] block\_live;
* \[ ] expire\_profile;
* \[ ] rollback\_profile;

Hard rules:

* \[ ] cannot skip scaling level;
* \[ ] cannot promote without minimum successful sessions;
* \[ ] cannot promote with unresolved P0/P1 findings;
* \[ ] cannot promote without operator approval;
* \[ ] cannot promote if latest session grade below A/B;
* \[ ] cannot promote after emergency stop until review complete.

Acceptatiecriteria:

* \[ ] Decision engine deterministic.
* \[ ] No auto-approval.
* \[ ] Level skip blocked.
* \[ ] P0/P1 finding blocks promotion.
* \[ ] Tests cover all decisions.

\---

## 9\. Fase 6 - Operator Approval Workflow

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/operator\_approval\_workflow.py
```

Approval objects:

* \[ ] `OperatorApprovalRequest`
* \[ ] `OperatorApprovalDecision`
* \[ ] `OperatorApprovalNote`
* \[ ] `OperatorApprovalAuditRecord`

Approval types:

* \[ ] approve\_repeat\_current\_level;
* \[ ] approve\_next\_level;
* \[ ] approve\_risk\_limit\_decrease;
* \[ ] approve\_risk\_limit\_increase;
* \[ ] reject\_scaling;
* \[ ] request\_more\_evidence;
* \[ ] demote\_level;
* \[ ] expire\_profile;
* \[ ] emergency\_block\_live.

Approval requirements:

* \[ ] exact confirmation phrase;
* \[ ] operator note;
* \[ ] evidence refs;
* \[ ] scorecard grade;
* \[ ] calibration report;
* \[ ] timestamp;
* \[ ] one-time approval token;
* \[ ] expiry time;
* \[ ] audit event.

Acceptatiecriteria:

* \[ ] Approval requires explicit confirm.
* \[ ] Approval expires.
* \[ ] Approval cannot be reused.
* \[ ] Approval recorded in audit log.
* \[ ] Tests cover approve/reject/expire.

\---

## 10\. Fase 7 - Live Profile Promotion/Demotion Lifecycle

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_profile\_lifecycle.py
```

Profile states:

* \[ ] live\_locked;
* \[ ] dry\_run\_only;
* \[ ] first\_order\_only;
* \[ ] controlled\_level\_1;
* \[ ] controlled\_level\_2;
* \[ ] controlled\_level\_3;
* \[ ] paused\_for\_review;
* \[ ] demoted;
* \[ ] blocked;
* \[ ] expired;
* \[ ] emergency\_blocked.

Lifecycle actions:

* \[ ] promote with approval;
* \[ ] demote automatically on blocker;
* \[ ] pause for review;
* \[ ] expire after time/no evidence;
* \[ ] rollback to previous safe profile;
* \[ ] clone profile with proposed limits;
* \[ ] write profile migration report.

Rules:

* \[ ] Promotion never happens automatically.
* \[ ] Demotion/block can happen automatically.
* \[ ] Profile edit disarms active live session.
* \[ ] Profile state change audited.

Acceptatiecriteria:

* \[ ] State transitions validated.
* \[ ] Promotion requires approval.
* \[ ] Demotion can be automatic on blocker.
* \[ ] Rollback works.
* \[ ] Tests cover lifecycle.

\---

## 11\. Fase 8 - Risk Preset Proposal Builder

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/risk\_preset\_proposals.py
```

Proposal types:

* \[ ] reduce order size;
* \[ ] reduce max session exposure;
* \[ ] reduce max session orders;
* \[ ] reduce max loss;
* \[ ] lower spread cap;
* \[ ] lower stale data max age;
* \[ ] lower slippage cap;
* \[ ] keep same;
* \[ ] request more demo/paper validation;
* \[ ] block live.

Outputs:

* \[ ] proposed profile patch;
* \[ ] proposed risk preset patch;
* \[ ] explanation;
* \[ ] evidence refs;
* \[ ] approval requirement;
* \[ ] rollback plan.

Acceptatiecriteria:

* \[ ] Proposals do not mutate active profile directly.
* \[ ] Increases require approval.
* \[ ] Unsafe proposals blocked.
* \[ ] Secret redaction works.
* \[ ] Tests cover proposal generation.

\---

## 12\. Fase 9 - Session Regression Comparator

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_session\_regression.py
```

Compare current live session against:

* \[ ] previous live sessions;
* \[ ] paper replay;
* \[ ] testnet rehearsal;
* \[ ] demo spot expected behavior;
* \[ ] Roadmap 118 first-order dry-run;
* \[ ] configured risk baseline.

Regression checks:

* \[ ] worse slippage;
* \[ ] worse fee drag;
* \[ ] more rejections;
* \[ ] more disarm triggers;
* \[ ] slower reconciliation;
* \[ ] poorer heartbeat;
* \[ ] worse drawdown;
* \[ ] unexpected order status;
* \[ ] higher spread at execution;
* \[ ] model/risk decision drift.

Acceptatiecriteria:

* \[ ] Comparator works with fixture sessions.
* \[ ] Regressions become findings.
* \[ ] Missing baseline becomes warning.
* \[ ] Report secret-free.
* \[ ] Tests cover regression cases.

\---

## 13\. Fase 10 - Live Governance Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_governance\_evidence.py
```

Bundle bevat:

* \[ ] safety contract;
* \[ ] live session review;
* \[ ] live session scorecards;
* \[ ] execution quality analytics;
* \[ ] risk limit calibration report;
* \[ ] scaling governance decision;
* \[ ] operator approval request/decision;
* \[ ] profile lifecycle report;
* \[ ] risk preset proposal;
* \[ ] regression comparator report;
* \[ ] audit hash chain;
* \[ ] no auto-scale proof;
* \[ ] no unattended live proof;
* \[ ] no secret proof;
* \[ ] hashes.

Output:

```text
data/live-trading/governance-evidence/<run\_id>/
  live\_governance\_evidence\_manifest.json
  live\_governance\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Evidence secret-free.
* \[ ] Evidence has manifest/hash.
* \[ ] Evidence can be verified.
* \[ ] Evidence states approval/rejection clearly.
* \[ ] Dashboard can download bundle.

\---

## 14\. Fase 11 - Dashboard V2 Live Governance Cockpit

Nieuwe routes/pages:

```text
/live/governance
/live/governance/reviews
/live/governance/scorecards
/live/governance/calibration
/live/governance/approvals
/live/governance/profile-lifecycle
/live/governance/regression
/live/governance/evidence
```

Panels:

* \[ ] latest live session review;
* \[ ] scorecard grade;
* \[ ] unresolved findings;
* \[ ] execution quality analytics;
* \[ ] risk calibration proposal;
* \[ ] scaling governance decision;
* \[ ] operator approval queue;
* \[ ] approval details;
* \[ ] profile lifecycle state;
* \[ ] regression comparator;
* \[ ] rollback/demotion actions;
* \[ ] evidence export;
* \[ ] no auto-scale banner.

UX rules:

* \[ ] next level button hidden until eligible;
* \[ ] approval requires exact phrase;
* \[ ] risk increases clearly marked;
* \[ ] demotion/block actions easier than promotion;
* \[ ] unresolved blockers always visible;
* \[ ] no unattended live statement visible.

Acceptatiecriteria:

* \[ ] Governance page loads.
* \[ ] Scorecard visible.
* \[ ] Approval queue visible.
* \[ ] Promotion blocked by default.
* \[ ] Browser smoke covers blocked and approval-preview flows.

\---

## 15\. Fase 12 - Live Governance API Routes

Nieuwe API routes:

```text
GET  /api/live-governance/status
POST /api/live-governance/review/run
GET  /api/live-governance/reviews
POST /api/live-governance/scorecards/generate
POST /api/live-governance/execution-quality/analyze
POST /api/live-governance/risk-calibration/run
POST /api/live-governance/scaling-decision
POST /api/live-governance/approval/request
POST /api/live-governance/approval/decide
POST /api/live-governance/profile-lifecycle/apply
POST /api/live-governance/risk-preset-proposal
POST /api/live-governance/regression/compare
POST /api/live-governance/evidence/export
WS   /ws/live-governance
```

API rules:

* \[ ] no route places orders;
* \[ ] no route starts live session;
* \[ ] approvals do not execute orders;
* \[ ] profile promotions require exact confirmation;
* \[ ] risk increases require explicit approval;
* \[ ] all responses redacted.

Acceptatiecriteria:

* \[ ] TestClient covers core routes.
* \[ ] Promotion blocked without approval.
* \[ ] Risk increase blocked without approval.
* \[ ] Routes never call order endpoints.
* \[ ] Secrets redacted.

\---

## 16\. Fase 13 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli live-governance-status --json
python -m binance\_spot\_bot.cli live-session-review --session <id> --json
python -m binance\_spot\_bot.cli live-session-scorecard --session <id> --json
python -m binance\_spot\_bot.cli live-execution-quality --session <id> --json
python -m binance\_spot\_bot.cli live-risk-calibration --session <id> --json
python -m binance\_spot\_bot.cli live-scaling-decision --profile <id> --json
python -m binance\_spot\_bot.cli live-approval-request --profile <id> --decision approve\_next\_level
python -m binance\_spot\_bot.cli live-approval-decide --request <id> --confirm I\_APPROVE\_THIS\_LIVE\_SCALING\_DECISION
python -m binance\_spot\_bot.cli live-profile-lifecycle --profile <id> --json
python -m binance\_spot\_bot.cli live-risk-preset-proposal --profile <id> --json
python -m binance\_spot\_bot.cli live-session-regression --session <id> --json
python -m binance\_spot\_bot.cli live-governance-evidence-export --profile <id>
python -m binance\_spot\_bot.cli dashboard-v2-live-governance-smoke --json
```

Acceptatiecriteria:

* \[ ] Commands work offline from evidence.
* \[ ] Commands support JSON.
* \[ ] Approval requires exact confirm.
* \[ ] Commands never place orders.
* \[ ] Commands redact secrets.

\---

## 17\. Fase 14 - Check-All Integration

Fast profile:

* \[ ] live governance modules import;
* \[ ] safety contract check;
* \[ ] scorecard fixture;
* \[ ] scaling decision fixture;
* \[ ] approval workflow fixture;
* \[ ] secret redaction tests;
* \[ ] no order endpoint call tests.

Deep profile:

* \[ ] live session evidence fixture;
* \[ ] full review pipeline;
* \[ ] execution quality report;
* \[ ] calibration report;
* \[ ] scaling decision blocked by default;
* \[ ] approval request/decision;
* \[ ] profile lifecycle update dry-run;
* \[ ] governance evidence export/verify;
* \[ ] Dashboard V2 governance browser smoke.

Acceptatiecriteria:

* \[ ] Fast check-all stays safe.
* \[ ] Deep profile proves governance flow.
* \[ ] Any auto-scale hard fails.
* \[ ] Any order endpoint call hard fails.
* \[ ] Any secret leak hard fails.

\---

## 18\. Fase 15 - UAT / Operator Workflow

UAT scenarios:

* \[ ] open live governance cockpit;
* \[ ] select live session evidence;
* \[ ] run session review;
* \[ ] generate scorecard;
* \[ ] inspect unresolved findings;
* \[ ] run risk calibration;
* \[ ] generate scaling decision;
* \[ ] request approval;
* \[ ] reject scaling due to warning;
* \[ ] approve repeat current level;
* \[ ] attempt next-level approval without enough evidence and verify block;
* \[ ] export governance evidence.

Acceptatiecriteria:

* \[ ] UAT confirms no auto-scale.
* \[ ] UAT confirms no order placement.
* \[ ] UAT confirms approval is explicit.
* \[ ] UAT confirms blockers are clear.
* \[ ] UAT evidence attached.

\---

## 19\. Fase 16 - Release / Knowledge / Test / Performance Integration

Roadmap 089:

* \[ ] release notes mention live governance and scaling approvals.
* \[ ] version manifest includes live governance schema.
* \[ ] migration notes include governance evidence path.

Roadmap 091:

* \[ ] knowledge graph maps live session evidence → review → scorecard → calibration → approval → lifecycle.
* \[ ] impact analysis detects risk/execution/session changes affecting governance.

Roadmap 092:

* \[ ] test selector chooses live governance tests for live\_trading governance modules.
* \[ ] risk/config/execution changes select governance tests.
* \[ ] dashboard live governance UI changes select browser smoke.

Roadmap 093:

* \[ ] performance budget for scorecard generation, calibration, evidence export and dashboard render.

Acceptatiecriteria:

* \[ ] Release evidence includes governance evidence.
* \[ ] Knowledge graph updated.
* \[ ] Test selector protects governance code.
* \[ ] Performance reports include governance budgets.
* \[ ] No live order placement in governance.

\---

## 20\. Fase 17 - Scheduled Live Governance Reports

Scheduled jobs:

* \[ ] daily live governance status report;
* \[ ] weekly live session scorecard refresh;
* \[ ] weekly scaling decision dry-run;
* \[ ] weekly risk calibration dry-run;
* \[ ] weekly profile lifecycle health check;
* \[ ] monthly governance evidence export.

Metrics:

* \[ ] latest session grade;
* \[ ] unresolved findings count;
* \[ ] current scaling level;
* \[ ] eligible/not eligible state;
* \[ ] approval request count;
* \[ ] rejected approval count;
* \[ ] demotion/block count;
* \[ ] risk calibration recommendations;
* \[ ] evidence export status;
* \[ ] no auto-scale proof.

Acceptatiecriteria:

* \[ ] Scheduled jobs never place orders.
* \[ ] Reports are secret-free.
* \[ ] Dashboard can show reports.
* \[ ] Check-all safe env preserved.

\---

## 21\. Tests

### Unit tests

* \[ ] `tests/test\_live\_scaling\_governance\_safety\_contract.py`
* \[ ] `tests/test\_live\_session\_review.py`
* \[ ] `tests/test\_live\_session\_scorecards.py`
* \[ ] `tests/test\_live\_execution\_quality.py`
* \[ ] `tests/test\_risk\_limit\_calibration.py`
* \[ ] `tests/test\_scaling\_governance.py`
* \[ ] `tests/test\_operator\_approval\_workflow.py`
* \[ ] `tests/test\_live\_profile\_lifecycle.py`
* \[ ] `tests/test\_risk\_preset\_proposals.py`
* \[ ] `tests/test\_live\_session\_regression.py`
* \[ ] `tests/test\_live\_governance\_evidence.py`
* \[ ] `tests/test\_live\_governance\_api.py`

### Integration tests

* \[ ] Load live session evidence fixture.
* \[ ] Run session review.
* \[ ] Generate scorecard.
* \[ ] Run execution quality analytics.
* \[ ] Generate calibration report.
* \[ ] Generate scaling decision.
* \[ ] Create approval request.
* \[ ] Approve/reject with exact confirmation.
* \[ ] Apply profile lifecycle dry-run.
* \[ ] Export governance evidence.

### Browser smoke

* \[ ] `/live/governance` loads.
* \[ ] session review panel visible.
* \[ ] scorecard panel visible.
* \[ ] calibration panel visible.
* \[ ] scaling decision panel visible.
* \[ ] approval queue visible.
* \[ ] profile lifecycle panel visible.
* \[ ] evidence export visible.
* \[ ] no auto-scale banner visible.
* \[ ] no order execute button visible.

### Safety tests

* \[ ] Governance routes never place orders.
* \[ ] Auto-scale impossible.
* \[ ] Promotion blocked without approval.
* \[ ] Promotion blocked with P0/P1 finding.
* \[ ] Risk increase blocked without approval.
* \[ ] Evidence hash failure blocks promotion.
* \[ ] Secret redaction works.
* \[ ] Financial advice wording blocked.
* \[ ] Check-all safe env preserved.

\---

## 22\. Docs

Nieuwe docs:

```text
docs/live-trading/live-scaling-governance-safety-contract.md
docs/live-trading/live-session-review.md
docs/live-trading/live-session-scorecards.md
docs/live-trading/live-execution-quality.md
docs/live-trading/risk-limit-calibration.md
docs/live-trading/scaling-governance.md
docs/live-trading/operator-approval-workflow.md
docs/live-trading/live-profile-lifecycle.md
docs/live-trading/risk-preset-proposals.md
docs/live-trading/live-session-regression.md
docs/live-trading/live-governance-evidence.md
docs/live-trading/dashboard-live-governance-cockpit.md
```

README updates:

* \[ ] Live scaling governance overview.
* \[ ] No automatic scale-up.
* \[ ] Live session scorecards.
* \[ ] Risk calibration proposals.
* \[ ] Operator approval workflow.
* \[ ] Profile lifecycle.
* \[ ] Governance evidence export.
* \[ ] No unattended live statement.

\---

## 23\. Codex bouwvolgorde

### PR 1 - Safety Contract + Live Session Review Schema

* \[ ] `docs/live-trading/live-scaling-governance-safety-contract.md`
* \[ ] `live\_trading/live\_session\_review.py`
* \[ ] review validation tests.
* \[ ] evidence missing/blocker tests.

### PR 2 - Live Session Scorecards

* \[ ] `live\_session\_scorecards.py`
* \[ ] score dimensions/grades.
* \[ ] hard blocker tests.

### PR 3 - Execution Quality Analytics

* \[ ] `live\_execution\_quality.py`
* \[ ] slippage/fee/spread/latency reports.
* \[ ] fixture tests.

### PR 4 - Risk Limit Calibration

* \[ ] `risk\_limit\_calibration.py`
* \[ ] proposal-only calibration.
* \[ ] risk increase approval-required tests.

### PR 5 - Scaling Governance Decision Engine

* \[ ] `scaling\_governance.py`
* \[ ] no level skip.
* \[ ] no auto-approval tests.

### PR 6 - Operator Approval Workflow

* \[ ] `operator\_approval\_workflow.py`
* \[ ] approval token/expiry/audit tests.

### PR 7 - Profile Lifecycle + Risk Preset Proposals

* \[ ] `live\_profile\_lifecycle.py`
* \[ ] `risk\_preset\_proposals.py`
* \[ ] promotion/demotion/rollback tests.

### PR 8 - Regression Comparator + Evidence

* \[ ] `live\_session\_regression.py`
* \[ ] `live\_governance\_evidence.py`
* \[ ] evidence export/verify tests.

### PR 9 - Dashboard Governance Cockpit + API

* \[ ] API routes.
* \[ ] Dashboard V2 governance pages.
* \[ ] browser smoke.

### PR 10 - CLI + Check-All + Docs + UAT + Integrations

* \[ ] CLI commands.
* \[ ] check-all profiles.
* \[ ] docs.
* \[ ] UAT scenarios.
* \[ ] release/knowledge/test/performance integration.
* \[ ] scheduled reports.

\---

## 24\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 120 PR 1: Live Scaling Governance Safety Contract + Live Session Review Schema.

Maak docs/live-trading/live-scaling-governance-safety-contract.md.

Maak src/binance\_spot\_bot/live\_trading/live\_session\_review.py met:
- LiveSessionReview
- LiveSessionReviewInput
- LiveSessionReviewFinding
- LiveSessionReviewScore
- LiveSessionReviewReport
- validate\_live\_session\_review\_input(...)
- live\_session\_review\_to\_dict(...)
- write\_live\_session\_review\_report(...)

Review input moet minimaal ondersteunen:
- live\_session\_evidence\_manifest\_path
- session\_plan\_path
- order\_lifecycle\_paths
- reconciliation\_report\_paths
- heartbeat\_report\_paths
- disarm\_event\_paths
- circuit\_breaker\_report\_paths
- audit\_log\_path
- risk\_limits\_used
- scaling\_level\_used
- operator\_notes optional

Review report moet bevatten:
- review\_id
- session\_id
- evidence\_integrity\_status
- findings
- blockers
- warnings
- score\_summary
- eligible\_for\_scorecard
- eligible\_for\_scaling\_review
- no\_auto\_scale\_statement
- not\_financial\_advice\_statement
- secret\_redaction\_status
- created\_at\_ms

Validatie moet blokkeren op:
- missing live session evidence manifest
- missing session plan
- missing reconciliation report when live orders exist
- unknown order state
- unreconciled order
- evidence hash mismatch
- secret-like values
- buy/sell/profit guarantee wording
- no\_auto\_scale\_statement ontbreekt
- not\_financial\_advice\_statement ontbreekt

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
- valid review input
- missing evidence blocks
- missing reconciliation blocks when orders exist
- unknown order state blocks
- unreconciled order blocks
- evidence hash mismatch blocks
- secret-like values worden geredact
- advice/profit wording blocked
- JSON serialization
- eligible\_for\_scaling\_review false by default
- no\_auto\_scale\_statement aanwezig
```

Waarom eerst:

* Na controlled live sessions moet je eerst evidence kunnen reviewen voordat je überhaupt scorecards, calibration of scaling governance bouwt.
* Het is read-only en raakt execution/runtime/frontend niet.
* Het voorkomt automatische scale-up.
* Daarna kunnen scorecards, risk calibration en approval workflows veilig op review reports bouwen.

\---

## 25\. Definition of Done

Roadmap 120 is klaar als:

* \[ ] Live Scaling Governance Safety Contract bestaat.
* \[ ] Live Session Review Schema werkt.
* \[ ] Live Session Scorecard Engine werkt.
* \[ ] Live Execution Quality Analytics werkt.
* \[ ] Live Risk Limit Calibration werkt.
* \[ ] Scaling Governance Decision Engine werkt.
* \[ ] Operator Approval Workflow werkt.
* \[ ] Live Profile Promotion/Demotion Lifecycle werkt.
* \[ ] Risk Preset Proposal Builder werkt.
* \[ ] Session Regression Comparator werkt.
* \[ ] Live Governance Evidence Bundle werkt.
* \[ ] Dashboard V2 Live Governance Cockpit werkt.
* \[ ] Live Governance API Routes werken.
* \[ ] CLI commands werken.
* \[ ] Check-All Integration werkt.
* \[ ] UAT/Operator Workflow werkt.
* \[ ] Release/Knowledge/Test/Performance integration werkt.
* \[ ] Scheduled Live Governance Reports werken.
* \[ ] Tests bewijzen geen auto-scale.
* \[ ] Tests bewijzen governance routes nooit orders plaatsen.
* \[ ] Tests bewijzen promotion approval vereist.
* \[ ] Tests bewijzen P0/P1 findings promotion blokkeren.
* \[ ] Tests bewijzen evidence hash failure promotion blokkeert.
* \[ ] Tests bewijzen secrets redacted zijn.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Roadmap 120 kan na uitvoering naar `Voltooid docs`.

\---

## 26\. Verwachte Roadmap 121 daarna

Als Roadmap 120 groen is:

```text
Roadmap 121 - Live Operations Runbook Automation, Incident Response, Rollback Drills \& Post-Trade Forensics
```

Mogelijke inhoud:

* \[ ] incident response workflows;
* \[ ] live rollback drills;
* \[ ] post-trade forensic analysis;
* \[ ] audit timeline reconstruction;
* \[ ] emergency stop drills;
* \[ ] operator runbook automation;
* \[ ] still no unattended live.

```

Als Roadmap 120 blockers vindt:

```text
Roadmap 121 - Live Governance Blocker Burn-Down, Scorecard Calibration \& Approval Workflow Hardening
```

Mogelijke inhoud:

* \[ ] scorecard blockers oplossen;
* \[ ] calibration logic verbeteren;
* \[ ] approval workflow UX verbeteren;
* \[ ] evidence hash failures oplossen;
* \[ ] profile lifecycle hardening;
* \[ ] live blijft capped/locked.

```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Live performance review, scorecards, risk calibration and approvals.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.

