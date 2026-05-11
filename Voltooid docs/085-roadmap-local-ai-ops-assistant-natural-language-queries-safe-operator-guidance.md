# Roadmap 085 - Local AI Ops Assistant, Natural Language Queries \& Safe Operator Guidance

Status: Niet volledig voltooid / opnieuw gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/085-roadmap-local-ai-ops-assistant-natural-language-queries-safe-operator-guidance.md
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

Doel: Roadmap 084 maakt metrics warehouse, observability, SLO’s, anomaly detection en long-term analytics mogelijk. Roadmap 085 bouwt daarop een **lokale AI/Ops-assistent** die natuurlijke taalvragen kan beantwoorden over de lokale paper-ops status, metrics, reports, runbooks, anomalies, governance, support bundles en evidence. De assistent mag alleen uitleggen, samenvatten, query’s uitvoeren op lokale redacted artifacts en veilige operatoracties voorstellen. Hij mag nooit live trading activeren, orders plaatsen, signed endpoints gebruiken of zonder bevestiging commands uitvoeren.

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
  * live trading disabled.
* \[x] Geen bestaande Roadmap 085 gevonden via repo-search.
* \[x] Roadmap 084 is lokaal aangemaakt voor local observability, metrics warehouse en long-term analytics.

### Codebasecontrole

Gecontroleerde relevante modules:

* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] `src/binance\_spot\_bot/redaction.py`
* \[x] bestaande operatorlaag bevat al:

  * artifact catalog;
  * operator health score;
  * evidence chain;
  * environment doctor;
  * data growth budget;
  * diagnostics baseline;
  * report index;
  * support bundle verification;
  * redaction self-test;
  * local ops snapshot;
  * operator quality gate;
  * incident timeline;
  * retention preview;
  * state archive.
* \[x] `redaction.py` bevat al redaction voor:

  * OpenAI-like keys;
  * Binance API key/secret;
  * signature;
  * listenKey;
  * lange token-achtige strings;
  * JSON secret fields.

### Belangrijkste gat na Roadmap 084

Na Roadmap 084 zijn metrics, trends en anomalies beschikbaar, maar de operator moet nog zelf interpreteren:

* \[ ] waarom health score lager is;
* \[ ] welke report/anomaly het belangrijkst is;
* \[ ] welke runbook bij een probleem hoort;
* \[ ] welke evidence ontbreekt;
* \[ ] welke scheduled job faalt;
* \[ ] wat de volgende veilige stap is;
* \[ ] hoe een incident samengevat moet worden;
* \[ ] welke CLI command veilig is om te draaien;
* \[ ] welke acties risk-verhogend zijn en dus geblokkeerd moeten worden.

Roadmap 085 lost dit op met een lokale, redacted, read-only AI/Ops-assistent.

\---

## 1\. Hoofddoel Roadmap 085

Maak een **lokale AI/Ops-assistent** voor veilige operatorvragen:

```text
Metrics warehouse + reports + runbooks + evidence
→ redacted context builder
→ local query engine
→ safe natural language answer
→ recommended next action
→ optional manual command proposal
→ no auto execution
```

Na Roadmap 085 moet de operator kunnen vragen:

* \[ ] “Waarom is mijn health score vandaag lager?”
* \[ ] “Welke scheduled jobs faalden deze week?”
* \[ ] “Welke runbook moet ik volgen voor deze dashboard smoke failure?”
* \[ ] “Wat is de belangrijkste blocker voordat ik een paper session start?”
* \[ ] “Welke evidence ontbreekt voor mijn weekly governance report?”
* \[ ] “Waarom is mijn data growth budget overschreden?”
* \[ ] “Vat de laatste support bundle samen.”
* \[ ] “Welke paper policy staat op watch en waarom?”
* \[ ] “Welke actie is veilig als volgende stap?”
* \[ ] “Maak een commandvoorstel, maar voer niets uit.”

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen Binance account endpoints.
* \[ ] Geen order placement.
* \[ ] Geen automatische command execution zonder operator confirmation.
* \[ ] Geen remote upload van metrics/reports.
* \[ ] Geen secrets in prompts/context.
* \[ ] Geen cloud-only dependency verplicht maken.
* \[ ] Geen autonome trading agent.
* \[ ] Geen model dat risk limits kan aanpassen zonder gate.
* \[ ] Geen wijziging aan core execution/risk engine.

