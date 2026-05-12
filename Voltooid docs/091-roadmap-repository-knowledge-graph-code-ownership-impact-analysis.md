# Roadmap 091 - Repository Knowledge Graph, Code Ownership Maps \& Impact Analysis

Status: Voltooid na hercontrole en volledige validatie  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/091-roadmap-repository-knowledge-graph-code-ownership-impact-analysis.md
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

Doel: Roadmap 090 maakt roadmap execution, duplicate guards, Codex task packs, PR templates en roadmap completion gates mogelijk. Roadmap 091 bouwt daarop een **Repository Knowledge Graph**: een lokale kennislaag die code, tests, docs, roadmaps, CLI commands, dashboardpanelen, data artifacts, safety constraints en evidence aan elkaar koppelt. Daardoor kan de bot vóór elke wijziging voorspellen welke onderdelen geraakt worden, welke tests nodig zijn, welke docs aangepast moeten worden en waar risico op dubbele bouw of regressie zit.

Live trading blijft volledig buiten scope.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 091`, `091-roadmap`, `Repository Knowledge Graph`, `Code Ownership Maps`, `Impact Analysis` en `test selection`.
* \[x] Geen bestaande Roadmap 091 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 090 is lokaal aangemaakt als Developer Experience, Codex Task Packs \& Roadmap Execution Automation.
* \[x] Roadmap 075 bevestigt dat check-all, browser smoke, roadmapverplaatsing naar `Voltooid docs` en live trading disabled al onderdeel van de workflow waren.

### Codebasecontrole

Breed bekeken:

* \[x] `pyproject.toml`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/evaluation.py`
* \[x] `src/binance\_spot\_bot/ui/streamlit\_app.py`
* \[x] bestaande operator/evidence/security tooling
* \[x] bestaande tests/check-all workflow
* \[x] bestaande roadmap workflow tot en met Roadmap 090

### Belangrijke bestaande basis

De codebase heeft inmiddels duidelijke lagen:

* \[x] Packaging en entrypoint via `pyproject.toml`.
* \[x] Grote CLI-laag met veel commands voor runtime, paper/demo, dashboard, diagnostics, support bundles, evidence, security, check-all, operator quality gates en demo execution.
* \[x] Runtime-laag met `BotRuntime`, `RuntimeOptions`, `RuntimeSnapshot`, demo/paper/testnet-readiness modes, data sources, risk engine, paper accounting, session reports en demo pilot.
* \[x] Dashboard-laag met Streamlit, veel tabs/panels, demo spot trading, risk controls, evaluation, research, portfolio, readiness, logs/security en demo pilot.
* \[x] Operator/evidence-laag met artifact catalog, evidence chain, local ops snapshot, operator report, redaction self-test, support bundle verify, report index, data growth budget en quality gate.
* \[x] Evaluation-laag met walk-forward evaluation, dataset manifests, leakage guard, baseline/candidate comparison en costs.
* \[x] Check-all-laag met tests, config validation, preflight, security scan, dashboard import, diagnostics, support bundle, operator quality gate, local ops snapshot, pilot smoke, no-live UI en ruff.

### Belangrijkste gat na Roadmap 090

Na Roadmap 090 kan de roadmapuitvoering zelf beter georganiseerd worden. Wat dan nog mist:

* \[ ] een volledig overzicht van alle modules en hun afhankelijkheden;
* \[ ] welke CLI command bij welke module hoort;
* \[ ] welke dashboard tab/panel bij welke module hoort;
* \[ ] welke tests welke modules dekken;
* \[ ] welke roadmaps welke modules hebben geïntroduceerd;
* \[ ] welke docs bij welke code horen;
* \[ ] welke artifacts door welke command/module worden geproduceerd;
* \[ ] impactanalyse bij wijziging van een bestand;
* \[ ] testselectie op basis van changed files;
* \[ ] waarschuwing als een wijziging safety/no-live gebieden raakt;
* \[ ] code ownership map per domein;
* \[ ] traceability van roadmap → code → tests → evidence → release notes.

Roadmap 091 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 091

Maak een lokale repository knowledge graph:

```text
Codebase
→ file inventory
→ Python import graph
→ CLI command graph
→ dashboard graph
→ test coverage map
→ docs/roadmap traceability
→ ownership map
→ impact analysis
→ recommended tests/docs/evidence
```

Na Roadmap 091 moet je kunnen vragen:

* \[ ] “Welke modules worden geraakt als ik `runtime.py` wijzig?”
* \[ ] “Welke tests moet Codex draaien als `operator\_ops.py` verandert?”
* \[ ] “Welke dashboardpanelen gebruiken `SpotPreview`?”
* \[ ] “Welke CLI commands schrijven naar `data/evidence`?”
* \[ ] “Welke roadmap introduceerde deze module?”
* \[ ] “Welke docs ontbreken voor deze module?”
* \[ ] “Welke safety checks moeten verplicht draaien na deze wijziging?”
* \[ ] “Welke modules zijn te centraal/monolithisch?”
* \[ ] “Welke PR task pack moet generated worden voor deze wijziging?”
* \[ ] “Welke release notes secties moeten worden bijgewerkt?”

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe roadmap execution engine; Roadmap 090 doet dat.
* \[ ] Geen release manager opnieuw bouwen; Roadmap 089 doet dat.
* \[ ] Geen observability warehouse opnieuw bouwen; Roadmap 084 doet dat.
* \[ ] Geen AI/Ops assistant opnieuw bouwen; Roadmap 085 doet dat.
* \[ ] Geen Action Center opnieuw bouwen; Roadmap 086 doet dat.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen Binance account endpoints.
* \[ ] Geen order endpoints.
* \[ ] Geen cloud dependency graph service.
* \[ ] Geen remote telemetry.
* \[ ] Geen GitHub write actions zonder operator confirmation.

