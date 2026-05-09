# Roadmap 012 - Advanced Scanner UX, Experiment Database, Notebook Exports \& Dashboard Performance

Status: Concept / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-09  
Voorgestelde bestandsnaam:

```text
Roadmap docs/012-roadmap-advanced-scanner-experiment-database-notebook-exports-dashboard-performance.md
```

Volgt op:

* `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
* `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
* `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
* `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
* `Roadmap docs/005-roadmap-long-paper-testnet-alerts-scanner-packaging.md`
* `006-roadmap-multi-symbol-portfolio-testnet-endurance-mlops.md`
* `007-roadmap-live-readiness-audit-shadow-chaos-release-governance.md`
* `008-roadmap-strict-live-readiness-pilot-design.md`
* `009-roadmap-unified-dashboard-launcher-binance-spot-demo-trading-control-center.md`
* `010-roadmap-dashboard-strategy-lab-signal-debugging-replay-sandbox.md`
* `011-roadmap-safe-dashboard-copilot-strategy-templates-dataset-builder-ui.md`

Doel: Roadmap 012 maakt het project beter als lokaal research- en dashboardplatform. De focus ligt op advanced scanner UX, een lokale experiment database, notebook/HTML exports, performance/profiling, data caching en optionele offline/local LLM integratie. Dit maakt het dashboard sneller, overzichtelijker en beter bruikbaar voor strategieonderzoek zonder live trading te activeren.

Live trading blijft volledig buiten scope.

\---

## 0\. Waarom deze Roadmap 012

Roadmap 009 maakt de startflow en demo trading beter.  
Roadmap 010 maakt Strategy Lab, signal debugging en replay mogelijk.  
Roadmap 011 maakt Copilot, strategy templates en dataset/model wizards mogelijk.

Daarna is de volgende logische stap:

* \[ ] alle experimenten netjes bewaren;
* \[ ] scanner-resultaten beter visualiseren;
* \[ ] dashboard sneller maken;
* \[ ] research exports maken;
* \[ ] lokale notebooks genereren;
* \[ ] data caching verbeteren;
* \[ ] offline/local LLM support optioneel toevoegen;
* \[ ] performance bottlenecks opsporen.

\---

## 1\. Onderzoek en huidige basis

### Repo-status

* \[x] Er is geen Roadmap 012 gevonden in de repo-zoekresultaten.
* \[x] Dashboard is momenteel Streamlit-gebaseerd en bevat al veel tabs.
* \[x] Dashboard gebruikt runtime snapshots en session state.
* \[x] `SessionStore` bewaart summaries, snapshots en fills in lokale JSON/JSONL/CSV bestanden.
* \[x] `DataStore` bewaart raw JSON, processed candle CSV en features/labels JSONL.
* \[x] Binance Spot public market data is geschikt voor scanner preview en research zonder credentials.

### Huidige beperkingen

* \[ ] Geen centrale experiment database.
* \[ ] Geen snelle query/index over oude sessies.
* \[ ] Geen notebook exports.
* \[ ] Geen HTML research reports.
* \[ ] Geen dashboard performance profiler.
* \[ ] Geen data cache management UI.
* \[ ] Geen advanced scanner heatmap/market map.
* \[ ] Geen lokaal/offline LLM pad.
* \[ ] Geen experiment lineage tussen dataset → model → session → report.
* \[ ] Geen archivering/cleanup voor data directories.

\---

## 2\. Scope

### In scope

* \[ ] Advanced scanner UX.
* \[ ] Market heatmap.
* \[ ] Scanner ranking history.
* \[ ] Local experiment database.
* \[ ] DuckDB/SQLite optional backend.
* \[ ] Notebook exports.
* \[ ] HTML research reports.
* \[ ] Dashboard performance profiler.
* \[ ] Data cache manager.
* \[ ] Experiment lineage graph.
* \[ ] Offline/local LLM integration as optional read-only helper.
* \[ ] Data cleanup/archive UI.
* \[ ] Research workspace.

### Out of scope

* \[ ] Live trading.
* \[ ] Live pilot implementation.
* \[ ] Cloud deployment as requirement.
* \[ ] Remote code execution plugins.
* \[ ] Strategy marketplace with untrusted code.
* \[ ] Futures/margin/leverage.
* \[ ] AI order placement.

\---

## 3\. Fase 0 - Research workspace safety contract

Doel: research-functionaliteit veilig houden.

### Taken

