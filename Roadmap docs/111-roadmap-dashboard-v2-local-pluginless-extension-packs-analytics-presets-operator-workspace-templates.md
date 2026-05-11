# Roadmap 111 - Dashboard V2 Local Plugin-Less Extension Packs, Analytics Presets \& Operator Workspace Templates

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/111-roadmap-dashboard-v2-local-pluginless-extension-packs-analytics-presets-operator-workspace-templates.md
```

## Samenvatting

Roadmap 104 bouwt Dashboard V2 naast Streamlit met FastAPI/WebSocket/React.

Roadmap 105 migreert feature parity van Streamlit naar Dashboard V2.

Roadmap 106 maakt Dashboard V2 performant, lokaal packagebaar, offline/static, browser-smoke-ready en cutover-ready.

Roadmap 107 vereenvoudigt operatorflows, verwerkt UAT-feedback en maakt Streamlit deprecation planning concreet.

Roadmap 108 zet Dashboard V2 als primaire UI neer, maakt V2-only operator mode en houdt Streamlit als legacy/fallback.

Roadmap 109 maakt Streamlit removal-candidate, dependency isolation, V2-only release hardening, legacy archive en removal readiness gate.

Roadmap 110 maakt Dashboard V2 een echte operator workspace met custom layouts, widgets, watchlists, preferences, synchronized charts en workspace evidence.

Roadmap 111 is de logische volgende stap: **bouw veilige lokale extension packs zonder arbitraire plugin-code**. Geen externe plugin runtime, geen onbekende JavaScript, geen cloud store. Wel lokale, gevalideerde, versioned packs met workspace templates, widget preset packs, analytics presets, watchlist packs, operator workflows, support/evidence templates, model-ops templates en portfolio templates.

Het doel is dat een operator met één klik een complete veilige workspace kan laden, bijvoorbeeld:

* `Beginner Paper Operator`
* `Demo Spot Trading Control Room`
* `Binance Spot Market Scanner`
* `Risk \& Alerts War Room`
* `Model Monitoring Desk`
* `Portfolio Allocation Desk`
* `Support \& Evidence Desk`
* `Roadmap/Release Ops Desk`

Live trading blijft volledig buiten scope. Alle packs zijn local-only en demo/paper/testnet-readiness-only. Geen live mode, geen signed real-order endpoints, geen echte account workflows, geen externe telemetry en geen arbitraire plugin-code.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 111`, `111-roadmap`, `Dashboard V2 Local Plugin-Less Extension Packs`, `Analytics Presets`, `Operator Workspace Templates` en `extension packs`.
* \[x] Geen bestaande Roadmap 111 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 110 is lokaal aangemaakt als Dashboard V2 Advanced Realtime Analytics, Multi-Panel Layouts \& Operator Customization.

### Codebasecontrole

Breed bekeken met focus op Dashboard V2 vervolg, runtime snapshots, page registry, market data, check-all en safety:

