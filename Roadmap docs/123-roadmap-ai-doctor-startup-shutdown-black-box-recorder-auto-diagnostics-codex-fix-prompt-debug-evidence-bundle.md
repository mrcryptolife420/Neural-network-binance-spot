# Roadmap 123 - AI Doctor, Startup/Shutdown Black Box Recorder, Auto-Diagnostics, Codex Fix Prompt Generator & Debug Evidence Bundle

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-13  
Voorgestelde locatie:

```text
Roadmap docs/123-roadmap-ai-doctor-startup-shutdown-black-box-recorder-auto-diagnostics-codex-fix-prompt-debug-evidence-bundle.md
```

## Samenvatting

Deze roadmap bouwt een **AI Doctor** voor de volledige app/codebase. Het doel is dat de bot bij start, runtime, crash en shutdown automatisch alle nuttige informatie verzamelt, samenvat en omzet naar een AI-interpreteerbaar debugpakket voor ChatGPT/Codex.

Gewenste eindflow:

```text
Start bot/dashboard
→ AI Doctor start snapshot
→ runtime/dashboard/log/error recorder draait mee
→ bij stop/crash/fout: finish snapshot
→ diagnostics + check-all + evidence + logs + stacktraces + git/codebase context
→ known issue matcher
→ AI summary
→ Codex fix prompt
→ downloadbaar ai_doctor_bundle.zip
```

Waarom deze roadmap nu logisch is:

Roadmap 122 maakt packaging/installer/recovery sterker. Daarna is de beste stap niet opnieuw meer features bouwen, maar de app veel beter **zelfverklarend** maken. Als iets fout gaat, moet de app meteen kunnen zeggen:

```text
Wat gebeurde er?
Waar gebeurde het?
Welke files zijn waarschijnlijk verantwoordelijk?
Welke logs/evidence bewijzen dat?
Welke veilige fix moet Codex doen?
Welke tests moeten daarna draaien?
```

---

## 0. Controle vooraf

### Repo- en roadmapcontrole

