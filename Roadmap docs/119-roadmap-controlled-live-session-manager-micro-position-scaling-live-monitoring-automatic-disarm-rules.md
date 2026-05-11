# Roadmap 119 - Controlled Live Session Manager, Micro-Position Scaling, Live Monitoring \& Automatic Disarm Rules

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/119-roadmap-controlled-live-session-manager-micro-position-scaling-live-monitoring-automatic-disarm-rules.md
```

## Samenvatting

Roadmap 116 maakt de bot een one-click app met één Dashboard V2 Control Center.  
Roadmap 117 bouwt de demo-spot-data → dataset quality → model/strategy validation → paper replay → testnet promotion pipeline.  
Roadmap 118 bouwt de eerste live-safety laag: live dry-run, read-only account verification, order preview, sizing guard, kill-switch/cancel drill en een tiny capped first-order gate.

Roadmap 119 is de beste vervolgstap: **niet onbeperkt live traden, maar gecontroleerde live sessies bouwen**. Na een geslaagde first-order gate mag de bot alleen binnen handmatig geactiveerde micro-live sessies handelen met harde budgets, monitoring, reconciliation, circuit breakers en automatische disarm rules.

De kern:

```text
Roadmap 117 evidence
→ Roadmap 118 first-order evidence
→ controlled live session plan
→ micro-position budget
→ manually armed live session
→ max N capped orders
→ reconciliation after every order
→ live monitoring heartbeat
→ automatic disarm rules
→ session evidence
→ scaling only after review
```

Belangrijk: dit is nog steeds geen volledig autonome live bot. Live blijft handmatig geactiveerd, klein, gecontroleerd, geaudit, stopbaar en automatisch disarmed bij risico, stale data, configwijziging, restart, evidenceproblemen, unknown order state of connectivity issues.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 119`, `119-roadmap`, `Controlled Live Session Manager`, `Micro-Position Scaling`, `Automatic Disarm Rules` en `Live Monitoring`.
* \[x] Geen bestaande Roadmap 119 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 118 is lokaal aangemaakt als Live Trading Dry-Run, Read-Only Account Verification, Order Preview \& Minimal Real-Order Safety Layer.

### Codebasecontrole

Breed bekeken met focus op live execution, risk limits, signed endpoints, session store, audit redaction en runtime safety:

