# Roadmap 027 - Demo Pilot Quality Gates & Evidence Scorecards

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-10  
Locatie:

```text
Roadmap docs/027-roadmap-demo-pilot-quality-gates-evidence-scorecards.md
```

Volgt op:

- `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
- `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
- `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
- `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
- `Voltooid docs/005` t/m `Voltooid docs/026`

Live trading blijft volledig buiten scope. Deze roadmap bouwt voort op de bestaande runner telemetry, dashboard browser-smoke, operator evidence en Demo Execution Drill. Er wordt niets dubbel gebouwd.

Voltooiingsnotitie 2026-05-10:

- `evidence_scorecard.py` toegevoegd met pass/warn/fail quality gates.
- CLI command toegevoegd: `spot-bot evidence-scorecard --json --strict`.
- Dashboard Readiness-tab toont `Evidence Scorecard` met blockers, warnings en next safe action.
- Scorecard beoordeelt launch evidence, browser-smoke, operator evidence, Demo Execution Drill en runner health.
- Docs toegevoegd/bijgewerkt voor evidence scorecards en operator workflow.
- Validatie uitgevoerd: roadmap 027 tests, `python -m pytest` en `python -m binance_spot_bot.cli check-all --skip-tests --json`.

---

## 0. Onderzoeksconclusie

Roadmaps 025 en 026 hebben bewijs en execution-drills toegevoegd:

- dashboard launch evidence;
- browser-smoke met screenshots;
- operator evidence export;
- Demo Execution Drill preview/test/place/query/cancel;
- demo execution lifecycle evidence;
- runner telemetry en command status.

Wat nog ontbreekt is een automatische **kwaliteitspoort** die deze artifacts beoordeelt en één duidelijke operator-score geeft. Nu kan de operator evidence verzamelen, maar moet hij nog zelf interpreteren of een demo pilot goed genoeg was.

De volgende beste verbetering is daarom: **scorecards en gates bovenop bestaande evidence**, zodat het dashboard objectief toont of de bot klaar is voor de volgende demo/paper stap.

---

## 1. Doel

Maak een evidence scorecard die bestaande artifacts beoordeelt:

- launch evidence;
- browser smoke;
- operator evidence;
- runner telemetry;
- Demo Execution Drill evidence;
- check-all output;
- session reports.

De scorecard geeft:

- overall status: `pass`, `warn`, `fail`;
- blockers;
- warnings;
- next safe action;
- links naar relevante artifacts;
- no-live proof.

---

## 2. Scope

### In scope

- Nieuwe scorecard service.
- CLI command voor scorecard generatie.
- Dashboardpaneel met scorecard.
- Evidence schema checks.
- Quality gates voor demo pilot acceptance.
- Tests en docs.

### Out of scope

- Geen live trading.
- Geen nieuwe order execution.
- Geen nieuwe modeltraining.
- Geen duplicate dashboard.
- Geen LLM/autonomous trading decisions.

---

## 3. Nieuwe component

```text
src/binance_spot_bot/evidence_scorecard.py
```

Verantwoordelijkheden:

- artifacts vinden;
- JSON payloads veilig laden;
- score berekenen;
- blockers/warnings verzamelen;
- report schrijven naar `data/evidence/scorecards/`;
- redaction toepassen.

---

## 4. Quality Gates

Minimale gates:

- `live_trading_enabled` moet overal `false` zijn.
- launch evidence moet bestaan.
- browser smoke moet `ok` zijn als dashboard-evidence gevraagd wordt.
- Demo Execution Drill mag geen unknown/reconcile-needed state bevatten.
- runner telemetry mag niet stale zijn.
- command queue mag geen failed commands bevatten.
- check-all moet `ok` zijn of als ontbrekend artifact een warning geven.
- secret scan moet geen findings hebben.

Score:

- `pass`: geen blockers, maximaal beperkte warnings.
- `warn`: geen blockers, maar evidence is incompleet of oud.
- `fail`: een blocker of safety violation.

---

## 5. CLI

Nieuwe commands:

```powershell
spot-bot evidence-scorecard
spot-bot evidence-scorecard --json
spot-bot evidence-scorecard --strict
```

Acceptatiecriteria:

- Command werkt zonder Binance keys.
- Command schrijft JSON naar `data/evidence/scorecards/latest-scorecard.json`.
- `--strict` exit non-zero bij `warn` of `fail`.
- Payload bevat geen secrets.

---

## 6. Dashboard

Toevoegen aan Readiness of Reports:

- paneel `Evidence Scorecard`;
- status badges:
  - overall;
  - blockers;
  - warnings;
  - live disabled;
  - browser smoke;
  - demo execution;
  - runner health;
- tabel met blockers/warnings;
- knop `Generate scorecard`;
- link/pad naar latest scorecard.

Acceptatiecriteria:

- Operator ziet direct pass/warn/fail.
- Next safe action is zichtbaar.
- Geen secrets zichtbaar.
- Browser-smoke blijft groen.

---

## 7. Tests

Nieuwe tests:

- `tests/test_roadmap_027_evidence_scorecard.py`
- `tests/test_roadmap_027_scorecard_cli_dashboard.py`

Testdoelen:

- missing artifacts geven `warn`, geen crash.
- live enabled in artifact geeft `fail`.
- browser smoke failed geeft blocker.
- demo execution unknown/reconcile-needed geeft blocker.
- clean sample artifacts geven `pass`.
- CLI schrijft latest scorecard.
- strict mode faalt bij warnings/failures.
- dashboard bevat scorecard markers.

---

## 8. Docs

Toevoegen:

```text
docs/evidence-scorecards.md
```

Aanpassen:

```text
docs/operator-workflow.md
docs/dashboard-operator-evidence.md
docs/live-readiness-checklist.md
```

Documentatie moet uitleggen:

- hoe scorecards worden gegenereerd;
- welke artifacts worden beoordeeld;
- wat pass/warn/fail betekent;
- waarom dit geen live-trading approval is.

---

## 9. Definition of Done

- Evidence scorecard service bestaat.
- CLI scorecard command bestaat.
- Dashboard toont scorecard.
- Scorecard beoordeelt launch/browser/operator/demo-execution/runner evidence.
- Safety blockers werken.
- Tests slagen.
- `python -m pytest` slaagt.
- `check-all --skip-tests --json` blijft groen.
- Live trading blijft uitgeschakeld.

---

## 10. Verplaatsregel

Wanneer deze roadmap volledig is uitgevoerd en gevalideerd:

```text
Roadmap docs/027-roadmap-demo-pilot-quality-gates-evidence-scorecards.md
```

verplaatsen naar:

```text
Voltooid docs/027-roadmap-demo-pilot-quality-gates-evidence-scorecards.md
```
