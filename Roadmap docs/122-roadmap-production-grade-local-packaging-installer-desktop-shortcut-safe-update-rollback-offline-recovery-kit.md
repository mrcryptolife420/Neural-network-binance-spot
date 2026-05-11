# Roadmap 122 - Production-Grade Local Packaging, Installer, Desktop Shortcut, Safe Update/Rollback \& Offline Recovery Kit

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/122-roadmap-production-grade-local-packaging-installer-desktop-shortcut-safe-update-rollback-offline-recovery-kit.md
```

## Samenvatting

Roadmap 116 maakt de gewenste one-click bot-app richting duidelijk:

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

Roadmap 117 bouwt demo spot data collection, dataset quality, model/strategy validation, paper replay en testnet promotion.

Roadmap 118 bouwt live dry-run, read-only account verification, order preview, sizing guards, safety drills en een tiny capped first-order gate.

Roadmap 119 bouwt controlled live sessions met micro-position budgets, max orders, reconciliation, live monitoring en automatic disarm.

Roadmap 120 bouwt live governance met scorecards, risk-limit calibration, scaling decisions, operator approvals en lifecycle governance.

Roadmap 121 bouwt live operations: incident response, runbook automation, rollback drills, post-trade forensics, recovery gates en incident evidence.

Roadmap 122 is de beste volgende stap: **maak van de repo een productieklare lokale Windows/desktop app-package die veilig te installeren, starten, updaten, herstellen en terug te draaien is**.

De kern:

```text
repo/source
→ reproducible local package
→ dependency lock
→ one-click installer/portable bundle
→ desktop shortcut
→ startup health
→ safe update guard
→ backup/restore
→ rollback kit
→ offline recovery kit
→ package evidence
```

Belangrijk: packaging en updates mogen nooit live trading automatisch starten. Een installer, shortcut, update of restore mag geen live session armeren, geen live order plaatsen en geen secrets tonen. Live blijft volledig onder Roadmap 117-121 gates.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 122`, `122-roadmap`, `Production-Grade Local Packaging`, `Installer`, `Desktop Shortcut`, `Offline Recovery Kit` en `Auto-Update Guard`.
* \[x] Geen bestaande Roadmap 122 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 121 is lokaal aangemaakt als Live Operations Runbook Automation, Incident Response, Rollback Drills \& Post-Trade Forensics.

### Codebasecontrole

Breed bekeken met focus op packaging, dependency management, launcher, CLI, check-all, dashboard startup, operator artifacts en safety:

* \[x] `pyproject.toml`
* \[x] `src/binance\_spot\_bot/launcher.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/config.py`
* \[x] `src/binance\_spot\_bot/session\_store.py`
* \[x] `src/binance\_spot\_bot/audit.py`
* \[x] roadmaplijn 104-121.

### Belangrijke conclusies uit de codebase

* \[x] `pyproject.toml` heeft projectnaam, versie `0.1.0`, Python `>=3.12`, optionele dependency-groepen `research`, `dev`, `ui`, `visual`, `realtime`, `mlops` en een `spot-bot` console script.
* \[x] Core dependencies staan leeg en veel dependencies zijn optioneel; packaging moet dus expliciet kiezen welke extras in welke package zitten.
* \[x] `launcher.py` vindt een vrije lokale poort en bouwt nu een Streamlit dashboard command voor `127.0.0.1`-achtige lokale dashboardstart.
* \[x] `cli.py` bevat al veel operationele commands, waaronder config validation, preflight, support bundle, local ops, dashboard launch/control center, sessions, demo execution en check-all.
* \[x] `check\_all.py` forceert veilige env tijdens checks: `PYTHONPATH=src`, `LIVE\_TRADING\_ENABLED=false`, `KILL\_SWITCH=true`.
* \[x] `SessionStore` en `AuditLog` geven basis voor backup/restore/evidence en secret redaction.
* \[x] Roadmap 116-121 plannen app-control, live-training, live-trading, governance en live-ops modules, die allemaal mee moeten in package/installer checks.

### Belangrijkste gat na Roadmap 121

Na Roadmap 121 is de bot functioneel en operationeel veilig, maar nog niet “gewoon als app” te beheren:

* \[ ] Geen productieklare lokale installer.
* \[ ] Geen portable bundle.
* \[ ] Geen dependency lock per profile/extras.
* \[ ] Geen offline install cache.
* \[ ] Geen desktop shortcut lifecycle.
* \[ ] Geen startmenu shortcut.
* \[ ] Geen app version manifest.
* \[ ] Geen package integrity manifest.
* \[ ] Geen safe update guard.
* \[ ] Geen rollback naar vorige versie.
* \[ ] Geen offline recovery kit.
* \[ ] Geen backup/restore wizard voor profiles, evidence, sessions en data.
* \[ ] Geen migration planner voor profile/data/schema changes.
* \[ ] Geen package evidence bundle.
* \[ ] Geen release smoke die de one-click flow end-to-end test.

Roadmap 122 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 122

Maak een betrouwbare lokale desktop distributie:

```text
source repo
→ dependency lock
→ package manifest
→ local installer/portable bundle
→ desktop shortcut
→ startup health
→ safe update guard
→ backup/rollback/recovery kit
→ package evidence
```