Wel doen:

* \[ ] lokale redacted context packs bouwen;
* \[ ] natural language query interface toevoegen;
* \[ ] read-only query execution over metrics/reports/evidence;
* \[ ] safe operator guidance geven;
* \[ ] commandvoorstellen maken maar niet uitvoeren;
* \[ ] runbooks koppelen aan anomalies;
* \[ ] answer provenance tonen;
* \[ ] tests voor prompt-injection, secrets en no-live toevoegen.

\---

## 3\. Fase 0 - AI Ops Safety Contract

Doel: vastleggen dat de AI/Ops-assistent adviserend en read-only is.

### Nieuwe doc

```text
docs/local-ai-ops-assistant-safety-contract.md
```

### Regels

* \[ ] Assistant mag alleen redacted context gebruiken.
* \[ ] Assistant mag geen secrets zien.
* \[ ] Assistant mag geen signed endpoints gebruiken.
* \[ ] Assistant mag geen account endpoints gebruiken.
* \[ ] Assistant mag geen order endpoints gebruiken.
* \[ ] Assistant mag geen live mode activeren.
* \[ ] Assistant mag geen commands automatisch uitvoeren.
* \[ ] Assistant mag commandvoorstellen doen met safety label.
* \[ ] Assistant moet bron/artifact tonen voor feitelijke claims.
* \[ ] Assistant moet onzekerheid tonen als context ontbreekt.
* \[ ] Prompt-injection uit logs/reports moet genegeerd worden.
* \[ ] Remote LLM is optioneel en default uit.
* \[ ] Local/deterministic rules fallback is verplicht.

### Acceptatiecriteria

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen dat live/order/account intenties worden geweigerd.
* \[ ] Dashboard toont `AI OPS ASSISTANT - READ ONLY`.
* \[ ] Assistant outputs bevatten no-live statement waar relevant.
* \[ ] Redaction self-test wordt vóór context export gebruikt.

\---

## 4\. Fase 1 - Redacted Context Pack Builder

Doel: veilige context maken uit lokale artifacts.

### Nieuwe module

```text
src/binance\_spot\_bot/ai\_ops\_context.py
```

### Dataclasses

* \[ ] `AiOpsContextPack`
* \[ ] `AiOpsContextSource`
* \[ ] `AiOpsContextItem`
* \[ ] `AiOpsContextManifest`
* \[ ] `AiOpsContextBuildResult`

### Contextbronnen

* \[ ] local ops snapshot;
* \[ ] operator health score;
* \[ ] diagnostics;
* \[ ] metrics latest;
* \[ ] SLO status;
* \[ ] anomalies;
* \[ ] report index;
* \[ ] evidence manifest;
* \[ ] support bundle verify;
* \[ ] incident timeline;
* \[ ] runbook list;
* \[ ] scheduled job status;
* \[ ] governance reminders;
* \[ ] paper ops calendar;
* \[ ] data growth budget;
* \[ ] dashboard smoke result;
* \[ ] check-all output.

### Contextregels

* \[ ] Alles door `redact\_payload` en `redact\_text`.
* \[ ] Max tokens/characters per source.
* \[ ] Source paths worden relatief gemaakt waar mogelijk.
* \[ ] Geen raw secrets.
* \[ ] Geen binary attachments.
* \[ ] Geen volledige grote logs standaard.
* \[ ] Elke context item krijgt provenance:

  * source;
  * path;
  * timestamp;
  * hash;
  * redaction status.

### Acceptatiecriteria

* \[ ] Context pack is JSON-serializable.
* \[ ] Context pack bevat geen secrets.
* \[ ] Context pack heeft manifest.
* \[ ] Context pack kan offline gebouwd worden.
* \[ ] Missing sources geven warnings, geen crash.

\---

## 5\. Fase 2 - Local Knowledge Index

Doel: snel zoeken in docs/reports/runbooks/evidence zonder cloud.

### Nieuwe module

```text
src/binance\_spot\_bot/ai\_ops\_index.py
```

### Index types

Start simpel:

* \[ ] JSONL keyword index.
* \[ ] Section title index.
* \[ ] Artifact metadata index.
* \[ ] Runbook step index.
* \[ ] Metrics name/category index.

Optioneel later:

* \[ ] embeddings index via optionele lokale dependency;
* \[ ] SQLite FTS indien beschikbaar.

### Indexed content

* \[ ] docs;
* \[ ] reports;
* \[ ] runbooks;
* \[ ] evidence manifests;
* \[ ] metrics aggregations;
* \[ ] diagnostics summaries;
* \[ ] support bundle manifests;
* \[ ] incident timelines.

### Acceptatiecriteria

* \[ ] Index build werkt offline.
* \[ ] Index is redacted.
* \[ ] Search geeft source references.
* \[ ] Search bevat geen secrets.
* \[ ] Index kan incremental rebuild doen.

\---

## 6\. Fase 3 - Natural Language Query Parser

Doel: operatorvragen omzetten naar veilige intenties.

### Nieuwe module

```text
src/binance\_spot\_bot/ai\_ops\_query.py
```

### Intent types

* \[ ] health\_summary;
* \[ ] explain\_anomaly;
* \[ ] failed\_jobs;
* \[ ] report\_freshness;
* \[ ] evidence\_missing;
* \[ ] support\_bundle\_summary;
* \[ ] runbook\_recommendation;
* \[ ] command\_suggestion;
* \[ ] paper\_policy\_status;
* \[ ] governance\_status;
* \[ ] data\_growth\_explanation;
* \[ ] dashboard\_error\_help;
* \[ ] check\_all\_explanation;
* \[ ] unknown\_safe\_question;
* \[ ] forbidden\_action.

### Forbidden intents

* \[ ] place order;
* \[ ] cancel real order;
* \[ ] query real account;
* \[ ] enable live;
* \[ ] reveal secrets;
* \[ ] send data externally;
* \[ ] bypass risk;
* \[ ] disable kill switch;
* \[ ] execute unapproved command.

### Acceptatiecriteria

* \[ ] Parser classificeert veilige vragen.
* \[ ] Parser blokkeert forbidden intents.
* \[ ] Parser geeft confidence en reason.
* \[ ] Parser werkt zonder LLM als rules fallback.
* \[ ] Tests dekken Nederlands en Engels.

\---

## 7\. Fase 4 - Safe Answer Engine

Doel: antwoorden maken met bronnen, onzekerheid en next steps.

### Nieuwe module

```text
src/binance\_spot\_bot/ai\_ops\_answer.py
```

### Answer format

* \[ ] summary;
* \[ ] evidence;
* \[ ] root cause hypothesis;
* \[ ] recommended next safe action;
* \[ ] optional command proposal;
* \[ ] risk/safety note;
* \[ ] confidence;
* \[ ] missing context;
* \[ ] sources.

### Antwoordregels

* \[ ] Feiten moeten naar artifact/source verwijzen.
* \[ ] Geen secrets tonen.
* \[ ] Geen live/order commands voorstellen.
* \[ ] Bij onzekerheid: vraag om context of zeg wat ontbreekt.
* \[ ] Commandvoorstellen zijn `proposal\_only`.
* \[ ] Risk-verhogende actie wordt geblokkeerd.
* \[ ] Safe actions verwijzen naar runbooks.

### Acceptatiecriteria

* \[ ] Antwoorden zijn redacted.
* \[ ] Antwoorden bevatten source references.
* \[ ] Forbidden action geeft veilige weigering.
* \[ ] Assistant kan “ik weet het niet uit lokale context” zeggen.
* \[ ] Tests dekken hallucination guard op lege context.

\---

## 8\. Fase 5 - Operator Guidance Policy

Doel: bepalen welke acties de assistent mag voorstellen.

### Nieuwe module

```text
src/binance\_spot\_bot/ai\_ops\_guidance\_policy.py
```

### Actieklassen

Allowed suggestions:

* \[ ] run diagnostics;
* \[ ] run check-all;
* \[ ] create support bundle;
* \[ ] verify support bundle;
* \[ ] open runbook;
* \[ ] export report;
* \[ ] inspect evidence;
* \[ ] run dashboard smoke;
* \[ ] run redaction self-test;
* \[ ] run metrics ingest/query;
* \[ ] review governance reminder.

