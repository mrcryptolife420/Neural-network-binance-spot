# Roadmap 077 - Data-Driven Strategy Confidence, Backtest Dataset Builder \& Indicator Calibration

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/077-roadmap-data-driven-strategy-confidence-backtest-dataset-builder-indicator-calibration.md
```

Volgt op:

* `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
* `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
* `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
* `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
* `Voltooid docs/005` t/m `Voltooid docs/075`
* `Roadmap docs/076-roadmap-binance-public-data-ingestion-indicator-warmup-feature-expansion.md`

Doel: Roadmap 076 geeft de demo bot meer echte Binance public data, indicator warmup, multi-timeframe indicators, liquidity features en data quality. Roadmap 077 gebruikt die data om de strategie-confidence, indicatorgewichten, symbol ranking en backtestresultaten evidence-based te maken. De bot moet niet alleen “meer data” hebben, maar ook kunnen bewijzen welke signalen, indicators en symbolen historisch beter/slechter werken in demo/paper omstandigheden.

Live trading blijft volledig buiten scope.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] `Voltooid docs/075-roadmap-simple-demo-multi-symbol-final-validation.md` bestaat.
* \[x] Roadmap 075 heeft status `Voltooid`.
* \[x] Roadmap 075 rondde roadmaps 066-074 af.
* \[x] Roadmap 075 valideerde multi-symbol dashboard helpers, dashboard markers, pytest, check-all, browser smoke en live disabled.
* \[x] Roadmap 076 is lokaal aangemaakt als public Binance data ingestion + indicator warmup roadmap.
* \[x] Geen bestaande Roadmap 077 gevonden via repo-search.

### Codebasecontrole

Gecontroleerde relevante modules:

* \[x] `src/binance\_spot\_bot/evaluation.py`
* \[x] `src/binance\_spot\_bot/backtest.py`
* \[x] `src/binance\_spot\_bot/dataset\_governance.py`
* \[x] `src/binance\_spot\_bot/features.py`
* \[x] `src/binance\_spot\_bot/indicators.py`
* \[x] `src/binance\_spot\_bot/data.py`

### Belangrijke bestaande basis

Er bestaat al:

* \[x] `BacktestEngine`;
* \[x] `BacktestResult`;
* \[x] `evaluate\_rule\_baseline`;
* \[x] `evaluate\_walk\_forward`;
* \[x] `WalkForwardConfig`;
* \[x] `DatasetManifest`;
* \[x] `leakage\_guard`;
* \[x] feature rows;
* \[x] label rows;
* \[x] chronological split;
* \[x] no-lookahead checks.

### Belangrijkste gat na Roadmap 076

Na Roadmap 076 heeft de bot meer echte data, maar dan moet nog bepaald worden:

* \[ ] welke indicators echt nuttig zijn;
* \[ ] welke confidence-drempel historisch beter werkt;
* \[ ] welke symbolen beter/slechter presteren;
* \[ ] welke market regimes riskanter zijn;
* \[ ] of de indicator advisor te vaak BUY/SELL/HOLD verkeerd inschat;
* \[ ] of paper/demotrading evidence overeenkomt met backtests;
* \[ ] of de strategy “paper-approved” mag worden voor langdurige demo runs.

\---

## 1\. Hoofddoel Roadmap 077

Maak de bot data-driven in plaats van alleen indicator-driven.

Roadmap 077 moet:

* \[ ] datasets bouwen uit Roadmap 076 public data cache;
* \[ ] indicator features valideren;
* \[ ] confidence score kalibreren;
* \[ ] backtests draaien per symbol/timeframe/regime;
* \[ ] walk-forward resultaten vergelijken;
* \[ ] indicatorprofielen objectief ranken;
* \[ ] symbol ranking historisch testen;
* \[ ] strategy presets evidence-based maken;
* \[ ] paper-only promotion gates toevoegen;
* \[ ] dashboardrapporten maken voor “waarom deze symbol/strategie?”;
* \[ ] live trading disabled houden.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe Binance data ingestion laag bouwen; dat hoort bij Roadmap 076.
* \[ ] Geen tweede BacktestEngine bouwen.
* \[ ] Geen tweede DatasetManifest bouwen.
* \[ ] Geen tweede dashboard bouwen.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen futures/margin/leverage.
* \[ ] Geen autonomous AI trading.
* \[ ] Geen model promotie zonder bewijs.

Wel doen:

* \[ ] bestaande `BacktestEngine` uitbreiden;
* \[ ] bestaande `evaluation.py` uitbreiden;
* \[ ] bestaande `dataset\_governance.py` gebruiken;
* \[ ] bestaande `features.py` uitbreiden met Roadmap 076 features;
* \[ ] bestaande indicator advisor calibreren;
* \[ ] bestaande dashboard research/evaluation panels uitbreiden;
* \[ ] alles paper/demo/read-only houden.

\---

## 3\. Fase 0 - Research safety \& promotion contract

Doel: vastleggen dat backtest/calibration geen live toestemming geeft.

### Taken

* \[ ] Maak `docs/research-to-paper-promotion-contract.md`.
* \[ ] Definieer levels:

  * `research\_only`;
  * `backtest\_candidate`;
  * `paper\_candidate`;
  * `paper\_approved`;
  * `testnet\_review\_candidate`;
  * nooit `live\_approved`.
* \[ ] Leg vast:

  * backtestresultaten zijn geen winstgarantie;
  * paper approval is alleen demo/paper;
  * model/indicator promotie vereist evidence;
  * live trading blijft disabled.
* \[ ] Voeg no-live assert toe in promotion module.
* \[ ] Voeg tests toe dat `live\_allowed=False`.

### Acceptatiecriteria

* \[ ] Contract bestaat in docs.
* \[ ] Promotion kan geen live activeren.
* \[ ] Dashboard toont “paper-only”.
* \[ ] Reports bevatten disclaimer.

\---

## 4\. Fase 1 - Backtest Dataset Builder

Doel: datasets bouwen uit Roadmap 076 public data cache.

### Nieuwe module

```text
src/binance\_spot\_bot/backtest\_dataset\_builder.py
```

### Input

* \[ ] public Binance candle cache;
* \[ ] indicator warmup data;
* \[ ] multi-timeframe candles;
* \[ ] liquidity features;
* \[ ] 24h/rolling ticker context;
* \[ ] public data quality score.

### Output

* \[ ] `BacktestDataset`;
* \[ ] feature rows;
* \[ ] label rows;
* \[ ] dataset manifest;
* \[ ] split manifest;
* \[ ] feature schema;
* \[ ] data quality summary.

### Dataset types

* \[ ] single-symbol single-timeframe;
* \[ ] single-symbol multi-timeframe;
* \[ ] multi-symbol scanner dataset;
* \[ ] regime-specific dataset;
* \[ ] liquidity-aware dataset.

### Acceptatiecriteria

* \[ ] Dataset builder werkt offline vanuit cache.
* \[ ] Dataset builder werkt zonder API keys.
* \[ ] Dataset manifest gebruikt bestaande `DatasetManifest`.
* \[ ] Leakage guard draait verplicht.
* \[ ] Geen secrets in dataset artifacts.

\---

## 5\. Fase 2 - Feature Schema V2

Doel: features uitbreiden met data uit Roadmap 076.

### Uitbreiding `features.py`

Nieuwe featuregroepen:

#### Price/return

* \[ ] ret\_1;
* \[ ] ret\_3;
* \[ ] ret\_5;
* \[ ] ret\_15;
* \[ ] rolling return;
* \[ ] distance to rolling high;
* \[ ] distance to rolling low.

#### Volatility

* \[ ] rolling volatility;
* \[ ] ATR percent;
* \[ ] Bollinger width;
* \[ ] volatility percentile;
* \[ ] candle range percent.

#### Trend

* \[ ] EMA spread percent;
* \[ ] EMA slope;
* \[ ] MACD histogram;
* \[ ] MACD slope;
* \[ ] multi-timeframe trend alignment.

#### Momentum

* \[ ] RSI;
* \[ ] RSI slope;
* \[ ] volume z-score;
* \[ ] breakout score;
* \[ ] rolling momentum.

#### Liquidity

* \[ ] spread bps;
* \[ ] top 5 depth liquidity;
* \[ ] top 20 depth liquidity;
* \[ ] order book imbalance;
* \[ ] estimated slippage 25 USDT;
* \[ ] liquidity score.

#### Market context

* \[ ] 24h change percent;
* \[ ] 24h quote volume;
* \[ ] 24h trade count;
* \[ ] 1h rolling change;
* \[ ] 4h rolling change;
* \[ ] market activity score.

#### Data quality

* \[ ] candle\_count\_score;
* \[ ] freshness\_score;
* \[ ] missing\_gap\_count;
* \[ ] stale\_data\_flag;
* \[ ] cache\_fallback\_flag.

### Acceptatiecriteria

* \[ ] Feature schema krijgt versie `features-v2-public-data`.
* \[ ] Schema hash verandert voorspelbaar.
* \[ ] Oude features blijven backward-compatible.
* \[ ] Tests dekken lege/missing liquidity data.
* \[ ] No-lookahead blijft groen.

\---

## 6\. Fase 3 - Label Builder V2

Doel: betere labels maken voor backtesting/calibration.

### Nieuwe labeltypes

* \[ ] future\_return\_up;
* \[ ] future\_return\_after\_fees;
* \[ ] future\_return\_after\_fees\_slippage;
* \[ ] max\_favorable\_excursion;
* \[ ] max\_adverse\_excursion;
* \[ ] hit\_take\_profit\_before\_stop;
* \[ ] regime\_next\_window;
* \[ ] volatility\_next\_window.

### Horizon opties

* \[ ] 3 bars;
* \[ ] 5 bars;
* \[ ] 10 bars;
* \[ ] 20 bars.

### Acceptatiecriteria

* \[ ] Labels gebruiken alleen toekomstige data binnen label horizon.
* \[ ] Features gebruiken geen toekomstige data.
* \[ ] Leakage guard detecteert foutieve overlap.
* \[ ] Label manifest bevat horizon en cost assumptions.

\---

## 7\. Fase 4 - BacktestEngine V2

Doel: bestaande backtest realistischer maken zonder nieuw systeem.

### Uitbreiden bestaande `BacktestEngine`

Nieuwe metrics:

* \[ ] win rate;
* \[ ] average win;
* \[ ] average loss;
* \[ ] profit factor;
* \[ ] Sharpe-like ratio;
* \[ ] max consecutive losses;
* \[ ] exposure time;
* \[ ] turnover;
* \[ ] fee total;
* \[ ] slippage total;
* \[ ] blocked reasons;
* \[ ] regime performance;
* \[ ] per-symbol performance.

Nieuwe simulatie-opties:

* \[ ] fees uit config;
* \[ ] slippage uit Roadmap 076 liquidity estimate;
* \[ ] spread-aware fill;
* \[ ] minimum notional;
* \[ ] step size rounding;
* \[ ] insufficient liquidity block;
* \[ ] confidence threshold sweep.

### Acceptatiecriteria

* \[ ] Bestaande tests blijven groen.
* \[ ] Backtest gebruikt realistic fee/slippage opties.
* \[ ] Geen signed endpoints.
* \[ ] Result bevat report-ready metrics.
* \[ ] Per-symbol backtest mogelijk.

\---

## 8\. Fase 5 - Walk-forward Evaluation V2

Doel: bestaande `evaluate\_walk\_forward` uitbreiden naar multi-symbol/multi-regime.

### Uitbreidingen

* \[ ] multi-symbol walk-forward;
* \[ ] multi-timeframe feature support;
* \[ ] regime-aware folds;
* \[ ] liquidity-aware costs;
* \[ ] candidate vs baseline vs no-trade;
* \[ ] buy-and-hold baseline;
* \[ ] shuffled-label sanity check;
* \[ ] random-entry baseline;
* \[ ] robustness summary.

### Reports

* \[ ] `walk\_forward\_v2\_report.json`;
* \[ ] `walk\_forward\_v2\_report.md`;
* \[ ] `fold\_metrics.csv`;
* \[ ] `baseline\_comparison.csv`;
* \[ ] `regime\_breakdown.csv`.

### Acceptatiecriteria

* \[ ] Candidate moet baseline verslaan op test folds, niet alleen train.
* \[ ] Shuffled-label check moet niet “goed” scoren.
* \[ ] Regime performance is zichtbaar.
* \[ ] Reports zijn secret-free.

\---

## 9\. Fase 6 - Indicator confidence calibration

Doel: confidence score objectief kalibreren.

### Nieuwe module

```text
src/binance\_spot\_bot/indicator\_calibration.py
```

### Taken

* \[ ] Verzamel historische indicator snapshots.
* \[ ] Koppel indicator bias/confidence aan toekomstige returns.
* \[ ] Maak calibration buckets:

  * 0.00-0.25;
  * 0.25-0.50;
  * 0.50-0.75;
  * 0.75-1.00.
* \[ ] Meet per bucket:

  * sample count;
  * average future return;
  * win rate;
  * drawdown;
  * false positive rate;
  * false sell rate.
* \[ ] Maak calibration curve.
* \[ ] Voeg confidence penalty toe bij slechte calibration.
* \[ ] Voeg minimum sample count toe.

### Acceptatiecriteria

* \[ ] Confidence 0.75+ moet historisch beter zijn dan 0.25-0.50, anders warning.
* \[ ] Te weinig samples geeft `insufficient\_calibration\_data`.
* \[ ] Calibration output is dashboard-ready.
* \[ ] Geen order execution.

\---

## 10\. Fase 7 - Indicator weight optimizer

Doel: indicator advisor minder handmatig maken.

### Nieuwe module

```text
src/binance\_spot\_bot/indicator\_weight\_optimizer.py
```

### Te optimaliseren weights

* \[ ] EMA trend;
* \[ ] MACD histogram;
* \[ ] RSI oversold/overbought;
* \[ ] Bollinger position;
* \[ ] ATR/volatility;
* \[ ] volume z-score;
* \[ ] liquidity score;
* \[ ] multi-timeframe agreement.

### Guardrails

* \[ ] Geen overfit op één symbol.
* \[ ] Walk-forward only.
* \[ ] Minimum sample count.
* \[ ] Maximum weight per indicator.
* \[ ] Stability penalty.
* \[ ] Complexity penalty.

### Output

* \[ ] `indicator\_weights.json`;
* \[ ] `indicator\_weight\_report.md`;
* \[ ] `weight\_stability.csv`.

### Acceptatiecriteria

* \[ ] Optimizer mag weights voorstellen, niet automatisch toepassen.
* \[ ] Dashboard toont old vs proposed weights.
* \[ ] Apply vereist expliciete paper-only confirm.
* \[ ] Evidence wordt opgeslagen.

\---

## 11\. Fase 8 - Strategy confidence model

Doel: indicator advisor omzetten naar betere strategy confidence.

### Nieuwe module

```text
src/binance\_spot\_bot/strategy\_confidence.py
```

### Inputs

* \[ ] indicator bias;
* \[ ] indicator confidence;
* \[ ] calibration score;
* \[ ] multi-timeframe agreement;
* \[ ] liquidity score;
* \[ ] data quality score;
* \[ ] regime score;
* \[ ] recent paper performance;
* \[ ] backtest robustness.

### Output

* \[ ] adjusted confidence;
* \[ ] raw confidence;
* \[ ] penalties;
* \[ ] boosts;
* \[ ] reason codes;
* \[ ] action recommendation:

  * observe;
  * paper eligible;
  * reduce size;
  * skip symbol;
  * needs more data.

### Acceptatiecriteria

* \[ ] Confidence wordt lager bij slechte data/liquidity/calibration.
* \[ ] Confidence wordt niet verhoogd zonder evidence.
* \[ ] Reason codes zijn dashboard-ready.
* \[ ] Tests dekken penalties/boosts.

\---

## 12\. Fase 9 - Symbol ranking validation

Doel: watchlist ranking historisch bewijzen.

### Nieuwe module

```text
src/binance\_spot\_bot/symbol\_ranking\_validation.py
```

### Ranking inputs

* \[ ] indicator confidence;
* \[ ] adjusted confidence;
* \[ ] liquidity score;
* \[ ] volume score;
* \[ ] volatility score;
* \[ ] data quality score;
* \[ ] backtest score;
* \[ ] recent paper score.

### Validatie

* \[ ] top ranked vs low ranked historical performance;
* \[ ] rank stability;
* \[ ] turnover in ranking;
* \[ ] regime-specific ranking;
* \[ ] symbol exclusion reasons.

### Acceptatiecriteria

* \[ ] Dashboard kan uitleggen waarom BTCUSDT boven ETHUSDT staat.
* \[ ] Ranking werkt niet alleen op confidence.
* \[ ] Low liquidity symbols worden gedowngraded.
* \[ ] Ranking report is exporteerbaar.

\---

## 13\. Fase 10 - Regime-aware strategy presets

Doel: strategy presets aanpassen aan marktregime.

### Presets

* \[ ] trend regime preset;
* \[ ] range regime preset;
* \[ ] high volatility preset;
* \[ ] low liquidity preset;
* \[ ] insufficient data preset;
* \[ ] uncertain/mixed regime preset.

### Per preset

* \[ ] allowed signals;
* \[ ] confidence threshold;
* \[ ] position size multiplier;
* \[ ] max trades;
* \[ ] cooldown;
* \[ ] skip conditions;
* \[ ] required evidence.

### Acceptatiecriteria

* \[ ] Preset wordt alleen paper/demo toegepast.
* \[ ] Low data quality forceert conservative/observe.
* \[ ] High volatility verlaagt size of blokkeert.
* \[ ] Dashboard toont waarom preset gekozen werd.

\---

## 14\. Fase 11 - Backtest Dataset Builder UI

Doel: gebruiker kan dataset/backtest maken vanuit dashboard.

### Dashboard panel

```text
Research / Backtest Builder
```

### Controls

* \[ ] symbols;
* \[ ] intervals;
* \[ ] date range/cache range;
* \[ ] feature set version;
* \[ ] label horizon;
* \[ ] fee/slippage assumptions;
* \[ ] train/validation/test split;
* \[ ] walk-forward folds;
* \[ ] regime filters;
* \[ ] run backtest;
* \[ ] export dataset manifest.

### Output

* \[ ] row count;
* \[ ] candle count;
* \[ ] data quality;
* \[ ] leakage guard status;
* \[ ] baseline metrics;
* \[ ] candidate metrics;
* \[ ] calibration status;
* \[ ] next action.

### Acceptatiecriteria

* \[ ] UI werkt offline op cache.
* \[ ] Geen Binance keys nodig.
* \[ ] Geen live order button.
* \[ ] Export evidence werkt.

\---

## 15\. Fase 12 - Paper-only promotion gates

Doel: strategieën pas naar paper-demo laten gaan als bewijs voldoende is.

### Nieuwe module

```text
src/binance\_spot\_bot/paper\_promotion.py
```

### Gate requirements

* \[ ] dataset manifest valid;
* \[ ] leakage guard pass;
* \[ ] data quality healthy/warning;
* \[ ] minimum rows;
* \[ ] baseline comparison pass;
* \[ ] walk-forward pass;
* \[ ] shuffled-label sanity pass;
* \[ ] calibration sample count pass;
* \[ ] max drawdown below threshold;
* \[ ] paper-only confirm.

### Statussen

* \[ ] blocked;
* \[ ] needs\_data;
* \[ ] research\_candidate;
* \[ ] backtest\_candidate;
* \[ ] paper\_candidate;
* \[ ] paper\_approved.

### Acceptatiecriteria

* \[ ] Geen live approval status.
* \[ ] Promotion status is evidence-based.
* \[ ] Dashboard toont blockers.
* \[ ] Strategy kan teruggezet worden bij slechte paper performance.

\---

## 16\. Fase 13 - Research-to-paper evidence bundle

Doel: alles wat tot een paper decision leidt exporteerbaar maken.

### Bundle bevat

* \[ ] dataset manifest;
* \[ ] feature schema;
* \[ ] leakage report;
* \[ ] calibration report;
* \[ ] backtest report;
* \[ ] walk-forward report;
* \[ ] symbol ranking report;
* \[ ] paper promotion decision;
* \[ ] configs redacted;
* \[ ] hashes;
* \[ ] timestamp;
* \[ ] no-live proof.

### Acceptatiecriteria

* \[ ] Bundle is secret-free.
* \[ ] Bundle is reproduceerbaar.
* \[ ] Evidence kan later vergeleken worden.
* \[ ] Support bundle kan research evidence linken.

\---

## 17\. Fase 14 - Dashboard explainability

Doel: gebruiker begrijpt waarom de bot een confidence of ranking geeft.

### Toevoegen aan dashboard

* \[ ] confidence breakdown;
* \[ ] raw vs adjusted confidence;
* \[ ] penalties/boosts;
* \[ ] calibration status;
* \[ ] backtest score;
* \[ ] data quality score;
* \[ ] liquidity score;
* \[ ] regime preset;
* \[ ] reason codes;
* \[ ] next recommended step.

### Voorbeelden reason codes

* \[ ] `low\_data\_quality\_penalty`;
* \[ ] `liquidity\_penalty`;
* \[ ] `timeframe\_disagreement`;
* \[ ] `calibration\_insufficient\_samples`;
* \[ ] `walk\_forward\_failed`;
* \[ ] `baseline\_not\_beaten`;
* \[ ] `paper\_eligible`;
* \[ ] `observe\_only`.

### Acceptatiecriteria

* \[ ] Geen black box confidence.
* \[ ] Dashboard toont waarom confidence verandert.
* \[ ] Export bevat reason codes.
* \[ ] No-live badge blijft zichtbaar.

\---

## 18\. Fase 15 - Tests

### Unit tests

* \[ ] `tests/test\_backtest\_dataset\_builder.py`
* \[ ] `tests/test\_feature\_schema\_v2.py`
* \[ ] `tests/test\_label\_builder\_v2.py`
* \[ ] `tests/test\_backtest\_engine\_v2.py`
* \[ ] `tests/test\_walk\_forward\_v2.py`
* \[ ] `tests/test\_indicator\_calibration.py`
* \[ ] `tests/test\_indicator\_weight\_optimizer.py`
* \[ ] `tests/test\_strategy\_confidence.py`
* \[ ] `tests/test\_symbol\_ranking\_validation.py`
* \[ ] `tests/test\_regime\_strategy\_presets.py`
* \[ ] `tests/test\_paper\_promotion.py`
* \[ ] `tests/test\_research\_to\_paper\_bundle.py`

### Integration tests

* \[ ] Build dataset from public data cache.
* \[ ] Run leakage guard.
* \[ ] Run walk-forward backtest.
* \[ ] Run confidence calibration.
* \[ ] Generate adjusted confidence.
* \[ ] Validate symbol ranking.
* \[ ] Generate paper promotion decision.
* \[ ] Export research-to-paper evidence bundle.

### Safety tests

* \[ ] Geen live status.
* \[ ] Geen signed endpoints.
* \[ ] Geen order execution in backtest/calibration.
* \[ ] Promotion kan geen live activeren.
* \[ ] Reports/evidence bevatten geen secrets.
* \[ ] Check-all blijft groen.

\---

## 19\. CLI commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli build-backtest-dataset --symbols BTCUSDT,ETHUSDT --interval 1m --source public-cache
python -m binance\_spot\_bot.cli calibrate-indicators --dataset-id <id>
python -m binance\_spot\_bot.cli optimize-indicator-weights --dataset-id <id>
python -m binance\_spot\_bot.cli validate-symbol-ranking --dataset-id <id>
python -m binance\_spot\_bot.cli paper-promotion-check --strategy-id <id>
python -m binance\_spot\_bot.cli export-research-evidence --strategy-id <id>
```

