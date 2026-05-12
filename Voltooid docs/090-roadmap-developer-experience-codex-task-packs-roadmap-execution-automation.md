# Roadmap 090 - Developer Experience, Codex Task Packs \& Roadmap Execution Automation

Status: Voltooid na hercontrole en volledige validatie  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/090-roadmap-developer-experience-codex-task-packs-roadmap-execution-automation.md
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

Doel: Roadmap 089 maakt lokale releases, versioned upgrade paths, schema migrations en release evidence veilig. Roadmap 090 richt zich op **developer experience en roadmap-uitvoering**: Codex-ready task packs, PR templates, automatische roadmapvalidatie, dependency graphs, duplicate-work guards, roadmap evidence checks, uitvoeringstatus, en een flow om roadmaps veilig van `Roadmap docs` naar `Voltooid docs` te verplaatsen zodra tests/evidence groen zijn.

Live trading blijft volledig buiten scope.

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
  * roadmaps verplaatsen naar `Voltooid docs`;
  * live trading disabled.
* \[x] Geen bestaande Roadmap 090 gevonden via repo-search.
* \[x] Roadmap 089 is lokaal aangemaakt voor release management, versioned upgrade paths en migration safety.

### Codebasecontrole

Gecontroleerde relevante modules/bestanden:

* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] `pyproject.toml`
* \[x] bestaande CLI bevat al:

  * `check-all`;
  * `dashboard-smoke`;
  * `dashboard-browser-smoke`;
  * `operator-quality-gate`;
  * `operator-command-manifest`;
  * `evidence-manifest`;
  * `evidence-chain`;
  * `report-index`;
  * `artifact-catalog`;
  * `local-ops-snapshot`;
  * `support-bundle`;
  * `support-bundle-verify`;
  * `security-scan`;
  * `redaction-self-test`.

### Belangrijkste gat na Roadmap 089

Na Roadmap 089 zijn releases en migraties veilig, maar de dagelijkse bouwflow kan nog sneller en minder foutgevoelig:

* \[ ] Codex krijgt nog geen automatisch gegenereerde taakpakketten per roadmapfase.
* \[ ] Er is nog geen machine-readable roadmap index.
* \[ ] Er is nog geen duplicate-roadmap guard die `Voltooid docs`, `Roadmap docs` en `docs` structureel vergelijkt.
* \[ ] Er is nog geen dependency graph tussen roadmaps, modules, tests en evidence.
* \[ ] Er is nog geen PR-template generator per roadmapfase.
* \[ ] Er is nog geen roadmap completion validator die checkt of acceptance criteria, tests, docs en evidence compleet zijn.
* \[ ] Er is nog geen veilige mover van `Roadmap docs` naar `Voltooid docs` met evidence.
* \[ ] Er is nog geen Codex prompt pack dat precies zegt welke files wel/niet geraakt mogen worden.
* \[ ] Er is nog geen dashboard voor roadmap-uitvoering en voortgang.
* \[ ] Er is nog geen lokale roadmap quality gate.

Roadmap 090 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 090

Maak een lokale roadmap-execution laag:

```text
Roadmap docs
→ roadmap index
→ dependency graph
→ Codex task packs
→ PR templates
→ implementation checklist
→ validation/evidence
→ completion gate
→ move to Voltooid docs
→ release notes input
```

Na Roadmap 090 moet de bot kunnen:

* \[ ] alle roadmapbestanden indexeren;
* \[ ] hoogste roadmapnummer bepalen;
* \[ ] duplicate/overlap detecteren;
* \[ ] per roadmap fase Codex task packs genereren;
* \[ ] per task duidelijke file boundaries geven;
* \[ ] tests/evidence per fase koppelen;
* \[ ] roadmap completion status berekenen;
* \[ ] roadmap evidence bundle maken;
* \[ ] roadmap veilig naar `Voltooid docs` verplaatsen;
* \[ ] release notes input leveren aan Roadmap 089;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe trading/runtime engine.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen Binance account endpoints.
* \[ ] Geen order endpoints.
* \[ ] Geen cloud project management tool.
* \[ ] Geen GitHub write automation zonder operator confirm.
* \[ ] Geen automatische codewijzigingen buiten task scope.
* \[ ] Geen roadmap verplaatsen zonder evidence.
* \[ ] Geen oude roadmaps overschrijven.

Wel doen:

* \[ ] lokale roadmap parser/indexer maken;
* \[ ] duplicate work guard toevoegen;
* \[ ] Codex task packs genereren;
* \[ ] PR templates genereren;
* \[ ] roadmap evidence checken;
* \[ ] dashboard/CLI toevoegen;
* \[ ] `Roadmap docs` → `Voltooid docs` flow veilig maken;
* \[ ] koppeling maken met release/evidence tooling.

\---

## 3\. Fase 0 - Roadmap Execution Safety Contract

Nieuwe doc:

```text
docs/roadmap-execution-safety-contract.md
```

Regels:

* \[ ] Roadmap tooling is local-only.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen order/account endpoints.
* \[ ] Geen remote GitHub write zonder explicit operator step.
* \[ ] Geen roadmap verplaatsen zonder completion gate.
* \[ ] Geen roadmapnummer hergebruiken.
* \[ ] Geen overlap bouwen als `Voltooid docs` al hetzelfde bevat.
* \[ ] Codex task packs moeten file boundaries hebben.
* \[ ] Codex task packs moeten safety constraints hebben.
* \[ ] Roadmap evidence moet secret-free zijn.
* \[ ] Completion gate moet check-all en relevante tests vereisen.
* \[ ] Browser smoke vereist voor dashboard-roadmaps.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen duplicate roadmap number wordt geblokkeerd.
* \[ ] Tests bewijzen completion mover faalt zonder evidence.
* \[ ] Roadmap tooling output bevat `live\_trading\_enabled=False`.
* \[ ] Dashboard toont `ROADMAP EXECUTION ONLY`.

\---

## 4\. Fase 1 - Roadmap File Indexer

Nieuwe module:

```text
src/binance\_spot\_bot/roadmap\_index.py
```

Dataclasses:

* \[ ] `RoadmapFile`
* \[ ] `RoadmapIndex`
* \[ ] `RoadmapLocation`
* \[ ] `RoadmapParseResult`
* \[ ] `RoadmapNumberStatus`

Te indexeren locaties:

* \[ ] `Voltooid docs/`
* \[ ] `Roadmap docs/`
* \[ ] `docs/`
* \[ ] `docs/runbooks/`
* \[ ] optioneel root docs indien roadmap-like naam.

Velden per roadmap:

* \[ ] number;
* \[ ] title;
* \[ ] status;
* \[ ] path;
* \[ ] location;
* \[ ] modified\_at;
* \[ ] sha256;
* \[ ] follows\_on;
* \[ ] definition\_of\_done count;
* \[ ] checkbox count;
* \[ ] unchecked count;
* \[ ] checked count;
* \[ ] linked tests;
* \[ ] linked docs;
* \[ ] linked modules.

Acceptatiecriteria:

* \[ ] Indexer vindt roadmaps in `Voltooid docs`.
* \[ ] Indexer vindt roadmaps in `Roadmap docs`.
* \[ ] Indexer detecteert dubbele nummers.
* \[ ] Indexer werkt offline.
* \[ ] Output is JSON-serializable en secret-free.

\---

## 5\. Fase 2 - Roadmap Number \& Duplicate Guard

Nieuwe module:

```text
src/binance\_spot\_bot/roadmap\_duplicate\_guard.py
```

Checks:

* \[ ] hoogste roadmapnummer;
* \[ ] ontbrekende nummers;
* \[ ] dubbele nummers;
* \[ ] duplicate titles;
* \[ ] roadmap in `Roadmap docs` die al in `Voltooid docs` bestaat;
* \[ ] roadmap met zelfde thema/keywords als eerdere roadmaps;
* \[ ] mismatch tussen bestandsnaam en titelnummer;
* \[ ] roadmap zonder status;
* \[ ] roadmap zonder Definition of Done;
* \[ ] roadmap zonder acceptance criteria.

Output:

* \[ ] `duplicate\_guard\_report.json`
* \[ ] `duplicate\_guard\_report.md`

Acceptatiecriteria:

* \[ ] Guard blokkeert nieuw roadmapnummer als het al bestaat.
* \[ ] Guard geeft volgend vrije nummer.
* \[ ] Guard geeft overlap warnings.
* \[ ] Guard kan door CLI worden gebruikt vóór nieuwe roadmap wordt gemaakt.
* \[ ] Tests gebruiken fixture roadmaps.

\---

## 6\. Fase 3 - Roadmap Dependency Graph

Nieuwe module:

```text
src/binance\_spot\_bot/roadmap\_dependency\_graph.py
```

Nodes:

* \[ ] roadmap;
* \[ ] module;
* \[ ] test file;
* \[ ] docs file;
* \[ ] CLI command;
* \[ ] dashboard panel;
* \[ ] evidence artifact;
* \[ ] release artifact.

Edges:

* \[ ] follows\_on;
* \[ ] implements;
* \[ ] validates;
* \[ ] documents;
* \[ ] depends\_on;
* \[ ] produces\_evidence;
* \[ ] moves\_to\_completed;
* \[ ] feeds\_release\_notes.

Output:

```text
data/roadmaps/graph/
  roadmap\_graph.json
  roadmap\_graph.md
  roadmap\_dependencies.csv
```

Acceptatiecriteria:

* \[ ] Graph kan Roadmap 076-090 koppelen.
* \[ ] Graph toont welke modules/tests per roadmap horen.
* \[ ] Graph detecteert missing tests.
* \[ ] Graph detecteert unlinked docs.
* \[ ] Dashboard kan graph summary tonen.

\---

## 7\. Fase 4 - Codex Task Pack Schema

Nieuwe module:

```text
src/binance\_spot\_bot/codex\_task\_packs.py
```

Dataclasses:

* \[ ] `CodexTaskPack`
* \[ ] `CodexTask`
* \[ ] `CodexFileBoundary`
* \[ ] `CodexSafetyConstraint`
* \[ ] `CodexValidationCommand`
* \[ ] `CodexExpectedArtifact`
* \[ ] `CodexCompletionChecklist`

Task pack velden:

* \[ ] task\_pack\_id;
* \[ ] roadmap\_number;
* \[ ] roadmap\_title;
* \[ ] phase;
* \[ ] pr\_number;
* \[ ] goal;
* \[ ] allowed\_files;
* \[ ] forbidden\_files;
* \[ ] required\_tests;
* \[ ] required\_docs;
* \[ ] required\_evidence;
* \[ ] safety\_constraints;
* \[ ] commands\_to\_run;
* \[ ] acceptance\_criteria;
* \[ ] rollback\_notes;
* \[ ] no\_live\_statement.

Acceptatiecriteria:

* \[ ] Task packs zijn JSON + Markdown.
* \[ ] Elk task pack bevat allowed/forbidden files.
* \[ ] Elk task pack bevat safety constraints.
* \[ ] Elk task pack bevat tests.
* \[ ] Geen task pack mag live/signed/order/account toestaan.

\---

## 8\. Fase 5 - Task Pack Generator

Nieuwe module:

```text
src/binance\_spot\_bot/codex\_task\_pack\_generator.py
```

Inputs:

* \[ ] roadmap markdown;
* \[ ] roadmap dependency graph;
* \[ ] existing module index;
* \[ ] existing test index;
* \[ ] safety contract;
* \[ ] release/migration context.

Output:

```text
data/roadmaps/task-packs/<roadmap\_number>/
  pr-01-task-pack.md
  pr-01-task-pack.json
  pr-02-task-pack.md
  pr-02-task-pack.json
```

Generatorregels:

* \[ ] Maak één task pack per PR/fase.
* \[ ] Begin met de kleinste foundation PR.
* \[ ] Voeg expliciete file boundaries toe.
* \[ ] Voeg test commands toe.
* \[ ] Voeg no-live constraints toe.
* \[ ] Voeg “niet bouwen” scope toe.
* \[ ] Voeg evidence outputs toe.
* \[ ] Voeg rollback notes toe.

Acceptatiecriteria:

* \[ ] Generator kan Roadmap 089/090 task packs maken.
* \[ ] Task packs zijn copy-paste klaar voor Codex.
* \[ ] Task packs bevatten geen secrets.
* \[ ] Task packs vermijden te brede scopes.
* \[ ] Tests valideren minimaal 3 sample roadmaps.

\---

## 9\. Fase 6 - PR Template Generator

Nieuwe module:

```text
src/binance\_spot\_bot/pr\_template\_generator.py
```

Template types:

* \[ ] feature PR;
* \[ ] dashboard PR;
* \[ ] CLI PR;
* \[ ] docs PR;
* \[ ] migration PR;
* \[ ] security/redaction PR;
* \[ ] roadmap completion PR;
* \[ ] release PR.

PR template secties:

* \[ ] Roadmap link;
* \[ ] Phase/PR number;
* \[ ] Summary;
* \[ ] Changed files;
* \[ ] Safety constraints;
* \[ ] Tests run;
* \[ ] Evidence generated;
* \[ ] Screenshots if dashboard;
* \[ ] Migration notes;
* \[ ] Rollback notes;
* \[ ] No-live confirmation;
* \[ ] Checklist.

Acceptatiecriteria:

* \[ ] PR templates zijn Markdown.
* \[ ] Template kiest juiste type op basis van roadmapfase.
* \[ ] Dashboard PR vereist smoke/browser smoke.
* \[ ] Migration PR vereist backup/dry-run.
* \[ ] Security PR vereist redaction/security scan.

\---

## 10\. Fase 7 - Roadmap Validation Engine

Nieuwe module:

```text
src/binance\_spot\_bot/roadmap\_validation.py
```

Validaties:

* \[ ] roadmap heeft status;
* \[ ] roadmap heeft opvolgrelatie;
* \[ ] roadmap heeft phases;
* \[ ] roadmap heeft Definition of Done;
* \[ ] roadmap heeft tests sectie;
* \[ ] roadmap heeft docs sectie;
* \[ ] roadmap heeft safety constraints;
* \[ ] roadmap heeft beste eerste Codex-opdracht;
* \[ ] roadmapnummer klopt met bestandsnaam;
* \[ ] geen duplicate nummer;
* \[ ] checkboxes zijn parsebaar;
* \[ ] linked tests bestaan of zijn gepland;
* \[ ] linked modules bestaan of zijn gepland;
* \[ ] no-live statement aanwezig.

Acceptatiecriteria:

* \[ ] Validation report is JSON/Markdown.
* \[ ] Invalid roadmap krijgt blockers.
* \[ ] Report kan gebruikt worden vóór nieuwe roadmap wordt aangenomen.
* \[ ] Tests dekken incomplete roadmap fixtures.
* \[ ] Output is secret-free.

\---

## 11\. Fase 8 - Roadmap Completion Gate

Nieuwe module:

```text
src/binance\_spot\_bot/roadmap\_completion\_gate.py
```

Completion checks:

* \[ ] all required phases done;
* \[ ] all acceptance criteria checked;
* \[ ] required tests passed;
* \[ ] check-all passed;
* \[ ] dashboard smoke passed if UI touched;
* \[ ] browser smoke passed if dashboard touched;
* \[ ] docs updated;
* \[ ] evidence manifest generated;
* \[ ] support bundle optional generated;
* \[ ] no-live proof present;
* \[ ] roadmap status ready for completed;
* \[ ] release notes input generated if code changed.

Status:

* \[ ] blocked;
* \[ ] needs\_tests;
* \[ ] needs\_docs;
* \[ ] needs\_evidence;
* \[ ] ready\_to\_complete.

Acceptatiecriteria:

* \[ ] Completion gate blocks incomplete roadmaps.
* \[ ] Completion gate detects missing check-all.
* \[ ] Completion gate detects missing browser smoke for dashboard roadmaps.
* \[ ] Completion gate requires no-live proof.
* \[ ] Tests use fixture evidence.

\---

## 12\. Fase 9 - Completed Roadmap Mover

Nieuwe module:

```text
src/binance\_spot\_bot/roadmap\_mover.py
```

Flow:

* \[ ] load roadmap from `Roadmap docs`;
* \[ ] run duplicate guard;
* \[ ] run validation;
* \[ ] run completion gate;
* \[ ] generate completion report;
* \[ ] update status to `Voltooid`;
* \[ ] move file to `Voltooid docs`;
* \[ ] write move manifest;
* \[ ] write evidence link;
* \[ ] update roadmap index;
* \[ ] optionally generate release notes input.

Guardrails:

* \[ ] dry-run default;
* \[ ] exact confirm phrase required for move;
* \[ ] never overwrite existing completed roadmap;
* \[ ] no-live proof required;
* \[ ] hash before/after;
* \[ ] rollback instructions.

Acceptatiecriteria:

* \[ ] Dry-run shows exact move.
* \[ ] Move fails if target exists.
* \[ ] Move fails if completion gate blocked.
* \[ ] Move manifest is created.
* \[ ] Tests use temp dirs.

\---

