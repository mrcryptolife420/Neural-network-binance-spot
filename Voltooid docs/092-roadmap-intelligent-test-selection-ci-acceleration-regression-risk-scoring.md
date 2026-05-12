# Roadmap 092 - Intelligent Test Selection, CI Acceleration \& Regression Risk Scoring

Status: Voltooid na hercontrole en volledige validatie  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/092-roadmap-intelligent-test-selection-ci-acceleration-regression-risk-scoring.md
```

Volgt op:

* `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
* `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
* `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
* `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
* `Voltooid docs/005` t/m `Voltooid docs/075`
* `Roadmap docs/076-roadmap-binance-public-data-ingestion-indicator-warmup-feature-expansion.md`
* `Roadmap docs/077-roadmap-data-driven-strategy-confidence-backtest-dataset-builder-indicator-calibration.md`
* `Roadmap docs/078-roadmap-paper-strategy-deployment-continuous-evaluation-auto-rollback.md`
* `Roadmap docs/079-roadmap-paper-portfolio-operations-capital-allocation-strategy-rotation.md`
* `Roadmap docs/080-roadmap-paper-portfolio-benchmarking-stress-testing-scenario-replay.md`
* `Roadmap docs/081-roadmap-paper-portfolio-optimization-risk-budget-search-robust-allocation-selection.md`
* `Roadmap docs/082-roadmap-paper-policy-rollout-ab-paper-experiments-champion-challenger-governance.md`
* `Roadmap docs/083-roadmap-local-paper-operations-automation-scheduled-reports-operator-runbooks.md`
* `Roadmap docs/084-roadmap-local-paper-ops-observability-metrics-warehouse-long-term-analytics.md`
* `Roadmap docs/085-roadmap-local-ai-ops-assistant-natural-language-queries-safe-operator-guidance.md`
* `Roadmap docs/086-roadmap-safe-human-in-the-loop-action-center-approval-workflows-operator-decision-journal.md`
* `Roadmap docs/087-roadmap-local-permission-profiles-operator-roles-hardening-audit-grade-compliance-reports.md`
* `Roadmap docs/088-roadmap-offline-disaster-recovery-backup-restore-drills-local-state-integrity.md`
* `Roadmap docs/089-roadmap-local-release-management-versioned-upgrade-paths-migration-safety.md`
* `Roadmap docs/090-roadmap-developer-experience-codex-task-packs-roadmap-execution-automation.md`
* `Roadmap docs/091-roadmap-repository-knowledge-graph-code-ownership-impact-analysis.md`

Doel: Roadmap 091 maakt een Repository Knowledge Graph, ownership maps en impactanalyse mogelijk. Roadmap 092 gebruikt die kennislaag om **intelligent te bepalen welke tests, checks, smoke tests, safety scans en docs-validaties nodig zijn per wijziging**. Daardoor hoeft Codex niet altijd alles blind te draaien, maar blijft veiligheid wel behouden via regression risk scoring, fast/standard/deep test profiles, flaky-test tracking, check-all v2 en evidence-backed test reports.

Live trading blijft volledig buiten scope.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 092`, `092-roadmap`, `Intelligent Test Selection`, `CI Acceleration`, `Regression Risk Scoring` en `flaky test`.
* \[x] Geen bestaande Roadmap 092 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 091 is lokaal aangemaakt als Repository Knowledge Graph, Code Ownership Maps \& Impact Analysis.

### Codebasecontrole

Gecontroleerde relevante modules/bestanden:

* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `pyproject.toml`
* \[x] bestaande roadmaplijn tot en met Roadmap 091.

Bestaande basis:

* \[x] `check\_all.py` heeft al `CheckResult`, `run\_command(...)`, `run\_checks(...)`, `payload\_for(...)` en `print\_payload(...)`.
* \[x] `check\_all.py` zet bij alle commands `PYTHONPATH=src`, `LIVE\_TRADING\_ENABLED=false` en `KILL\_SWITCH=true`.
* \[x] `check\_all.py` draait nu onder andere:

  * unit tests via `unittest discover`;
  * config validation;
  * preflight;
  * security scan;
  * dashboard import;
  * diagnostics CLI;
  * support bundle CLI;
  * operator quality gate CLI;
  * local ops snapshot CLI;
  * pilot imports/smokes;
  * CLI smoke;
  * no-live UI check;
  * no-secret artifacts;
  * ruff indien geïnstalleerd.
* \[x] `pyproject.toml` gebruikt Python `>=3.12`, heeft dev dependencies `pytest` en `ruff`, en project entrypoint `spot-bot = "binance\_spot\_bot.cli:main"`.

### Belangrijkste gat na Roadmap 091

Na Roadmap 091 weet de repo welke modules, tests, docs, commands en safety surfaces geraakt worden. Wat dan nog mist:

* \[ ] automatische testselectie op basis van changed files;
* \[ ] fast/standard/deep testprofielen;
* \[ ] regressierisico-score per wijziging;
* \[ ] test runtime history;
* \[ ] flaky-test detectie;
* \[ ] check-all v2 met selectieve profielen;
* \[ ] bewijs waarom een test wel/niet gekozen werd;
* \[ ] Codex-task-pack integratie met aanbevolen tests;
* \[ ] dashboard/CLI voor testadvies;
* \[ ] safety hard blockers die altijd deep checks afdwingen.

Roadmap 092 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 092

Maak een intelligente lokale testlaag:

```text
Changed files
→ knowledge graph impact
→ safety surface detection
→ regression risk score
→ selected test profile
→ selected commands
→ execution plan
→ test run evidence
→ recommendation for Codex/PR/release
```

Na Roadmap 092 moet de bot kunnen:

* \[ ] changed files detecteren;
* \[ ] impacted modules/tests bepalen;
* \[ ] risk level berekenen;
* \[ ] snel testprofiel voorstellen;
* \[ ] standaard testprofiel voorstellen;
* \[ ] deep testprofiel afdwingen bij safety-critical wijzigingen;
* \[ ] flaky tests herkennen;
* \[ ] testduur/history opslaan;
* \[ ] check-all sneller en slimmer maken;
* \[ ] test evidence bundelen;
* \[ ] PR/Codex task packs automatisch aanvullen met exacte testcommands;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe knowledge graph; Roadmap 091 doet dat.
* \[ ] Geen release manager opnieuw bouwen; Roadmap 089 doet dat.
* \[ ] Geen roadmap execution opnieuw bouwen; Roadmap 090 doet dat.
* \[ ] Geen externe CI-service verplicht maken.
* \[ ] Geen cloud telemetry.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen Binance account endpoints.
* \[ ] Geen order endpoints.
* \[ ] Geen tests uitvoeren met live env vars.
* \[ ] Geen flaky tests stil negeren zonder rapport.
* \[ ] Geen safety-critical wijziging met alleen fast profile goedkeuren.

Wel doen:

* \[ ] bestaande check-all uitbreiden naar profielen;
* \[ ] Roadmap 091 impact graph gebruiken;
* \[ ] test history lokaal opslaan;
* \[ ] risk scoring toevoegen;
* \[ ] slimme testselectie toevoegen;
* \[ ] command execution veilig houden;
* \[ ] evidence en reports toevoegen;
* \[ ] dashboard/CLI toevoegen;
* \[ ] Codex/roadmap/release integratie toevoegen.

\---

## 3\. Fase 0 - Test Selection Safety Contract

Nieuwe doc:

```text
docs/intelligent-test-selection-safety-contract.md
```

Regels:

* \[ ] Testselectie is local-only.
* \[ ] Geen remote telemetry.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen order endpoints.
* \[ ] Testcommands draaien altijd met `LIVE\_TRADING\_ENABLED=false`.
* \[ ] Testcommands draaien altijd met `KILL\_SWITCH=true`.
* \[ ] Safety-critical changes mogen fast profile niet alleen gebruiken.
* \[ ] Security/redaction changes vereisen security scan en redaction self-test.
* \[ ] Dashboard changes vereisen dashboard import/smoke en eventueel browser smoke.
* \[ ] Migration/restore/release apply changes vereisen dry-run en deep profile.
* \[ ] Reports zijn secret-free.
* \[ ] Test selection moet explainable zijn.
* \[ ] Skipped tests moeten reden hebben.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen live/signed/order/account commands geweigerd worden.
* \[ ] Fast profile blokkeert safety-critical changes.
* \[ ] Output bevat `live\_trading\_enabled=False`.
* \[ ] Dashboard toont `LOCAL TEST SELECTION ONLY`.

\---

## 4\. Fase 1 - Test Inventory Engine

Nieuwe module:

```text
src/binance\_spot\_bot/test\_inventory.py
```

Dataclasses:

* \[ ] `TestFile`
* \[ ] `TestCaseInfo`
* \[ ] `TestCommand`
* \[ ] `TestInventory`
* \[ ] `TestInventoryManifest`

Te detecteren:

* \[ ] test files onder `tests/`;
* \[ ] unittest classes;
* \[ ] pytest-style test functions;
* \[ ] imported modules;
* \[ ] fixture usage indien statisch detecteerbaar;
* \[ ] slow/heavy markers indien aanwezig;
* \[ ] dashboard/browser tests;
* \[ ] security/redaction tests;
* \[ ] migration/restore tests;
* \[ ] roadmap/CLI tests.

Per testfile:

* \[ ] path;
* \[ ] sha256;
* \[ ] line\_count;
* \[ ] test\_count;
* \[ ] imported source modules;
* \[ ] likely domain;
* \[ ] safety\_relevance;
* \[ ] estimated\_profile:

  * fast;
  * standard;
  * deep.
* \[ ] recommended command.

Acceptatiecriteria:

* \[ ] Inventory werkt offline.
* \[ ] Inventory detecteert unittest en pytest stijl.
* \[ ] Inventory bevat geen secrets.
* \[ ] Inventory schrijft manifest/hashes.
* \[ ] Tests gebruiken fixture testrepo.

\---

## 5\. Fase 2 - Test Runtime History Store

Nieuwe module:

```text
src/binance\_spot\_bot/test\_runtime\_history.py
```

Storage:

```text
data/test-runs/
  history.jsonl
  latest.json
  summaries/
```

Dataclasses:

* \[ ] `TestRunRecord`
* \[ ] `TestCommandRuntime`
* \[ ] `TestRuntimeSummary`
* \[ ] `TestHistoryStore`

Velden:

* \[ ] run\_id;
* \[ ] timestamp\_ms;
* \[ ] profile;
* \[ ] command;
* \[ ] status;
* \[ ] returncode;
* \[ ] duration\_ms;
* \[ ] stdout\_tail redacted;
* \[ ] stderr\_tail redacted;
* \[ ] selected\_by\_reason;
* \[ ] changed\_files;
* \[ ] risk\_score;
* \[ ] flaky\_candidate;
* \[ ] live\_trading\_enabled=false.

Acceptatiecriteria:

* \[ ] Test runtime history is append-only.
* \[ ] Output is redacted.
* \[ ] History kan gemiddelde duur per command berekenen.
* \[ ] History kan laatste status tonen.
* \[ ] No secrets in history.

\---

## 6\. Fase 3 - Changed Files Detector

Nieuwe module:

```text
src/binance\_spot\_bot/changed\_files.py
```

Bronnen:

* \[ ] explicit `--changed` CLI args;
* \[ ] git diff indien beschikbaar;
* \[ ] git staged diff indien beschikbaar;
* \[ ] compare with last inventory hash;
* \[ ] manual file list;
* \[ ] Roadmap 090 task pack allowed files.

Dataclasses:

* \[ ] `ChangedFile`
* \[ ] `ChangedFileSet`
* \[ ] `ChangeDetectionResult`

Per changed file:

* \[ ] path;
* \[ ] status:

  * added;
  * modified;
  * deleted;
  * renamed;
  * unknown.
* \[ ] category;
* \[ ] owner domain from Roadmap 091;
* \[ ] safety surface;
* \[ ] hash\_before indien beschikbaar;
* \[ ] hash\_after indien beschikbaar.

Acceptatiecriteria:

* \[ ] Werkt zonder git.
* \[ ] Werkt met explicit changed args.
* \[ ] Git unavailable geeft warning, geen crash.
* \[ ] Output is secret-free.
* \[ ] Tests gebruiken fixture repo.

\---

## 7\. Fase 4 - Regression Risk Scoring

Nieuwe module:

```text
src/binance\_spot\_bot/regression\_risk.py
```

Dataclasses:

* \[ ] `RegressionRiskScore`
* \[ ] `RiskFactor`
* \[ ] `RiskPolicy`
* \[ ] `RiskScoreResult`

Risicofactoren:

* \[ ] safety surface touched;
* \[ ] runtime/execution/risk touched;
* \[ ] security/redaction touched;
* \[ ] dashboard action controls touched;
* \[ ] CLI command parser touched;
* \[ ] support bundle/evidence touched;
* \[ ] migration/restore/release apply touched;
* \[ ] tests changed but source not changed;
* \[ ] source changed but no direct tests;
* \[ ] high fan-in module touched;
* \[ ] high fan-out module touched;
* \[ ] changed module historically flaky;
* \[ ] large diff;
* \[ ] multiple domains touched;
* \[ ] docs-only change;
* \[ ] roadmap-only change.

Risk levels:

* \[ ] low;
* \[ ] medium;
* \[ ] high;
* \[ ] critical.

Hard critical:

* \[ ] live/signed/order/account gates touched;
* \[ ] redaction/security scanner touched;
* \[ ] action executor touched;
* \[ ] restore/migration apply touched;
* \[ ] risk engine/execution engine touched;
* \[ ] dashboard order/action button touched.

Acceptatiecriteria:

* \[ ] Risk score is deterministic.
* \[ ] Risk score explains all factors.
* \[ ] Critical changes force deep profile.
* \[ ] Low docs-only changes can use fast docs profile.
* \[ ] Tests cover all risk levels.

\---

## 8\. Fase 5 - Test Profile Definitions

Nieuwe module:

```text
src/binance\_spot\_bot/test\_profiles.py
```

Profiles:

### `fast`

Voor kleine veilige wijzigingen.

* \[ ] targeted unit tests;
* \[ ] changed module import;
* \[ ] relevant CLI smoke;
* \[ ] docs validation indien docs changed;
* \[ ] no-live quick check.

### `standard`

Voor normale feature/bugfix PR.