Na Roadmap 122 moet de gebruiker:

* \[ ] de bot lokaal kunnen installeren of portable draaien;
* \[ ] één desktop shortcut kunnen gebruiken;
* \[ ] automatisch de juiste venv/dependencies kunnen laten klaarzetten;
* \[ ] Dashboard V2/Control Center kunnen openen;
* \[ ] profiles, secrets refs, sessions, evidence en data kunnen back-uppen;
* \[ ] veilig kunnen updaten zonder live auto-start;
* \[ ] terug kunnen rollen naar vorige versie;
* \[ ] offline kunnen herstellen na mislukte update;
* \[ ] support/evidence bundle kunnen exporteren;
* \[ ] zeker weten dat installer/updater nooit live orders uitvoert.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen Dashboard V2 foundation opnieuw bouwen.
* \[ ] Geen one-click app logic opnieuw bouwen.
* \[ ] Geen live trading gates opnieuw bouwen.
* \[ ] Geen Strategy/Portfolio/Live Ops opnieuw bouwen.
* \[ ] Geen installer die secrets opslaat.
* \[ ] Geen updater die live sessions start.
* \[ ] Geen update tijdens armed live session.
* \[ ] Geen rollback die live profile automatisch armt.
* \[ ] Geen cloud auto-update.
* \[ ] Geen remote telemetry.
* \[ ] Geen packaging die check-all safety env omzeilt.
* \[ ] Geen raw API keys in package/evidence/logs.
* \[ ] Geen live order routes in installer/update/recovery tools.

Wel doen:

* \[ ] package schema;
* \[ ] dependency lock;
* \[ ] local installer;
* \[ ] portable bundle;
* \[ ] desktop/startmenu shortcuts;
* \[ ] startup health;
* \[ ] update guard;
* \[ ] backup/restore;
* \[ ] rollback;
* \[ ] offline recovery kit;
* \[ ] package evidence;
* \[ ] release smoke tests.

\---

## 3\. Fase 0 - Packaging Safety Contract

Nieuw docbestand:

```text
docs/packaging/packaging-safety-contract.md
```

Regels:

* \[ ] Installer mag nooit live session starten.
* \[ ] Installer mag nooit live order placement uitvoeren.
* \[ ] Updater mag nooit live session starten.
* \[ ] Updater mag nooit actief updaten tijdens armed/running live session.
* \[ ] Rollback mag nooit live session automatisch armeren.
* \[ ] Desktop shortcut opent alleen launcher/control center.
* \[ ] Default environment blijft veilig:

  * `LIVE\_TRADING\_ENABLED=false`
  * `KILL\_SWITCH=true`
* \[ ] Secrets worden nooit in package bundle ingebakken.
* \[ ] Secrets worden nooit in logs/evidence getoond.
* \[ ] Backup/restore gebruikt secret references, niet raw secrets.
* \[ ] Package evidence is secret-free.
* \[ ] Offline recovery kit bevat geen raw API keys.
* \[ ] Geen remote telemetry.
* \[ ] Geen financial advice.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen installer/updater/rollback geen order endpoints kunnen aanroepen.
* \[ ] Tests bewijzen live sessions update blokkeren.
* \[ ] Tests bewijzen secrets niet in package/evidence zitten.
* \[ ] Tests bewijzen safe env defaults aanwezig zijn.

\---

## 4\. Fase 1 - Package Profile Matrix

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/package\_profiles.py
```

Package profiles:

### `minimal-operator`

* \[ ] Core bot.
* \[ ] CLI.
* \[ ] Control Center.
* \[ ] Dashboard V2 static/app shell.
* \[ ] No research dependencies.
* \[ ] No Playwright.

### `dashboard-full`

* \[ ] Core bot.
* \[ ] Dashboard V2.
* \[ ] UI dependencies.
* \[ ] Browser smoke support optional.

### `research-local`

* \[ ] Core bot.
* \[ ] Research dependencies.
* \[ ] ML/data dependencies.
* \[ ] Dataset tooling.

### `live-ops-safe`

* \[ ] Core bot.
* \[ ] Dashboard V2.
* \[ ] Live ops/governance modules.
* \[ ] No auto-live.
* \[ ] Strong safety checks.

### `developer`

* \[ ] All extras.
* \[ ] Tests.
* \[ ] Ruff.
* \[ ] Playwright optional.

Dataclasses:

* \[ ] `PackageProfile`
* \[ ] `PackageDependencyGroup`
* \[ ] `PackageProfileValidationResult`
* \[ ] `PackageProfileReport`

Acceptatiecriteria:

* \[ ] Package profiles are JSON-serializable.
* \[ ] Profiles map to pyproject extras.
* \[ ] Invalid extras fail.
* \[ ] Live package still safe by default.
* \[ ] Tests cover profile matrix.

\---

## 5\. Fase 2 - Dependency Lock \& Offline Wheelhouse Plan

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/dependency\_lock.py
```

Doel:

* \[ ] lock dependencies per package profile;
* \[ ] generate requirements lock;
* \[ ] prepare offline wheelhouse manifest;
* \[ ] hash every wheel;
* \[ ] record Python version;
* \[ ] record platform;
* \[ ] detect missing wheels;
* \[ ] detect unsafe/unpinned dependencies;
* \[ ] support local-only install.

Outputs:

```text
dist/package-locks/
  minimal-operator.lock
  dashboard-full.lock
  research-local.lock
  live-ops-safe.lock
  developer.lock

dist/wheelhouse-manifest.json
```

Acceptatiecriteria:

* \[ ] Lock manifest generated.
* \[ ] Wheelhouse manifest generated.
* \[ ] Missing wheel becomes blocker.
* \[ ] Hash mismatch blocks install.
* \[ ] Tests use fixture manifests.

\---

## 6\. Fase 3 - Application Version \& Build Manifest

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/build\_manifest.py
```

Manifest fields:

* \[ ] app\_name;
* \[ ] package\_version;
* \[ ] source\_git\_ref;
* \[ ] build\_time\_ms;
* \[ ] package\_profile;
* \[ ] python\_version;
* \[ ] platform;
* \[ ] dependency\_lock\_hash;
* \[ ] wheelhouse\_hash;
* \[ ] dashboard\_build\_hash;
* \[ ] package\_files\_hashes;
* \[ ] docs\_hashes;
* \[ ] check\_all\_result;
* \[ ] browser\_smoke\_result;
* \[ ] safe\_env\_defaults;
* \[ ] live\_trading\_enabled\_default=false;
* \[ ] kill\_switch\_default=true;
* \[ ] secret\_scan\_status;
* \[ ] no\_live\_auto\_start\_statement.

Acceptatiecriteria:

* \[ ] Build manifest deterministic where possible.
* \[ ] Manifest includes hashes.
* \[ ] Missing check-all blocks release package.
* \[ ] Secret scan failure blocks package.
* \[ ] Tests cover manifest validation.

\---

## 7\. Fase 4 - Portable App Bundle Builder

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/portable\_bundle.py
```

Portable bundle layout:

```text
Neural-Binance-Spot-Bot/
  app/
  src/
  dashboard/
  docs/
  scripts/
  data-template/
  dist-info/
  Start-Neural-Binance-Bot.cmd
  Start-Neural-Binance-Bot.ps1
  Stop-Neural-Binance-Bot.cmd
  Open-Dashboard.cmd
  README-START-HERE.md
  package-manifest.json
```

Rules:

* \[ ] Do not include raw secrets.
* \[ ] Do not include user data by default.
* \[ ] Include sample `.env.template`.
* \[ ] Include safe default env.
* \[ ] Include recovery scripts.
* \[ ] Include offline docs.
* \[ ] Include package evidence.
* \[ ] No live auto-start.

Acceptatiecriteria:

* \[ ] Portable bundle builds in temp dir.
* \[ ] Manifest validates.
* \[ ] No secrets included.
* \[ ] Start script points to local app.
* \[ ] Tests cover bundle contents.

\---

## 8\. Fase 5 - Windows Installer / Setup Script

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/windows\_installer.py
```

Installer approach:

* \[ ] script-based installer first;
* \[ ] no admin by default;
* \[ ] install under user directory;
* \[ ] create desktop shortcut;
* \[ ] create start menu shortcut optional;
* \[ ] create app data directory;
* \[ ] copy package files;
* \[ ] create safe `.env.local` template;
* \[ ] run startup health;
* \[ ] open dashboard optional;
* \[ ] write install manifest;
* \[ ] no live start.

Generated scripts:

```text
Install-Neural-Binance-Bot.ps1
Uninstall-Neural-Binance-Bot.ps1
Repair-Neural-Binance-Bot.ps1
Create-Desktop-Shortcut.ps1
```

Acceptatiecriteria:

* \[ ] Installer dry-run works.
* \[ ] Installer writes manifest.
* \[ ] Shortcut target validated.
* \[ ] Uninstaller preserves user data by default.
* \[ ] Tests verify scripts are safe text.

\---

## 9\. Fase 6 - Desktop Shortcut Lifecycle

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/shortcuts.py
```

Shortcut types:

* \[ ] desktop start shortcut;
* \[ ] start menu shortcut;
* \[ ] dashboard shortcut;
* \[ ] safe mode shortcut;
* \[ ] repair shortcut;
* \[ ] recovery shortcut.

Shortcut rules:

* \[ ] shortcut never passes live arm flags;
* \[ ] shortcut never passes API keys;
* \[ ] shortcut starts launcher/control center only;
* \[ ] shortcut uses app install path;
* \[ ] shortcut has clear icon/name;
* \[ ] shortcut validation command.

Acceptatiecriteria:

* \[ ] Shortcut specs generated.
* \[ ] Dangerous args blocked.
* \[ ] Shortcut repair works.
* \[ ] Tests cover generated targets.
* \[ ] Docs include shortcut troubleshooting.

\---

