# Roadmap 109 - Streamlit Removal Candidate, Legacy Cleanup \& Dashboard V2-Only Release Hardening

Status: Nieuw / Gepland  
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

* \[ ] dependency complexity houden;
* \[ ] dubbele dashboardwaarheid veroorzaken;
* \[ ] extra check-all/import-smoke kosten geven;
* \[ ] oude docs/commands in leven houden;
* \[ ] nieuwe features per ongeluk terug naar Streamlit trekken;
* \[ ] operatorverwarring veroorzaken;
* \[ ] release packaging zwaarder maken;
* \[ ] oude component wrappers laten bestaan;
* \[ ] legacy tests en browser smoke dupliceren;
* \[ ] cleanup moeilijker maken.

Roadmap 109 lost dit op met gecontroleerde cleanup en removal-candidate gates.

\---

## 1\. Hoofddoel Roadmap 109

Maak het project klaar voor een veilige V2-only dashboard release:

```text
Dashboard V2 primary
→ Streamlit legacy inventory
→ final removal gate
→ dependency isolation
→ legacy code archive
→ V2-only release hardening
→ rollback package
→ removal candidate evidence
```

Na Roadmap 109 moet het project kunnen:

* \[ ] Dashboard V2 volledig V2-only draaien zonder Streamlit import.
* \[ ] Streamlit dependency optioneel/legacy houden of veilig verwijderen als gate groen is.
* \[ ] Alle Streamlit-only code inventariseren en classificeren.
* \[ ] Legacy files archiveren of isoleren.
* \[ ] Streamlit imports uit core checks en default CLI halen.
* \[ ] V2-only check-all profile draaien.
* \[ ] V2-only support/evidence bundles maken.
* \[ ] V2-only release simulation draaien.
* \[ ] Rollback naar legacy archive/fallback documenteren.
* \[ ] No-live proof behouden.
* \[ ] Een harde beslissing geven:

  * remove\_now;
  * keep\_legacy;
  * blocked\_cleanup\_required.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen Dashboard V2 foundation opnieuw bouwen.
* \[ ] Geen page parity opnieuw plannen.
* \[ ] Geen UX wizards opnieuw bouwen.
* \[ ] Geen runtime refactor opnieuw bouwen.
* \[ ] Geen model/data/portfolio pipelines opnieuw bouwen.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte account workflows.
* \[ ] Geen cloud dashboard.
* \[ ] Geen remote telemetry.
* \[ ] Geen Streamlit verwijderen zonder removal gate.
* \[ ] Geen fallback archive overschrijven zonder hash/evidence.
* \[ ] Geen docs verwijderen zonder V2 equivalent.

Wel doen:

* \[ ] Streamlit legacy inventariseren;
* \[ ] V2-only imports/checks hard maken;
* \[ ] dependency isoleren;
* \[ ] legacy tests en docs opruimen;
* \[ ] support/evidence/release V2-only maken;
* \[ ] rollback archive maken;
* \[ ] final removal gate bouwen;
* \[ ] no-live proof behouden.

\---

## 3\. Fase 0 - Streamlit Removal Candidate Safety Contract

Nieuw docbestand:

```text
docs/dashboard-v2-streamlit-removal-candidate-safety-contract.md
```

Regels:

* \[ ] Removal candidate is local-only.
* \[ ] Geen live trading.
* \[ ] Geen live mode in V2-only UI, backend, CLI, docs of tests.
* \[ ] Alleen demo, paper en testnet-readiness.
* \[ ] Streamlit removal mag alleen na removal gate pass.
* \[ ] Als gate faalt, blijft Streamlit legacy/fallback.
* \[ ] V2-only mode mag geen Streamlit import nodig hebben.
* \[ ] V2-only release moet support/evidence/no-live proof hebben.
* \[ ] Rollback archive is verplicht vóór removal.
* \[ ] Legacy docs mogen pas weg na V2 docs coverage.
* \[ ] Legacy commands mogen pas weg na V2 CLI coverage.
* \[ ] Reports/evidence zijn secret-free.
* \[ ] Removal decision is auditable en reversible via archive.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen no-live proof verplicht is.
* \[ ] Tests bewijzen removal gate faalt bij missing V2 parity.
* \[ ] Tests bewijzen rollback archive verplicht is.
* \[ ] Tests bewijzen reports secret-free zijn.

