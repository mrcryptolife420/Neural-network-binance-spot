# Roadmap 088 - Offline Disaster Recovery, Backup/Restore Drills \& Local State Integrity

Status: Niet volledig voltooid / opnieuw gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/088-roadmap-offline-disaster-recovery-backup-restore-drills-local-state-integrity.md
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

Doel: Roadmap 087 maakt local permissions, operator roles, separation of duties en compliance reports sterker. Roadmap 088 zorgt dat de volledige lokale state daarna veilig kan worden beschermd: offline backups, restore previews, disaster recovery drills, state integrity checks, corrupt-data recovery, permission/audit restore validatie, evidence continuity en recovery runbooks.

Live trading blijft volledig buiten scope. Disaster recovery mag nooit live trading activeren, signed endpoints gebruiken of real account data herstellen.

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
* \[x] Geen bestaande Roadmap 088 gevonden via repo-search.
* \[x] Roadmap 087 is lokaal aangemaakt voor Local Permission Profiles, Operator Roles Hardening \& Audit-Grade Compliance Reports.

### Codebasecontrole

Gecontroleerde relevante modules:

* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] `src/binance\_spot\_bot/support\_bundle.py`
* \[x] `src/binance\_spot\_bot/security.py`
* \[x] `src/binance\_spot\_bot/redaction.py`

Bestaande basis:

* \[x] `operator\_ops.py` bevat al:

  * `retention\_preview`;
  * `create\_state\_archive`;
  * `support\_bundle\_restore\_preview`;
  * `artifact\_catalog`;
  * `evidence\_chain`;
  * `data\_growth\_budget`;
  * `report\_index`;
  * `verify\_support\_bundles`;
  * `redaction\_self\_test`;
  * `local\_ops\_snapshot`;
  * `operator\_quality\_gate`;
  * `operator\_command\_manifest`;
  * `incident\_timeline`.
* \[x] `create\_state\_archive(...)` bestaat al als preview-only archive met `retention-preview.json` en `archive-manifest.json`.
* \[x] `support\_bundle\_restore\_preview(...)` kan support bundle inhoud inspecteren zonder extractie.
* \[x] `support\_bundle.py` kan redacted support bundles maken en verifiëren met manifest/hashes.
* \[x] `security.py` en `redaction.py` bieden secret scanning/redaction.
* \[x] Operator outputs bevatten `live\_trading\_enabled=False`.

### Belangrijkste gat na Roadmap 087

Na Roadmap 087 zijn permissions/compliance sterker, maar de lokale state kan nog steeds kwetsbaar zijn voor:

* \[ ] schijfcorruptie;
* \[ ] per ongeluk verwijderde data;
* \[ ] kapotte JSON manifests;
* \[ ] ontbrekende evidence;
* \[ ] stale/corrupt permission profiles;
* \[ ] kapotte decision journals;
* \[ ] onvolledige support bundles;
* \[ ] restore zonder integriteitscontrole;
* \[ ] backup met secrets;
* \[ ] backup zonder no-live bewijs;
* \[ ] ongeteste disaster recovery procedure.

Roadmap 088 maakt herstel daarom testbaar, reproduceerbaar en veilig.

\---

## 1\. Hoofddoel Roadmap 088

Maak een lokale disaster recovery-laag:

```text
Local state
→ backup profile
→ pre-backup checks
→ redacted backup package
→ manifest/hash/signature-like chain
→ restore preview
→ sandbox restore drill
→ integrity verification
→ recovery report
→ evidence continuity
```

Na Roadmap 088 moet de bot kunnen:

* \[ ] offline backup packages maken;
* \[ ] backup profiles gebruiken;
* \[ ] state integrity controleren;
* \[ ] restore preview uitvoeren zonder bestanden te overschrijven;
* \[ ] sandbox restore drill draaien;
* \[ ] corrupt data detecteren;
* \[ ] permission/audit/evidence continuity controleren;
* \[ ] disaster recovery reports exporteren;
* \[ ] recovery runbooks tonen;
* \[ ] backup/restore nooit live trading laten activeren.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen cloud backup.
* \[ ] Geen remote upload.
* \[ ] Geen secrets opslaan in backups.
* \[ ] Geen automatische destructive restore.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen Binance account endpoints.
* \[ ] Geen real-money state.
* \[ ] Geen externe backup service verplicht maken.
* \[ ] Geen restore die bestaande data overschrijft zonder preview + confirm.
* \[ ] Geen encryption-key management als grote enterprise feature in deze roadmap.

Wel doen:

* \[ ] lokale offline backup packages maken;
* \[ ] restore preview uitbreiden;
* \[ ] state integrity manifests maken;
* \[ ] sandbox restore drills toevoegen;
* \[ ] corrupt data recovery plannen;
* \[ ] permission/compliance/evidence continuity checken;
* \[ ] dashboard/CLI toevoegen;
* \[ ] alles redacted, local-only en no-live houden.

\---

## 3\. Fase 0 - Disaster Recovery Safety Contract

Doel: vastleggen dat backup/restore veilig, lokaal en no-live blijft.

### Nieuwe doc

```text
docs/offline-disaster-recovery-safety-contract.md
```