Wel doen:

* \[ ] codebase lokaal analyseren;
* \[ ] AST/static import graph bouwen;
* \[ ] CLI commands mappen;
* \[ ] dashboard panels mappen;
* \[ ] tests mappen;
* \[ ] docs/roadmaps mappen;
* \[ ] ownership domeinen voorstellen;
* \[ ] impactanalyse toevoegen;
* \[ ] recommended tests/evidence genereren;
* \[ ] dashboard/CLI toevoegen;
* \[ ] alles local-only en no-live houden.

\---

## 3\. Fase 0 - Repository Knowledge Safety Contract

Nieuwe doc:

```text
docs/repository-knowledge-graph-safety-contract.md
```

Regels:

* \[ ] Knowledge graph tooling is local-only.
* \[ ] Geen remote telemetry.
* \[ ] Geen remote upload.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen order endpoints.
* \[ ] Analysis is read-only by default.
* \[ ] Generated recommendations mogen geen code uitvoeren.
* \[ ] Impact recommendations mogen alleen veilige commands voorstellen.
* \[ ] Reports zijn secret-free.
* \[ ] File paths worden relatief waar mogelijk.
* \[ ] Secrets in code/artifacts worden geredact.
* \[ ] No-live proof wordt in reports opgenomen.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen knowledge graph geen network/order/account calls doet.
* \[ ] Output bevat `live\_trading\_enabled=False`.
* \[ ] Dashboard toont `LOCAL REPOSITORY KNOWLEDGE ONLY`.
* \[ ] Reports zijn secret-free.

\---

## 4\. Fase 1 - Repository Inventory Engine

Nieuwe module:

```text
src/binance\_spot\_bot/repo\_inventory.py
```

Dataclasses:

* \[ ] `RepoFile`
* \[ ] `RepoInventory`
* \[ ] `RepoDirectorySummary`
* \[ ] `RepoInventoryManifest`
* \[ ] `RepoInventoryResult`

Te scannen locaties:

* \[ ] `src/`
* \[ ] `tests/`
* \[ ] `docs/`
* \[ ] `Roadmap docs/`
* \[ ] `Voltooid docs/`
* \[ ] `scripts/`
* \[ ] root config files:

  * `pyproject.toml`;
  * `README.md`;
  * `.gitignore`;
  * eventuele configbestanden.

Per bestand:

* \[ ] path;
* \[ ] relative\_path;
* \[ ] suffix;
* \[ ] size\_bytes;
* \[ ] modified\_at;
* \[ ] sha256;
* \[ ] category:

  * source;
  * test;
  * docs;
  * roadmap;
  * completed\_roadmap;
  * script;
  * config;
  * artifact;
  * unknown.
* \[ ] line\_count;
* \[ ] class\_count;
* \[ ] function\_count;
* \[ ] import\_count;
* \[ ] has\_tests\_guess;
* \[ ] safety\_relevant\_guess;
* \[ ] secret\_scan\_status.

Acceptatiecriteria:

* \[ ] Inventory werkt offline.
* \[ ] Inventory is JSON-serializable.
* \[ ] Inventory bevat geen secrets.
* \[ ] Inventory markeert safety-relevante bestanden.
* \[ ] Inventory schrijft manifest met hashes.

\---

## 5\. Fase 2 - Python AST Import \& Symbol Graph

Nieuwe module:

```text
src/binance\_spot\_bot/code\_graph.py
```

Dataclasses:

* \[ ] `PythonModuleNode`
* \[ ] `PythonImportEdge`
* \[ ] `PythonSymbol`
* \[ ] `CodeGraph`
* \[ ] `CodeGraphBuildResult`

Graph nodes:

* \[ ] Python module;
* \[ ] class;
* \[ ] function;
* \[ ] dataclass;
* \[ ] enum;
* \[ ] constant;
* \[ ] import alias.

Graph edges:

* \[ ] imports;
* \[ ] imports\_from;
* \[ ] defines\_class;
* \[ ] defines\_function;
* \[ ] uses\_symbol;
* \[ ] calls\_function waar statisch detecteerbaar;
* \[ ] references\_dataclass;
* \[ ] writes\_artifact waar detecteerbaar;
* \[ ] reads\_artifact waar detecteerbaar.

Analyse:

* \[ ] Parse AST van `src/binance\_spot\_bot/\*\*/\*.py`.
* \[ ] Detecteer interne imports.
* \[ ] Detecteer externe imports.
* \[ ] Detecteer cyclische imports.
* \[ ] Detecteer modules met hoge fan-in.
* \[ ] Detecteer modules met hoge fan-out.
* \[ ] Detecteer grote modules boven configured line count.
* \[ ] Detecteer modules zonder bijpassende tests.

Acceptatiecriteria:

* \[ ] AST parser crasht niet op geldige Python files.
* \[ ] Import graph bevat `cli.py`, `runtime.py`, `operator\_ops.py`, `streamlit\_app.py`, `evaluation.py`.
* \[ ] Circular dependencies worden gerapporteerd.
* \[ ] High fan-in/out modules worden gerapporteerd.
* \[ ] Tests gebruiken fixture packages.

\---

## 6\. Fase 3 - CLI Command Surface Map

Nieuwe module:

```text
src/binance\_spot\_bot/cli\_surface\_map.py
```

Doel: alle commands in `cli.py` automatisch mappen naar modules, handlers en safety class.

Per command:

* \[ ] command name;
* \[ ] arguments;
* \[ ] handler block;
* \[ ] imported modules used;
* \[ ] output type;
* \[ ] writes artifacts yes/no;
* \[ ] reads artifacts yes/no;
* \[ ] safety class:

  * read\_only;
  * artifact\_generation;
  * paper\_demo\_runtime;
  * demo\_execution;
  * migration\_like;
  * destructive\_confirm\_required;
  * forbidden\_if\_live.
* \[ ] required tests;
* \[ ] no-live constraints;
* \[ ] related docs;
* \[ ] related roadmap.

Commands minimaal mappen:

* \[ ] diagnostics;
* \[ ] support-bundle;
* \[ ] support-bundle-verify;
* \[ ] support-bundle-restore-preview;
* \[ ] retention-preview;
* \[ ] state-archive;
* \[ ] operator-report;
* \[ ] operator-quality-gate;
* \[ ] artifact-catalog;
* \[ ] evidence-chain;
* \[ ] evidence-manifest;
* \[ ] redaction-self-test;
* \[ ] local-ops-snapshot;
* \[ ] check-all;
* \[ ] dashboard-smoke;
* \[ ] dashboard-browser-smoke;
* \[ ] demo-execution-preview/test-order/place/query/cancel;
* \[ ] run-local;
* \[ ] paper-session;
* \[ ] evaluate-model;
* \[ ] promote-model;
* \[ ] launch-dashboard;
* \[ ] dashboard.

Acceptatiecriteria:

* \[ ] CLI map detecteert alle subcommands.
* \[ ] CLI map koppelt commands aan modules/imports.
* \[ ] CLI map markeert commands met execution/demo risk.
* \[ ] CLI map output is secret-free.
* \[ ] Test fixture detecteert nieuwe commands automatisch.

\---