\---

## 4\. Fase 1 - Streamlit Removal Readiness Gate

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/removal\_readiness\_gate.py
```

Inputs:

* \[ ] Roadmap 108 deprecation gate report.
* \[ ] final parity lock report.
* \[ ] critical workflow lock report.
* \[ ] V2-only smoke report.
* \[ ] V2 browser smoke matrix.
* \[ ] V2 API smoke.
* \[ ] V2 UAT sign-off.
* \[ ] support/evidence V2-first verification.
* \[ ] Streamlit-only inventory.
* \[ ] docs V2-first check.
* \[ ] rollback archive manifest.
* \[ ] no-live proof pack.
* \[ ] check-all V2-only profile result.

Gate outcomes:

* \[ ] `remove\_now`
* \[ ] `keep\_legacy`
* \[ ] `blocked\_cleanup\_required`
* \[ ] `unsafe`

Hard blockers:

* \[ ] live mode found.
* \[ ] no-live proof missing.
* \[ ] V2-only smoke failed.
* \[ ] V2 browser smoke failed on critical route.
* \[ ] V2 UAT P0/P1 open.
* \[ ] critical page parity missing.
* \[ ] support/evidence V2 failed.
* \[ ] rollback archive missing.
* \[ ] Streamlit still imported by V2-only path.
* \[ ] docs still Streamlit-first.
* \[ ] check-all V2-only profile failed.

Acceptatiecriteria:

* \[ ] Gate is deterministic.
* \[ ] Gate never removes code itself.
* \[ ] Gate explains blockers.
* \[ ] Gate output is Markdown + JSON.
* \[ ] Tests cover remove\_now/keep\_legacy/blocked/unsafe.

\---

## 5\. Fase 2 - Streamlit Dependency Isolation

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/dependency\_isolation.py
```

Doel: Streamlit afhankelijkheid scheiden van core en V2.

Taken:

* \[ ] Detecteer `import streamlit` buiten legacy UI package.
* \[ ] Detecteer `st.` usage buiten legacy UI package.
* \[ ] Detecteer Streamlit dependency in default install path.
* \[ ] Maak dependency group `legacy-streamlit` of behoud `\[ui]` als legacy.
* \[ ] Zorg dat Dashboard V2 dependency group zonder Streamlit kan installeren.
* \[ ] Zorg dat V2-only imports werken zonder Streamlit installed.
* \[ ] Rapporteer packages die Streamlit hard importeren.

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

* \[ ] V2-only import test werkt zonder Streamlit.
* \[ ] Streamlit imports alleen in legacy package.
* \[ ] pyproject heeft duidelijke legacy dependency.
* \[ ] Check-all heeft V2-only profile zonder Streamlit.
* \[ ] Tests gebruiken import monkeypatch/fixture.

\---

## 6\. Fase 3 - Legacy Streamlit Archive Builder

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/legacy\_archive.py
```

Archive bevat:

* \[ ] `ui/streamlit\_app.py`
* \[ ] Streamlit-only components.
* \[ ] Streamlit docs.
* \[ ] Streamlit smoke reports.
* \[ ] Streamlit page/action inventory.
* \[ ] Streamlit fallback instructions.
* \[ ] hash manifest.
* \[ ] rollback instructions.
* \[ ] no-live statement.

Output:

```text
data/dashboard-v2/legacy-archive/<run\_id>/
  streamlit\_legacy\_archive\_manifest.json
  streamlit\_legacy\_archive\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Archive is created before removal candidate.
* \[ ] Archive has hashes.
* \[ ] Archive is secret-free.
* \[ ] Archive can be verified.
* \[ ] Rollback instructions are included.

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

