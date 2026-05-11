# Roadmap 118 - Live Trading Dry-Run, Read-Only Account Verification, Order Preview \& Minimal Real-Order Safety Layer

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/118-roadmap-live-trading-dry-run-read-only-account-verification-order-preview-minimal-real-order-safety-layer.md
```

## Samenvatting

Roadmap 116 maakt de bot bruikbaar als één lokale app:

```text
1 klikbaar startbestand
→ alles start samen
→ Dashboard V2 Control Center opent
→ profiel kiezen
→ config/API keys invullen
→ Start klikken
→ bot haalt data op
→ bot draait in gekozen profiel
```

Roadmap 117 bouwt daarna de noodzakelijke data- en trainingsbrug richting live:

```text
Demo spot data
→ dataset vault
→ dataset quality burn-down
→ feature/label dataset
→ model/strategy validation
→ paper replay
→ testnet promotion gate
→ live candidate gate
```

Roadmap 118 is de logische volgende stap: **live trading technisch voorbereiden zonder meteen gevaarlijk “auto-live” te bouwen**. De bot krijgt eerst live dry-run, live read-only account verification, API-permission checks, live order preview, first-order simulation, live kill-switch drills, cancel drills, audit/evidence en pas daarna een streng beperkte minimal real-order safety layer.

Belangrijk: live trading blijft standaard locked. Echte live order placement mag alleen na alle Roadmap 117 evidence plus Roadmap 118 live-dry-run gates. Geen unattended live. Geen launcher die live automatisch start. Geen “Start Live” zonder multi-step arm/confirm/review.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 118`, `118-roadmap`, `Live Trading Dry-Run`, `Read-Only Account Verification`, `Order Preview`, `Minimal Real-Order Safety Layer` en `tiny capped first order`.
* \[x] Geen bestaande Roadmap 118 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 117 is lokaal aangemaakt als Demo Spot Data Collection Sprint, Dataset Quality Burn-Down, Model Validation Improvement \& Testnet Promotion Gate.

### Codebasecontrole

Breed bekeken met focus op live safety, config, execution, signed endpoints, Binance adapter, TradingMode, demo/testnet/live gates, audit en evidence:

* \[x] `src/binance\_spot\_bot/config.py`
* \[x] `src/binance\_spot\_bot/types.py`
* \[x] `src/binance\_spot\_bot/binance.py`
* \[x] `src/binance\_spot\_bot/execution.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/risk.py`
* \[x] `src/binance\_spot\_bot/paper.py`
* \[x] `src/binance\_spot\_bot/paper\_accounting.py`
* \[x] `src/binance\_spot\_bot/session\_store.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] roadmaplijn 104-117.

### Belangrijke conclusies uit de codebase

* \[x] `TradingMode` bevat al `disabled`, `paper`, `testnet` en `live`.
* \[x] `BotSettings.validate\_live\_readiness()` blokkeert live als `APP\_ENV`, `LIVE\_TRADING\_ENABLED`, `KILL\_SWITCH`, `MANUAL\_LIVE\_APPROVAL`, risk limits of credentials niet kloppen.
* \[x] `BinanceSpotAdapter` heeft public data endpoints, read-only account endpoint, test order, place order, cancel order, order query en open orders.
* \[x] `\_assert\_signed\_order\_base\_url()` blokkeert signed order routes voor verkeerde base URLs/profiles.
* \[x] `ExecutionEngine` bouwt al orders, voert paper fills uit, ondersteunt demo/testnet guarded flow en blokkeert live order placement expliciet met `live order placement requires a separate manual implementation step`.
* \[x] De juiste volgende stap is daarom niet “alle live trading vrijgeven”, maar een aparte live safety layer rond:

  * dry-run;
  * read-only account verification;
  * order preview;
  * live permissions;
  * cancel drill;
  * kill-switch drill;
  * tiny capped first order gate.

### Belangrijkste gat na Roadmap 117

Na Roadmap 117 is er hopelijk genoeg demo/paper/testnet evidence. Maar er ontbreekt nog:

* \[ ] live dry-run mode;
* \[ ] live account read-only verification;
* \[ ] live API permission verifier;
* \[ ] live order preview zonder plaatsing;
* \[ ] live order sizing hard cap;
* \[ ] live first-order gate;
* \[ ] live cancel/emergency stop drill;
* \[ ] live session audit log;
* \[ ] live disarm on restart/config/risk warning;
* \[ ] live Dashboard V2 guarded workflow;
* \[ ] live evidence bundle;
* \[ ] live execution tests met fake adapter;
* \[ ] live execution code die niet door launcher of normale Start-knop kan worden geraakt.

Roadmap 118 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 118

Maak een gecontroleerde live-trading safety layer:

```text
Roadmap 117 evidence
→ live dry-run
→ read-only account verification
→ API permission proof
→ order preview
→ first-order simulation
→ kill-switch/cancel drill
→ live arm gate
→ tiny capped first order safety layer
→ evidence bundle
```

Na Roadmap 118 moet de bot:

* \[ ] live profile nog steeds standaard locked houden;
* \[ ] live dry-run kunnen draaien zonder echte orders;
* \[ ] live account read-only kunnen verifiëren zonder secrets te tonen;
* \[ ] API key permissions kunnen controleren;
* \[ ] order previews kunnen maken;
* \[ ] order size hard caps kunnen toepassen;
* \[ ] first live order alleen na multi-step confirmation toelaten;
* \[ ] cancel/emergency stop kunnen testen;
* \[ ] live sessions auditen;
* \[ ] live onmiddellijk disarmen bij restart/config change/risk issue;
* \[ ] alle live stappen in Dashboard V2 tonen;
* \[ ] evidence exporteren voor elke live dry-run/live attempt.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen one-click launcher opnieuw bouwen.
* \[ ] Geen Dashboard V2 foundation opnieuw bouwen.
* \[ ] Geen demo training pipeline opnieuw bouwen.
* \[ ] Geen modeltraining pipeline opnieuw bouwen.
* \[ ] Geen Strategy/Portfolio Lab opnieuw bouwen.
* \[ ] Geen Binance adapter volledig herschrijven.
* \[ ] Geen unattended live trading.
* \[ ] Geen live auto-start.
* \[ ] Geen live start vanuit launcher.
* \[ ] Geen live mode die demo/paper/testnet gates overslaat.
* \[ ] Geen onbeperkte order size.
* \[ ] Geen market-buy/sell zonder preview.
* \[ ] Geen live order zonder cancel/kill-switch bewijs.
* \[ ] Geen raw API keys in logs/reports/dashboard/evidence.
* \[ ] Geen financieel advies.

Wel doen:

* \[ ] live dry-run;
* \[ ] read-only account verification;
* \[ ] API permission verifier;
* \[ ] order preview;
* \[ ] live order sizing guard;
* \[ ] first-order safety gate;
* \[ ] cancel drill;
* \[ ] kill-switch drill;
* \[ ] live audit/evidence;
* \[ ] dashboard workflow;
* \[ ] fake-adapter tests;
* \[ ] live disarm rules.

\---

## 3\. Fase 0 - Live Dry-Run \& Minimal Execution Safety Contract

Nieuw docbestand:

```text
docs/live-trading/live-dry-run-minimal-execution-safety-contract.md
```

Regels:

* \[ ] Live trading is standaard disabled.
* \[ ] One-click launcher mag nooit live order placement starten.
* \[ ] Dashboard normale Start-knop mag nooit live order placement starten.
* \[ ] Live requires manual arm + exact confirmation.
* \[ ] Live dry-run is verplicht vóór echte live.
* \[ ] Read-only account verification is verplicht.
* \[ ] API permission verification is verplicht.
* \[ ] Roadmap 117 evidence is verplicht.
* \[ ] Order preview is verplicht.
* \[ ] Tiny capped first order is verplicht.
* \[ ] Session max loss is verplicht.
* \[ ] Session max order count is verplicht.
* \[ ] Emergency stop/kill-switch drill is verplicht.
* \[ ] Cancel drill is verplicht indien cancelable order type gebruikt wordt.
* \[ ] Live disarms on restart.
* \[ ] Live disarms on profile edit.
* \[ ] Live disarms on key/secret change.
* \[ ] Live disarms on stale data/risk warning/connectivity loss.
* \[ ] Reports/evidence zijn secret-free.
* \[ ] Output is geen financieel advies.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen launcher live niet kan starten.
* \[ ] Tests bewijzen normale Start-knop live niet kan starten.
* \[ ] Tests bewijzen live order placement exact confirm vereist.
* \[ ] Tests bewijzen evidence secret-free is.

\---

## 4\. Fase 1 - Live Evidence Prerequisite Gate

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_evidence\_prerequisite\_gate.py
```

