# Roadmap 011 - Safe Dashboard Copilot, Strategy Templates \& Dataset Builder UI

Status: Concept / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-09  
Voorgestelde bestandsnaam:

```text
Roadmap docs/011-roadmap-safe-dashboard-copilot-strategy-templates-dataset-builder-ui.md
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

Doel: na Roadmap 009 en 010 is het dashboard bruikbaar en analyseerbaar. Roadmap 011 maakt het dashboard slimmer en sneller bruikbaar door een veilige dashboard-copilot, strategy templates, dataset builder UI, experiment assistant en plugin-structuur toe te voegen. De copilot mag uitleggen, samenvatten en voorstellen doen, maar mag nooit orders plaatsen of risk gates omzeilen.

Live trading blijft buiten scope.

\---

## 0\. Waarom deze Roadmap 011

Roadmap 009 maakt het dashboard/starten/demo trading beter.  
Roadmap 010 maakt strategy lab, signal debugging en replay sandbox beter.

Daarna zou ik toevoegen:

* \[ ] veilige dashboard-copilot;
* \[ ] strategy templates;
* \[ ] dataset builder UI;
* \[ ] experiment assistant;
* \[ ] report assistant;
* \[ ] plugin-architectuur;
* \[ ] guided research workflow;
* \[ ] betere onboarding voor beginners;
* \[ ] betere workflows voor modeltraining;
* \[ ] betere scanner/strategy configuratie zonder code te schrijven.

Belangrijk: dit is geen “AI mag traden”-roadmap. De AI/copilot is alleen read-only/advisory.

\---

## 1\. Huidige basis

Gecontroleerde huidige dashboardrichting:

* \[x] Streamlit dashboard bestaat.
* \[x] Dashboard heeft al tabs voor Overview, Credentials, Bot Controls, Risk Controls, Strategy \& Model, Market Data, Orders, Sessions, Evaluation en Logs/Security.
* \[x] Dashboard toont expliciet `LIVE TRADING DISABLED`.
* \[x] In `Strategy \& Model` bestaat al een kleine placeholder voor optional AI summaries.
* \[x] Runtime en dashboard gebruiken al session snapshots, fills, signals, metrics en model metadata.
* \[x] Public Binance Spot-data voor BTCUSDT is geschikt voor read-only analytics en demo/paper-onderzoek.

Belangrijkste gaten:

* \[ ] Geen echte veilige copilot in dashboard.
* \[ ] Geen strategy templates voor snelle experimenten.
* \[ ] Geen UI om datasets te bouwen zonder CLI.
* \[ ] Geen guided modeltraining workflow.
* \[ ] Geen automatische report-samenvatting.
* \[ ] Geen plugin-systeem voor dashboardpanelen.
* \[ ] Geen natural language uitleg van sessies, risk blocks en modelresultaten.
* \[ ] Geen beginner-friendly “wat moet ik nu doen?” workflow.

\---

## 2\. Scope

### In scope

* \[ ] Safe Dashboard Copilot.
* \[ ] Copilot permission system.
* \[ ] Read-only AI summaries.
* \[ ] Strategy template library.
* \[ ] Dataset Builder UI.
* \[ ] Guided experiment assistant.
* \[ ] Report summarizer.
* \[ ] Model training wizard.
* \[ ] Scanner configuration wizard.
* \[ ] Dashboard plugin architecture.
* \[ ] Prompt/report audit logs.
* \[ ] Redaction before AI calls.
* \[ ] Offline/local fallback summaries.

### Out of scope

* \[ ] AI orders laten plaatsen.
* \[ ] AI risk gates laten aanpassen zonder menselijke bevestiging.
* \[ ] Live trading.
* \[ ] Futures/margin/leverage.
* \[ ] Cloud deployment als verplicht onderdeel.
* \[ ] Winstgaranties.
* \[ ] Secrets naar AI sturen.

\---

## 3\. Fase 0 - Copilot safety contract

Doel: exact vastleggen wat de copilot wel en niet mag.

### Regels

* \[ ] Copilot is read-only.
* \[ ] Copilot mag geen orders plaatsen.
* \[ ] Copilot mag geen `ExecutionEngine.execute()` triggeren.
* \[ ] Copilot mag geen signed Binance endpoints aanroepen.
* \[ ] Copilot mag geen API keys zien.
* \[ ] Copilot mag geen live mode zichtbaar maken.
* \[ ] Copilot mag settings voorstellen, maar niet automatisch toepassen.
* \[ ] Copilot mag risk changes alleen als concept tonen.
* \[ ] Copilot output moet altijd gemarkeerd worden als advies/uitleg.
* \[ ] Copilot mag nooit financiële garanties geven.

### Nieuwe doc

```text
docs/copilot-safety-contract.md
```

### Acceptatiecriteria

* \[ ] Safety contract staat in docs.
* \[ ] Safety contract is zichtbaar in dashboard.
* \[ ] Tests bewijzen dat copilot geen orderpad kan raken.
* \[ ] Redaction wordt verplicht vóór elke AI-samenvatting.

\---

## 4\. Fase 1 - Copilot permission system

Doel: copilot hard beperken via permissies.

### Nieuwe module

```text
src/binance\_spot\_bot/copilot\_permissions.py
```

### Permissies

* \[ ] `read\_session\_summary`
* \[ ] `read\_market\_snapshot`
* \[ ] `read\_strategy\_lab\_report`
* \[ ] `read\_risk\_debug\_report`
* \[ ] `read\_model\_metadata`
* \[ ] `propose\_settings\_change`
* \[ ] `explain\_block\_reason`
* \[ ] `summarize\_report`

Verboden permissies:

* \[ ] `place\_order`
* \[ ] `cancel\_order`
* \[ ] `modify\_live\_settings`
* \[ ] `read\_api\_secret`
* \[ ] `enable\_live`
* \[ ] `bypass\_risk`
* \[ ] `send\_signed\_request`

### Acceptatiecriteria

* \[ ] Copilot API vereist expliciete permissie.
* \[ ] Verboden acties bestaan niet als callable tools.
* \[ ] Permission failure wordt gelogd.
* \[ ] Tests dekken alle verboden acties.

\---

## 5\. Fase 2 - Safe Dashboard Copilot panel

Doel: een dashboardpaneel dat uitlegt wat er gebeurt.

### Nieuwe tab/panel

```text
Copilot
```

### Copilot kan vragen beantwoorden over:

* \[ ] huidige sessie;
* \[ ] laatste trade;
* \[ ] laatste risk block;
* \[ ] market data status;
* \[ ] data quality;
* \[ ] model status;
* \[ ] strategy lab resultaat;
* \[ ] waarom bot HOLD doet;
* \[ ] waarom bot blokkeerde;
* \[ ] wat de volgende veilige stap is.

### Voorbeeldvragen

* \[ ] “Waarom heeft de bot niet gekocht?”
* \[ ] “Wat betekent deze risk block?”
* \[ ] “Welke sessie was beter en waarom?”
* \[ ] “Welke instellingen moet ik testen in paper mode?”
* \[ ] “Maak een samenvatting van deze sessie.”
* \[ ] “Welke data-quality waarschuwingen zijn belangrijk?”

### Acceptatiecriteria

* \[ ] Copilot werkt zonder API key via rule-based/local summary fallback.
* \[ ] Als AI API aanwezig is, worden payloads eerst geredact.
* \[ ] Copilot kan geen orders uitvoeren.
* \[ ] Copilot toont bronnen/data waarop antwoord gebaseerd is.
* \[ ] Copilot output is exporteerbaar.

\---

## 6\. Fase 3 - Redaction \& prompt audit

Doel: nooit secrets of gevoelige data naar AI sturen.

### Nieuwe module

```text
src/binance\_spot\_bot/copilot\_redaction.py
```

### Taken

* \[ ] Redact:

  * API keys;
  * API secrets;
  * signatures;
  * listenKeys;
  * account identifiers;
  * absolute local paths indien gewenst;
  * raw config secrets.
* \[ ] Prompt audit log:

  * prompt hash;
  * redacted payload hash;
  * model/provider;
  * timestamp;
  * response hash;
  * no raw secrets.
* \[ ] Dashboard toont:

  * “redaction active” badge;
  * “payload preview” zonder secrets.

### Acceptatiecriteria

* \[ ] Tests injecteren fake secrets en controleren redaction.
* \[ ] Geen secrets in prompt audit.
* \[ ] Gebruiker kan AI summaries uitzetten.
* \[ ] Copilot werkt ook zonder externe AI.

\---

## 7\. Fase 4 - Strategy Template Library

Doel: strategieën sneller en veiliger testen zonder code te schrijven.

### Nieuwe module

```text
src/binance\_spot\_bot/strategy\_templates.py
```

### Templates

* \[ ] No-trade baseline.
* \[ ] Buy-and-hold baseline.
* \[ ] Simple momentum.
* \[ ] Mean reversion.
* \[ ] Volatility filter.
* \[ ] Spread-aware entry.
* \[ ] Confidence-threshold strategy.
* \[ ] Risk-conservative template.
* \[ ] Demo-only aggressive template.
* \[ ] Custom template from YAML/JSON.

### Template metadata

* \[ ] name;
* \[ ] description;
* \[ ] allowed modes;
* \[ ] required features;
* \[ ] risk profile;
* \[ ] parameters;
* \[ ] warnings;
* \[ ] default safe settings.

### Acceptatiecriteria

* \[ ] Templates zijn demo/paper-first.
* \[ ] Geen template kan live activeren.
* \[ ] Template kan in Strategy Lab geladen worden.
* \[ ] Template kan als experiment opgeslagen worden.
* \[ ] Template changes vereisen menselijke Apply.

\---

## 8\. Fase 5 - Strategy Template UI

Doel: templates visueel kiezen, aanpassen en testen.

### UI

* \[ ] Template gallery.
* \[ ] Template details.
* \[ ] Parameter sliders.
* \[ ] Risk warning.
* \[ ] Run on demo data.
* \[ ] Run on selected session.
* \[ ] Compare to baseline.
* \[ ] Save as experiment.
* \[ ] Export config.

### Acceptatiecriteria

* \[ ] Gebruiker kan template testen zonder code.
* \[ ] Template result toont PnL/drawdown/trades/blocks/fees.
* \[ ] Overfit waarschuwing zichtbaar.
* \[ ] Template wordt niet automatisch runtime-strategy zonder bevestiging.

\---

## 9\. Fase 6 - Dataset Builder UI

Doel: dataset bouwen vanuit dashboard in plaats van alleen CLI/code.

### Nieuwe module

```text
src/binance\_spot\_bot/dataset\_builder\_ui.py
```

### UI stappen

1. \[ ] Kies symbol(s).
2. \[ ] Kies interval.
3. \[ ] Kies bron:

   * demo replay;
   * stored candles;
   * public spot REST cache.
4. \[ ] Kies time range.
5. \[ ] Kies feature set.
6. \[ ] Kies label horizon.
7. \[ ] Run data-quality check.
8. \[ ] Build dataset.
9. \[ ] Save manifest.
10. \[ ] Export dataset summary.

### Acceptatiecriteria

* \[ ] Dataset build werkt zonder API keys.
* \[ ] Data-quality warnings zijn zichtbaar.
* \[ ] Dataset manifest wordt opgeslagen.
* \[ ] Dataset hash is zichtbaar.
* \[ ] Dataset kan gebruikt worden in Model Training Wizard.

\---

## 10\. Fase 7 - Model Training Wizard

Doel: modeltraining starten zonder handmatig alle CLI-stappen te kennen.

### Wizard stappen

* \[ ] Kies dataset.
* \[ ] Kies model type:

  * rule baseline;
  * tiny neural;
  * sklearn baseline indien beschikbaar;
  * PyTorch indien beschikbaar.
* \[ ] Kies train/validation/test split.
* \[ ] Kies feature set.
* \[ ] Kies seed.
* \[ ] Start training.
* \[ ] Toon metrics.
* \[ ] Compare to baseline.
* \[ ] Save as candidate.
* \[ ] Promotion check.

### Acceptatiecriteria

* \[ ] Training wizard werkt op demo/small dataset.
* \[ ] Geen model wordt automatisch champion.
* \[ ] Slechte modellen krijgen waarschuwing.
* \[ ] Metrics worden opgeslagen.
* \[ ] Model card wordt gegenereerd indien Roadmap 007/010 modules bestaan.

\---

## 11\. Fase 8 - Scanner Configuration Wizard

Doel: multi-symbol scanner makkelijker instellen.

### UI stappen

* \[ ] Kies symbols.
* \[ ] Kies interval.
* \[ ] Kies template/model.
* \[ ] Kies filters:

  * min volume;
  * max spread;
  * min confidence;
  * data quality status.
* \[ ] Preview Binance public market info.
* \[ ] Run scanner.
* \[ ] Toon ranking.
* \[ ] Export watchlist.

### Acceptatiecriteria

* \[ ] Scanner config plaatst geen orders.
* \[ ] Scanner gebruikt public/demo data.
* \[ ] Rate-limit waarschuwing zichtbaar.
* \[ ] Watchlist kan worden opgeslagen.

\---

## 12\. Fase 9 - Report Assistant

Doel: rapporten automatisch samenvatten.

### Report types

* \[ ] Session report.
* \[ ] Strategy Lab report.
* \[ ] Parameter sweep report.
* \[ ] Risk debug timeline.
* \[ ] Model training report.
* \[ ] Scanner report.
* \[ ] Evidence/readiness report.

### Output

* \[ ] korte samenvatting;
* \[ ] belangrijkste issues;
* \[ ] belangrijkste metrics;
* \[ ] aanbevolen veilige volgende stappen;
* \[ ] blockers;
* \[ ] geen financieel advies disclaimer.

### Acceptatiecriteria

* \[ ] Report assistant werkt zonder secrets.
* \[ ] Report assistant kan rule-based fallback gebruiken.
* \[ ] AI output is duidelijk als samenvatting gemarkeerd.
* \[ ] Report assistant kan exporteren naar Markdown.

\---

## 13\. Fase 10 - Dashboard Plugin Architecture

Doel: dashboard uitbreidbaar maken zonder `streamlit\_app.py` steeds groter te maken.

### Nieuwe modules

```text
src/binance\_spot\_bot/ui/plugin\_api.py
src/binance\_spot\_bot/ui/plugins/
```

### Plugin interface

* \[ ] plugin name;
* \[ ] plugin tab name;
* \[ ] permissions;
* \[ ] render function;
* \[ ] required data;
* \[ ] safety level;
* \[ ] enabled/disabled.

### Core plugins

* \[ ] Overview plugin.
* \[ ] Demo Trading plugin.
* \[ ] Strategy Lab plugin.
* \[ ] Copilot plugin.
* \[ ] Dataset Builder plugin.
* \[ ] Model Training plugin.
* \[ ] Scanner plugin.
* \[ ] Sessions plugin.
* \[ ] Security plugin.

### Acceptatiecriteria

* \[ ] `streamlit\_app.py` wordt kleiner en modulairder.
* \[ ] Plugins kunnen geen verboden permissies krijgen.
* \[ ] Plugin registry is testbaar.
* \[ ] Plugin failure breekt heel dashboard niet.

\---

## 14\. Fase 11 - Beginner Mode / Expert Mode

Doel: dashboard minder overweldigend maken.

### Beginner Mode

* \[ ] Alleen:

  * Start local demo;
  * Demo Spot Trading;
  * Basic chart;
  * Basic fills;
  * Session summary;
  * Copilot help.
* \[ ] Geen geavanceerde risk/model controls standaard zichtbaar.

### Expert Mode

* \[ ] Alle tabs.
* \[ ] Strategy Lab.
* \[ ] Dataset Builder.
* \[ ] Model Training.
* \[ ] Scanner.
* \[ ] Debug panels.

### Acceptatiecriteria

* \[ ] Mode toggle reset runtime niet.
* \[ ] Beginner kan veilig starten.
* \[ ] Expert kan dieper analyseren.
* \[ ] Live blijft in beide modes disabled.

\---

## 15\. Fase 12 - Guided Research Workflow

Doel: gebruiker krijgt een duidelijke volgorde voor onderzoek.

### Workflow

1. \[ ] Start local demo.
2. \[ ] Run demo session.
3. \[ ] Open Strategy Lab.
4. \[ ] Inspect signals.
5. \[ ] Inspect risk blocks.
6. \[ ] Run replay sandbox.
7. \[ ] Try strategy template.
8. \[ ] Run parameter sweep.
9. \[ ] Build dataset.
10. \[ ] Train candidate model.
11. \[ ] Compare to baseline.
12. \[ ] Run paper session.
13. \[ ] Generate report.

### Acceptatiecriteria

* \[ ] Dashboard toont progress checklist.
* \[ ] Elke stap linkt naar juiste tab.
* \[ ] Copilot kan stap uitleggen.
* \[ ] Geen stap vereist live trading.

\---

## 16\. Fase 13 - AI-assisted docs generator

Doel: automatisch lokale docs/reports maken van experimenten.

### Output

* \[ ] `experiment\_notes.md`
* \[ ] `strategy\_template\_summary.md`
* \[ ] `dataset\_manifest\_summary.md`
* \[ ] `model\_training\_summary.md`
* \[ ] `scanner\_summary.md`
* \[ ] `next\_steps.md`

### Acceptatiecriteria

* \[ ] Docs zijn lokaal downloadbaar.
* \[ ] Docs bevatten geen secrets.
* \[ ] Docs linken naar artifacts.
* \[ ] Docs zeggen duidelijk dat paper/demo geen live garantie is.

\---

## 17\. Tests

### Unit tests

* \[ ] `tests/test\_copilot\_permissions.py`
* \[ ] `tests/test\_copilot\_redaction.py`
* \[ ] `tests/test\_copilot\_panel.py`
* \[ ] `tests/test\_strategy\_templates.py`
* \[ ] `tests/test\_dataset\_builder\_ui.py`
* \[ ] `tests/test\_model\_training\_wizard.py`
* \[ ] `tests/test\_scanner\_configuration\_wizard.py`
* \[ ] `tests/test\_report\_assistant.py`
* \[ ] `tests/test\_plugin\_api.py`
* \[ ] `tests/test\_beginner\_expert\_mode.py`

### Integration tests

* \[ ] Copilot summarizes session without secrets.
* \[ ] Strategy template runs on demo data.
* \[ ] Dataset builder creates manifest.
* \[ ] Model wizard registers candidate.
* \[ ] Scanner wizard exports watchlist.
* \[ ] Plugin failure isolation.
* \[ ] Beginner mode smoke test.
* \[ ] Expert mode smoke test.

### Safety tests

* \[ ] Copilot cannot call execution.
* \[ ] Copilot cannot see API secret.
* \[ ] Template cannot enable live.
* \[ ] Plugin cannot request forbidden permissions.
* \[ ] Report assistant redacts secrets.
* \[ ] Live remains hidden/disabled.

\---

## 18\. Nieuwe bestanden

### Source

* \[ ] `src/binance\_spot\_bot/copilot\_permissions.py`
* \[ ] `src/binance\_spot\_bot/copilot\_redaction.py`
* \[ ] `src/binance\_spot\_bot/copilot.py`
* \[ ] `src/binance\_spot\_bot/strategy\_templates.py`
* \[ ] `src/binance\_spot\_bot/dataset\_builder\_ui.py`
* \[ ] `src/binance\_spot\_bot/model\_training\_wizard.py`
* \[ ] `src/binance\_spot\_bot/scanner\_wizard.py`
* \[ ] `src/binance\_spot\_bot/report\_assistant.py`
* \[ ] `src/binance\_spot\_bot/ui/plugin\_api.py`
* \[ ] `src/binance\_spot\_bot/ui/plugins/`
* \[ ] `src/binance\_spot\_bot/ui/copilot\_panel.py`
* \[ ] `src/binance\_spot\_bot/ui/template\_gallery.py`
* \[ ] `src/binance\_spot\_bot/ui/dataset\_builder.py`
* \[ ] `src/binance\_spot\_bot/ui/model\_training.py`

### Docs

* \[ ] `docs/copilot-safety-contract.md`
* \[ ] `docs/dashboard-copilot.md`
* \[ ] `docs/strategy-templates.md`
* \[ ] `docs/dataset-builder-ui.md`
* \[ ] `docs/model-training-wizard.md`
* \[ ] `docs/scanner-wizard.md`
* \[ ] `docs/report-assistant.md`
* \[ ] `docs/dashboard-plugin-architecture.md`
* \[ ] `docs/beginner-expert-mode.md`
* \[ ] `docs/guided-research-workflow.md`

\---

## 19\. Prioriteiten

### Eerst

1. \[ ] Copilot safety contract.
2. \[ ] Copilot permissions.
3. \[ ] Redaction + prompt audit.
4. \[ ] Rule-based/local copilot summaries.
5. \[ ] Strategy template library.

### Daarna

6. \[ ] Strategy template UI.
7. \[ ] Dataset Builder UI.
8. \[ ] Model Training Wizard.
9. \[ ] Report Assistant.
10. \[ ] Scanner Configuration Wizard.

### Als laatste

11. \[ ] Plugin architecture.
12. \[ ] Beginner/Expert mode.
13. \[ ] Guided research workflow.
14. \[ ] AI-assisted docs generator.

\---

## 20\. Definition of Done

Roadmap 011 is klaar als:

* \[ ] Copilot bestaat en is read-only.
* \[ ] Copilot permissions blokkeren orderacties.
* \[ ] Redaction werkt voor prompts/reports.
* \[ ] Strategy templates kunnen veilig getest worden.
* \[ ] Dataset Builder UI maakt dataset manifests.
* \[ ] Model Training Wizard maakt candidate models.
* \[ ] Scanner Wizard maakt watchlists zonder orders.
* \[ ] Report Assistant vat reports samen zonder secrets.
* \[ ] Dashboard is modulairder via plugin API.
* \[ ] Beginner/Expert mode werkt.
* \[ ] Guided research workflow werkt.
* \[ ] Alle tests slagen.
* \[ ] Security scan is groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 011 kan na uitvoering naar `Voltooid docs`.

\---

## 21\. Verwachte Roadmap 012 daarna

Na Roadmap 011 zou ik Roadmap 012 richten op:

* \[ ] advanced multi-symbol scanner UX;
* \[ ] dashboard performance/profiling;
* \[ ] local notebook exports;
* \[ ] model explainability charts;
* \[ ] experiment database;
* \[ ] optional offline local LLM integration;
* \[ ] strategy template marketplace lokaal, zonder remote code execution.