* \[ ] Streamlit app onder legacy path plaatsen.
* \[ ] Compat import houden voor één release:

  * `binance\_spot\_bot.ui.streamlit\_app` → legacy wrapper.
* \[ ] Waarschuwing tonen bij legacy import.
* \[ ] `launch-dashboard --legacy-streamlit` gebruikt legacy path.
* \[ ] V2-only paths importeren legacy niet.
* \[ ] Legacy wrapper kan later verwijderd worden.

Acceptatiecriteria:

* \[ ] Legacy path werkt.
* \[ ] Oude import geeft deprecation warning maar werkt.
* \[ ] V2-only smoke importeert geen legacy path.
* \[ ] Tests cover old/new import path.
* \[ ] No-live banner blijft in legacy UI.

\---

## 8\. Fase 5 - Streamlit Component Cleanup

Inventariseer componenten:

* \[ ] chart wrappers.
* \[ ] metric cards.
* \[ ] badges.
* \[ ] JSON expanders.
* \[ ] tables.
* \[ ] alert lists.
* \[ ] demo pilot charts.
* \[ ] evidence/support widgets.

Acties:

* \[ ] Markeer legacy-only.
* \[ ] Verwijder duplicaten alleen als V2 equivalent bestaat.
* \[ ] Verplaats nuttige pure helpers naar shared non-Streamlit module.
* \[ ] Houd Streamlit wrappers in legacy package.
* \[ ] Voeg tests toe voor pure helper extraction.

Acceptatiecriteria:

* \[ ] Geen Streamlit imports in shared helpers.
* \[ ] Legacy wrappers blijven werken.
* \[ ] V2 gebruikt eigen components/frontend.
* \[ ] Cleanup report bestaat.
* \[ ] Tests pass.

\---

## 9\. Fase 6 - CLI V2-Only Default Finalization

Wijzig CLI default na removal gate:

* \[ ] `dashboard` → Dashboard V2 default.
* \[ ] `dashboard --legacy-streamlit` → legacy fallback.
* \[ ] `launch-dashboard` → waarschuwing of alias naar V2 afhankelijk policy.
* \[ ] `launch-dashboard --legacy-streamlit` beschikbaar.
* \[ ] `dashboard-v2` blijft expliciet.
* \[ ] `dashboard-status` toont default UI.
* \[ ] `dashboard-fallback-info` toont rollback.

Safety:

* \[ ] No-live statement in CLI output.
* \[ ] Geen live flags.
* \[ ] Geen signed/account/order actions.

Acceptatiecriteria:

* \[ ] CLI default is V2 when gate pass.
* \[ ] Legacy command still works if legacy kept.
* \[ ] Old commands produce helpful migration message.
* \[ ] Tests cover CLI routing.
* \[ ] Docs updated.

\---

## 10\. Fase 7 - V2-Only Check-All Profile

Nieuwe profiles:

```text
check-all --profile v2-only
check-all --profile v2-release
check-all --profile legacy-fallback
```

V2-only checks:

* \[ ] V2 imports without Streamlit.
* \[ ] V2 API smoke.
* \[ ] V2 browser smoke.
* \[ ] V2 no-live proof.
* \[ ] V2 critical workflow lock.
* \[ ] V2 support/evidence export.
* \[ ] V2 UAT evidence.
* \[ ] Streamlit dependency absent from V2 import graph.

Legacy fallback checks:

* \[ ] Legacy Streamlit import if installed.
* \[ ] Legacy no-live banner.
* \[ ] Legacy fallback command.
* \[ ] Legacy archive exists.

Acceptatiecriteria:

* \[ ] V2-only profile works without Streamlit.
* \[ ] Legacy profile is optional.
* \[ ] No-live failure hard fails.
* \[ ] Reports are secret-free.
* \[ ] Check-all fast remains reasonable.

\---

## 11\. Fase 8 - V2-Only Support \& Evidence Bundle

Support/evidence must not rely on Streamlit.

Update:

* \[ ] support bundle can be created from V2 UI.
* \[ ] support bundle can be created from CLI.
* \[ ] evidence manifest can be created from V2 UI.
* \[ ] operator quality gate visible in V2.
* \[ ] local ops snapshot visible in V2.
* \[ ] redaction self-test visible in V2.
* \[ ] no-live proof visible in V2.

Acceptatiecriteria:

* \[ ] V2 support/evidence workflow passes.
* \[ ] Streamlit not required.
* \[ ] Artifacts secret-free.
* \[ ] Reports linked in V2.
* \[ ] Tests use temp dirs.

\---

## 12\. Fase 9 - V2-Only Release Simulation

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/v2\_release\_simulation.py
```

Simulation checks:

* \[ ] clean env without Streamlit.
* \[ ] install core + dashboard-v2 extras.
* \[ ] import package.
* \[ ] launch V2 app fake/server smoke.
* \[ ] API smoke.
* \[ ] browser smoke if configured.
* \[ ] support/evidence smoke.
* \[ ] check-all v2-only.
* \[ ] no-live proof.
* \[ ] static assets present.
* \[ ] release version manifest.
* \[ ] rollback archive present.

Acceptatiecriteria:

* \[ ] Simulation output JSON + Markdown.
* \[ ] Missing Streamlit does not fail V2.
* \[ ] Missing V2 dependency gives useful error.
* \[ ] No-live proof included.
* \[ ] Tests use fake environment.

\---

## 13\. Fase 10 - Legacy Docs Freeze \& V2-Only Docs Lock

Docs changes:

* \[ ] README dashboard section V2-only primary.
* \[ ] Streamlit marked legacy fallback only.
* \[ ] Legacy docs archived.
* \[ ] Operator manual V2-only primary.
* \[ ] CLI cookbook V2 commands primary.
* \[ ] Troubleshooting V2-first.
* \[ ] Release docs V2-only.
* \[ ] Legacy fallback docs retained.
* \[ ] Removal candidate docs explain gates.

Docs checks:

* \[ ] No Streamlit-first instructions except legacy fallback.
* \[ ] No live approval wording.
* \[ ] All V2 commands exist.
* \[ ] All legacy references have fallback context.
* \[ ] Broken links fail.

Acceptatiecriteria:

* \[ ] Docs V2-only lock passes.
* \[ ] Legacy docs archive exists.
* \[ ] Docs consistency tests pass.
* \[ ] Operator can still find fallback info.
* \[ ] No-live statement present.

\---

## 14\. Fase 11 - Legacy Test Cleanup

Tasks:

* \[ ] Mark Streamlit tests as legacy.
* \[ ] Move Streamlit tests under `tests/legacy\_streamlit/`.
* \[ ] Keep minimal fallback smoke.
* \[ ] Remove duplicated full legacy browser matrix.
* \[ ] Ensure V2 tests cover primary workflows.
* \[ ] Test selector maps dashboard changes to V2 by default.
* \[ ] Streamlit changes trigger legacy freeze test.

Acceptatiecriteria:

* \[ ] V2 tests are primary.
* \[ ] Legacy tests only cover fallback.
* \[ ] Test selection updated.
* \[ ] Check-all profiles updated.
* \[ ] No-live tests still cover both when legacy installed.

\---

## 15\. Fase 12 - Legacy Runtime/State Coupling Audit

Doel: zorgen dat runtime niet afhankelijk blijft van Streamlit session state.

Checks:

* \[ ] `st.session\_state` usage only in legacy UI.
* \[ ] runtime bridge owns V2 state.
* \[ ] settings/profile persistence not Streamlit-only.
* \[ ] dashboard actions go through V2 action policy.
* \[ ] runtime snapshot DTOs independent.
* \[ ] no shared mutable conflict between legacy and V2.

Acceptatiecriteria:

* \[ ] No Streamlit state usage outside legacy.
* \[ ] V2 can run with fresh process.
* \[ ] V2 can restart after crash.
* \[ ] Legacy/V2 not run against same runtime by default unless safe.
* \[ ] Audit report exists.

\---

## 16\. Fase 13 - Removal Patch Plan

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/removal\_patch\_plan.py
```