* \[x] `src/binance\_spot\_bot/ui/page\_registry.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/market\_data\_source.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] roadmaplijn 104-110.

### Belangrijke bestaande basis

De codebase heeft nu of wordt via Roadmap 104-110 voorbereid met:

* \[x] Een page registry met 36 dashboard pages en live-page blocking.
* \[x] Runtime modes alleen `demo`, `paper` en `testnet-readiness`.
* \[x] Runtime snapshots met candles, signals, fills, equity, market data, top of book, data quality, sessions, active model, alerts, paper account, readiness, demo account/orders, demo pilot en reconciliation.
* \[x] Market data sources voor static/demo, REST polling en WebSocket-wrapper met fallback naar safe polling/demo data.
* \[x] Check-all forceert `LIVE\_TRADING\_ENABLED=false`, `KILL\_SWITCH=true` en `PYTHONPATH=src`.
* \[x] Dashboard V2 workspaces, widget registry, watchlists, preferences en import/export worden in Roadmap 110 gepland.
* \[x] Operator evidence, support bundle, redaction, quality gate en local ops snapshot bestaan al als bredere operatorbasis.

### Belangrijkste gat na Roadmap 110

Roadmap 110 geeft operators vrijheid om eigen workspaces te bouwen. Maar zonder veilige templates en packs krijg je alsnog veel handwerk en inconsistentie:

* \[ ] elke operator moet zelf widgets combineren;
* \[ ] geen standaard workspace per persona;
* \[ ] geen bewezen analytics presets;
* \[ ] geen herbruikbare watchlist packs;
* \[ ] geen model/portfolio/support workspace packs;
* \[ ] geen pack versioning;
* \[ ] geen pack validation/evidence;
* \[ ] geen safe import/export van template packs;
* \[ ] geen local catalog;
* \[ ] geen pack compatibility met workspace schema;
* \[ ] geen pack-level browser smoke;
* \[ ] geen pack recommendation op basis van workflow/doel.

Roadmap 111 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 111

Maak een veilige lokale pack-laag bovenop Dashboard V2 workspaces:

```text
Dashboard V2 workspace schema
→ safe widget registry
→ plugin-less pack schema
→ template packs
→ analytics presets
→ watchlist packs
→ workflow packs
→ local catalog
→ validation/evidence
```

Na Roadmap 111 moet de operator:

* \[ ] een workspace pack kunnen kiezen uit een lokale catalog;
* \[ ] een complete workspace template kunnen installeren zonder code execution;
* \[ ] analytics presets kunnen toevoegen aan bestaande workspaces;
* \[ ] watchlists/symbol groups kunnen importeren;
* \[ ] pack compatibility kunnen controleren;
* \[ ] pack evidence kunnen exporteren;
* \[ ] pack updates/migrations kunnen dry-runnen;
* \[ ] pack recommendations krijgen voor demo/paper/model/portfolio/support workflows;
* \[ ] zeker weten dat packs geen live mode of unsafe actions bevatten.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen echte plugin runtime.
* \[ ] Geen arbitraire JavaScript uitvoering.
* \[ ] Geen Python code execution uit packs.
* \[ ] Geen remote marketplace.
* \[ ] Geen cloud sync.
* \[ ] Geen externe telemetry.
* \[ ] Geen Dashboard V2 workspace schema opnieuw bouwen.
* \[ ] Geen widget registry opnieuw bouwen.
* \[ ] Geen runtime refactor opnieuw bouwen.
* \[ ] Geen trading engine opnieuw bouwen.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte account workflows.
* \[ ] Geen pack dat no-live/safety widgets kan verbergen.
* \[ ] Geen pack die unknown widgets installeert zonder registry validation.

Wel doen:

* \[ ] lokale plugin-less pack schema;
* \[ ] pack registry/catalog;
* \[ ] template packs;
* \[ ] analytics presets;
* \[ ] watchlist packs;
* \[ ] pack import/export;
* \[ ] pack migrations;
* \[ ] pack compatibility;
* \[ ] pack validation/evidence;
* \[ ] pack recommendation;
* \[ ] dashboard/CLI/docs/tests.

\---

## 3\. Fase 0 - Plugin-Less Extension Pack Safety Contract

Nieuw docbestand:

```text
docs/dashboard-v2-extension-pack-safety-contract.md
```

Regels:

* \[ ] Extension packs zijn local-only.
* \[ ] Geen remote marketplace.
* \[ ] Geen cloud sync.
* \[ ] Geen arbitraire JS/Python/plugin-code.
* \[ ] Packs bestaan alleen uit JSON/Markdown/static metadata.
* \[ ] Packs mogen alleen allowlisted widget types gebruiken.
* \[ ] Packs mogen geen live mode bevatten.
* \[ ] Packs mogen geen signed/order/account actions definiëren.
* \[ ] Packs mogen safety/no-live widgets niet verwijderen.
* \[ ] Packs mogen stop/runtime safety controls niet verbergen in operator mode.
* \[ ] Pack imports zijn preview-first.
* \[ ] Pack install vereist validatie.
* \[ ] Pack export is secret-free.
* \[ ] Pack evidence bevat `live\_trading\_enabled=False`.
* \[ ] Pack registry is local-only.
* \[ ] Unknown pack versions worden geblokkeerd of gemigreerd via dry-run.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen packs geen code kunnen uitvoeren.
* \[ ] Tests bewijzen live mode/action geblokkeerd wordt.
* \[ ] Tests bewijzen unknown widget types geblokkeerd worden.
* \[ ] Tests bewijzen pack export secret-free is.

\---

## 4\. Fase 1 - Extension Pack Schema

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/extension\_pack\_schema.py
```

Dataclasses:

* \[ ] `DashboardExtensionPack`
* \[ ] `DashboardExtensionPackManifest`
* \[ ] `DashboardPackContent`
* \[ ] `DashboardPackDependency`
* \[ ] `DashboardPackCompatibility`
* \[ ] `DashboardPackValidationResult`

Pack types:

* \[ ] workspace\_template;
* \[ ] widget\_preset;
* \[ ] analytics\_preset;
* \[ ] watchlist\_pack;
* \[ ] operator\_workflow;
* \[ ] support\_evidence\_pack;
* \[ ] model\_ops\_pack;
* \[ ] portfolio\_ops\_pack;
* \[ ] training\_uat\_pack;
* \[ ] release\_ops\_pack.

Manifest fields:

* \[ ] pack\_id;
* \[ ] name;
* \[ ] description;
* \[ ] version;
* \[ ] author;
* \[ ] created\_at\_ms;
* \[ ] pack\_type;
* \[ ] compatible\_workspace\_schema\_versions;
* \[ ] required\_widget\_types;
* \[ ] required\_dashboard\_v2\_features;
* \[ ] mode\_scope;
* \[ ] operator\_level;
* \[ ] tags;
* \[ ] no\_live\_statement;
* \[ ] live\_trading\_enabled=false;
* \[ ] content\_hash.

Validation blocks:

* \[ ] live mode.
* \[ ] live\_trading\_enabled=True.
* \[ ] unknown pack\_type.
* \[ ] missing no\_live\_statement.
* \[ ] unknown widget type.
* \[ ] code/script fields.
* \[ ] raw secrets.
* \[ ] missing safety widget in workspace template.
* \[ ] unsupported schema version.

Acceptatiecriteria:

* \[ ] Pack schema is JSON-serializable.
* \[ ] Pack validation blocks unsafe input.
* \[ ] Secret-like values are redacted.
* \[ ] Hash can be computed.
* \[ ] Tests cover valid/invalid manifests.

\---

## 5\. Fase 2 - Local Pack Registry

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/extension\_pack\_registry.py
```

Storage:

```text
data/dashboard-v2/extension-packs/
  installed/
  catalog/
  exports/
  cache/
  evidence/
