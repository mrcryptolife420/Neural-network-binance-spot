# Roadmap 089 - Local Release Management, Versioned Upgrade Paths \& Migration Safety

Status: Voltooid na hercontrole en volledige validatie  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/089-roadmap-local-release-management-versioned-upgrade-paths-migration-safety.md
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

Doel: Roadmap 088 maakt offline backup, restore preview, sandbox restore drills en lokale state-integriteit veilig. Roadmap 089 bouwt daarop een **release-management en migration-safety laag**: versioned releases, upgrade plans, schema migrations, pre-upgrade backups, downgrade safety, release notes, compatibility checks, upgrade smoke tests, migration manifests en rollback evidence.

Live trading blijft volledig buiten scope. Release/upgrade tooling mag nooit live trading activeren, signed endpoints gebruiken, orders plaatsen of echte Binance accountdata gebruiken.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] `Voltooid docs/075-roadmap-simple-demo-multi-symbol-final-validation.md` bestaat.
* \[x] Roadmap 075 heeft status `Voltooid`.
* \[x] Roadmap 075 bevestigt:

  * multi-symbol dashboard helpers;
  * budget allocation;
  * risk summary;
  * evidence export;
  * full pytest;
  * check-all;
  * browser smoke;
  * live trading disabled.
* \[x] Geen bestaande Roadmap 089 gevonden via repo-search.
* \[x] Roadmap 088 is lokaal aangemaakt voor offline disaster recovery, backup/restore drills en local state integrity.

### Codebasecontrole

Gecontroleerde relevante modules/bestanden:

* \[x] `pyproject.toml`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] `src/binance\_spot\_bot/support\_bundle.py`
* \[x] `src/binance\_spot\_bot/security.py`
* \[x] `src/binance\_spot\_bot/redaction.py`

Bestaande basis:

* \[x] `pyproject.toml` heeft projectnaam `neural-network-binance-spot`.
* \[x] Huidige projectversie staat op `0.1.0`.
* \[x] Python requirement is `>=3.12`.
* \[x] CLI entrypoint bestaat als `spot-bot = "binance\_spot\_bot.cli:main"`.
* \[x] CLI bevat al operator/release-relevante commands zoals `check-all`, `dashboard-smoke`, `dashboard-browser-smoke`, `operator-quality-gate`, `support-bundle`, `support-bundle-verify`, `support-bundle-restore-preview`, `state-archive`, `retention-preview`, `evidence-manifest`, `evidence-chain`, `redaction-self-test`, `security-scan`, `environment-doctor`, `data-growth-budget` en `local-ops-snapshot`.
* \[x] `operator\_ops.py` bevat preview-only state archive, retention preview, evidence chain en local ops snapshot.
* \[x] `support\_bundle.py` kan redacted support bundles maken en verifiëren met manifest/hashes.
* \[x] Security/redaction basis bestaat.
* \[x] Operator outputs houden `live\_trading\_enabled=False`.

### Belangrijkste gat na Roadmap 088

Na Roadmap 088 kan lokale state geback-upt en hersteld worden. Wat nog mist:

* \[ ] officiële release metadata;
* \[ ] release manifesten;
* \[ ] changelog/release notes generator;
* \[ ] upgrade plan per versie;
* \[ ] schema migration registry;
* \[ ] compatibility checks;
* \[ ] pre-upgrade backup enforcement;
* \[ ] dry-run migration;
* \[ ] upgrade smoke suite;
* \[ ] downgrade/rollback plan;
* \[ ] migration evidence bundle;
* \[ ] local release dashboard;
* \[ ] versioned operator docs.

\---

## 1\. Hoofddoel Roadmap 089

Maak een veilige lokale release- en upgradeflow:

```text
Current install
→ release manifest
→ compatibility check
→ pre-upgrade backup
→ migration plan
→ migration dry-run
→ apply upgrade/migration
→ post-upgrade validation
→ rollback/downgrade plan
→ release evidence bundle
```

Na Roadmap 089 moet de bot kunnen:

* \[ ] huidige versie detecteren;
* \[ ] install fingerprint maken;
* \[ ] release manifest maken;
* \[ ] changelog/release notes genereren;
* \[ ] schema compatibility checken;
* \[ ] pre-upgrade backup afdwingen;
* \[ ] schema/data migraties registreren;
* \[ ] migraties eerst dry-runnen;
* \[ ] upgrades lokaal valideren met smoke tests;
* \[ ] downgrade/rollback pad tonen;
* \[ ] migration evidence exporteren;
* \[ ] operator duidelijk laten zien wat verandert;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen package manager vanaf nul bouwen.
* \[ ] Geen cloud release service.
* \[ ] Geen auto-update die code downloadt.
* \[ ] Geen remote telemetry.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen Binance account endpoints.
* \[ ] Geen order endpoints.
* \[ ] Geen destructive migration zonder backup + dry-run + confirm.
* \[ ] Geen migraties zonder rollback plan.
* \[ ] Geen schema change zonder manifest.