* \[ ] Maak `docs/research-workspace-safety-contract.md`.
* \[ ] Definieer research workspace als:

  * read-only analysis;
  * demo/paper/testnet report analysis;
  * no live execution;
  * no signed order calls;
  * no secret exposure.
* \[ ] Voeg dashboard badge toe:

  * `Research Workspace = analysis only`.
* \[ ] Tests:

  * workspace kan geen live mode activeren;
  * workspace kan geen order plaatsen;
  * exports bevatten geen secrets;
  * local LLM krijgt alleen redacted payloads.

### Acceptatiecriteria

* \[ ] Safety contract bestaat.
* \[ ] Dashboard toont safety badge.
* \[ ] Geen research feature kan order execution triggeren.
* \[ ] Security scan controleert exports.

\---

## 4\. Fase 1 - Experiment Database

Doel: alle experimenten, sessies, datasets, modellen en reports centraal indexeren.

### Nieuwe module

```text
src/binance\_spot\_bot/experiment\_db.py
```

### Backend opties

* \[ ] JSON index als fallback.
* \[ ] SQLite als standaard lichtgewicht optie.
* \[ ] DuckDB optioneel voor analytics.
* \[ ] Geen zware dependency verplicht voor demo.

### Tabellen / collecties

* \[ ] experiments;
* \[ ] sessions;
* \[ ] datasets;
* \[ ] models;
* \[ ] strategy\_templates;
* \[ ] scanner\_runs;
* \[ ] reports;
* \[ ] alerts;
* \[ ] evidence\_records.

### Velden experiment

* \[ ] experiment\_id;
* \[ ] name;
* \[ ] type;
* \[ ] created\_at;
* \[ ] symbol(s);
* \[ ] interval;
* \[ ] strategy/template;
* \[ ] model\_id;
* \[ ] dataset\_id;
* \[ ] session\_id;
* \[ ] report\_path;
* \[ ] metrics;
* \[ ] tags;
* \[ ] notes;
* \[ ] hash.

### CLI

```powershell
python -m binance\_spot\_bot.cli experiment-list
python -m binance\_spot\_bot.cli experiment-show --experiment-id <id>
python -m binance\_spot\_bot.cli experiment-index-sessions
```

### Acceptatiecriteria

* \[ ] Oude sessions kunnen worden geïndexeerd.
* \[ ] Nieuwe experiments worden automatisch geregistreerd.
* \[ ] Dashboard kan zoeken/filteren.
* \[ ] Fallback werkt zonder SQLite/DuckDB.
* \[ ] Geen secrets in database.

\---

## 5\. Fase 2 - Experiment Lineage Graph

Doel: zien welke dataset/model/session/report bij elkaar horen.

### Nieuwe module

```text
src/binance\_spot\_bot/lineage.py
```

### Graph nodes

* \[ ] dataset;
* \[ ] feature set;
* \[ ] model;
* \[ ] strategy template;
* \[ ] scanner run;
* \[ ] paper session;
* \[ ] testnet session;
* \[ ] report;
* \[ ] evidence record.

### Dashboard UI

* \[ ] Lineage tab.
* \[ ] Node list.
* \[ ] Directed graph.
* \[ ] Click node for metadata.
* \[ ] Missing link warnings.
* \[ ] Export lineage as JSON/Markdown.

### Acceptatiecriteria

* \[ ] Gebruiker ziet van welke dataset een model komt.
* \[ ] Gebruiker ziet welke sessies met welk model draaiden.
* \[ ] Gebruiker ziet welke reports bij welke experimenten horen.
* \[ ] Missing metadata wordt zichtbaar.

\---

## 6\. Fase 3 - Advanced Scanner UX

Doel: scanner-resultaten bruikbaar maken voor research.

### Scanner dashboards

* \[ ] Watchlist ranking.
* \[ ] Symbol heatmap.
* \[ ] Spread heatmap.
* \[ ] Volume/quote-volume panel.
* \[ ] Signal confidence grid.
* \[ ] Risk block matrix.
* \[ ] Data quality matrix.
* \[ ] Top movers.
* \[ ] Lowest spread pairs.
* \[ ] High volume pairs.
* \[ ] Candidate watchlist export.

### Scanner result fields

* \[ ] symbol;
* \[ ] price;
* \[ ] 1h change;
* \[ ] 24h change;
* \[ ] quote volume;
* \[ ] spread bps;
* \[ ] signal;
* \[ ] confidence;
* \[ ] risk block reason;
* \[ ] data quality;
* \[ ] model version;
* \[ ] timestamp.

