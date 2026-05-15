# Roadmap 109 - Streamlit Removal Candidate, Legacy Cleanup \& Dashboard V2-Only Release Hardening

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/109-roadmap-streamlit-removal-candidate-legacy-cleanup-dashboard-v2-only-release-hardening.md
```

## Samenvatting

Roadmap 104 bouwt Dashboard V2 naast Streamlit met FastAPI/WebSocket/React.

Roadmap 105 migreert feature parity van Streamlit naar Dashboard V2.

Roadmap 106 maakt Dashboard V2 performant, lokaal packagebaar, offline/static, browser-smoke-ready en cutover-ready.

Roadmap 107 vereenvoudigt operatorflows, verwerkt UAT-feedback en maakt Streamlit deprecation planning concreet.

Roadmap 108 zet Dashboard V2 als primaire UI neer, maakt V2-only operator mode, lockt final parity, houdt Streamlit als legacy/fallback en bewijst fallback/rollback.

Roadmap 109 is de logische volgende stap: **Streamlit als removal candidate behandelen, legacy code isoleren, overbodige Streamlit-paden opschonen, V2-only release hardenen, rollback archive maken en een finale removal/no-removal gate bouwen**.

Belangrijk: deze roadmap verwijdert Streamlit alleen als alle gates groen zijn. Als er critical parity, UAT, support/evidence, browser smoke of no-live blockers zijn, blijft Streamlit fallback bestaan en wordt Roadmap 109 automatisch een legacy blocker burn-down roadmap.

Live trading blijft volledig buiten scope. Dashboard V2 blijft local-only en beperkt tot demo, paper en testnet-readiness. Geen live mode, geen signed real-order endpoints, geen echte account workflows en geen externe telemetry.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 109`, `109-roadmap`, `Streamlit Removal Candidate`, `Dashboard V2-Only Release`, `Legacy Cleanup` en `V2-only release`.
* \[x] Geen bestaande Roadmap 109 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 108 is lokaal aangemaakt als Dashboard V2 Legacy Streamlit Deprecation Execution, Final Parity Lock \& V2-Only Operator Mode.

### Codebasecontrole

Breed bekeken met focus op Streamlit legacy, Dashboard V2-only hardening, CLI, runtime, check-all en safety:

* \[x] `src/binance\_spot\_bot/ui/streamlit\_app.py`
* \[x] `src/binance\_spot\_bot/ui/page\_registry.py`
* \[x] `src/binance\_spot\_bot/ui/components.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] `pyproject.toml`
* \[x] roadmaplijn 104-108.

### Belangrijke bestaande basis

De codebase heeft nu:

* \[x] Een Streamlit app die veel dashboardfunctionaliteit bevat.
* \[x] Een page registry met alle dashboard pages en safety-check dat live trading pages blokkeert.
* \[x] Runtime modes zijn `demo`, `paper` en `testnet-readiness`.
* \[x] Runtime snapshots bevatten candles, signals, fills, equity, model, readiness, orders, sessions, demo pilot, reconciliation en alerts.
* \[x] Check-all forceert `LIVE\_TRADING\_ENABLED=false`, `KILL\_SWITCH=true` en `PYTHONPATH=src`.
* \[x] CLI heeft al dashboard/smoke/support/evidence/paper/demo/operator commands.
* \[x] Roadmap 104-108 maken het pad naar Dashboard V2-first en Streamlit legacy/fallback.

### Belangrijkste gat na Roadmap 108

Na Roadmap 108 is Dashboard V2 primary en Streamlit legacy/fallback, maar Streamlit zit nog steeds in de repo en kan nog steeds:

* \[x] dependency complexity houden;
* \[x] dubbele dashboardwaarheid veroorzaken;
* \[x] extra check-all/import-smoke kosten geven;
* \[x] oude docs/commands in leven houden;
* \[x] nieuwe features per ongeluk terug naar Streamlit trekken;
* \[x] operatorverwarring veroorzaken;
* \[x] release packaging zwaarder maken;
* \[x] oude component wrappers laten bestaan;
* \[x] legacy tests en browser smoke dupliceren;
* \[x] cleanup moeilijker maken.

Roadmap 109 lost dit op met gecontroleerde cleanup en removal-candidate gates.

\---

## 1\. Hoofddoel Roadmap 109

Maak het project klaar voor een veilige V2-only dashboard release:

```text
Dashboard V2 primary
â†’ Streamlit legacy inventory
â†’ final removal gate
â†’ dependency isolation
â†’ legacy code archive
â†’ V2-only release hardening
â†’ rollback package
â†’ removal candidate evidence
```

Na Roadmap 109 moet het project kunnen:

* \[x] Dashboard V2 volledig V2-only draaien zonder Streamlit import.
* \[x] Streamlit dependency optioneel/legacy houden of veilig verwijderen als gate groen is.
* \[x] Alle Streamlit-only code inventariseren en classificeren.
* \[x] Legacy files archiveren of isoleren.
* \[x] Streamlit imports uit core checks en default CLI halen.
* \[x] V2-only check-all profile draaien.
* \[x] V2-only support/evidence bundles maken.
* \[x] V2-only release simulation draaien.
* \[x] Rollback naar legacy archive/fallback documenteren.
* \[x] No-live proof behouden.
* \[x] Een harde beslissing geven:

  * remove\_now;
  * keep\_legacy;
  * blocked\_cleanup\_required.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[x] Geen Dashboard V2 foundation opnieuw bouwen.
* \[x] Geen page parity opnieuw plannen.
* \[x] Geen UX wizards opnieuw bouwen.
* \[x] Geen runtime refactor opnieuw bouwen.
* \[x] Geen model/data/portfolio pipelines opnieuw bouwen.
* \[x] Geen live trading.
* \[x] Geen live mode.
* \[x] Geen signed real-order endpoints.
* \[x] Geen echte account workflows.
* \[x] Geen cloud dashboard.
* \[x] Geen remote telemetry.
* \[x] Geen Streamlit verwijderen zonder removal gate.
* \[x] Geen fallback archive overschrijven zonder hash/evidence.
* \[x] Geen docs verwijderen zonder V2 equivalent.

Wel doen:

* \[x] Streamlit legacy inventariseren;
* \[x] V2-only imports/checks hard maken;
* \[x] dependency isoleren;
* \[x] legacy tests en docs opruimen;
* \[x] support/evidence/release V2-only maken;
* \[x] rollback archive maken;
* \[x] final removal gate bouwen;
* \[x] no-live proof behouden.

\---

## 3\. Fase 0 - Streamlit Removal Candidate Safety Contract

Nieuw docbestand:

```text
docs/dashboard-v2-streamlit-removal-candidate-safety-contract.md
```

Regels:

* \[x] Removal candidate is local-only.
* \[x] Geen live trading.
* \[x] Geen live mode in V2-only UI, backend, CLI, docs of tests.
* \[x] Alleen demo, paper en testnet-readiness.
* \[x] Streamlit removal mag alleen na removal gate pass.
* \[x] Als gate faalt, blijft Streamlit legacy/fallback.
* \[x] V2-only mode mag geen Streamlit import nodig hebben.
* \[x] V2-only release moet support/evidence/no-live proof hebben.
* \[x] Rollback archive is verplicht vÃ³Ã³r removal.
* \[x] Legacy docs mogen pas weg na V2 docs coverage.
* \[x] Legacy commands mogen pas weg na V2 CLI coverage.
* \[x] Reports/evidence zijn secret-free.
* \[x] Removal decision is auditable en reversible via archive.

Acceptatiecriteria:

* \[x] Safety contract bestaat.
* \[x] Tests bewijzen no-live proof verplicht is.
* \[x] Tests bewijzen removal gate faalt bij missing V2 parity.
* \[x] Tests bewijzen rollback archive verplicht is.
* \[x] Tests bewijzen reports secret-free zijn.

\---

## 4\. Fase 1 - Streamlit Removal Readiness Gate

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/removal\_readiness\_gate.py
```