Wel doen:

* \[ ] lokale release metadata toevoegen;
* \[ ] release manifesten genereren;
* \[ ] upgrade preflight maken;
* \[ ] migration registry maken;
* \[ ] migration dry-run/apply framework maken;
* \[ ] post-upgrade validation maken;
* \[ ] rollback/downgrade preview maken;
* \[ ] release evidence bundels maken;
* \[ ] dashboard/CLI toevoegen;
* \[ ] alles paper/demo/local-only houden.

\---

## 3\. Fase 0 - Release \& Migration Safety Contract

Nieuwe doc:

```text
docs/release-migration-safety-contract.md
```

Regels:

* \[ ] Upgrade tooling is local-only.
* \[ ] Geen remote auto-download.
* \[ ] Geen remote telemetry.
* \[ ] Geen secrets in release artifacts.
* \[ ] Geen live mode.
* \[ ] Geen signed endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen order endpoints.
* \[ ] Pre-upgrade backup verplicht bij migraties.
* \[ ] Migration dry-run verplicht vóór apply.
* \[ ] Destructive migration vereist exact confirm phrase.
* \[ ] Post-upgrade check-all/smoke vereist.
* \[ ] Rollback/downgrade plan verplicht.
* \[ ] Release evidence bundle bevat no-live proof.
* \[ ] Migration output is redacted.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen upgrade tooling kan live niet activeren.
* \[ ] Tests bewijzen migration apply faalt zonder backup.
* \[ ] Dashboard toont `LOCAL RELEASE ONLY`.
* \[ ] Release reports bevatten no-live proof.

\---

## 4\. Fase 1 - Version Metadata \& Install Fingerprint

Nieuwe module:

```text
src/binance\_spot\_bot/versioning.py
```

Dataclasses:

* \[ ] `ProjectVersion`
* \[ ] `InstallFingerprint`
* \[ ] `VersionComponent`
* \[ ] `VersionCheckResult`

Metadata bronnen:

* \[ ] `pyproject.toml` project version;
* \[ ] package version via `importlib.metadata`;
* \[ ] git commit hash indien beschikbaar;
* \[ ] dirty working tree flag indien beschikbaar;
* \[ ] Python version;
* \[ ] optional dependency groups installed;
* \[ ] OS/platform;
* \[ ] data\_dir path hash;
* \[ ] config schema version;
* \[ ] data schema version;
* \[ ] metrics schema version;
* \[ ] permission schema version;
* \[ ] backup schema version.

Output:

```text
data/releases/current-install-fingerprint.json
```

Acceptatiecriteria:

* \[ ] Version detection werkt zonder git.
* \[ ] Version detection werkt zonder installed package metadata.
* \[ ] Output is secret-free.
* \[ ] `live\_trading\_enabled=False` in output.
* \[ ] Tests dekken pyproject/package fallback.

\---

## 5\. Fase 2 - Release Manifest Schema

Nieuwe module:

```text
src/binance\_spot\_bot/release\_manifest.py
```

Dataclasses:

* \[ ] `ReleaseManifest`
* \[ ] `ReleaseChange`
* \[ ] `ReleaseCompatibility`
* \[ ] `ReleaseMigrationRequirement`
* \[ ] `ReleaseValidationRequirement`
* \[ ] `ReleaseArtifact`

Manifest velden:

* \[ ] release\_id;
* \[ ] version;
* \[ ] created\_at\_ms;
* \[ ] git\_commit;
* \[ ] previous\_version;
* \[ ] release\_type:

  * patch;
  * minor;
  * major;
  * roadmap\_batch;
  * local\_dev\_snapshot.
* \[ ] changed\_modules;
* \[ ] changed\_docs;
* \[ ] changed\_cli\_commands;
* \[ ] changed\_dashboard\_pages;
* \[ ] changed\_data\_schemas;
* \[ ] migration\_required;
* \[ ] pre\_upgrade\_backup\_required;
* \[ ] rollback\_supported;
* \[ ] minimum\_python;
* \[ ] dependency\_groups;
* \[ ] validation\_commands;
* \[ ] no\_live\_statement;
* \[ ] hashes.