### Acceptatiecriteria

* \[ ] Scanner plaatst geen orders.
* \[ ] Scanner gebruikt public/demo data.
* \[ ] Symbol ranking is uitlegbaar.
* \[ ] Scanner run wordt experiment record.
* \[ ] Watchlist kan worden opgeslagen en geëxporteerd.

\---

## 7\. Fase 4 - Scanner History \& Replay

Doel: scannerresultaten over tijd vergelijken.

### Taken

* \[ ] Bewaar scanner snapshots.
* \[ ] Maak scanner history chart.
* \[ ] Toon ranking changes.
* \[ ] Toon symbols die vaak kandidaat zijn.
* \[ ] Toon symbols die vaak geblokkeerd worden.
* \[ ] Replay scanner state per timestamp.
* \[ ] Export scanner history.

### Acceptatiecriteria

* \[ ] Scanner trends zijn zichtbaar.
* \[ ] Gebruiker kan zien of een symbol consistent interessant is.
* \[ ] Scanner history werkt offline.
* \[ ] Geen live execution.

\---

## 8\. Fase 5 - Notebook Export Generator

Doel: onderzoek exporteren naar lokale notebooks.

### Nieuwe module

```text
src/binance\_spot\_bot/notebook\_export.py
```

### Exports

* \[ ] Jupyter notebook `.ipynb`.
* \[ ] Markdown notebook.
* \[ ] Python script `.py`.
* \[ ] HTML report optional.

### Notebook types

* \[ ] Session analysis notebook.
* \[ ] Strategy Lab notebook.
* \[ ] Parameter sweep notebook.
* \[ ] Model training notebook.
* \[ ] Scanner analysis notebook.
* \[ ] Dataset quality notebook.
* \[ ] Risk block analysis notebook.

### Acceptatiecriteria

* \[ ] Notebook bevat data paths, metrics en charts.
* \[ ] Notebook bevat geen secrets.
* \[ ] Notebook kan offline worden geopend.
* \[ ] Notebook export is reproduceerbaar.
* \[ ] Export wordt experiment record.

\---

## 9\. Fase 6 - HTML Research Reports

Doel: mooie lokale rapporten maken zonder dashboard nodig te hebben.

### Nieuwe module

```text
src/binance\_spot\_bot/html\_reports.py
```

### Reports

* \[ ] Session report.
* \[ ] Strategy report.
* \[ ] Scanner report.
* \[ ] Model comparison report.
* \[ ] Dataset report.
* \[ ] Portfolio report.
* \[ ] Risk report.

### Inhoud

* \[ ] summary cards;
* \[ ] charts;
* \[ ] tables;
* \[ ] parameters;
* \[ ] warnings;
* \[ ] limitations;
* \[ ] no financial advice / paper-not-live disclaimer.

### Acceptatiecriteria

* \[ ] HTML opent lokaal.
* \[ ] Geen externe server nodig.
* \[ ] Geen secrets in HTML.
* \[ ] Report link zichtbaar in dashboard.

\---

## 10\. Fase 7 - Dashboard Performance Profiler

Doel: Streamlit-dashboard sneller en stabieler maken.

### Nieuwe module

```text
src/binance\_spot\_bot/dashboard\_profiler.py
```

### Meetpunten

* \[ ] render time per tab;
* \[ ] chart build time;
* \[ ] data load time;
* \[ ] session load time;
* \[ ] scanner run time;
* \[ ] cache hit rate;
* \[ ] memory usage optional;
* \[ ] large table warning.

### Dashboard UI

* \[ ] Performance tab.
* \[ ] Slowest components.
* \[ ] Cache stats.
* \[ ] Large session warnings.
* \[ ] Recommended actions.

### Acceptatiecriteria

* \[ ] Dashboard kan performance bottlenecks tonen.
* \[ ] Profiler kan uitgezet worden.
* \[ ] Profiler lekt geen secrets.
* \[ ] Performance reports exporteerbaar.

\---

## 11\. Fase 8 - Cache Manager

Doel: data-caching inzichtelijk en controleerbaar maken.

### Nieuwe module

```text
src/binance\_spot\_bot/cache\_manager.py
```

### Cache types

* \[ ] public spot klines;
* \[ ] symbol filters;
* \[ ] scanner snapshots;
* \[ ] generated reports;
* \[ ] notebooks;
* \[ ] model metrics;
* \[ ] dashboard computed charts.

### UI