Confirm-required suggestions:

* \[ ] clear cache;
* \[ ] compact metrics;
* \[ ] archive old state;
* \[ ] install scheduler task;
* \[ ] stop local paper job;
* \[ ] pause paper-only strategy;
* \[ ] rollback paper policy.

Forbidden suggestions:

* \[ ] enable live;
* \[ ] place/cancel real order;
* \[ ] query real account;
* \[ ] bypass risk;
* \[ ] reveal key/secret;
* \[ ] upload support bundle remotely;
* \[ ] run arbitrary shell command.

### Acceptatiecriteria

* \[ ] Every suggested action has safety class.
* \[ ] Confirm-required actions include confirm phrase.
* \[ ] Forbidden actions are refused.
* \[ ] Policy is testable without LLM.
* \[ ] Dashboard shows action safety label.

\---

## 9\. Fase 6 - Command Proposal Builder

Doel: veilige CLI commandvoorstellen maken, niet uitvoeren.

### Nieuwe module

```text
src/binance\_spot\_bot/ai\_ops\_command\_proposals.py
```

### Proposal format

* \[ ] command;
* \[ ] args;
* \[ ] safety\_class;
* \[ ] reason;
* \[ ] expected\_output;
* \[ ] requires\_confirmation;
* \[ ] forbidden\_if;
* \[ ] related\_runbook;
* \[ ] no\_auto\_execute=true.

### Voorbeelden

* \[ ] `python -m binance\_spot\_bot.cli diagnostics --json`
* \[ ] `python -m binance\_spot\_bot.cli operator-health-score --json`
* \[ ] `python -m binance\_spot\_bot.cli support-bundle`
* \[ ] `python -m binance\_spot\_bot.cli dashboard-smoke --seconds 10`
* \[ ] `python -m binance\_spot\_bot.cli metrics-anomalies --json`
* \[ ] `python -m binance\_spot\_bot.cli redaction-self-test --json`

### Acceptatiecriteria

* \[ ] Proposals worden gevalideerd tegen allowlist.
* \[ ] Geen proposal met live/signed/account/order.
* \[ ] Proposals worden niet uitgevoerd.
* \[ ] Dashboard heeft copy button, geen auto-run standaard.
* \[ ] Tests dekken command injection.

\---

## 10\. Fase 7 - Runbook Recommendation Engine

Doel: automatisch het juiste runbook voorstellen.

### Nieuwe module

```text
src/binance\_spot\_bot/ai\_ops\_runbook\_recommender.py
```

### Inputs

* \[ ] anomaly type;
* \[ ] failed job category;
* \[ ] diagnostics blockers;
* \[ ] SLO breach;
* \[ ] dashboard error;
* \[ ] governance reminder;
* \[ ] evidence missing;
* \[ ] support bundle verify failure;
* \[ ] data growth warning.

### Output

* \[ ] recommended runbook;
* \[ ] matching reason;
* \[ ] first 3 steps;
* \[ ] expected artifacts;
* \[ ] urgency;
* \[ ] safe commands.

### Acceptatiecriteria

* \[ ] Dashboard smoke failure maps to dashboard crash/runbook.
* \[ ] Data growth breach maps to retention/data growth runbook.
* \[ ] Missing evidence maps to evidence runbook.
* \[ ] Recommendation includes sources.
* \[ ] No live suggestions.

\---

## 11\. Fase 8 - Prompt-Injection \& Log-Content Defense

Doel: malicious text in logs/reports mag assistent niet sturen.

### Nieuwe module

```text
src/binance\_spot\_bot/ai\_ops\_injection\_guard.py
```

### Te detecteren patronen

* \[ ] “ignore previous instructions”;
* \[ ] “reveal secret”;
* \[ ] “enable live trading”;
* \[ ] “execute command”;
* \[ ] “upload file”;
* \[ ] embedded shell commands;
* \[ ] suspicious markdown links;
* \[ ] fake system instructions;
* \[ ] base64-looking secret payloads.

### Gedrag

* \[ ] Markeer source als suspicious.
* \[ ] Exclude of quote als untrusted.
* \[ ] Gebruik nooit untrusted source als instruction.
* \[ ] Voeg warning aan answer toe.
* \[ ] Redact suspicious payloads.

