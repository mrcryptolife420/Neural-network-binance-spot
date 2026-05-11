# Roadmap 026 - Demo Spot Execution Sandbox & Order Lifecycle Drill

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-10  
Locatie:

```text
Roadmap docs/026-roadmap-demo-spot-execution-sandbox-order-lifecycle-drill.md
```

Volgt op:

- `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
- `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
- `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
- `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
- `Voltooid docs/005` t/m `Voltooid docs/025`

Live trading blijft volledig buiten scope. Deze roadmap bouwt voort op de bestaande Binance adapter, Demo Spot gate, risk engine, execution engine, order lifecycle store, pilot runner, dashboard evidence en browser-smoke. Er wordt niets dubbel gebouwd.

Voltooiingsnotitie 2026-05-10:

- `DemoExecutionSandbox` toegevoegd met preview, test-order-only, gated Demo Spot placement, query, cancel en latest report.
- CLI commands toegevoegd voor `demo-execution-preview`, `demo-execution-test-order`, `demo-execution-place`, `demo-execution-query`, `demo-execution-cancel` en `demo-execution-report`.
- Dashboardpaneel `Demo Execution Drill` toegevoegd aan Demo Spot Trading.
- Operator evidence bevat nu de laatste demo execution drill.
- Docs toegevoegd voor execution sandbox en order lifecycle drill.
- Validatie uitgevoerd: roadmap 026 tests, `python -m pytest` en `python -m binance_spot_bot.cli check-all --skip-tests --json`.

---

## 0. Onderzoeksconclusie

### Wat al bestaat

- `BinanceSpotAdapter` heeft veilige methodes voor:
  - `test_order`;
  - `place_order`;
  - `cancel_order`;
  - `query_order`;
  - `open_orders`;
  - account state.
- `ExecutionEngine` bouwt orders vanuit risk decisions en blokkeert live order placement.
- `evaluate_demo_trading_gate` vereist:
  - Binance Demo Spot profiel;
  - demo base URL;
  - credentials;
  - connection ok;
  - explicit armed;
  - live disabled;
  - kill switch off voor demo execution;
  - risk allowed;
  - filters loaded;
  - max order budget ok.
- `BotRuntime` heeft al Demo Spot state, reconciliation, order lifecycle en pilot status.
- `Dashboard` heeft sinds roadmap 025 operator evidence, visual smoke en statusbar.

### Wat nog ontbreekt

- Geen afzonderlijke, operator-veilige **execution sandbox** die de volledige order lifecycle kan drillen zonder meteen echte demo orders te sturen.
- Geen dashboardflow die één geplande Demo Spot trade stap voor stap toont:
  - signal;
  - risk decision;
  - Binance filters;
  - quantized order request;
  - test order result;
  - optional armed demo place order;
  - query/reconcile result;
  - cancel result.
- Geen duidelijke `test order only` modus als tussenstap tussen paper fills en echte Demo Spot order placement.
- Geen order lifecycle drill report dat bewijst dat een demo orderflow veilig afgerond is.
- Geen dedicated regression tests voor:
  - test-order-only path;
  - place-order gated path;
  - reconcile/cancel drill;
  - no-live guarantees in execution sandbox.

Conclusie: de volgende beste verbetering is een **Demo Spot execution sandbox** die echte operator-controle geeft over de stap van paper/demo dashboard naar gecontroleerde Binance Demo Spot orderflow, zonder live trading te introduceren.

---

## 1. Doel

Maak een gecontroleerde flow waarmee de operator in het dashboard en via CLI kan zien hoe een trade intent door de volledige execution lifecycle gaat, met harde gates voor Demo Spot en duidelijke bewijsbestanden.

Na deze roadmap moet een operator kunnen:

- een trade intent laten voorbereiden;
- Binance symbol filters zien;
- de afgeronde order request zien;
- eerst `/api/v3/order/test` uitvoeren;
- pas daarna, expliciet armed, een Demo Spot order plaatsen;
- order status query/reconcile uitvoeren;
- open demo orders cancelen;
- een lifecycle evidence report exporteren.