## 13\. Fase 10 - Roadmap Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/roadmap\_evidence\_bundle.py
```

Bundle bevat:

* \[ ] roadmap file;
* \[ ] roadmap validation report;
* \[ ] task packs;
* \[ ] PR templates;
* \[ ] test outputs;
* \[ ] check-all output;
* \[ ] dashboard smoke/browser smoke output;
* \[ ] docs changed summary;
* \[ ] completion gate report;
* \[ ] move manifest;
* \[ ] no-live proof;
* \[ ] release notes input;
* \[ ] hashes.

Output:

```text
data/roadmaps/evidence/<roadmap\_number>/
  roadmap\_evidence\_manifest.json
  roadmap\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle links to release evidence.
* \[ ] Dashboard/CLI export works.

\---

## 14\. Fase 11 - Roadmap Execution CLI

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli roadmap-index
python -m binance\_spot\_bot.cli roadmap-next-number
python -m binance\_spot\_bot.cli roadmap-duplicate-guard --number 090
python -m binance\_spot\_bot.cli roadmap-validate --file "Roadmap docs/090-roadmap-..."
python -m binance\_spot\_bot.cli roadmap-graph
python -m binance\_spot\_bot.cli codex-task-packs --roadmap 090
python -m binance\_spot\_bot.cli pr-template --roadmap 090 --phase 1
python -m binance\_spot\_bot.cli roadmap-completion-gate --roadmap 090
python -m binance\_spot\_bot.cli roadmap-move-completed --roadmap 090 --confirm MOVE\_ROADMAP\_TO\_VOLTOOID
python -m binance\_spot\_bot.cli roadmap-evidence-export --roadmap 090
```

Acceptatiecriteria:

* \[ ] Commands werken offline.
* \[ ] Commands ondersteunen JSON output.
* \[ ] Move command vereist confirm.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Reports zijn secret-free.

\---

## 15\. Fase 12 - Roadmap Execution Dashboard

Nieuwe dashboardsectie:

```text
Roadmap Execution
```

Panels:

* \[ ] roadmap index;
* \[ ] next roadmap number;
* \[ ] duplicate guard status;
* \[ ] roadmap validation status;
* \[ ] roadmap dependency graph summary;
* \[ ] task pack generator;
* \[ ] PR template generator;
* \[ ] completion gate;
* \[ ] evidence bundle;
* \[ ] move to completed dry-run;
* \[ ] no-live proof.

Actions:

* \[ ] refresh roadmap index;
* \[ ] validate selected roadmap;
* \[ ] generate task packs;
* \[ ] generate PR template;
* \[ ] run completion gate;
* \[ ] export evidence;
* \[ ] dry-run move to completed;
* \[ ] confirmed move to completed.

Safeguards:

* \[ ] Move button hidden until completion gate ready.
* \[ ] Exact confirm phrase required.
* \[ ] No live controls.
* \[ ] Raw JSON only in debug expanders.
* \[ ] Stable widget keys.
* \[ ] Browser smoke covers panel.

Acceptatiecriteria:

* \[ ] Dashboard shows `ROADMAP EXECUTION ONLY`.
* \[ ] Dashboard detects duplicate numbers.
* \[ ] Dashboard cannot move blocked roadmap.
* \[ ] Task packs downloadable.
* \[ ] Browser smoke passes.

\---

## 16\. Fase 13 - Codex Prompt Library

Nieuwe map:

```text
docs/codex-prompts/
```

Prompts:

* \[ ] foundation module PR;
* \[ ] CLI PR;
* \[ ] dashboard PR;
* \[ ] tests-only PR;
* \[ ] docs PR;
* \[ ] migration PR;
* \[ ] security/redaction PR;
* \[ ] evidence/report PR;
* \[ ] roadmap completion PR;
* \[ ] bugfix PR.

Elke prompt bevat:

* \[ ] task goal;
* \[ ] allowed files;
* \[ ] forbidden files;
* \[ ] tests to run;
* \[ ] safety constraints;
* \[ ] no-live statement;
* \[ ] expected output;
* \[ ] do-not-overbuild section.

Acceptatiecriteria:

* \[ ] Prompt library bestaat.
* \[ ] Prompts zijn generiek en roadmap-parametriseerbaar.
* \[ ] Prompts bevatten no-live constraints.
* \[ ] Prompts bevatten test/evidence requirements.
* \[ ] Docs leggen uit hoe ze in Codex gebruikt worden.

\---

## 17\. Fase 14 - Roadmap Quality Score

Nieuwe module:

```text
src/binance\_spot\_bot/roadmap\_quality\_score.py
```

Scorecategorieën:

* \[ ] completeness;
* \[ ] phase clarity;
* \[ ] test coverage clarity;
* \[ ] evidence clarity;
* \[ ] safety clarity;
* \[ ] file boundary clarity;
* \[ ] dependency clarity;
* \[ ] duplicate risk;
* \[ ] execution readiness;
* \[ ] release readiness.

Grades:

* \[ ] A: ready for Codex;
* \[ ] B: usable;
* \[ ] C: needs refinement;
* \[ ] D: weak;
* \[ ] F: blocked.

Hard blockers:

* \[ ] duplicate roadmap number;
* \[ ] no safety constraints;
* \[ ] no tests;
* \[ ] no Definition of Done;
* \[ ] no no-live statement;
* \[ ] missing completion gate.

Acceptatiecriteria:

* \[ ] Score explains penalties.
* \[ ] Hard blockers force F/blocked.
* \[ ] Dashboard can show score.
* \[ ] Tests cover weak/strong fixtures.
* \[ ] Score output is secret-free.

\---

## 18\. Fase 15 - Roadmap Release Integration

Doel: Roadmap 090 voedt Roadmap 089 release tooling.

Nieuwe module:

```text
src/binance\_spot\_bot/roadmap\_release\_integration.py
```

Taken:

* \[ ] changed roadmap list exporteren;
* \[ ] completed roadmap summary maken;
* \[ ] task pack summary maken;
* \[ ] evidence summary maken;
* \[ ] release notes input genereren;
* \[ ] migration-roadmap marker detecteren;
* \[ ] dashboard-roadmap marker detecteren;
* \[ ] required validation commands voorstellen.

Output:

```text
data/roadmaps/release-input/
  roadmap-release-input.json
  roadmap-release-input.md