## 7\. Fase 4 - Dashboard Surface Map

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_surface\_map.py
```

Doel: Streamlit dashboardstructuur inzichtelijk maken.

Te mappen:

* \[ ] imports;
* \[ ] tabs;
* \[ ] render functions;
* \[ ] forms;
* \[ ] buttons;
* \[ ] plotly charts;
* \[ ] chart keys;
* \[ ] session\_state keys;
* \[ ] dashboard evidence outputs;
* \[ ] CLI/actions die dashboard indirect triggert;
* \[ ] safety badges/no-live labels;
* \[ ] panels met demo/paper/risk/action functionaliteit.

Belangrijk:

* \[ ] Detecteer `st.plotly\_chart` en wrappergebruik.
* \[ ] Detecteer ontbrekende stable keys.
* \[ ] Detecteer duplicate chart key risico.
* \[ ] Detecteer buttons zonder unieke key.
* \[ ] Detecteer dashboard imports die zwaar of optioneel zijn.
* \[ ] Detecteer panels zonder browser smoke coverage.

Acceptatiecriteria:

* \[ ] Dashboard map bevat tabs/panels.
* \[ ] Dashboard map bevat render functions.
* \[ ] Dashboard map detecteert chart key usage.
* \[ ] Dashboard map kan duplicate/unstable key warnings geven.
* \[ ] Browser smoke requirements worden gekoppeld.

\---

## 8\. Fase 5 - Test Coverage \& Test Selection Map

Nieuwe module:

```text
src/binance\_spot\_bot/test\_impact\_map.py
```

Doel: bepalen welke tests moeten draaien bij changed files.

Inputs:

* \[ ] repo inventory;
* \[ ] code graph;
* \[ ] test files;
* \[ ] imports in tests;
* \[ ] test names;
* \[ ] check-all config;
* \[ ] roadmap task packs.

Per module:

* \[ ] direct tests;
* \[ ] indirect tests;
* \[ ] smoke tests;
* \[ ] safety tests;
* \[ ] dashboard smoke needed;
* \[ ] browser smoke needed;
* \[ ] check-all needed;
* \[ ] security scan needed;
* \[ ] redaction self-test needed.

Test selection rules:

* \[ ] `ui/` changed → dashboard import + dashboard smoke + browser smoke.
* \[ ] `cli.py` changed → CLI smoke + command manifest + check-all.
* \[ ] `operator\_ops.py` changed → operator quality gate + local ops snapshot + support bundle tests.
* \[ ] `security.py`/`redaction.py` changed → security scan + redaction self-test.
* \[ ] `runtime.py`/`execution.py`/`risk.py` changed → runtime/paper/session tests + no-live tests.
* \[ ] `evaluation.py`/`features.py`/`dataset\_governance.py` changed → evaluation/walk-forward/leakage tests.
* \[ ] roadmap docs changed → roadmap validation + duplicate guard.
* \[ ] release/migration modules changed → release quality gate + migration dry-run tests.

Acceptatiecriteria:

* \[ ] Test selector returns minimal recommended tests.
* \[ ] Test selector can return strict full test set.
* \[ ] Test selector includes safety tests.
* \[ ] Test selector explains why each test is needed.
* \[ ] Tests use changed-file fixtures.

\---

## 9\. Fase 6 - Code Ownership Map

Nieuwe module:

```text
src/binance\_spot\_bot/code\_ownership.py
```

Ownership domeinen:

* \[ ] runtime;
* \[ ] execution;
* \[ ] risk;
* \[ ] data;
* \[ ] evaluation;
* \[ ] model\_registry;
* \[ ] dashboard;
* \[ ] operator\_ops;
* \[ ] evidence;
* \[ ] security\_redaction;
* \[ ] support\_bundle;
* \[ ] roadmap\_execution;
* \[ ] release\_management;
* \[ ] disaster\_recovery;
* \[ ] permissions\_compliance;
* \[ ] ai\_ops;
* \[ ] portfolio;
* \[ ] tests;
* \[ ] docs.

Per domein:

* \[ ] included paths;
* \[ ] primary modules;
* \[ ] related tests;
* \[ ] related docs;
* \[ ] related roadmaps;
* \[ ] safety level;
* \[ ] required validators;
* \[ ] suggested reviewer role;
* \[ ] forbidden changes;
* \[ ] no-live constraints.

Acceptatiecriteria:

* \[ ] Ownership map is YAML/JSON.
* \[ ] Ownership map covers all source files.
* \[ ] Unknown owner files are reported.
* \[ ] Safety critical domains require stronger tests.
* \[ ] Dashboard can show owner summary.

\---

## 10\. Fase 7 - Change Impact Analyzer

Nieuwe module:

```text
src/binance\_spot\_bot/impact\_analysis.py
```

Inputs:

* \[ ] changed files list;
* \[ ] repo inventory;
* \[ ] code graph;
* \[ ] CLI surface map;
* \[ ] dashboard surface map;
* \[ ] test impact map;
* \[ ] ownership map;
* \[ ] roadmap dependency graph from Roadmap 090.

Output:

* \[ ] impacted modules;
* \[ ] impacted CLI commands;
* \[ ] impacted dashboard panels;
* \[ ] impacted tests;
* \[ ] impacted docs;
* \[ ] impacted roadmaps;
* \[ ] impacted data artifacts;
* \[ ] impacted safety constraints;
* \[ ] required validation commands;
* \[ ] recommended PR template;
* \[ ] recommended Codex task type;
* \[ ] release notes sections;
* \[ ] risk level:

  * low;
  * medium;
  * high;
  * critical.
* \[ ] no-live blockers.

Risk rules:

* \[ ] Execution/risk/runtime changes are high.
* \[ ] Security/redaction changes are critical.
* \[ ] Dashboard-only display changes are medium unless action buttons touched.
* \[ ] Docs-only changes are low unless roadmap/compliance/release docs.
* \[ ] Migration/restore/release apply code is critical.
* \[ ] Anything touching live/signed/order/account guard is critical.

Acceptatiecriteria:

* \[ ] Impact analyzer works with explicit changed file list.
* \[ ] Impact analyzer works with git diff if available.
* \[ ] Impact analyzer explains every recommendation.
* \[ ] Output is secret-free.
* \[ ] Tests cover low/high/critical examples.

\---

## 11\. Fase 8 - Docs/Code Consistency Checker

Nieuwe module:

```text
src/binance\_spot\_bot/docs\_code\_consistency.py
```

Checks:

* \[ ] every CLI command has docs or generated command manifest entry;
* \[ ] every dashboard panel has docs/smoke marker;
* \[ ] every safety-critical module has tests;
* \[ ] every release/migration module has runbook/docs;
* \[ ] every roadmap-introduced module links to roadmap;
* \[ ] every docs command still exists;
* \[ ] no docs mention live mode as selectable;
* \[ ] no stale command examples;
* \[ ] docs no-live statements present.

Acceptatiecriteria:

* \[ ] Stale CLI command examples are detected.
* \[ ] Missing docs are reported.
* \[ ] Missing tests are reported.
* \[ ] No-live doc drift is detected.
* \[ ] Reports are Markdown + JSON.

\---

## 12\. Fase 9 - Roadmap-to-Code Traceability

Nieuwe module:

```text
src/binance\_spot\_bot/roadmap\_traceability.py
```

Traceability edges:

* \[ ] roadmap introduces module;
* \[ ] roadmap modifies module;
* \[ ] roadmap adds test;
* \[ ] roadmap adds CLI command;
* \[ ] roadmap adds dashboard panel;
* \[ ] roadmap adds docs;
* \[ ] roadmap adds evidence artifact;
* \[ ] roadmap validated by command;
* \[ ] roadmap completed by completion report;
* \[ ] roadmap feeds release notes.

Inputs:

* \[ ] roadmap markdown;
* \[ ] completed docs;
* \[ ] source file headers/comments if available;
* \[ ] test names;
* \[ ] evidence manifests;
* \[ ] release notes input.

Acceptatiecriteria:

* \[ ] Traceability map links Roadmap 090 to its modules once implemented.
* \[ ] Missing traceability is reported.
* \[ ] Roadmap-to-code report is exportable.
* \[ ] Duplicate feature themes can be warned.
* \[ ] Output is secret-free.

\---

## 13\. Fase 10 - Safety Surface Map

Nieuwe module:

```text
src/binance\_spot\_bot/safety\_surface\_map.py
```

Safety surfaces:

* \[ ] live trading gates;
* \[ ] signed endpoint gates;
* \[ ] order endpoints;
* \[ ] account endpoints;
* \[ ] demo execution;
* \[ ] paper execution;
* \[ ] risk limits;
* \[ ] kill switch;
* \[ ] credential handling;
* \[ ] secret scanning;
* \[ ] redaction;
* \[ ] support bundles;
* \[ ] restore/migration apply;
* \[ ] action execution;
* \[ ] permissions/compliance;
* \[ ] scheduler commands.

Per surface:

* \[ ] owning modules;
* \[ ] related tests;
* \[ ] related CLI commands;
* \[ ] related dashboard panels;
* \[ ] hard blockers;
* \[ ] recommended validation;
* \[ ] no-live proof requirement.

Acceptatiecriteria:

* \[ ] Safety map identifies critical paths.
* \[ ] Any change touching safety surface gets high/critical impact.
* \[ ] Safety map links to check-all/security scan/redaction tests.
* \[ ] Dashboard can show safety impact.
* \[ ] Output includes no-live statement.

\---

## 14\. Fase 11 - Artifact \& Data Flow Graph

Nieuwe module:

```text
src/binance\_spot\_bot/artifact\_flow\_graph.py
```

Nodes:

* \[ ] CLI command;
* \[ ] module;
* \[ ] data directory;
* \[ ] report;
* \[ ] evidence file;
* \[ ] support bundle;
* \[ ] session report;
* \[ ] roadmap evidence;
* \[ ] release evidence;
* \[ ] metrics artifact.

Edges:

* \[ ] writes;
* \[ ] reads;
* \[ ] verifies;
* \[ ] bundles;
* \[ ] indexes;
* \[ ] validates;
* \[ ] moves;
* \[ ] archives.

Important artifact roots:

* \[ ] `data/checks`;
* \[ ] `data/evidence`;
* \[ ] `data/reports`;
* \[ ] `data/support`;
* \[ ] `data/sessions`;
* \[ ] `data/pilot-runs`;
* \[ ] `data/roadmaps`;
* \[ ] `data/releases`;
* \[ ] `data/metrics`;
* \[ ] `data/backups`;
* \[ ] `data/action-center`;
* \[ ] `data/compliance`.

Acceptatiecriteria:

* \[ ] Artifact flow graph maps operator\_ops outputs.
* \[ ] Artifact flow graph maps support bundle flow.
* \[ ] Artifact flow graph maps check-all evidence.
* \[ ] Missing producer/consumer warnings exist.
* \[ ] Output is secret-free.

\---

## 15\. Fase 12 - Repository Knowledge Store

Nieuwe module:

```text
src/binance\_spot\_bot/repo\_knowledge\_store.py
```

Storage:

```text
data/repository-knowledge/
  inventory.json
  code-graph.json
  cli-surface-map.json
  dashboard-surface-map.json
  test-impact-map.json
  ownership-map.json
  safety-surface-map.json
  artifact-flow-graph.json
  traceability-map.json
  manifests/
  reports/