### Regels

* \[ ] Backup is local-only.
* \[ ] Geen remote upload.
* \[ ] Geen secrets in backup.
* \[ ] Geen `.env`, `.pem`, `.key` of raw credentials.
* \[ ] Restore is standaard preview-only.
* \[ ] Restore naar sandbox is toegestaan.
* \[ ] Restore naar live data dir vereist exact confirm phrase.
* \[ ] Restore mag nooit live trading activeren.
* \[ ] Restore mag geen signed/order/account endpoints triggeren.
* \[ ] Backups bevatten no-live proof.
* \[ ] Backups bevatten redaction proof.
* \[ ] Backups bevatten manifest/hashes.
* \[ ] Corrupt backups worden geweigerd.
* \[ ] Permission/compliance state krijgt extra validatie.

### Acceptatiecriteria

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen dat secrets niet in backup komen.
* \[ ] Tests bewijzen restore default preview-only is.
* \[ ] Tests bewijzen live mode niet via restore kan ontstaan.
* \[ ] Dashboard toont `OFFLINE DR ONLY`.

\---

## 4\. Fase 1 - Backup Profile Schema

Doel: verschillende soorten backups declaratief vastleggen.

### Nieuwe module

```text
src/binance\_spot\_bot/backup\_profiles.py
```

### Dataclasses

* \[ ] `BackupProfile`
* \[ ] `BackupIncludeRule`
* \[ ] `BackupExcludeRule`
* \[ ] `BackupProfileValidation`
* \[ ] `BackupProfileManifest`

### Default profiles

#### `minimal\_ops`

Bevat:

* \[ ] settings-redacted;
* \[ ] diagnostics;
* \[ ] local ops snapshot;
* \[ ] operator reports;
* \[ ] evidence manifest;
* \[ ] permission/compliance manifests.

#### `paper\_ops\_full`

Bevat:

* \[ ] alles uit `minimal\_ops`;
* \[ ] paper session reports;
* \[ ] portfolio reports;
* \[ ] strategy/policy metadata;
* \[ ] metrics aggregates;
* \[ ] action center journal;
* \[ ] governance reports.

#### `audit\_evidence`

Bevat:

* \[ ] evidence manifests;
* \[ ] compliance reports;
* \[ ] decision journals;
* \[ ] support bundle verify reports;
* \[ ] redaction self-test;
* \[ ] secret scan result;
* \[ ] no-live proof.

#### `restore\_drill\_fixture`

Bevat:

* \[ ] kleine fixture subset;
* \[ ] fake paper state;
* \[ ] fake reports;
* \[ ] no secrets;
* \[ ] deterministic test data.

### Exclusions

Altijd uitsluiten:

* \[ ] `.env`;
* \[ ] `\*.pem`;
* \[ ] `\*.key`;
* \[ ] raw credential files;
* \[ ] cache met secrets;
* \[ ] user-specific OS secrets;
* \[ ] arbitrary external files.

### Acceptatiecriteria

* \[ ] Profiles zijn JSON-serializable.
* \[ ] Default profiles zijn veilig.
* \[ ] Exclusion rules winnen altijd van include rules.
* \[ ] Profile validation blokkeert unsafe paths.
* \[ ] Tests dekken profiles.

\---

## 5\. Fase 2 - State Inventory \& Integrity Manifest

Doel: exact weten welke lokale state bestaat en of die intact is.

### Nieuwe module

```text
src/binance\_spot\_bot/state\_inventory.py
```

### Inventory categories

* \[ ] config redacted;
* \[ ] checks;
* \[ ] evidence;
* \[ ] reports;
* \[ ] support bundles;
* \[ ] sessions;
* \[ ] pilot-runs;
* \[ ] public data cache manifests;
* \[ ] metrics;
* \[ ] local jobs;
* \[ ] runbooks;
* \[ ] AI ops sessions;
* \[ ] action center;
* \[ ] permissions;
* \[ ] compliance;
* \[ ] portfolio policies;
* \[ ] deployments;
* \[ ] backups.

### Manifest fields

* \[ ] path;
* \[ ] category;
* \[ ] suffix;
* \[ ] size\_bytes;
* \[ ] modified\_at;
* \[ ] sha256;
* \[ ] redacted;
* \[ ] required;
* \[ ] stale;
* \[ ] include\_eligible;
* \[ ] restore\_priority.

### Acceptatiecriteria

* \[ ] Inventory werkt offline.
* \[ ] Manifest bevat hashes.
* \[ ] Unsafe paths worden gemarkeerd.
* \[ ] Missing required state geeft warning/blocker.
* \[ ] Manifest is secret-free.

\---

## 6\. Fase 3 - Pre-Backup Checks

Doel: backup alleen maken als lokale state veilig genoeg is.

### Nieuwe module

```text
src/binance\_spot\_bot/backup\_preflight.py
```

### Checks

* \[ ] redaction self-test;
* \[ ] secret scan;
* \[ ] evidence manifest verify;
* \[ ] support bundle verify;
* \[ ] permission drift check;
* \[ ] compliance score;
* \[ ] action journal integrity;
* \[ ] metrics manifest verify;
* \[ ] report index available;
* \[ ] data growth budget;
* \[ ] no-live proof;
* \[ ] write permission check;
* \[ ] disk space estimate.