Acceptatie:

* \[ ] Alle commands werken zonder API keys.
* \[ ] Alle commands kunnen JSON output geven.
* \[ ] Geen command plaatst orders.
* \[ ] Geen command activeert live.

\---

## 20\. Codex bouwvolgorde

### PR 1 - Backtest Dataset Builder

* \[ ] `backtest\_dataset\_builder.py`
* \[ ] cache input;
* \[ ] manifest output;
* \[ ] tests.

### PR 2 - Feature Schema V2

* \[ ] nieuwe features;
* \[ ] schema hash;
* \[ ] no-lookahead tests.

### PR 3 - Label Builder V2

* \[ ] nieuwe labels;
* \[ ] horizon/cost-aware labels;
* \[ ] leakage tests.

### PR 4 - BacktestEngine V2 metrics

* \[ ] win rate;
* \[ ] profit factor;
* \[ ] drawdown;
* \[ ] fees/slippage;
* \[ ] per-symbol results.

### PR 5 - Walk-forward V2

* \[ ] multi-symbol;
* \[ ] baselines;
* \[ ] shuffled-label sanity;
* \[ ] reports.

### PR 6 - Indicator Calibration

* \[ ] buckets;
* \[ ] curves;
* \[ ] sample count checks;
* \[ ] dashboard payload.