```

Core functies:

* \[ ] save/load knowledge graph;
* \[ ] save/load each map;
* \[ ] write manifest;
* \[ ] verify manifest;
* \[ ] compare previous graph;
* \[ ] export summary;
* \[ ] compact old graph snapshots.

Acceptatiecriteria:

* \[ ] Store is local-only.
* \[ ] Store is manifest/hash based.
* \[ ] Store is secret-free.
* \[ ] Store can diff previous graph.
* \[ ] Tests use temp dirs.

\---

## 16\. Fase 13 - Impact Analysis CLI

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli repo-inventory
python -m binance\_spot\_bot.cli code-graph
python -m binance\_spot\_bot.cli cli-surface-map
python -m binance\_spot\_bot.cli dashboard-surface-map
python -m binance\_spot\_bot.cli test-impact-map
python -m binance\_spot\_bot.cli code-ownership-map
python -m binance\_spot\_bot.cli impact-analysis --changed src/binance\_spot\_bot/runtime.py
python -m binance\_spot\_bot.cli docs-code-consistency
python -m binance\_spot\_bot.cli roadmap-traceability
python -m binance\_spot\_bot.cli safety-surface-map
python -m binance\_spot\_bot.cli artifact-flow-graph
python -m binance\_spot\_bot.cli repo-knowledge-build
python -m binance\_spot\_bot.cli repo-knowledge-report
```

Acceptatiecriteria:

* \[ ] Commands werken offline.
* \[ ] Commands ondersteunen JSON output.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Reports zijn secret-free.

\---

## 17\. Fase 14 - Repository Knowledge Dashboard

Nieuwe dashboardsectie:

```text
Repository Knowledge
```

Panels:

* \[ ] repo inventory summary;
* \[ ] module graph summary;
* \[ ] high fan-in/fan-out modules;
* \[ ] CLI command map;
* \[ ] dashboard panel map;
* \[ ] test impact selector;
* \[ ] ownership domains;
* \[ ] impact analysis form;
* \[ ] docs/code consistency;
* \[ ] safety surface map;
* \[ ] artifact/data flow graph;
* \[ ] roadmap traceability;
* \[ ] recommended tests;
* \[ ] recommended docs updates;
* \[ ] no-live proof.