## 10\. Fase 7 - Startup Health for Installed App

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/installed\_startup\_health.py
```

Checks:

* \[ ] install manifest exists;
* \[ ] Python/venv available;
* \[ ] package import works;
* \[ ] dependency lock matches;
* \[ ] dashboard assets exist;
* \[ ] app data dir writable;
* \[ ] profile store accessible;
* \[ ] secret refs status fingerprint only;
* \[ ] ports available;
* \[ ] safe env defaults;
* \[ ] no armed live session from previous run;
* \[ ] no stale lock file;
* \[ ] recovery kit present.

Recovery suggestions:

* \[ ] repair venv;
* \[ ] recreate shortcut;
* \[ ] restore config backup;
* \[ ] rollback previous version;
* \[ ] open safe mode dashboard;
* \[ ] export support bundle.

Acceptatiecriteria:

* \[ ] Startup health reports helpful blockers.
* \[ ] Safe mode available.
* \[ ] Secrets redacted.
* \[ ] No live auto-resume.
* \[ ] Tests cover failure modes.

\---

## 11\. Fase 8 - Safe Update Guard

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/update\_guard.py
```

Update preconditions:

* \[ ] no running live session;
* \[ ] no armed live profile;
* \[ ] no active order lifecycle;
* \[ ] no unreconciled order;
* \[ ] latest session closed or disarmed;
* \[ ] backup created;
* \[ ] package manifest verified;
* \[ ] dependency lock verified;
* \[ ] migrations previewed;
* \[ ] rollback point created;
* \[ ] operator confirm for update.

Update blocks:

* \[ ] active live session;
* \[ ] emergency incident open;
* \[ ] evidence export in progress;
* \[ ] secret scan failure;
* \[ ] package hash mismatch;
* \[ ] failed check-all package smoke;
* \[ ] migration unsafe.

Acceptatiecriteria:

* \[ ] Update blocked during active live session.
* \[ ] Update blocked on hash mismatch.
* \[ ] Rollback point required.
* \[ ] Update plan is JSON + Markdown.
* \[ ] Tests cover blockers.

\---

## 12\. Fase 9 - Versioned Data/Profile Migration Planner

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/migration\_planner.py
```

Migration targets:

* \[ ] profiles;
* \[ ] profile templates;
* \[ ] app-control data;
* \[ ] dashboard workspace data;
* \[ ] extension packs;
* \[ ] live-training evidence;
* \[ ] live-trading evidence;
* \[ ] live-ops incidents;
* \[ ] session store;
* \[ ] support bundles;
* \[ ] package manifests.

Migration modes:

* \[ ] preview;
* \[ ] dry-run;
* \[ ] apply;
* \[ ] rollback.

Rules:

* \[ ] backup before apply;
* \[ ] no migration during live session;
* \[ ] no secret material in migration report;
* \[ ] unknown schema blocks;
* \[ ] dry-run required before apply.

Acceptatiecriteria:

* \[ ] Migration preview works.
* \[ ] Unknown schema blocks.
* \[ ] Backup required.
* \[ ] Rollback available.
* \[ ] Tests use fixture data dirs.

\---

## 13\. Fase 10 - Backup \& Restore Manager

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/backup\_restore.py
```

Backup scopes:

* \[ ] profiles;
* \[ ] profile templates;
* \[ ] secret references, not raw secrets;
* \[ ] dashboard workspaces;
* \[ ] sessions;
* \[ ] evidence;
* \[ ] live training data manifests;
* \[ ] live trading session evidence;
* \[ ] live ops incident evidence;
* \[ ] local settings;
* \[ ] logs, redacted.

Restore modes:

* \[ ] preview;
* \[ ] restore profiles only;
* \[ ] restore workspaces only;
* \[ ] restore evidence only;
* \[ ] full safe restore;
* \[ ] recovery mode restore.

Rules:

* \[ ] no raw secrets.
* \[ ] restore never arms live.
* \[ ] restore invalidates live arm tokens.
* \[ ] restore forces live locked.
* \[ ] restore writes audit record.
* \[ ] restore creates pre-restore backup.

Acceptatiecriteria:

* \[ ] Backup archive created.
* \[ ] Restore preview works.
* \[ ] Restore forces live locked.
* \[ ] Secret redaction passes.
* \[ ] Tests use temp dirs.

\---

## 14\. Fase 11 - Rollback Manager

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/rollback\_manager.py
```

Rollback points:

* \[ ] before update;
* \[ ] before migration;
* \[ ] before profile lifecycle change;
* \[ ] before package repair;
* \[ ] manual snapshot.

Rollback contents:

* \[ ] package manifest;
* \[ ] dependency lock;
* \[ ] app files hash manifest;
* \[ ] data backup refs;
* \[ ] migration state;
* \[ ] restore instructions;
* \[ ] safety state.

Rules:

* \[ ] rollback never starts live.
* \[ ] rollback locks live profiles.
* \[ ] rollback invalidates arm tokens.
* \[ ] rollback writes evidence.
* \[ ] rollback verifies hashes.

Acceptatiecriteria:

* \[ ] Rollback point created.
* \[ ] Rollback preview works.
* \[ ] Rollback locks live state.
* \[ ] Hash verification works.
* \[ ] Tests cover failed rollback.

\---

## 15\. Fase 12 - Offline Recovery Kit

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/offline\_recovery\_kit.py
```

Kit layout:

```text
recovery-kit/
  README-RECOVERY.md
  safe-mode-start.cmd
  repair-shortcuts.ps1
  verify-package.cmd
  restore-backup.cmd
  rollback.cmd
  export-support-bundle.cmd
  offline-docs/
  manifests/
```

Capabilities:

* \[ ] start safe mode dashboard;
* \[ ] verify package manifest;
* \[ ] repair shortcuts;
* \[ ] restore latest backup;
* \[ ] rollback previous version;
* \[ ] export support bundle;
* \[ ] run redaction self-test;
* \[ ] open troubleshooting docs.

Rules:

* \[ ] no live start.
* \[ ] no live arm.
* \[ ] no order execution.
* \[ ] safe env defaults.
* \[ ] secret-free kit.

Acceptatiecriteria:

* \[ ] Kit generated.
* \[ ] Kit verifies package.
* \[ ] Safe mode script has safe env.
* \[ ] No secrets included.
* \[ ] Tests inspect script contents.

\---

## 16\. Fase 13 - Safe Mode

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/safe\_mode.py
```

Safe mode behavior:

* \[ ] dashboard opens in read-only/safe mode;
* \[ ] live profiles locked;
* \[ ] no runtime auto-start;
* \[ ] no order endpoints;
* \[ ] only diagnostics, restore, backup, docs, evidence;
* \[ ] clear banner;
* \[ ] export support bundle;
* \[ ] repair shortcuts;
* \[ ] run startup health;
* \[ ] run package verification.

Acceptatiecriteria:

* \[ ] Safe mode starts without API keys.
* \[ ] Safe mode cannot start bot runtime.
* \[ ] Safe mode cannot arm live.
* \[ ] Safe mode shows recovery tools.
* \[ ] Browser smoke covers safe mode.

\---

## 17\. Fase 14 - Package Verification \& Integrity CLI

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/package\_verify.py
```

Checks:

* \[ ] package manifest exists;
* \[ ] file hashes match;
* \[ ] dependency lock matches;
* \[ ] wheelhouse hash matches;
* \[ ] dashboard assets hash match;
* \[ ] docs hash match;
* \[ ] no forbidden files;
* \[ ] no raw secrets;
* \[ ] safe env scripts;
* \[ ] launcher scripts safe;
* \[ ] rollback kit present.

Acceptatiecriteria:

* \[ ] Verify passes on fixture package.
* \[ ] Hash mismatch fails.
* \[ ] Secret finding fails.
* \[ ] Dangerous launcher arg fails.
* \[ ] Report JSON + Markdown.

\---

## 18\. Fase 15 - Installer/Package Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/packaging/package\_evidence.py
```

Bundle bevat:

* \[ ] packaging safety contract;
* \[ ] package profile report;
* \[ ] dependency lock report;
* \[ ] wheelhouse manifest;
* \[ ] build manifest;
* \[ ] portable bundle report;
* \[ ] installer dry-run report;
* \[ ] shortcut validation report;
* \[ ] startup health report;
* \[ ] update guard report;
* \[ ] migration planner report;
* \[ ] backup/restore report;
* \[ ] rollback report;
* \[ ] recovery kit report;
* \[ ] safe mode report;
* \[ ] package verification report;
* \[ ] check-all output;
* \[ ] browser smoke output;
* \[ ] secret redaction proof;
* \[ ] no live auto-start proof;
* \[ ] hashes.

Output:

```text
dist/evidence/package\_evidence\_manifest.json
dist/evidence/package\_evidence\_summary.md
```

Acceptatiecriteria:

* \[ ] Evidence secret-free.
* \[ ] Evidence has manifest/hash.
* \[ ] Evidence can be verified.
* \[ ] Evidence required before release package.
* \[ ] Dashboard/CLI can open evidence.

\---

## 19\. Fase 16 - Packaging CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli package-profiles --json
python -m binance\_spot\_bot.cli package-lock --profile dashboard-full --json
python -m binance\_spot\_bot.cli package-build-manifest --profile dashboard-full --json
python -m binance\_spot\_bot.cli package-portable-build --profile dashboard-full
python -m binance\_spot\_bot.cli package-installer-build --profile dashboard-full
python -m binance\_spot\_bot.cli package-shortcuts-create --dry-run
python -m binance\_spot\_bot.cli package-startup-health --json
python -m binance\_spot\_bot.cli package-update-plan --from <old> --to <new> --json
python -m binance\_spot\_bot.cli package-migration-preview --json
python -m binance\_spot\_bot.cli package-backup-create --json
python -m binance\_spot\_bot.cli package-restore-preview --backup <path> --json
python -m binance\_spot\_bot.cli package-rollback-preview --rollback-point <id> --json
python -m binance\_spot\_bot.cli package-recovery-kit-build
python -m binance\_spot\_bot.cli package-safe-mode-start
python -m binance\_spot\_bot.cli package-verify --path <package> --json
python -m binance\_spot\_bot.cli package-evidence-export
```

Acceptatiecriteria:

* \[ ] Commands work locally.
* \[ ] Commands support JSON where relevant.
* \[ ] Commands never start live.
* \[ ] Commands never expose secrets.
* \[ ] Dangerous actions require confirm.