* \[x] `src/binance\_spot\_bot/execution.py`
* \[x] `src/binance\_spot\_bot/config.py`
* \[x] `src/binance\_spot\_bot/binance.py`
* \[x] `src/binance\_spot\_bot/risk.py`
* \[x] `src/binance\_spot\_bot/session\_store.py`
* \[x] `src/binance\_spot\_bot/audit.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] roadmaplijn 104-118.

### Belangrijke conclusies

* \[x] `ExecutionEngine` ondersteunt disabled, paper, demo/testnet guarded flows en blokkeert live order placement bewust tot een aparte manual implementation step.
* \[x] `BotSettings.validate\_live\_readiness()` heeft al live voorwaarden: `APP\_ENV=live`, `LIVE\_TRADING\_ENABLED=true`, `KILL\_SWITCH=false`, manual approval phrase, risk limits en credentials.
* \[x] `BinanceSpotAdapter` bevat public endpoints én signed endpoints zoals account, test order, place order, cancel, query order en open orders.
* \[x] `RiskEngine` heeft al belangrijke blockers: kill switch, lage confidence, max trades, max position, max daily loss, stale data, spread en balance checks.
* \[x] `SessionStore` kan snapshots, fills, alerts, orders, heartbeats en session summaries opslaan.
* \[x] `AuditLog` redigeert secret-like velden zoals API key, secret, signature, authorization en X-MBX-APIKEY.

### Belangrijkste gat na Roadmap 118

* \[ ] Geen controlled live session manager.
* \[ ] Geen per-session live budget.
* \[ ] Geen micro-position scaling.
* \[ ] Geen live order lifecycle tracker.
* \[ ] Geen reconciliation verplichting vóór een volgende order.
* \[ ] Geen automatic disarm rule engine.
* \[ ] Geen live heartbeat monitor.
* \[ ] Geen live circuit breakers.
* \[ ] Geen live session cockpit in Dashboard V2.
* \[ ] Geen live session evidence bundle.
* \[ ] Geen scaling review gate.

\---

## 1\. Hoofddoel Roadmap 119

Maak gecontroleerde live sessies mogelijk:

```text
live evidence
→ live session plan
→ session budget
→ manual arm
→ capped order execution
→ reconciliation
→ heartbeat monitoring
→ automatic disarm
→ evidence
```

Na Roadmap 119 moet de bot:

* \[ ] live sessies kunnen plannen met vaste budgets;
* \[ ] live sessies alleen handmatig kunnen armeren;
* \[ ] micro-position scaling levels afdwingen;
* \[ ] max orders per live session afdwingen;
* \[ ] max quote exposure per live session afdwingen;
* \[ ] max loss per session afdwingen;
* \[ ] order lifecycle en exchange status volgen;
* \[ ] account/order reconciliation na elke live order verplichten;
* \[ ] automatisch disarmen bij hard-risk events;
* \[ ] live monitoring in Dashboard V2 tonen;
* \[ ] live session evidence exporteren;
* \[ ] scaling pas toestaan na review/evidence.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen one-click launcher opnieuw bouwen.
* \[ ] Geen Roadmap 117 demo-data pipeline opnieuw bouwen.
* \[ ] Geen Roadmap 118 first-order gate opnieuw bouwen.
* \[ ] Geen Binance adapter herschrijven.
* \[ ] Geen unattended live trading.
* \[ ] Geen live auto-start.
* \[ ] Geen live vanuit launcher.
* \[ ] Geen onbeperkte order loops.
* \[ ] Geen onbeperkte position sizing.
* \[ ] Geen martingale/grid/averaging-down.
* \[ ] Geen financial advice.
* \[ ] Geen raw secrets in logs/evidence/dashboard.

Wel doen:

* \[ ] live session schema;
* \[ ] session budget engine;
* \[ ] micro-position scaling;
* \[ ] live order lifecycle tracker;
* \[ ] account/order reconciliation;
* \[ ] automatic disarm rules;
* \[ ] live monitoring/cockpit;
* \[ ] live session evidence;
* \[ ] scaling review gate;
* \[ ] fake adapter tests;
* \[ ] check-all/browser smoke/UAT.

\---

## 3\. Fase 0 - Controlled Live Session Safety Contract

Nieuw docbestand:

```text
docs/live-trading/controlled-live-session-safety-contract.md
```

Regels:

* \[ ] Live sessions zijn standaard disabled.
* \[ ] Live sessions starten nooit via launcher.
* \[ ] Live sessions starten nooit via normale Start-knop.
* \[ ] Elke live session vereist handmatige arm.
* \[ ] Elke live session vereist Roadmap 117 evidence.
* \[ ] Elke live session vereist Roadmap 118 first-order/live dry-run evidence.
* \[ ] Elke live session heeft max orders, max quote exposure, max loss en max duration.
* \[ ] Elke live order heeft preview hash.
* \[ ] Elke live order heeft session token.
* \[ ] Elke live order wordt gereconciled.
* \[ ] Volgende order blijft geblokkeerd tot reconciliation pass.
* \[ ] Disarm automatisch op restart, profile/config/key change, stale data, high spread, loss limit, connectivity issue, reconciliation mismatch, unknown order state, unexpected open order of kill switch.
* \[ ] Geen raw secrets in logs/dashboard/evidence.
* \[ ] Geen financieel advies.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen launcher/normal Start geen live session kunnen starten.
* \[ ] Tests bewijzen session budgets verplicht zijn.
* \[ ] Tests bewijzen disarm rules verplicht zijn.
* \[ ] Tests bewijzen evidence secret-free is.

\---

## 4\. Fase 1 - Live Session Plan Schema

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_session\_plan.py
```

Dataclasses:

* \[ ] `LiveSessionPlan`
* \[ ] `LiveSessionBudget`
* \[ ] `LiveSessionSymbolScope`
* \[ ] `LiveSessionRiskScope`
* \[ ] `LiveSessionEvidenceRefs`
* \[ ] `LiveSessionValidationResult`
* \[ ] `LiveSessionPlanReport`

Belangrijkste velden:

* \[ ] session\_plan\_id;
* \[ ] profile\_id;
* \[ ] symbol;
* \[ ] allowed\_sides;
* \[ ] allowed\_order\_types;
* \[ ] max\_session\_orders;
* \[ ] max\_session\_quote\_exposure;
* \[ ] max\_single\_order\_quote;
* \[ ] max\_session\_loss\_quote;
* \[ ] max\_daily\_loss\_quote;
* \[ ] max\_spread\_bps;
* \[ ] max\_data\_age\_ms;
* \[ ] max\_session\_duration\_minutes;
* \[ ] max\_open\_orders;
* \[ ] require\_preview\_hash;
* \[ ] require\_arm\_token;
* \[ ] require\_reconciliation\_after\_each\_order;
* \[ ] require\_kill\_switch\_drill;
* \[ ] require\_cancel\_drill;
* \[ ] evidence\_refs;
* \[ ] no\_unattended\_live\_statement;
* \[ ] not\_financial\_advice\_statement;
* \[ ] created\_at\_ms;
* \[ ] expires\_at\_ms.