### Statussen

* \[ ] ok;
* \[ ] warn;
* \[ ] blocked;
* \[ ] failed.

### Acceptatiecriteria

* \[ ] Backup blocks on secret scan finding.
* \[ ] Backup warns on stale evidence.
* \[ ] Backup blocks if no-live proof missing.
* \[ ] Backup estimates output size.
* \[ ] Preflight report is exportable.

\---

## 7\. Fase 4 - Offline Backup Package Builder

Doel: redacted backup zip maken met manifest/hashes.

### Nieuwe module

```text
src/binance\_spot\_bot/offline\_backup.py
```

### Output

```text
data/backups/<backup\_id>/
  backup.zip
  backup\_manifest.json
  backup\_summary.md
  preflight\_report.json
  inventory\_manifest.json
  no\_live\_proof.json
  redaction\_proof.json
```

### Backup package inhoud

* \[ ] selected files per profile;
* \[ ] manifest.json;
* \[ ] inventory manifest;
* \[ ] preflight report;
* \[ ] redaction proof;
* \[ ] no-live proof;
* \[ ] restore instructions;
* \[ ] backup summary.

### Builder rules

* \[ ] Redact text/json before writing.
* \[ ] Store relative paths.
* \[ ] Include SHA256 per file.
* \[ ] Include backup profile hash.
* \[ ] Include project version info.
* \[ ] Include created\_at timestamp.
* \[ ] Include source data\_dir fingerprint.
* \[ ] No secrets.
* \[ ] No external upload.

### Acceptatiecriteria

* \[ ] Backup package verifies after creation.
* \[ ] Backup contains no secrets.
* \[ ] Backup manifest has hashes.
* \[ ] Backup can be inspected without extraction.
* \[ ] Tests use temp dirs.

\---

## 8\. Fase 5 - Backup Verification

Doel: backup achteraf kunnen controleren.

### Nieuwe module

```text
src/binance\_spot\_bot/backup\_verification.py
```

### Checks

* \[ ] zip readable;
* \[ ] manifest present;
* \[ ] all files present;
* \[ ] file hashes match;
* \[ ] redaction proof present;
* \[ ] no-live proof present;
* \[ ] forbidden files absent;
* \[ ] permission/compliance manifests valid;
* \[ ] evidence chain continuity;
* \[ ] restore instructions present.

### Output

* \[ ] `backup\_verify\_report.json`
* \[ ] `backup\_verify\_report.md`

### Acceptatiecriteria

* \[ ] Corrupt zip fails verification.
* \[ ] Missing file fails verification.
* \[ ] Hash mismatch fails verification.
* \[ ] Forbidden file fails verification.
* \[ ] Verification report is secret-free.

\---

## 9\. Fase 6 - Restore Preview V2

Doel: restore volledig simuleren zonder te overschrijven.

### Nieuwe module

```text
src/binance\_spot\_bot/restore\_preview.py
```

### Preview checks

* \[ ] backup readable;
* \[ ] manifest valid;
* \[ ] target data\_dir exists/empty/non-empty;
* \[ ] files to create;
* \[ ] files to overwrite;
* \[ ] files to skip;
* \[ ] conflicts;
* \[ ] incompatible paths;
* \[ ] version mismatch;
* \[ ] permission profile changes;
* \[ ] compliance state changes;
* \[ ] evidence chain continuity;
* \[ ] no-live proof;
* \[ ] secrets scan on extracted preview content.

### Output

```text
data/backups/restore-previews/<preview\_id>/
  restore\_preview.json
  restore\_preview.md
  conflict\_report.json
```

### Acceptatiecriteria

* \[ ] Preview never writes to target.
* \[ ] Preview detects conflicts.
* \[ ] Preview detects forbidden files.
* \[ ] Preview shows exact changes.
* \[ ] Restore cannot proceed without successful preview.

\---

## 10\. Fase 7 - Sandbox Restore Drill

Doel: backup in veilige sandbox herstellen en testen.

### Nieuwe module

```text
src/binance\_spot\_bot/restore\_drill.py
```

### Drill flow

* \[ ] create temp sandbox data dir;
* \[ ] extract backup into sandbox;
* \[ ] verify manifest;
* \[ ] run redaction self-test;
* \[ ] run secret scan;
* \[ ] run evidence manifest verify;
* \[ ] run permission drift check;
* \[ ] run compliance score;
* \[ ] run local ops snapshot;
* \[ ] run dashboard smoke in safe mode if possible;
* \[ ] compare original backup manifest vs restored state;
* \[ ] generate drill report;
* \[ ] clean sandbox unless keep flag.

### Acceptatiecriteria

* \[ ] Drill runs offline.
* \[ ] Drill uses no API keys.
* \[ ] Drill uses no signed endpoints.
* \[ ] Drill proves restore viability.
* \[ ] Drill report is evidence-linked.

\---

## 11\. Fase 8 - Controlled Restore Executor

Doel: echte restore alleen gecontroleerd, confirm-gated en rollback-aware.

### Nieuwe module