```

Registry functies:

* \[ ] list available packs;
* \[ ] list installed packs;
* \[ ] install pack from local file;
* \[ ] uninstall pack with confirm;
* \[ ] enable/disable pack;
* \[ ] validate installed packs;
* \[ ] verify pack hash;
* \[ ] generate local catalog;
* \[ ] search packs;
* \[ ] show pack details;
* \[ ] detect broken packs.

Pack statuses:

* \[ ] available;
* \[ ] installed;
* \[ ] enabled;
* \[ ] disabled;
* \[ ] incompatible;
* \[ ] blocked;
* \[ ] corrupted;
* \[ ] migrated.

Acceptatiecriteria:

* \[ ] Registry is local-only.
* \[ ] Registry refuses path traversal.
* \[ ] Registry validates every pack before install.
* \[ ] Uninstall requires confirm.
* \[ ] Tests use temp dirs.

\---

## 6\. Fase 3 - Pack Compatibility Engine

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/pack\_compatibility.py
```

Checks:

* \[ ] workspace schema version compatible;
* \[ ] required widgets exist;
* \[ ] required API scopes exist;
* \[ ] required Dashboard V2 features exist;
* \[ ] safe modes supported;
* \[ ] operator level allowed;
* \[ ] performance budget estimated;
* \[ ] no-live proof present;
* \[ ] pack dependencies installed;
* \[ ] no dependency cycles;
* \[ ] migration available if needed.

Statuses:

* \[ ] compatible;
* \[ ] compatible\_with\_warnings;
* \[ ] migration\_required;
* \[ ] incompatible;
* \[ ] blocked\_unsafe.

Acceptatiecriteria:

* \[ ] Compatibility report is deterministic.
* \[ ] Missing widget blocks install.
* \[ ] Live mode blocks install.
* \[ ] Unknown schema version requires migration or blocks.
* \[ ] Tests cover compatibility matrix.

\---

## 7\. Fase 4 - Pack Preview \& Dry-Run Install

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/pack\_install\_preview.py
```

Preview toont:

* \[ ] files/artifacts that will be added;
* \[ ] workspace templates;
* \[ ] widgets used;
* \[ ] analytics presets;
* \[ ] watchlists;
* \[ ] preferences affected;
* \[ ] migrations needed;
* \[ ] warnings;
* \[ ] blockers;
* \[ ] no-live proof;
* \[ ] rollback plan.

Install modes:

* \[ ] preview\_only;
* \[ ] dry\_run;
* \[ ] install\_disabled;
* \[ ] install\_enabled\_after\_confirm.

Acceptatiecriteria:

* \[ ] Default is preview/dry-run.
* \[ ] Install requires confirmation.
* \[ ] Unsafe pack blocked before write.
* \[ ] Rollback plan generated.
* \[ ] Tests cover dry-run/install-block.

\---

## 8\. Fase 5 - Workspace Template Packs

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/workspace\_template\_packs.py
```

Template packs:

### `beginner\_paper\_operator`

* \[ ] no-live banner;
* \[ ] start paper session;
* \[ ] candle chart;
* \[ ] equity chart;
* \[ ] risk decision;
* \[ ] alerts;
* \[ ] session report.

### `demo\_spot\_control\_room`

* \[ ] no-live banner;
* \[ ] demo profile status;
* \[ ] demo order preview;
* \[ ] demo order status;
* \[ ] reconciliation;
* \[ ] demo pilot counters;
* \[ ] evidence export.

### `market\_analysis\_desk`

* \[ ] candle chart;
* \[ ] top of book;
* \[ ] spread;
* \[ ] volume;
* \[ ] data quality;
* \[ ] watchlist quick switch.

### `risk\_alerts\_war\_room`

* \[ ] no-live banner;
* \[ ] risk blocks;
* \[ ] max loss status;
* \[ ] data quality warnings;
* \[ ] alerts inbox;
* \[ ] stop button;
* \[ ] runbook links.

### `model\_monitoring\_desk`

* \[ ] active model;
* \[ ] model alias;
* \[ ] signal confidence;
* \[ ] model health;
* \[ ] drift status;
* \[ ] downgrade recommendations.

### `portfolio\_allocation\_desk`

* \[ ] portfolio allocation;
* \[ ] strategy weights;
* \[ ] risk budget;
* \[ ] attribution;
* \[ ] rotation status;
* \[ ] governance evidence.

### `support\_evidence\_desk`

* \[ ] support bundle;
* \[ ] evidence manifest;
* \[ ] local ops snapshot;
* \[ ] operator quality gate;
* \[ ] redaction self-test;
* \[ ] no-live proof.

Acceptatiecriteria:

* \[ ] All template packs validate.
* \[ ] All include mandatory safety widgets.
* \[ ] All can instantiate workspace.
* \[ ] All export evidence.
* \[ ] Browser smoke covers at least three templates.

\---