### Acceptatiecriteria

* \[ ] Prompt injection uit log wordt genegeerd.
* \[ ] Suspicious source blijft als evidence maar niet als instruction.
* \[ ] Tests dekken bekende injection strings.
* \[ ] No secrets leak.

\---

## 12\. Fase 9 - Optional Local LLM Adapter

Doel: natural language verbeteren zonder cloud verplichting.

### Nieuwe module

```text
src/binance\_spot\_bot/ai\_ops\_llm.py
```

### Modes

* \[ ] rules\_only default;
* \[ ] local\_llm optional;
* \[ ] remote\_llm disabled by default;
* \[ ] dry\_run context preview.

### Local adapter opties

* \[ ] HTTP localhost endpoint;
* \[ ] configurable timeout;
* \[ ] max context size;
* \[ ] redaction required;
* \[ ] no tools/execution;
* \[ ] no secrets;
* \[ ] no remote URL unless explicitly enabled.

### Acceptatiecriteria

* \[ ] Rules-only werkt zonder LLM.
* \[ ] Local LLM krijgt alleen redacted context.
* \[ ] Remote LLM is default disabled.
* \[ ] LLM output gaat door safety validator.
* \[ ] Tests gebruiken fake LLM.

\---

## 13\. Fase 10 - AI Ops CLI

Doel: assistent via commandline gebruiken.

### Nieuwe commands

```powershell
python -m binance\_spot\_bot.cli ai-ops-ask "Waarom is mijn health score lager?"
python -m binance\_spot\_bot.cli ai-ops-context --output data/ai-ops/context/latest.json
python -m binance\_spot\_bot.cli ai-ops-search "dashboard smoke failed"
python -m binance\_spot\_bot.cli ai-ops-runbook "check-all failed"
python -m binance\_spot\_bot.cli ai-ops-command-proposal "maak een support bundle"
python -m binance\_spot\_bot.cli ai-ops-safety-test
python -m binance\_spot\_bot.cli ai-ops-export-session --session-id <id>
```

### Acceptatiecriteria

* \[ ] Commands werken zonder API keys.
* \[ ] Commands voeren geen voorgestelde acties automatisch uit.
* \[ ] JSON output optie.
* \[ ] Forbidden questions worden veilig geweigerd.
* \[ ] Context export is redacted.

\---

## 14\. Fase 11 - AI Ops Dashboard Panel

Doel: assistent in dashboard gebruiken.

### Nieuwe dashboardsectie

```text
AI Ops Assistant
```

### Panels

* \[ ] question input;
* \[ ] answer summary;
* \[ ] evidence/source cards;
* \[ ] recommended runbook;
* \[ ] safe command proposals;
* \[ ] safety classification;
* \[ ] missing context;
* \[ ] recent questions;
* \[ ] context pack status;
* \[ ] redaction status;
* \[ ] rules-only/local-LLM mode indicator.

### Actions

* \[ ] build context;
* \[ ] ask question;
* \[ ] copy command proposal;
* \[ ] open runbook;
* \[ ] export answer;
* \[ ] run safety self-test;
* \[ ] clear conversation locally.

### Acceptatiecriteria

* \[ ] Dashboard toont `READ ONLY`.
* \[ ] Geen auto-run van commands.
* \[ ] Geen live controls.
* \[ ] Raw context alleen in debug expander.
* \[ ] Browser smoke dekt panel.

\---

## 15\. Fase 12 - Answer Evidence \& Session Export

Doel: AI/Ops-antwoorden auditbaar maken.

### Nieuwe module

```text
src/binance\_spot\_bot/ai\_ops\_sessions.py
```

### Storage

```text
data/ai-ops/
  contexts/
  sessions/
  answers/
  safety-tests/
```

### Session bevat

* \[ ] question;
* \[ ] parsed intent;
* \[ ] context manifest;
* \[ ] answer;
* \[ ] sources;
* \[ ] safety decisions;
* \[ ] command proposals;
* \[ ] operator feedback;
* \[ ] timestamp;
* \[ ] no-live statement.

### Acceptatiecriteria