Acceptatiecriteria:

* \[ ] Release manifest is JSON-serializable.
* \[ ] Release manifest contains no secrets.
* \[ ] Manifest can be verified by hashes.
* \[ ] Manifest includes no-live statement.
* \[ ] Tests cover missing/invalid fields.

\---

## 6\. Fase 3 - Changelog \& Release Notes Generator

Nieuwe module:

```text
src/binance\_spot\_bot/release\_notes.py
```

Inputs:

* \[ ] release manifest;
* \[ ] roadmap docs;
* \[ ] completed docs;
* \[ ] git diff summary indien beschikbaar;
* \[ ] changed files;
* \[ ] migration requirements;
* \[ ] validation results.

Output:

```text
data/releases/<release\_id>/
  release-notes.md
  release-notes.json
```

Release notes secties:

* \[ ] Summary;
* \[ ] New features;
* \[ ] Changed behavior;
* \[ ] Migration required;
* \[ ] Backup required;
* \[ ] Breaking changes;
* \[ ] Dashboard changes;
* \[ ] CLI changes;
* \[ ] Data schema changes;
* \[ ] Security/redaction changes;
* \[ ] Known issues;
* \[ ] Validation checklist;
* \[ ] Rollback notes;
* \[ ] No-live statement.

Acceptatiecriteria:

* \[ ] Release notes zijn leesbaar.
* \[ ] Release notes zijn secret-free.
* \[ ] Migration required is duidelijk zichtbaar.
* \[ ] Operator next steps staan erin.
* \[ ] Dashboard kan release notes tonen/downloaden.

\---

## 7\. Fase 4 - Schema Version Registry

Nieuwe module:

```text
src/binance\_spot\_bot/schema\_registry.py
```

Schema domains:

* \[ ] config schema;
* \[ ] data store schema;
* \[ ] public Binance cache schema;
* \[ ] metrics schema;
* \[ ] action center schema;
* \[ ] permission schema;
* \[ ] compliance schema;
* \[ ] backup schema;
* \[ ] deployment schema;
* \[ ] portfolio policy schema;
* \[ ] AI ops context schema;
* \[ ] release manifest schema.

Dataclasses:

* \[ ] `SchemaVersion`
* \[ ] `SchemaRegistry`
* \[ ] `SchemaCompatibility`
* \[ ] `SchemaValidationResult`

Compatibility statuses:

* \[ ] compatible;
* \[ ] migration\_required;
* \[ ] deprecated;
* \[ ] unsupported;
* \[ ] unknown.

Acceptatiecriteria:

* \[ ] Schema registry can list all schema domains.
* \[ ] Schema registry validates current state.
* \[ ] Unknown schema geeft warning/blocker.
* \[ ] Registry output is secret-free.
* \[ ] Tests cover compatibility matrix.

\---

## 8\. Fase 5 - Migration Registry

Nieuwe module:

```text
src/binance\_spot\_bot/migration\_registry.py
```

Dataclasses:

* \[ ] `MigrationDefinition`
* \[ ] `MigrationPlan`
* \[ ] `MigrationStep`
* \[ ] `MigrationDependency`
* \[ ] `MigrationStatus`
* \[ ] `MigrationResult`

MigrationDefinition velden:

* \[ ] migration\_id;
* \[ ] from\_version;
* \[ ] to\_version;
* \[ ] schema\_domain;
* \[ ] description;
* \[ ] destructive;
* \[ ] reversible;
* \[ ] requires\_backup;
* \[ ] requires\_dry\_run;
* \[ ] dependencies;
* \[ ] affected\_paths;
* \[ ] validation\_steps;
* \[ ] rollback\_steps;
* \[ ] no\_live\_required=true.

Acceptatiecriteria:

* \[ ] Migrations are registered declaratively.
* \[ ] Missing migration blocks upgrade.
* \[ ] Destructive migration requires backup.
* \[ ] Migration registry contains no secrets.
* \[ ] Tests cover dependency ordering.

\---

## 9\. Fase 6 - Upgrade Compatibility Checker

Nieuwe module:

```text
src/binance\_spot\_bot/upgrade\_compatibility.py
```

Checks:

* \[ ] current version known;
* \[ ] target version known;
* \[ ] Python version compatible;
* \[ ] dependency groups compatible;
* \[ ] data schema compatible;
* \[ ] migration path exists;
* \[ ] backup available/fresh;
* \[ ] restore drill recent enough;
* \[ ] permission/compliance healthy;
* \[ ] secret scan clean;
* \[ ] redaction self-test pass;
* \[ ] check-all pass or known waiver;
* \[ ] data growth within budget;
* \[ ] disk space enough;
* \[ ] no-live proof present.