* \[ ] targeted unit tests;
* \[ ] related integration tests;
* \[ ] config validation;
* \[ ] preflight;
* \[ ] security scan;
* \[ ] dashboard import if UI touched;
* \[ ] operator quality gate if operator/evidence touched;
* \[ ] ruff if available.

### `deep`

Voor safety-critical of brede wijzigingen.

* \[ ] full unittest discover;
* \[ ] check-all;
* \[ ] security scan;
* \[ ] redaction self-test;
* \[ ] dashboard smoke;
* \[ ] browser smoke if dashboard touched;
* \[ ] support bundle create/verify;
* \[ ] local ops snapshot;
* \[ ] release/migration dry-run where relevant;
* \[ ] no-live proof.

### `dashboard`

Voor UI changes.

* \[ ] dashboard import;
* \[ ] dashboard-smoke;
* \[ ] dashboard-browser-smoke;
* \[ ] chart key/duplicate element checks;
* \[ ] UI no-live check.

### `security`

Voor security/redaction changes.

* \[ ] security scan;
* \[ ] redaction self-test;
* \[ ] support bundle secret-free verify;
* \[ ] no-secret artifacts;
* \[ ] tests for redaction/security.

### `release\_migration`

Voor release/migration/restore changes.

* \[ ] migration dry-run tests;
* \[ ] backup/restore preview tests;
* \[ ] release quality gate;
* \[ ] check-all;
* \[ ] no-live proof.

Acceptatiecriteria:

* \[ ] Profiles are JSON-serializable.
* \[ ] Profiles contain commands and reasons.
* \[ ] Profiles cannot include live/signed/order/account commands.
* \[ ] Critical changes cannot select only fast.
* \[ ] Tests validate profile rules.

\---

## 9\. Fase 6 - Intelligent Test Selector

Nieuwe module:

```text
src/binance\_spot\_bot/intelligent\_test\_selector.py
```

Inputs:

* \[ ] changed files;
* \[ ] test inventory;
* \[ ] Roadmap 091 impact analysis;
* \[ ] ownership map;
* \[ ] safety surface map;
* \[ ] regression risk score;
* \[ ] test runtime history;
* \[ ] selected policy:

  * fast;
  * balanced;
  * strict.

Output:

* \[ ] selected profile;
* \[ ] selected commands;
* \[ ] skipped commands with reasons;
* \[ ] required commands;
* \[ ] optional commands;
* \[ ] estimated runtime;
* \[ ] risk score;
* \[ ] blockers;
* \[ ] explanation;
* \[ ] no-live proof.

Selection rules:

* \[ ] Always include no-live quick check.
* \[ ] Always include security scan for security/evidence/support changes.
* \[ ] Always include redaction self-test for redaction/support bundle changes.
* \[ ] Always include dashboard import for UI changes.
* \[ ] Include browser smoke for dashboard action/chart changes.
* \[ ] Include full check-all for critical changes.
* \[ ] Include targeted tests for direct imports.
* \[ ] Include operator quality gate for operator/evidence/support changes.
* \[ ] Include roadmap validation for roadmap docs changes.
* \[ ] Include release quality gate for release/migration changes.

Acceptatiecriteria:

* \[ ] Selector explains why each command was chosen.
* \[ ] Selector estimates runtime from history.
* \[ ] Selector refuses unsafe profile.
* \[ ] Selector can output Codex-ready test block.
* \[ ] Tests cover common changed-file scenarios.

\---

## 10\. Fase 7 - Check-All V2 Orchestrator

Nieuwe module:

```text
src/binance\_spot\_bot/check\_all\_v2.py
```

Doel: bestaande `check\_all.py` niet breken, maar uitbreiden met profielen.

Commands:

```powershell
python -m binance\_spot\_bot.cli check-selected --changed src/binance\_spot\_bot/runtime.py
python -m binance\_spot\_bot.cli check-profile --profile fast
python -m binance\_spot\_bot.cli check-profile --profile standard
python -m binance\_spot\_bot.cli check-profile --profile deep
python -m binance\_spot\_bot.cli check-all-v2 --profile auto
```

Gedrag:

* \[ ] gebruikt dezelfde veilige env:

  * `PYTHONPATH=src`;
  * `LIVE\_TRADING\_ENABLED=false`;
  * `KILL\_SWITCH=true`.
* \[ ] voert geselecteerde commands sequentieel uit;
* \[ ] ondersteunt timeout per command;
* \[ ] redacted stdout/stderr tails;
* \[ ] schrijft test runtime history;
* \[ ] schrijft check report;
* \[ ] behoudt bestaande `check-all` als full safety fallback.

Acceptatiecriteria:

* \[ ] Check-all v2 draait selected commands.
* \[ ] Check-all v2 kan deep/full afdwingen.
* \[ ] Check-all v2 output is compatibel met evidence tooling.
* \[ ] Bestaande `check-all` blijft werken.
* \[ ] Tests gebruiken fake command runner.

\---

## 11\. Fase 8 - Flaky Test Tracking

