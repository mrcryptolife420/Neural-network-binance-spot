# Roadmap 028 - One-click Demo Acceptance Rehearsal & Evidence Trends

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-10  
Locatie:

```text
Voltooid docs/028-roadmap-one-click-demo-acceptance-rehearsal-evidence-trends.md
```

Volgt op:

- `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
- `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
- `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
- `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
- `Voltooid docs/005` t/m `Voltooid docs/027`

Live trading blijft volledig buiten scope. Deze roadmap bouwt voort op de bestaande one-click dashboard launcher, browser-smoke, Demo Execution Drill, operator evidence, runner telemetry en evidence scorecards. Er wordt niets dubbel gebouwd.

---

## 0. Onderzoeksconclusie

De vorige roadmaps hebben nu losse bouwstenen:

- dashboard kan met één klik starten;
- dashboard kan visueel getest worden met browser-smoke;
- Demo Execution Drill kan preview/test/place/query/cancel veilig oefenen;
- operator evidence kan worden geëxporteerd;
- evidence scorecard geeft `pass`, `warn` of `fail`;
- runner telemetry en command status zijn zichtbaar.

Wat nog ontbreekt: een **éénknops acceptatie-repetitie** die deze stappen automatisch in de juiste volgorde uitvoert, bundelt, trendt en als “laatste betrouwbare demo readiness run” toont.

De volgende beste verbetering is daarom een **Demo Acceptance Rehearsal**: één CLI/dashboardactie die check-all, static smoke, browser smoke, demo execution preview/test-order, operator evidence en scorecard combineert in één run met history en trends.

---

## 1. Doel

Maak een operator-run die lokaal bewijst:

- dashboard start veilig;
- browser-smoke werkt;
- no-live safety blijft actief;
- Demo Execution Drill preview werkt;
- test-order-only pad is aantoonbaar veilig;
- evidence scorecard wordt gegenereerd;
- resultaten worden historisch opgeslagen;
- dashboard toont trend over eerdere rehearsals.

Na deze roadmap kan de operator één knop gebruiken: `Run Demo Acceptance Rehearsal`.

---

## 2. Scope

### In scope

- Nieuwe rehearsal orchestrator.
- CLI command voor full rehearsal.
- Dashboardpaneel met runknop en history.
- Evidence bundle per rehearsal.
- Trenddata voor pass/warn/fail, blockers, warnings, runtime en artifact completeness.
- Tests en docs.

### Out of scope

- Geen live trading.
- Geen autonome order placement.
- Geen nieuwe modeltraining.
- Geen duplicaat scorecard.
- Geen nieuwe exchange adapter.

---

## 3. Nieuwe component

```text
src/binance_spot_bot/demo_acceptance_rehearsal.py
```

Verantwoordelijkheden:

- run-id maken;
- bestaande checks in volgorde aanroepen;
- artifacts verzamelen;
- scorecard genereren;
- run summary opslaan;
- trend history bijwerken;
- redaction toepassen;
- no-live contract afdwingen.

Artifactlocaties:

```text
data/evidence/rehearsals/<run_id>/summary.json
data/evidence/rehearsals/<run_id>/artifacts.json
data/evidence/rehearsals/history.jsonl
data/evidence/rehearsals/latest.json
```

---

## 4. Rehearsal stappen

Minimale stappen:

1. `validate-config`
2. `preflight`
3. `dashboard-smoke`
4. optioneel `dashboard-browser-smoke` als URL beschikbaar is
5. `demo-execution-preview`
6. optioneel `demo-execution-test-order` als Demo Spot credentials aanwezig zijn
7. `dashboard-operator-evidence`
8. `evidence-scorecard`

Belangrijk:

- Standaard geen `demo-execution-place`.
- Place order blijft alleen mogelijk in een latere expliciete, apart bevestigde operatoractie.
- Rehearsal moet bruikbaar zijn zonder Binance keys.

---

## 5. CLI

Nieuw command:

```powershell
spot-bot demo-acceptance-rehearsal
spot-bot demo-acceptance-rehearsal --browser-url http://127.0.0.1:8503
spot-bot demo-acceptance-rehearsal --strict
spot-bot demo-acceptance-rehearsal --json
```