* \[ ] Cache size.
* \[ ] Cache last updated.
* \[ ] Clear selected cache.
* \[ ] Rebuild cache.
* \[ ] Export cache manifest.
* \[ ] Archive old cache.

### Acceptatiecriteria

* \[ ] Gebruiker ziet hoeveel data lokaal staat.
* \[ ] Cache kan veilig opgeschoond worden.
* \[ ] Geen models/sessions per ongeluk wissen zonder confirm.
* \[ ] Cache manifest bevat hashes.

\---

## 12\. Fase 9 - Data Archive \& Cleanup UI

Doel: data directory beheersbaar houden.

### Taken

* \[ ] Toon data directory overview.
* \[ ] Toon grootste mappen.
* \[ ] Archive old sessions.
* \[ ] Archive old reports.
* \[ ] Archive old scanner snapshots.
* \[ ] Keep/delete policy.
* \[ ] Confirm required voor delete.
* \[ ] Secret scan vóór archive/export.

### Acceptatiecriteria

* \[ ] Data cleanup wist niet per ongeluk actieve sessies.
* \[ ] Archive bevat manifest.
* \[ ] Delete vereist confirm phrase.
* \[ ] Security scan draait vóór export.

\---

## 13\. Fase 10 - Optional Offline Local LLM Integration

Doel: lokale AI-hulp mogelijk maken zonder externe API en zonder orderrechten.

### Ondersteunde richting

* \[ ] Local HTTP endpoint, bijvoorbeeld Ollama/LM Studio-compatible.
* \[ ] Geen verplichte dependency.
* \[ ] Alleen read-only summaries.
* \[ ] Redacted payloads.
* \[ ] Timeout en fallback.
* \[ ] Geen tool-calling naar execution.
* \[ ] Geen secrets.

### Nieuwe module

```text
src/binance\_spot\_bot/local\_llm.py
```

### Use cases

* \[ ] Session summary.
* \[ ] Risk block explanation.
* \[ ] Strategy Lab report summary.
* \[ ] Dataset quality explanation.
* \[ ] Scanner summary.
* \[ ] Next safe research steps.

### Acceptatiecriteria

* \[ ] Local LLM is optioneel.
* \[ ] Dashboard werkt zonder local LLM.
* \[ ] Local LLM krijgt geen secrets.
* \[ ] Local LLM kan geen orders plaatsen.
* \[ ] Fallback rule-based summary blijft bestaan.

\---

## 14\. Fase 11 - Research Workspace Dashboard

Doel: één plek voor experiments, reports, notebooks en scanner research.

### Nieuwe tab

```text
Research Workspace
```

### Panels

* \[ ] Recent experiments.
* \[ ] Favorite experiments.
* \[ ] Scanner runs.
* \[ ] Reports.
* \[ ] Notebooks.
* \[ ] Datasets.
* \[ ] Models.
* \[ ] Tags.
* \[ ] Search.
* \[ ] Export bundle.

### Acceptatiecriteria

* \[ ] Onderzoek is vindbaar.
* \[ ] Reports/notebooks zijn downloadbaar.
* \[ ] Experimenten kunnen getagd worden.
* \[ ] Workspace werkt offline.

\---

## 15\. Fase 12 - Experiment Bundle Export

Doel: één experiment compleet kunnen delen/archiveren.

### Bundle inhoud

* \[ ] experiment metadata;
* \[ ] dataset manifest;
* \[ ] model metadata;
* \[ ] session summary;
* \[ ] fills/equity CSV;
* \[ ] scanner results;
* \[ ] charts;
* \[ ] notebook;
* \[ ] HTML report;
* \[ ] redacted config;
* \[ ] hash manifest.

### Acceptatiecriteria

* \[ ] Bundle bevat geen secrets.
* \[ ] Bundle heeft manifest.
* \[ ] Bundle kan later opnieuw geïmporteerd worden.
* \[ ] Import overschrijft niets zonder confirm.

\---

## 16\. Fase 13 - Tests

### Unit tests

* \[ ] `tests/test\_experiment\_db.py`
* \[ ] `tests/test\_lineage.py`
* \[ ] `tests/test\_advanced\_scanner\_ux.py`
* \[ ] `tests/test\_scanner\_history.py`
* \[ ] `tests/test\_notebook\_export.py`
* \[ ] `tests/test\_html\_reports.py`
* \[ ] `tests/test\_dashboard\_profiler.py`
* \[ ] `tests/test\_cache\_manager.py`
* \[ ] `tests/test\_data\_archive.py`
* \[ ] `tests/test\_local\_llm.py`
* \[ ] `tests/test\_experiment\_bundle.py`