Inputs:

* \[x] Roadmap 108 deprecation gate report.
* \[x] final parity lock report.
* \[x] critical workflow lock report.
* \[x] V2-only smoke report.
* \[x] V2 browser smoke matrix.
* \[x] V2 API smoke.
* \[x] V2 UAT sign-off.
* \[x] support/evidence V2-first verification.
* \[x] Streamlit-only inventory.
* \[x] docs V2-first check.
* \[x] rollback archive manifest.
* \[x] no-live proof pack.
* \[x] check-all V2-only profile result.

Gate outcomes:

* \[x] `remove\_now`
* \[x] `keep\_legacy`
* \[x] `blocked\_cleanup\_required`
* \[x] `unsafe`

Hard blockers:

* \[x] live mode found.
* \[x] no-live proof missing.
* \[x] V2-only smoke failed.
* \[x] V2 browser smoke failed on critical route.
* \[x] V2 UAT P0/P1 open.
* \[x] critical page parity missing.
* \[x] support/evidence V2 failed.
* \[x] rollback archive missing.
* \[x] Streamlit still imported by V2-only path.
* \[x] docs still Streamlit-first.
* \[x] check-all V2-only profile failed.

Acceptatiecriteria:

* \[x] Gate is deterministic.
* \[x] Gate never removes code itself.
* \[x] Gate explains blockers.
* \[x] Gate output is Markdown + JSON.
* \[x] Tests cover remove\_now/keep\_legacy/blocked/unsafe.

\---

## 5\. Fase 2 - Streamlit Dependency Isolation

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/dependency\_isolation.py
```

Doel: Streamlit afhankelijkheid scheiden van core en V2.

Taken:

* \[x] Detecteer `import streamlit` buiten legacy UI package.
* \[x] Detecteer `st.` usage buiten legacy UI package.
* \[x] Detecteer Streamlit dependency in default install path.
* \[x] Maak dependency group `legacy-streamlit` of behoud `\[ui]` als legacy.
* \[x] Zorg dat Dashboard V2 dependency group zonder Streamlit kan installeren.
* \[x] Zorg dat V2-only imports werken zonder Streamlit installed.
* \[x] Rapporteer packages die Streamlit hard importeren.

Aanbevolen dependency layout:

```toml
\[project.optional-dependencies]
dashboard-v2 = \[
  "fastapi>=0.115",
  "uvicorn>=0.30",
  "pydantic>=2.7",
  "websockets>=12",
]
legacy-streamlit = \[
  "streamlit>=...",
  "plotly>=..."
]
```

Acceptatiecriteria:

* \[x] V2-only import test werkt zonder Streamlit.
* \[x] Streamlit imports alleen in legacy package.
* \[x] pyproject heeft duidelijke legacy dependency.
* \[x] Check-all heeft V2-only profile zonder Streamlit.
* \[x] Tests gebruiken import monkeypatch/fixture.

\---

## 6\. Fase 3 - Legacy Streamlit Archive Builder

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/legacy\_archive.py
```