```

Acceptatiecriteria:

* \[ ] Release notes generator kan roadmap input gebruiken.
* \[ ] Completed roadmaps worden samengevat.
* \[ ] Dashboard changes worden gemarkeerd.
* \[ ] Migration changes worden gemarkeerd.
* \[ ] Output is secret-free.

\---

## 19\. Fase 16 - Roadmap Execution Reports

Nieuwe module:

```text
src/binance\_spot\_bot/roadmap\_execution\_report.py
```

Reports:

Daily:

* \[ ] active roadmaps;
* \[ ] blocked roadmaps;
* \[ ] task packs generated;
* \[ ] tests/evidence missing;
* \[ ] duplicate risk;
* \[ ] next Codex task.

Per roadmap:

* \[ ] status;
* \[ ] progress;
* \[ ] blockers;
* \[ ] generated task packs;
* \[ ] validation status;
* \[ ] completion readiness;
* \[ ] release readiness.

Output:

```text
data/roadmaps/reports/
  daily/
  roadmap-090/
```

Acceptatiecriteria:

* \[ ] Reports zijn Markdown + JSON.
* \[ ] Reports zijn secret-free.
* \[ ] Reports kunnen scheduled worden door Roadmap 083.
* \[ ] Reports voeden Roadmap 084 metrics.
* \[ ] Dashboard kan reports downloaden.

\---

## 20\. Fase 17 - Tests

### Unit tests

* \[ ] `tests/test\_roadmap\_index.py`
* \[ ] `tests/test\_roadmap\_duplicate\_guard.py`
* \[ ] `tests/test\_roadmap\_dependency\_graph.py`
* \[ ] `tests/test\_codex\_task\_packs.py`
* \[ ] `tests/test\_codex\_task\_pack\_generator.py`
* \[ ] `tests/test\_pr\_template\_generator.py`
* \[ ] `tests/test\_roadmap\_validation.py`
* \[ ] `tests/test\_roadmap\_completion\_gate.py`
* \[ ] `tests/test\_roadmap\_mover.py`
* \[ ] `tests/test\_roadmap\_evidence\_bundle.py`
* \[ ] `tests/test\_roadmap\_quality\_score.py`
* \[ ] `tests/test\_roadmap\_release\_integration.py`
* \[ ] `tests/test\_roadmap\_execution\_report.py`

### Integration tests

* \[ ] Build roadmap index from fixture dirs.
* \[ ] Detect duplicate roadmap number.
* \[ ] Generate dependency graph.
* \[ ] Generate Codex task packs.
* \[ ] Generate PR template.
* \[ ] Validate incomplete roadmap.
* \[ ] Validate complete roadmap.
* \[ ] Run completion gate with fake evidence.
* \[ ] Dry-run move to completed.
* \[ ] Export roadmap evidence bundle.
* \[ ] Generate release input.

### Safety tests

* \[ ] Duplicate number blocked.
* \[ ] Completion move blocked without check-all evidence.
* \[ ] Dashboard roadmap requires smoke evidence.
* \[ ] Task pack cannot allow live trading.
* \[ ] Task pack cannot allow signed/order/account endpoints.
* \[ ] Move cannot overwrite existing completed roadmap.
* \[ ] Reports contain no secrets.
* \[ ] No-live proof remains true.

\---

## 21\. Docs

Nieuwe docs:

* \[ ] `docs/roadmap-execution-safety-contract.md`
* \[ ] `docs/roadmap-indexer.md`
* \[ ] `docs/roadmap-duplicate-guard.md`
* \[ ] `docs/roadmap-dependency-graph.md`
* \[ ] `docs/codex-task-packs.md`
* \[ ] `docs/codex-task-pack-generator.md`
* \[ ] `docs/pr-template-generator.md`
* \[ ] `docs/roadmap-validation-engine.md`
* \[ ] `docs/roadmap-completion-gate.md`
* \[ ] `docs/completed-roadmap-mover.md`
* \[ ] `docs/roadmap-evidence-bundle.md`
* \[ ] `docs/roadmap-execution-cli.md`
* \[ ] `docs/roadmap-execution-dashboard.md`
* \[ ] `docs/codex-prompt-library.md`
* \[ ] `docs/roadmap-quality-score.md`
* \[ ] `docs/roadmap-release-integration.md`

README updates:

* \[ ] roadmap workflow;
* \[ ] how to choose next roadmap number;
* \[ ] how to generate Codex task packs;
* \[ ] how to run completion gate;
* \[ ] how to move to `Voltooid docs`;
* \[ ] no-live statement.

\---

## 22\. CLI command examples

### Bepaal volgende roadmapnummer

```powershell
python -m binance\_spot\_bot.cli roadmap-next-number --json
```

### Valideer roadmap

```powershell
python -m binance\_spot\_bot.cli roadmap-validate --file "Roadmap docs/090-roadmap-developer-experience-codex-task-packs-roadmap-execution-automation.md" --json
```

### Genereer Codex task packs

```powershell
python -m binance\_spot\_bot.cli codex-task-packs --roadmap 090
```

### Run completion gate

```powershell
python -m binance\_spot\_bot.cli roadmap-completion-gate --roadmap 090 --json
```

### Dry-run move naar voltooid

```powershell
python -m binance\_spot\_bot.cli roadmap-move-completed --roadmap 090 --dry-run
```

### Confirmed move

```powershell
python -m binance\_spot\_bot.cli roadmap-move-completed --roadmap 090 --confirm MOVE\_ROADMAP\_TO\_VOLTOOID
```

\---

## 23\. Codex bouwvolgorde

### PR 1 - Roadmap Indexer + Duplicate Guard

* \[ ] `roadmap\_index.py`
* \[ ] `roadmap\_duplicate\_guard.py`
* \[ ] fixture tests.
* \[ ] next number output.

### PR 2 - Roadmap Dependency Graph

* \[ ] `roadmap\_dependency\_graph.py`
* \[ ] graph output.
* \[ ] missing tests/docs detection.

### PR 3 - Codex Task Pack Schema

* \[ ] `codex\_task\_packs.py`
* \[ ] JSON/Markdown task packs.
* \[ ] no-live validation.

### PR 4 - Task Pack Generator

* \[ ] `codex\_task\_pack\_generator.py`
* \[ ] roadmap phase extraction.
* \[ ] PR/fase task generation.

### PR 5 - PR Template Generator

* \[ ] `pr\_template\_generator.py`
* \[ ] dashboard/CLI/docs/migration templates.
* \[ ] tests.

### PR 6 - Roadmap Validation Engine

* \[ ] `roadmap\_validation.py`
* \[ ] validation report.
* \[ ] tests.

### PR 7 - Completion Gate + Mover

* \[ ] `roadmap\_completion\_gate.py`
* \[ ] `roadmap\_mover.py`
* \[ ] dry-run/confirm move.
* \[ ] tests.

### PR 8 - Roadmap Evidence Bundle

* \[ ] `roadmap\_evidence\_bundle.py`
* \[ ] evidence manifest.
* \[ ] verification.

### PR 9 - CLI + Dashboard

* \[ ] roadmap execution CLI.
* \[ ] dashboard panel.
* \[ ] browser smoke.

### PR 10 - Prompt Library + Quality Score + Release Integration

* \[ ] `roadmap\_quality\_score.py`
* \[ ] `roadmap\_release\_integration.py`
* \[ ] prompt library docs.
* \[ ] execution reports.

\---

## 24\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 090 PR 1: Roadmap Indexer + Duplicate Guard.

Maak src/binance\_spot\_bot/roadmap\_index.py met:
- RoadmapFile
- RoadmapIndex
- RoadmapLocation
- RoadmapParseResult
- RoadmapNumberStatus
- build\_roadmap\_index(root: Path)
- find\_next\_roadmap\_number(index)

Maak src/binance\_spot\_bot/roadmap\_duplicate\_guard.py met:
- detect duplicate roadmap numbers
- detect mismatch tussen bestandsnaamnummer en titelnummer
- detect roadmap in Roadmap docs die al in Voltooid docs staat
- report highest existing roadmap number
- propose next free number

Scan minimaal:
- Voltooid docs/
- Roadmap docs/
- docs/

Voeg tests toe met fixture directories voor:
- Roadmap 075 in Voltooid docs
- Roadmap 089 in Roadmap docs
- duplicate Roadmap 089 in Voltooid docs
- missing status
- filename/title mismatch
- next number = 090

Geen GitHub API calls.
Geen dashboard.
Geen mover.
Geen signed endpoints.
Geen orders.
Geen live trading.
Output moet secret-free zijn en live\_trading\_enabled=False bevatten.
```

