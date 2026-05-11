# Roadmap 029 - Demo Pilot State Machine Start Recovery & Dashboard Guardrails

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-10  
Locatie:

```text
Voltooid docs/029-roadmap-demo-pilot-state-machine-start-recovery-dashboard-guardrails.md
```

Volgt op:

- `Voltooid docs/028-roadmap-one-click-demo-acceptance-rehearsal-evidence-trends.md`

Live trading blijft volledig buiten scope. Deze roadmap bouwt verder op de bestaande Demo Spot pilot orchestrator, runtime, dashboard, runner telemetry, evidence scorecards en demo acceptance rehearsal. Er wordt niets dubbel gebouwd.

---

## 0. Aanleiding

In het dashboard kan de operator deze fout krijgen bij `Start Demo Spot Pilot`:

```text
ValueError: invalid pilot transition: running -> ready
```

Tracepad:

```text
streamlit_app.py -> _render_demo_pilot() -> runtime.start()
runtime.py -> BotRuntime.start()
pilot_orchestrator.py -> DemoPilotOrchestrator.mark_running()
transition_record(): invalid pilot transition: running -> ready
```

Root cause hypothese:

- Er bestaat al een niet-terminale pilot-run met state `running`.
- De dashboardknop of Streamlit rerun roept `runtime.start()` opnieuw aan.
- `mark_running()` gebruikt `_ensure_run()` en krijgt de bestaande `running` run terug.
- Omdat `record.state != "ready"` wordt de start gate opnieuw geevalueerd.
- De gate kan `ready` teruggeven, waarna `transition_record(record, "ready", ...)` probeert `running -> ready` uit te voeren.
- Die transitie is terecht ongeldig in `PILOT_TRANSITIONS`.

Dit is geen trading-strategieprobleem, maar een lifecycle/state-machine probleem in de operatorlaag.

---

## 1. Doel

Maak de Demo Spot pilot startflow idempotent, herstelbaar en dashboardveilig:

- opnieuw klikken op `Start Demo Spot Pilot` mag nooit crashen;
- een bestaande `running` run blijft `running`;
- een startpoging met actieve run geeft een duidelijke operatorboodschap;
- dashboardknoppen tonen correcte disabled/allowed states;
- stale of inconsistente pilot-run records kunnen veilig worden herkend en hersteld;
- evidence/rehearsal/check-all vangen deze regressie voortaan af.

---

## 2. Scope

### In scope

- State-machine fix in `DemoPilotOrchestrator.mark_running()`.
- Expliciete idempotente startsemantiek voor `running`.
- Dashboard guardrails rond start/stop/resolve knoppen.
- Operator hint bij bestaande actieve run.
- Tests voor dubbele start, stale run en UI-marker gedrag.
- Rehearsal/check-all uitbreiding zodat deze fout niet opnieuw stil binnensluipt.
- Documentatie voor pilot lifecycle recovery.

### Out of scope

- Geen live trading.
- Geen Binance live keys.
- Geen nieuwe exchange adapter.
- Geen nieuwe strategy/model.
- Geen wijziging aan order placement policies buiten lifecycle safety.

---

## 3. Gewenst Gedrag

### Start Demo Spot Pilot

Als er geen actieve run is:

1. Start gate evalueren.
2. Bij allowed: run aanmaken/voorbereiden.
3. Run naar `running`.
4. Start snapshot checkpoint schrijven.

Als er al een run `running` is:

1. Geen transitie naar `ready`.
2. Geen nieuwe run aanmaken.
3. Bestaande run teruggeven.
4. Checkpoint `start_idempotent` schrijven.
5. Dashboardmelding: `Pilot is already running`.

Als er een run `stopping`, `resume_required`, `blocked`, `failed` of `completed` is:

- `stopping`: start blokkeren tot stopflow klaar is.
- `resume_required`: start blokkeren en operator naar reconcile/resolve sturen.
- `blocked`: start gate opnieuw tonen, geen crash.
- `failed`/`completed`: nieuwe run mag pas na expliciete prepare/start flow.

---

## 4. Backend Fixes