Validation blocks:

* \[ ] missing Roadmap 117 evidence ref;
* \[ ] missing Roadmap 118 evidence ref;
* \[ ] invalid budgets;
* \[ ] missing preview hash requirement;
* \[ ] missing arm token requirement;
* \[ ] missing reconciliation requirement;
* \[ ] unsafe order type;
* \[ ] empty symbol;
* \[ ] secret-like values;
* \[ ] advice/profit wording.

\---

## 5\. Fase 2 - Live Session Store

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_session\_store.py
```

Storage:

```text
data/live-trading/sessions/
  plans/
  active/
  completed/
  failed/
  evidence/
```

Taken:

* \[ ] save/load/list session plans;
* \[ ] create live session instance;
* \[ ] update session state;
* \[ ] record live order lifecycle events;
* \[ ] record reconciliation results;
* \[ ] record disarm events;
* \[ ] archive completed sessions;
* \[ ] verify manifest/hash;
* \[ ] export summary.

Acceptatiecriteria:

* \[ ] Store is local-only.
* \[ ] Path traversal blocked.
* \[ ] Hash manifest generated.
* \[ ] Secrets redacted.
* \[ ] Tests use temp dirs.

\---

## 6\. Fase 3 - Live Session State Machine

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_session\_manager.py
```

States:

* \[ ] locked;
* \[ ] plan\_required;
* \[ ] plan\_validated;
* \[ ] evidence\_verified;
* \[ ] account\_verified;
* \[ ] dry\_run\_required;
* \[ ] ready\_to\_arm;
* \[ ] armed;
* \[ ] running;
* \[ ] waiting\_for\_reconciliation;
* \[ ] paused\_by\_rule;
* \[ ] disarming;
* \[ ] disarmed;
* \[ ] completed;
* \[ ] failed;
* \[ ] emergency\_stopped.

Acceptatiecriteria:

* \[ ] Invalid transitions blocked.
* \[ ] Restart forces locked/disarmed.
* \[ ] Config/profile edit forces disarmed.
* \[ ] Kill switch forces emergency stopped.
* \[ ] Tests cover transition graph.

\---

## 7\. Fase 4 - Micro-Position Scaling Policy

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/micro\_position\_scaling.py
```

Scaling levels:

* \[ ] Level 0: dry-run only.
* \[ ] Level 1: exactly one tiny order, disarm after order.
* \[ ] Level 2: micro session, max 2-3 tiny orders, reconciliation after every order.
* \[ ] Level 3: cautious session, still small exposure, only after multiple successful Level 2 sessions.

Scaling requirements:

* \[ ] prior session evidence;
* \[ ] zero unreconciled orders;
* \[ ] no emergency stop in recent sessions;
* \[ ] max drawdown below threshold;
* \[ ] no critical disarm triggers;
* \[ ] operator review.

Acceptatiecriteria:

* \[ ] Level cannot skip.
* \[ ] Failed session blocks scaling.
* \[ ] Missing evidence blocks scaling.
* \[ ] Scaling report explains why.
* \[ ] Tests cover level transitions.

\---

## 8\. Fase 5 - Live Session Budget Engine

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_session\_budget.py
```

Budgets:

* \[ ] max orders per session;
* \[ ] max single order quote;
* \[ ] max total quote exposure;
* \[ ] max current open quote exposure;
* \[ ] max realized session loss;
* \[ ] max unrealized drawdown;
* \[ ] max spread;
* \[ ] max data age;
* \[ ] max order retry attempts;
* \[ ] max open orders;
* \[ ] max session duration;
* \[ ] max API errors;
* \[ ] max reconciliation mismatches.

Decisions:

* \[ ] allow;
* \[ ] warn;
* \[ ] block;
* \[ ] disarm.

Acceptatiecriteria:

* \[ ] Budget decisions deterministic.
* \[ ] Hard budget breach disarms.
* \[ ] Warnings visible in dashboard.
* \[ ] Decimal safe.
* \[ ] Tests cover all budgets.

\---

## 9\. Fase 6 - Live Order Lifecycle Tracker

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_order\_lifecycle.py
```

States:

* \[ ] preview\_created;
* \[ ] preview\_validated;
* \[ ] submitted;
* \[ ] accepted;
* \[ ] partially\_filled;
* \[ ] filled;
* \[ ] rejected;
* \[ ] canceled;
* \[ ] expired;
* \[ ] unknown;
* \[ ] reconciliation\_required;
* \[ ] reconciled;
* \[ ] failed.

Acceptatiecriteria:

* \[ ] Lifecycle deterministic.
* \[ ] Unknown status triggers disarm.
* \[ ] Missing exchange order id triggers reconciliation warning.
* \[ ] Redaction tests pass.
* \[ ] Tests cover partial/rejected/canceled.

\---

## 10\. Fase 7 - Live Reconciliation Loop

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_reconciliation.py
```