## 9\. Fase 6 - Analytics Preset Packs

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/analytics\_preset\_packs.py
```

Preset packs:

### Market analytics

* \[ ] candle trend;
* \[ ] spread trend;
* \[ ] top-of-book freshness;
* \[ ] volatility bucket;
* \[ ] data quality warnings;
* \[ ] reconnect/degraded source count.

### Paper trading analytics

* \[ ] equity curve;
* \[ ] drawdown;
* \[ ] fills by side;
* \[ ] fees paid;
* \[ ] realized PnL;
* \[ ] risk blocks by reason;
* \[ ] trades per session.

### Model analytics

* \[ ] signal confidence distribution;
* \[ ] signal side counts;
* \[ ] active model timeline;
* \[ ] fallback model usage;
* \[ ] drift/model health links.

### Portfolio analytics

* \[ ] allocation by strategy/model/symbol;
* \[ ] exposure by symbol;
* \[ ] risk budget usage;
* \[ ] attribution summary;
* \[ ] rotation decisions.

### Operator analytics

* \[ ] support bundle status;
* \[ ] evidence freshness;
* \[ ] check-all status;
* \[ ] dashboard smoke status;
* \[ ] UAT/training status.

Acceptatiecriteria:

* \[ ] Presets compile to analytics queries.
* \[ ] Presets enforce payload limits.
* \[ ] Missing data gives useful empty states.
* \[ ] Presets are secret-free.
* \[ ] Tests use fixture snapshots/sessions.

\---

## 10\. Fase 7 - Watchlist \& Symbol Group Packs

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/watchlist\_packs.py
```

Built-in local packs:

* \[ ] `binance\_spot\_majors`

  * BTCUSDT
  * ETHUSDT
  * BNBUSDT
  * SOLUSDT
  * XRPUSDT
* \[ ] `stablecoin\_pairs`

  * BTCUSDT
  * ETHUSDT
  * BNBUSDT
  * ADAUSDT
  * DOGEUSDT
* \[ ] `operator\_demo\_watchlist`

  * BTCUSDT
  * ETHUSDT
* \[ ] `low\_scope\_smoke\_watchlist`

  * BTCUSDT only.
* \[ ] custom user watchlist pack.

Validation:

* \[ ] symbol uppercase.
* \[ ] symbol length sane.
* \[ ] quote asset allowlist optional.
* \[ ] duplicate symbols removed/warned.
* \[ ] unsupported symbols warning, not crash.
* \[ ] no account dependency.

Acceptatiecriteria:

* \[ ] Watchlist packs validate.
* \[ ] Duplicates handled.
* \[ ] Invalid symbol rejected/warned.
* \[ ] Watchlist can feed workspace.
* \[ ] Tests cover import/export.

\---

## 11\. Fase 8 - Workflow Pack Builder

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/workflow\_packs.py
```

Workflow packs:

* \[ ] first install health check;
* \[ ] first dashboard launch;
* \[ ] first paper session;
* \[ ] demo spot guarded order rehearsal;
* \[ ] support bundle creation;
* \[ ] evidence review;
* \[ ] no-live proof review;
* \[ ] model monitoring review;
* \[ ] portfolio allocation review;
* \[ ] release readiness review;
* \[ ] UAT acceptance run.

Per workflow pack:

* \[ ] steps;
* \[ ] required widgets;
* \[ ] required docs;
* \[ ] required CLI commands;
* \[ ] expected artifacts;
* \[ ] pass criteria;
* \[ ] troubleshooting links;
* \[ ] no-live proof.

Acceptatiecriteria:

* \[ ] Workflow packs validate.
* \[ ] Workflow can instantiate guided workspace.
* \[ ] Commands are safe variants.
* \[ ] Pack links valid docs/playbooks.
* \[ ] Tests cover command validation.

\---

## 12\. Fase 9 - Pack Recommendation Engine

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/pack\_recommendations.py
```

Inputs:

* \[ ] operator level;
* \[ ] current workflow;
* \[ ] active mode;
* \[ ] selected symbol/watchlist;
* \[ ] open blockers;
* \[ ] UAT feedback;
* \[ ] recent sessions;
* \[ ] model/portfolio status;
* \[ ] support/evidence freshness;
* \[ ] performance budget.

Recommendations:

* \[ ] recommended template pack;
* \[ ] recommended analytics presets;
* \[ ] recommended watchlist;
* \[ ] recommended workflow pack;
* \[ ] reasons;
* \[ ] blockers;
* \[ ] no-live proof;
* \[ ] expected impact.

Acceptatiecriteria:

* \[ ] Recommendations are deterministic.
* \[ ] Unsafe packs never recommended.
* \[ ] Missing data handled.
* \[ ] Report is Markdown + JSON.
* \[ ] Tests use fixture operator contexts.

\---

## 13\. Fase 10 - Extension Pack API

Nieuwe API routes:

```text
GET  /api/extension-packs
GET  /api/extension-packs/catalog
GET  /api/extension-packs/installed
GET  /api/extension-packs/{pack\_id}
POST /api/extension-packs/preview-import
POST /api/extension-packs/install
POST /api/extension-packs/uninstall
POST /api/extension-packs/enable
POST /api/extension-packs/disable
GET  /api/extension-packs/{pack\_id}/compatibility
GET  /api/extension-packs/recommendations
POST /api/extension-packs/{pack\_id}/instantiate-workspace
POST /api/extension-packs/evidence-export
```

Rules:

* \[ ] All mutations use action policy.
* \[ ] Install/uninstall require confirm.
* \[ ] No remote fetch.
* \[ ] No code execution.
* \[ ] All payloads redacted.
* \[ ] All responses include no-live statement.

Acceptatiecriteria:

* \[ ] TestClient covers routes.
* \[ ] Unsafe import blocked.
* \[ ] Local catalog works.
* \[ ] Recommendations work.
* \[ ] Reports secret-free.

\---

## 14\. Fase 11 - Extension Pack Dashboard UI

Nieuwe Dashboard V2 pages:

```text
/extension-packs
/extension-packs/catalog
/extension-packs/installed
/extension-packs/import
/extension-packs/recommendations
/templates
/analytics-presets
/workflow-packs
```

UI features:

* \[ ] pack catalog cards;
* \[ ] pack details drawer;
* \[ ] compatibility badge;
* \[ ] install preview;
* \[ ] dry-run result;
* \[ ] confirm install;
* \[ ] enable/disable toggle;
* \[ ] instantiate workspace button;
* \[ ] recommendation panel;
* \[ ] evidence export;
* \[ ] no-live proof.

Acceptatiecriteria:

* \[ ] UI can browse built-in packs.
* \[ ] UI can preview install.
* \[ ] UI blocks unsafe pack.
* \[ ] UI can instantiate workspace.
* \[ ] Browser smoke covers catalog/install preview.

\---

## 15\. Fase 12 - Pack Import/Export \& Signing-Lite Hashes

Geen cryptographic trust system nodig, maar wel local integrity.

Features:

* \[ ] export pack as folder or zip;
* \[ ] manifest with SHA256 hashes;
* \[ ] import preview verifies hashes;
* \[ ] tamper detection;
* \[ ] pack author metadata;
* \[ ] local origin metadata;
* \[ ] redaction scan before export;
* \[ ] no external signature service;
* \[ ] optional local trust note.

Acceptatiecriteria:

* \[ ] Export has manifest/hash.
* \[ ] Import detects tampering.
* \[ ] Export contains no secrets.
* \[ ] Import does not execute code.
* \[ ] Tests cover tampered pack fixture.

\---

## 16\. Fase 13 - Pack Migration System

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/pack\_migrations.py
```

Features:

* \[ ] pack schema version;
* \[ ] migration registry;
* \[ ] migrate manifest;
* \[ ] migrate workspace templates;
* \[ ] migrate widget references;
* \[ ] dry-run migration;
* \[ ] backup before apply;
* \[ ] rollback migration;
* \[ ] migration report.

Acceptatiecriteria:

* \[ ] Old pack fixture migrates.
* \[ ] Unknown version blocked.
* \[ ] Migration dry-run works.
* \[ ] Backup created before apply.
* \[ ] Report secret-free.

\---

## 17\. Fase 14 - Pack Performance Budgeting

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/pack\_performance.py
```

Budgets:

* \[ ] max widgets added per pack;
* \[ ] max chart widgets;
* \[ ] max analytics queries;
* \[ ] max payload estimate;
* \[ ] max event subscriptions;
* \[ ] max workspace panels;
* \[ ] max installed packs;
* \[ ] max import file size;
* \[ ] max total pack catalog size.

Actions:

* \[ ] pass;
* \[ ] warn;
* \[ ] block;
* \[ ] recommend lighter preset.

Acceptatiecriteria:

* \[ ] Heavy pack gets warning/block.
* \[ ] Performance score shown in UI.
* \[ ] Pack install preview includes performance.
* \[ ] Tests cover heavy pack fixture.
* \[ ] No-live proof preserved.

\---

## 18\. Fase 15 - Pack Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/extension\_pack\_evidence.py
```

Bundle bevat:

* \[ ] safety contract;
* \[ ] pack schema validation;
* \[ ] registry report;
* \[ ] compatibility report;
* \[ ] install preview/dry-run report;
* \[ ] built-in template validation;
* \[ ] analytics preset validation;
* \[ ] watchlist pack validation;
* \[ ] workflow pack validation;
* \[ ] recommendation report;
* \[ ] import/export hash verification;
* \[ ] migration report;
* \[ ] performance budget report;
* \[ ] browser smoke report;
* \[ ] no-live proof;
* \[ ] redaction proof;
* \[ ] hashes.

Output:

```text
data/dashboard-v2/extension-packs/evidence/<run\_id>/
  extension\_pack\_evidence\_manifest.json
  extension\_pack\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle links to workspace evidence.
* \[ ] Dashboard can download bundle.

\---

## 19\. Fase 16 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli dashboard-v2-extension-packs --json
python -m binance\_spot\_bot.cli dashboard-v2-extension-pack-validate --path pack.json --json
python -m binance\_spot\_bot.cli dashboard-v2-extension-pack-preview --path pack.json --json
python -m binance\_spot\_bot.cli dashboard-v2-extension-pack-install --path pack.json --confirm INSTALL\_LOCAL\_PACK
python -m binance\_spot\_bot.cli dashboard-v2-extension-pack-uninstall --pack-id <id> --confirm UNINSTALL\_LOCAL\_PACK
python -m binance\_spot\_bot.cli dashboard-v2-extension-pack-enable --pack-id <id>
python -m binance\_spot\_bot.cli dashboard-v2-extension-pack-disable --pack-id <id>
python -m binance\_spot\_bot.cli dashboard-v2-extension-pack-export --pack-id <id>
python -m binance\_spot\_bot.cli dashboard-v2-extension-pack-compatibility --pack-id <id> --json
python -m binance\_spot\_bot.cli dashboard-v2-template-packs --json
python -m binance\_spot\_bot.cli dashboard-v2-analytics-presets --json
python -m binance\_spot\_bot.cli dashboard-v2-workflow-packs --json
python -m binance\_spot\_bot.cli dashboard-v2-pack-recommendations --workflow paper-session --json
python -m binance\_spot\_bot.cli dashboard-v2-extension-pack-evidence-export
```

Acceptatiecriteria:

* \[ ] Commands werken offline.
* \[ ] Commands ondersteunen JSON waar relevant.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Dangerous actions require confirm.
* \[ ] Reports zijn secret-free.

\---

## 20\. Fase 17 - Built-In Pack Catalog

Nieuwe map:

```text
src/binance\_spot\_bot/dashboard\_v2/builtin\_packs/
```

Catalog:

```text
builtin\_packs/
  beginner-paper-operator/
  demo-spot-control-room/
  market-analysis-desk/
  risk-alerts-war-room/
  model-monitoring-desk/
  portfolio-allocation-desk/
  support-evidence-desk/
  release-roadmap-ops-desk/
  uat-training-desk/