### PR 7 - Indicator Weight Optimizer

* \[ ] propose weights;
* \[ ] guardrails;
* \[ ] evidence.

### PR 8 - Strategy Confidence

* \[ ] adjusted confidence;
* \[ ] penalties/boosts;
* \[ ] reason codes.

### PR 9 - Symbol Ranking Validation

* \[ ] ranking report;
* \[ ] dashboard explanation;
* \[ ] tests.

### PR 10 - Paper Promotion + Evidence

* \[ ] promotion gates;
* \[ ] evidence bundle;
* \[ ] dashboard panel;
* \[ ] docs.

\---

## 21\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 077 PR 1: Backtest Dataset Builder.

Maak src/binance\_spot\_bot/backtest\_dataset\_builder.py.
Gebruik bestaande DataStore, DatasetManifest, build\_feature\_rows, build\_label\_rows en leakage\_guard.
Bouw een dataset vanuit de Roadmap 076 public Binance data cache.
Ondersteun symbols, interval, feature\_set\_version, label\_horizon en train/validation/test split.
Schrijf dataset manifest en leakage report.
Voeg tests toe met fake cached BTCUSDT/ETHUSDT candles.
Geen Binance API calls, geen signed endpoints, geen orders, geen live trading.
```

Waarom eerst:

* Dataset builder is de basis voor calibration.
* Zonder dataset geen betrouwbare backtest.
* Zonder backtest geen paper-promotion.
* De bestaande code heeft al manifests, leakage guard, features en evaluation, dus deze PR bouwt voort in plaats van dubbel te bouwen.

\---

## 22\. Definition of Done

Roadmap 077 is klaar als:

* \[ ] Backtest dataset builder werkt op public data cache.
* \[ ] Feature Schema V2 bestaat.
* \[ ] Label Builder V2 bestaat.
* \[ ] BacktestEngine V2 geeft uitgebreide metrics.
* \[ ] Walk-forward V2 werkt multi-symbol.
* \[ ] Indicator confidence calibration werkt.
* \[ ] Indicator weight optimizer stelt paper-only weights voor.
* \[ ] Strategy confidence gebruikt data quality, liquidity, calibration en regime.
* \[ ] Symbol ranking validation werkt.
* \[ ] Regime-aware strategy presets werken.
* \[ ] Dashboard Research/Backtest Builder werkt.
* \[ ] Paper-only promotion gates werken.
* \[ ] Research-to-paper evidence bundle werkt.
* \[ ] Tests bewijzen geen signed endpoints/live/order execution.
* \[ ] Reports bevatten geen secrets.
* \[ ] Check-all blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 077 kan na uitvoering naar `Voltooid docs`.

\---

## 23\. Verwachte Roadmap 078 daarna

Na Roadmap 077 zou Roadmap 078 logisch focussen op:

```text
Roadmap 078 - Paper Strategy Deployment, Continuous Evaluation \& Auto-Rollback
```

Mogelijke inhoud:

* \[ ] paper-approved strategy deployment;
* \[ ] continuous paper evaluation;
* \[ ] drift detection;
* \[ ] auto rollback naar conservative preset;
* \[ ] daily strategy report;
* \[ ] paper performance watchdog;
* \[ ] evidence-based demotion;
* \[ ] nog steeds geen live trading.