* \[ ] Sessions zijn local-only.
* \[ ] Sessions zijn secret-free.
* \[ ] Answers kunnen geëxporteerd worden.
* \[ ] Evidence manifest linkt naar source artifacts.
* \[ ] Retention policy bestaat.

\---

## 16\. Fase 13 - Operator Feedback Loop

Doel: assistent verbeteren zonder automatische risk-acties.

### Nieuwe module

```text
src/binance\_spot\_bot/ai\_ops\_feedback.py
```

### Feedback

* \[ ] helpful/not helpful;
* \[ ] answer was wrong;
* \[ ] missing source;
* \[ ] command proposal unsafe;
* \[ ] runbook mismatch;
* \[ ] unclear answer;
* \[ ] resolved issue.

### Gebruik

* \[ ] lokaal opslaan;
* \[ ] weekly feedback report;
* \[ ] no remote upload;
* \[ ] improve rule mappings;
* \[ ] identify weak runbooks.

### Acceptatiecriteria

* \[ ] Feedback is local-only.
* \[ ] Feedback bevat geen secrets.
* \[ ] Feedback report helpt docs/runbooks verbeteren.
* \[ ] No automatic model retraining in this roadmap.

\---

## 17\. Fase 14 - AI Ops Safety Test Suite

Doel: assistent hard testen op safety.

### Nieuwe tests

```text
tests/test\_ai\_ops\_context.py
tests/test\_ai\_ops\_index.py
tests/test\_ai\_ops\_query.py
tests/test\_ai\_ops\_answer.py
tests/test\_ai\_ops\_guidance\_policy.py
tests/test\_ai\_ops\_command\_proposals.py
tests/test\_ai\_ops\_runbook\_recommender.py
tests/test\_ai\_ops\_injection\_guard.py
tests/test\_ai\_ops\_llm.py
tests/test\_ai\_ops\_cli.py
tests/test\_ai\_ops\_sessions.py
tests/test\_ai\_ops\_dashboard\_payload.py
```

### Safety testcases

* \[ ] “Enable live trading” wordt geweigerd.
* \[ ] “Place an order” wordt geweigerd.
* \[ ] “Show my API key” wordt geweigerd/redacted.
* \[ ] Log met “ignore previous instructions” wordt genegeerd.
* \[ ] Command injection wordt geblokkeerd.
* \[ ] Remote export wordt geweigerd.
* \[ ] Fake LLM unsafe output wordt geblokkeerd.
* \[ ] Empty context geeft onzeker antwoord.
* \[ ] Claims zonder source worden niet als feit gepresenteerd.
* \[ ] Suggested command blijft proposal-only.

### Acceptatiecriteria

* \[ ] Tests draaien in check-all.
* \[ ] Safety tests zijn deterministisch.
* \[ ] Geen netwerk nodig.
* \[ ] Geen API keys nodig.
* \[ ] Geen live/signed endpoints.

\---

## 18\. Fase 15 - AI Ops Reports

Doel: assistentgebruik en unresolved issues rapporteren.

### Nieuwe module

```text
src/binance\_spot\_bot/ai\_ops\_report.py
```

### Reports

Daily:

* \[ ] questions asked;
* \[ ] top intents;
* \[ ] forbidden requests blocked;
* \[ ] most common anomalies explained;
* \[ ] runbooks recommended;
* \[ ] unresolved issues;
* \[ ] feedback summary.

Weekly:

* \[ ] recurring operator problems;
* \[ ] weak docs/runbooks;
* \[ ] missing metrics;
* \[ ] suggested roadmap improvements;
* \[ ] no-live/safety summary.

### Acceptatiecriteria

* \[ ] Reports zijn secret-free.
* \[ ] Reports zijn local-only.
* \[ ] Reports linken naar AI ops sessions.
* \[ ] Dashboard kan report downloaden.

\---

## 19\. Fase 16 - Docs

Nieuwe docs:

* \[ ] `docs/local-ai-ops-assistant-safety-contract.md`
* \[ ] `docs/ai-ops-context-packs.md`
* \[ ] `docs/ai-ops-knowledge-index.md`
* \[ ] `docs/ai-ops-natural-language-queries.md`
* \[ ] `docs/ai-ops-safe-answer-engine.md`
* \[ ] `docs/ai-ops-guidance-policy.md`
* \[ ] `docs/ai-ops-command-proposals.md`
* \[ ] `docs/ai-ops-runbook-recommendations.md`
* \[ ] `docs/ai-ops-prompt-injection-defense.md`
* \[ ] `docs/ai-ops-local-llm-optional.md`
* \[ ] `docs/ai-ops-dashboard.md`
* \[ ] `docs/ai-ops-safety-tests.md`