Actions:

* \[ ] rebuild knowledge graph;
* \[ ] run impact analysis;
* \[ ] export report;
* \[ ] copy recommended test commands;
* \[ ] copy Codex task-pack hints;
* \[ ] export ownership map.

Safeguards:

* \[ ] `LOCAL REPOSITORY KNOWLEDGE ONLY` badge.
* \[ ] No live controls.
* \[ ] Raw JSON only in debug expanders.
* \[ ] Stable widget keys.
* \[ ] Browser smoke covers panel.

Acceptatiecriteria:

* \[ ] Dashboard can show impacted tests for changed file.
* \[ ] Dashboard shows safety impact.
* \[ ] Dashboard suggests docs updates.
* \[ ] Dashboard does not execute test commands by default.
* \[ ] Browser smoke passes.

\---

## 18\. Fase 15 - Knowledge Reports \& Evidence

Nieuwe module:

```text
src/binance\_spot\_bot/repo\_knowledge\_report.py
```

Reports:

```text
data/repository-knowledge/reports/
  repository\_knowledge\_report.md
  repository\_knowledge\_report.json
  impact\_analysis\_report.md
  impact\_analysis\_report.json
  docs\_code\_consistency\_report.md
  safety\_surface\_report.md
  artifact\_flow\_report.md
```

Report secties:

* \[ ] summary;
* \[ ] module inventory;
* \[ ] top central modules;
* \[ ] modules without tests;
* \[ ] stale docs;
* \[ ] CLI surface;
* \[ ] dashboard surface;
* \[ ] safety surfaces;
* \[ ] artifacts/data flow;
* \[ ] roadmap traceability;
* \[ ] recommended refactors;
* \[ ] recommended test improvements;
* \[ ] no-live proof.

Acceptatiecriteria:

* \[ ] Reports zijn Markdown + JSON.
* \[ ] Reports zijn secret-free.
* \[ ] Reports hebben manifest/hash.
* \[ ] Reports kunnen door Roadmap 084 metrics worden geïndexeerd.
* \[ ] Reports kunnen door Roadmap 090 roadmap evidence worden gebruikt.

\---

## 19\. Fase 16 - Codex/Roadmap Integration

Doel: Roadmap 091 voedt Roadmap 090 task packs.

Nieuwe module:

```text
src/binance\_spot\_bot/repo\_knowledge\_codex\_integration.py
```

Functionaliteit:

* \[ ] impact analysis → Codex file boundaries;
* \[ ] impact analysis → required tests;
* \[ ] impact analysis → forbidden files;
* \[ ] safety surface map → safety constraints;
* \[ ] ownership map → suggested reviewer role;
* \[ ] docs consistency → docs tasks;
* \[ ] artifact flow → evidence outputs;
* \[ ] traceability → roadmap/release notes updates.

Acceptatiecriteria:

* \[ ] Task pack generator kan knowledge graph gebruiken.
* \[ ] PR template generator kan impacted tests invullen.
* \[ ] Completion gate kan knowledge evidence gebruiken.
* \[ ] Release notes input krijgt impacted components.
* \[ ] Output is secret-free.

\---

## 20\. Fase 17 - Refactor Candidate Detector

Nieuwe module:

```text
src/binance\_spot\_bot/refactor\_candidates.py
```

Detecties:

* \[ ] modules boven line-count threshold;
* \[ ] functions boven line-count threshold;
* \[ ] modules met hoge fan-in;
* \[ ] modules met hoge fan-out;
* \[ ] CLI command cluster te groot;
* \[ ] dashboard render file te groot;
* \[ ] repeated command patterns;
* \[ ] duplicate safety checks;
* \[ ] missing wrappers/components;
* \[ ] tests te breed of te traag;
* \[ ] docs drift.

Output:

* \[ ] candidate id;
* \[ ] module;
* \[ ] reason;
* \[ ] impact;
* \[ ] suggested split;
* \[ ] required tests;
* \[ ] risk level;
* \[ ] roadmap suggestion.

Acceptatiecriteria:

* \[ ] Detector geeft geen automatische codewijzigingen.
* \[ ] Detector geeft concrete safe suggestions.
* \[ ] Detector markeert `cli.py`/`streamlit\_app.py` als analyseerbare high-complexity modules indien thresholds overschreden worden.
* \[ ] Reports zijn dashboard-ready.
* \[ ] Tests gebruiken fixture modules.

\---

## 21\. Fase 18 - Scheduled Knowledge Refresh

Doel: Roadmap 083 scheduler kan knowledge graph dagelijks/wekelijks verversen.

Scheduled jobs:

* \[ ] daily repo inventory;
* \[ ] daily docs/code consistency check;
* \[ ] weekly full code graph rebuild;
* \[ ] weekly safety surface report;
* \[ ] weekly artifact flow report;
* \[ ] weekly refactor candidate report;
* \[ ] post-roadmap-completion traceability refresh;
* \[ ] post-release knowledge graph refresh.

Acceptatiecriteria:

* \[ ] Jobs zijn allowlisted.
* \[ ] Jobs zijn read-only.
* \[ ] Failed refresh creates support bundle if configured.
* \[ ] Reports feed Roadmap 084 metrics.
* \[ ] No live trading.

\---

## 22\. Fase 19 - Tests

### Unit tests

* \[ ] `tests/test\_repo\_inventory.py`
* \[ ] `tests/test\_code\_graph.py`
* \[ ] `tests/test\_cli\_surface\_map.py`
* \[ ] `tests/test\_dashboard\_surface\_map.py`
* \[ ] `tests/test\_test\_impact\_map.py`
* \[ ] `tests/test\_code\_ownership.py`
* \[ ] `tests/test\_impact\_analysis.py`
* \[ ] `tests/test\_docs\_code\_consistency.py`
* \[ ] `tests/test\_roadmap\_traceability.py`
* \[ ] `tests/test\_safety\_surface\_map.py`
* \[ ] `tests/test\_artifact\_flow\_graph.py`
* \[ ] `tests/test\_repo\_knowledge\_store.py`
* \[ ] `tests/test\_repo\_knowledge\_report.py`
* \[ ] `tests/test\_repo\_knowledge\_codex\_integration.py`
* \[ ] `tests/test\_refactor\_candidates.py`

### Integration tests

* \[ ] Build repo inventory from fixture repo.
* \[ ] Build AST import graph.
* \[ ] Detect CLI commands from fixture CLI.
* \[ ] Detect dashboard render functions and chart keys.
* \[ ] Map tests to modules.
* \[ ] Build ownership map.
* \[ ] Run impact analysis for `runtime.py`.
* \[ ] Run impact analysis for dashboard file.
* \[ ] Run docs/code consistency.
* \[ ] Generate repository knowledge report.
* \[ ] Export knowledge store manifest.

### Safety tests

* \[ ] Knowledge graph does not execute code.
* \[ ] Knowledge graph does not call network.
* \[ ] Knowledge graph does not call signed/order/account endpoints.
* \[ ] Output redacts secrets.
* \[ ] Safety surface changes force high/critical impact.
* \[ ] Task recommendations never include live trading.
* \[ ] Reports contain no secrets.
* \[ ] No-live proof remains true.

\---

## 23\. Docs

Nieuwe docs:

* \[ ] `docs/repository-knowledge-graph-safety-contract.md`
* \[ ] `docs/repo-inventory.md`
* \[ ] `docs/code-graph.md`
* \[ ] `docs/cli-surface-map.md`
* \[ ] `docs/dashboard-surface-map.md`
* \[ ] `docs/test-impact-map.md`
* \[ ] `docs/code-ownership-map.md`
* \[ ] `docs/impact-analysis.md`
* \[ ] `docs/docs-code-consistency.md`
* \[ ] `docs/roadmap-code-traceability.md`
* \[ ] `docs/safety-surface-map.md`
* \[ ] `docs/artifact-flow-graph.md`
* \[ ] `docs/repo-knowledge-store.md`
* \[ ] `docs/repo-knowledge-dashboard.md`
* \[ ] `docs/refactor-candidate-detector.md`
* \[ ] `docs/repo-knowledge-codex-integration.md`

README updates:

* \[ ] knowledge graph workflow;
* \[ ] impact analysis command;
* \[ ] test selection command;
* \[ ] ownership map explanation;
* \[ ] docs/code consistency command;
* \[ ] no-live statement.

\---

## 24\. CLI command examples

### Build volledige knowledge graph

```powershell
python -m binance\_spot\_bot.cli repo-knowledge-build --json
```

### Impactanalyse voor runtimewijziging

```powershell
python -m binance\_spot\_bot.cli impact-analysis --changed src/binance\_spot\_bot/runtime.py --json
```

### Testselectie voor dashboardwijziging

```powershell
python -m binance\_spot\_bot.cli impact-analysis --changed src/binance\_spot\_bot/ui/streamlit\_app.py --json
```

### Docs/code consistency

```powershell
python -m binance\_spot\_bot.cli docs-code-consistency --json
```

### Ownership map

```powershell
python -m binance\_spot\_bot.cli code-ownership-map --json
```

### Safety surface

```powershell
python -m binance\_spot\_bot.cli safety-surface-map --json
```

\---

## 25\. Codex bouwvolgorde

### PR 1 - Repo Inventory + Safety Contract

* \[ ] `repo\_inventory.py`
* \[ ] safety contract doc
* \[ ] inventory manifest
* \[ ] tests.

### PR 2 - Python Code Graph

* \[ ] `code\_graph.py`
* \[ ] AST import graph
* \[ ] cycle/fan-in/fan-out reports
* \[ ] tests.

### PR 3 - CLI Surface Map

* \[ ] `cli\_surface\_map.py`
* \[ ] command extraction
* \[ ] safety class mapping
* \[ ] tests.

### PR 4 - Dashboard Surface Map

* \[ ] `dashboard\_surface\_map.py`
* \[ ] tabs/render functions/chart key detection
* \[ ] tests.

### PR 5 - Test Impact Map

* \[ ] `test\_impact\_map.py`
* \[ ] changed file → tests mapping
* \[ ] tests.

### PR 6 - Ownership + Safety Surface

* \[ ] `code\_ownership.py`
* \[ ] `safety\_surface\_map.py`
* \[ ] tests.

### PR 7 - Impact Analyzer