```text
src/binance\_spot\_bot/restore\_executor.py
```

### Restore modes

* \[ ] preview-only default;
* \[ ] sandbox restore;
* \[ ] partial restore to new directory;
* \[ ] controlled restore to data\_dir with confirm;
* \[ ] dry-run with conflict report.

### Guardrails

* \[ ] Requires successful restore preview.
* \[ ] Requires backup verification.
* \[ ] Requires exact confirm phrase.
* \[ ] Creates pre-restore snapshot.
* \[ ] Never restores forbidden files.
* \[ ] Never restores live-enabled config.
* \[ ] Writes restore journal.
* \[ ] Runs post-restore verification.
* \[ ] Supports rollback to pre-restore snapshot.

### Acceptatiecriteria

* \[ ] Restore cannot run without preview.
* \[ ] Restore cannot restore forbidden files.
* \[ ] Restore cannot enable live.
* \[ ] Restore creates pre-restore snapshot.
* \[ ] Restore journal is append-only.

\---

## 12\. Fase 9 - Corrupt Data Detection \& Repair Plans

Doel: kapotte lokale state detecteren en herstelplan maken.

### Nieuwe module

```text
src/binance\_spot\_bot/state\_integrity.py
```

### Checks

* \[ ] invalid JSON;
* \[ ] missing required manifests;
* \[ ] hash mismatch;
* \[ ] truncated JSONL;
* \[ ] missing evidence files;
* \[ ] stale report index;
* \[ ] broken support bundle;
* \[ ] corrupt metrics warehouse;
* \[ ] broken permission profile;
* \[ ] broken action journal;
* \[ ] broken compliance bundle;
* \[ ] inconsistent session report;
* \[ ] duplicate IDs;
* \[ ] path escape attempt.

### Repair plan types

* \[ ] rebuild index;
* \[ ] rebuild manifest;
* \[ ] quarantine corrupt file;
* \[ ] restore from backup;
* \[ ] regenerate report;
* \[ ] re-run evidence chain;
* \[ ] re-run redaction;
* \[ ] manual review required.

### Acceptatiecriteria

* \[ ] Integrity checker is read-only by default.
* \[ ] Repair plan does not auto-delete.
* \[ ] Quarantine requires confirm.
* \[ ] Repair reports are dashboard-ready.
* \[ ] Tests include corrupt fixture files.

\---

## 13\. Fase 10 - Permission/Audit Restore Validation

Doel: na restore checken dat permissions en audit trail nog betrouwbaar zijn.

### Nieuwe module

```text
src/binance\_spot\_bot/permission\_restore\_validation.py
```

### Checks

* \[ ] operator identities exist;
* \[ ] disabled operators remain disabled;
* \[ ] forbidden scopes absent;
* \[ ] permission profile hashes match;
* \[ ] role templates valid;
* \[ ] action journal present;
* \[ ] decision journal hash chain valid;
* \[ ] compliance report present;
* \[ ] permission drift ok;
* \[ ] no-live proof present.

### Acceptatiecriteria

* \[ ] Restore fails if forbidden scope appears.
* \[ ] Restore warns if journal missing.
* \[ ] Restore blocks if live-enabled state appears.
* \[ ] Validation report links to compliance evidence.
* \[ ] Tests use restored fixture.

\---

## 14\. Fase 11 - Evidence Continuity Validation

Doel: bewijzen dat evidence vóór en na restore klopt.

### Nieuwe module

```text
src/binance\_spot\_bot/evidence\_continuity.py
```

### Checks

* \[ ] evidence manifest present;
* \[ ] evidence chain valid;
* \[ ] latest evidence IDs preserved;
* \[ ] compliance evidence preserved;
* \[ ] action audit evidence preserved;
* \[ ] support bundle verification preserved;
* \[ ] metrics evidence preserved;
* \[ ] backup manifest links to evidence;
* \[ ] restored evidence hashes match backup.

### Acceptatiecriteria

* \[ ] Evidence continuity report generated.
* \[ ] Hash mismatch fails continuity.
* \[ ] Missing non-critical evidence warns.
* \[ ] Missing critical evidence blocks restore approval.
* \[ ] Dashboard can show continuity status.

\---

## 15\. Fase 12 - Disaster Recovery Runbooks

Doel: operator heeft duidelijke herstelprocedures.

### Nieuwe docs/runbooks

```text
docs/runbooks/disaster-recovery/
```

Runbooks:

* \[ ] `backup-before-maintenance.md`
* \[ ] `restore-preview.md`
* \[ ] `sandbox-restore-drill.md`
* \[ ] `corrupt-json-recovery.md`
* \[ ] `corrupt-metrics-recovery.md`
* \[ ] `permission-profile-restore.md`
* \[ ] `evidence-chain-rebuild.md`
* \[ ] `support-bundle-restore-preview.md`
* \[ ] `data-dir-migration.md`
* \[ ] `full-local-drill.md`

### Acceptatiecriteria

* \[ ] Runbooks have step-by-step commands.
* \[ ] Runbooks include safety warnings.
* \[ ] Runbooks include expected outputs.
* \[ ] Runbooks include done criteria.
* \[ ] Runbooks are linked in dashboard.