Checks:

* \[ ] query submitted order;
* \[ ] compare local lifecycle vs exchange status;
* \[ ] compare executed quantity;
* \[ ] compare fills if available;
* \[ ] compare account balances;
* \[ ] compare open orders;
* \[ ] detect unexpected open order;
* \[ ] detect balance drift;
* \[ ] detect duplicate client order id.

Rules:

* \[ ] reconciliation required after every live order;
* \[ ] mismatch triggers disarm;
* \[ ] unknown order state triggers emergency stop recommendation;
* \[ ] no next live order until reconciliation pass.

Acceptatiecriteria:

* \[ ] Works with fake adapter.
* \[ ] Mismatch disarms session.
* \[ ] Unexpected open order disarms.
* \[ ] Reports redacted.
* \[ ] Tests cover mismatch cases.

\---

## 11\. Fase 8 - Live Monitoring Heartbeat

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_monitoring.py
```

Heartbeat checks:

* \[ ] backend alive;
* \[ ] dashboard/WebSocket alive;
* \[ ] exchange server time reachable;
* \[ ] market data fresh;
* \[ ] spread under cap;
* \[ ] account verification fresh;
* \[ ] session budget remaining;
* \[ ] order lifecycle stable;
* \[ ] reconciliation status;
* \[ ] kill switch false;
* \[ ] stop button reachable;
* \[ ] evidence writer healthy.

Statuses:

* \[ ] healthy;
* \[ ] degraded;
* \[ ] warning;
* \[ ] critical;
* \[ ] disarm\_required.

Acceptatiecriteria:

* \[ ] Heartbeat runs on timer.
* \[ ] Critical heartbeat triggers disarm.
* \[ ] Stale data triggers disarm.
* \[ ] Dashboard shows heartbeat.
* \[ ] Tests use fake clocks/adapters.

\---

## 12\. Fase 9 - Automatic Disarm Rule Engine

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/automatic\_disarm\_rules.py
```

Disarm triggers:

* \[ ] restart detected;
* \[ ] profile/config/key changed;
* \[ ] kill switch toggled;
* \[ ] stop/emergency stop clicked;
* \[ ] market data stale;
* \[ ] spread too high;
* \[ ] API connectivity lost;
* \[ ] account verification stale;
* \[ ] order rejection;
* \[ ] unknown order status;
* \[ ] reconciliation mismatch;
* \[ ] unexpected open order;
* \[ ] balance drift;
* \[ ] max session orders reached;
* \[ ] max session loss reached;
* \[ ] max daily loss reached;
* \[ ] max duration reached;
* \[ ] evidence writer failure;
* \[ ] dashboard disconnected too long;
* \[ ] manual disarm.

Acceptatiecriteria:

* \[ ] Every trigger maps to action.
* \[ ] Hard triggers disarm immediately.
* \[ ] Disarm event audited.
* \[ ] Dashboard shows disarm reason.
* \[ ] Tests cover every trigger.

\---

## 13\. Fase 10 - Live Session Circuit Breakers

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_circuit\_breakers.py
```

Circuit breakers:

* \[ ] loss breaker;
* \[ ] spread breaker;
* \[ ] stale-data breaker;
* \[ ] connectivity breaker;
* \[ ] order-rejection breaker;
* \[ ] reconciliation breaker;
* \[ ] unknown-order breaker;
* \[ ] open-order breaker;
* \[ ] heartbeat breaker;
* \[ ] evidence-writer breaker;
* \[ ] operator-disconnect breaker.

Actions:

* \[ ] warn;
* \[ ] pause;
* \[ ] block next order;
* \[ ] disarm;
* \[ ] emergency stop recommendation.

\---

## 14\. Fase 11 - Controlled Live Order Executor

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/controlled\_live\_executor.py
```

Executor regels:

* \[ ] wraps Roadmap 118 first-order gate;
* \[ ] session-level max N orders;
* \[ ] preview required for every order;
* \[ ] session token required;
* \[ ] budget allow required;
* \[ ] disarm rules pass required;
* \[ ] heartbeat healthy required;
* \[ ] submit order through gated adapter;
* \[ ] track lifecycle;
* \[ ] force reconciliation before next order;
* \[ ] disarm on completion or issue.

Forbidden:

* \[ ] no unattended loops;
* \[ ] no order without preview;
* \[ ] no order without budget;
* \[ ] no order after disarm;
* \[ ] no retry place order without manual review;
* \[ ] no live trading from normal runtime loop unless live session manager explicitly owns it.

\---

