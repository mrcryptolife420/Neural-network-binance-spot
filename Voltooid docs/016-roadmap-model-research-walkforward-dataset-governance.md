# Roadmap 016: Model Research, Walk-forward Validation en Dataset Governance

## Status

Voltooid.

Validatie:

- `python -m unittest discover -s tests` groen: 85 tests.
- `python -m binance_spot_bot.cli check-all --json` groen.
- Security scan groen: geen secret artifacts gevonden.
- Live trading blijft disabled.

Geimplementeerd:

- Dataset manifest, feature schema hashing en checksum.
- Leakage guard voor chronologische splits, embargo, duplicates en gaps.
- Walk-forward evaluator met baseline-vs-candidate vergelijking en kosten.
- Model registry governance met candidate/champion/shadow rollen, model cards en promotiegates.
- Experiment DB records voor dataset manifests, walk-forward evals, model cards en promotiebeslissingen.
- Dashboard Model Lab met dataset, leakage, folds, model registry gates en raw report expander.
- CLI flow voor walk-forward evaluatie, demo modelregistratie en handmatige promotiebeslissing.
- Tests voor Roadmap 016 governance-flow.

Deze roadmap bouwt direct verder op roadmaps 001 t/m 015. De bot heeft nu een lokale Windows-startflow, Streamlit-dashboard, paper/testnet-ready runtime, alerts, rapportage, workspace-profielen, readiness checks, replay/sandbox tooling, experiment database, model registry en operationele hardening. De volgende beste stap is daarom niet nog meer losse dashboardbediening, maar een betrouwbare onderzoeks- en validatielaag voor het neural-network model.

Doel: maak modelontwikkeling reproduceerbaar, controleerbaar en lekvrij voordat signalen meer invloed krijgen op paper/shadow trading.

Live trading blijft buiten scope. Deze roadmap mag geen live-order route activeren.

## Belangrijkste conclusie

De grootste resterende technische zwakte is niet de lokale bediening van de bot, maar de vraag of een model op een correcte manier wordt getraind, getest, vergeleken en gepromoveerd.

Zonder dataset governance, leakage checks en walk-forward validatie kan een model er goed uitzien in een backtest terwijl het in werkelijkheid alleen profiteert van look-ahead bias, overfitting, verkeerde splits, ontbrekende kosten of onrealistische executie. Roadmap 016 moet daarom de ML-basis harder maken voordat er nieuwe autonomie, live-readiness of complexe strategiefeatures worden toegevoegd.

## Scope

In scope:

- Dataset manifests voor elke train/eval-run.
- Feature schema versiebeheer.
- Label horizon vastleggen en valideren.
- Chronologische train/validation/test splits.
- Look-ahead leakage guards.
- Walk-forward evaluator.
- Baseline-vs-model vergelijking.
- Fees, spread en slippage assumptions in elke evaluatie.
- Model registry promotiegates.
- Candidate/champion/shadow modelrollen.
- Model cards en evaluatierapporten.
- Experiment database uitbreiding.
- Dashboard Model Lab uitbreiding.
- Tests voor splits, leakage, registry gates en evaluatie-output.

Niet in scope:

- Live trading inschakelen.
- Automatisch model promoveren naar live.
- RL als MVP-strategie.
- LLM als autonome trader.
- Nieuwe exchange-integraties.
- Dupliceren van bestaande dashboard-, launcher-, credentials-, paper-, alert- of workspace-infrastructuur.

## Huidige basis waar we op voortbouwen

De roadmap moet hergebruik maken van bestaande infrastructuur:

- `dataset_model_wizard.py` voor dataset/model planning.
- `evaluation.py` voor time-series folds en baseline evaluatie.
- `model_registry.py` voor modelregistratie.
- `experiment_db.py` voor experimentindexering.
- `features.py` voor feature pipeline.
- `signal_model.py` voor neural-network signaalinterface.
- `backtest.py` voor historische simulatie.
- `paper.py`, `runtime.py`, `shadow.py` en `paper_accounting.py` voor paper/shadow runtime.
- `session_report.py`, `html_reports.py` en `evidence.py` voor rapportage.
- `ui/streamlit_app.py`, `ui/components.py` en `ui/wizard.py` voor dashboarduitbreiding.
- `check_all.py` en bestaande tests als regressiebasis.

Nieuwe code moet deze modules uitbreiden of eraan koppelen. Geen tweede model registry, geen tweede dashboard, geen tweede paper-accounting systeem.

## Architectuurkeuze

### DatasetManifest

Nieuwe of uitgebreide component voor reproduceerbare datasetbeschrijving.

Minimale velden:

- `dataset_id`
- `created_at`
- `source`
- `symbols`
- `interval`
- `raw_data_range`
- `feature_range`
- `label_range`
- `train_range`
- `validation_range`
- `test_range`
- `feature_set_version`
- `feature_schema_hash`
- `label_name`
- `label_horizon`
- `fee_bps`
- `slippage_bps`
- `spread_bps`
- `data_quality_summary`
- `row_count`
- `gap_count`
- `duplicate_count`
- `checksum`

Opslag:

- Per workspace onder een bestaande artifact/report/experiment locatie.
- JSON als machineleesbare bron.
- Markdown/HTML samenvatting via bestaande rapportagehelpers waar nuttig.

Acceptatie:

- Elke modeltraining en evaluatie verwijst naar exact één dataset manifest.
- Een model kan niet worden geregistreerd zonder `dataset_id`.
- Dashboard kan dataset manifest metadata tonen zonder secrets of ruwe API keys.

### FeatureSchema

Doel: vastleggen welke features een model verwacht en voorkomen dat model en runtime ongemerkt uit elkaar lopen.

Minimale velden:

- feature namen
- volgorde
- type
- normalisatieconfig
- lookback window
- feature generator versie
- schema hash

Acceptatie:

- Evaluatie faalt expliciet als runtime-features niet overeenkomen met het geregistreerde model.
- Schema hash staat in dataset manifest, model metadata en evaluatierapport.
- Tests bewijzen dat gewijzigde featurevolgorde of ontbrekende feature wordt geblokkeerd.

### LeakageGuard

Doel: voorkomen dat training of evaluatie toekomstige informatie gebruikt.

Checks:

- Chronologische ranges mogen niet overlappen.
- Validation start moet na train end liggen.
- Test start moet na validation end liggen.
- Label horizon mag geen toekomstige candle in feature window lekken.
- Gap tussen train/validation/test moet minimaal label horizon of configureerbare embargo zijn.
- Duplicates en ontbrekende timestamps worden gerapporteerd.
- Feature timestamps moeten kleiner of gelijk zijn aan decision timestamp.

Acceptatie:

- Foute splits geven een duidelijke foutmelding.
- Tests dekken overlap, verkeerde volgorde, te kleine gap, duplicate timestamps en future feature timestamps.
- Dashboard toont leakage status als pass/fail met korte reden.

### WalkForwardEvaluator

Doel: realistischere validatie dan één vaste split.

Functionaliteit:

- Rolling of expanding windows.
- Configureerbare `train_size`, `validation_size`, `test_size`, `step_size` en `embargo`.
- Per fold metrics opslaan.
- Aggregate metrics berekenen.
- Baseline vergelijken met candidate model.
- Fees/slippage/spread meenemen.
- Max drawdown, turnover, exposure en trade count rapporteren.

Metrics:

- total return
- net return na kosten
- max drawdown
- win rate
- profit factor
- expectancy
- Sharpe-like ratio waar zinvol
- trade count
- average holding time
- turnover
- exposure time
- blocked trade count door risk engine
- confidence bucket performance

Acceptatie:

- Evaluatie zonder kosten mag niet als promotiebasis gelden.
- Minimaal één naive/rule baseline wordt altijd meegerapporteerd.
- Elke fold heeft eigen ranges en eigen metrics.
- Rapport toont of candidate beter, gelijk of slechter is dan baseline.

### ModelRegistry Governance

Doel: modellen niet alleen opslaan, maar gecontroleerd beheren.

Modelrollen:

- `candidate`: nieuw getraind of nieuw geëvalueerd model.
- `champion`: huidige beste paper/shadow modelversie.
- `shadow`: model dat passief naast de actieve paperstrategie meedraait.
- `archived`: oude of afgewezen versie.

Promotiegates:

- dataset manifest aanwezig.
- leakage guard pass.
- feature schema hash match.
- walk-forward report aanwezig.
- net performance na kosten boven baseline.
- max drawdown onder ingestelde limiet.
- minimum trade count gehaald.
- geen extreme turnover.
- model card aanwezig.
- handmatige operatorgoedkeuring vereist voor champion-promotie.

Acceptatie:

- Geen automatische promotie naar champion zonder expliciete lokale operatoractie.
- Rollback naar vorige champion is beschikbaar.
- Registry toont reden waarom promotie toegestaan of geblokkeerd is.
- Tests dekken pass/fail promotiegates.

### ModelCard

Doel: elk model begrijpelijk en auditbaar maken.

Minimale inhoud:

- model id
- model role
- dataset id
- feature schema hash
- training config
- validation/test ranges
- walk-forward summary
- baseline comparison
- known limitations
- intended use: paper/shadow only
- forbidden use: live trading zonder latere roadmap en handmatige gate
- creation timestamp
- operator notes

Acceptatie:

- Model card wordt automatisch aangemaakt bij kandidaatregistratie.
- Dashboard kan model card openen.
- Rapport bevat geen secrets, API keys of volledige `.env` inhoud.

### ExperimentDB Uitbreiding