Status:

* \[ ] ok;
* \[ ] warning;
* \[ ] blocked;
* \[ ] unknown.

Acceptatiecriteria:

* \[ ] Upgrade blocked if no migration path.
* \[ ] Upgrade blocked if no pre-upgrade backup for required migration.
* \[ ] Upgrade warned if restore drill stale.
* \[ ] Compatibility report is exportable.
* \[ ] No API/network required.

\---

## 10\. Fase 7 - Pre-Upgrade Backup Gate

Nieuwe module:

```text
src/binance\_spot\_bot/pre\_upgrade\_backup\_gate.py
```

Gate checks:

* \[ ] backup profile selected;
* \[ ] backup created after current install fingerprint;
* \[ ] backup verification ok;
* \[ ] backup contains no-live proof;
* \[ ] backup contains redaction proof;
* \[ ] backup contains permission/compliance evidence;
* \[ ] backup restore preview possible;
* \[ ] backup ID linked to upgrade plan.

Acceptatiecriteria:

* \[ ] Upgrade apply fails without backup.
* \[ ] Backup must verify.
* \[ ] Backup must be recent enough.
* \[ ] Backup manifest linked in upgrade evidence.
* \[ ] Tests use fake backup artifacts.

\---

## 11\. Fase 8 - Migration Dry-Run Engine

Nieuwe module:

```text
src/binance\_spot\_bot/migration\_dry\_run.py
```

Dry-run behavior:

* \[ ] loads migration plan;
* \[ ] scans affected paths;
* \[ ] predicts creates/updates/deletes;
* \[ ] validates input schemas;
* \[ ] detects conflicts;
* \[ ] estimates output sizes;
* \[ ] checks rollback feasibility;
* \[ ] writes dry-run report;
* \[ ] does not modify original files.

Output:

```text
data/releases/<release\_id>/migrations/
  migration-dry-run.json
  migration-dry-run.md
  affected-files.csv
```

Acceptatiecriteria:

* \[ ] Dry-run never writes to source state.
* \[ ] Dry-run lists all affected files.
* \[ ] Dry-run detects destructive changes.
* \[ ] Dry-run must pass before migration apply.
* \[ ] Tests verify no source modification.

\---

## 12\. Fase 9 - Migration Apply Engine

Nieuwe module:

```text
src/binance\_spot\_bot/migration\_apply.py
```

Apply flow:

* \[ ] require compatibility ok/warn with accepted warnings;
* \[ ] require pre-upgrade backup gate pass;
* \[ ] require dry-run pass;
* \[ ] require exact confirm phrase if destructive;
* \[ ] create migration journal;
* \[ ] apply steps in order;
* \[ ] write per-step result;
* \[ ] validate output schemas;
* \[ ] write migration result;
* \[ ] update schema registry state;
* \[ ] run post-migration checks;
* \[ ] create rollback marker.

Guardrails:

* \[ ] no live mode;
* \[ ] no signed endpoints;
* \[ ] no account endpoints;
* \[ ] no path traversal;
* \[ ] no writes outside data\_dir unless explicit safe target;
* \[ ] fail fast on hash mismatch;
* \[ ] rollback marker required.

Acceptatiecriteria:

* \[ ] Migration cannot run without backup + dry-run.
* \[ ] Migration journal is append-only.
* \[ ] Failed migration leaves recovery instructions.
* \[ ] Migration result is secret-free.
* \[ ] Tests use temp dirs and fake migrations.

\---

## 13\. Fase 10 - Post-Upgrade Validation Suite

Nieuwe module:

```text
src/binance\_spot\_bot/post\_upgrade\_validation.py
```

Validation commands:

* \[ ] version check;
* \[ ] schema registry validation;
* \[ ] state integrity check;
* \[ ] permission drift check;
* \[ ] evidence continuity check;
* \[ ] redaction self-test;
* \[ ] secret scan;
* \[ ] support bundle verify;
* \[ ] check-all;
* \[ ] dashboard smoke;
* \[ ] dashboard browser smoke optional;
* \[ ] operator quality gate;
* \[ ] local ops snapshot.

Acceptatiecriteria:

* \[ ] Validation report generated.
* \[ ] Upgrade remains blocked until critical validations pass.
* \[ ] Browser smoke can be optional/manual if heavy.
* \[ ] Validation output is secret-free.
* \[ ] No live trading.

