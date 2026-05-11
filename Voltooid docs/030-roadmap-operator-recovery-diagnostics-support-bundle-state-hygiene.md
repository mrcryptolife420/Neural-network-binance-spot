# Roadmap 030 - Operator Recovery Diagnostics, Support Bundle & State Hygiene

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-10  
Locatie:

```text
Voltooid docs/030-roadmap-operator-recovery-diagnostics-support-bundle-state-hygiene.md
```

Volgt op:

- `Voltooid docs/028-roadmap-one-click-demo-acceptance-rehearsal-evidence-trends.md`
- `Voltooid docs/029-roadmap-demo-pilot-state-machine-start-recovery-dashboard-guardrails.md`

Live trading blijft volledig buiten scope. Deze roadmap bouwt voort op de bestaande dashboard launcher, Demo Spot pilot lifecycle, runner telemetry, evidence scorecards, demo acceptance rehearsal, security scan en recovery docs. Er wordt niets dubbel gebouwd.

---

## 0. Onderzoeksconclusie

De vorige roadmaps hebben de bot lokaal startbaar, visueel controleerbaar en veiliger gemaakt. Roadmap 029 heeft een concrete dashboardcrash opgelost door de Demo Spot pilot state-machine idempotent te maken.

Wat nu nog ontbreekt is een centrale operatorplek voor:

- lokale state-problemen herkennen;
- runner locks en stale pilot-runs begrijpen;
- evidence-freshness controleren;
- dashboard/rehearsal/check-all/security resultaten samen bekijken;
- veilige herstelacties uitvoeren zonder bestanden handmatig te zoeken;
- een support bundle exporteren wanneer iets misgaat.

De volgende beste verbetering is daarom een **Operator Recovery & Diagnostics Center**. Dit maakt het dashboard robuuster voor echt langdurig lokaal gebruik op Windows 11.

---

## 1. Doel

Maak één dashboard- en CLI-laag die lokaal uitlegt:

- welke subsystemen gezond zijn;
- welke state vastzit of stale is;
- welke recovery-actie veilig is;
- welke evidence ontbreekt of oud is;
- welke bestanden relevant zijn voor debugging;
- hoe een support bundle veilig wordt geëxporteerd zonder secrets.

Na deze roadmap moet de operator niet meer hoeven zoeken in `data/`, `sessions/`, `pilot-runs/`, `checks/` en `evidence/` om te begrijpen waarom de bot niet start, niet stopt of niet door rehearsal komt.

---

## 2. Scope

### In scope

- Nieuwe diagnostics service.
- Nieuwe dashboardsectie of pagina `Recovery & Diagnostics`.
- CLI commands voor state-health en support bundle export.
- State hygiene checks voor pilot-runs, runner locks, rehearsal, scorecard, check-all, browser smoke en local settings.
- Veilige herstelacties met expliciete operatorbevestiging.
- Support bundle met redactie van secrets.
- Integratie met Demo Acceptance Rehearsal en Evidence Scorecard.
- Tests en docs.

### Out of scope

- Geen live trading.
- Geen automatische live-order recovery.
- Geen echte API keys opslaan.
- Geen destructieve cleanup zonder expliciete operatoractie.
- Geen duplicaat van bestaande scorecard, runner of rehearsal logic.

---

## 3. Nieuwe Component

Bestand:

```text
src/binance_spot_bot/operator_diagnostics.py
```

Interfaces:

```text
OperatorDiagnostics(settings, project_root)
  .state_health() -> dict
  .artifact_health() -> dict
  .pilot_run_health() -> dict
  .runner_lock_health() -> dict
  .recommended_actions() -> list[dict]
  .write_health_report() -> Path
  .export_support_bundle() -> Path
```

Output moet altijd bevatten:

- `status`: `ok`, `warn` of `fail`;
- `blockers`;
- `warnings`;
- `next_safe_action`;
- `live_trading_enabled: false`;
- relevante artifact-paden;
- timestamps en age seconds;
- redacted payloads.

Acceptatiecriteria:

- Werkt met lege `data/` map.
- Werkt met corrupte JSON-artifacts door warning te geven, niet te crashen.
- Leest geen secrets naar logs of output.
- Live trading blijft altijd false in diagnostics output.

---

## 4. State Health Checks

Controleer minimaal:

- laatste pilot-run state;
- non-terminal pilot-runs;
- stale `running` pilot-run;
- runner lock state;
- runner telemetry freshness;
- latest rehearsal status;
- latest scorecard status;
- check-all artifact age;
- dashboard browser-smoke artifact age;
- pilot-start-idempotency artifact status;
- launch evidence status;
- local dashboard settings parsebaarheid;
- audit log schrijfbaarheid.

Statusregels:

- `fail`: live trading enabled, security findings, corrupt critical state, runner failed commands, impossible recovery state.
- `warn`: stale/missing evidence, stale runner lock, non-terminal run zonder actieve runtime, missing browser smoke.
- `ok`: geen blockers en geen warnings.

Acceptatiecriteria:

- Een stale runner lock geeft duidelijke next action.
- Een stale non-terminal pilot-run geeft recovery hint, geen automatische reset.
- Missing browser smoke blijft warning, geen blocker.
- Security finding is blocker.

---

## 5. Dashboard: Recovery & Diagnostics

Bestand:

```text
src/binance_spot_bot/ui/streamlit_app.py
```

Toevoegen aan bestaande dashboardstructuur zonder dubbele componenten:

- Sectie of pagina `Recovery & Diagnostics`.
- Badges:
  - `Overall health`
  - `Pilot run`
  - `Runner lock`
  - `Latest rehearsal`
  - `Latest scorecard`
  - `Evidence freshness`
  - `Live`
- Tabellen:
  - blockers;
  - warnings;
  - recommended actions;
  - artifact inventory;
  - recent pilot-runs;
  - recent rehearsals.
- Acties:
  - `Refresh diagnostics`;
  - `Run check-all`;
  - `Run rehearsal`;
  - `Export support bundle`;
  - `Open recovery docs`.

Veilige herstelacties:

- `Mark stale pilot recovery required`;
- `Clear stale runner lock` alleen als lock stale is en proces niet actief lijkt;
- `Archive old generated artifacts` alleen met bevestiging en zonder verwijderen van bewijs.

Acceptatiecriteria:

- Dashboard crasht niet bij lege/corrupte artifacts.
- Start/stop pilot blijft gekoppeld aan bestaande Demo Pilot UI, niet gedupliceerd.
- Elke herstelactie toont wat er gebeurt voordat ze wordt uitgevoerd.
- Geen secrets zichtbaar in tabellen.

---

## 6. CLI Commands

Bestand:

```text
src/binance_spot_bot/cli.py
```

Toevoegen:

```powershell
spot-bot diagnostics --json
spot-bot diagnostics --strict
spot-bot support-bundle --json
spot-bot support-bundle --output data/support/
```

Gedrag:

- `diagnostics --json` print volledige redacted health payload.
- `diagnostics --strict` exit non-zero bij `warn` of `fail`.
- `support-bundle` schrijft zip of directory met redacted artifacts.
- Bundle bevat geen `.env`, geen echte API keys, geen secret values.

Acceptatiecriteria:

- CLI werkt zonder Binance keys.
- CLI werkt met lege `data/`.
- Strict mode faalt bij stale/corrupt critical state.
- Support bundle bevat manifest met checksums en redaction summary.

---

## 7. Support Bundle

Nieuwe output:

```text
data/support/support-bundle-<timestamp>/
```

Minimaal opnemen:

- diagnostics report;
- latest scorecard;
- latest rehearsal;
- check-all artifact;
- launch evidence;
- browser-smoke artifact indien aanwezig;
- pilot-start-idempotency artifact;
- latest pilot-run metadata;
- runner lock/telemetry summary;
- sanitized dashboard settings;
- sanitized audit tail;
- package manifest.

Niet opnemen:

- `.env`;
- raw secrets;
- API key/secret values;
- full account balances als die later gevoelige data bevatten;
- live-order artifacts.

Acceptatiecriteria:

- Secret scan op support bundle geeft geen findings.
- Manifest bevat bestandslijst en redaction status.
- Bundle kan opnieuw worden gelezen door diagnostics.

---

## 8. Rehearsal & Scorecard Integratie

Aanpassen:

```text
src/binance_spot_bot/demo_acceptance_rehearsal.py
src/binance_spot_bot/evidence_scorecard.py
```

Toevoegen:

- Rehearsal step `operator-diagnostics`.
- Scorecard item voor diagnostics report.
- Blocker als diagnostics status `fail`.
- Warning als diagnostics status `warn`.
- Artifact path `data/evidence/diagnostics/latest-diagnostics.json`.

Acceptatiecriteria:

- `demo-acceptance-rehearsal --json` schrijft diagnostics artifact.
- Scorecard ziet diagnostics status.
- Diagnostics zelf veroorzaakt geen circular crash als scorecard ontbreekt.

---

## 9. Tests

Nieuwe tests:

```text
tests/test_roadmap_030_operator_diagnostics.py
tests/test_roadmap_030_support_bundle.py
tests/test_roadmap_030_diagnostics_cli_dashboard.py
tests/test_roadmap_030_rehearsal_scorecard_integration.py
```

Testdoelen:

- diagnostics werkt met lege data map;
- corrupt JSON wordt warning;
- stale pilot-run wordt warning met recovery action;
- stale runner lock wordt warning/blocker volgens severity;
- support bundle redacts secrets;
- support bundle bevat manifest;
- CLI `--strict` faalt bij warn/fail;
- dashboard bevat `Recovery & Diagnostics`;
- rehearsal schrijft diagnostics artifact;
- scorecard verwerkt diagnostics artifact;
- live trading blijft false.

Acceptatiecriteria:

- Nieuwe tests slagen.
- `python -m pytest` slaagt.
- `python -m binance_spot_bot.cli check-all --skip-tests --json` blijft groen.
- `python -m binance_spot_bot.cli demo-acceptance-rehearsal --json` blijft bruikbaar.
- `python -m binance_spot_bot.cli security-scan` geeft geen findings.

---

## 10. Documentatie

Toevoegen:

```text
docs/operator-diagnostics.md
docs/support-bundle.md
```

Aanpassen:

```text
docs/operator-workflow.md
docs/demo-pilot-state-recovery.md
docs/demo-acceptance-rehearsal.md
docs/evidence-scorecards.md
docs/security-runbook.md
```

Documenteren:

- wanneer diagnostics draaien;
- betekenis van `ok`, `warn`, `fail`;
- support bundle maken;
- wat wel/niet in bundle zit;
- hoe stale pilot/runner state veilig wordt behandeld;
- waarom dit geen live-trading approval is.

---

## 11. Windows One-click Verbetering

Bestanden:

```text
scripts/start-dashboard.ps1
Start Bot Dashboard.cmd
```

Toevoegen:

- Na dashboard launch diagnostics preflight draaien.
- Launch evidence uitbreiden met diagnostics status.
- Dashboard automatisch openen zoals bestaande flow.
- Als diagnostics `fail` is: dashboard nog steeds openen, maar Recovery & Diagnostics prominent tonen.

Acceptatiecriteria:

- One-click blijft werken op Windows 11.
- Foutdiagnose staat in dashboard zonder terminal te hoeven lezen.
- Geen nieuwe dependency nodig.

---

## 12. Definition of Done

- OperatorDiagnostics service bestaat.
- CLI diagnostics en support-bundle bestaan.
- Dashboard heeft Recovery & Diagnostics.
- Support bundle redactie is getest.
- Rehearsal bevat diagnostics step.
- Scorecard verwerkt diagnostics status.
- Docs zijn bijgewerkt.
- Nieuwe tests slagen.
- `python -m pytest` slaagt.
- `python -m binance_spot_bot.cli check-all --skip-tests --json` slaagt.
- `python -m binance_spot_bot.cli demo-acceptance-rehearsal --json` slaagt minimaal zonder blockers.
- `python -m binance_spot_bot.cli security-scan` geeft geen findings.

Validatie uitgevoerd:

- `python -m pytest`
- `python -m binance_spot_bot.cli check-all --skip-tests --json`
- `python -m binance_spot_bot.cli diagnostics --json`
- `python -m binance_spot_bot.cli support-bundle --json`
- `python -m binance_spot_bot.cli demo-acceptance-rehearsal --json`
- `python -m binance_spot_bot.cli security-scan`

---

## 13. Verplaatsregel

Wanneer deze roadmap volledig is uitgevoerd en gevalideerd:

```text
Roadmap docs/030-roadmap-operator-recovery-diagnostics-support-bundle-state-hygiene.md
```

verplaatsen naar:

```text
Voltooid docs/030-roadmap-operator-recovery-diagnostics-support-bundle-state-hygiene.md
```