Nieuwe module:

```text
src/binance\_spot\_bot/flaky\_tests.py
```

Detecties:

* \[ ] test faalt en slaagt later zonder codewijziging;
* \[ ] command duration spikes;
* \[ ] intermittent dashboard/browser smoke failure;
* \[ ] timeout patterns;
* \[ ] environment-dependent failure;
* \[ ] repeated stderr signatures;
* \[ ] known flaky classification.

Dataclasses:

* \[ ] `FlakyTestCandidate`
* \[ ] `FlakyTestSignature`
* \[ ] `FlakyTestReport`
* \[ ] `FlakyPolicy`

Output:

```text
data/test-runs/flaky/
  flaky-tests.json
  flaky-tests.md
```

Acceptatiecriteria:

* \[ ] Flaky candidates worden gerapporteerd, niet genegeerd.
* \[ ] Flaky test kan deep profile afdwingen.
* \[ ] Flaky report bevat evidence.
* \[ ] Dashboard toont flaky status.
* \[ ] Tests gebruiken synthetic history.

\---

## 12\. Fase 9 - Test Result Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/test\_evidence\_bundle.py
```

Bundle bevat:

* \[ ] changed files;
* \[ ] impact analysis;
* \[ ] risk score;
* \[ ] selected profile;
* \[ ] selected commands;
* \[ ] skipped commands + reasons;
* \[ ] command results;
* \[ ] stdout/stderr redacted tails;
* \[ ] runtime history summary;
* \[ ] flaky test report;
* \[ ] no-live proof;
* \[ ] security/redaction proof;
* \[ ] hashes.

Output:

```text
data/test-runs/evidence/<run\_id>/
  test\_evidence\_manifest.json
  test\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle links to Roadmap 090 evidence.
* \[ ] Bundle links to Roadmap 089 release evidence if relevant.

\---

## 13\. Fase 10 - Regression Risk Report

Nieuwe module:

```text
src/binance\_spot\_bot/regression\_risk\_report.py
```

Report secties:

* \[ ] changed files;
* \[ ] impacted domains;
* \[ ] impacted CLI commands;
* \[ ] impacted dashboard panels;
* \[ ] impacted safety surfaces;
* \[ ] impacted tests;
* \[ ] risk score;
* \[ ] selected profile;
* \[ ] required tests;
* \[ ] optional tests;
* \[ ] blockers;
* \[ ] estimated runtime;
* \[ ] no-live proof.

Output:

```text
data/test-runs/reports/
  regression-risk-report.md
  regression-risk-report.json
```

Acceptatiecriteria:

* \[ ] Report is Markdown + JSON.
* \[ ] Report explains recommendations.
* \[ ] Report is secret-free.
* \[ ] Report can be attached to PR template.
* \[ ] Dashboard can display report.

\---