Inputs from Roadmap 117:

* \[ ] demo session target report;
* \[ ] demo recording manifests;
* \[ ] dataset quality v2 report;
* \[ ] feature/label dataset manifest;
* \[ ] split governance report;
* \[ ] model/strategy validation report;
* \[ ] paper replay report;
* \[ ] testnet promotion report;
* \[ ] testnet rehearsal report;
* \[ ] live candidate gate report;
* \[ ] demo-to-live evidence manifest.

Gate requires:

* \[ ] dataset quality grade A/B;
* \[ ] model validation grade A/B;
* \[ ] paper replay pass;
* \[ ] testnet promotion pass;
* \[ ] testnet rehearsal pass;
* \[ ] live candidate state not blocked;
* \[ ] no secret leak;
* \[ ] no live contamination;
* \[ ] evidence hashes verify.

Gate states:

* \[ ] blocked\_missing\_evidence;
* \[ ] blocked\_low\_quality\_data;
* \[ ] blocked\_validation\_failed;
* \[ ] blocked\_testnet\_failed;
* \[ ] blocked\_secret\_leak;
* \[ ] eligible\_for\_live\_dry\_run;
* \[ ] eligible\_for\_live\_readiness\_review.

Acceptatiecriteria:

* \[ ] Gate blocks if Roadmap 117 evidence missing.
* \[ ] Gate blocks low dataset quality.
* \[ ] Gate blocks failed testnet rehearsal.
* \[ ] Gate verifies manifest hashes.
* \[ ] Report is JSON + Markdown.

\---

## 5\. Fase 2 - Live Read-Only Account Verifier

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_account\_verifier.py
```

Purpose:

* \[ ] verify live API credentials exist;
* \[ ] verify live base URL is exactly Binance live spot;
* \[ ] verify account endpoint can be read;
* \[ ] verify expected account type/permissions where available;
* \[ ] verify balances are read and redacted/summarized;
* \[ ] verify trading permissions without placing order;
* \[ ] verify symbol trading status;
* \[ ] verify account restrictions/warnings;
* \[ ] verify server time drift.

Important:

* \[ ] Never print raw balances if privacy mode enabled.
* \[ ] Never print API keys/secrets.
* \[ ] Fingerprint API key only.
* \[ ] Do not place orders.
* \[ ] Do not cancel orders.
* \[ ] Read-only mode only.

Output:

* \[ ] account verification status;
* \[ ] API key fingerprint;
* \[ ] permissions summary;
* \[ ] restricted symbols;
* \[ ] blockers/warnings;
* \[ ] redacted balance summary;
* \[ ] server time drift;
* \[ ] report hash.

Acceptatiecriteria:

* \[ ] Works with fake adapter.
* \[ ] Blocks non-live base URL.
* \[ ] Blocks missing credentials.
* \[ ] Secrets redacted.
* \[ ] No order endpoints called.

\---

## 6\. Fase 3 - Live API Permission \& Endpoint Policy

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_endpoint\_policy.py
```