```

Per pack:

* \[ ] manifest.json;
* \[ ] workspace\_template.json;
* \[ ] analytics\_presets.json;
* \[ ] watchlists.json optional;
* \[ ] workflow\_steps.json optional;
* \[ ] docs.md;
* \[ ] evidence\_expectations.json.

Acceptatiecriteria:

* \[ ] Built-in packs validate.
* \[ ] Built-in packs install from package data.
* \[ ] Built-in packs are no-live.
* \[ ] Built-in packs are browser-smokeable.
* \[ ] Tests validate full catalog.

\---

## 21\. Fase 18 - Operator/UAT Integration

Roadmap 102:

* \[ ] Operator manual krijgt extension pack guide.
* \[ ] CLI cookbook krijgt pack commands.
* \[ ] Troubleshooting krijgt unsafe/incompatible pack playbooks.
* \[ ] Support guide krijgt pack evidence uitleg.

Roadmap 103:

* \[ ] UAT scenario: browse local pack catalog.
* \[ ] UAT scenario: preview pack install.
* \[ ] UAT scenario: install beginner paper operator pack.
* \[ ] UAT scenario: instantiate workspace from pack.
* \[ ] UAT scenario: export pack evidence.
* \[ ] UAT scenario: unsafe pack import blocked.

Acceptatiecriteria:

* \[ ] UAT scenarios pass.
* \[ ] Docs link valid.
* \[ ] Unsafe import blocked in UAT.
* \[ ] No-live proof included.
* \[ ] UAT feedback can create pack backlog items.

\---

## 22\. Fase 19 - Release/Knowledge/Test/Performance Integration

Roadmap 089:

* \[ ] Release notes include built-in pack catalog.
* \[ ] Version manifest includes pack schema version.
* \[ ] Migration notes include pack migration.

Roadmap 091:

* \[ ] Knowledge graph maps packs to widgets/routes/API/docs.
* \[ ] Impact analysis detects widget changes affecting packs.
* \[ ] Ownership map includes built-in packs.

Roadmap 092:

* \[ ] Test selector chooses pack validation tests for pack changes.
* \[ ] Widget registry changes select pack compatibility tests.
* \[ ] Frontend pack UI changes select browser smoke.

Roadmap 093:

* \[ ] Pack performance budgets tracked.
* \[ ] Heavy pack warnings become findings.
* \[ ] Pack install preview includes performance.

Acceptatiecriteria:

* \[ ] Release evidence includes pack evidence.
* \[ ] Knowledge graph updated.
* \[ ] Test selection works.
* \[ ] Performance reports include pack budgets.
* \[ ] No-live proof preserved.

\---

## 23\. Fase 20 - Scheduled Pack Reports

Uitbreiding op local scheduled reports:

Scheduled jobs:

* \[ ] weekly pack registry validation;
* \[ ] weekly installed pack compatibility check;
* \[ ] weekly built-in pack validation;
* \[ ] weekly pack performance report;
* \[ ] monthly pack evidence export;
* \[ ] post-release pack migration dry-run;
* \[ ] post-widget-registry-change pack compatibility run.

Metrics:

* \[ ] installed pack count;
* \[ ] enabled pack count;
* \[ ] incompatible pack count;
* \[ ] blocked unsafe pack count;
* \[ ] built-in pack validation status;
* \[ ] pack performance warnings;
* \[ ] pack import/export failures;
* \[ ] pack evidence export status.

Acceptatiecriteria:

* \[ ] Reports are local-only.
* \[ ] Reports are secret-free.
* \[ ] Dashboard can show reports.
* \[ ] No-live proof included.
* \[ ] No live trading.

\---

## 24\. Tests

### Unit tests

* \[ ] `tests/test\_dashboard\_v2\_extension\_pack\_safety\_contract.py`
* \[ ] `tests/test\_dashboard\_v2\_extension\_pack\_schema.py`
* \[ ] `tests/test\_dashboard\_v2\_extension\_pack\_registry.py`
* \[ ] `tests/test\_dashboard\_v2\_pack\_compatibility.py`
* \[ ] `tests/test\_dashboard\_v2\_pack\_install\_preview.py`
* \[ ] `tests/test\_dashboard\_v2\_workspace\_template\_packs.py`
* \[ ] `tests/test\_dashboard\_v2\_analytics\_preset\_packs.py`
* \[ ] `tests/test\_dashboard\_v2\_watchlist\_packs.py`
* \[ ] `tests/test\_dashboard\_v2\_workflow\_packs.py`
* \[ ] `tests/test\_dashboard\_v2\_pack\_recommendations.py`
* \[ ] `tests/test\_dashboard\_v2\_extension\_pack\_api.py`
* \[ ] `tests/test\_dashboard\_v2\_pack\_import\_export.py`
* \[ ] `tests/test\_dashboard\_v2\_pack\_migrations.py`
* \[ ] `tests/test\_dashboard\_v2\_pack\_performance.py`
* \[ ] `tests/test\_dashboard\_v2\_extension\_pack\_evidence.py`

### Integration tests

* \[ ] Validate built-in catalog.
* \[ ] Preview install built-in pack.
* \[ ] Install built-in pack into temp registry.
* \[ ] Instantiate workspace from template pack.
* \[ ] Run analytics presets with fixture snapshot.
* \[ ] Import/export watchlist pack.
* \[ ] Generate recommendations from fixture operator context.
* \[ ] Export extension pack evidence.
* \[ ] Migrate old pack fixture.
* \[ ] Reject tampered pack.

### Browser smoke

* \[ ] `/extension-packs` loads.
* \[ ] catalog page loads.
* \[ ] pack details opens.
* \[ ] install preview works.
* \[ ] unsafe pack blocked.
* \[ ] instantiate workspace button works.
* \[ ] analytics presets page loads.
* \[ ] workflow packs page loads.
* \[ ] no-live banner visible.
* \[ ] no live controls visible.

### Safety tests

* \[ ] Pack with live mode blocked.
* \[ ] Pack with signed/order/account action blocked.
* \[ ] Pack with script/html injection blocked.
* \[ ] Unknown widget type blocked.
* \[ ] Pack cannot hide no-live widget.
* \[ ] Pack cannot hide stop control in operator mode.
* \[ ] Pack export redacts secrets.
* \[ ] Remote URL marketplace blocked.
* \[ ] No arbitrary code execution.
* \[ ] Check-all safe env preserved.

\---

## 25\. Docs

Nieuwe docs:

```text
docs/dashboard-v2/extension-pack-safety-contract.md
docs/dashboard-v2/extension-pack-schema.md
docs/dashboard-v2/local-pack-registry.md
docs/dashboard-v2/pack-compatibility.md
docs/dashboard-v2/pack-install-preview.md
docs/dashboard-v2/workspace-template-packs.md
docs/dashboard-v2/analytics-preset-packs.md
docs/dashboard-v2/watchlist-packs.md
docs/dashboard-v2/workflow-packs.md
docs/dashboard-v2/pack-recommendations.md
docs/dashboard-v2/extension-pack-api.md
docs/dashboard-v2/extension-pack-dashboard-ui.md
docs/dashboard-v2/pack-import-export.md
docs/dashboard-v2/pack-migrations.md
docs/dashboard-v2/pack-performance-budgets.md
docs/dashboard-v2/extension-pack-evidence-bundle.md
```

README updates:

* \[ ] Dashboard V2 extension packs overview.
* \[ ] Difference between plugin-less packs and unsafe plugins.
* \[ ] How to browse built-in packs.
* \[ ] How to preview install.
* \[ ] How to instantiate workspace from pack.
* \[ ] How to export evidence.
* \[ ] No-live statement.

Operator docs updates:

* \[ ] Extension pack guide.
* \[ ] Template pack guide.
* \[ ] Analytics preset guide.
* \[ ] Unsafe pack troubleshooting.
* \[ ] Pack evidence guide.

\---

## 26\. Codex bouwvolgorde

### PR 1 - Safety Contract + Pack Schema

* \[ ] `docs/dashboard-v2-extension-pack-safety-contract.md`
* \[ ] `extension\_pack\_schema.py`
* \[ ] schema/validation tests.
* \[ ] no-live tests.

### PR 2 - Local Pack Registry

* \[ ] `extension\_pack\_registry.py`
* \[ ] local registry storage.
* \[ ] temp-dir tests.

### PR 3 - Compatibility + Install Preview

* \[ ] `pack\_compatibility.py`
* \[ ] `pack\_install\_preview.py`
* \[ ] compatibility/dry-run tests.

### PR 4 - Workspace Template Packs

* \[ ] `workspace\_template\_packs.py`
* \[ ] built-in workspace templates.
* \[ ] template validation tests.

### PR 5 - Analytics Preset Packs

* \[ ] `analytics\_preset\_packs.py`
* \[ ] local analytics presets.
* \[ ] fixture snapshot/session tests.

### PR 6 - Watchlist + Workflow Packs

* \[ ] `watchlist\_packs.py`
* \[ ] `workflow\_packs.py`
* \[ ] symbol/command/doc validation tests.

### PR 7 - Recommendation Engine + API

* \[ ] `pack\_recommendations.py`
* \[ ] FastAPI routes.
* \[ ] TestClient tests.

### PR 8 - Dashboard UI + Built-In Catalog

* \[ ] extension pack frontend pages.
* \[ ] built-in catalog files.
* \[ ] browser smoke.

### PR 9 - Import/Export + Migrations + Performance

* \[ ] pack import/export/hash verification.
* \[ ] `pack\_migrations.py`
* \[ ] `pack\_performance.py`
* \[ ] tamper/heavy pack tests.

### PR 10 - Evidence, CLI, Docs \& Integrations

* \[ ] `extension\_pack\_evidence.py`
* \[ ] CLI commands.
* \[ ] docs/operator/UAT/release/test/knowledge integration.
* \[ ] scheduled reports.

\---

## 27\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 111 PR 1: Dashboard V2 Extension Pack Safety Contract + Plugin-Less Pack Schema.

Maak docs/dashboard-v2-extension-pack-safety-contract.md.

Maak src/binance\_spot\_bot/dashboard\_v2/extension\_pack\_schema.py met:
- DashboardExtensionPack
- DashboardExtensionPackManifest
- DashboardPackContent
- DashboardPackDependency
- DashboardPackCompatibility
- DashboardPackValidationResult
- validate\_dashboard\_extension\_pack(pack: DashboardExtensionPack)
- dashboard\_extension\_pack\_to\_dict(...)
- load\_dashboard\_extension\_pack(path: Path)
- write\_dashboard\_extension\_pack(path: Path, pack: DashboardExtensionPack)

Pack manifest moet minimaal ondersteunen:
- pack\_id
- name
- description
- version
- author
- created\_at\_ms
- pack\_type
- compatible\_workspace\_schema\_versions
- required\_widget\_types
- required\_dashboard\_v2\_features
- mode\_scope
- operator\_level
- tags
- no\_live\_statement
- live\_trading\_enabled=False
- content\_hash

Pack content moet minimaal ondersteunen:
- workspace\_templates
- widget\_presets
- analytics\_presets
- watchlists
- workflow\_steps
- docs
- evidence\_expectations

Validatie moet blokkeren op:
- live mode in mode\_scope
- live\_trading\_enabled=True
- unknown pack\_type
- missing no\_live\_statement
- unknown/empty required widget type
- script/html injection in any string field
- Python/JS/code execution fields zoals code, script, eval, function\_body
- raw secret-like values
- remote marketplace/download URL
- workspace template zonder no\_live\_banner
- workspace template zonder stop/runtime safety widget in operator mode
- unsupported schema version

Gebruik alleen stdlib.
Geen command execution.
Geen frontend execution.
Geen backend server starten.
Geen Streamlit wijzigen.
Geen GitHub API calls.
Geen remote downloads.
Geen signed endpoints.
Geen account/order endpoints.
Geen live trading.

Voeg tests toe voor:
- valid plugin-less pack
- live mode blocked
- live\_trading\_enabled True blocked
- unknown pack\_type blocked
- missing no\_live\_statement blocked
- script injection blocked
- code execution field blocked
- remote URL blocked
- secret-like values worden geredact/geblokkeerd
- missing safety widget blocked
- JSON serialization
- content hash deterministic
- live\_trading\_enabled=False
- no\_live\_statement aanwezig
```