## 15\. Fase 12 - Live Session Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_session\_evidence.py
```

Bundle bevat:

* \[ ] safety contract;
* \[ ] live session plan;
* \[ ] session budget report;
* \[ ] scaling policy report;
* \[ ] session state transitions;
* \[ ] order lifecycle logs;
* \[ ] reconciliation reports;
* \[ ] heartbeat reports;
* \[ ] disarm rule report;
* \[ ] circuit breaker report;
* \[ ] executor report;
* \[ ] account verification refs;
* \[ ] Roadmap 117 evidence refs;
* \[ ] Roadmap 118 evidence refs;
* \[ ] audit hash chain;
* \[ ] order responses redacted;
* \[ ] emergency stop proof if any;
* \[ ] no unattended live proof;
* \[ ] secret redaction proof;
* \[ ] hashes.

Output:

```text
data/live-trading/session-evidence/<run\_id>/
  live\_session\_evidence\_manifest.json
  live\_session\_evidence\_summary.md
  files/
```

\---

## 16\. Fase 13 - Dashboard V2 Live Session Cockpit

Nieuwe routes/pages:

```text
/live/session
/live/session/plan
/live/session/budget
/live/session/orders
/live/session/reconciliation
/live/session/monitoring
/live/session/disarm
/live/session/evidence
```

Panels:

* \[ ] locked/disarmed/live status banner;
* \[ ] session plan card;
* \[ ] evidence prerequisites;
* \[ ] scaling level;
* \[ ] budget remaining;
* \[ ] heartbeat status;
* \[ ] current order lifecycle;
* \[ ] reconciliation status;
* \[ ] open order status;
* \[ ] circuit breakers;
* \[ ] disarm reason timeline;
* \[ ] emergency stop button;
* \[ ] manual disarm button;
* \[ ] session evidence export;
* \[ ] no unattended live statement.

UX rules:

* \[ ] no normal Start Live button;
* \[ ] “Arm Controlled Live Session” only after all gates;
* \[ ] every order preview shown before execution;
* \[ ] next order disabled until reconciliation;
* \[ ] emergency stop always visible;
* \[ ] disarm reason always visible.

\---

## 17\. Fase 14 - Live Session API Routes

Nieuwe API routes:

```text
GET  /api/live-session/status
POST /api/live-session/plan/validate
POST /api/live-session/create
POST /api/live-session/arm
POST /api/live-session/disarm
POST /api/live-session/emergency-stop
GET  /api/live-session/budget
GET  /api/live-session/scaling
GET  /api/live-session/orders
POST /api/live-session/orders/preview
POST /api/live-session/orders/execute
POST /api/live-session/orders/reconcile
GET  /api/live-session/heartbeat
GET  /api/live-session/disarm-rules
GET  /api/live-session/circuit-breakers
GET  /api/live-session/evidence
POST /api/live-session/evidence/export
WS   /ws/live-session
```

API rules:

* \[ ] execute order requires controlled live session armed;
* \[ ] execute order requires preview hash;
* \[ ] execute order requires budget allow;
* \[ ] execute order requires heartbeat healthy;
* \[ ] execute order requires no disarm trigger;
* \[ ] next order requires reconciliation pass;
* \[ ] emergency stop always available;
* \[ ] all responses redacted.

\---

## 18\. Fase 15 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli live-session-plan-validate --plan <path> --json
python -m binance\_spot\_bot.cli live-session-create --plan <path>
python -m binance\_spot\_bot.cli live-session-status --json
python -m binance\_spot\_bot.cli live-session-arm --session <id> --confirm I\_UNDERSTAND\_CONTROLLED\_LIVE\_SESSION\_RISK
python -m binance\_spot\_bot.cli live-session-disarm --session <id>
python -m binance\_spot\_bot.cli live-session-emergency-stop
python -m binance\_spot\_bot.cli live-session-budget --session <id> --json
python -m binance\_spot\_bot.cli live-session-scaling --json
python -m binance\_spot\_bot.cli live-session-order-preview --session <id> --json
python -m binance\_spot\_bot.cli live-session-order-execute --session <id> --preview <id> --confirm I\_UNDERSTAND\_THIS\_PLACES\_A\_REAL\_BINANCE\_SPOT\_ORDER
python -m binance\_spot\_bot.cli live-session-reconcile --session <id> --json
python -m binance\_spot\_bot.cli live-session-heartbeat --session <id> --json
python -m binance\_spot\_bot.cli live-session-evidence-export --session <id>
python -m binance\_spot\_bot.cli dashboard-v2-live-session-smoke --json
```

\---

## 19\. Fase 16 - Check-All Integration

Fast profile:

* \[ ] live session modules import;
* \[ ] safety contract check;
* \[ ] session plan schema tests;
* \[ ] scaling policy tests;
* \[ ] budget engine tests;
* \[ ] automatic disarm rule tests;
* \[ ] secret redaction tests.

Deep profile:

* \[ ] fake live session plan;
* \[ ] fake session creation;
* \[ ] fake order with Roadmap 118 evidence;
* \[ ] second order blocked until reconciliation;
* \[ ] fake reconciliation pass;
* \[ ] fake disarm trigger;
* \[ ] heartbeat critical disarm;
* \[ ] live session evidence export/verify;
* \[ ] Dashboard V2 live session browser smoke.

\---

## 20\. Fase 17 - UAT / Operator Workflow

UAT scenarios:

* \[ ] live session cockpit loads locked;
* \[ ] missing Roadmap 117/118 evidence blocks session;
* \[ ] create fake live session plan;
* \[ ] validate budget;
* \[ ] arm fake controlled session;
* \[ ] preview first order;
* \[ ] execute fake order once;
* \[ ] next order blocked until reconciliation;
* \[ ] reconciliation pass allows next preview;
* \[ ] max orders reached disarms;
* \[ ] stale data trigger disarms;
* \[ ] emergency stop disarms;
* \[ ] evidence export.

Acceptatiecriteria:

* \[ ] UAT confirms no unattended live.
* \[ ] UAT confirms max budget enforcement.
* \[ ] UAT confirms disarm triggers.
* \[ ] UAT confirms reconciliation before next order.
* \[ ] UAT evidence attached.

\---

## 21\. Fase 18 - Release / Knowledge / Test / Performance Integration

* \[ ] Release notes mention controlled live session manager.
* \[ ] Version manifest includes live session schema version.
* \[ ] Knowledge graph maps first-order evidence → session plan → budget → orders → reconciliation → disarm/evidence.
* \[ ] Impact analysis detects execution/binance/risk/session changes affecting live session safety.
* \[ ] Test selector chooses live session tests for live\_trading modules.
* \[ ] Execution/binance/config/risk changes select live safety tests.
* \[ ] Performance budget for heartbeat loop, reconciliation, evidence export and order preview.
* \[ ] Dashboard live cockpit render budget.

\---

## 22\. Fase 19 - Scheduled Live Session Safety Reports

Scheduled jobs:

* \[ ] daily live session plan validation;
* \[ ] daily live profile locked-state check;
* \[ ] weekly fake live session smoke;
* \[ ] weekly disarm rule test;
* \[ ] weekly reconciliation fake adapter test;
* \[ ] weekly emergency stop drill;
* \[ ] monthly live session evidence export.

Metrics:

* \[ ] valid session plan count;
* \[ ] last live session status;
* \[ ] disarm trigger count;
* \[ ] reconciliation mismatch count;
* \[ ] order count per session;
* \[ ] max exposure used;
* \[ ] max loss used;
* \[ ] heartbeat critical count;
* \[ ] emergency stop count;
* \[ ] evidence export status.

\---

## 23\. Tests

### Unit tests

* \[ ] `tests/test\_controlled\_live\_session\_safety\_contract.py`
* \[ ] `tests/test\_live\_session\_plan.py`
* \[ ] `tests/test\_live\_session\_store.py`
* \[ ] `tests/test\_live\_session\_manager.py`
* \[ ] `tests/test\_micro\_position\_scaling.py`
* \[ ] `tests/test\_live\_session\_budget.py`
* \[ ] `tests/test\_live\_order\_lifecycle.py`
* \[ ] `tests/test\_live\_reconciliation.py`
* \[ ] `tests/test\_live\_monitoring.py`
* \[ ] `tests/test\_automatic\_disarm\_rules.py`
* \[ ] `tests/test\_live\_circuit\_breakers.py`
* \[ ] `tests/test\_controlled\_live\_executor.py`
* \[ ] `tests/test\_live\_session\_evidence.py`
* \[ ] `tests/test\_live\_session\_api.py`

### Integration tests

* \[ ] Validate session plan fixture.
* \[ ] Create fake live session.
* \[ ] Arm fake controlled session.
* \[ ] Execute fake order within budget.
* \[ ] Block second order before reconciliation.
* \[ ] Reconcile fake order.
* \[ ] Execute second fake order if budget allows.
* \[ ] Disarm on stale data.
* \[ ] Disarm on reconciliation mismatch.
* \[ ] Disarm on max orders reached.
* \[ ] Emergency stop from any active state.
* \[ ] Export evidence.

### Browser smoke

* \[ ] `/live/session` loads.
* \[ ] locked banner visible.
* \[ ] budget panel visible.
* \[ ] scaling panel visible.
* \[ ] order lifecycle panel visible.
* \[ ] reconciliation panel visible.
* \[ ] disarm rules visible.
* \[ ] emergency stop visible.
* \[ ] evidence export visible.
* \[ ] no normal Start Live button visible.