Doel: alle onderzoekruns terugvindbaar maken.

Uitbreidingen:

- `dataset_manifest` recordtype.
- `walkforward_eval` recordtype.
- `model_card` recordtype.
- `promotion_decision` recordtype.
- metrics indexeerbaar maken per run.
- filteren op symbol, interval, model role, dataset id en status.

Acceptatie:

- Nieuwe evaluatie verschijnt in experimentoverzicht.
- Rapporten zijn via artifact path terug te vinden.
- Bestaande session indexing blijft werken.

### Dashboard Model Lab

Doel: operator kan modelkwaliteit beoordelen zonder ruwe JSON te lezen.

UI-uitbreidingen:

- Dataset manifest overzicht.
- Leakage status panel.
- Walk-forward fold tabel.
- Candidate vs baseline comparison.
- Confidence bucket chart.
- Drawdown chart.
- Model registry rollen en promotiestatus.
- Model card viewer.
- Shadow-only toggle voor candidate model.
- Promotieknop alleen zichtbaar/actief wanneer gates pass zijn.

Belangrijk:

- UI mag geen trading keys tonen.
- UI mag geen live trading activeren.
- UI moet duidelijk tonen: `paper`, `testnet/demo`, `shadow`, of `offline evaluation`.

Acceptatie:

- Operator ziet welke dataset en welk model actief zijn.
- Operator ziet waarom een model niet gepromoveerd mag worden.
- Candidate kan shadow-only gekoppeld worden zonder paper execution te veranderen.

## Gefaseerde implementatie

### Fase 1: Dataset manifest en schema hashing

Taken:

- Ontwerp `DatasetManifest` dataclass of module.
- Voeg JSON serialisatie/deserialisatie toe.
- Voeg feature schema hash helper toe.
- Koppel manifest aan dataset/model wizard.
- Sla manifest op als artifact.
- Voeg tests toe voor verplichte velden, checksum en schema hash stabiliteit.

Acceptatiecriteria:

- Dataset wizard kan een manifest aanmaken.
- Manifest bevat symbol, interval, ranges, feature schema hash en label horizon.
- Manifest kan opnieuw worden geladen met dezelfde checksum.
- `check-all` blijft groen.

### Fase 2: LeakageGuard

Taken:

- Bouw split-validatie voor train/validation/test.
- Voeg embargo/label horizon check toe.
- Voeg timestamp monotonicity, duplicates en gap reporting toe.
- Koppel guard aan dataset wizard en evaluation.
- Voeg dashboardstatus toe.

Acceptatiecriteria:

- Overlappende ranges worden geblokkeerd.
- Te kleine gap tussen train en validation wordt geblokkeerd.
- Future feature timestamps worden geblokkeerd.
- Dashboard toont pass/fail met reden.
- Tests dekken positieve en negatieve cases.

### Fase 3: Walk-forward evaluator

Taken:

- Breid `evaluation.py` uit met walk-forward configuratie.
- Ondersteun rolling en expanding windows.
- Voeg fold-level en aggregate reports toe.
- Neem fees, spread en slippage mee.
- Voeg baseline comparison toe.
- Exporteer report naar JSON en HTML/Markdown.

Acceptatiecriteria:

- Evaluator produceert minimaal drie folds op voldoende datasetlengte.
- Elke fold heeft train/validation/test ranges.
- Net metrics na kosten worden gerapporteerd.
- Baseline en candidate staan in hetzelfde rapport.
- Tests bewijzen dat fold windows chronologisch blijven.

### Fase 4: Model registry governance

Taken:

- Voeg modelrollen toe aan registry metadata.
- Voeg promotion gate evaluatie toe.
- Voeg rollback metadata toe.
- Vereis dataset manifest en model card voor kandidaatregistratie.
- Voeg tests toe voor blocked/allowed promotion.

Acceptatiecriteria:

- Candidate zonder manifest kan niet worden gepromoveerd.
- Candidate met failed leakage guard kan niet worden gepromoveerd.
- Candidate zonder kosten-gecorrigeerde baselineverbetering kan niet automatisch door.
- Champion-promotie vereist operatoractie.
- Vorige champion blijft terugvindbaar.

### Fase 5: Model cards en experiment indexing

Taken:

- Maak model card generator.
- Koppel model card aan registry entry.
- Breid `ExperimentDB` uit met dataset/eval/model-card records.
- Voeg artifact links toe aan dashboard.
- Voeg redaction checks toe voor rapportinhoud.

Acceptatiecriteria:

- Elke geregistreerde candidate heeft een model card.
- Experiment DB toont dataset, eval en model card artifacts.
- Rapporten bevatten geen secrets.
- Tests bewijzen dat artifact records herlaadbaar zijn.

### Fase 6: Dashboard Model Lab

Taken:

- Voeg Model Lab sectie toe of breid bestaande modelops UI uit.
- Toon dataset manifest overzicht.
- Toon leakage status.
- Toon fold metrics.
- Toon candidate vs baseline.
- Toon model role en promotiegates.
- Voeg shadow-only candidate selectie toe.

Acceptatiecriteria:

- Dashboard toont modelkwaliteit visueel en scanbaar.
- Operator kan zien waarom een model geblokkeerd is.
- Shadow-only selectie verandert geen live/paper orderroute zonder expliciete runtimeconfig.
- UI blijft bruikbaar op lokale Windows laptop.

### Fase 7: Shadow trial voor candidate modellen

Taken:

- Koppel candidate model aan bestaande `shadow.py` flow.
- Log shadow signalen naast actieve paper signalen.
- Vergelijk shadow intent met paper outcome.
- Voeg shadow report toe.
- Voeg dashboardweergave toe voor shadow delta.

Acceptatiecriteria:

- Candidate kan passief meedraaien zonder orders te plaatsen.
- Shadow signalen worden geaudit met model id en feature schema hash.
- Rapport toont verschil tussen champion/paper en candidate/shadow.
- Kill switch en risk engine blijven onaangetast.

### Fase 8: End-to-end test en documentatie

Taken:

- Breid `check_all.py` uit met nieuwe testcategorieën.
- Voeg docs toe voor model research workflow.
- Voeg voorbeeldconfig toe zonder secrets.
- Voeg troubleshooting toe voor failed leakage, failed gates en slechte folds.
- Voeg acceptatiechecklist toe voor afronden van Roadmap 016.

Acceptatiecriteria:

- `check-all` draait groen.
- Nieuwe workflow is lokaal uitvoerbaar zonder echte keys.
- Geen secretwaarden in docs, tests of artifacts.
- Roadmap kan pas naar `Voltooid docs/` na succesvolle implementatie en validatie.

## Testplan

Minimale testgroepen:

- Dataset manifest:
  - verplichte velden
  - JSON roundtrip
  - checksum stabiliteit
  - feature schema hash stabiliteit

- Leakage guard:
  - overlappende ranges failen
  - niet-chronologische ranges failen
  - onvoldoende embargo failt
  - duplicate timestamps worden gemeld
  - future feature timestamps failen

- Walk-forward evaluator:
  - fold ranges zijn chronologisch
  - gap/embargo wordt gerespecteerd
  - fees/slippage veranderen net metrics
  - baseline en candidate worden samen gerapporteerd
  - te korte datasets geven duidelijke fout

- Model registry:
  - candidate registratie met manifest
  - promotion gate pass/fail
  - rollback metadata
  - schema mismatch blokkeert gebruik

- Dashboard:
  - Model Lab rendert zonder crash
  - failed gates zichtbaar
  - geen secrets zichtbaar
  - shadow-only status duidelijk

- Integratie:
  - dataset wizard naar manifest
  - manifest naar evaluation
  - evaluation naar experiment DB
  - evaluation naar model card
  - model card naar dashboard
  - candidate naar shadow report

## Security en safety regels

- Geen API keys of secrets in repo.
- Geen secrets in model cards, experiment DB, logs of reports.
- `.env.example` blijft zonder echte waarden.
- Live trading blijft disabled.
- Withdrawal permissions blijven buiten scope en moeten disabled blijven.
- Modelpromotie mag risk engine niet omzeilen.
- LLM mag geen autonome tradingbeslissingen nemen.
- Dashboardacties moeten lokaal en expliciet blijven.

## Definition of Done

Roadmap 016 is volledig afgewerkt wanneer:

- Dataset manifests zijn geïmplementeerd en getest.
- Feature schema hashing is geïmplementeerd en getest.
- LeakageGuard blokkeert ongeldige datasets/splits.
- WalkForwardEvaluator produceert fold-level en aggregate reports.
- Fees/slippage/spread zitten in evaluatiemetrics.
- Candidate-vs-baseline vergelijking staat in rapporten.
- Model registry heeft rollen en promotiegates.
- Model cards worden aangemaakt en gelinkt.
- Experiment DB indexeert dataset/eval/model-card artifacts.
- Dashboard Model Lab toont dataset, leakage, walk-forward en promotiestatus.
- Candidate shadow trial werkt zonder orders te plaatsen.
- `check-all` is groen.
- Er zijn geen secrets toegevoegd.
- De roadmap is pas daarna verplaatst naar `Voltooid docs/`.

## Aanbevolen eerste implementatiestap

Start met Fase 1 en Fase 2 samen:

1. `DatasetManifest` toevoegen.
2. Feature schema hash helper toevoegen.
3. `LeakageGuard` toevoegen.
4. Tests schrijven voor correcte en foutieve chronologische splits.

Deze basis voorkomt dat latere walk-forward en model registry functies op zwakke of onbetrouwbare data steunen.