\---

## 20\. Fase 17 - Dashboard V2 Package \& Recovery Center

Nieuwe routes/pages:

```text
/package
/package/profiles
/package/installer
/package/startup-health
/package/update
/package/backup-restore
/package/rollback
/package/recovery-kit
/package/safe-mode
/package/evidence
```

Panels:

* \[ ] installed app status;
* \[ ] package version;
* \[ ] package profile;
* \[ ] dependency lock status;
* \[ ] startup health;
* \[ ] shortcut status;
* \[ ] update eligibility;
* \[ ] active live blocker;
* \[ ] backup status;
* \[ ] restore preview;
* \[ ] rollback points;
* \[ ] recovery kit status;
* \[ ] safe mode status;
* \[ ] package evidence export.

UX rules:

* \[ ] update blocked if live session active;
* \[ ] restore warns and locks live;
* \[ ] rollback locks live;
* \[ ] secrets never shown;
* \[ ] emergency/support links visible.

Acceptatiecriteria:

* \[ ] Package Center loads.
* \[ ] Startup health visible.
* \[ ] Backup/restore preview visible.
* \[ ] Update blocked state visible.
* \[ ] Browser smoke covers package center.

\---

## 21\. Fase 18 - Check-All Packaging Profile

Fast profile:

* \[ ] package module imports;
* \[ ] package profile validation;
* \[ ] build manifest fixture;
* \[ ] launcher script safety;
* \[ ] shortcut safety;
* \[ ] secret redaction;
* \[ ] safe env defaults.

Deep profile:

* \[ ] build portable fixture package;
* \[ ] verify package;
* \[ ] create backup fixture;
* \[ ] restore preview fixture;
* \[ ] rollback preview fixture;
* \[ ] recovery kit fixture;
* \[ ] safe mode browser smoke;
* \[ ] package evidence export/verify.

Acceptatiecriteria:

* \[ ] Fast check-all remains safe.
* \[ ] Deep package profile validates package end-to-end.
* \[ ] Secret leak hard fails.
* \[ ] Live auto-start hard fails.
* \[ ] Hash mismatch hard fails.

\---

## 22\. Fase 19 - UAT / Operator Workflow

UAT scenarios:

* \[ ] build portable package;
* \[ ] install in temp/local user dir;
* \[ ] create desktop shortcut;
* \[ ] launch app from shortcut;
* \[ ] dashboard opens;
* \[ ] startup health passes;
* \[ ] create backup;
* \[ ] run restore preview;
* \[ ] run update plan dry-run;
* \[ ] block update during fake active live session;
* \[ ] create rollback point;
* \[ ] run rollback preview;
* \[ ] start safe mode;
* \[ ] build offline recovery kit;
* \[ ] export package evidence.

Acceptatiecriteria:

* \[ ] UAT confirms one-click installed start works.
* \[ ] UAT confirms no live auto-start.
* \[ ] UAT confirms update blocked during live session.
* \[ ] UAT confirms backup/restore locks live.
* \[ ] UAT evidence attached.

\---

## 23\. Fase 20 - Release / Knowledge / Test / Performance Integration

Roadmap 089:

* \[ ] release notes include package profile and installer.
* \[ ] version manifest includes package manifest hash.
* \[ ] migration notes include backup/rollback requirements.

Roadmap 091:

* \[ ] knowledge graph maps package profile → dependencies → launcher → dashboard → data dir → recovery.
* \[ ] impact analysis detects packaging risk from pyproject/CLI/launcher/check-all changes.

Roadmap 092:

* \[ ] test selector chooses packaging tests for pyproject/launcher/cli/check-all/installer changes.
* \[ ] dashboard package center changes select browser smoke.

Roadmap 093:

* \[ ] package build time budget;
* \[ ] installer startup time budget;
* \[ ] dashboard open time budget;
* \[ ] backup/restore time budget;
* \[ ] package size budget.

Acceptatiecriteria:

* \[ ] Release evidence includes package evidence.
* \[ ] Knowledge graph updated.
* \[ ] Test selector protects package flow.
* \[ ] Performance reports include package budgets.
* \[ ] No live auto-start.

\---

## 24\. Fase 21 - Scheduled Packaging Health Reports

Scheduled jobs:

* \[ ] daily startup health check.
* \[ ] daily shortcut validation.
* \[ ] weekly package verification.
* \[ ] weekly backup dry-run.
* \[ ] weekly restore preview.
* \[ ] weekly recovery kit validation.
* \[ ] weekly safe mode smoke.
* \[ ] monthly package evidence export.

Metrics:

* \[ ] installed package version;
* \[ ] startup health status;
* \[ ] shortcut status;
* \[ ] dependency lock status;
* \[ ] backup status;
* \[ ] rollback point count;
* \[ ] recovery kit status;
* \[ ] package verification status;
* \[ ] package size;
* \[ ] no live auto-start proof.

Acceptatiecriteria:

* \[ ] Jobs never start live.
* \[ ] Reports secret-free.
* \[ ] Dashboard shows reports.
* \[ ] Check-all safe env preserved.

\---

## 25\. Tests

### Unit tests