### Safety tests

* \[ ] Launcher cannot start live session.
* \[ ] Normal dashboard Start cannot start live session.
* \[ ] Live session requires Roadmap 117/118 evidence refs.
* \[ ] Order requires preview hash.
* \[ ] Order requires budget allow.
* \[ ] Order requires healthy heartbeat.
* \[ ] Order after disarm blocked.
* \[ ] Next order before reconciliation blocked.
* \[ ] Max session orders enforced.
* \[ ] Max exposure enforced.
* \[ ] Secrets redacted.
* \[ ] Check-all safe env preserved.

\---

## 24\. Docs

Nieuwe docs:

```text
docs/live-trading/controlled-live-session-safety-contract.md
docs/live-trading/live-session-plan.md
docs/live-trading/live-session-store.md
docs/live-trading/live-session-manager.md
docs/live-trading/micro-position-scaling.md
docs/live-trading/live-session-budget.md
docs/live-trading/live-order-lifecycle.md
docs/live-trading/live-reconciliation.md
docs/live-trading/live-monitoring.md
docs/live-trading/automatic-disarm-rules.md
docs/live-trading/live-circuit-breakers.md
docs/live-trading/controlled-live-executor.md
docs/live-trading/live-session-evidence.md
docs/live-trading/dashboard-live-session-cockpit.md
```

README updates:

* \[ ] Controlled live sessions overview.
* \[ ] Manual arm only.
* \[ ] Micro-position scaling.
* \[ ] Reconciliation before next order.
* \[ ] Automatic disarm rules.
* \[ ] Emergency stop.
* \[ ] Evidence export.
* \[ ] No unattended live statement.

\---

## 25\. Codex bouwvolgorde

### PR 1 - Safety Contract + Live Session Plan Schema

* \[ ] `docs/live-trading/controlled-live-session-safety-contract.md`
* \[ ] `live\_trading/live\_session\_plan.py`
* \[ ] plan validation tests.
* \[ ] evidence refs required tests.

### PR 2 - Live Session Store + State Machine

* \[ ] `live\_session\_store.py`
* \[ ] `live\_session\_manager.py`
* \[ ] state transition tests.

### PR 3 - Micro-Position Scaling + Budget Engine

* \[ ] `micro\_position\_scaling.py`
* \[ ] `live\_session\_budget.py`
* \[ ] scaling/budget tests.

### PR 4 - Order Lifecycle + Reconciliation

* \[ ] `live\_order\_lifecycle.py`
* \[ ] `live\_reconciliation.py`
* \[ ] fake adapter reconciliation tests.

### PR 5 - Monitoring + Automatic Disarm + Circuit Breakers

* \[ ] `live\_monitoring.py`
* \[ ] `automatic\_disarm\_rules.py`
* \[ ] `live\_circuit\_breakers.py`
* \[ ] disarm trigger tests.

### PR 6 - Controlled Live Executor

* \[ ] `controlled\_live\_executor.py`
* \[ ] fake adapter max-N order tests.
* \[ ] no bypass tests.

### PR 7 - Live Session Evidence

* \[ ] `live\_session\_evidence.py`
* \[ ] evidence export/verify tests.
* \[ ] audit/redaction tests.

### PR 8 - Dashboard Live Session Cockpit + API

* \[ ] live session API routes.
* \[ ] Dashboard V2 live session pages.
* \[ ] browser smoke.

### PR 9 - CLI + Check-All

* \[ ] CLI commands.
* \[ ] check-all profiles.
* \[ ] fake live session deep smoke.

### PR 10 - Docs, UAT, Release/Knowledge/Test/Performance Integration

* \[ ] docs.
* \[ ] UAT scenarios.
* \[ ] release notes.
* \[ ] knowledge/test/performance integration.
* \[ ] scheduled reports.

\---

## 26\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 119 PR 1: Controlled Live Session Safety Contract + Live Session Plan Schema.

Maak docs/live-trading/controlled-live-session-safety-contract.md.

Maak src/binance\_spot\_bot/live\_trading/live\_session\_plan.py met:
- LiveSessionPlan
- LiveSessionBudget
- LiveSessionSymbolScope
- LiveSessionRiskScope
- LiveSessionEvidenceRefs
- LiveSessionValidationResult
- LiveSessionPlanReport
- validate\_live\_session\_plan(plan: LiveSessionPlan)
- live\_session\_plan\_to\_dict(...)
- write\_live\_session\_plan\_report(...)