### Integration tests

* \[ ] Index old sessions.
* \[ ] Create scanner run experiment.
* \[ ] Export notebook.
* \[ ] Export HTML report.
* \[ ] Generate lineage graph.
* \[ ] Clear cache safely.
* \[ ] Export experiment bundle.
* \[ ] Local LLM mock summary.
* \[ ] Security scan exported artifacts.

### Safety tests

* \[ ] No live execution.
* \[ ] No signed order endpoints.
* \[ ] No secrets in notebooks.
* \[ ] No secrets in HTML.
* \[ ] No secrets in experiment DB.
* \[ ] Local LLM receives redacted payload only.

\---

## 17\. Nieuwe bestanden

### Source

* \[ ] `src/binance\_spot\_bot/experiment\_db.py`
* \[ ] `src/binance\_spot\_bot/lineage.py`
* \[ ] `src/binance\_spot\_bot/scanner\_history.py`
* \[ ] `src/binance\_spot\_bot/notebook\_export.py`
* \[ ] `src/binance\_spot\_bot/html\_reports.py`
* \[ ] `src/binance\_spot\_bot/dashboard\_profiler.py`
* \[ ] `src/binance\_spot\_bot/cache\_manager.py`
* \[ ] `src/binance\_spot\_bot/data\_archive.py`
* \[ ] `src/binance\_spot\_bot/local\_llm.py`
* \[ ] `src/binance\_spot\_bot/experiment\_bundle.py`
* \[ ] `src/binance\_spot\_bot/ui/research\_workspace.py`
* \[ ] `src/binance\_spot\_bot/ui/scanner\_dashboard.py`
* \[ ] `src/binance\_spot\_bot/ui/performance.py`

### Docs

* \[ ] `docs/research-workspace-safety-contract.md`
* \[ ] `docs/experiment-database.md`
* \[ ] `docs/experiment-lineage.md`
* \[ ] `docs/advanced-scanner-ux.md`
* \[ ] `docs/notebook-exports.md`
* \[ ] `docs/html-reports.md`
* \[ ] `docs/dashboard-performance.md`
* \[ ] `docs/cache-manager.md`
* \[ ] `docs/data-archive-cleanup.md`
* \[ ] `docs/local-llm-integration.md`
* \[ ] `docs/experiment-bundles.md`

\---

## 18\. Prioriteiten

### Eerst

1. \[ ] Research workspace safety contract.
2. \[ ] Experiment Database.
3. \[ ] Experiment Lineage Graph.
4. \[ ] Advanced Scanner UX.
5. \[ ] Scanner History.

### Daarna

6. \[ ] Notebook Export Generator.
7. \[ ] HTML Research Reports.
8. \[ ] Research Workspace Dashboard.
9. \[ ] Experiment Bundle Export.

### Als laatste

10. \[ ] Dashboard Performance Profiler.
11. \[ ] Cache Manager.
12. \[ ] Data Archive \& Cleanup UI.
13. \[ ] Optional Offline Local LLM Integration.

\---

## 19\. Definition of Done

Roadmap 012 is klaar als:

* \[ ] Experiment database werkt met fallback.
* \[ ] Oude sessions zijn indexeerbaar.
* \[ ] Lineage tussen dataset/model/session/report is zichtbaar.
* \[ ] Advanced scanner UX werkt zonder orders.
* \[ ] Scanner history wordt opgeslagen en weergegeven.
* \[ ] Notebook exports werken.
* \[ ] HTML reports werken.
* \[ ] Dashboard profiler toont bottlenecks.
* \[ ] Cache manager werkt veilig.
* \[ ] Data archive/cleanup werkt met confirm.
* \[ ] Local LLM is optioneel en read-only.
* \[ ] Research Workspace bundelt experiments/reports/notebooks.
* \[ ] Experiment bundle export bevat geen secrets.
* \[ ] Alle tests slagen.
* \[ ] Security scan is groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 012 kan na uitvoering naar `Voltooid docs`.

\---

## 20\. Verwachte Roadmap 013 daarna

Na Roadmap 012 zou ik Roadmap 013 richten op:

* \[ ] production-quality testing harness;
* \[ ] CI/CD hardening;
* \[ ] static typing/mypy;
* \[ ] mutation testing;
* \[ ] benchmark suite;
* \[ ] plugin sandboxing;
* \[ ] release signing;
* \[ ] full documentation portal;
* \[ ] installer UX.