* \[ ] `tests/test\_packaging\_safety\_contract.py`
* \[ ] `tests/test\_package\_profiles.py`
* \[ ] `tests/test\_dependency\_lock.py`
* \[ ] `tests/test\_build\_manifest.py`
* \[ ] `tests/test\_portable\_bundle.py`
* \[ ] `tests/test\_windows\_installer.py`
* \[ ] `tests/test\_shortcuts.py`
* \[ ] `tests/test\_installed\_startup\_health.py`
* \[ ] `tests/test\_update\_guard.py`
* \[ ] `tests/test\_migration\_planner.py`
* \[ ] `tests/test\_backup\_restore.py`
* \[ ] `tests/test\_rollback\_manager.py`
* \[ ] `tests/test\_offline\_recovery\_kit.py`
* \[ ] `tests/test\_safe\_mode.py`
* \[ ] `tests/test\_package\_verify.py`
* \[ ] `tests/test\_package\_evidence.py`

### Integration tests

* \[ ] Build package profile fixture.
* \[ ] Generate dependency lock fixture.
* \[ ] Generate build manifest.
* \[ ] Build portable bundle fixture.
* \[ ] Generate installer scripts.
* \[ ] Validate shortcuts.
* \[ ] Run startup health fixture.
* \[ ] Block update during fake live session.
* \[ ] Create backup.
* \[ ] Restore preview.
* \[ ] Rollback preview.
* \[ ] Build recovery kit.
* \[ ] Verify package.
* \[ ] Export evidence.

### Browser smoke

* \[ ] `/package` loads.
* \[ ] package status visible.
* \[ ] startup health visible.
* \[ ] update guard visible.
* \[ ] backup/restore visible.
* \[ ] rollback visible.
* \[ ] recovery kit visible.
* \[ ] safe mode visible.
* \[ ] evidence export visible.
* \[ ] no live start button visible.

### Safety tests

* \[ ] Installer never calls order endpoints.
* \[ ] Updater never calls order endpoints.
* \[ ] Rollback never calls order endpoints.
* \[ ] Recovery kit never starts live.
* \[ ] Update blocked during active live session.
* \[ ] Restore locks live profiles.
* \[ ] Rollback locks live profiles.
* \[ ] Secrets redacted from package/evidence.
* \[ ] Launcher scripts contain safe env defaults.
* \[ ] Check-all safe env preserved.

\---

## 26\. Docs

Nieuwe docs:

```text
docs/packaging/packaging-safety-contract.md
docs/packaging/package-profiles.md
docs/packaging/dependency-lock.md
docs/packaging/build-manifest.md
docs/packaging/portable-bundle.md
docs/packaging/windows-installer.md
docs/packaging/desktop-shortcuts.md
docs/packaging/startup-health.md
docs/packaging/safe-update-guard.md
docs/packaging/migration-planner.md
docs/packaging/backup-restore.md
docs/packaging/rollback-manager.md
docs/packaging/offline-recovery-kit.md
docs/packaging/safe-mode.md
docs/packaging/package-verification.md
docs/packaging/package-evidence.md
docs/packaging/dashboard-package-center.md
```

README updates:

* \[ ] Install locally.
* \[ ] Portable mode.
* \[ ] Desktop shortcut.
* \[ ] First start.
* \[ ] Update safely.
* \[ ] Backup/restore.
* \[ ] Rollback.
* \[ ] Offline recovery.
* \[ ] Safe mode.
* \[ ] No live auto-start statement.

\---

## 27\. Codex bouwvolgorde

### PR 1 - Safety Contract + Package Profile Matrix

* \[ ] `docs/packaging/packaging-safety-contract.md`
* \[ ] `packaging/package\_profiles.py`
* \[ ] package profile tests.
* \[ ] no-live/no-secret tests.

### PR 2 - Dependency Lock + Build Manifest

* \[ ] `dependency\_lock.py`
* \[ ] `build\_manifest.py`
* \[ ] lock/manifest tests.

### PR 3 - Portable Bundle Builder

* \[ ] `portable\_bundle.py`
* \[ ] bundle layout.
* \[ ] bundle content tests.

### PR 4 - Windows Installer + Shortcuts

* \[ ] `windows\_installer.py`
* \[ ] `shortcuts.py`
* \[ ] script safety tests.

### PR 5 - Startup Health + Safe Mode

* \[ ] `installed\_startup\_health.py`
* \[ ] `safe\_mode.py`
* \[ ] health/safe-mode tests.

### PR 6 - Update Guard + Migration Planner

* \[ ] `update\_guard.py`
* \[ ] `migration\_planner.py`
* \[ ] update/migration tests.

### PR 7 - Backup/Restore + Rollback

* \[ ] `backup\_restore.py`
* \[ ] `rollback\_manager.py`
* \[ ] backup/rollback tests.

### PR 8 - Offline Recovery Kit + Package Verification

* \[ ] `offline\_recovery\_kit.py`
* \[ ] `package\_verify.py`
* \[ ] recovery/verify tests.

### PR 9 - Package Evidence + CLI + Check-All

* \[ ] `package\_evidence.py`
* \[ ] CLI commands.
* \[ ] check-all packaging profile.