Endpoint classes:

### Allowed in read-only verification

* \[ ] `server\_time`
* \[ ] `get\_exchange\_info`
* \[ ] `get\_symbol\_filters`
* \[ ] `get\_klines`
* \[ ] `get\_order\_book`
* \[ ] `get\_24hr\_ticker`
* \[ ] `get\_book\_ticker`
* \[ ] `get\_account\_state`
* \[ ] `open\_orders` optional read-only check only after explicit permission.

### Allowed in dry-run

* \[ ] public market data endpoints;
* \[ ] local order preview;
* \[ ] no live signed order placement.

### Allowed in order preview

* \[ ] public market data;
* \[ ] filters;
* \[ ] local quantity/notional check;
* \[ ] optional `/order/test` only if explicitly configured.

### Allowed in first-order gate

* \[ ] `place\_order` only after:

  * all gates pass;
  * exact confirm;
  * tiny cap;
  * live arm token;
  * session budget;
  * audit entry pre-written.

Forbidden by default:

* \[ ] `place\_order`
* \[ ] `cancel\_order`
* \[ ] `query\_order`
* \[ ] `open\_orders`
* \[ ] user data stream writes
* \[ ] any endpoint not allowlisted for current phase.

Acceptatiecriteria:

* \[ ] Policy is phase-aware.
* \[ ] Dry-run blocks `place\_order`.
* \[ ] Preview blocks `place\_order`.
* \[ ] First-order gate can allow exactly one tiny order only with confirm.
* \[ ] Tests cover all phases.

\---

## 7\. Fase 4 - Live Dry-Run Session

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_dry\_run\_session.py
```

Dry-run simulates:

* \[ ] selected live profile;
* \[ ] live data fetch;
* \[ ] live symbol filters;
* \[ ] live top-of-book/spread;
* \[ ] model signal;
* \[ ] risk decision;
* \[ ] order intent;
* \[ ] quantity/notional;
* \[ ] fees/slippage estimate;
* \[ ] account balance compatibility;
* \[ ] expected API request plan;
* \[ ] no order placement;
* \[ ] audit events;
* \[ ] evidence report.

Dry-run states:

* \[ ] not\_started;
* \[ ] verifying\_evidence;
* \[ ] verifying\_account;
* \[ ] fetching\_live\_market\_data;
* \[ ] building\_order\_preview;
* \[ ] risk\_checking;
* \[ ] blocked;
* \[ ] dry\_run\_passed;
* \[ ] dry\_run\_failed.

Acceptatiecriteria:

* \[ ] Dry-run works with fake live adapter.
* \[ ] Dry-run does not call `place\_order`.
* \[ ] Dry-run report includes exact blockers.
* \[ ] Dry-run output secret-free.
* \[ ] Dashboard can show dry-run timeline.

\---

## 8\. Fase 5 - Live Order Preview Builder

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_order\_preview.py
```

Preview includes:

* \[ ] profile id;
* \[ ] symbol;
* \[ ] side;
* \[ ] order type;
* \[ ] intended quote size;
* \[ ] calculated quantity;
* \[ ] min/max qty check;
* \[ ] min notional check;
* \[ ] market max qty check;
* \[ ] estimated price;
* \[ ] spread;
* \[ ] estimated fees;
* \[ ] max slippage;
* \[ ] max loss impact;
* \[ ] account balance impact;
* \[ ] session budget impact;
* \[ ] risk decision link;
* \[ ] model/strategy evidence link;
* \[ ] cancelability note;
* \[ ] exact confirm phrase;
* \[ ] preview hash.

Rules:

* \[ ] Preview cannot place order.
* \[ ] Preview hash required for first-order gate.
* \[ ] Preview expires quickly.
* \[ ] Preview invalidated by price/spread/profile/key changes.
* \[ ] Preview is stored in audit log.

Acceptatiecriteria:

* \[ ] Preview deterministic with fixture data.
* \[ ] Preview rejects stale market data.
* \[ ] Preview rejects too-large order.
* \[ ] Preview invalidation works.
* \[ ] Tests cover filter/notional/quantity logic.

\---

## 9\. Fase 6 - Live Order Sizing Guard

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_order\_sizing\_guard.py
```

Hard caps:

* \[ ] absolute first order max quote amount;
* \[ ] max percent of free quote balance;
* \[ ] max position quote;
* \[ ] max session order count;
* \[ ] max daily loss quote;
* \[ ] min notional;
* \[ ] max slippage bps;
* \[ ] max spread bps;
* \[ ] max stale data age;
* \[ ] max open orders;
* \[ ] max retry count;
* \[ ] only configured symbol/watchlist.

Recommended default first-order cap:

```text
first live order: tiny capped amount only, configurable but hard-limited
```

Acceptatiecriteria:

* \[ ] Oversized first order blocked.
* \[ ] Stale data blocked.
* \[ ] High spread blocked.
* \[ ] Missing free balance blocked.
* \[ ] Tests cover cap combinations.

\---

## 10\. Fase 7 - Live Arm Token \& Manual Confirmation Flow

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_arm\_token.py
```

Live arm requires:

* \[ ] live evidence prerequisite pass;
* \[ ] read-only account verifier pass;
* \[ ] live endpoint policy pass;
* \[ ] dry-run pass;
* \[ ] order preview hash;
* \[ ] sizing guard pass;
* \[ ] kill-switch drill pass;
* \[ ] cancel drill pass if needed;
* \[ ] exact manual confirmation phrase;
* \[ ] operator session id;
* \[ ] short expiration;
* \[ ] one-time use.