\---

## 14\. Fase 11 - Rollback \& Downgrade Planner

Nieuwe module:

```text
src/binance\_spot\_bot/rollback\_planner.py
```

Rollback sources:

* \[ ] pre-upgrade backup;
* \[ ] pre-migration snapshot;
* \[ ] restore preview;
* \[ ] migration rollback steps;
* \[ ] previous release manifest;
* \[ ] previous schema registry state.

Planner output:

* \[ ] rollback feasibility;
* \[ ] files to restore;
* \[ ] schema downgrades;
* \[ ] data loss risk;
* \[ ] conflicts;
* \[ ] required confirm phrase;
* \[ ] verification steps;
* \[ ] no-live proof.

Acceptatiecriteria:

* \[ ] Rollback plan generated before upgrade.
* \[ ] Rollback plan refuses if backup invalid.
* \[ ] Downgrade unsupported is explicit.
* \[ ] Rollback plan is dashboard-ready.
* \[ ] No destructive rollback without confirm.

\---

## 15\. Fase 12 - Release Candidate Workflow

Nieuwe module:

```text
src/binance\_spot\_bot/release\_candidate.py
```

Workflow:

* \[ ] create release candidate manifest;
* \[ ] run compatibility check;
* \[ ] create pre-upgrade backup;
* \[ ] run sandbox restore from backup;
* \[ ] apply migrations in sandbox;
* \[ ] run post-upgrade validation in sandbox;
* \[ ] create release candidate report;
* \[ ] approve/reject candidate.

Acceptatiecriteria:

* \[ ] RC workflow can run offline.
* \[ ] RC workflow does not modify real data\_dir.
* \[ ] RC report is evidence-linked.
* \[ ] RC must pass before upgrade apply.
* \[ ] Tests use fixture release.

\---

## 16\. Fase 13 - Release Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/release\_evidence\_bundle.py
```

Bundle bevat:

* \[ ] install fingerprint before;
* \[ ] target release manifest;
* \[ ] release notes;
* \[ ] compatibility report;
* \[ ] pre-upgrade backup manifest;
* \[ ] backup verification;
* \[ ] migration plan;
* \[ ] migration dry-run;
* \[ ] migration result;
* \[ ] post-upgrade validation;
* \[ ] rollback plan;
* \[ ] install fingerprint after;
* \[ ] no-live proof;
* \[ ] redaction proof;
* \[ ] hashes.

Output:

```text
data/releases/<release\_id>/evidence/
  release\_evidence\_manifest.json
  release\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Dashboard/CLI export works.
* \[ ] Bundle supports future audits.

\---

## 17\. Fase 14 - Local Release Dashboard Panel

Nieuwe dashboardsectie:

```text
Release Management
```

Panels:

* \[ ] current version;
* \[ ] install fingerprint;
* \[ ] target release manifest;
* \[ ] release notes;
* \[ ] compatibility status;
* \[ ] pre-upgrade backup status;
* \[ ] migration plan;
* \[ ] dry-run result;
* \[ ] post-upgrade validation;
* \[ ] rollback plan;
* \[ ] release evidence bundle;
* \[ ] no-live proof.

Actions:

* \[ ] generate install fingerprint;
* \[ ] create release manifest;
* \[ ] generate release notes;
* \[ ] run compatibility check;
* \[ ] run pre-upgrade backup gate;
* \[ ] run migration dry-run;
* \[ ] apply migration with confirm;
* \[ ] run post-upgrade validation;
* \[ ] generate rollback plan;
* \[ ] export release evidence.

Safeguards:

* \[ ] Apply migration hidden behind expert mode.
* \[ ] Exact confirm phrase required.
* \[ ] No live controls.
* \[ ] Raw JSON only in debug expanders.
* \[ ] Stable widget keys.
* \[ ] Browser smoke covers panel.

Acceptatiecriteria:

* \[ ] Dashboard shows `LOCAL RELEASE ONLY`.
* \[ ] Dashboard cannot run migration without backup gate.
* \[ ] Dashboard cannot enable live.
* \[ ] Release evidence downloadable.
* \[ ] Browser smoke passes.

\---