## 14\. Fase 11 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli test-inventory
python -m binance\_spot\_bot.cli changed-files --changed src/binance\_spot\_bot/runtime.py
python -m binance\_spot\_bot.cli regression-risk --changed src/binance\_spot\_bot/runtime.py
python -m binance\_spot\_bot.cli test-select --changed src/binance\_spot\_bot/runtime.py
python -m binance\_spot\_bot.cli check-selected --changed src/binance\_spot\_bot/runtime.py
python -m binance\_spot\_bot.cli check-profile --profile fast
python -m binance\_spot\_bot.cli check-profile --profile standard
python -m binance\_spot\_bot.cli check-profile --profile deep
python -m binance\_spot\_bot.cli check-all-v2 --profile auto
python -m binance\_spot\_bot.cli test-history --days 14
python -m binance\_spot\_bot.cli flaky-tests
python -m binance\_spot\_bot.cli test-evidence-export --run-id latest
```

Acceptatiecriteria:

* \[ ] Commands werken offline.
* \[ ] Commands ondersteunen JSON output.
* \[ ] Commands gebruiken veilige env.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account/order endpoints.
* \[ ] Reports zijn secret-free.

\---

## 15\. Fase 12 - Test Selection Dashboard Panel

Nieuwe dashboardsectie:

```text
Test Selection \& Regression Risk
```

Panels:

* \[ ] changed files input;
* \[ ] detected changed files;
* \[ ] regression risk score;
* \[ ] selected profile;
* \[ ] selected commands;
* \[ ] skipped commands with reasons;
* \[ ] estimated runtime;
* \[ ] flaky tests;
* \[ ] latest test runs;
* \[ ] test runtime trends;
* \[ ] evidence bundle;
* \[ ] no-live proof.

Actions:

* \[ ] analyze changes;
* \[ ] generate test plan;
* \[ ] copy test commands;
* \[ ] run selected tests only with confirm;
* \[ ] run deep profile with confirm;
* \[ ] export test evidence;
* \[ ] open regression risk report.

Safeguards:

* \[ ] `LOCAL TEST SELECTION ONLY` badge.
* \[ ] No live controls.
* \[ ] Commands are visible before execution.
* \[ ] Safety-critical changes block fast-only execution.
* \[ ] Raw JSON only in debug expanders.
* \[ ] Stable widget keys.
* \[ ] Browser smoke covers panel.

Acceptatiecriteria:

* \[ ] Dashboard shows selected tests for changed files.
* \[ ] Dashboard blocks unsafe fast profile.
* \[ ] Dashboard can copy commands.
* \[ ] Dashboard can export evidence.
* \[ ] Browser smoke passes.

\---

## 16\. Fase 13 - Codex Task Pack Integration

Uitbreiding op Roadmap 090:

* \[ ] Codex task pack krijgt `recommended\_test\_profile`.
* \[ ] Codex task pack krijgt `required\_test\_commands`.
* \[ ] Codex task pack krijgt `risk\_score`.
* \[ ] Codex task pack krijgt `safety\_surface`.
* \[ ] Codex task pack krijgt `evidence\_required`.
* \[ ] PR template krijgt test evidence checklist.
* \[ ] Completion gate gebruikt test evidence bundle.

Acceptatiecriteria:

* \[ ] Task packs bevatten exacte testcommands.
* \[ ] Critical tasks krijgen deep profile.
* \[ ] Dashboard tasks krijgen dashboard/browser smoke.
* \[ ] Security tasks krijgen security/redaction checks.
* \[ ] Roadmap completion gate kan test evidence lezen.

\---

## 17\. Fase 14 - Release \& Migration Integration

Uitbreiding op Roadmap 089:

* \[ ] release quality gate leest regression risk.
* \[ ] migration changes vereisen release\_migration profile.
* \[ ] pre-release validation gebruikt test selection report.
* \[ ] release notes krijgen test profile summary.
* \[ ] release evidence bundle bevat test evidence.
* \[ ] rollback planner krijgt failed test context.

Acceptatiecriteria:

* \[ ] Release gate blocks missing required tests.
* \[ ] Migration apply changes force deep/release\_migration profile.
* \[ ] Release evidence links to test evidence.
* \[ ] No-live proof preserved.
* \[ ] Reports are secret-free.

\---

## 18\. Fase 15 - Metrics/Observability Integration

Uitbreiding op Roadmap 084:

Metrics:

* \[ ] test run count;
* \[ ] pass/fail count;
* \[ ] average runtime;
* \[ ] selected profile count;
* \[ ] risk score trend;
* \[ ] flaky test count;
* \[ ] deep profile frequency;
* \[ ] skipped tests count by reason;
* \[ ] check-all v2 duration;
* \[ ] safety blocker count.

Acceptatiecriteria:

* \[ ] Test metrics exporteerbaar naar metrics warehouse.
* \[ ] Weekly test analytics report mogelijk.
* \[ ] Flaky tests zichtbaar in observability.
* \[ ] Test runtime trends zichtbaar.
* \[ ] No secrets in metrics.

\---

## 19\. Fase 16 - Test Policy Configuration

Nieuwe config:

```text
config/test-selection-policy.json
```

Policy opties:

* \[ ] default mode:

  * fast;
  * balanced;
  * strict.
* \[ ] critical path rules;
* \[ ] dashboard smoke rules;
* \[ ] browser smoke rules;
* \[ ] security rules;
* \[ ] timeout per command;
* \[ ] retry policy for flaky candidates;
* \[ ] max estimated runtime for fast;
* \[ ] forced deep domains;
* \[ ] required commands always;
* \[ ] forbidden commands.

Acceptatiecriteria:

* \[ ] Policy is validated.
* \[ ] Forbidden commands cannot be enabled.
* \[ ] Invalid policy falls back to strict.
* \[ ] Policy changes are evidence-linked.
* \[ ] Tests cover invalid policy.

\---

## 20\. Fase 17 - Tests

### Unit tests

* \[ ] `tests/test\_test\_inventory.py`
* \[ ] `tests/test\_test\_runtime\_history.py`
* \[ ] `tests/test\_changed\_files.py`
* \[ ] `tests/test\_regression\_risk.py`
* \[ ] `tests/test\_test\_profiles.py`
* \[ ] `tests/test\_intelligent\_test\_selector.py`
* \[ ] `tests/test\_check\_all\_v2.py`
* \[ ] `tests/test\_flaky\_tests.py`
* \[ ] `tests/test\_test\_evidence\_bundle.py`
* \[ ] `tests/test\_regression\_risk\_report.py`
* \[ ] `tests/test\_test\_selection\_cli.py`
* \[ ] `tests/test\_test\_selection\_dashboard\_payload.py`
* \[ ] `tests/test\_test\_policy\_configuration.py`

### Integration tests

* \[ ] Build test inventory from fixture tests.
* \[ ] Detect changed files from explicit args.
* \[ ] Detect changed files from fixture git diff if available.
* \[ ] Score docs-only change as low risk.
* \[ ] Score runtime change as high risk.
* \[ ] Score redaction/security change as critical.
* \[ ] Select dashboard profile for UI change.
* \[ ] Select deep profile for execution/risk change.
* \[ ] Run check-all v2 with fake runner.
* \[ ] Write runtime history.
* \[ ] Detect flaky candidate from synthetic history.
* \[ ] Export test evidence bundle.

### Safety tests

* \[ ] Fast profile blocked for critical changes.
* \[ ] Live env is forced false.
* \[ ] Kill switch is forced true.
* \[ ] No signed endpoint command allowed.
* \[ ] No account endpoint command allowed.
* \[ ] No order endpoint command allowed.
* \[ ] Security/redaction changes require security scan and redaction self-test.
* \[ ] Dashboard changes require dashboard import/smoke.
* \[ ] Reports contain no secrets.
* \[ ] No-live proof remains true.

\---

## 21\. Docs

Nieuwe docs:

* \[ ] `docs/intelligent-test-selection-safety-contract.md`
* \[ ] `docs/test-inventory-engine.md`
* \[ ] `docs/test-runtime-history.md`
* \[ ] `docs/changed-files-detector.md`
* \[ ] `docs/regression-risk-scoring.md`
* \[ ] `docs/test-profiles.md`
* \[ ] `docs/intelligent-test-selector.md`
* \[ ] `docs/check-all-v2.md`
* \[ ] `docs/flaky-test-tracking.md`
* \[ ] `docs/test-evidence-bundle.md`
* \[ ] `docs/regression-risk-report.md`
* \[ ] `docs/test-selection-cli.md`
* \[ ] `docs/test-selection-dashboard.md`
* \[ ] `docs/test-selection-policy.md`

README updates:

* \[ ] when to use `check-all`;
* \[ ] when to use `check-all-v2`;
* \[ ] test profile explanation;
* \[ ] changed file examples;
* \[ ] Codex testing workflow;
* \[ ] no-live statement.

\---

## 22\. CLI command examples

### Selecteer tests voor runtimewijziging

```powershell
python -m binance\_spot\_bot.cli test-select --changed src/binance\_spot\_bot/runtime.py --json
```

### Run geselecteerde checks

```powershell
python -m binance\_spot\_bot.cli check-selected --changed src/binance\_spot\_bot/runtime.py
```

### Dashboardwijziging

```powershell
python -m binance\_spot\_bot.cli test-select --changed src/binance\_spot\_bot/ui/streamlit\_app.py --json
```

### Securitywijziging

```powershell
python -m binance\_spot\_bot.cli test-select --changed src/binance\_spot\_bot/redaction.py --json
```

### Deep profile

```powershell
python -m binance\_spot\_bot.cli check-profile --profile deep
```

### Flaky tests

```powershell
python -m binance\_spot\_bot.cli flaky-tests --json
```

\---

## 23\. Codex bouwvolgorde

### PR 1 - Test Inventory + Safety Contract

* \[ ] `test\_inventory.py`
* \[ ] safety contract doc
* \[ ] fixture tests.

### PR 2 - Test Runtime History

* \[ ] `test\_runtime\_history.py`
* \[ ] append-only history
* \[ ] redaction tests.

### PR 3 - Changed Files Detector

* \[ ] `changed\_files.py`
* \[ ] explicit args + git fallback
* \[ ] tests.

### PR 4 - Regression Risk Scoring

* \[ ] `regression\_risk.py`
* \[ ] risk policies
* \[ ] safety-critical hard blockers
* \[ ] tests.

### PR 5 - Test Profiles

* \[ ] `test\_profiles.py`
* \[ ] fast/standard/deep/dashboard/security/release\_migration
* \[ ] validation tests.

### PR 6 - Intelligent Test Selector

* \[ ] `intelligent\_test\_selector.py`
* \[ ] command selection
* \[ ] explainability
* \[ ] estimated runtime.

### PR 7 - Check-All V2

* \[ ] `check\_all\_v2.py`
* \[ ] fake command runner tests
* \[ ] safe env enforcement.

### PR 8 - Flaky Tests + Evidence Bundle

* \[ ] `flaky\_tests.py`
* \[ ] `test\_evidence\_bundle.py`
* \[ ] synthetic history tests.

### PR 9 - CLI + Reports

* \[ ] CLI commands
* \[ ] regression risk report
* \[ ] JSON/Markdown reports.

### PR 10 - Dashboard + Integrations + Docs

* \[ ] Test Selection dashboard panel
* \[ ] Codex integration
* \[ ] release/metrics integration
* \[ ] browser smoke
* \[ ] docs.

\---

## 24\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 092 PR 1: Test Inventory + Test Selection Safety Contract.

Maak docs/intelligent-test-selection-safety-contract.md.

Maak src/binance\_spot\_bot/test\_inventory.py met:
- TestFile
- TestCaseInfo
- TestCommand
- TestInventory
- TestInventoryManifest
- build\_test\_inventory(root: Path)
- write\_test\_inventory\_manifest(...)
- verify\_test\_inventory\_manifest(...)

Scan tests/ en detecteer:
- unittest classes
- pytest-style test functions
- imports naar src/binance\_spot\_bot
- likely domain per testfile
- safety\_relevance
- estimated\_profile fast/standard/deep
- recommended command per testfile

Guardrails:
- read-only
- geen code execution
- geen network calls
- geen API keys nodig
- geen signed/order/account endpoints
- output is secret-free
- live\_trading\_enabled=False in output

Voeg tests toe voor:
- unittest class detectie
- pytest function detectie
- imported source modules detectie
- domain guess voor runtime/operator/security/ui tests
- safety relevance voor risk/execution/security/redaction tests
- manifest hash verify pass/fail
- secret-like fixture content wordt niet gelekt
```