Arm token invalidates on:

* \[ ] restart;
* \[ ] profile edit;
* \[ ] config edit;
* \[ ] key change;
* \[ ] symbol change;
* \[ ] model/strategy/risk change;
* \[ ] price/spread stale;
* \[ ] dry-run rerun needed;
* \[ ] kill switch toggled;
* \[ ] stop/emergency stop;
* \[ ] token timeout.

Acceptatiecriteria:

* \[ ] Token cannot be reused.
* \[ ] Token expires.
* \[ ] Token invalidates on profile edit.
* \[ ] Token never stored with secrets.
* \[ ] Tests cover invalidation triggers.

\---

## 11\. Fase 8 - Kill-Switch \& Cancel Drill

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_safety\_drills.py
```

Kill-switch drill:

* \[ ] simulate running live session;
* \[ ] toggle kill switch;
* \[ ] verify order path blocked;
* \[ ] verify runtime disarmed;
* \[ ] verify dashboard status;
* \[ ] verify audit log.

Cancel drill:

* \[ ] only in testnet/demo/fake live adapter by default;
* \[ ] place/cancel simulation or testnet cancel;
* \[ ] verify cancel path;
* \[ ] verify open order query path;
* \[ ] verify audit/evidence;
* \[ ] verify no live order unless dedicated gate.

Acceptatiecriteria:

* \[ ] Kill-switch drill required before live arm.
* \[ ] Cancel drill required for limit orders.
* \[ ] Drills work with fake adapter.
* \[ ] Reports secret-free.
* \[ ] Dashboard shows drill status.

\---

## 12\. Fase 9 - Minimal First Live Order Gate

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/first\_live\_order\_gate.py
```

This is the only phase allowed to call `place\_order`, and only when every gate passes.

Preconditions:

* \[ ] Roadmap 117 evidence verified.
* \[ ] live read-only account verified.
* \[ ] endpoint policy phase = first\_order.
* \[ ] live dry-run passed.
* \[ ] order preview hash valid.
* \[ ] sizing guard passed.
* \[ ] kill-switch drill passed.
* \[ ] cancel drill passed if needed.
* \[ ] live arm token valid.
* \[ ] exact confirmation:

  * `I\_UNDERSTAND\_THIS\_WILL\_PLACE\_A\_REAL\_BINANCE\_SPOT\_ORDER`
* \[ ] first-order cap not exceeded.
* \[ ] session budget not exceeded.
* \[ ] audit pre-entry written.
* \[ ] emergency stop visible.

Allowed behavior:

* \[ ] place exactly one tiny capped order;
* \[ ] store response redacted;
* \[ ] query order result;
* \[ ] disarm after order;
* \[ ] export first-order evidence.

Forbidden behavior:

* \[ ] looped live trading;
* \[ ] unattended live trading;
* \[ ] multiple live orders;
* \[ ] auto retry placing order;
* \[ ] live sell/buy without preview;
* \[ ] launcher triggered live order.

Acceptatiecriteria:

* \[ ] Fake adapter tests prove exactly one order.
* \[ ] Gate disarms after attempt.
* \[ ] Gate blocks second order.
* \[ ] Gate blocks without exact confirm.
* \[ ] Live evidence exported.

\---

## 13\. Fase 10 - Live Execution Engine Adapter Layer

Update carefully around `ExecutionEngine`:

New module:

```text
src/binance\_spot\_bot/live\_trading/live\_execution\_adapter.py
```

Design:

* \[ ] Do not replace existing `ExecutionEngine` blindly.
* \[ ] Keep current live block as default.
* \[ ] Add explicit `LiveExecutionAdapter` only called by first-order gate.
* \[ ] Adapter requires arm token.
* \[ ] Adapter requires preview hash.
* \[ ] Adapter requires first-order gate decision.
* \[ ] Adapter emits audit pre/post entries.
* \[ ] Adapter disarms after order.
* \[ ] Adapter never loops.
* \[ ] Adapter never called by paper/demo/testnet.

Acceptatiecriteria:

* \[ ] Existing `ExecutionEngine` live block remains unless explicit adapter path used.
* \[ ] Paper/demo/testnet unaffected.
* \[ ] Live adapter cannot be instantiated without gate context.
* \[ ] Tests prove normal runtime cannot call live place order.
* \[ ] Tests prove gated path uses fake adapter only in tests.

\---

## 14\. Fase 11 - Live Session State Machine

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_session\_state.py
```

States:

* \[ ] locked;
* \[ ] evidence\_required;
* \[ ] account\_verification\_required;
* \[ ] dry\_run\_required;
* \[ ] preview\_required;
* \[ ] drills\_required;
* \[ ] ready\_to\_arm;
* \[ ] armed;
* \[ ] placing\_first\_order;
* \[ ] order\_submitted;
* \[ ] disarmed\_after\_order;
* \[ ] emergency\_stopped;
* \[ ] failed;
* \[ ] blocked.

Allowed transitions:

* \[ ] locked → evidence\_required;
* \[ ] evidence\_required → account\_verification\_required;
* \[ ] account\_verification\_required → dry\_run\_required;
* \[ ] dry\_run\_required → preview\_required;
* \[ ] preview\_required → drills\_required;
* \[ ] drills\_required → ready\_to\_arm;
* \[ ] ready\_to\_arm → armed;
* \[ ] armed → placing\_first\_order;
* \[ ] placing\_first\_order → order\_submitted;
* \[ ] order\_submitted → disarmed\_after\_order;
* \[ ] any active state → emergency\_stopped;
* \[ ] any active state → blocked/failed.

Acceptatiecriteria:

* \[ ] Invalid transitions blocked.
* \[ ] Restart forces locked/disarmed.
* \[ ] Profile edit forces locked/disarmed.
* \[ ] Kill switch forces emergency stopped.
* \[ ] Tests cover transition graph.

\---

## 15\. Fase 12 - Live Audit Log \& Evidence Trail

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_audit.py
```