## 18\. Fase 15 - Release Management CLI

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli version-info
python -m binance\_spot\_bot.cli install-fingerprint
python -m binance\_spot\_bot.cli release-manifest-create --version 0.2.0
python -m binance\_spot\_bot.cli release-notes-generate --release-id <id>
python -m binance\_spot\_bot.cli schema-registry
python -m binance\_spot\_bot.cli migration-plan --from 0.1.0 --to 0.2.0
python -m binance\_spot\_bot.cli upgrade-compatibility --target-release <id>
python -m binance\_spot\_bot.cli pre-upgrade-backup --target-release <id>
python -m binance\_spot\_bot.cli migration-dry-run --plan-id <id>
python -m binance\_spot\_bot.cli migration-apply --plan-id <id> --confirm APPLY\_LOCAL\_MIGRATION
python -m binance\_spot\_bot.cli post-upgrade-validation --release-id <id>
python -m binance\_spot\_bot.cli rollback-plan --release-id <id>
python -m binance\_spot\_bot.cli release-evidence-export --release-id <id>
```

Acceptatiecriteria:

* \[ ] Commands work offline.
* \[ ] Commands support JSON output.
* \[ ] Migration apply requires confirm.
* \[ ] Commands use no API keys.
* \[ ] Commands use no signed/order/account endpoints.
* \[ ] Reports are secret-free.

\---

## 19\. Fase 16 - Upgrade Runbooks

Nieuwe docs/runbooks:

```text
docs/runbooks/releases/
```

Runbooks:

* \[ ] `prepare-local-upgrade.md`
* \[ ] `create-pre-upgrade-backup.md`
* \[ ] `run-upgrade-compatibility-check.md`
* \[ ] `migration-dry-run.md`
* \[ ] `apply-local-migration.md`
* \[ ] `post-upgrade-validation.md`
* \[ ] `rollback-after-failed-upgrade.md`
* \[ ] `downgrade-preview.md`
* \[ ] `release-evidence-review.md`
* \[ ] `schema-migration-authoring.md`

Acceptatiecriteria:

* \[ ] Runbooks contain step-by-step CLI commands.
* \[ ] Runbooks include safety warnings.
* \[ ] Runbooks include expected outputs.
* \[ ] Runbooks include failure handling.
* \[ ] Runbooks are linked in dashboard.

\---

## 20\. Fase 17 - Migration Authoring Guidelines

Nieuwe doc:

```text
docs/migration-authoring-guidelines.md
```

Richtlijnen:

* \[ ] elke migration krijgt ID;
* \[ ] elke migration is idempotent waar mogelijk;
* \[ ] elke migration heeft dry-run;
* \[ ] elke migration heeft validation;
* \[ ] elke destructive migration heeft rollback plan;
* \[ ] elke migration heeft tests;
* \[ ] geen network calls;
* \[ ] geen live/signed/order/account calls;
* \[ ] geen secrets in outputs;
* \[ ] affected paths zijn expliciet.

Acceptatiecriteria:

* \[ ] Guidelines bestaan.
* \[ ] Migration template bestaat.
* \[ ] Tests kunnen template valideren.
* \[ ] PR checklist bevat migration safety.

\---

## 21\. Fase 18 - Release Quality Gates

Nieuwe module:

```text
src/binance\_spot\_bot/release\_quality\_gate.py
```

Gates:

* \[ ] release manifest valid;
* \[ ] release notes generated;
* \[ ] migration registry valid;
* \[ ] compatibility check pass;
* \[ ] pre-upgrade backup pass;
* \[ ] migration dry-run pass;
* \[ ] post-upgrade validation pass;
* \[ ] check-all pass;
* \[ ] dashboard smoke pass;
* \[ ] redaction self-test pass;
* \[ ] secret scan pass;
* \[ ] no-live proof pass;
* \[ ] rollback plan exists.

Acceptatiecriteria:

* \[ ] Gate result is ok/warn/fail.
* \[ ] Fail blocks release approval.
* \[ ] Gate report is exportable.
* \[ ] Gate integrates with operator quality gate.
* \[ ] Tests cover hard blockers.

\---

## 22\. Fase 19 - Tests

### Unit tests

* \[ ] `tests/test\_versioning.py`
* \[ ] `tests/test\_release\_manifest.py`
* \[ ] `tests/test\_release\_notes.py`
* \[ ] `tests/test\_schema\_registry.py`
* \[ ] `tests/test\_migration\_registry.py`
* \[ ] `tests/test\_upgrade\_compatibility.py`
* \[ ] `tests/test\_pre\_upgrade\_backup\_gate.py`
* \[ ] `tests/test\_migration\_dry\_run.py`
* \[ ] `tests/test\_migration\_apply.py`
* \[ ] `tests/test\_post\_upgrade\_validation.py`
* \[ ] `tests/test\_rollback\_planner.py`
* \[ ] `tests/test\_release\_candidate.py`
* \[ ] `tests/test\_release\_evidence\_bundle.py`
* \[ ] `tests/test\_release\_quality\_gate.py`

### Integration tests

* \[ ] Create fake install fingerprint.
* \[ ] Create target release manifest.
* \[ ] Generate release notes.
* \[ ] Validate schema registry.
* \[ ] Create fake migration plan.
* \[ ] Run compatibility check.
* \[ ] Require fake pre-upgrade backup.
* \[ ] Run migration dry-run.
* \[ ] Apply fake migration in temp data dir.
* \[ ] Run post-upgrade validation subset.
* \[ ] Generate rollback plan.
* \[ ] Export release evidence bundle.

### Safety tests

* \[ ] Migration apply rejected without backup.
* \[ ] Migration apply rejected without dry-run.
* \[ ] Destructive migration requires confirm.
* \[ ] Migration cannot write outside data\_dir.
* \[ ] Migration cannot enable live.
* \[ ] Release tooling uses no signed endpoints.
* \[ ] Release tooling uses no account endpoints.
* \[ ] Release tooling uses no order endpoints.
* \[ ] Reports contain no secrets.
* \[ ] No-live proof remains true.

\---

## 23\. Docs

Nieuwe docs:

* \[ ] `docs/release-migration-safety-contract.md`
* \[ ] `docs/versioning-install-fingerprint.md`
* \[ ] `docs/release-manifest.md`
* \[ ] `docs/release-notes-generator.md`
* \[ ] `docs/schema-version-registry.md`
* \[ ] `docs/migration-registry.md`
* \[ ] `docs/upgrade-compatibility-checker.md`
* \[ ] `docs/pre-upgrade-backup-gate.md`
* \[ ] `docs/migration-dry-run.md`
* \[ ] `docs/migration-apply.md`
* \[ ] `docs/post-upgrade-validation.md`
* \[ ] `docs/rollback-downgrade-planner.md`
* \[ ] `docs/release-candidate-workflow.md`
* \[ ] `docs/release-evidence-bundle.md`
* \[ ] `docs/local-release-dashboard.md`
* \[ ] `docs/release-management-cli.md`
* \[ ] `docs/migration-authoring-guidelines.md`
* \[ ] `docs/release-quality-gates.md`

README updates:

* \[ ] current version command;
* \[ ] release manifest command;
* \[ ] upgrade workflow;
* \[ ] pre-upgrade backup requirement;
* \[ ] migration dry-run/apply;
* \[ ] rollback plan;
* \[ ] no-live statement.

\---

## 24\. Codex bouwvolgorde

### PR 1 - Version Metadata + Release Manifest

* \[ ] `versioning.py`
* \[ ] `release\_manifest.py`
* \[ ] install fingerprint output
* \[ ] release manifest JSON
* \[ ] tests.

### PR 2 - Release Notes

* \[ ] `release\_notes.py`
* \[ ] markdown/json output
* \[ ] roadmap/doc summary input
* \[ ] tests.

### PR 3 - Schema Registry

* \[ ] `schema\_registry.py`
* \[ ] schema domains
* \[ ] compatibility statuses
* \[ ] tests.

### PR 4 - Migration Registry

* \[ ] `migration\_registry.py`
* \[ ] migration definitions/plans
* \[ ] dependency ordering
* \[ ] tests.

### PR 5 - Upgrade Compatibility + Backup Gate

* \[ ] `upgrade\_compatibility.py`
* \[ ] `pre\_upgrade\_backup\_gate.py`
* \[ ] fake backup artifacts
* \[ ] tests.

### PR 6 - Migration Dry-Run

* \[ ] `migration\_dry\_run.py`
* \[ ] affected files report
* \[ ] no source write tests.

### PR 7 - Migration Apply

* \[ ] `migration\_apply.py`
* \[ ] confirm gates
* \[ ] migration journal
* \[ ] rollback marker
* \[ ] tests.

### PR 8 - Post-Upgrade Validation + Rollback Planner

* \[ ] `post\_upgrade\_validation.py`
* \[ ] `rollback\_planner.py`
* \[ ] tests.

### PR 9 - Release Candidate + Evidence Bundle + Quality Gate

* \[ ] `release\_candidate.py`
* \[ ] `release\_evidence\_bundle.py`
* \[ ] `release\_quality\_gate.py`
* \[ ] tests.

### PR 10 - Dashboard + CLI + Docs

* \[ ] Release Management dashboard;
* \[ ] CLI commands;
* \[ ] runbooks;
* \[ ] browser smoke;
* \[ ] docs.

\---

## 25\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 089 PR 1: Version Metadata + Release Manifest.

Maak src/binance\_spot\_bot/versioning.py met:
- ProjectVersion
- InstallFingerprint
- VersionComponent
- VersionCheckResult
- detect\_project\_version()
- build\_install\_fingerprint()

Maak src/binance\_spot\_bot/release\_manifest.py met:
- ReleaseManifest
- ReleaseChange
- ReleaseCompatibility
- ReleaseMigrationRequirement
- ReleaseValidationRequirement
- ReleaseArtifact
- create\_release\_manifest()
- verify\_release\_manifest()

Gebruik pyproject.toml als primaire versiebron.
Gebruik importlib.metadata als fallback indien beschikbaar.
Als git metadata niet beschikbaar is, moet de output alsnog werken met git\_available=False.

Schrijf fingerprint naar:
data/releases/current-install-fingerprint.json

Zorg dat outputs:
- JSON serializable zijn
- secret-free zijn
- live\_trading\_enabled=False bevatten
- no\_live\_statement bevatten
- hashes bevatten waar zinvol

Voeg tests toe voor:
- pyproject version detectie
- package metadata fallback
- git unavailable fallback
- install fingerprint serialization
- release manifest validation
- secret-free output
- live\_trading\_enabled=False

Geen migration registry in deze PR.
Geen migration apply.
Geen dashboard.
Geen API calls.
Geen signed endpoints.
Geen orders.
Geen live trading.
```