### PR 10 - Dashboard Package Center + Docs + UAT + Integrations

* \[ ] Dashboard routes/pages.
* \[ ] browser smoke.
* \[ ] docs.
* \[ ] UAT scenarios.
* \[ ] release/knowledge/test/performance integration.
* \[ ] scheduled reports.

\---

## 28\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 122 PR 1: Packaging Safety Contract + Package Profile Matrix.

Maak docs/packaging/packaging-safety-contract.md.

Maak src/binance\_spot\_bot/packaging/\_\_init\_\_.py.
Maak src/binance\_spot\_bot/packaging/package\_profiles.py met:
- PackageProfile
- PackageDependencyGroup
- PackageProfileValidationResult
- PackageProfileReport
- default\_package\_profiles()
- validate\_package\_profile(profile: PackageProfile)
- package\_profile\_report\_to\_dict(...)
- write\_package\_profile\_report(...)

Package profiles minimaal:
- minimal-operator
- dashboard-full
- research-local
- live-ops-safe
- developer

Elke PackageProfile moet minimaal bevatten:
- profile\_id
- name
- description
- extras
- include\_dashboard
- include\_research
- include\_visual\_smoke
- include\_live\_ops
- include\_dev\_tools
- safe\_env\_defaults
- forbidden\_runtime\_actions
- no\_live\_auto\_start\_statement
- secret\_free\_package\_statement

Validatie moet blokkeren op:
- unknown extras
- missing safe env defaults
- LIVE\_TRADING\_ENABLED niet false als default
- KILL\_SWITCH niet true als default
- forbidden\_runtime\_actions ontbreekt
- package profile die live auto-start toestaat
- package profile die order endpoints toestaat
- raw secret-like values
- buy/sell/profit guarantee wording

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
- all default profiles validate
- unknown extra blocked
- missing safe env blocked
- live auto-start blocked
- order endpoint action blocked
- secret-like values worden geredact
- JSON serialization
- no\_live\_auto\_start\_statement aanwezig
- secret\_free\_package\_statement aanwezig
```

Waarom eerst:

* Packaging moet eerst bepalen welke app-profielen bestaan en welke dependencies/features erin mogen.
* Dit is read-only en raakt runtime/trading/frontend niet.
* Het beschermt meteen tegen live auto-start en secret leaks in packages.
* Daarna kunnen dependency lock, portable bundle, installer en recovery kit veilig op deze profile matrix bouwen.

\---

## 29\. Definition of Done

Roadmap 122 is klaar als:

* \[ ] Packaging Safety Contract bestaat.
* \[ ] Package Profile Matrix werkt.
* \[ ] Dependency Lock \& Offline Wheelhouse Plan werkt.
* \[ ] Application Version \& Build Manifest werkt.
* \[ ] Portable App Bundle Builder werkt.
* \[ ] Windows Installer / Setup Script werkt.
* \[ ] Desktop Shortcut Lifecycle werkt.
* \[ ] Startup Health for Installed App werkt.
* \[ ] Safe Update Guard werkt.
* \[ ] Versioned Data/Profile Migration Planner werkt.
* \[ ] Backup \& Restore Manager werkt.
* \[ ] Rollback Manager werkt.
* \[ ] Offline Recovery Kit werkt.
* \[ ] Safe Mode werkt.
* \[ ] Package Verification \& Integrity CLI werkt.
* \[ ] Installer/Package Evidence Bundle werkt.
* \[ ] Packaging CLI commands werken.
* \[ ] Dashboard V2 Package \& Recovery Center werkt.
* \[ ] Check-All Packaging Profile werkt.
* \[ ] UAT/Operator Workflow werkt.
* \[ ] Release/Knowledge/Test/Performance integration werkt.
* \[ ] Scheduled Packaging Health Reports werken.
* \[ ] Tests bewijzen installer/updater/rollback nooit orders plaatsen.
* \[ ] Tests bewijzen update active live session blokkeert.
* \[ ] Tests bewijzen restore/rollback live locked forceert.
* \[ ] Tests bewijzen package/evidence secret-free is.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Roadmap 122 kan na uitvoering naar `Voltooid docs`.

\---

## 30\. Verwachte Roadmap 123 daarna

Als Roadmap 122 groen is:

```text
Roadmap 123 - Local App Settings, User Onboarding Wizard, First-Run Setup \& Operator Training Mode
```

Mogelijke inhoud:

* \[ ] first-run onboarding;
* \[ ] guided setup;
* \[ ] API key safety education;
* \[ ] demo mode tutorial;
* \[ ] paper/live locked explanation;
* \[ ] operator training scenarios;
* \[ ] still no live auto-start.

```

Als Roadmap 122 package blockers vindt:

```text
Roadmap 123 - Packaging Blocker Burn-Down, Installer Reliability, Dependency Lock Cleanup \& Recovery Kit Hardening
```

Mogelijke inhoud:

* \[ ] dependency lock issues oplossen;
* \[ ] installer path issues oplossen;
* \[ ] shortcut reliability verbeteren;
* \[ ] recovery kit gaps oplossen;
* \[ ] safe update blockers verbeteren;
* \[ ] live blijft locked.

```