Audit events:

* \[ ] live evidence checked;
* \[ ] account read-only verified;
* \[ ] API permission checked;
* \[ ] dry-run started/completed;
* \[ ] order preview created;
* \[ ] sizing guard decision;
* \[ ] kill-switch drill;
* \[ ] cancel drill;
* \[ ] arm token created;
* \[ ] live armed;
* \[ ] first-order gate decision;
* \[ ] order submitted;
* \[ ] order response received;
* \[ ] order query result;
* \[ ] disarmed;
* \[ ] emergency stop;
* \[ ] failure/blocker.

Rules:

* \[ ] hash chain;
* \[ ] redaction;
* \[ ] no raw keys;
* \[ ] no raw secret headers;
* \[ ] response redaction for sensitive fields;
* \[ ] exportable.

Acceptatiecriteria:

* \[ ] Audit hash chain verifies.
* \[ ] Secret redaction tests pass.
* \[ ] Every live transition emits event.
* \[ ] Evidence links audit hash.
* \[ ] Tests cover tamper detection.

\---

## 16\. Fase 13 - Dashboard V2 Live Dry-Run \& First-Order Workflow

Nieuwe routes/pages:

```text
/live
/live/dry-run
/live/account
/live/order-preview
/live/safety-drills
/live/arm
/live/first-order
/live/evidence
```

Dashboard panels:

* \[ ] live locked banner;
* \[ ] Roadmap 117 evidence status;
* \[ ] account read-only verifier;
* \[ ] API permission status;
* \[ ] dry-run timeline;
* \[ ] order preview card;
* \[ ] order sizing guard;
* \[ ] kill-switch drill status;
* \[ ] cancel drill status;
* \[ ] arm token status;
* \[ ] first-order gate status;
* \[ ] exact confirm field;
* \[ ] emergency stop button;
* \[ ] audit timeline;
* \[ ] evidence export.

UX rules:

* \[ ] no normal Start Live button;
* \[ ] first-order button hidden until every gate pass;
* \[ ] button says real order clearly;
* \[ ] confirmation phrase required;
* \[ ] order amount and symbol shown prominently;
* \[ ] disarm after order.

Acceptatiecriteria:

* \[ ] Live page loads.
* \[ ] Dry-run can run with fake adapter.
* \[ ] First-order button blocked by default.
* \[ ] Emergency stop visible.
* \[ ] Browser smoke covers blocked flow.

\---

## 17\. Fase 14 - Live API Routes

Nieuwe API routes:

```text
GET  /api/live/status
GET  /api/live/evidence-prerequisites
POST /api/live/account/verify
POST /api/live/endpoint-policy/check
POST /api/live/dry-run/start
GET  /api/live/dry-run/{run\_id}
POST /api/live/order-preview
POST /api/live/sizing-guard/check
POST /api/live/safety-drills/kill-switch
POST /api/live/safety-drills/cancel
POST /api/live/arm-token/create
POST /api/live/arm-token/revoke
POST /api/live/first-order/preview-final
POST /api/live/first-order/execute
POST /api/live/emergency-stop
GET  /api/live/audit
POST /api/live/evidence/export
WS   /ws/live
```

API rules:

* \[ ] first-order execute requires exact confirm;
* \[ ] first-order execute requires valid one-time arm token;
* \[ ] no endpoint can be called by launcher;
* \[ ] no raw secrets returned;
* \[ ] all responses redacted;
* \[ ] first-order route disarms after attempt;
* \[ ] emergency stop always available.

Acceptatiecriteria:

* \[ ] TestClient covers blocked paths.
* \[ ] Execute route blocked without token.
* \[ ] Execute route blocked without confirm.
* \[ ] Execute route calls fake adapter once in tests.
* \[ ] Secrets redacted.

\---