* \[ ] `impact\_analysis.py`
* \[ ] changed files → impacted modules/tests/docs/evidence
* \[ ] tests.

### PR 8 - Docs/Code + Roadmap Traceability

* \[ ] `docs\_code\_consistency.py`
* \[ ] `roadmap\_traceability.py`
* \[ ] tests.

### PR 9 - Artifact Flow + Knowledge Store + Reports

* \[ ] `artifact\_flow\_graph.py`
* \[ ] `repo\_knowledge\_store.py`
* \[ ] `repo\_knowledge\_report.py`
* \[ ] tests.

### PR 10 - CLI + Dashboard + Codex Integration

* \[ ] new CLI commands
* \[ ] Repository Knowledge dashboard
* \[ ] `repo\_knowledge\_codex\_integration.py`
* \[ ] refactor candidate detector
* \[ ] browser smoke
* \[ ] docs.

\---

## 26\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 091 PR 1: Repo Inventory + Repository Knowledge Safety Contract.

Maak docs/repository-knowledge-graph-safety-contract.md.

Maak src/binance\_spot\_bot/repo\_inventory.py met:
- RepoFile
- RepoInventory
- RepoDirectorySummary
- RepoInventoryManifest
- RepoInventoryResult
- build\_repo\_inventory(root: Path)
- write\_repo\_inventory\_manifest(...)
- verify\_repo\_inventory\_manifest(...)

Scan minimaal:
- src/
- tests/
- docs/
- Roadmap docs/
- Voltooid docs/
- scripts/
- pyproject.toml
- README.md indien aanwezig

Per bestand:
- relative path
- suffix
- size\_bytes
- modified\_at
- sha256
- category
- line\_count
- basic class/function/import counts voor Python files
- safety\_relevant\_guess
- secret\_scan\_status

Guardrails:
- read-only
- geen code execution
- geen network calls
- geen signed/order/account endpoints
- output is secret-free
- live\_trading\_enabled=False in output

Voeg tests toe voor:
- inventory over fixture repo
- category detection
- sha256 stable
- Python class/function/import counts
- safety relevant guess voor runtime/execution/risk/security/redaction files
- secret-like fixture content wordt niet gelekt in output
- manifest verify pass/fail
```

Waarom eerst:

* Je kunt geen impactanalyse doen zonder betrouwbare file inventory.
* Het is read-only en raakt geen runtime/trading.
* Het helpt Roadmap 090 meteen om roadmaps en code aan elkaar te koppelen.
* Het is klein genoeg voor Codex en goed testbaar.
* Het voorkomt latere dubbele bouw en onduidelijke ownership.

\---

## 27\. Definition of Done

Roadmap 091 is klaar als:

* \[ ] Repository Knowledge Safety Contract bestaat.
* \[ ] Repository Inventory Engine werkt.
* \[ ] Python AST Import \& Symbol Graph werkt.
* \[ ] CLI Command Surface Map werkt.
* \[ ] Dashboard Surface Map werkt.
* \[ ] Test Coverage \& Test Selection Map werkt.
* \[ ] Code Ownership Map werkt.
* \[ ] Change Impact Analyzer werkt.
* \[ ] Docs/Code Consistency Checker werkt.
* \[ ] Roadmap-to-Code Traceability werkt.
* \[ ] Safety Surface Map werkt.
* \[ ] Artifact \& Data Flow Graph werkt.
* \[ ] Repository Knowledge Store werkt.
* \[ ] Impact Analysis CLI werkt.
* \[ ] Repository Knowledge Dashboard werkt.
* \[ ] Knowledge Reports \& Evidence werken.
* \[ ] Codex/Roadmap Integration werkt.
* \[ ] Refactor Candidate Detector werkt.
* \[ ] Scheduled Knowledge Refresh werkt.
* \[ ] Tests bewijzen geen code execution/network/live/signed/order/account.
* \[ ] Reports/evidence zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 091 kan na uitvoering naar `Voltooid docs`.

\---

## 28\. Verwachte Roadmap 092 daarna

Na Roadmap 091 zou Roadmap 092 logisch focussen op:

```text
Roadmap 092 - Intelligent Test Selection, CI Acceleration \& Regression Risk Scoring
```

Mogelijke inhoud:

* \[ ] automatische testselectie op basis van impact graph;
* \[ ] regression risk scoring;
* \[ ] fast/standard/deep test profiles;
* \[ ] flaky test tracking;
* \[ ] test runtime analytics;
* \[ ] check-all acceleration;
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

Gebouwd: repo inventory, AST code graph, CLI surface map, dashboard surface map, test impact map, code ownership, impact analyzer, docs/code consistency, roadmap traceability, safety surface map, artifact flow graph, repo knowledge store/report, Codex integration, refactor candidate detector, CLI commands, dashboard panel en docs.

Validatie: tests/test_roadmap_091_repo_knowledge_acceptance.py; tests/test_roadmaps_089_096_full_surface.py; repo knowledge CLI flow; python -m binance_spot_bot.cli check-all --skip-tests --json; python -m pytest -q; python -m binance_spot_bot.cli dashboard-smoke --seconds 1; python -m binance_spot_bot.cli dashboard-browser-smoke --url http://127.0.0.1:8506/ --seconds 10.

Safety: lokaal/paper-only, geen live trading enablement.