Generates exact plan:

* \[ ] files to move;
* \[ ] files to delete later;
* \[ ] imports to update;
* \[ ] docs to update;
* \[ ] tests to move;
* \[ ] dependencies to change;
* \[ ] CLI aliases to keep;
* \[ ] rollback archive path;
* \[ ] validation commands;
* \[ ] no-live proof command.

Patch decision:

* \[ ] `plan\_only`
* \[ ] `isolate\_legacy`
* \[ ] `remove\_after\_gate`
* \[ ] `blocked`

Acceptatiecriteria:

* \[ ] Plan is generated before deletion.
* \[ ] Plan includes rollback.
* \[ ] Plan has validation commands.
* \[ ] Plan is Markdown + JSON.
* \[ ] Tests cover blocked plan.

\---

## 17\. Fase 14 - Optional Removal Execution Gate

Deze fase voert nog steeds geen automatische deletion uit zonder expliciete confirm.

Command:

```powershell
python -m binance\_spot\_bot.cli dashboard-v2-streamlit-removal-execute --confirm REMOVE\_STREAMLIT\_LEGACY\_AFTER\_GATE
```

Guardrails:

* \[ ] removal readiness gate must be `remove\_now`.
* \[ ] rollback archive verified.
* \[ ] V2-only release simulation pass.
* \[ ] check-all v2-only pass.
* \[ ] no-live proof pass.
* \[ ] operator confirmation required.
* \[ ] dry-run default.
* \[ ] patch plan printed first.
* \[ ] legacy fallback archived.

Acceptatiecriteria:

* \[ ] Dry-run default.
* \[ ] Execute blocked without exact confirm.
* \[ ] Execute blocked if gate not remove\_now.
* \[ ] Execute blocked if archive missing.
* \[ ] Tests use temp fixture repo.

\---

## 18\. Fase 15 - Post-Removal Verification

If removal executed or legacy isolated:

Checks:

* \[ ] package imports without Streamlit.
* \[ ] Dashboard V2 launches.
* \[ ] API smoke passes.
* \[ ] browser smoke passes.
* \[ ] check-all v2-only passes.
* \[ ] support/evidence passes.
* \[ ] docs V2-only pass.
* \[ ] no-live proof pass.
* \[ ] legacy archive verify pass.
* \[ ] rollback instructions still exist.

Acceptatiecriteria:

* \[ ] Verification report exists.
* \[ ] Failures produce rollback instructions.
* \[ ] No-live failure hard fails.
* \[ ] Reports secret-free.
* \[ ] Release simulation reads verification.

\---

## 19\. Fase 16 - Rollback Verification Drill

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/removal\_rollback\_drill.py
```

Drill:

* \[ ] load legacy archive.
* \[ ] verify hashes.
* \[ ] simulate restore to temp dir.
* \[ ] import legacy Streamlit path if dependencies installed.
* \[ ] verify no-live banner text.
* \[ ] verify fallback command docs.
* \[ ] export drill report.

Acceptatiecriteria:

* \[ ] Drill works offline.
* \[ ] Drill does not mutate working tree by default.
* \[ ] Hash mismatch fails.
* \[ ] Report is secret-free.
* \[ ] Tests use fixture archive.

\---

## 20\. Fase 17 - V2-Only Release Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/v2\_only\_release\_evidence.py
```

Bundle bevat:

* \[ ] safety contract.
* \[ ] removal readiness gate.
* \[ ] dependency isolation report.
* \[ ] legacy archive manifest.
* \[ ] code isolation report.
* \[ ] component cleanup report.
* \[ ] CLI V2-only default report.
* \[ ] check-all V2-only report.
* \[ ] support/evidence V2 report.
* \[ ] release simulation report.
* \[ ] docs lock report.
* \[ ] legacy test cleanup report.
* \[ ] runtime/state coupling audit.
* \[ ] removal patch plan.
* \[ ] optional removal execution result.
* \[ ] post-removal verification.
* \[ ] rollback drill.
* \[ ] no-live proof.
* \[ ] hashes.