## 18\. Fase 15 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli live-evidence-prerequisites --json
python -m binance\_spot\_bot.cli live-account-verify --profile <id> --json
python -m binance\_spot\_bot.cli live-endpoint-policy --phase dry\_run --json
python -m binance\_spot\_bot.cli live-dry-run --profile <id> --json
python -m binance\_spot\_bot.cli live-order-preview --profile <id> --json
python -m binance\_spot\_bot.cli live-sizing-guard --preview <id> --json
python -m binance\_spot\_bot.cli live-kill-switch-drill --profile <id> --json
python -m binance\_spot\_bot.cli live-cancel-drill --profile <id> --json
python -m binance\_spot\_bot.cli live-arm-token-create --profile <id> --confirm I\_UNDERSTAND\_LIVE\_SPOT\_TRADING\_RISK
python -m binance\_spot\_bot.cli live-first-order-execute --profile <id> --preview <id> --confirm I\_UNDERSTAND\_THIS\_WILL\_PLACE\_A\_REAL\_BINANCE\_SPOT\_ORDER
python -m binance\_spot\_bot.cli live-emergency-stop
python -m binance\_spot\_bot.cli live-audit --json
python -m binance\_spot\_bot.cli live-evidence-export
python -m binance\_spot\_bot.cli dashboard-v2-live-smoke --json
```

Acceptatiecriteria:

* \[ ] Dry-run commands work with fake adapter/fixtures.
* \[ ] First-order execute requires exact confirm.
* \[ ] First-order execute blocked by default.
* \[ ] Emergency stop command always available.
* \[ ] Commands redact secrets.

\---

## 19\. Fase 16 - Check-All Integration

Fast profile:

* \[ ] live\_trading modules import;
* \[ ] safety contract check;
* \[ ] endpoint policy tests;
* \[ ] session state machine tests;
* \[ ] secret redaction tests;
* \[ ] first-order blocked-by-default test.

Deep profile:

* \[ ] evidence prerequisite fixture;
* \[ ] read-only account fake adapter;
* \[ ] dry-run fake adapter;
* \[ ] order preview fixture;
* \[ ] sizing guard fixture;
* \[ ] kill-switch drill fixture;
* \[ ] cancel drill fixture;
* \[ ] arm token fixture;
* \[ ] first-order fake adapter one-order test;
* \[ ] Dashboard V2 live page browser smoke;
* \[ ] live evidence export/verify.

Acceptatiecriteria:

* \[ ] Fast check-all stays safe.
* \[ ] Deep check-all proves gated live path.
* \[ ] Any live auto-start path hard fails.
* \[ ] Any secret leak hard fails.
* \[ ] Any first-order without token/confirm hard fails.

\---

## 20\. Fase 17 - UAT / Operator Workflow

Roadmap 102 docs:

* \[ ] live dry-run guide;
* \[ ] read-only account verification guide;
* \[ ] order preview guide;
* \[ ] kill-switch drill guide;
* \[ ] first live order checklist;
* \[ ] emergency stop guide;
* \[ ] live evidence guide.

Roadmap 103 UAT scenarios:

* \[ ] live page shows locked by default;
* \[ ] missing Roadmap 117 evidence blocks live;
* \[ ] read-only account verification with fake adapter;
* \[ ] dry-run with fake adapter;
* \[ ] order preview from fixture;
* \[ ] sizing guard blocks too-large order;
* \[ ] kill-switch drill pass;
* \[ ] cancel drill pass;
* \[ ] arm token expires;
* \[ ] first-order route blocked without confirm;
* \[ ] first-order route fake adapter executes once after all gates;
* \[ ] emergency stop disarms;
* \[ ] evidence export.

Acceptatiecriteria:

* \[ ] UAT confirms no unattended live.
* \[ ] UAT confirms first-order exact confirm.
* \[ ] UAT confirms emergency stop visible.
* \[ ] UAT confirms secrets redacted.
* \[ ] UAT evidence attached.

\---

## 21\. Fase 18 - Live Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/live\_trading/live\_execution\_evidence.py
```

Bundle bevat:

* \[ ] safety contract;
* \[ ] Roadmap 117 evidence prerequisite report;
* \[ ] live account verification report;
* \[ ] endpoint policy report;
* \[ ] dry-run report;
* \[ ] order preview report;
* \[ ] sizing guard report;
* \[ ] kill-switch drill report;
* \[ ] cancel drill report;
* \[ ] arm token report;
* \[ ] first-order gate report;
* \[ ] order response redacted;
* \[ ] order query result redacted;
* \[ ] session state transitions;
* \[ ] audit hash chain;
* \[ ] emergency stop proof;
* \[ ] secret redaction proof;
* \[ ] no unattended live proof;
* \[ ] hashes.

Output:

```text
data/live-trading/evidence/<run\_id>/
  live\_execution\_evidence\_manifest.json
  live\_execution\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Evidence is secret-free.
* \[ ] Evidence has manifest/hash.
* \[ ] Evidence can be verified.
* \[ ] Evidence states whether real order was executed or dry-run only.
* \[ ] Dashboard can download bundle.

\---

## 22\. Fase 19 - Release / Knowledge / Test / Performance Integration

Roadmap 089:

* \[ ] release notes mention live dry-run and first-order gate;
* \[ ] version manifest includes live-trading safety schema;
* \[ ] migration notes explain live remains locked by default.

Roadmap 091:

* \[ ] knowledge graph maps Roadmap 117 evidence → live dry-run → first-order gate.
* \[ ] impact analysis detects changes affecting live safety.

Roadmap 092:

* \[ ] test selector chooses live safety tests for execution/binance/config changes.
* \[ ] dashboard live UI changes select browser smoke.

Roadmap 093:

* \[ ] performance budget for dry-run, account verify, preview build, evidence export.
* \[ ] endpoint pacing warnings.

Acceptatiecriteria:

* \[ ] Release evidence includes live execution evidence.
* \[ ] Knowledge graph updated.
* \[ ] Test selector protects live code.
* \[ ] Performance reports include live dry-run budgets.
* \[ ] Live remains locked by default.

\---

## 23\. Fase 20 - Scheduled Live Safety Reports

Scheduled jobs:

* \[ ] weekly live evidence prerequisite check;
* \[ ] weekly read-only account verifier if live profile configured;
* \[ ] weekly dry-run only, no order;
* \[ ] weekly kill-switch drill;
* \[ ] weekly endpoint policy check;
* \[ ] weekly live profile locked-state check;
* \[ ] monthly live safety evidence export.

Metrics:

* \[ ] evidence readiness;
* \[ ] account verification status;
* \[ ] dry-run pass/fail;
* \[ ] preview blockers;
* \[ ] kill-switch drill status;
* \[ ] arm token attempted count;
* \[ ] first-order attempts count;
* \[ ] emergency stop count;
* \[ ] secret redaction status;
* \[ ] locked-by-default status.

Acceptatiecriteria:

* \[ ] Scheduled jobs never place live orders.
* \[ ] Reports are secret-free.
* \[ ] Dashboard can show reports.
* \[ ] Live remains locked unless manually armed.
* \[ ] Check-all safe env preserved.

\---

## 24\. Tests

### Unit tests

* \[ ] `tests/test\_live\_dry\_run\_safety\_contract.py`
* \[ ] `tests/test\_live\_evidence\_prerequisite\_gate.py`
* \[ ] `tests/test\_live\_account\_verifier.py`
* \[ ] `tests/test\_live\_endpoint\_policy.py`
* \[ ] `tests/test\_live\_dry\_run\_session.py`
* \[ ] `tests/test\_live\_order\_preview.py`
* \[ ] `tests/test\_live\_order\_sizing\_guard.py`
* \[ ] `tests/test\_live\_arm\_token.py`
* \[ ] `tests/test\_live\_safety\_drills.py`
* \[ ] `tests/test\_first\_live\_order\_gate.py`
* \[ ] `tests/test\_live\_execution\_adapter.py`
* \[ ] `tests/test\_live\_session\_state.py`
* \[ ] `tests/test\_live\_audit.py`
* \[ ] `tests/test\_live\_execution\_evidence.py`

### Integration tests

* \[ ] Roadmap 117 evidence fixture passes prerequisite gate.
* \[ ] Missing evidence blocks.
* \[ ] Fake live account verifier pass/fail.
* \[ ] Dry-run fake adapter no-order proof.
* \[ ] Order preview from fixture market/risk.
* \[ ] Sizing guard blocks too-large.
* \[ ] Arm token one-time use.
* \[ ] First-order fake adapter executes exactly once.
* \[ ] Emergency stop disarms.
* \[ ] Evidence export/verify.

### Browser smoke

* \[ ] `/live` loads.
* \[ ] locked banner visible.
* \[ ] missing evidence blockers visible.
* \[ ] dry-run panel visible.
* \[ ] account verifier panel visible.
* \[ ] order preview panel visible.
* \[ ] kill-switch drill panel visible.
* \[ ] first-order button blocked by default.
* \[ ] emergency stop visible.
* \[ ] audit/evidence panel visible.

### Safety tests

* \[ ] Launcher cannot call live execute.
* \[ ] Normal Start cannot call live execute.
* \[ ] First-order blocked without Roadmap 117 evidence.
* \[ ] First-order blocked without dry-run.
* \[ ] First-order blocked without preview hash.
* \[ ] First-order blocked without arm token.
* \[ ] First-order blocked without exact confirm.
* \[ ] First-order disarms after attempt.
* \[ ] Second order blocked.
* \[ ] Secrets redacted.
* \[ ] Check-all safe env preserved.

\---

## 25\. Docs

Nieuwe docs:

```text
docs/live-trading/live-dry-run-minimal-execution-safety-contract.md
docs/live-trading/live-evidence-prerequisite-gate.md
docs/live-trading/live-read-only-account-verification.md
docs/live-trading/live-endpoint-policy.md
docs/live-trading/live-dry-run-session.md
docs/live-trading/live-order-preview.md
docs/live-trading/live-order-sizing-guard.md
docs/live-trading/live-arm-token.md
docs/live-trading/live-safety-drills.md
docs/live-trading/first-live-order-gate.md
docs/live-trading/live-execution-adapter.md
docs/live-trading/live-session-state.md
docs/live-trading/live-audit.md
docs/live-trading/live-execution-evidence.md
docs/live-trading/emergency-stop-playbook.md
```

README updates:

* \[ ] Live remains locked by default.
* \[ ] Live dry-run overview.
* \[ ] Read-only account verification.
* \[ ] Order preview.
* \[ ] First live order checklist.
* \[ ] Emergency stop.
* \[ ] Evidence export.
* \[ ] No unattended live statement.

\---

## 26\. Codex bouwvolgorde

### PR 1 - Safety Contract + Evidence Prerequisite Gate

* \[ ] `docs/live-trading/live-dry-run-minimal-execution-safety-contract.md`
* \[ ] `live\_trading/live\_evidence\_prerequisite\_gate.py`
* \[ ] evidence fixture tests.
* \[ ] missing evidence blocker tests.

### PR 2 - Read-Only Account Verifier + Endpoint Policy

* \[ ] `live\_account\_verifier.py`
* \[ ] `live\_endpoint\_policy.py`
* \[ ] fake adapter tests.
* \[ ] phase-aware endpoint tests.

### PR 3 - Live Dry-Run Session

* \[ ] `live\_dry\_run\_session.py`
* \[ ] fake adapter dry-run tests.
* \[ ] no order placement proof.

### PR 4 - Order Preview + Sizing Guard

* \[ ] `live\_order\_preview.py`
* \[ ] `live\_order\_sizing\_guard.py`
* \[ ] filter/notional/cap tests.

### PR 5 - Arm Token + Safety Drills

* \[ ] `live\_arm\_token.py`
* \[ ] `live\_safety\_drills.py`
* \[ ] token invalidation/drill tests.

### PR 6 - First Live Order Gate

* \[ ] `first\_live\_order\_gate.py`
* \[ ] exactly-one-order fake adapter tests.
* \[ ] confirm/token/preview gate tests.

### PR 7 - Live Execution Adapter + Session State + Audit

* \[ ] `live\_execution\_adapter.py`
* \[ ] `live\_session\_state.py`
* \[ ] `live\_audit.py`
* \[ ] transition/audit tests.

### PR 8 - API + Dashboard Live Workflow

* \[ ] live API routes.
* \[ ] Dashboard V2 live pages.
* \[ ] browser smoke.

### PR 9 - Evidence + CLI + Check-All

* \[ ] `live\_execution\_evidence.py`
* \[ ] CLI commands.
* \[ ] check-all integration.

### PR 10 - Docs, UAT, Release/Knowledge/Test/Performance Integration

* \[ ] docs.
* \[ ] UAT scenarios.
* \[ ] release notes.
* \[ ] knowledge/test/performance integration.
* \[ ] scheduled reports.

\---

## 27\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 118 PR 1: Live Dry-Run Safety Contract + Live Evidence Prerequisite Gate.

Maak docs/live-trading/live-dry-run-minimal-execution-safety-contract.md.

Maak src/binance\_spot\_bot/live\_trading/\_\_init\_\_.py.
Maak src/binance\_spot\_bot/live\_trading/live\_evidence\_prerequisite\_gate.py met:
- LiveEvidencePrerequisiteInput
- LiveEvidenceBlocker
- LiveEvidencePrerequisiteReport
- evaluate\_live\_evidence\_prerequisites(root: Path)
- live\_evidence\_prerequisite\_report\_to\_dict(...)
- write\_live\_evidence\_prerequisite\_report(...)

De gate moet best-effort Roadmap 117 evidence lezen:
- demo session target report
- demo recording manifests
- dataset quality v2 report
- feature/label dataset manifest
- split governance report
- model/strategy validation report
- paper replay report
- testnet promotion report
- testnet rehearsal report
- live candidate gate report
- demo-to-live evidence manifest

Gate states:
- blocked\_missing\_evidence
- blocked\_low\_quality\_data
- blocked\_validation\_failed
- blocked\_testnet\_failed
- blocked\_secret\_leak
- eligible\_for\_live\_dry\_run
- eligible\_for\_live\_readiness\_review

Hard blockers:
- missing Roadmap 117 evidence manifest
- dataset quality grade lower than B
- model validation grade lower than B
- paper replay failed/missing
- testnet promotion failed/missing
- testnet rehearsal failed/missing
- live candidate gate blocked/missing
- secret leak finding
- live contamination finding
- manifest hash mismatch

Output moet bevatten:
- live\_trading\_enabled=False
- live\_execution\_enabled=False
- live\_order\_placement\_enabled=False
- no\_auto\_live\_start\_statement
- not\_financial\_advice\_statement
- blockers
- warnings
- next\_required\_actions

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
- missing evidence blocks
- low dataset quality blocks
- failed validation blocks
- failed paper replay blocks
- failed testnet promotion blocks
- failed testnet rehearsal blocks
- secret leak blocks
- eligible fixture passes
- JSON serialization
- secret-like values worden geredact
- live\_execution\_enabled=False
- live\_order\_placement\_enabled=False
```