Waarom eerst:

* Testselectie begint met weten welke tests bestaan.
* Dit bouwt direct voort op Roadmap 091 repo inventory/knowledge graph.
* Het is read-only en raakt geen trading runtime.
* Het is klein genoeg voor Codex.
* Safety en no-live constraints kunnen meteen getest worden.

\---

## 25\. Definition of Done

Roadmap 092 is klaar als:

* \[ ] Test Selection Safety Contract bestaat.
* \[ ] Test Inventory Engine werkt.
* \[ ] Test Runtime History Store werkt.
* \[ ] Changed Files Detector werkt.
* \[ ] Regression Risk Scoring werkt.
* \[ ] Test Profile Definitions werken.
* \[ ] Intelligent Test Selector werkt.
* \[ ] Check-All V2 Orchestrator werkt.
* \[ ] Flaky Test Tracking werkt.
* \[ ] Test Result Evidence Bundle werkt.
* \[ ] Regression Risk Report werkt.
* \[ ] CLI commands werken.
* \[ ] Test Selection Dashboard Panel werkt.
* \[ ] Codex Task Pack Integration werkt.
* \[ ] Release \& Migration Integration werkt.
* \[ ] Metrics/Observability Integration werkt.
* \[ ] Test Policy Configuration werkt.
* \[ ] Tests bewijzen fast profile blokkeert critical changes.
* \[ ] Tests bewijzen env altijd `LIVE\_TRADING\_ENABLED=false` en `KILL\_SWITCH=true` zet.
* \[ ] Tests bewijzen geen signed/account/order endpoints.
* \[ ] Reports/evidence zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 092 kan na uitvoering naar `Voltooid docs`.