Waarom eerst:

* Extension packs zijn pas veilig als het pack schema onmogelijk maakt dat er plugin-code, live actions of unsafe widgets binnenkomen.
* Het is read-only en raakt runtime/trading/frontend niet.
* Het is klein genoeg voor Codex.
* No-live, secret-free en no-code-execution checks kunnen meteen getest worden.
* Daarna kunnen registry, template packs en dashboard UI veilig op dit schema bouwen.

\---

## 28\. Definition of Done

Roadmap 111 is klaar als:

* \[ ] Plugin-Less Extension Pack Safety Contract bestaat.
* \[ ] Extension Pack Schema werkt.
* \[ ] Local Pack Registry werkt.
* \[ ] Pack Compatibility Engine werkt.
* \[ ] Pack Preview \& Dry-Run Install werkt.
* \[ ] Workspace Template Packs werken.
* \[ ] Analytics Preset Packs werken.
* \[ ] Watchlist \& Symbol Group Packs werken.
* \[ ] Workflow Pack Builder werkt.
* \[ ] Pack Recommendation Engine werkt.
* \[ ] Extension Pack API werkt.
* \[ ] Extension Pack Dashboard UI werkt.
* \[ ] Pack Import/Export \& Signing-Lite Hashes werken.
* \[ ] Pack Migration System werkt.
* \[ ] Pack Performance Budgeting werkt.
* \[ ] Pack Evidence Bundle werkt.
* \[ ] CLI commands werken.
* \[ ] Built-In Pack Catalog bestaat.
* \[ ] Operator/UAT integration werkt.
* \[ ] Release/Knowledge/Test/Performance integration werkt.
* \[ ] Scheduled Pack Reports werken.
* \[ ] Tests bewijzen geen plugin-code execution.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen unsafe packs geblokkeerd worden.
* \[ ] Tests bewijzen pack import/export secret-free is.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Dashboard V2 pack catalog is local-only.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 111 kan na uitvoering naar `Voltooid docs`.

\---

## 29\. Verwachte Roadmap 112 daarna

Als Roadmap 111 groen is:

```text
Roadmap 112 - Dashboard V2 Local Market Intelligence Workbench, Binance Spot Scanner \& Multi-Symbol Paper Analytics
```

Mogelijke inhoud:

* \[ ] multi-symbol market scanner;
* \[ ] Binance public market metadata ingestion;
* \[ ] watchlist live snapshots;
* \[ ] spread/volume/volatility ranking;
* \[ ] paper strategy comparison per symbol;
* \[ ] no-live scanner evidence;
* \[ ] still no live trading.

```

Als Roadmap 111 zware workspace/pack performanceproblemen vindt:

```text
Roadmap 112 - Dashboard V2 Pack Performance Burn-Down, Workspace Query Cache \& Widget Virtualization
```

Mogelijke inhoud:

* \[ ] pack performance bottlenecks oplossen;
* \[ ] analytics query cache;
* \[ ] widget virtualization;
* \[ ] large watchlist optimization;
* \[ ] payload diffing;
* \[ ] still no live trading.

```