Waarom eerst:

* Echte live voorbereiding mag pas starten als Roadmap 117 bewijs bestaat.
* Dit is read-only en raakt runtime/trading/frontend niet.
* Het is klein genoeg voor Codex.
* Het voorkomt dat live dry-run of live order preview zonder demo-data/training/testnet bewijs gebruikt wordt.
* Daarna kunnen account verification, dry-run, preview en first-order gate veilig volgen.

\---

## 28\. Definition of Done

Roadmap 118 is klaar als:

* \[ ] Live Dry-Run \& Minimal Execution Safety Contract bestaat.
* \[ ] Live Evidence Prerequisite Gate werkt.
* \[ ] Live Read-Only Account Verifier werkt.
* \[ ] Live API Permission \& Endpoint Policy werkt.
* \[ ] Live Dry-Run Session werkt.
* \[ ] Live Order Preview Builder werkt.
* \[ ] Live Order Sizing Guard werkt.
* \[ ] Live Arm Token \& Manual Confirmation Flow werkt.
* \[ ] Kill-Switch \& Cancel Drill werkt.
* \[ ] Minimal First Live Order Gate werkt.
* \[ ] Live Execution Engine Adapter Layer werkt.
* \[ ] Live Session State Machine werkt.
* \[ ] Live Audit Log \& Evidence Trail werkt.
* \[ ] Dashboard V2 Live Dry-Run \& First-Order Workflow werkt.
* \[ ] Live API routes werken.
* \[ ] CLI commands werken.
* \[ ] Check-All Integration werkt.
* \[ ] UAT/Operator Workflow werkt.
* \[ ] Live Evidence Bundle werkt.
* \[ ] Release/Knowledge/Test/Performance integration werkt.
* \[ ] Scheduled Live Safety Reports werken.
* \[ ] Tests bewijzen launcher nooit live execute kan aanroepen.
* \[ ] Tests bewijzen normale Start nooit live execute kan aanroepen.
* \[ ] Tests bewijzen first-order exact confirm vereist.
* \[ ] Tests bewijzen first-order exact één order toelaat met fake adapter.
* \[ ] Tests bewijzen tweede order blokkeert.
* \[ ] Tests bewijzen emergency stop disarmed.
* \[ ] Tests bewijzen secrets redacted zijn.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Roadmap 118 kan na uitvoering naar `Voltooid docs`.

\---

## 29\. Verwachte Roadmap 119 daarna

Als Roadmap 118 groen is en first-order gate veilig werkt:

```text
Roadmap 119 - Controlled Live Session Manager, Micro-Position Scaling, Live Monitoring \& Automatic Disarm Rules
```

Mogelijke inhoud:

* \[ ] live session manager;
* \[ ] micro-position scaling;
* \[ ] max N live orders per manually armed session;
* \[ ] live monitoring;
* \[ ] live reconciliation;
* \[ ] automatic disarm rules;
* \[ ] live performance report;
* \[ ] still no unattended live.

```

Als Roadmap 118 blockers vindt:

```text
Roadmap 119 - Live Readiness Blocker Burn-Down, Dry-Run Reliability \& First-Order Gate Hardening
```

Mogelijke inhoud:

* \[ ] Roadmap 117 evidence blockers oplossen;
* \[ ] account verifier verbeteren;
* \[ ] dry-run blockers oplossen;
* \[ ] preview/sizing guard fixen;
* \[ ] kill-switch/cancel drills hardenen;
* \[ ] live blijft locked.

```