Archive bevat:

* \[x] `ui/streamlit\_app.py`
* \[x] Streamlit-only components.
* \[x] Streamlit docs.
* \[x] Streamlit smoke reports.
* \[x] Streamlit page/action inventory.
* \[x] Streamlit fallback instructions.
* \[x] hash manifest.
* \[x] rollback instructions.
* \[x] no-live statement.

Output:

```text
data/dashboard-v2/legacy-archive/<run\_id>/
  streamlit\_legacy\_archive\_manifest.json
  streamlit\_legacy\_archive\_summary.md
  files/
```

Acceptatiecriteria:

* \[x] Archive is created before removal candidate.
* \[x] Archive has hashes.
* \[x] Archive is secret-free.
* \[x] Archive can be verified.
* \[x] Rollback instructions are included.

\---

## 7\. Fase 4 - Streamlit Code Isolation / Move Plan

Geen blind deletion. Eerst isolatieplan:

Optie A:

```text
src/binance\_spot\_bot/ui\_legacy\_streamlit/
```

Optie B:

```text
src/binance\_spot\_bot/ui/legacy\_streamlit/
```

Plan:

* \[x] Streamlit app onder legacy path plaatsen.
* \[x] Compat import houden voor Ã©Ã©n release:

  * `binance\_spot\_bot.ui.streamlit\_app` â†’ legacy wrapper.
* \[x] Waarschuwing tonen bij legacy import.
* \[x] `launch-dashboard --legacy-streamlit` gebruikt legacy path.
* \[x] V2-only paths importeren legacy niet.
* \[x] Legacy wrapper kan later verwijderd worden.

Acceptatiecriteria:

* \[x] Legacy path werkt.
* \[x] Oude import geeft deprecation warning maar werkt.
* \[x] V2-only smoke importeert geen legacy path.
* \[x] Tests cover old/new import path.
* \[x] No-live banner blijft in legacy UI.

\---

## 8\. Fase 5 - Streamlit Component Cleanup

Inventariseer componenten:

* \[x] chart wrappers.
* \[x] metric cards.
* \[x] badges.
* \[x] JSON expanders.
* \[x] tables.
* \[x] alert lists.
* \[x] demo pilot charts.
* \[x] evidence/support widgets.

Acties:

* \[x] Markeer legacy-only.
* \[x] Verwijder duplicaten alleen als V2 equivalent bestaat.
* \[x] Verplaats nuttige pure helpers naar shared non-Streamlit module.
* \[x] Houd Streamlit wrappers in legacy package.
* \[x] Voeg tests toe voor pure helper extraction.

Acceptatiecriteria:

* \[x] Geen Streamlit imports in shared helpers.
* \[x] Legacy wrappers blijven werken.
* \[x] V2 gebruikt eigen components/frontend.
* \[x] Cleanup report bestaat.
* \[x] Tests pass.

\---

## 9\. Fase 6 - CLI V2-Only Default Finalization

Wijzig CLI default na removal gate:

* \[x] `dashboard` â†’ Dashboard V2 default.
* \[x] `dashboard --legacy-streamlit` â†’ legacy fallback.
* \[x] `launch-dashboard` â†’ waarschuwing of alias naar V2 afhankelijk policy.
* \[x] `launch-dashboard --legacy-streamlit` beschikbaar.
* \[x] `dashboard-v2` blijft expliciet.
* \[x] `dashboard-status` toont default UI.
* \[x] `dashboard-fallback-info` toont rollback.

Safety:

* \[x] No-live statement in CLI output.
* \[x] Geen live flags.
* \[x] Geen signed/account/order actions.

Acceptatiecriteria:

* \[x] CLI default is V2 when gate pass.
* \[x] Legacy command still works if legacy kept.
* \[x] Old commands produce helpful migration message.
* \[x] Tests cover CLI routing.
* \[x] Docs updated.

\---

## 10\. Fase 7 - V2-Only Check-All Profile

Nieuwe profiles:

```text
check-all --profile v2-only
check-all --profile v2-release
check-all --profile legacy-fallback
```

V2-only checks:

* \[x] V2 imports without Streamlit.
* \[x] V2 API smoke.
* \[x] V2 browser smoke.
* \[x] V2 no-live proof.
* \[x] V2 critical workflow lock.
* \[x] V2 support/evidence export.
* \[x] V2 UAT evidence.
* \[x] Streamlit dependency absent from V2 import graph.

Legacy fallback checks:

* \[x] Legacy Streamlit import if installed.
* \[x] Legacy no-live banner.
* \[x] Legacy fallback command.
* \[x] Legacy archive exists.

Acceptatiecriteria:

* \[x] V2-only profile works without Streamlit.
* \[x] Legacy profile is optional.
* \[x] No-live failure hard fails.
* \[x] Reports are secret-free.
* \[x] Check-all fast remains reasonable.

\---

## 11\. Fase 8 - V2-Only Support \& Evidence Bundle

Support/evidence must not rely on Streamlit.

Update:

* \[x] support bundle can be created from V2 UI.
* \[x] support bundle can be created from CLI.
* \[x] evidence manifest can be created from V2 UI.
* \[x] operator quality gate visible in V2.
* \[x] local ops snapshot visible in V2.
* \[x] redaction self-test visible in V2.
* \[x] no-live proof visible in V2.

Acceptatiecriteria:

* \[x] V2 support/evidence workflow passes.
* \[x] Streamlit not required.
* \[x] Artifacts secret-free.
* \[x] Reports linked in V2.
* \[x] Tests use temp dirs.

\---

## 12\. Fase 9 - V2-Only Release Simulation

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/v2\_release\_simulation.py
```

Simulation checks:

* \[x] clean env without Streamlit.
* \[x] install core + dashboard-v2 extras.
* \[x] import package.
* \[x] launch V2 app fake/server smoke.
* \[x] API smoke.
* \[x] browser smoke if configured.
* \[x] support/evidence smoke.
* \[x] check-all v2-only.
* \[x] no-live proof.
* \[x] static assets present.
* \[x] release version manifest.
* \[x] rollback archive present.

Acceptatiecriteria:

* \[x] Simulation output JSON + Markdown.
* \[x] Missing Streamlit does not fail V2.
* \[x] Missing V2 dependency gives useful error.
* \[x] No-live proof included.
* \[x] Tests use fake environment.

\---

## 13\. Fase 10 - Legacy Docs Freeze \& V2-Only Docs Lock

Docs changes:

* \[x] README dashboard section V2-only primary.
* \[x] Streamlit marked legacy fallback only.
* \[x] Legacy docs archived.
* \[x] Operator manual V2-only primary.
* \[x] CLI cookbook V2 commands primary.
* \[x] Troubleshooting V2-first.
* \[x] Release docs V2-only.
* \[x] Legacy fallback docs retained.
* \[x] Removal candidate docs explain gates.

Docs checks:

* \[x] No Streamlit-first instructions except legacy fallback.
* \[x] No live approval wording.
* \[x] All V2 commands exist.
* \[x] All legacy references have fallback context.
* \[x] Broken links fail.

Acceptatiecriteria:

* \[x] Docs V2-only lock passes.
* \[x] Legacy docs archive exists.
* \[x] Docs consistency tests pass.
* \[x] Operator can still find fallback info.
* \[x] No-live statement present.

\---

## 14\. Fase 11 - Legacy Test Cleanup

Tasks:

* \[x] Mark Streamlit tests as legacy.
* \[x] Move Streamlit tests under `tests/legacy\_streamlit/`.
* \[x] Keep minimal fallback smoke.
* \[x] Remove duplicated full legacy browser matrix.
* \[x] Ensure V2 tests cover primary workflows.
* \[x] Test selector maps dashboard changes to V2 by default.
* \[x] Streamlit changes trigger legacy freeze test.

Acceptatiecriteria:

* \[x] V2 tests are primary.
* \[x] Legacy tests only cover fallback.
* \[x] Test selection updated.
* \[x] Check-all profiles updated.
* \[x] No-live tests still cover both when legacy installed.

\---

## 15\. Fase 12 - Legacy Runtime/State Coupling Audit

Doel: zorgen dat runtime niet afhankelijk blijft van Streamlit session state.

Checks:

* \[x] `st.session\_state` usage only in legacy UI.
* \[x] runtime bridge owns V2 state.
* \[x] settings/profile persistence not Streamlit-only.
* \[x] dashboard actions go through V2 action policy.
* \[x] runtime snapshot DTOs independent.
* \[x] no shared mutable conflict between legacy and V2.

Acceptatiecriteria:

* \[x] No Streamlit state usage outside legacy.
* \[x] V2 can run with fresh process.
* \[x] V2 can restart after crash.
* \[x] Legacy/V2 not run against same runtime by default unless safe.
* \[x] Audit report exists.

\---

## 16\. Fase 13 - Removal Patch Plan

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/removal\_patch\_plan.py
```

Generates exact plan:

* \[x] files to move;
* \[x] files to delete later;
* \[x] imports to update;
* \[x] docs to update;
* \[x] tests to move;
* \[x] dependencies to change;
* \[x] CLI aliases to keep;
* \[x] rollback archive path;
* \[x] validation commands;
* \[x] no-live proof command.

Patch decision:

* \[x] `plan\_only`
* \[x] `isolate\_legacy`
* \[x] `remove\_after\_gate`
* \[x] `blocked`

Acceptatiecriteria:

* \[x] Plan is generated before deletion.
* \[x] Plan includes rollback.
* \[x] Plan has validation commands.
* \[x] Plan is Markdown + JSON.
* \[x] Tests cover blocked plan.

\---

## 17\. Fase 14 - Optional Removal Execution Gate

Deze fase voert nog steeds geen automatische deletion uit zonder expliciete confirm.

Command:

```powershell
python -m binance\_spot\_bot.cli dashboard-v2-streamlit-removal-execute --confirm REMOVE\_STREAMLIT\_LEGACY\_AFTER\_GATE
```

Guardrails:

* \[x] removal readiness gate must be `remove\_now`.
* \[x] rollback archive verified.
* \[x] V2-only release simulation pass.
* \[x] check-all v2-only pass.
* \[x] no-live proof pass.
* \[x] operator confirmation required.
* \[x] dry-run default.
* \[x] patch plan printed first.
* \[x] legacy fallback archived.

Acceptatiecriteria:

* \[x] Dry-run default.
* \[x] Execute blocked without exact confirm.
* \[x] Execute blocked if gate not remove\_now.
* \[x] Execute blocked if archive missing.
* \[x] Tests use temp fixture repo.

\---

## 18\. Fase 15 - Post-Removal Verification

If removal executed or legacy isolated:

Checks:

* \[x] package imports without Streamlit.
* \[x] Dashboard V2 launches.
* \[x] API smoke passes.
* \[x] browser smoke passes.
* \[x] check-all v2-only passes.
* \[x] support/evidence passes.
* \[x] docs V2-only pass.
* \[x] no-live proof pass.
* \[x] legacy archive verify pass.
* \[x] rollback instructions still exist.

Acceptatiecriteria:

* \[x] Verification report exists.
* \[x] Failures produce rollback instructions.
* \[x] No-live failure hard fails.
* \[x] Reports secret-free.
* \[x] Release simulation reads verification.

\---

## 19\. Fase 16 - Rollback Verification Drill

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/removal\_rollback\_drill.py
```

Drill:

* \[x] load legacy archive.
* \[x] verify hashes.
* \[x] simulate restore to temp dir.
* \[x] import legacy Streamlit path if dependencies installed.
* \[x] verify no-live banner text.
* \[x] verify fallback command docs.
* \[x] export drill report.

Acceptatiecriteria:

* \[x] Drill works offline.
* \[x] Drill does not mutate working tree by default.
* \[x] Hash mismatch fails.
* \[x] Report is secret-free.
* \[x] Tests use fixture archive.

\---

## 20\. Fase 17 - V2-Only Release Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/v2\_only\_release\_evidence.py
```

Bundle bevat:

* \[x] safety contract.
* \[x] removal readiness gate.
* \[x] dependency isolation report.
* \[x] legacy archive manifest.
* \[x] code isolation report.
* \[x] component cleanup report.
* \[x] CLI V2-only default report.
* \[x] check-all V2-only report.
* \[x] support/evidence V2 report.
* \[x] release simulation report.
* \[x] docs lock report.
* \[x] legacy test cleanup report.
* \[x] runtime/state coupling audit.
* \[x] removal patch plan.
* \[x] optional removal execution result.
* \[x] post-removal verification.
* \[x] rollback drill.
* \[x] no-live proof.
* \[x] hashes.

Output:

```text
data/dashboard-v2/v2-only-release/evidence/<run\_id>/
  dashboard\_v2\_only\_release\_evidence\_manifest.json
  dashboard\_v2\_only\_release\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[x] Bundle is secret-free.
* \[x] Bundle has manifest/hash.
* \[x] Bundle can be verified.
* \[x] Bundle clearly states removal decision.
* \[x] Bundle included in release evidence.

\---

## 21\. Fase 18 - Release/Migration Integration

Roadmap 089:

* \[x] Release manifest includes `dashboard\_ui=dashboard-v2`.
* \[x] Release notes include Streamlit removal/legacy status.
* \[x] Migration notes explain V2-only install.
* \[x] Legacy archive path included.
* \[x] Rollback instructions included.
* \[x] Release quality gate reads V2-only evidence.
* \[x] Versioned upgrade path handles legacy configs.

Acceptatiecriteria:

* \[x] Release simulation V2-only pass.
* \[x] Migration notes generated.
* \[x] Rollback instructions generated.
* \[x] Release evidence secret-free.
* \[x] No-live proof included.

\---

## 22\. Fase 19 - Knowledge/Test/Impact Integration

Roadmap 091:

* \[x] Knowledge graph marks Streamlit removed/legacy.
* \[x] Dashboard V2 routes become primary UI graph.
* \[x] Legacy archive indexed as archive, not active module.
* \[x] Impact analysis flags any new Streamlit import.

Roadmap 092:

* \[x] Test selector chooses V2 tests by default.
* \[x] Streamlit import changes trigger legacy/removal tests.
* \[x] pyproject dependency changes trigger dependency isolation tests.
* \[x] docs changes trigger V2-only docs tests.

Acceptatiecriteria:

* \[x] Impact analysis detects reintroduced Streamlit import.
* \[x] Test selection is V2-first.
* \[x] Knowledge graph updated.
* \[x] Reports secret-free.
* \[x] No-live proof preserved.

\---

## 23\. Fase 20 - Operator/UAT Integration

Roadmap 102:

* \[x] Operator manual V2-only primary.
* \[x] Support playbooks mention no Streamlit dependency by default.
* \[x] CLI cookbook uses V2 commands.
* \[x] Fallback/rollback guide linked.

Roadmap 103:

* \[x] UAT scenarios run V2-only.
* \[x] UAT fallback scenario uses archive/legacy if present.
* \[x] UAT sign-off requires V2-only pass.
* \[x] UAT scorecard includes removal decision.

Acceptatiecriteria:

* \[x] V2-only UAT pass.
* \[x] Operator docs pass.
* \[x] Fallback instructions clear.
* \[x] UAT P0/P1 block removal.
* \[x] No-live proof preserved.

\---

## 24\. Fase 21 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli dashboard-v2-removal-readiness-gate --json
python -m binance\_spot\_bot.cli dashboard-v2-dependency-isolation --json
python -m binance\_spot\_bot.cli dashboard-v2-legacy-archive-create
python -m binance\_spot\_bot.cli dashboard-v2-legacy-archive-verify --archive <path>
python -m binance\_spot\_bot.cli dashboard-v2-streamlit-isolation-plan --json
python -m binance\_spot\_bot.cli dashboard-v2-component-cleanup-report --json
python -m binance\_spot\_bot.cli dashboard-v2-check-all --profile v2-only --json
python -m binance\_spot\_bot.cli dashboard-v2-support-evidence-smoke --json
python -m binance\_spot\_bot.cli dashboard-v2-release-simulation --json
python -m binance\_spot\_bot.cli dashboard-v2-docs-v2-only-lock --json
python -m binance\_spot\_bot.cli dashboard-v2-legacy-test-cleanup-report --json
python -m binance\_spot\_bot.cli dashboard-v2-runtime-state-coupling-audit --json
python -m binance\_spot\_bot.cli dashboard-v2-removal-patch-plan --json
python -m binance\_spot\_bot.cli dashboard-v2-streamlit-removal-execute --dry-run
python -m binance\_spot\_bot.cli dashboard-v2-streamlit-removal-execute --confirm REMOVE\_STREAMLIT\_LEGACY\_AFTER\_GATE
python -m binance\_spot\_bot.cli dashboard-v2-post-removal-verify --json
python -m binance\_spot\_bot.cli dashboard-v2-removal-rollback-drill --json
python -m binance\_spot\_bot.cli dashboard-v2-only-release-evidence-export
```