\---

## 26\. Verwachte Roadmap 093 daarna

Na Roadmap 092 zou Roadmap 093 logisch focussen op:

```text
Roadmap 093 - Performance Profiling, Runtime Bottleneck Analysis \& Resource Budgeting
```

Mogelijke inhoud:

* \[ ] runtime profiler;
* \[ ] dashboard render performance;
* \[ ] CLI command timing;
* \[ ] data/cache read/write bottlenecks;
* \[ ] memory usage reports;
* \[ ] performance budgets;
* \[ ] slow test/performance regression detection;
* \[ ] still no live trading.



---

## Afwerking

Status: Voltooid na hercontrole op 2026-05-12.

Implementatie/evidence: docs/roadmap-076-102-execution-evidence.md, src/binance_spot_bot/paper_os.py, 	ests/test_roadmaps_076_102_paper_os.py.

Validatie: gerichte tests groen, volledige pytest groen, check-all groen, dashboard-smoke groen, browser-smoke groen.



---

## Correctie-audit 2026-05-11

Deze roadmap is teruggezet naar Roadmap docs/ omdat de eerdere markering als Voltooid te breed was. De huidige code bevat alleen een gedeelde foundation in src/binance_spot_bot/paper_os.py en regressietests in 	ests/test_roadmaps_076_102_paper_os.py. Niet alle checklistpunten uit deze roadmap zijn volledig als production-grade feature geimplementeerd.

Open status: opnieuw plannen, opdelen in kleinere uitvoerbare taken, en pas opnieuw naar Voltooid docs/ verplaatsen na concrete implementatie en validatie per roadmap.


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole en volledige validatie.

Gebouwd: test inventory, runtime history, changed-files detector, regression risk scoring, test profiles, intelligent selector, check-all v2 planner, flaky tracking, test evidence bundle, regression risk report, CLI commands, dashboard panel en docs.

Validatie: tests/test_roadmap_092_intelligent_test_selection_acceptance.py; tests/test_roadmaps_089_096_full_surface.py; test selection CLI flow; python -m binance_spot_bot.cli check-all --skip-tests --json; python -m pytest -q; python -m binance_spot_bot.cli dashboard-smoke --seconds 1; python -m binance_spot_bot.cli dashboard-browser-smoke --url http://127.0.0.1:8506/ --seconds 10.

Safety: lokaal/paper-only, geen live trading enablement.