LiveSessionPlan moet minimaal ondersteunen:
- session\_plan\_id
- profile\_id
- symbol
- allowed\_sides
- allowed\_order\_types
- max\_session\_orders
- max\_session\_quote\_exposure
- max\_single\_order\_quote
- max\_session\_loss\_quote
- max\_daily\_loss\_quote
- max\_spread\_bps
- max\_data\_age\_ms
- max\_session\_duration\_minutes
- max\_open\_orders
- require\_preview\_hash
- require\_arm\_token
- require\_reconciliation\_after\_each\_order
- require\_kill\_switch\_drill
- require\_cancel\_drill
- evidence\_refs
- no\_unattended\_live\_statement
- not\_financial\_advice\_statement
- created\_at\_ms
- expires\_at\_ms

Validation must block:
- missing Roadmap 117 evidence ref
- missing Roadmap 118 evidence ref
- max\_session\_orders <= 0
- max\_session\_quote\_exposure <= 0
- max\_single\_order\_quote <= 0
- max\_session\_loss\_quote <= 0
- max\_session\_duration\_minutes <= 0
- require\_preview\_hash=False
- require\_arm\_token=False
- require\_reconciliation\_after\_each\_order=False
- unsafe order type
- empty symbol
- buy/sell/profit guarantee wording
- secret-like values

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
- valid micro live session plan
- missing Roadmap 117 evidence blocked
- missing Roadmap 118 evidence blocked
- invalid budgets blocked
- missing preview hash requirement blocked
- missing arm token requirement blocked
- missing reconciliation requirement blocked
- unsafe order type blocked
- advice/profit wording blocked
- JSON serialization
- secret-like values worden geredact
```

Waarom eerst:

* Na de first-order gate mag live nooit meteen onbeperkt worden.
* Een live session plan legt budgets, evidence en safety rules machine-testbaar vast.
* Dit is read-only en raakt runtime/trading/frontend niet.
* Het is klein genoeg voor Codex.
* Daarna kunnen session manager, scaling, budget, reconciliation en disarm rules veilig op dit schema bouwen.

\---

## 27\. Definition of Done

Roadmap 119 is klaar als:

* \[ ] Controlled Live Session Safety Contract bestaat.
* \[ ] Live Session Plan Schema werkt.
* \[ ] Live Session Store werkt.
* \[ ] Live Session State Machine werkt.
* \[ ] Micro-Position Scaling Policy werkt.
* \[ ] Live Session Budget Engine werkt.
* \[ ] Live Order Lifecycle Tracker werkt.
* \[ ] Live Reconciliation Loop werkt.
* \[ ] Live Monitoring Heartbeat werkt.
* \[ ] Automatic Disarm Rule Engine werkt.
* \[ ] Live Session Circuit Breakers werken.
* \[ ] Controlled Live Order Executor werkt.
* \[ ] Live Session Evidence Bundle werkt.
* \[ ] Dashboard V2 Live Session Cockpit werkt.
* \[ ] Live Session API Routes werken.
* \[ ] CLI commands werken.
* \[ ] Check-All Integration werkt.
* \[ ] UAT/Operator Workflow werkt.
* \[ ] Release/Knowledge/Test/Performance integration werkt.
* \[ ] Scheduled Live Session Safety Reports werken.
* \[ ] Tests bewijzen geen unattended live.
* \[ ] Tests bewijzen normal Start/launcher nooit live session starten.
* \[ ] Tests bewijzen max budget en max orders afdwingen.
* \[ ] Tests bewijzen reconciliation verplicht is vóór volgende order.
* \[ ] Tests bewijzen disarm rules werken.
* \[ ] Tests bewijzen secrets redacted zijn.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Roadmap 119 kan na uitvoering naar `Voltooid docs`.

\---

## 28\. Verwachte Roadmap 120 daarna

Als Roadmap 119 groen is:

```text
Roadmap 120 - Live Session Performance Review, Scaling Governance, Risk Limit Calibration \& Operator Approval Workflow
```

Mogelijke inhoud:

* \[ ] live session performance review;
* \[ ] scaling approval workflow;
* \[ ] risk limit calibration from live micro sessions;
* \[ ] live session scorecards;
* \[ ] operator approval notes;
* \[ ] staged increase only after evidence;
* \[ ] still no unattended live.

```

Als Roadmap 119 blockers vindt:

```text
Roadmap 120 - Controlled Live Session Blocker Burn-Down, Reconciliation Reliability \& Disarm Rule Hardening
```

Mogelijke inhoud:

* \[ ] reconciliation mismatches oplossen;
* \[ ] disarm triggers verbeteren;
* \[ ] budget engine bugs oplossen;
* \[ ] fake adapter/live dry-run reliability;
* \[ ] dashboard cockpit blockers;
* \[ ] live blijft locked.

```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Controlled live session manager, micro scaling and automatic disarm.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.