Output:

```text
data/dashboard-v2/v2-only-release/evidence/<run\_id>/
  dashboard\_v2\_only\_release\_evidence\_manifest.json
  dashboard\_v2\_only\_release\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle clearly states removal decision.
* \[ ] Bundle included in release evidence.

\---

## 21\. Fase 18 - Release/Migration Integration

Roadmap 089:

* \[ ] Release manifest includes `dashboard\_ui=dashboard-v2`.
* \[ ] Release notes include Streamlit removal/legacy status.
* \[ ] Migration notes explain V2-only install.
* \[ ] Legacy archive path included.
* \[ ] Rollback instructions included.
* \[ ] Release quality gate reads V2-only evidence.
* \[ ] Versioned upgrade path handles legacy configs.

Acceptatiecriteria:

* \[ ] Release simulation V2-only pass.
* \[ ] Migration notes generated.
* \[ ] Rollback instructions generated.
* \[ ] Release evidence secret-free.
* \[ ] No-live proof included.

\---

## 22\. Fase 19 - Knowledge/Test/Impact Integration

Roadmap 091:

* \[ ] Knowledge graph marks Streamlit removed/legacy.
* \[ ] Dashboard V2 routes become primary UI graph.
* \[ ] Legacy archive indexed as archive, not active module.
* \[ ] Impact analysis flags any new Streamlit import.

Roadmap 092:

* \[ ] Test selector chooses V2 tests by default.
* \[ ] Streamlit import changes trigger legacy/removal tests.
* \[ ] pyproject dependency changes trigger dependency isolation tests.
* \[ ] docs changes trigger V2-only docs tests.

Acceptatiecriteria:

* \[ ] Impact analysis detects reintroduced Streamlit import.
* \[ ] Test selection is V2-first.
* \[ ] Knowledge graph updated.
* \[ ] Reports secret-free.
* \[ ] No-live proof preserved.

\---

## 23\. Fase 20 - Operator/UAT Integration

Roadmap 102:

* \[ ] Operator manual V2-only primary.
* \[ ] Support playbooks mention no Streamlit dependency by default.
* \[ ] CLI cookbook uses V2 commands.
* \[ ] Fallback/rollback guide linked.

Roadmap 103:

* \[ ] UAT scenarios run V2-only.
* \[ ] UAT fallback scenario uses archive/legacy if present.
* \[ ] UAT sign-off requires V2-only pass.
* \[ ] UAT scorecard includes removal decision.

Acceptatiecriteria:

* \[ ] V2-only UAT pass.
* \[ ] Operator docs pass.
* \[ ] Fallback instructions clear.
* \[ ] UAT P0/P1 block removal.
* \[ ] No-live proof preserved.

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

* \[ ] Commands werken offline.
* \[ ] Commands ondersteunen JSON waar relevant.
* \[ ] Dangerous command is dry-run by default.
* \[ ] Exact confirm required for execution.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Reports zijn secret-free.

\---

## 25\. Fase 22 - Tests

### Unit tests

* \[ ] `tests/test\_dashboard\_v2\_streamlit\_removal\_candidate\_safety\_contract.py`
* \[ ] `tests/test\_dashboard\_v2\_removal\_readiness\_gate.py`
* \[ ] `tests/test\_dashboard\_v2\_dependency\_isolation.py`
* \[ ] `tests/test\_dashboard\_v2\_legacy\_archive.py`
* \[ ] `tests/test\_dashboard\_v2\_streamlit\_code\_isolation.py`
* \[ ] `tests/test\_dashboard\_v2\_component\_cleanup.py`
* \[ ] `tests/test\_dashboard\_v2\_cli\_v2\_only\_default.py`
* \[ ] `tests/test\_dashboard\_v2\_check\_all\_profiles.py`
* \[ ] `tests/test\_dashboard\_v2\_v2\_release\_simulation.py`
* \[ ] `tests/test\_dashboard\_v2\_docs\_v2\_only\_lock.py`
* \[ ] `tests/test\_dashboard\_v2\_legacy\_test\_cleanup.py`
* \[ ] `tests/test\_dashboard\_v2\_runtime\_state\_coupling\_audit.py`
* \[ ] `tests/test\_dashboard\_v2\_removal\_patch\_plan.py`
* \[ ] `tests/test\_dashboard\_v2\_removal\_execution\_gate.py`
* \[ ] `tests/test\_dashboard\_v2\_post\_removal\_verification.py`
* \[ ] `tests/test\_dashboard\_v2\_removal\_rollback\_drill.py`
* \[ ] `tests/test\_dashboard\_v2\_only\_release\_evidence.py`

### Integration tests

* \[ ] V2-only import fixture without Streamlit.
* \[ ] Legacy archive create/verify fixture.
* \[ ] Dependency isolation fixture.
* \[ ] Removal readiness pass/fail fixture.
* \[ ] V2-only release simulation fixture.
* \[ ] Removal patch plan dry-run fixture.
* \[ ] Optional removal execution temp-repo fixture.
* \[ ] Post-removal verification fixture.
* \[ ] Rollback drill fixture.
* \[ ] Evidence bundle export/verify fixture.

### Browser smoke

* \[ ] Dashboard V2 loads.
* \[ ] No-live banner visible.
* \[ ] Start wizard visible.
* \[ ] Demo spot guided flow visible.
* \[ ] Paper session workflow visible.
* \[ ] Evidence/support visible.
* \[ ] V2-only mode visible.
* \[ ] No Streamlit fallback required for primary workflows.

### Safety tests

* \[ ] Live mode absent.
* \[ ] Signed/order/account endpoints absent.
* \[ ] No-live proof mandatory.
* \[ ] Removal blocked without archive.
* \[ ] Removal blocked if V2 smoke fails.
* \[ ] Removal blocked if Streamlit imported by V2-only path.
* \[ ] Removal command exact confirm required.
* \[ ] Evidence secret-free.
* \[ ] Rollback archive hash verified.
* \[ ] Check-all safe env preserved.

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

* \[ ] Dashboard V2 primary.
* \[ ] Streamlit legacy/removal status.
* \[ ] V2-only install instructions.
* \[ ] V2-only check commands.
* \[ ] Legacy archive/rollback instructions.
* \[ ] No-live statement.

Operator docs updates:

* \[ ] V2-only daily workflow.
* \[ ] Fallback/rollback guide.
* \[ ] Support/evidence V2-only guide.
* \[ ] Removal candidate explanation.

\---

## 27\. Codex bouwvolgorde

### PR 1 - Safety Contract + Removal Readiness Gate

* \[ ] `docs/dashboard-v2-streamlit-removal-candidate-safety-contract.md`
* \[ ] `dashboard\_v2/removal\_readiness\_gate.py`
* \[ ] gate tests.
* \[ ] no-live tests.

### PR 2 - Dependency Isolation

* \[ ] `dashboard\_v2/dependency\_isolation.py`
* \[ ] pyproject optional dependency split.
* \[ ] import isolation tests.

### PR 3 - Legacy Archive Builder

* \[ ] `dashboard\_v2/legacy\_archive.py`
* \[ ] archive create/verify.
* \[ ] hash tests.

### PR 4 - Streamlit Code Isolation Plan

* \[ ] legacy package/path plan.
* \[ ] compat wrapper.
* \[ ] old/new import tests.

### PR 5 - Component Cleanup + Runtime State Coupling Audit

* \[ ] `dashboard\_v2/component\_cleanup.py`
* \[ ] `dashboard\_v2/runtime\_state\_coupling\_audit.py`
* \[ ] shared helper extraction tests.

### PR 6 - CLI V2-Only Default + Check-All Profiles

* \[ ] CLI routing changes.
* \[ ] v2-only check-all profile.
* \[ ] tests.

### PR 7 - V2-Only Support/Evidence + Release Simulation

* \[ ] support/evidence V2-only smoke.
* \[ ] `v2\_release\_simulation.py`
* \[ ] release simulation tests.

### PR 8 - Docs Lock + Legacy Test Cleanup

* \[ ] docs V2-only lock.
* \[ ] legacy test cleanup.
* \[ ] docs/test selector tests.

### PR 9 - Removal Patch Plan + Optional Execution Gate

* \[ ] `removal\_patch\_plan.py`
* \[ ] dry-run/confirm gate.
* \[ ] temp-repo tests.

### PR 10 - Post-Removal Verify + Rollback + Evidence + Integrations

* \[ ] `post\_removal\_verification.py`
* \[ ] `removal\_rollback\_drill.py`
* \[ ] `v2\_only\_release\_evidence.py`
* \[ ] release/knowledge/UAT/operator integration.
* \[ ] final docs.

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

* \[ ] Streamlit Removal Candidate Safety Contract bestaat.
* \[ ] Streamlit Removal Readiness Gate werkt.
* \[ ] Streamlit Dependency Isolation werkt.
* \[ ] Legacy Streamlit Archive Builder werkt.
* \[ ] Streamlit Code Isolation / Move Plan werkt.
* \[ ] Streamlit Component Cleanup werkt.
* \[ ] CLI V2-Only Default Finalization werkt.
* \[ ] V2-Only Check-All Profile werkt.
* \[ ] V2-Only Support \& Evidence Bundle werkt.
* \[ ] V2-Only Release Simulation werkt.
* \[ ] Legacy Docs Freeze \& V2-Only Docs Lock werkt.
* \[ ] Legacy Test Cleanup werkt.
* \[ ] Legacy Runtime/State Coupling Audit werkt.
* \[ ] Removal Patch Plan werkt.
* \[ ] Optional Removal Execution Gate werkt.
* \[ ] Post-Removal Verification werkt.
* \[ ] Rollback Verification Drill werkt.
* \[ ] V2-Only Release Evidence Bundle werkt.
* \[ ] Release/Migration Integration werkt.
* \[ ] Knowledge/Test/Impact Integration werkt.
* \[ ] Operator/UAT Integration werkt.
* \[ ] CLI commands werken.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen removal gate code niet zelf verwijdert.
* \[ ] Tests bewijzen removal geblokkeerd wordt zonder archive/no-live/V2 smoke.
* \[ ] Tests bewijzen Dashboard V2 zonder Streamlit import kan.
* \[ ] Tests bewijzen rollback archive verify werkt.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all V2-only blijft groen.
* \[ ] Streamlit is removed, isolated of explicitly kept based on gate decision.
* \[ ] Dashboard V2 is primary.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 109 kan na uitvoering naar `Voltooid docs`.

\---

## 30\. Verwachte Roadmap 110 daarna

Als Roadmap 109 groen is en Streamlit veilig geïsoleerd/verwijderd is:

```text
Roadmap 110 - Dashboard V2 Advanced Realtime Analytics, Multi-Panel Layouts \& Operator Customization
```

Mogelijke inhoud:

* \[ ] aanpasbare Dashboard V2 layouts;
* \[ ] multi-panel workspace;
* \[ ] opgeslagen operator views;
* \[ ] advanced realtime charting;
* \[ ] custom alert panels;
* \[ ] local-only personalization;
* \[ ] still no live trading.

```

Als Roadmap 109 blockers vindt:

```text
Roadmap 110 - Streamlit Removal Blocker Burn-Down, Remaining Legacy Gaps \& V2-Only Stability Fixes
```

Mogelijke inhoud:

* \[ ] open removal blockers oplossen;
* \[ ] resterende legacy-only flows migreren;
* \[ ] V2-only smoke herstellen;
* \[ ] support/evidence gaps dichten;
* \[ ] docs/UAT V2-only lock afronden;
* \[ ] still no live trading.

```