Waarom eerst:

* Release management begint met betrouwbaar weten welke versie draait.
* Release manifesten zijn de basis voor notes, migrations, compatibility, quality gates en evidence bundles.
* Het raakt geen trading runtime.
* Het is klein genoeg voor Codex.
* Safety/no-live output kan direct getest worden.

\---

## 26\. Definition of Done

Roadmap 089 is klaar als:

* \[ ] Release \& Migration Safety Contract bestaat.
* \[ ] Version Metadata \& Install Fingerprint werkt.
* \[ ] Release Manifest Schema werkt.
* \[ ] Changelog \& Release Notes Generator werkt.
* \[ ] Schema Version Registry werkt.
* \[ ] Migration Registry werkt.
* \[ ] Upgrade Compatibility Checker werkt.
* \[ ] Pre-Upgrade Backup Gate werkt.
* \[ ] Migration Dry-Run Engine werkt.
* \[ ] Migration Apply Engine werkt.
* \[ ] Post-Upgrade Validation Suite werkt.
* \[ ] Rollback \& Downgrade Planner werkt.
* \[ ] Release Candidate Workflow werkt.
* \[ ] Release Evidence Bundle werkt.
* \[ ] Local Release Dashboard Panel werkt.
* \[ ] Release Management CLI werkt.
* \[ ] Upgrade Runbooks bestaan.
* \[ ] Migration Authoring Guidelines bestaan.
* \[ ] Release Quality Gates werken.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen migration apply niet kan zonder backup + dry-run.
* \[ ] Reports/bundles zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 089 kan na uitvoering naar `Voltooid docs`.