Waarom eerst:

* De gebruiker wil altijd eerst `Voltooid docs` en `Roadmap docs` controleren.
* Duplicate roadmapnummers waren eerder een echte fout.
* Roadmap index + duplicate guard voorkomt dubbel bouwen.
* Het raakt geen trading runtime.
* Het is klein genoeg voor Codex en direct testbaar.

\---

## 25\. Definition of Done

Roadmap 090 is klaar als:

* \[ ] Roadmap Execution Safety Contract bestaat.
* \[ ] Roadmap File Indexer werkt.
* \[ ] Roadmap Number \& Duplicate Guard werkt.
* \[ ] Roadmap Dependency Graph werkt.
* \[ ] Codex Task Pack Schema werkt.
* \[ ] Task Pack Generator werkt.
* \[ ] PR Template Generator werkt.
* \[ ] Roadmap Validation Engine werkt.
* \[ ] Roadmap Completion Gate werkt.
* \[ ] Completed Roadmap Mover werkt.
* \[ ] Roadmap Evidence Bundle werkt.
* \[ ] Roadmap Execution CLI werkt.
* \[ ] Roadmap Execution Dashboard werkt.
* \[ ] Codex Prompt Library bestaat.
* \[ ] Roadmap Quality Score werkt.
* \[ ] Roadmap Release Integration werkt.
* \[ ] Roadmap Execution Reports werken.
* \[ ] Tests bewijzen duplicate roadmaps worden geblokkeerd.
* \[ ] Tests bewijzen mover niet werkt zonder evidence.
* \[ ] Tests bewijzen task packs geen live/signed/order/account toestaan.
* \[ ] Reports/bundles zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 090 kan na uitvoering naar `Voltooid docs`.