---

## 2. Scope

### In scope

- Execution sandbox service bovenop bestaande `ExecutionEngine` en `BinanceSpotAdapter`.
- CLI commands voor order lifecycle drill.
- Dashboardpaneel in Demo Spot / Demo Pilot voor:
  - prepare;
  - test order;
  - place demo order;
  - query;
  - cancel;
  - export evidence.
- Test-order-only mode.
- Lifecycle evidence in JSON.
- Reconciliation drill met bestaande lifecycle store.
- Regression tests voor no-live en safe gates.

### Out of scope

- Geen live trading.
- Geen nieuwe exchange adapter.
- Geen nieuwe risk engine.
- Geen nieuwe strategy/model.
- Geen autonome LLM trading.
- Geen secrets in repo.
- Geen order placement zonder expliciete operator-arm en confirmation.

---

## 3. Architectuur

```text
Signal / Manual Intent
        |
        v
RiskEngine
        |
        v
ExecutionSandbox
        |
        +--> build_order_preview
        +--> test_order_only
        +--> place_demo_order_if_armed
        +--> query_order
        +--> cancel_order
        +--> lifecycle_evidence
        |
        v
AuditLog + OrderLifecycleStore + Dashboard Evidence
```

Nieuwe component:

```text
src/binance_spot_bot/demo_execution_sandbox.py
```

Verantwoordelijkheden:

- order preview maken zonder netwerkorder;
- Binance filters en quantization vastleggen;
- Demo Spot gate evalueren;
- test-order-only uitvoeren;
- optional place order uitvoeren wanneer alle gates groen zijn;
- query/cancel/reconcile payloads redacted opslaan;
- lifecycle evidence schrijven.

---

## 4. Fase 1 - Execution sandbox service

Taken:

- Maak `DemoExecutionSandbox`.
- Voeg dataclasses toe:
  - `SandboxIntent`;
  - `SandboxOrderPreview`;
  - `SandboxDrillResult`.
- Gebruik bestaande types:
  - `MarketState`;
  - `SymbolFilters`;
  - `OrderRequest`;
  - `RiskDecision`;
  - `ExecutionResult`.
- Gebruik bestaande `ExecutionEngine._build_order` of verplaats order-build naar een herbruikbare veilige helper zonder duplicatie.
- Voeg redaction toe voor alle payloads.
- Schrijf evidence naar:

```text
data/evidence/demo-execution/
```

Acceptatiecriteria:

- Order preview werkt zonder API keys.
- Test-order-only faalt duidelijk als credentials ontbreken.
- Place order blijft geblokkeerd zonder Demo Spot profiel, armed flag en confirmation.
- Payloads bevatten geen secrets.
- Live trading blijft onmogelijk.

---

## 5. Fase 2 - CLI drill commands

Nieuwe commands:

```powershell
spot-bot demo-execution-preview --symbol BTCUSDT --side BUY --quote-size 10
spot-bot demo-execution-test-order --symbol BTCUSDT --side BUY --quote-size 10
spot-bot demo-execution-place --symbol BTCUSDT --side BUY --quote-size 10 --confirm-demo-order
spot-bot demo-execution-query --symbol BTCUSDT --client-order-id <id>
spot-bot demo-execution-cancel --symbol BTCUSDT --order-id <id> --confirm-cancel
spot-bot demo-execution-report
```

Gates:

- `demo-execution-place` vereist:
  - `--confirm-demo-order`;
  - Demo Spot profile;
  - demo base URL;
  - credentials present;
  - live disabled;
  - order budget ok.
- `demo-execution-cancel` vereist `--confirm-cancel`.

Acceptatiecriteria:

- Preview command werkt offline.
- Test order command gebruikt alleen `/api/v3/order/test`.
- Place command kan niet zonder confirmation.
- Cancel command kan niet zonder confirmation.
- Alle commands printen JSON met `live_trading_enabled: false`.

---

## 6. Fase 3 - Dashboard execution drill panel

Toevoegen aan Demo Spot Trading of Demo Pilot:

- Paneel: `Demo Execution Drill`.
- Statusbadges:
  - profile;
  - base URL;
  - credentials present;
  - demo armed;
  - live disabled;
  - kill switch state;
  - last lifecycle state.
- Controls:
  - side;
  - quote size;
  - preview order;
  - test order only;
  - confirm demo order checkbox;
  - place demo order;
  - query status;
  - confirm cancel checkbox;
  - cancel open order;
  - export drill evidence.

Acceptatiecriteria:

- Paneel toont eerst preview/test-order flow.
- Place demo order is visueel en functioneel gated.
- Geen secrets zichtbaar.
- Browser-smoke blijft groen.
- Operator evidence bevat laatste drill status.

---

## 7. Fase 4 - Order lifecycle and reconciliation drill

Taken:

- Registreer lifecycle events voor:
  - preview created;
  - test order accepted/rejected;
  - demo order submitted;
  - query status;
  - cancel requested;
  - cancel result;
  - reconcile needed/resolved.
- Koppel `client_order_id` consequent aan evidence.
- Voeg `demo_execution_drill.json` toe als latest artifact.
- Voeg dashboard tabel toe voor laatste drill events.

Acceptatiecriteria:

- Elk drill-resultaat heeft traceerbare `client_order_id`.
- Reconciliation status is zichtbaar in dashboard.
- Unknown/timeout status leidt tot operator action required.
- Evidence export bevat lifecycle timeline.

---

## 8. Fase 5 - Tests

Nieuwe tests:

- `tests/test_roadmap_026_demo_execution_sandbox.py`
- `tests/test_roadmap_026_demo_execution_cli.py`
- `tests/test_roadmap_026_demo_execution_dashboard.py`

Testdoelen:

- Preview bouwt geldige order request met filters.
- Quantity wordt correct afgerond op step size.
- Min notional/min qty blokkades blijven werken.
- Test-order-only roept geen `place_order` aan.
- Place order vereist confirmation.
- Place order vereist Demo Spot profile/base URL.
- Live profile blijft onmogelijk.
- Evidence redaction werkt.
- Dashboard bevat drill panel markers.
- Full pytest blijft groen.

Acceptatiecriteria:

```powershell
python -m pytest tests/test_roadmap_026_demo_execution_sandbox.py tests/test_roadmap_026_demo_execution_cli.py tests/test_roadmap_026_demo_execution_dashboard.py
python -m pytest
python -m binance_spot_bot.cli check-all --skip-tests --json
```

Alle checks slagen.

---

## 9. Documentatie

Toevoegen:

```text
docs/demo-execution-sandbox.md
docs/demo-order-lifecycle-drill.md
```

Aanpassen:

```text
docs/operator-workflow.md
docs/dashboard-operator-evidence.md
docs/security-runbook.md
```

Documentatie moet uitleggen:

- verschil tussen preview, test order en placed Demo Spot order;
- waarom live trading uit blijft;
- welke confirmations nodig zijn;
- waar evidence staat;
- hoe open orders veilig worden gereconciled/gecanceld.

---

## 10. Definition of Done

- Execution sandbox service bestaat.
- CLI drill commands bestaan.
- Dashboard heeft Demo Execution Drill paneel.
- Test-order-only mode is aantoonbaar.
- Demo place order is strikt gated.
- Query/cancel/reconcile drill werkt.
- Evidence report wordt lokaal geschreven.
- Geen secrets in logs/evidence.
- Browser-smoke blijft groen.
- `python -m pytest` slaagt.
- `check-all --skip-tests --json` blijft groen.
- Roadmap wordt na validatie verplaatst naar `Voltooid docs`.

---

## 11. Verplaatsregel

Wanneer deze roadmap volledig is uitgevoerd en gevalideerd:

```text
Roadmap docs/026-roadmap-demo-spot-execution-sandbox-order-lifecycle-drill.md
```

verplaatsen naar:

```text
Voltooid docs/026-roadmap-demo-spot-execution-sandbox-order-lifecycle-drill.md
```