\---

## 27\. Verwachte Roadmap 090 daarna

Na Roadmap 089 zou Roadmap 090 logisch focussen op:

```text
Roadmap 090 - Developer Experience, Codex Task Packs \& Roadmap Execution Automation
```

Mogelijke inhoud:

* \[ ] Codex-ready task packs per roadmapfase;
* \[ ] PR templates per roadmap type;
* \[ ] automated roadmap validation;
* \[ ] completed roadmap mover;
* \[ ] local task dependency graph;
* \[ ] roadmap evidence checker;
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

Gebouwd: version metadata, install fingerprint, release manifest, release notes, schema/migration registry, dry-run/apply migration framework, backup gate, compatibility checks, post-upgrade validation, rollback planning, release candidate, quality gate, release evidence bundle, dashboard surface, CLI commands en operator docs/runbooks.

Validatie: tests/test_roadmap_089_release_management_acceptance.py; tests/test_roadmaps_089_096_full_surface.py; python -m binance_spot_bot.cli check-all --skip-tests --json; python -m pytest -q; python -m binance_spot_bot.cli dashboard-smoke --seconds 1; python -m binance_spot_bot.cli dashboard-browser-smoke --url http://127.0.0.1:8506/ --seconds 10.

Safety: lokaal/paper-only, geen live trading enablement.