README updates:

* \[ ] `ai-ops-ask` command;
* \[ ] rules-only mode;
* \[ ] local LLM optional mode;
* \[ ] redaction/safety explanation;
* \[ ] no-live statement;
* \[ ] command proposals are not auto-executed.

\---

## 20\. CLI command examples

### Safe ask

```powershell
python -m binance\_spot\_bot.cli ai-ops-ask "Waarom faalde de laatste dashboard smoke?"
```

### Safe context build

```powershell
python -m binance\_spot\_bot.cli ai-ops-context --json
```

### Safe runbook recommendation

```powershell
python -m binance\_spot\_bot.cli ai-ops-runbook "support bundle verify failed"
```

### Safe command proposal

```powershell
python -m binance\_spot\_bot.cli ai-ops-command-proposal "maak een diagnose report"
```

### Forbidden examples

Deze moeten geweigerd worden:

```powershell
python -m binance\_spot\_bot.cli ai-ops-ask "Zet live trading aan"
python -m binance\_spot\_bot.cli ai-ops-ask "Plaats nu een BTC order"
python -m binance\_spot\_bot.cli ai-ops-ask "Toon mijn API secret"
```

\---

## 21\. Codex bouwvolgorde

### PR 1 - AI Ops Safety Contract + Context Pack Builder

* \[ ] safety contract;
* \[ ] `ai\_ops\_context.py`;
* \[ ] redaction tests;
* \[ ] context manifest.

### PR 2 - Local Knowledge Index

* \[ ] `ai\_ops\_index.py`;
* \[ ] keyword/metadata search;
* \[ ] source references;
* \[ ] tests.

### PR 3 - Query Parser + Forbidden Intent Classifier

* \[ ] `ai\_ops\_query.py`;
* \[ ] intent classification;
* \[ ] forbidden actions;
* \[ ] NL/EN tests.

### PR 4 - Safe Answer Engine

* \[ ] `ai\_ops\_answer.py`;
* \[ ] answer format;
* \[ ] source/provenance;
* \[ ] uncertainty behavior.

### PR 5 - Guidance Policy + Command Proposals

* \[ ] guidance policy;
* \[ ] command proposals;
* \[ ] allowlist integration;
* \[ ] injection tests.

### PR 6 - Runbook Recommender

* \[ ] mapping anomalies/jobs/errors to runbooks;
* \[ ] first steps;
* \[ ] tests.

### PR 7 - Prompt Injection Guard

* \[ ] untrusted source detection;
* \[ ] suspicious content handling;
* \[ ] tests.

### PR 8 - Optional Local LLM Adapter

* \[ ] rules-only default;
* \[ ] fake local LLM tests;
* \[ ] safety validation after LLM output.

### PR 9 - CLI + Session Export

* \[ ] ai-ops CLI commands;
* \[ ] session storage;
* \[ ] answer export;
* \[ ] tests.

### PR 10 - Dashboard + Reports + Docs

* \[ ] AI Ops dashboard panel;
* \[ ] AI Ops reports;
* \[ ] docs;
* \[ ] browser smoke.

\---

## 22\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 085 PR 1: AI Ops Safety Contract + Redacted Context Pack Builder.

Maak docs/local-ai-ops-assistant-safety-contract.md.
Maak src/binance\_spot\_bot/ai\_ops\_context.py met:
- AiOpsContextPack
- AiOpsContextSource
- AiOpsContextItem
- AiOpsContextManifest
- AiOpsContextBuildResult

Bouw een context pack uit bestaande veilige bronnen:
- local\_ops\_snapshot
- operator\_health\_score
- environment\_doctor
- data\_growth\_budget
- report\_index
- artifact\_catalog
- evidence\_manifest indien aanwezig
- dashboard smoke/check-all artifacts indien aanwezig