\---

## 26\. Verwachte Roadmap 091 daarna

Na Roadmap 090 zou Roadmap 091 logisch focussen op:

```text
Roadmap 091 - Repository Knowledge Graph, Code Ownership Maps \& Impact Analysis
```

Mogelijke inhoud:

* \[ ] code ownership map;
* \[ ] module dependency graph;
* \[ ] impact analysis per change;
* \[ ] test selection by changed files;
* \[ ] docs/code consistency checker;
* \[ ] roadmap-to-code traceability;
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

Gebouwd: roadmap indexer, duplicate guard, dependency graph, Codex task pack schema/generator, PR template generator, validation engine, completion gate, completed-roadmap mover, evidence bundle, CLI commands, dashboard panel, prompt library, quality score, release integration en execution reports.

Validatie: tests/test_roadmap_090_roadmap_execution_acceptance.py; tests/test_roadmaps_089_096_full_surface.py; roadmap CLI flow; python -m binance_spot_bot.cli check-all --skip-tests --json; python -m pytest -q; python -m binance_spot_bot.cli dashboard-smoke --seconds 1; python -m binance_spot_bot.cli dashboard-browser-smoke --url http://127.0.0.1:8506/ --seconds 10.

Safety: lokaal/paper-only, geen live trading enablement.