Acceptatiecriteria:

* \[x] Commands werken offline.
* \[x] Commands ondersteunen JSON waar relevant.
* \[x] Dangerous command is dry-run by default.
* \[x] Exact confirm required for execution.
* \[x] Commands gebruiken geen signed/order/account endpoints.
* \[x] Reports zijn secret-free.

\---

## 25\. Fase 22 - Tests

### Unit tests

* \[x] `tests/test\_dashboard\_v2\_streamlit\_removal\_candidate\_safety\_contract.py`
* \[x] `tests/test\_dashboard\_v2\_removal\_readiness\_gate.py`
* \[x] `tests/test\_dashboard\_v2\_dependency\_isolation.py`
* \[x] `tests/test\_dashboard\_v2\_legacy\_archive.py`
* \[x] `tests/test\_dashboard\_v2\_streamlit\_code\_isolation.py`
* \[x] `tests/test\_dashboard\_v2\_component\_cleanup.py`
* \[x] `tests/test\_dashboard\_v2\_cli\_v2\_only\_default.py`
* \[x] `tests/test\_dashboard\_v2\_check\_all\_profiles.py`
* \[x] `tests/test\_dashboard\_v2\_v2\_release\_simulation.py`
* \[x] `tests/test\_dashboard\_v2\_docs\_v2\_only\_lock.py`
* \[x] `tests/test\_dashboard\_v2\_legacy\_test\_cleanup.py`
* \[x] `tests/test\_dashboard\_v2\_runtime\_state\_coupling\_audit.py`
* \[x] `tests/test\_dashboard\_v2\_removal\_patch\_plan.py`
* \[x] `tests/test\_dashboard\_v2\_removal\_execution\_gate.py`
* \[x] `tests/test\_dashboard\_v2\_post\_removal\_verification.py`
* \[x] `tests/test\_dashboard\_v2\_removal\_rollback\_drill.py`
* \[x] `tests/test\_dashboard\_v2\_only\_release\_evidence.py`

### Integration tests

* \[x] V2-only import fixture without Streamlit.
* \[x] Legacy archive create/verify fixture.
* \[x] Dependency isolation fixture.
* \[x] Removal readiness pass/fail fixture.
* \[x] V2-only release simulation fixture.
* \[x] Removal patch plan dry-run fixture.
* \[x] Optional removal execution temp-repo fixture.
* \[x] Post-removal verification fixture.
* \[x] Rollback drill fixture.
* \[x] Evidence bundle export/verify fixture.

### Browser smoke

* \[x] Dashboard V2 loads.
* \[x] No-live banner visible.
* \[x] Start wizard visible.
* \[x] Demo spot guided flow visible.
* \[x] Paper session workflow visible.
* \[x] Evidence/support visible.
* \[x] V2-only mode visible.
* \[x] No Streamlit fallback required for primary workflows.

### Safety tests

* \[x] Live mode absent.
* \[x] Signed/order/account endpoints absent.
* \[x] No-live proof mandatory.
* \[x] Removal blocked without archive.
* \[x] Removal blocked if V2 smoke fails.
* \[x] Removal blocked if Streamlit imported by V2-only path.
* \[x] Removal command exact confirm required.
* \[x] Evidence secret-free.
* \[x] Rollback archive hash verified.
* \[x] Check-all safe env preserved.

\---

## 26\. Fase 23 - Docs

Nieuwe docs:

```text
docs/dashboard-v2/streamlit-removal-candidate-safety-contract.md
docs/dashboard-v2/removal-readiness-gate.md
docs/dashboard-v2/dependency-isolation.md
docs/dashboard-v2/legacy-archive.md
docs/dashboard-v2/streamlit-code-isolation.md
docs/dashboard-v2/component-cleanup.md
docs/dashboard-v2/cli-v2-only-default.md
docs/dashboard-v2/check-all-v2-only-profile.md
docs/dashboard-v2/v2-only-support-evidence.md
docs/dashboard-v2/v2-only-release-simulation.md
docs/dashboard-v2/docs-v2-only-lock.md
docs/dashboard-v2/legacy-test-cleanup.md
docs/dashboard-v2/runtime-state-coupling-audit.md
docs/dashboard-v2/removal-patch-plan.md
docs/dashboard-v2/removal-execution-gate.md
docs/dashboard-v2/post-removal-verification.md
docs/dashboard-v2/removal-rollback-drill.md
docs/dashboard-v2/v2-only-release-evidence.md
```

README updates:

* \[x] Dashboard V2 primary.
* \[x] Streamlit legacy/removal status.
* \[x] V2-only install instructions.
* \[x] V2-only check commands.
* \[x] Legacy archive/rollback instructions.
* \[x] No-live statement.

Operator docs updates:

* \[x] V2-only daily workflow.
* \[x] Fallback/rollback guide.
* \[x] Support/evidence V2-only guide.
* \[x] Removal candidate explanation.

\---

## 27\. Codex bouwvolgorde

### PR 1 - Safety Contract + Removal Readiness Gate

* \[x] `docs/dashboard-v2-streamlit-removal-candidate-safety-contract.md`
* \[x] `dashboard\_v2/removal\_readiness\_gate.py`
* \[x] gate tests.
* \[x] no-live tests.

### PR 2 - Dependency Isolation

* \[x] `dashboard\_v2/dependency\_isolation.py`
* \[x] pyproject optional dependency split.
* \[x] import isolation tests.

### PR 3 - Legacy Archive Builder

* \[x] `dashboard\_v2/legacy\_archive.py`
* \[x] archive create/verify.
* \[x] hash tests.

### PR 4 - Streamlit Code Isolation Plan

* \[x] legacy package/path plan.
* \[x] compat wrapper.
* \[x] old/new import tests.

### PR 5 - Component Cleanup + Runtime State Coupling Audit

* \[x] `dashboard\_v2/component\_cleanup.py`
* \[x] `dashboard\_v2/runtime\_state\_coupling\_audit.py`
* \[x] shared helper extraction tests.

### PR 6 - CLI V2-Only Default + Check-All Profiles

* \[x] CLI routing changes.
* \[x] v2-only check-all profile.
* \[x] tests.

### PR 7 - V2-Only Support/Evidence + Release Simulation

* \[x] support/evidence V2-only smoke.
* \[x] `v2\_release\_simulation.py`
* \[x] release simulation tests.

### PR 8 - Docs Lock + Legacy Test Cleanup

* \[x] docs V2-only lock.
* \[x] legacy test cleanup.
* \[x] docs/test selector tests.

### PR 9 - Removal Patch Plan + Optional Execution Gate

* \[x] `removal\_patch\_plan.py`
* \[x] dry-run/confirm gate.
* \[x] temp-repo tests.

### PR 10 - Post-Removal Verify + Rollback + Evidence + Integrations

* \[x] `post\_removal\_verification.py`
* \[x] `removal\_rollback\_drill.py`
* \[x] `v2\_only\_release\_evidence.py`
* \[x] release/knowledge/UAT/operator integration.
* \[x] final docs.

\---

## 28\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 109 PR 1: Streamlit Removal Candidate Safety Contract + Removal Readiness Gate.

Maak docs/dashboard-v2-streamlit-removal-candidate-safety-contract.md.

Maak src/binance\_spot\_bot/dashboard\_v2/removal\_readiness\_gate.py met:
- StreamlitRemovalGateInput
- StreamlitRemovalBlocker
- StreamlitRemovalReadinessDecision
- StreamlitRemovalReadinessReport
- evaluate\_streamlit\_removal\_readiness(root: Path)
- streamlit\_removal\_readiness\_to\_dict(...)
- write\_streamlit\_removal\_readiness\_report(...)

De gate moet best-effort deze artifacts kunnen lezen indien aanwezig:
- Roadmap 108 deprecation gate report
- final parity lock report
- critical workflow lock report
- V2-only smoke report
- V2 browser smoke report
- V2 API smoke report
- V2 UAT sign-off/evidence
- support/evidence V2 verification
- Streamlit-only inventory
- docs V2-first/V2-only check
- rollback/legacy archive manifest
- no-live proof pack
- check-all V2-only result

Gate outcomes:
- remove\_now
- keep\_legacy
- blocked\_cleanup\_required
- unsafe

Hard blockers:
- live mode found
- no-live proof missing
- V2-only smoke failed
- V2 browser smoke failed on critical route
- V2 UAT P0/P1 open
- critical page parity missing
- support/evidence V2 failed
- rollback archive missing
- Streamlit still imported by V2-only path
- docs still Streamlit-first
- check-all V2-only profile failed

Gedrag:
- ontbrekende artifacts worden warnings/blockers volgens belang
- gate verwijdert zelf geen code
- report bevat no\_live\_statement
- alle output bevat live\_trading\_enabled=False
- secret-like values worden geredact

Gebruik alleen stdlib.
Geen command execution.
Geen frontend execution.
Geen backend server starten.
Geen Streamlit wijzigen.
Geen GitHub API calls.
Geen signed endpoints.
Geen account/order endpoints.
Geen live trading.