Acceptatiecriteria:

- Command werkt zonder Binance keys.
- Command schrijft `latest.json`.
- `--strict` faalt bij scorecard `warn` of `fail`.
- JSON bevat:
  - run id;
  - status;
  - started/finished timestamps;
  - steps;
  - artifact paths;
  - scorecard status;
  - next safe action;
  - `live_trading_enabled: false`.

---

## 6. Dashboard

Toevoegen aan Readiness of Reports:

- Paneel: `Demo Acceptance Rehearsal`.
- Knop: `Run rehearsal`.
- Optioneel inputveld voor browser URL.
- Statusbadges:
  - latest status;
  - scorecard;
  - blockers;
  - warnings;
  - duration;
  - artifacts count;
- Tabellen:
  - latest steps;
  - latest blockers/warnings;
  - recent rehearsals.
- Trend chart:
  - pass/warn/fail over tijd;
  - blockers count over tijd;
  - warnings count over tijd.

Acceptatiecriteria:

- Operator kan rehearsal starten vanuit dashboard.
- Dashboard blijft responsive.
- Geen secrets zichtbaar.
- Browser-smoke blijft optioneel en gebruikt bestaande command/service.

---

## 7. Trend en history

Nieuwe helper:

```text
RehearsalHistory
```

Moet kunnen:

- `append(run_summary)`;
- `latest()`;
- `list_recent(limit=20)`;
- `trend_points()`.

Trendpunten:

- timestamp;
- status;
- scorecard status;
- blocker count;
- warning count;
- duration seconds;
- artifact count.

Acceptatiecriteria:

- History werkt met lege data.
- Corrupt history-regels worden veilig overgeslagen.
- Dashboard kan trends renderen zonder crash.

---

## 8. Tests

Nieuwe tests:

```text
tests/test_roadmap_028_demo_acceptance_rehearsal.py
tests/test_roadmap_028_rehearsal_cli_dashboard.py
```

Testdoelen:

- rehearsal werkt zonder Binance keys;
- no-live flag blijft false;
- missing browser URL geeft warning, geen blocker;
- failed scorecard geeft fail/warn volgens strict mode;
- artifacts worden geschreven;
- history append/list/latest werkt;
- CLI `--strict` exit non-zero bij warn/fail;
- dashboard bevat `Demo Acceptance Rehearsal`;
- trend data schema blijft stabiel.

---

## 9. Docs

Toevoegen:

```text
docs/demo-acceptance-rehearsal.md
```

Aanpassen:

```text
docs/operator-workflow.md
docs/evidence-scorecards.md
docs/dashboard-smoke-tests.md
```

Documentatie moet uitleggen:

- wanneer je een rehearsal draait;
- welke stappen worden uitgevoerd;
- hoe artifacts worden gelezen;
- wat `strict` betekent;
- waarom dit geen live-trading approval is.

---

## 10. Definition of Done

- Rehearsal orchestrator bestaat.
- CLI command bestaat.
- Dashboardpaneel bestaat.
- History/trends werken.
- Scorecard wordt automatisch onderdeel van rehearsal.
- Rehearsal werkt zonder Binance keys.
- Rehearsal lekt geen secrets.
- Live trading blijft disabled.
- Nieuwe tests slagen.
- `python -m pytest` slaagt.
- `python -m binance_spot_bot.cli check-all --skip-tests --json` blijft groen.

Validatie uitgevoerd:

- `python -m pytest tests/test_roadmap_028_demo_acceptance_rehearsal.py tests/test_roadmap_028_rehearsal_cli_dashboard.py`
- `python -m pytest`
- `python -m binance_spot_bot.cli check-all --skip-tests --json`
- `python -m binance_spot_bot.cli demo-acceptance-rehearsal --json`

---

## 11. Verplaatsregel

Wanneer deze roadmap volledig is uitgevoerd en gevalideerd:

```text
Roadmap docs/028-roadmap-one-click-demo-acceptance-rehearsal-evidence-trends.md
```

verplaatsen naar:

```text
Voltooid docs/028-roadmap-one-click-demo-acceptance-rehearsal-evidence-trends.md
```