- [x] Gezocht naar bestaande `Roadmap 123`, `123-roadmap`, `AI Doctor`, `Black Box Recorder`, `Auto-Diagnostics`, `Codex Fix Prompt` en `Debug Evidence Bundle`.
- [x] Geen bestaande Roadmap 123 gevonden.
- [x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
- [x] Roadmap 122 is lokaal aangemaakt als Production-Grade Local Packaging, Installer, Desktop Shortcut, Safe Update/Rollback & Offline Recovery Kit.

### Codebasecontrole

Breed bekeken met focus op diagnostics, support bundle, AI ops, CLI commands, check-all, logs, evidence, dashboard/runtime status en redaction:

- [x] `src/binance_spot_bot/diagnostics.py`
- [x] `src/binance_spot_bot/ops_assistant.py`
- [x] `src/binance_spot_bot/cli.py`
- [x] `src/binance_spot_bot/check_all.py`
- [x] `src/binance_spot_bot/operator_ops.py`
- [x] `src/binance_spot_bot/support_bundle.py`
- [x] `src/binance_spot_bot/redaction.py`
- [x] `src/binance_spot_bot/audit.py`
- [x] `src/binance_spot_bot/runtime.py`
- [x] `src/binance_spot_bot/launcher.py`
- [x] Roadmaplijn 116-122.

### Bestaande basis die hergebruikt moet worden

De codebase heeft al veel puzzelstukken:

- [x] `diagnostics.py` heeft `DiagnosticsReport` met status, blockers, warnings, next safe action, Python/platform/package info, artifact inventory, pilot run health, runner lock health, recommended actions en redaction.
- [x] `diagnostics.py` kan health reports schrijven naar `data/evidence/diagnostics/latest-diagnostics.json` en `history.jsonl`.
- [x] `ops_assistant.py` kan lokale AI-ops vragen beantwoorden en sessies wegschrijven.
- [x] `cli.py` heeft al commands/imports voor diagnostics, support bundles, local ops, evidence manifests, AI ops context/search/runbook/command proposal, action center, environment doctor, roadmap tools en repo intelligence.
- [x] `check_all.py` forceert veilige defaults: `LIVE_TRADING_ENABLED=false`, `KILL_SWITCH=true`, `PYTHONPATH=src`.
- [x] `AuditLog` en redaction helpers beschermen tegen secret leaks.
- [x] Roadmap 116-122 plannen one-click launcher, package center, safe mode, recovery kit en support/evidence flows.

### Belangrijkste gat

Er zijn veel losse commands, maar nog geen één systeem dat automatisch alles samenpakt rond een concrete run/fout:

- [ ] Geen start snapshot bij launcher/app start.
- [ ] Geen finish snapshot bij stop/crash.
- [ ] Geen run-id die logs, diagnostics, check-all, evidence en runtime state aan elkaar bindt.
- [ ] Geen error/stacktrace collector.
- [ ] Geen known issue matcher.
- [ ] Geen AI debug summary.
- [ ] Geen Codex fix prompt generator.
- [ ] Geen “suspect files” detector.
- [ ] Geen dashboardpagina voor AI Doctor.
- [ ] Geen downloadbaar AI Doctor bundle.
- [ ] Geen automatische safe debugging workflow.
- [ ] Geen check-all profiel dat AI Doctor end-to-end test.

---

## 1. Hoofddoel Roadmap 123

Maak één AI-debug systeem:

```text
run starts
→ start snapshot
→ app/runtime/dashboard observer
→ error/log/event collectors
→ finish snapshot
→ diagnostics/check-all/evidence merge
→ known issue matcher
→ AI summary
→ Codex fix prompt
→ debug bundle
```

Na Roadmap 123 moet de operator:

- [ ] een run kunnen starten met AI Doctor actief;
- [ ] automatisch startcontext kunnen vastleggen;
- [ ] automatisch finish/crashcontext kunnen vastleggen;
- [ ] logs, stacktraces, runtime state en dashboard state kunnen bundelen;
- [ ] een AI Doctor summary kunnen krijgen;
- [ ] een Codex fix prompt kunnen genereren;
- [ ] een zip/bundle kunnen downloaden en aan ChatGPT/Codex geven;
- [ ] in Dashboard V2 kunnen zien wat fout ging;
- [ ] weten welke files waarschijnlijk geraakt zijn;
- [ ] weten welke tests/fixes veilig zijn;
- [ ] secrets en API keys automatisch redacted houden.

---

## 2. Niet opnieuw bouwen

Niet doen:

- [ ] Geen nieuwe trading runtime bouwen.
- [ ] Geen Dashboard V2 foundation opnieuw bouwen.
- [ ] Geen check-all opnieuw bouwen.
- [ ] Geen support bundle opnieuw bouwen.
- [ ] Geen AI ops assistant opnieuw bouwen.
- [ ] Geen live trading gates aanpassen.
- [ ] Geen live orders plaatsen.
- [ ] Geen runtime automatisch herstellen zonder operator.
- [ ] Geen secrets in logs/evidence/bundles.
- [ ] Geen cloud telemetry.
- [ ] Geen remote upload.
- [ ] Geen financial advice.

Wel doen:

- [ ] bestaande diagnostics/check-all/support/evidence hergebruiken;
- [ ] start/finish snapshots toevoegen;
- [ ] error/log collectors toevoegen;
- [ ] known issue matcher bouwen;
- [ ] AI summary writer bouwen;
- [ ] Codex prompt writer bouwen;
- [ ] debug bundle builder bouwen;
- [ ] dashboard AI Doctor pagina bouwen;
- [ ] CLI commands bouwen;
- [ ] check-all/browser/UAT integreren.

---

## 3. Fase 0 - AI Doctor Safety Contract

Nieuw docbestand:

```text
docs/ai-doctor/ai-doctor-safety-contract.md
```

Regels:

- [ ] AI Doctor is read-only tenzij expliciet een safe export wordt gemaakt.
- [ ] AI Doctor mag geen live orders plaatsen.
- [ ] AI Doctor mag geen live sessions starten.
- [ ] AI Doctor mag geen recovery acties automatisch uitvoeren.
- [ ] AI Doctor mag Codex fix prompts maken, maar niet zelf code wijzigen.
- [ ] AI Doctor bundle is secret-free.
- [ ] API keys, secrets, signatures, tokens, authorization headers en accountgevoelige velden worden geredact.
- [ ] AI Doctor mag safe env bevestigen:
  - `LIVE_TRADING_ENABLED=false`;
  - `KILL_SWITCH=true`.
- [ ] AI Doctor mag blockers/warnings aanraden, geen financieel advies.
- [ ] AI Doctor mag geen remote telemetry sturen.
- [ ] AI Doctor bundle blijft local-only.
- [ ] Crash collection mag nooit raw secrets lekken.

Acceptatiecriteria:

- [ ] Safety contract bestaat.
- [ ] Tests bewijzen AI Doctor geen order endpoints aanroept.
- [ ] Tests bewijzen AI Doctor geen live sessions start.
- [ ] Tests bewijzen secrets redacted zijn.
- [ ] Tests bewijzen bundle local-only is.

---

## 4. Fase 1 - AI Doctor Run Schema

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/run_schema.py
```

Dataclasses:

- [ ] `AIDoctorRun`
- [ ] `AIDoctorRunPhase`
- [ ] `AIDoctorRunStatus`
- [ ] `AIDoctorStartSnapshot`
- [ ] `AIDoctorFinishSnapshot`
- [ ] `AIDoctorFinding`
- [ ] `AIDoctorArtifactRef`
- [ ] `AIDoctorRunReport`

Run fields:

- [ ] run_id;
- [ ] profile_id;
- [ ] mode;
- [ ] app_entrypoint;
- [ ] started_at_ms;
- [ ] finished_at_ms optional;
- [ ] status;
- [ ] exit_code optional;
- [ ] error_count;
- [ ] warning_count;
- [ ] blocker_count;
- [ ] dashboard_url optional;
- [ ] data_dir;
- [ ] project_root;
- [ ] git_ref;
- [ ] python_version;
- [ ] platform;
- [ ] safe_env;
- [ ] live_trading_enabled=false;
- [ ] kill_switch=true by default;
- [ ] artifacts;
- [ ] no_live_order_statement;
- [ ] secret_redaction_status.

Acceptatiecriteria:

- [ ] Run schema is JSON-serializable.
- [ ] Run ID deterministic enough and unique.
- [ ] `live_trading_enabled` is false by default.
- [ ] Secret-like values redacted.
- [ ] Tests cover serialization/redaction.

---

## 5. Fase 2 - Start Snapshot Collector

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/start_snapshot.py
```

Collect:

- [ ] run id;
- [ ] timestamp;
- [ ] git branch/ref/dirty state if available;
- [ ] Python version;
- [ ] platform;
- [ ] current working directory;
- [ ] project root;
- [ ] package version;
- [ ] selected profile;
- [ ] env safe flags;
- [ ] redacted BotSettings;
- [ ] dashboard target URL/port if known;
- [ ] data dir;
- [ ] recent diagnostics trend;
- [ ] startup health if available;
- [ ] package/installer version if available;
- [ ] launcher command metadata;
- [ ] active live session state if available, redacted;
- [ ] no-live-auto-start proof.

Output:

```text
data/ai-doctor/runs/<run_id>/start_snapshot.json
```

Acceptatiecriteria:

- [ ] Snapshot works without API keys.
- [ ] Snapshot works before dashboard starts.
- [ ] Snapshot redacts secrets.
- [ ] Snapshot records safe env.
- [ ] Tests use temp dirs.

---

## 6. Fase 3 - Runtime/Dashboard Observer Hook

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/observer.py
```

Observer events:

- [ ] app_start;
- [ ] dashboard_starting;
- [ ] dashboard_ready;
- [ ] runtime_starting;
- [ ] runtime_ready;
- [ ] data_bootstrap_start;
- [ ] data_bootstrap_done;
- [ ] profile_selected;
- [ ] bot_start_clicked;
- [ ] bot_stop_clicked;
- [ ] dashboard_error;
- [ ] runtime_error;
- [ ] exception_seen;
- [ ] shutdown_requested;
- [ ] crash_detected.

Storage:

```text
data/ai-doctor/runs/<run_id>/events.jsonl
```

Rules:

- [ ] Non-blocking.
- [ ] Best-effort.
- [ ] Redacted payloads only.
- [ ] No order execution.
- [ ] No recovery execution.

Acceptatiecriteria:

- [ ] Event writer appends JSONL.
- [ ] Corrupt event does not crash app.
- [ ] Secrets redacted.
- [ ] Tests cover event append/read.

---

## 7. Fase 4 - Finish Snapshot Collector

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/finish_snapshot.py
```

Collect:

- [ ] run id;
- [ ] finish timestamp;
- [ ] exit status;
- [ ] exit code;
- [ ] last event;
- [ ] last exception;
- [ ] error count;
- [ ] warning count;
- [ ] blocker count;
- [ ] diagnostics status;
- [ ] check-all status if run;
- [ ] dashboard status;
- [ ] runtime status;
- [ ] pilot/runner lock health;
- [ ] recent artifact health;
- [ ] new files created during run;
- [ ] files changed during run;
- [ ] log/error pointers;
- [ ] next safe action.

Output:

```text
data/ai-doctor/runs/<run_id>/finish_snapshot.json
```

Acceptatiecriteria:

- [ ] Finish snapshot works on normal stop.
- [ ] Finish snapshot works on simulated crash.
- [ ] Missing start snapshot gives warning, not crash.
- [ ] Secrets redacted.
- [ ] Tests cover stop/crash.

---

## 8. Fase 5 - Error & Stacktrace Collector

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/error_collector.py
```

Collect from:

- [ ] Python exception hook where safe;
- [ ] dashboard logs;
- [ ] runtime logs;
- [ ] check-all output;
- [ ] diagnostics output;
- [ ] support bundle output;
- [ ] known app error files;
- [ ] Streamlit/FastAPI/browser smoke errors;
- [ ] recent terminal command output if captured.

Outputs:

```text
data/ai-doctor/runs/<run_id>/errors.txt
data/ai-doctor/runs/<run_id>/stacktraces.txt
data/ai-doctor/runs/<run_id>/error_summary.json
```

Error fields:

- [ ] error_id;
- [ ] error_type;
- [ ] message;
- [ ] file path if known;
- [ ] line if known;
- [ ] traceback hash;
- [ ] first_seen_ms;
- [ ] last_seen_ms;
- [ ] count;
- [ ] severity guess;
- [ ] redacted text.

Acceptatiecriteria:

- [ ] Collector parses Python tracebacks.
- [ ] Collector detects StreamlitDuplicateElementId.
- [ ] Collector detects ModuleNotFoundError.
- [ ] Collector detects JSONDecodeError.
- [ ] Secrets redacted.

---

## 9. Fase 6 - Log Collector

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/log_collector.py
```

Collect:

- [ ] app logs;
- [ ] dashboard logs;
- [ ] runtime logs;
- [ ] launcher logs;
- [ ] check-all logs;
- [ ] latest diagnostics history;
- [ ] latest audit entries, redacted;
- [ ] session heartbeats;
- [ ] pilot runner telemetry;
- [ ] browser smoke logs.

Outputs:

```text
data/ai-doctor/runs/<run_id>/recent_logs.txt
data/ai-doctor/runs/<run_id>/log_index.json
```

Rules:

- [ ] Max size per log.
- [ ] Redact secrets.
- [ ] Mark missing logs as warnings.
- [ ] Do not fail bundle if optional log missing.

Acceptatiecriteria:

- [ ] Log collector handles missing logs.
- [ ] Log truncation works.
- [ ] Secret scan passes.
- [ ] Tests cover log collection.

---

## 10. Fase 7 - System State Collector

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/system_state_collector.py
```

Collect:

- [ ] diagnostics report;
- [ ] environment doctor report;
- [ ] local ops snapshot;
- [ ] operator report;
- [ ] operator quality gate;
- [ ] evidence manifest;
- [ ] command manifest;
- [ ] artifact catalog;
- [ ] report index;
- [ ] redaction self-test;
- [ ] package/startup health if Roadmap 122 exists;
- [ ] active sessions summary;
- [ ] dashboard/routing state if available;
- [ ] runtime snapshot if available.

Outputs:

```text
data/ai-doctor/runs/<run_id>/system_state/
  diagnostics.json
  environment_doctor.json
  local_ops_snapshot.json
  operator_report.json
  evidence_manifest.json
  command_manifest.json
  redaction_self_test.json
```

Acceptatiecriteria:

- [ ] Collector reuses existing functions where possible.
- [ ] Missing command/function becomes warning.
- [ ] No command execution in unit tests.
- [ ] Redaction applied to all payloads.
- [ ] Tests use fixture reports.

---

## 11. Fase 8 - Check-All Capture Adapter

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/check_all_capture.py
```

Purpose:

- [ ] run or ingest check-all result;
- [ ] capture status;
- [ ] capture failed checks;
- [ ] capture warnings;
- [ ] capture safe env proof;
- [ ] link to generated check-all artifact;
- [ ] create AI-readable summary.

Modes:

- [ ] `ingest_existing`;
- [ ] `fast`;
- [ ] `deep`;
- [ ] `no_run_summary_only`.

Rules:

- [ ] Default is not to run expensive deep checks automatically.
- [ ] Never set live env unsafe.
- [ ] Always force safe env when running.
- [ ] Redact output.

Acceptatiecriteria:

- [ ] Existing check-all artifact ingested.
- [ ] Failed check mapped to finding.
- [ ] Safe env proof included.
- [ ] Tests cover fixture check-all payloads.

---

## 12. Fase 9 - Git/Codebase Context Collector

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/codebase_context.py
```

Collect:

- [ ] git ref if available;
- [ ] git status if available;
- [ ] changed files;
- [ ] untracked files;
- [ ] repo tree from `git ls-files` equivalent where safe;
- [ ] recent roadmap index;
- [ ] Voltooid docs/Roadmap docs latest numbers;
- [ ] suspected files from errors;
- [ ] nearby files from imports;
- [ ] test files likely relevant;
- [ ] hotspots:
  - TODO;
  - FIXME;
  - StreamlitDuplicateElementId;
  - LIVE_TRADING_ENABLED;
  - KILL_SWITCH;
  - place_order;
  - cancel_order;
  - validate_live_readiness;
  - RuntimeError;
  - traceback.

Outputs:

```text
data/ai-doctor/runs/<run_id>/codebase_context/
  git_status.txt
  changed_files.txt
  repo_tree.txt
  suspect_files.json
  hotspots.txt
```

Acceptatiecriteria:

- [ ] Works without git, with warning.
- [ ] Suspect files extracted from stacktrace paths.
- [ ] Roadmap/docs latest numbers included.
- [ ] Secret scan passes.
- [ ] Tests use fixture repo tree.

---

## 13. Fase 10 - Known Issue Matcher

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/known_issue_matcher.py
```

Known issue patterns:

### Dashboard/UI

- [ ] `StreamlitDuplicateElementId`
  - probable fix: add unique `key=` to repeated Streamlit elements.
  - suspect files: `streamlit_app.py`, chart/widget rendering files.
- [ ] Plotly chart duplicate render.
- [ ] Missing dashboard route.
- [ ] Browser smoke failure.
- [ ] Port already in use.

### Python/dependency

- [ ] `ModuleNotFoundError`
  - probable fix: dependency/profile/install issue.
- [ ] `ImportError`.
- [ ] Python version mismatch.
- [ ] Missing optional extra.

### Data/evidence

- [ ] `JSONDecodeError`
  - probable fix: corrupt artifact, regenerate evidence.
- [ ] Stale artifact.
- [ ] Missing critical evidence.
- [ ] Invalid manifest/hash mismatch.

### Runtime

- [ ] Stale runner lock.
- [ ] Non-terminal stale pilot run.
- [ ] Failed runner command.
- [ ] Data bootstrap failure.
- [ ] Market data stale.

### Safety/live

- [ ] `LIVE_TRADING_ENABLED=true` during safe checks.
- [ ] `KILL_SWITCH=false` in unsafe context.
- [ ] Forbidden order endpoint in non-live gate.
- [ ] Raw secret detected.

Output:

```text
data/ai-doctor/runs/<run_id>/known_issue_matches.json
```

Each match:

- [ ] issue_id;
- [ ] title;
- [ ] severity;
- [ ] confidence;
- [ ] evidence_refs;
- [ ] suspect_files;
- [ ] recommended_fix;
- [ ] recommended_tests;
- [ ] codex_instructions;
- [ ] safety_notes.

Acceptatiecriteria:

- [ ] Detects StreamlitDuplicateElementId from fixture.
- [ ] Detects ModuleNotFoundError.
- [ ] Detects stale runner lock.
- [ ] Detects secret leak.
- [ ] Tests cover issue matching.

---

## 14. Fase 11 - Root Cause Hypothesis Engine

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/root_cause_hypotheses.py
```

Purpose:

- [ ] combine diagnostics, logs, errors, check-all, known issue matches and codebase context;
- [ ] generate likely causes;
- [ ] rank by evidence;
- [ ] avoid fake certainty;
- [ ] include “unknown/needs more evidence” when needed.

Output fields:

- [ ] hypothesis_id;
- [ ] title;
- [ ] confidence;
- [ ] evidence_refs;
- [ ] supporting signals;
- [ ] contradicting signals;
- [ ] suspect files;
- [ ] safest next step;
- [ ] recommended tests.

Acceptatiecriteria:

- [ ] Hypotheses deterministic.
- [ ] Low evidence gives low confidence.
- [ ] Unknown is allowed.
- [ ] No financial advice wording.
- [ ] Tests cover fixture issues.

---

## 15. Fase 12 - AI Summary Writer

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/ai_summary_writer.py
```

Output:

```text
data/ai-doctor/runs/<run_id>/ai_summary.md
```

Template:

```md
# AI Doctor Summary

## Main status
...

## Main problem
...

## Most likely cause
...

## Evidence
...

## Suspect files
...

## Recommended safe fix
...

## Recommended tests
...

## Safety state
- LIVE_TRADING_ENABLED=false
- KILL_SWITCH=true
- No live order path touched

## What to ask ChatGPT/Codex
...
```

Rules:

- [ ] Simple language.
- [ ] Evidence links/paths.
- [ ] No raw secrets.
- [ ] No fake certainty.
- [ ] Include confidence.
- [ ] Include safe next action.

Acceptatiecriteria:

- [ ] Summary generated from fixture bundle.
- [ ] Missing evidence noted.
- [ ] Suspect files included.
- [ ] Secret scan passes.
- [ ] Tests snapshot summary.

---

## 16. Fase 13 - Codex Fix Prompt Generator

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/codex_prompt_writer.py
```

Output:

```text
data/ai-doctor/runs/<run_id>/codex_fix_prompt.md
```

Prompt includes:

- [ ] problem statement;
- [ ] evidence files to read first;
- [ ] suspect files;
- [ ] files not to touch;
- [ ] safety constraints;
- [ ] exact requested fix;
- [ ] acceptance criteria;
- [ ] tests to run;
- [ ] no-live/no-secret rules;
- [ ] rollback if risky.

Acceptatiecriteria:

- [ ] Prompt generated from issue match.
- [ ] Prompt includes no-live constraints.
- [ ] Prompt includes tests.
- [ ] Prompt includes suspect files.
- [ ] Secret scan passes.

---

## 17. Fase 14 - Debug Pack Builder

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/debug_pack_builder.py
```

Bundle layout:

```text
data/ai-doctor/runs/<run_id>/
  start_snapshot.json
  finish_snapshot.json
  events.jsonl
  errors.txt
  stacktraces.txt
  error_summary.json
  recent_logs.txt
  log_index.json
  system_state/
  codebase_context/
  known_issue_matches.json
  root_cause_hypotheses.json
  ai_summary.md
  codex_fix_prompt.md
  manifest.json
  redaction_report.json
  ai_doctor_bundle.zip
```

Manifest fields:

- [ ] run_id;
- [ ] created_at_ms;
- [ ] files;
- [ ] hashes;
- [ ] redaction_status;
- [ ] secret_scan_status;
- [ ] live_trading_enabled=false;
- [ ] no_order_endpoint_called=true;
- [ ] no_remote_upload=true.

Acceptatiecriteria:

- [ ] Bundle zip created.
- [ ] Manifest hashes verify.
- [ ] Secret scan passes.
- [ ] Missing optional artifact becomes warning.
- [ ] Tests create bundle in temp dir.

---

## 18. Fase 15 - AI Doctor Evidence Bundle

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/doctor_evidence_bundle.py
```

Evidence bevat:

- [ ] AI Doctor safety contract;
- [ ] run schema report;
- [ ] start snapshot;
- [ ] finish snapshot;
- [ ] observer events;
- [ ] error collector report;
- [ ] log collector report;
- [ ] system state collector report;
- [ ] check-all capture report;
- [ ] codebase context report;
- [ ] known issue matches;
- [ ] root cause hypotheses;
- [ ] AI summary;
- [ ] Codex fix prompt;
- [ ] debug bundle manifest;
- [ ] redaction proof;
- [ ] no-live/no-order proof;
- [ ] hashes.

Output:

```text
data/ai-doctor/evidence/<run_id>/
  ai_doctor_evidence_manifest.json
  ai_doctor_evidence_summary.md
  files/
```

Acceptatiecriteria:

- [ ] Evidence bundle secret-free.
- [ ] Evidence has manifest/hash.
- [ ] Evidence can be verified.
- [ ] Evidence links debug pack.
- [ ] Tests verify evidence.

---

## 19. Fase 16 - CLI Commands

Nieuwe commands:

```powershell
python -m binance_spot_bot.cli ai-doctor-start --profile paper --json
python -m binance_spot_bot.cli ai-doctor-event --run <id> --type dashboard_ready --json
python -m binance_spot_bot.cli ai-doctor-finish --run latest --status ok --json
python -m binance_spot_bot.cli ai-doctor-crash-report --run latest --error-file <path> --json
python -m binance_spot_bot.cli ai-doctor-status --run latest --json
python -m binance_spot_bot.cli ai-doctor-collect --run latest --json
python -m binance_spot_bot.cli ai-doctor-match-issues --run latest --json
python -m binance_spot_bot.cli ai-doctor-summary --run latest
python -m binance_spot_bot.cli ai-doctor-codex-prompt --run latest
python -m binance_spot_bot.cli ai-doctor-export --run latest
python -m binance_spot_bot.cli ai-doctor-evidence-export --run latest --json
python -m binance_spot_bot.cli ai-doctor-verify --bundle <path> --json
python -m binance_spot_bot.cli dashboard-v2-ai-doctor-smoke --json
```

Acceptatiecriteria:

- [ ] Commands werken lokaal.
- [ ] Commands ondersteunen JSON waar relevant.
- [ ] Commands werken zonder API keys.
- [ ] Commands starten geen live session.
- [ ] Commands plaatsen geen orders.
- [ ] Commands redacteren secrets.

---

## 20. Fase 17 - Launcher / App-Control Integratie

Integratie met Roadmap 116/122:

- [ ] launcher maakt automatisch AI Doctor run id aan;
- [ ] launcher schrijft start snapshot;
- [ ] dashboard krijgt run id via env/session state;
- [ ] app supervisor schrijft events;
- [ ] shutdown schrijft finish snapshot;
- [ ] crash writes crash report;
- [ ] safe mode kan laatste AI Doctor bundle exporteren;
- [ ] package/recovery center kan AI Doctor status tonen.

Start flow:

```text
Start-Neural-Binance-Bot.cmd
→ ai-doctor-start
→ app supervisor start
→ dashboard opens
```

Shutdown/crash flow:

```text
app stop/crash
→ ai-doctor-finish
→ ai-doctor-collect
→ ai-doctor-summary
→ ai-doctor-codex-prompt
```

Acceptatiecriteria:

- [ ] Launcher start snapshot in safe mode.
- [ ] Dashboard run id zichtbaar.
- [ ] Normal shutdown finish snapshot.
- [ ] Simulated crash creates crash report.
- [ ] No live auto-start introduced.

---

## 21. Fase 18 - Dashboard V2 AI Doctor Center

Nieuwe route:

```text
/ai-doctor
```

Panels:

- [ ] current run status;
- [ ] latest run summary;
- [ ] start snapshot;
- [ ] finish snapshot;
- [ ] detected errors;
- [ ] known issue matches;
- [ ] root cause hypotheses;
- [ ] suspect files;
- [ ] recommended safe fix;
- [ ] recommended tests;
- [ ] Codex fix prompt preview;
- [ ] export bundle button;
- [ ] evidence export button;
- [ ] redaction status;
- [ ] no-live/no-order status.

UX rules:

- [ ] “Export AI Doctor Bundle” prominent.
- [ ] “Copy Codex Fix Prompt” prominent.
- [ ] No raw logs with secrets.
- [ ] Safe env visible.
- [ ] Missing evidence shown clearly.
- [ ] No live controls on this page.

Acceptatiecriteria:

- [ ] AI Doctor page loads.
- [ ] Latest run visible.
- [ ] Known issue match visible.
- [ ] Codex prompt preview visible.
- [ ] Browser smoke covers page.

---

## 22. Fase 19 - AI Doctor API Routes

Nieuwe API routes:

```text
GET  /api/ai-doctor/status
POST /api/ai-doctor/runs/start
POST /api/ai-doctor/runs/{run_id}/event
POST /api/ai-doctor/runs/{run_id}/finish
POST /api/ai-doctor/runs/{run_id}/collect
POST /api/ai-doctor/runs/{run_id}/match-issues
POST /api/ai-doctor/runs/{run_id}/summary
POST /api/ai-doctor/runs/{run_id}/codex-prompt
POST /api/ai-doctor/runs/{run_id}/export
POST /api/ai-doctor/runs/{run_id}/evidence
GET  /api/ai-doctor/runs
GET  /api/ai-doctor/runs/{run_id}
GET  /api/ai-doctor/runs/{run_id}/download
WS   /ws/ai-doctor
```

API rules:

- [ ] No route places orders.
- [ ] No route starts live session.
- [ ] No route returns raw secrets.
- [ ] Bundle export remains local.
- [ ] Long collection jobs are bounded.

Acceptatiecriteria:

- [ ] TestClient covers core routes.
- [ ] Export route produces bundle.
- [ ] Secrets redacted.
- [ ] No live/order calls.
- [ ] WebSocket emits doctor events.

---

## 23. Fase 20 - Auto-Diagnostics Rules

Rules when app starts:

- [ ] start snapshot always created;
- [ ] diagnostics trend loaded;
- [ ] stale critical artifacts create warning;
- [ ] stale runner lock warning visible;
- [ ] missing check-all warning visible;
- [ ] live enabled blocker visible;
- [ ] dashboard port/status recorded.

Rules when app stops:

- [ ] finish snapshot always attempted;
- [ ] errors collected;
- [ ] logs collected;
- [ ] known issue matching run;
- [ ] AI summary generated if failure/warning;
- [ ] Codex prompt generated if actionable issue.

Rules on crash:

- [ ] crash report created;
- [ ] stacktrace captured;
- [ ] finish snapshot marks failed;
- [ ] bundle export suggested.

Acceptatiecriteria:

- [ ] Normal run gives ok summary.
- [ ] Warning run gives advice.
- [ ] Crash run gives bundle.
- [ ] No app crash if AI Doctor fails.
- [ ] Tests cover all run outcomes.

---

## 24. Fase 21 - Codex Task Classifier

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/codex_task_classifier.py
```

Classify issue into:

- [ ] dashboard_fix;
- [ ] runtime_fix;
- [ ] config_fix;
- [ ] dependency_fix;
- [ ] evidence_repair;
- [ ] test_fix;
- [ ] docs_fix;
- [ ] packaging_fix;
- [ ] safety_blocker;
- [ ] unknown_investigate_first.

For each class:

- [ ] allowed files;
- [ ] forbidden files;
- [ ] required tests;
- [ ] safety notes;
- [ ] rollback advice;
- [ ] PR size recommendation.

Acceptatiecriteria:

- [ ] StreamlitDuplicateElementId classified as dashboard_fix.
- [ ] ModuleNotFoundError classified as dependency_fix.
- [ ] Secret leak classified as safety_blocker.
- [ ] Unknown gets investigate-first.
- [ ] Tests cover classification.

---

## 25. Fase 22 - Repair Suggestion Engine

Nieuwe module:

```text
src/binance_spot_bot/ai_doctor/repair_suggestions.py
```

Suggestion types:

- [ ] add unique Streamlit keys;
- [ ] regenerate corrupt artifact;
- [ ] clear stale runner lock safely;
- [ ] install missing dependency/extra;
- [ ] run safe mode;
- [ ] run check-all fast;
- [ ] run browser smoke;
- [ ] rebuild dashboard assets;
- [ ] recreate support bundle;
- [ ] repair shortcut/recovery kit;
- [ ] stop active unsafe state;
- [ ] investigate manually.

Each suggestion:

- [ ] title;
- [ ] severity;
- [ ] why;
- [ ] evidence refs;
- [ ] command suggestion if safe;
- [ ] manual steps;
- [ ] tests to run;
- [ ] Codex task wording.

Acceptatiecriteria:

- [ ] Suggestions generated for known issue matches.
- [ ] Unsafe suggestions blocked.
- [ ] Commands marked safe/unsafe.
- [ ] Tests cover suggestion generation.

---

## 26. Fase 23 - AI Context Pack Integration

Integrate with AI context layer:

```text
data/ai-context/latest-ai-doctor-summary.md
data/ai-context/latest-codex-fix-prompt.md
data/ai-context/latest-debug-pack-manifest.json
```

Update/produce:

- [ ] latest AI Doctor summary;
- [ ] latest Codex prompt;
- [ ] latest suspect files;
- [ ] latest check-all status;
- [ ] latest dashboard/runtime status;
- [ ] latest known issue matches;
- [ ] latest roadmap/docs context pointers.

Acceptatiecriteria:

- [ ] AI context pack includes latest doctor status.
- [ ] Context pack remains secret-free.
- [ ] Codex can read one file first.
- [ ] Tests verify output.

---

## 27. Fase 24 - Check-All Integration

Fast profile:

- [ ] AI Doctor modules import.
- [ ] safety contract exists.
- [ ] run schema serialization.
- [ ] start snapshot fixture.
- [ ] finish snapshot fixture.
- [ ] known issue matcher fixture.
- [ ] secret redaction.
- [ ] no-live/no-order tests.

Deep profile:

- [ ] simulated dashboard error.
- [ ] error collector.
- [ ] log collector.
- [ ] system state collector with fixtures.
- [ ] check-all capture.
- [ ] codebase context.
- [ ] root cause hypotheses.
- [ ] AI summary.
- [ ] Codex prompt.
- [ ] debug bundle export/verify.
- [ ] Dashboard AI Doctor browser smoke.

Acceptatiecriteria:

- [ ] Fast check-all blijft snel.
- [ ] Deep profile dekt end-to-end doctor bundle.
- [ ] Secret leak hard fails.
- [ ] Live/order endpoint use hard fails.
- [ ] Bundle hash verification works.

---

## 28. Fase 25 - UAT / Operator Workflow

UAT scenario 1: normale start/stop

- [ ] start app met AI Doctor;
- [ ] dashboard opent;
- [ ] stop app;
- [ ] finish snapshot exists;
- [ ] summary status ok;
- [ ] bundle export works.

UAT scenario 2: simulated dashboard crash

- [ ] inject fixture error;
- [ ] AI Doctor detects error;
- [ ] stacktrace captured;
- [ ] known issue matched;
- [ ] Codex prompt generated;
- [ ] bundle export works.

UAT scenario 3: stale runner lock

- [ ] create stale lock fixture;
- [ ] diagnostics warning;
- [ ] known issue match;
- [ ] recommended safe action.

UAT scenario 4: secret redaction

- [ ] fixture with fake secret;
- [ ] bundle redacts;
- [ ] redaction report pass.

UAT scenario 5: Codex handoff

- [ ] export `codex_fix_prompt.md`;
- [ ] verify it lists read-first files;
- [ ] verify it includes forbidden live changes;
- [ ] verify tests listed.

Acceptatiecriteria:

- [ ] UAT proves AI Doctor makes debugging faster.
- [ ] UAT proves no secrets leak.
- [ ] UAT proves Codex prompt usable.
- [ ] UAT evidence attached.

---

## 29. Fase 26 - Release / Knowledge / Test / Performance Integration

Roadmap 089:

- [ ] release notes mention AI Doctor.
- [ ] version manifest includes AI Doctor schema.
- [ ] migration notes include `data/ai-doctor` paths.

Roadmap 091:

- [ ] knowledge graph maps diagnostics/check-all/logs/errors → known issue → fix prompt.
- [ ] impact analysis detects changes affecting AI Doctor.

Roadmap 092:

- [ ] test selector chooses AI Doctor tests for diagnostics/cli/check-all/dashboard/runtime changes.
- [ ] dashboard AI Doctor changes select browser smoke.

Roadmap 093:

- [ ] performance budget for start snapshot.
- [ ] performance budget for finish collection.
- [ ] bundle size budget.
- [ ] log collection max time.
- [ ] dashboard render budget.

Acceptatiecriteria:

- [ ] Release evidence includes AI Doctor evidence.
- [ ] Knowledge graph updated.
- [ ] Test selector protects AI Doctor.
- [ ] Performance reports include AI Doctor budgets.

---

## 30. Fase 27 - Scheduled AI Doctor Reports

Scheduled jobs:

- [ ] daily AI Doctor health summary.
- [ ] daily diagnostics trend summary.
- [ ] weekly known issue scan.
- [ ] weekly stale artifact scan.
- [ ] weekly redaction self-test.
- [ ] weekly AI Doctor bundle verify.
- [ ] monthly AI Doctor evidence export.

Metrics:

- [ ] latest run status;
- [ ] warning count trend;
- [ ] blocker count trend;
- [ ] top known issues;
- [ ] stale artifact count;
- [ ] latest check-all status;
- [ ] latest bundle export status;
- [ ] redaction status;
- [ ] no-live/no-order proof.

Acceptatiecriteria:

- [ ] Jobs never start live.
- [ ] Jobs never place orders.
- [ ] Reports secret-free.
- [ ] Dashboard can show reports.

---

## 31. Tests

### Unit tests

- [ ] `tests/test_ai_doctor_safety_contract.py`
- [ ] `tests/test_ai_doctor_run_schema.py`
- [ ] `tests/test_ai_doctor_start_snapshot.py`
- [ ] `tests/test_ai_doctor_observer.py`
- [ ] `tests/test_ai_doctor_finish_snapshot.py`
- [ ] `tests/test_ai_doctor_error_collector.py`
- [ ] `tests/test_ai_doctor_log_collector.py`
- [ ] `tests/test_ai_doctor_system_state_collector.py`
- [ ] `tests/test_ai_doctor_check_all_capture.py`
- [ ] `tests/test_ai_doctor_codebase_context.py`
- [ ] `tests/test_ai_doctor_known_issue_matcher.py`
- [ ] `tests/test_ai_doctor_root_cause_hypotheses.py`
- [ ] `tests/test_ai_doctor_ai_summary_writer.py`
- [ ] `tests/test_ai_doctor_codex_prompt_writer.py`
- [ ] `tests/test_ai_doctor_debug_pack_builder.py`
- [ ] `tests/test_ai_doctor_evidence_bundle.py`
- [ ] `tests/test_ai_doctor_codex_task_classifier.py`
- [ ] `tests/test_ai_doctor_repair_suggestions.py`
- [ ] `tests/test_ai_doctor_api.py`

### Integration tests

- [ ] Create start snapshot.
- [ ] Append observer events.
- [ ] Create finish snapshot.
- [ ] Collect fixture stacktrace.
- [ ] Match known issue.
- [ ] Build root cause hypothesis.
- [ ] Generate AI summary.
- [ ] Generate Codex prompt.
- [ ] Build debug pack.
- [ ] Verify debug pack.
- [ ] Export evidence bundle.

### Browser smoke

- [ ] `/ai-doctor` loads.
- [ ] current run card visible.
- [ ] latest summary visible.
- [ ] known issue matches visible.
- [ ] suspect files visible.
- [ ] Codex prompt preview visible.
- [ ] export bundle button visible.
- [ ] redaction status visible.
- [ ] no live controls visible.

### Safety tests

- [ ] AI Doctor never calls order endpoints.
- [ ] AI Doctor never starts live session.
- [ ] AI Doctor never changes code.
- [ ] AI Doctor never leaks secrets.
- [ ] AI Doctor bundle stays local.
- [ ] Codex prompt includes no-live constraints.
- [ ] Check-all safe env preserved.

---

## 32. Docs

Nieuwe docs:

```text
docs/ai-doctor/ai-doctor-safety-contract.md
docs/ai-doctor/overview.md
docs/ai-doctor/run-schema.md
docs/ai-doctor/start-snapshot.md
docs/ai-doctor/finish-snapshot.md
docs/ai-doctor/error-collector.md
docs/ai-doctor/log-collector.md
docs/ai-doctor/system-state-collector.md
docs/ai-doctor/known-issue-matcher.md
docs/ai-doctor/root-cause-hypotheses.md
docs/ai-doctor/ai-summary.md
docs/ai-doctor/codex-fix-prompt.md
docs/ai-doctor/debug-pack.md
docs/ai-doctor/dashboard-ai-doctor-center.md
docs/ai-doctor/troubleshooting.md
```

README updates:

- [ ] “How to debug with AI Doctor”.
- [ ] “Export bundle for ChatGPT/Codex”.
- [ ] “How to read AI summary”.
- [ ] “How to use Codex fix prompt”.
- [ ] “No secrets/no live safety”.
- [ ] “Common known issues”.

---

## 33. Codex bouwvolgorde

### PR 1 - Safety Contract + Run Schema

- [ ] `docs/ai-doctor/ai-doctor-safety-contract.md`
- [ ] `ai_doctor/run_schema.py`
- [ ] serialization/redaction tests.

### PR 2 - Start/Finish Snapshots + Observer

- [ ] `start_snapshot.py`
- [ ] `finish_snapshot.py`
- [ ] `observer.py`
- [ ] run lifecycle tests.

### PR 3 - Error & Log Collectors

- [ ] `error_collector.py`
- [ ] `log_collector.py`
- [ ] traceback/log tests.

### PR 4 - System State + Check-All Capture

- [ ] `system_state_collector.py`
- [ ] `check_all_capture.py`
- [ ] fixture report tests.

### PR 5 - Codebase Context + Known Issue Matcher

- [ ] `codebase_context.py`
- [ ] `known_issue_matcher.py`
- [ ] StreamlitDuplicateElementId/ModuleNotFoundError/stale-lock tests.

### PR 6 - Root Cause + Repair Suggestions

- [ ] `root_cause_hypotheses.py`
- [ ] `repair_suggestions.py`
- [ ] hypothesis/suggestion tests.

### PR 7 - AI Summary + Codex Prompt

- [ ] `ai_summary_writer.py`
- [ ] `codex_prompt_writer.py`
- [ ] output snapshot tests.

### PR 8 - Debug Pack + Evidence Bundle

- [ ] `debug_pack_builder.py`
- [ ] `doctor_evidence_bundle.py`
- [ ] zip/manifest/hash/redaction tests.

### PR 9 - CLI + App/Launcher Integration

- [ ] AI Doctor CLI commands.
- [ ] launcher start snapshot hook.
- [ ] shutdown/crash finish hook.
- [ ] safe mode export hook.

### PR 10 - Dashboard AI Doctor Center + API

- [ ] API routes.
- [ ] `/ai-doctor` page.
- [ ] browser smoke.

### PR 11 - AI Context Pack + Check-All Integration

- [ ] latest AI Doctor context outputs.
- [ ] check-all fast/deep AI Doctor profile.
- [ ] test selector integration.

### PR 12 - Docs, UAT, Release/Knowledge/Performance

- [ ] docs.
- [ ] UAT scenarios.
- [ ] release notes.
- [ ] knowledge/test/performance integration.
- [ ] scheduled reports.

---

## 34. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 123 PR 1: AI Doctor Safety Contract + Run Schema.

Maak docs/ai-doctor/ai-doctor-safety-contract.md.

Maak src/binance_spot_bot/ai_doctor/__init__.py.
Maak src/binance_spot_bot/ai_doctor/run_schema.py met:
- AIDoctorRun
- AIDoctorRunPhase
- AIDoctorRunStatus
- AIDoctorStartSnapshot
- AIDoctorFinishSnapshot
- AIDoctorFinding
- AIDoctorArtifactRef
- AIDoctorRunReport
- create_ai_doctor_run_id(...)
- ai_doctor_run_to_dict(...)
- write_ai_doctor_run_report(...)
- redact_ai_doctor_payload(...)

AIDoctorRun moet minimaal ondersteunen:
- run_id
- profile_id
- mode
- app_entrypoint
- started_at_ms
- finished_at_ms optional
- status
- exit_code optional
- error_count
- warning_count
- blocker_count
- dashboard_url optional
- data_dir
- project_root
- git_ref
- python_version
- platform
- safe_env
- live_trading_enabled=False
- kill_switch=True
- artifacts
- no_live_order_statement
- secret_redaction_status

Validatie moet blokkeren of warnings geven op:
- live_trading_enabled=True
- missing no_live_order_statement
- missing secret_redaction_status
- raw secret-like values
- unsafe dashboard_url
- invalid status
- invalid phase
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
- create valid AI Doctor run
- JSON serialization
- run id generation
- live_trading_enabled true blocked/warned
- safe_env contains LIVE_TRADING_ENABLED=false and KILL_SWITCH=true
- secret-like values worden geredact
- missing no_live_order_statement blocked
- invalid status blocked
- invalid phase blocked
- unsafe dashboard_url blocked
```

Waarom eerst:

- Alles in AI Doctor hangt aan een run id en schema.
- Dit raakt nog geen runtime/dashboard/trading.
- Het maakt no-live en redaction meteen machine-testbaar.
- Daarna kunnen start/finish snapshots, collectors, summaries en Codex prompts veilig op dit schema bouwen.

---

## 35. Definition of Done

Roadmap 123 is klaar als:

- [ ] AI Doctor Safety Contract bestaat.
- [ ] AI Doctor Run Schema werkt.
- [ ] Start Snapshot Collector werkt.
- [ ] Runtime/Dashboard Observer Hook werkt.
- [ ] Finish Snapshot Collector werkt.
- [ ] Error & Stacktrace Collector werkt.
- [ ] Log Collector werkt.
- [ ] System State Collector werkt.
- [ ] Check-All Capture Adapter werkt.
- [ ] Git/Codebase Context Collector werkt.
- [ ] Known Issue Matcher werkt.
- [ ] Root Cause Hypothesis Engine werkt.
- [ ] AI Summary Writer werkt.
- [ ] Codex Fix Prompt Generator werkt.
- [ ] Debug Pack Builder werkt.
- [ ] AI Doctor Evidence Bundle werkt.
- [ ] CLI commands werken.
- [ ] Launcher/App-Control integratie werkt.
- [ ] Dashboard V2 AI Doctor Center werkt.
- [ ] AI Doctor API routes werken.
- [ ] Auto-Diagnostics Rules werken.
- [ ] Codex Task Classifier werkt.
- [ ] Repair Suggestion Engine werkt.
- [ ] AI Context Pack Integration werkt.
- [ ] Check-All Integration werkt.
- [ ] UAT/Operator Workflow werkt.
- [ ] Release/Knowledge/Test/Performance Integration werkt.
- [ ] Scheduled AI Doctor Reports werken.
- [ ] Tests bewijzen geen order endpoints.
- [ ] Tests bewijzen geen live sessions gestart worden.
- [ ] Tests bewijzen secrets redacted zijn.
- [ ] Tests bewijzen debug bundle verifieerbaar is.
- [ ] Browser smoke blijft groen.
- [ ] Check-all blijft groen.
- [ ] Roadmap 123 kan na uitvoering naar `Voltooid docs`.

---

## 36. Verwachte Roadmap 124 daarna

Als Roadmap 123 groen is:

```text
Roadmap 124 - AI Doctor Auto-Repair Proposals, Safe Action Center Integration & Patch Review Workflow
```

Mogelijke inhoud:

- [ ] AI Doctor maakt automatisch safe repair proposals;
- [ ] Action Center approval workflow;
- [ ] Codex patch review;
- [ ] test-run evidence;
- [ ] rollback proposal;
- [ ] still no automatic code changes without approval.
```

Als Roadmap 123 vooral veel diagnostische gaten vindt:

```text
Roadmap 124 - Diagnostics Coverage Burn-Down, Missing Evidence Repair & Known Issue Matcher Expansion
```

Mogelijke inhoud:

- [ ] meer known issue patterns;
- [ ] betere dashboard/runtime logging;
- [ ] missing evidence collectors;
- [ ] support bundle uitbreiding;
- [ ] root cause confidence verbetering.
```