\---

## 16\. Fase 13 - Backup/Restore Dashboard Panel

Doel: disaster recovery bedienen zonder raw JSON.

### Nieuwe dashboardsectie

```text
Disaster Recovery
```

### Panels

* \[ ] backup profiles;
* \[ ] latest backup status;
* \[ ] backup preflight;
* \[ ] backup package list;
* \[ ] backup verification status;
* \[ ] restore preview;
* \[ ] restore conflicts;
* \[ ] sandbox restore drills;
* \[ ] state integrity;
* \[ ] permission restore validation;
* \[ ] evidence continuity;
* \[ ] DR runbooks;
* \[ ] no-live proof.

### Actions

* \[ ] run pre-backup checks;
* \[ ] create backup;
* \[ ] verify backup;
* \[ ] run restore preview;
* \[ ] run sandbox restore drill;
* \[ ] generate repair plan;
* \[ ] export DR report;
* \[ ] open DR runbook.

### Safeguards

* \[ ] Real restore hidden behind expert mode.
* \[ ] Real restore requires exact confirm phrase.
* \[ ] No live controls.
* \[ ] Raw JSON only in debug expanders.
* \[ ] All buttons/forms have stable keys.

### Acceptatiecriteria

* \[ ] Dashboard shows `OFFLINE DR ONLY`.
* \[ ] Browser smoke covers panel.
* \[ ] Restore preview cannot overwrite files.
* \[ ] Dashboard cannot enable live.
* \[ ] Dashboard reports are secret-free.

\---

## 17\. Fase 14 - Backup/Restore CLI

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli backup-profiles
python -m binance\_spot\_bot.cli state-inventory
python -m binance\_spot\_bot.cli backup-preflight --profile paper\_ops\_full
python -m binance\_spot\_bot.cli backup-create --profile paper\_ops\_full
python -m binance\_spot\_bot.cli backup-verify --backup-id <id>
python -m binance\_spot\_bot.cli restore-preview --backup-id <id> --target data-restored-preview
python -m binance\_spot\_bot.cli restore-drill --backup-id <id>
python -m binance\_spot\_bot.cli state-integrity-check
python -m binance\_spot\_bot.cli repair-plan --from-integrity-report <id>
python -m binance\_spot\_bot.cli permission-restore-validate --backup-id <id>
python -m binance\_spot\_bot.cli evidence-continuity-check --backup-id <id>
python -m binance\_spot\_bot.cli dr-report --backup-id <id>
```

Controlled restore command:

```powershell
python -m binance\_spot\_bot.cli restore-execute --backup-id <id> --target <path> --confirm RESTORE\_OFFLINE\_STATE
```

### Acceptatiecriteria

* \[ ] CLI works offline.
* \[ ] CLI requires no API keys.
* \[ ] Real restore requires confirm.
* \[ ] Commands reject live/signed/account routes.
* \[ ] JSON output supported.
* \[ ] Reports are secret-free.

\---

## 18\. Fase 15 - Disaster Recovery Reports

Doel: alle DR acties auditbaar rapporteren.

### Nieuwe module

```text
src/binance\_spot\_bot/disaster\_recovery\_report.py
```

### Reports

```text
data/disaster-recovery/
  backups/
  restore-previews/
  drills/
  integrity/
  reports/
```

Report types:

* \[ ] backup preflight report;
* \[ ] backup summary;
* \[ ] backup verification report;
* \[ ] restore preview report;
* \[ ] sandbox restore drill report;
* \[ ] state integrity report;
* \[ ] repair plan report;
* \[ ] permission restore validation report;
* \[ ] evidence continuity report;
* \[ ] final DR report.

### Acceptatiecriteria

* \[ ] Reports are Markdown + JSON.
* \[ ] Reports include no-live proof.
* \[ ] Reports include redaction proof.
* \[ ] Reports link to manifests/hashes.
* \[ ] Reports are dashboard-downloadable.

\---

## 19\. Fase 16 - Scheduled Backup \& DR Drills Integration

Doel: Roadmap 083 scheduler gebruiken voor veilige DR routines.

### Scheduled jobs

* \[ ] daily state inventory;
* \[ ] daily integrity check;
* \[ ] weekly backup preflight;
* \[ ] weekly minimal ops backup;
* \[ ] weekly backup verification;
* \[ ] monthly sandbox restore drill;
* \[ ] monthly DR report;
* \[ ] post-permission-change backup;
* \[ ] pre-maintenance backup.

### Guardrails

* \[ ] Scheduled backup uses safe profile.
* \[ ] Scheduled backup never restores.
* \[ ] Scheduled restore drill only uses sandbox.
* \[ ] Failed DR job creates support bundle.
* \[ ] No remote upload.
* \[ ] No secrets in scheduled job args.

### Acceptatiecriteria

* \[ ] Scheduler jobs are allowlisted.
* \[ ] Jobs are local-only.
* \[ ] Failed job creates support bundle if configured.
* \[ ] Dashboard shows last DR job.
* \[ ] No live trading.

\---

## 20\. Fase 17 - DR Evidence Bundle

Doel: één bundel voor disaster recovery bewijs.

### Nieuwe module

```text
src/binance\_spot\_bot/dr\_evidence\_bundle.py
```

### Bundle bevat

* \[ ] backup profile;
* \[ ] inventory manifest;
* \[ ] preflight report;
* \[ ] backup manifest;
* \[ ] backup verification;
* \[ ] restore preview;
* \[ ] restore drill report;
* \[ ] state integrity report;
* \[ ] permission restore validation;
* \[ ] evidence continuity report;
* \[ ] redaction self-test;
* \[ ] secret scan result;
* \[ ] no-live proof;
* \[ ] hashes.

### Output

```text
data/disaster-recovery/evidence/<bundle\_id>/
  dr\_evidence\_manifest.json
  dr\_evidence\_summary.md
  files/