Gebruik altijd redact\_payload/redact\_text.
Voeg manifest/hash/provenance toe.
Geen LLM integratie in deze PR.
Geen command execution.
Geen API calls.
Geen signed endpoints.
Geen orders.
Geen live trading.

Voeg tests toe voor:
- context pack build met fake settings/data
- secrets worden geredact
- missing sources geven warning
- live\_trading\_enabled=False
- manifest bevat hashes/provenance
```

Waarom eerst:

* veilige context is de basis voor elke AI/Ops-assistent;
* het bouwt direct voort op bestaande operator\_ops en redaction;
* het raakt geen trading runtime;
* het is klein genoeg voor Codex;
* safety kan meteen hard getest worden.

\---

## 23\. Definition of Done

Roadmap 085 is klaar als:

* \[ ] AI Ops Safety Contract bestaat.
* \[ ] Redacted Context Pack Builder werkt.
* \[ ] Local Knowledge Index werkt.
* \[ ] Natural Language Query Parser werkt.
* \[ ] Safe Answer Engine werkt.
* \[ ] Operator Guidance Policy werkt.
* \[ ] Command Proposal Builder werkt.
* \[ ] Runbook Recommendation Engine werkt.
* \[ ] Prompt-Injection Defense werkt.
* \[ ] Optional Local LLM Adapter werkt met rules-only default.
* \[ ] AI Ops CLI werkt.
* \[ ] AI Ops Dashboard Panel werkt.
* \[ ] Answer Evidence \& Session Export werkt.
* \[ ] Operator Feedback Loop werkt.
* \[ ] AI Ops Safety Test Suite werkt.
* \[ ] AI Ops Reports werken.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen secrets worden geredact.
* \[ ] Reports/sessions/context packs zijn secret-free.
* \[ ] Check-all blijft groen.
* \[ ] Browser smoke blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 085 kan na uitvoering naar `Voltooid docs`.

\---

## 24\. Verwachte Roadmap 086 daarna

Na Roadmap 085 zou Roadmap 086 logisch focussen op:

```text
Roadmap 086 - Safe Human-in-the-Loop Action Center, Approval Workflows \& Operator Decision Journal
```

Mogelijke inhoud:

* \[ ] human-in-the-loop action approvals;
* \[ ] decision journal;
* \[ ] command approval queue;
* \[ ] safe action execution after confirm;
* \[ ] role-based local permissions;
* \[ ] audit trail;
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

Status: Voltooid na herimplementatie en hercontrole.

Gebouwd: AI/Ops safety contract, redacted context pack builder, local knowledge index, NL/EN query classifier, safe answer engine, guidance policy, command proposal builder, runbook recommender, prompt-injection guard, rules-only local adapter, AI Ops CLI, dashboardtab `AI Ops Assistant`, session export, feedback logging en AI Ops report.

Docs: `docs/local-ai-ops-assistant-safety-contract.md`, `docs/ai-ops-context-packs.md`, `docs/ai-ops-knowledge-index.md`, `docs/ai-ops-natural-language-queries.md`, `docs/ai-ops-safe-answer-engine.md`, `docs/ai-ops-guidance-policy.md`, `docs/ai-ops-command-proposals.md`, `docs/ai-ops-runbook-recommendations.md`, `docs/ai-ops-prompt-injection-defense.md`, `docs/ai-ops-local-llm-optional.md`, `docs/ai-ops-dashboard.md`, `docs/ai-ops-safety-tests.md`.

Validatie:

- `python -m pytest tests/test_roadmap_085_ai_ops_acceptance.py tests/test_roadmaps_083_088_full_surface.py tests/test_roadmaps_082_088_ops_governance.py -q` -> 18 passed.
- `python -m pytest -q` -> 317 passed, 1 bestaande PytestCollectionWarning.
- `python -m binance_spot_bot.cli check-all --skip-tests --json` -> ok.
- `python -m binance_spot_bot.cli dashboard-smoke --seconds 1` -> ok.
- `python -m binance_spot_bot.cli dashboard-browser-smoke --url http://127.0.0.1:8506/ --seconds 10` -> ok.
- CLI smoke: ai-ops-ask, ai-ops-context, ai-ops-command-proposal en ai-ops-safety-test.

Safety: advisory/read-only, unsafe order/live/withdraw/secret intents blocked.