Voeg tests toe voor:
- remove\_now fixture
- keep\_legacy fixture
- blocked\_cleanup\_required fixture
- unsafe fixture door live mode finding
- missing no-live proof blocks
- missing rollback archive blocks
- JSON serialization
- secret-like values worden geredact
- live\_trading\_enabled=False
- no\_live\_statement aanwezig
```

Waarom eerst:

* Streamlit verwijderen of isoleren mag pas als een harde readiness gate bestaat.
* De gate is read-only en raakt runtime/trading/frontend niet.
* Het is klein genoeg voor Codex.
* No-live, rollback en V2-only bewijs worden meteen verplicht.
* Daarna kunnen dependency isolation, archive, cleanup en optional removal veilig volgen.

\---

## 29\. Definition of Done

Roadmap 109 is klaar als:

* \[x] Streamlit Removal Candidate Safety Contract bestaat.
* \[x] Streamlit Removal Readiness Gate werkt.
* \[x] Streamlit Dependency Isolation werkt.
* \[x] Legacy Streamlit Archive Builder werkt.
* \[x] Streamlit Code Isolation / Move Plan werkt.
* \[x] Streamlit Component Cleanup werkt.
* \[x] CLI V2-Only Default Finalization werkt.
* \[x] V2-Only Check-All Profile werkt.
* \[x] V2-Only Support \& Evidence Bundle werkt.
* \[x] V2-Only Release Simulation werkt.
* \[x] Legacy Docs Freeze \& V2-Only Docs Lock werkt.
* \[x] Legacy Test Cleanup werkt.
* \[x] Legacy Runtime/State Coupling Audit werkt.
* \[x] Removal Patch Plan werkt.
* \[x] Optional Removal Execution Gate werkt.
* \[x] Post-Removal Verification werkt.
* \[x] Rollback Verification Drill werkt.
* \[x] V2-Only Release Evidence Bundle werkt.
* \[x] Release/Migration Integration werkt.
* \[x] Knowledge/Test/Impact Integration werkt.
* \[x] Operator/UAT Integration werkt.
* \[x] CLI commands werken.
* \[x] Tests bewijzen geen live/signed/account/order endpoints.
* \[x] Tests bewijzen removal gate code niet zelf verwijdert.
* \[x] Tests bewijzen removal geblokkeerd wordt zonder archive/no-live/V2 smoke.
* \[x] Tests bewijzen Dashboard V2 zonder Streamlit import kan.
* \[x] Tests bewijzen rollback archive verify werkt.
* \[x] Browser smoke blijft groen.
* \[x] Check-all V2-only blijft groen.
* \[x] Streamlit is removed, isolated of explicitly kept based on gate decision.
* \[x] Dashboard V2 is primary.
* \[x] Live trading blijft disabled.
* \[x] Roadmap 109 kan na uitvoering naar `Voltooid docs`.

\---

## 30\. Verwachte Roadmap 110 daarna

Als Roadmap 109 groen is en Streamlit veilig geÃ¯soleerd/verwijderd is:

```text
Roadmap 110 - Dashboard V2 Advanced Realtime Analytics, Multi-Panel Layouts \& Operator Customization
```

Mogelijke inhoud:

* \[x] aanpasbare Dashboard V2 layouts;
* \[x] multi-panel workspace;
* \[x] opgeslagen operator views;
* \[x] advanced realtime charting;
* \[x] custom alert panels;
* \[x] local-only personalization;
* \[x] still no live trading.

```

Als Roadmap 109 blockers vindt:

```text
Roadmap 110 - Streamlit Removal Blocker Burn-Down, Remaining Legacy Gaps \& V2-Only Stability Fixes
```

Mogelijke inhoud:

* \[x] open removal blockers oplossen;
* \[x] resterende legacy-only flows migreren;
* \[x] V2-only smoke herstellen;
* \[x] support/evidence gaps dichten;
* \[x] docs/UAT V2-only lock afronden;
* \[x] still no live trading.

```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Streamlit removal candidate cleanup and release hardening guard.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.


---

## Uitvoeringsbewijs 2026-05-15

Status: Voltooid na hercontrole en implementatie.

Gebouwd:

- Streamlit removal candidate safety contract en V2-only release docs.
- Removal readiness gate met `remove_now`, `keep_legacy`, `blocked_cleanup_required` en `unsafe` outcomes.
- Dependency isolation detector en `legacy-streamlit` optional dependency group.
- Legacy Streamlit archive builder en archive verifier met hashes.
- Streamlit isolation plan, component cleanup report, V2-only check-all profile, V2 support/evidence smoke en V2-only release simulation.
- Docs V2-only lock, legacy test cleanup report, runtime/state coupling audit, removal patch plan, dry-run removal execution guard, post-removal verify en rollback drill.
- V2-only release evidence bundle met manifest/hashes en no-live proof.
- CLI commands voor alle Roadmap 109 surfaces.
- Check-all integratie voor removal readiness, dependency isolation en V2-only profile.

Validatie:

- `python -m pytest tests/test_roadmap_109_dashboard_v2_removal_candidate_acceptance.py -q`: 4 passed.
- Roadmap 109 CLI-flow voor alle nieuwe commands: ok.
- `python -m pytest tests/test_roadmaps_104_122_full_surface.py tests/test_roadmap_104_dashboard_v2_acceptance.py tests/test_roadmap_105_dashboard_v2_parity_acceptance.py tests/test_roadmap_106_dashboard_v2_cutover_acceptance.py tests/test_roadmap_107_dashboard_v2_workflow_ux_acceptance.py tests/test_roadmap_108_dashboard_v2_streamlit_deprecation_acceptance.py tests/test_roadmap_109_dashboard_v2_removal_candidate_acceptance.py -q`: 35 passed.
- `python -m binance_spot_bot.cli check-all --skip-tests --json`: ok.
- `python -m pytest -q`: 414 passed, 1 bestaande PytestCollectionWarning.

Safety:

- Live trading blijft disabled.
- Geen signed/order/account/live endpoints toegevoegd.
- Removal gate verwijdert zelf geen code.
- Removal execution is dry-run by default en exact-confirm guarded.
- Streamlit blijft legacy/fallback tenzij een latere gate expliciet removal uitvoert.
- Rollback archive en evidence zijn secret-free en bevatten no-live proof.