```

### Acceptatiecriteria

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Dashboard/CLI export works.
* \[ ] Bundle supports audit/compliance.

\---

## 21\. Fase 18 - Data Directory Migration Preview

Doel: project veilig naar nieuwe lokale data directory kunnen verplaatsen.

### Nieuwe module

```text
src/binance\_spot\_bot/data\_dir\_migration.py
```

### Flow

* \[ ] source data\_dir inventory;
* \[ ] target path validation;
* \[ ] migration preview;
* \[ ] path conflict detection;
* \[ ] permission check;
* \[ ] backup before migration;
* \[ ] sandbox restore to target;
* \[ ] post-migration verify;
* \[ ] rollback plan.

### Acceptatiecriteria

* \[ ] Migration is preview-first.
* \[ ] Target outside allowed local paths warns/blocks.
* \[ ] Backup required before migration.
* \[ ] No secrets in migration report.
* \[ ] No live mode.

\---

## 22\. Fase 19 - Tests

### Unit tests

* \[ ] `tests/test\_backup\_profiles.py`
* \[ ] `tests/test\_state\_inventory.py`
* \[ ] `tests/test\_backup\_preflight.py`
* \[ ] `tests/test\_offline\_backup.py`
* \[ ] `tests/test\_backup\_verification.py`
* \[ ] `tests/test\_restore\_preview.py`
* \[ ] `tests/test\_restore\_drill.py`
* \[ ] `tests/test\_restore\_executor.py`
* \[ ] `tests/test\_state\_integrity.py`
* \[ ] `tests/test\_permission\_restore\_validation.py`
* \[ ] `tests/test\_evidence\_continuity.py`
* \[ ] `tests/test\_disaster\_recovery\_report.py`
* \[ ] `tests/test\_dr\_evidence\_bundle.py`
* \[ ] `tests/test\_data\_dir\_migration.py`

### Integration tests

* \[ ] Create fixture data dir.
* \[ ] Build state inventory.
* \[ ] Run backup preflight.
* \[ ] Create backup.
* \[ ] Verify backup.
* \[ ] Run restore preview.
* \[ ] Run sandbox restore drill.
* \[ ] Corrupt one JSON file and detect it.
* \[ ] Validate permission restore.
* \[ ] Validate evidence continuity.
* \[ ] Export DR evidence bundle.

### Safety tests

* \[ ] Backup excludes `.env`.
* \[ ] Backup excludes `\*.pem` and `\*.key`.
* \[ ] Backup excludes raw secrets.
* \[ ] Restore cannot enable live.
* \[ ] Restore cannot write outside target.
* \[ ] Restore requires preview.
* \[ ] Restore requires confirm.
* \[ ] Backup/restore uses no signed endpoints.
* \[ ] Backup/restore uses no account endpoints.
* \[ ] Reports are secret-free.
* \[ ] No-live proof remains true.

\---

## 23\. Docs

Nieuwe docs:

* \[ ] `docs/offline-disaster-recovery-safety-contract.md`
* \[ ] `docs/backup-profiles.md`
* \[ ] `docs/state-inventory-integrity-manifest.md`
* \[ ] `docs/backup-preflight.md`
* \[ ] `docs/offline-backup-package.md`
* \[ ] `docs/backup-verification.md`
* \[ ] `docs/restore-preview-v2.md`
* \[ ] `docs/sandbox-restore-drill.md`
* \[ ] `docs/controlled-restore-executor.md`
* \[ ] `docs/state-integrity-checks.md`
* \[ ] `docs/permission-audit-restore-validation.md`
* \[ ] `docs/evidence-continuity-validation.md`
* \[ ] `docs/disaster-recovery-dashboard.md`
* \[ ] `docs/disaster-recovery-cli.md`
* \[ ] `docs/dr-evidence-bundle.md`
* \[ ] `docs/data-dir-migration-preview.md`

README updates:

* \[ ] backup commands;
* \[ ] restore preview commands;
* \[ ] sandbox drill commands;
* \[ ] disaster recovery workflow;
* \[ ] no-live statement;
* \[ ] secret exclusion rules.

\---

## 24\. Codex bouwvolgorde

### PR 1 - Backup Profiles + State Inventory

* \[ ] `backup\_profiles.py`
* \[ ] `state\_inventory.py`
* \[ ] safe include/exclude rules
* \[ ] tests.

### PR 2 - Backup Preflight

* \[ ] `backup\_preflight.py`
* \[ ] redaction/secret/no-live checks
* \[ ] tests.

### PR 3 - Offline Backup Builder

* \[ ] `offline\_backup.py`
* \[ ] backup zip + manifest
* \[ ] tests.

### PR 4 - Backup Verification

* \[ ] `backup\_verification.py`
* \[ ] corrupt/missing/hash mismatch tests.

### PR 5 - Restore Preview V2

* \[ ] `restore\_preview.py`
* \[ ] conflict reports
* \[ ] preview-only guarantee
* \[ ] tests.

### PR 6 - Sandbox Restore Drill

* \[ ] `restore\_drill.py`
* \[ ] temp data dir restore
* \[ ] integrity checks
* \[ ] tests.

### PR 7 - Controlled Restore Executor

* \[ ] `restore\_executor.py`
* \[ ] confirm gate
* \[ ] pre-restore snapshot
* \[ ] post-restore verify
* \[ ] tests.

### PR 8 - State Integrity + Repair Plans

* \[ ] `state\_integrity.py`
* \[ ] repair plan reports
* \[ ] corrupt fixtures.

### PR 9 - Permission/Evidence Continuity

* \[ ] permission restore validation
* \[ ] evidence continuity
* \[ ] tests.

### PR 10 - Dashboard + CLI + DR Evidence Bundle + Docs

* \[ ] dashboard panel;
* \[ ] CLI commands;
* \[ ] DR evidence bundle;
* \[ ] runbooks;
* \[ ] browser smoke.

\---

## 25\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 088 PR 1: Backup Profiles + State Inventory.

Maak src/binance\_spot\_bot/backup\_profiles.py met:
- BackupProfile
- BackupIncludeRule
- BackupExcludeRule
- BackupProfileValidation
- BackupProfileManifest

Maak src/binance\_spot\_bot/state\_inventory.py met:
- inventory van lokale data\_dir categorieën checks/evidence/reports/support/sessions/pilot-runs/metrics/permissions/compliance/action-center
- sha256 per bestand
- size/modified/category/suffix
- include\_eligible
- restore\_priority
- redacted flag

Voeg default backup profiles toe:
- minimal\_ops
- paper\_ops\_full
- audit\_evidence
- restore\_drill\_fixture

Altijd uitsluiten:
- .env
- \*.pem
- \*.key
- raw credential files
- path traversal/outside data\_dir

Gebruik bestaande redact\_payload/redact\_text waar nodig.
Voeg tests toe voor:
- profile serialization
- unsafe path rejected
- forbidden suffix excluded
- inventory hash stable
- no secrets in inventory output
- live\_trading\_enabled=False

Geen backup zip builder in deze PR.
Geen restore executor in deze PR.
Geen API calls.
Geen signed endpoints.
Geen orders.
Geen live trading.
```