### 4.1 `DemoPilotOrchestrator.mark_running()`

Bestand:

```text
src/binance_spot_bot/pilot_orchestrator.py
```

Aanpassen:

- Voeg helper toe:

```text
is_start_idempotent_state(state) -> bool
```

Minimaal:

- `running` is idempotent.
- `paused` kan optioneel naar `running` via bestaande toegestane transitie.
- `stopping` blijft geblokkeerd.

Nieuwe regels:

- Als record state `running` is:
  - geen gate transitie uitvoeren;
  - checkpoint toevoegen;
  - `active_run_id` zetten;
  - record teruggeven.
- Als gate `ready` teruggeeft terwijl record al `running` is, niet transiteren.
- Ongeldige transitions mogen nog steeds failen in unit tests, maar niet door een normale dubbele startklik.

Acceptatiecriteria:

- Dubbele `runtime.start()` veroorzaakt geen `ValueError`.
- Bestaande run blijft dezelfde `run_id`.
- `running -> ready` wordt nergens meer aangeroepen vanuit normale startflow.
- Transition guard blijft streng voor echte ongeldige transities.

### 4.2 `BotRuntime.start()`

Bestand:

```text
src/binance_spot_bot/runtime.py
```

Aanpassen:

- Als runtime al `running` is:
  - idempotent terugkeren;
  - geen dubbele audit spam;
  - optioneel alert `runtime_start_idempotent`.
- Pilot metadata bijwerken met bestaande run.
- `self.message` zetten naar duidelijke status.

Acceptatiecriteria:

- Dubbele dashboardklik blijft stabiel.
- Runtime status blijft `running`.
- Session metadata blijft consistent.

### 4.3 Pilot Run Store Recovery

Bestand:

```text
src/binance_spot_bot/pilot_orchestrator.py
```

Toevoegen of aanscherpen:

- Detecteer latest non-terminal state.
- Stale `running` run ouder dan ingestelde limiet markeren als `resume_required`, niet automatisch als `completed`.
- Maak herstel expliciet via dashboard `Mark resolved`.

Acceptatiecriteria:

- Oude `running` run zonder actieve runtime blokkeert nieuwe start met duidelijke next action.
- Geen stille state reset.
- Geen verlies van audit/checkpoint data.

---

## 5. Dashboard Guardrails

Bestand:

```text
src/binance_spot_bot/ui/streamlit_app.py
```

Aanpassen bij `Pilot Run`:

- `Start Demo Spot Pilot` disabled wanneer:
  - runtime al running is;
  - pilot run state `running` of `stopping` is;
  - resume required actief is;
  - start gate niet allowed is.
- Toon aparte statusbadge:
  - `Runtime`
  - `Pilot run`
  - `Start action`
  - `Recovery action`
- Startknop mag nooit een exception naar Streamlit laten lekken.
- Bij onverwachte `ValueError`:
  - fout vangen;
  - operator hint tonen;
  - event naar audit/evidence schrijven.

Acceptatiecriteria:

- Dashboard crasht niet bij dubbele klik.
- Operator ziet waarom start disabled/geblokkeerd is.
- Safe stop blijft beschikbaar wanneer runtime/pilot running is.
- Mark resolved blijft beschikbaar bij `resume_required`.

---

## 6. Rehearsal & Evidence Updates

Bestanden:

```text
src/binance_spot_bot/demo_acceptance_rehearsal.py
src/binance_spot_bot/evidence_scorecard.py
docs/demo-acceptance-rehearsal.md
```

Uitbreiden:

- Nieuwe rehearsal stap: `pilot-idempotent-start-smoke`.
- Deze stap maakt een veilige lokale runtime/pilot simulatie zonder Binance order placement.
- De stap roept start twee keer aan.
- Verwacht:
  - geen exception;
  - run blijft `running`;
  - run_id blijft gelijk;
  - live trading blijft false.
- Scorecard item toevoegen:
  - `pilot_start_idempotency.pass`
  - warning/fail bij ontbrekende evidence.

Acceptatiecriteria:

- `demo-acceptance-rehearsal --json` detecteert dubbele-start regressie.
- Evidence bundle bevat idempotency artifact.
- Strict mode faalt bij regressie.

---

## 7. Tests

Nieuwe of aangepaste tests:

```text
tests/test_roadmap_029_pilot_state_machine.py
tests/test_roadmap_029_dashboard_start_guardrails.py
tests/test_roadmap_029_rehearsal_idempotency.py
```

Testcases:

- `mark_running()` op bestaande `ready` run maakt `running`.
- `mark_running()` op bestaande `running` run is idempotent.
- Dubbele `BotRuntime.start()` crasht niet.
- Geen `running -> ready` transition in transitions log.
- `stopping` run blokkeert nieuwe start.
- `resume_required` run toont herstelactie.
- Dashboard bevat markers voor disabled start/recovery hint.
- Rehearsal schrijft idempotency artifact.
- Security scan blijft secrets-vrij.

Acceptatiecriteria:

- Nieuwe tests slagen.
- `python -m pytest` slaagt.
- `python -m binance_spot_bot.cli check-all --skip-tests --json` blijft groen.
- `python -m binance_spot_bot.cli demo-acceptance-rehearsal --json` blijft bruikbaar.

---

## 8. Documentatie

Toevoegen:

```text
docs/demo-pilot-state-recovery.md
```

Aanpassen:

```text
docs/operator-workflow.md
docs/demo-acceptance-rehearsal.md
docs/evidence-scorecards.md
```

Documenteren:

- normale pilot lifecycle;
- wat `ready`, `running`, `stopping`, `resume_required`, `completed`, `failed` betekenen;
- wat operator moet doen bij stale running run;
- waarom dubbele start idempotent is;
- waarom dit geen live-trading approval is.

---

## 9. Extra Verbeteringen

### 9.1 Operator UX

- Voeg compacte lifecycle timeline toe in dashboard.
- Toon laatste transition reason.
- Toon laatste checkpoint timestamp.
- Toon recovery call-to-action naast state.

### 9.2 Observability

- Audit event voor:
  - idempotent start;
  - blocked start;
  - stale run detected;
  - recovery completed.
- Evidence artifact voor state-machine health.

### 9.3 Data Hygiene

- Maak oude stale non-terminal runs zichtbaar.
- Voeg `pilot_runs_health` summary toe aan dashboard.
- Geen automatische delete van run evidence.

### 9.4 Safety

- Start blijft onmogelijk wanneer:
  - live trading enabled is;
  - kill switch actief moet blijven;
  - demo profile niet klopt;
  - open orders/reconciliation blockers bestaan.

---

## 10. Definition of Done

- De gemelde Streamlit crash is opgelost.
- Dubbele start is idempotent.
- `running -> ready` kan niet meer via dashboard startflow ontstaan.
- Dashboard toont duidelijke start/recovery state.
- Rehearsal controleert dubbele-start veiligheid.
- Evidence scorecard neemt pilot start idempotency mee.
- Docs zijn bijgewerkt.
- Nieuwe tests slagen.
- `python -m pytest` slaagt.
- `python -m binance_spot_bot.cli check-all --skip-tests --json` slaagt.
- `python -m binance_spot_bot.cli security-scan` geeft geen findings.

Validatie uitgevoerd:

- `python -m pytest tests/test_roadmap_029_pilot_state_machine.py tests/test_roadmap_029_dashboard_start_guardrails.py tests/test_roadmap_029_rehearsal_idempotency.py`
- `python -m pytest`
- `python -m binance_spot_bot.cli check-all --skip-tests --json`
- `python -m binance_spot_bot.cli demo-acceptance-rehearsal --json`
- `python -m binance_spot_bot.cli security-scan`

---

## 11. Verplaatsregel

Wanneer deze roadmap volledig is uitgevoerd en gevalideerd:

```text
Roadmap docs/029-roadmap-demo-pilot-state-machine-start-recovery-dashboard-guardrails.md
```

verplaatsen naar:

```text
Voltooid docs/029-roadmap-demo-pilot-state-machine-start-recovery-dashboard-guardrails.md
```