Waarom eerst:

* Backup profiles en state inventory zijn de fundering voor elke backup/restore flow.
* Het bouwt direct voort op bestaande `artifact\_catalog`, `retention\_preview` en support bundle manifesten.
* Het raakt geen trading runtime.
* Het is klein genoeg voor Codex.
* Secret/no-live safety kan meteen getest worden.

\---

## 26\. Definition of Done

Roadmap 088 is klaar als:

* \[ ] Disaster Recovery Safety Contract bestaat.
* \[ ] Backup Profile Schema werkt.
* \[ ] State Inventory \& Integrity Manifest werkt.
* \[ ] Pre-Backup Checks werken.
* \[ ] Offline Backup Package Builder werkt.
* \[ ] Backup Verification werkt.
* \[ ] Restore Preview V2 werkt.
* \[ ] Sandbox Restore Drill werkt.
* \[ ] Controlled Restore Executor werkt.
* \[ ] Corrupt Data Detection \& Repair Plans werken.
* \[ ] Permission/Audit Restore Validation werkt.
* \[ ] Evidence Continuity Validation werkt.
* \[ ] Disaster Recovery Runbooks bestaan.
* \[ ] Backup/Restore Dashboard Panel werkt.
* \[ ] Backup/Restore CLI werkt.
* \[ ] Disaster Recovery Reports werken.
* \[ ] Scheduled Backup \& DR Drills Integration werkt.
* \[ ] DR Evidence Bundle werkt.
* \[ ] Data Directory Migration Preview werkt.
* \[ ] Tests bewijzen geen secrets in backups.
* \[ ] Tests bewijzen restore kan live niet activeren.
* \[ ] Tests bewijzen geen signed/account/order endpoints.
* \[ ] Reports/bundles zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 088 kan na uitvoering naar `Voltooid docs`.

\---

## 27\. Verwachte Roadmap 089 daarna

Na Roadmap 088 zou Roadmap 089 logisch focussen op:

```text
Roadmap 089 - Local Release Management, Versioned Upgrade Paths \& Migration Safety
```

Mogelijke inhoud:

* \[ ] versioned local releases;
* \[ ] migration plans;
* \[ ] pre-upgrade backup requirement;
* \[ ] downgrade safety;
* \[ ] schema migrations;
* \[ ] release notes generator;
* \[ ] upgrade smoke tests;
* \[ ] still no live trading.



---

## Afwerking

Status: Niet volledig voltooid / opnieuw gepland op 2026-05-11.

Implementatie/evidence: docs/roadmap-076-102-execution-evidence.md, src/binance_spot_bot/paper_os.py, 	ests/test_roadmaps_076_102_paper_os.py.

Validatie: gerichte tests groen, volledige pytest groen, check-all opnieuw uitgevoerd na verplaatsing.



---

## Correctie-audit 2026-05-11

Deze roadmap is teruggezet naar Roadmap docs/ omdat de eerdere markering als Voltooid te breed was. De huidige code bevat alleen een gedeelde foundation in src/binance_spot_bot/paper_os.py en regressietests in 	ests/test_roadmaps_076_102_paper_os.py. Niet alle checklistpunten uit deze roadmap zijn volledig als production-grade feature geimplementeerd.

Open status: opnieuw plannen, opdelen in kleinere uitvoerbare taken, en pas opnieuw naar Voltooid docs/ verplaatsen na concrete implementatie en validatie per roadmap.

---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: backup profiles, state inventory, backup preflight, offline backup package, backup verification, restore preview, restore drill, restore executor guard, state integrity, permission restore validation, evidence continuity, disaster recovery report, DR evidence bundle, data-dir migration preview, dashboardtab `Disaster Recovery`, CLI smoke via `disaster-recovery-drill`.

Validatie: `tests/test_roadmaps_083_088_full_surface.py`, `tests/test_roadmaps_082_088_ops_governance.py`, dashboard-smoke en CLI smoke.

Safety: offline/local-only, forbidden secret files excluded from backup, restore preview-first, no live trading.

---

## Finale afwerking 2026-05-12

Status: Voltooid en verplaatsbaar naar `Voltooid docs/`.

Gebouwd en herbouwd zonder facade-only implementatie:

* `src/binance_spot_bot/backup_profiles.py`
* `src/binance_spot_bot/state_inventory.py`
* `src/binance_spot_bot/backup_preflight.py`
* `src/binance_spot_bot/offline_backup.py`
* `src/binance_spot_bot/backup_verification.py`
* `src/binance_spot_bot/restore_preview.py`
* `src/binance_spot_bot/restore_drill.py`
* `src/binance_spot_bot/restore_executor.py`
* `src/binance_spot_bot/state_integrity.py`
* `src/binance_spot_bot/permission_restore_validation.py`
* `src/binance_spot_bot/evidence_continuity.py`
* `src/binance_spot_bot/disaster_recovery_report.py`
* `src/binance_spot_bot/dr_evidence_bundle.py`
* `src/binance_spot_bot/data_dir_migration.py`
* `src/binance_spot_bot/disaster_recovery_drills.py`
* `src/binance_spot_bot/ui/streamlit_app.py` Disaster Recovery panel
* `src/binance_spot_bot/cli.py` backup/restore/DR CLI
* `tests/test_roadmap_088_disaster_recovery_acceptance.py`

Docs en runbooks toegevoegd:

* `docs/offline-disaster-recovery-safety-contract.md`
* `docs/backup-profiles.md`
* `docs/state-inventory-integrity-manifest.md`
* `docs/backup-preflight.md`
* `docs/offline-backup-package.md`
* `docs/backup-verification.md`
* `docs/restore-preview-v2.md`
* `docs/sandbox-restore-drill.md`
* `docs/controlled-restore-executor.md`
* `docs/state-integrity-checks.md`
* `docs/permission-audit-restore-validation.md`
* `docs/evidence-continuity-validation.md`
* `docs/disaster-recovery-dashboard.md`
* `docs/disaster-recovery-cli.md`
* `docs/dr-evidence-bundle.md`
* `docs/data-dir-migration-preview.md`
* `docs/runbooks/disaster-recovery/*.md`

Validatie uitgevoerd:

* `python -m pytest tests/test_roadmap_088_disaster_recovery_acceptance.py tests/test_roadmaps_083_088_full_surface.py tests/test_roadmaps_082_088_ops_governance.py -q` -> groen.
* Backup/restore CLI flow: profiles, inventory, preflight, create, verify, preview, drill, integrity, repair plan, permission restore validation, evidence continuity, DR report, DR evidence bundle -> groen.
* `python -m binance_spot_bot.cli check-all --skip-tests --json` -> groen.
* `python -m pytest -q` -> `327 passed, 1 warning`.
* `python -m binance_spot_bot.cli dashboard-smoke --seconds 1` -> groen.
* `python -m binance_spot_bot.cli dashboard-browser-smoke --url http://127.0.0.1:8506/ --seconds 10` -> groen.

Safety evidence:

* Backup profiles sluiten lokale credential/sleutelbestanden uit.
* Restore is preview-first en controlled restore vereist `RESTORE_OFFLINE_STATE`.
* Restore schrijft niet buiten target en herstelt geen forbidden files.
* Backup verification, restore preview, restore drill, permission restore validation en evidence continuity zijn offline.
* Public-data manifest hashes zijn ingekort om token-achtige false positives in secret scan te voorkomen.
* `live_trading_enabled=false` blijft expliciet in outputs.

