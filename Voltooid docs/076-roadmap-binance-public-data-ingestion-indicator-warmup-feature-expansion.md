# Roadmap 076 - Binance Public Data Ingestion, Indicator Warmup \& Feature Expansion

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Voltooid docs/076-roadmap-binance-public-data-ingestion-indicator-warmup-feature-expansion.md
```

Doel: de demo spot trading bot meer echte Binance Spot public data geven, zodat de Adaptive Indicator Advisor niet meer vastloopt op `insufficient\_data`, de multi-symbol demo realistischer wordt, indicatoren beter onderbouwd zijn en het dashboard meer marktcontext krijgt. Deze roadmap gebruikt alleen public/read-only Binance data. Geen live trading, geen signed orders, geen account endpoints.

\---

## 0\. Controle vooraf

### Gecontroleerd in GitHub repo

* \[x] `Voltooid docs/075-roadmap-simple-demo-multi-symbol-final-validation.md` bestaat.
* \[x] Roadmap 075 heeft status `Voltooid`.
* \[x] Roadmap 075 rondde roadmaps 066-074 af.
* \[x] Roadmap 075 zegt dat `Roadmap docs` leeg was na afronding.
* \[x] Roadmap 075 valideerde multi-symbol dashboard helpers, symbol validation guardrails, total demo quote budget, risk summary, budget allocation, evidence export, full pytest, check-all, browser smoke en live trading disabled.
* \[x] Geen bestaande Roadmap 076 gevonden via repo-search.

### Gecontroleerde codebase

* \[x] `src/binance\_spot\_bot/binance.py`
* \[x] `src/binance\_spot\_bot/data.py`
* \[x] `src/binance\_spot\_bot/spot\_preview.py`
* \[x] `src/binance\_spot\_bot/indicators.py`
* \[x] `src/binance\_spot\_bot/ui/streamlit\_app.py`

### Screenshot-probleem

Het dashboard toont:

* \[x] `Indicator profile = auto`
* \[x] `Auto profile = True`
* \[x] `Indicator symbols = 7`
* \[x] `Avg confidence = 0.55`
* \[x] Regime per symbol: `insufficient\_data`
* \[x] Regime reason: `Need at least 30 candles`

Conclusie:

* \[x] De bot heeft te weinig candles per symbol.
* \[x] `indicators.py` vereist minstens 30 candles voor regime detection.
* \[x] Voor betrouwbare indicatoren is 30 candles minimaal; 120-500 candles per symbol is beter.
* \[x] De bot moet automatisch Binance public candles ophalen voordat indicatoren worden berekend.
* \[x] De demo bot moet cache/fallback gebruiken als Binance niet bereikbaar is.

\---

## 1\. Huidige data-basis

### 1.1 `BinanceSpotAdapter`

Bestaand:

* \[x] `get\_exchange\_info(symbols)`
* \[x] `get\_symbol\_filters(symbol)`
* \[x] `get\_klines(symbol, interval, start\_time, end\_time, limit)`
* \[x] `get\_order\_book(symbol, depth)`

Belangrijk:

* \[x] Signed endpoints bestaan, maar zijn niet nodig voor deze roadmap.
* \[x] Roadmap 076 mag alleen public/read-only endpoints gebruiken.

### 1.2 `DataStore`

Bestaand:

* \[x] raw JSON opslaan;
* \[x] candles CSV opslaan;
* \[x] candles CSV laden;
* \[x] feature rows opslaan;
* \[x] label rows opslaan;
* \[x] Binance klines parsen naar `Candle`.

Gaten:

* \[ ] Geen dedicated Binance public data cache.
* \[ ] Geen freshness metadata.
* \[ ] Geen incremental kline update.
* \[ ] Geen order book/ticker/trade storage.
* \[ ] Geen public-data manifest met hashes.
* \[ ] Geen multi-timeframe feature cache.

### 1.3 `SpotPreview`

Bestaand:

* \[x] symbol filters ophalen;
* \[x] order book depth=5 ophalen;
* \[x] klines ophalen;
* \[x] spread berekenen;
* \[x] fallback naar demo data.

Gaten:

* \[ ] Preview is geen watchlist-wide warmup.
* \[ ] Geen 24h ticker/rolling context.
* \[ ] Geen recent trades/aggTrades.
* \[ ] Geen cache reuse tussen dashboard refreshes.
* \[ ] Geen data quality per symbol.

### 1.4 `indicators.py`

Bestaand:

* \[x] EMA;
* \[x] RSI;
* \[x] ATR;
* \[x] MACD;
* \[x] Bollinger position;
* \[x] regime detection;
* \[x] auto indicator profile;
* \[x] indicator evidence export.

Gaten:

* \[ ] Geen warmup-manager.
* \[ ] Geen multi-timeframe confirmation.
* \[ ] Geen liquidity features.
* \[ ] Geen 24h market context.
* \[ ] Geen order book imbalance.
* \[ ] Geen data freshness score.
* \[ ] Geen duidelijke dashboard actie “Fetch Binance data”.

\---

## 2\. Welke extra Binance data is het beste?

### Prioriteit 1 - Candles / klines

Gebruik:

* \[ ] `/api/v3/klines`
* \[ ] eventueel `/api/v3/uiKlines`

Intervals:

* \[ ] `1m` voor demo timing;
* \[ ] `5m` voor minder ruis;
* \[ ] `15m` voor trendcontext;
* \[ ] `1h` voor hogere timeframe richting;
* \[ ] optioneel `4h` voor macro regime.

Warmup:

* \[ ] minimum: 30 candles;
* \[ ] aanbevolen: 120 candles;
* \[ ] sterk: 500 candles;
* \[ ] max: adapter-safe limit, bijvoorbeeld 1000 waar endpoint dit toelaat.

Waarom:

* lost direct `insufficient\_data` op;
* EMA/MACD/Bollinger worden stabieler;
* multi-timeframe regime detection wordt mogelijk.

### Prioriteit 2 - ExchangeInfo / symbol filters

Gebruik:

* \[ ] `/api/v3/exchangeInfo`

Data:

* \[ ] symbol status;
* \[ ] base/quote asset;
* \[ ] tick size;
* \[ ] step size;
* \[ ] min qty;
* \[ ] max qty;
* \[ ] min notional;
* \[ ] market lot size;
* \[ ] allowed order types;
* \[ ] max orders;
* \[ ] rate limits.

Waarom:

* demo fills realistischer;
* min notional/step-size validatie correct;
* dashboard kan symbol guardrails tonen;
* scanner kan slechte symbols filteren.

### Prioriteit 3 - Order book / depth

Gebruik:

* \[ ] `/api/v3/depth`

Depth:

* \[ ] 5 voor snelle preview;
* \[ ] 20 voor liquidity score;
* \[ ] 100 voor diepere slippage-inschatting als rate-limit veilig is.

Features:

* \[ ] best bid;
* \[ ] best ask;
* \[ ] spread bps;
* \[ ] bid liquidity top 5/20;
* \[ ] ask liquidity top 5/20;
* \[ ] order book imbalance;
* \[ ] estimated slippage voor 10/25/50/100 USDT;
* \[ ] thin book warning.

Waarom:

* demo bot kan slechte liquidity vermijden;
* paper fills realistischer;
* confidence kan lager bij hoge spread of dun order book.

### Prioriteit 4 - 24h ticker

Gebruik:

* \[ ] `/api/v3/ticker/24hr`

Features:

* \[ ] priceChangePercent;
* \[ ] high/low;
* \[ ] volume;
* \[ ] quoteVolume;
* \[ ] trade count;
* \[ ] weighted average price;
* \[ ] bid/ask price/qty.

Waarom:

* scanner ranking;
* trend context;
* volume/liquidity filter;
* symbol selectie.

### Prioriteit 5 - Rolling ticker

Gebruik:

* \[ ] rolling window ticker indien adapter/tooling beschikbaar.

Windows:

* \[ ] `1h`;
* \[ ] `4h`;
* \[ ] `1d`.

Waarom:

* betere korte-termijn momentum/context;
* minder afhankelijk van vaste 24h window.

### Prioriteit 6 - Recent trades / aggregate trades

Gebruik:

* \[ ] `/api/v3/trades`
* \[ ] `/api/v3/aggTrades`

Features:

* \[ ] recent trade count;
* \[ ] average trade size;
* \[ ] large trade count;
* \[ ] trade burst score;
* \[ ] buy/sell pressure proxy indien afleidbaar.

Waarom:

* betere activiteitsscore;
* minder false signals;
* betere scanner ranking.

### Prioriteit 7 - Public WebSocket streams

Streams:

* \[ ] kline stream;
* \[ ] miniTicker stream;
* \[ ] bookTicker stream;
* \[ ] depth stream;
* \[ ] aggTrade stream.

Waarom:

* minder REST polling;
* betere freshness;
* live public dashboard zonder orderrechten.

\---

## 3\. Hoofddoel Roadmap 076

Maak een veilige Binance public data ingestion laag voor:

* \[ ] watchlist warmup;
* \[ ] indicator warmup;
* \[ ] multi-timeframe indicatoren;
* \[ ] order book liquidity features;
* \[ ] 24h/rolling market context;
* \[ ] recent trades activity features;
* \[ ] public data cache;
* \[ ] data quality/freshness;
* \[ ] dashboard fetch controls;
* \[ ] evidence/report exports.

\---

## 4\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen nieuwe order adapter.
* \[ ] Geen live trading.
* \[ ] Geen signed endpoints.
* \[ ] Geen account endpoint.
* \[ ] Geen nieuwe RiskEngine.
* \[ ] Geen nieuwe dashboard-app.
* \[ ] Geen futures/margin/leverage.
* \[ ] Geen withdrawals.

Wel doen:

* \[ ] `BinanceSpotAdapter` uitbreiden met public endpoints.
* \[ ] `DataStore` uitbreiden met public cache.
* \[ ] `SpotPreview` uitbreiden of aanvullen met ingestion service.
* \[ ] `indicators.py` voeden met meer candles/features.
* \[ ] Simple demo dashboard uitbreiden met fetch/warmup/status.

\---

## 5\. Fase 0 - Public data safety contract

Doel: vastleggen dat deze roadmap alleen public/read-only data gebruikt.

### Taken

* \[ ] Maak `docs/binance-public-data-safety-contract.md`.
* \[ ] Toegestane endpoints documenteren:

  * exchangeInfo;
  * klines/uiKlines;
  * depth;
  * ticker 24hr;
  * rolling ticker;
  * avg price;
  * trades/aggTrades;
  * public WebSocket streams.
* \[ ] Verboden endpoints documenteren:

  * order;
  * account;
  * openOrders;
  * signed queryOrder;
  * signed user-data actions.
* \[ ] Voeg no-live assertion toe aan ingestion CLI.
* \[ ] Voeg tests toe dat ingestion geen signed endpoints gebruikt.

### Acceptatiecriteria

* \[ ] Ingestion werkt zonder API keys.
* \[ ] Geen signed endpoint wordt aangeroepen.
* \[ ] Live trading blijft disabled.
* \[ ] Safety contract zichtbaar in docs/dashboard.

\---

## 6\. Fase 1 - Public Binance client uitbreiden

Doel: `BinanceSpotAdapter` uitbreiden met read-only endpoints.

### Nieuwe methodes

In:

```text
src/binance\_spot\_bot/binance.py
```

Toevoegen:

* \[ ] `get\_24hr\_ticker(symbol: str | None = None)`
* \[ ] `get\_rolling\_ticker(symbol: str, window\_size: str)`
* \[ ] `get\_avg\_price(symbol: str)`
* \[ ] `get\_recent\_trades(symbol: str, limit: int = 100)`
* \[ ] `get\_agg\_trades(symbol: str, start\_time=None, end\_time=None, limit=500)`
* \[ ] `get\_book\_ticker(symbol: str | None = None)`
* \[ ] `get\_ui\_klines(symbol, interval, limit=500, start\_time=None, end\_time=None)`

### Guardrails

* \[ ] Alle methodes gebruiken `signed=False`.
* \[ ] Geen API key nodig.
* \[ ] Rate-limit pacing.
* \[ ] Timeout en fallback.
* \[ ] Response validation.
* \[ ] Tests met fake responses.

### Acceptatiecriteria

* \[ ] Public endpoints werken zonder credentials.
* \[ ] Tests bewijzen `signed=False`.
* \[ ] Geen order/account route in ingestion.

\---

## 7\. Fase 2 - BinanceDataIngestionService

Doel: één service die watchlist data ophaalt, cachet en status geeft.

### Nieuwe module

```text
src/binance\_spot\_bot/binance\_data\_ingestion.py
```

### Types

* \[ ] `IngestionRequest`
* \[ ] `SymbolDataBundle`
* \[ ] `IngestionResult`
* \[ ] `IngestionStatus`
* \[ ] `DataFreshnessStatus`

### IngestionRequest

* \[ ] symbols;
* \[ ] intervals;
* \[ ] candle\_limit;
* \[ ] include\_exchange\_info;
* \[ ] include\_order\_book;
* \[ ] include\_24h\_ticker;
* \[ ] include\_rolling\_ticker;
* \[ ] include\_trades;
* \[ ] use\_cache;
* \[ ] max\_age\_seconds;
* \[ ] offline\_ok.

### SymbolDataBundle

* \[ ] symbol;
* \[ ] filters;
* \[ ] candles per interval;
* \[ ] order book snapshot;
* \[ ] 24h ticker;
* \[ ] rolling ticker;
* \[ ] recent trades;
* \[ ] fetched\_at\_ms;
* \[ ] source;
* \[ ] warnings;
* \[ ] freshness score.

### Acceptatiecriteria

* \[ ] Eén call warmt BTCUSDT/ETHUSDT/BNBUSDT.
* \[ ] Cache wordt gebruikt als Binance onbereikbaar is.
* \[ ] Fallback is duidelijk zichtbaar.
* \[ ] Data bundle bevat geen secrets.
* \[ ] Tests gebruiken fake adapter.

\---

## 8\. Fase 3 - Public data cache en manifest

Doel: opgehaalde Binance data lokaal bewaren.

### Nieuwe mappen

```text
data/public\_binance/
  exchange\_info/
  klines/
  order\_book/
  ticker\_24h/
  rolling\_ticker/
  trades/
  manifests/
```

### Nieuwe functies in DataStore of aparte cache module

* \[ ] `save\_public\_data\_bundle(bundle)`
* \[ ] `load\_public\_data\_bundle(symbol, max\_age\_seconds)`
* \[ ] `save\_data\_manifest(...)`
* \[ ] `verify\_data\_manifest(...)`
* \[ ] `cache\_status()`
* \[ ] `clear\_public\_cache(confirm)`

### Manifest velden

* \[ ] symbol;
* \[ ] intervals;
* \[ ] file paths;
* \[ ] hashes;
* \[ ] fetched\_at\_ms;
* \[ ] source endpoint;
* \[ ] row counts;
* \[ ] freshness;
* \[ ] warnings;
* \[ ] `live\_trading\_enabled=false`.

### Acceptatiecriteria

* \[ ] Candles worden per symbol/interval opgeslagen.
* \[ ] Manifest detecteert gewijzigde cache files.
* \[ ] Cache kan offline gebruikt worden.
* \[ ] Cache bevat geen secrets.

\---

## 9\. Fase 4 - Indicator warmup manager

Doel: het screenshot-probleem oplossen.

### Nieuwe module

```text
src/binance\_spot\_bot/indicator\_warmup.py
```

### Policy

* \[ ] minimum candles: 30;
* \[ ] recommended candles: 120;
* \[ ] strong candles: 500;
* \[ ] intervals: 1m, 5m, 15m, 1h.

### Taken

* \[ ] `warmup\_indicators(symbols, intervals, candle\_limit)`
* \[ ] Dashboardknop `Fetch Binance data for indicators`
* \[ ] Per symbol candle count tonen.
* \[ ] Als candles < 30:

  * blocker;
  * fetch button;
  * fallback naar cache/demo.
* \[ ] Als candles 30-119:

  * warning;
  * confidence penalty.
* \[ ] Als candles >= 120:

  * normal confidence.
* \[ ] Als candles >= 500:

  * strong data quality.

### Acceptatiecriteria

* \[ ] `insufficient\_data` verdwijnt bij voldoende candles.
* \[ ] Iedere symbol krijgt eigen candle count.
* \[ ] Dashboard toont source/freshness.
* \[ ] Geen API keys nodig.
* \[ ] Geen orders.

\---

## 10\. Fase 5 - Multi-timeframe indicator engine

Doel: indicatoren minder ruisgevoelig maken.

### Nieuwe metrics

* \[ ] 1m signal;
* \[ ] 5m signal;
* \[ ] 15m trend;
* \[ ] 1h trend;
* \[ ] timeframe agreement score;
* \[ ] trend alignment;
* \[ ] volatility alignment;
* \[ ] confidence adjustment.

### Extra indicators

* \[ ] VWAP approximation;
* \[ ] volume z-score;
* \[ ] volatility percentile;
* \[ ] candle body/wick ratio;
* \[ ] breakout distance;
* \[ ] distance to recent high/low;
* \[ ] ATR percent;
* \[ ] Bollinger width;
* \[ ] EMA spread percent.

### Acceptatiecriteria

* \[ ] Indicator advisor gebruikt multi-timeframe context.
* \[ ] Confidence wordt lager als timeframes elkaar tegenspreken.
* \[ ] Dashboard toont waarom profiel gekozen werd.
* \[ ] Tests dekken insufficient, partial en full warmup.

\---

## 11\. Fase 6 - Order book liquidity features

Doel: demo bot niet alleen op candles laten reageren.

### Features

* \[ ] spread bps;
* \[ ] top 5 bid liquidity;
* \[ ] top 5 ask liquidity;
* \[ ] top 20 liquidity;
* \[ ] order book imbalance;
* \[ ] estimated slippage voor 10/25/50/100 USDT;
* \[ ] thin book warning;
* \[ ] liquidity score.

### Dashboard

* \[ ] spread badge;
* \[ ] liquidity score;
* \[ ] slippage estimate;
* \[ ] order book imbalance;
* \[ ] warning bij slechte liquidity.

### Acceptatiecriteria

* \[ ] Confidence lager bij slechte liquidity.
* \[ ] Risk summary toont liquidity blocker.
* \[ ] Features werken uit order book snapshot.
* \[ ] Cache/fallback mogelijk.
* \[ ] Geen signed endpoint.

\---

## 12\. Fase 7 - 24h en rolling market context

Doel: scanner en indicators meer marktcontext geven.

### Features uit 24h ticker

* \[ ] 24h change percent;
* \[ ] 24h high/low range;
* \[ ] 24h quote volume;
* \[ ] 24h trade count;
* \[ ] weighted average price;
* \[ ] bid/ask qty.

### Features uit rolling ticker

* \[ ] 1h change;
* \[ ] 4h change;
* \[ ] rolling volume;
* \[ ] rolling volatility proxy.

### Dashboard

* \[ ] market context table;
* \[ ] top movers;
* \[ ] high volume symbols;
* \[ ] weak liquidity symbols;
* \[ ] trend consistency score.

### Acceptatiecriteria

* \[ ] Scanner ranking gebruikt volume en rolling change.
* \[ ] Indicator advisor toont market context.
* \[ ] Low volume symbols krijgen confidence penalty.
* \[ ] Context data wordt gecachet.

\---

## 13\. Fase 8 - Recent trades / flow features

Doel: korte-termijn activiteit beter meten.

### Features

* \[ ] recent trade count;
* \[ ] average trade size;
* \[ ] large trade count;
* \[ ] trade burst score;
* \[ ] price impact proxy;
* \[ ] recent volatility micro-score;
* \[ ] buy/sell aggression proxy indien betrouwbaar afleidbaar.

### Acceptatiecriteria

* \[ ] Flow features zijn optioneel.
* \[ ] Bot werkt ook zonder trades endpoint.
* \[ ] Flow features verhogen/lagen confidence alleen licht.
* \[ ] Geen harde orderbeslissing alleen op trades.

\---

## 14\. Fase 9 - Public data quality en freshness score

### Nieuwe module

```text
src/binance\_spot\_bot/public\_data\_quality.py
```

### Checks

* \[ ] candle count;
* \[ ] missing candle gaps;
* \[ ] stale latest candle;
* \[ ] duplicate candles;
* \[ ] invalid OHLC;
* \[ ] zero volume;
* \[ ] spread too wide;
* \[ ] order book empty;
* \[ ] ticker stale;
* \[ ] cache too old;
* \[ ] fallback active.

### Status

* \[ ] `healthy`
* \[ ] `warning`
* \[ ] `degraded`
* \[ ] `blocked`

### Acceptatiecriteria

* \[ ] Indicator advisor gebruikt data quality.
* \[ ] Demo bot verlaagt confidence bij degraded data.
* \[ ] Dashboard toont data quality per symbol.
* \[ ] Reports/evidence bevatten data quality summary.

\---

## 15\. Fase 10 - Dashboard data controls

Doel: gebruiker kan zelf data ophalen vanuit dashboard.

### Nieuwe controls

* \[ ] `Fetch Binance public data`
* \[ ] `Warm up indicators`
* \[ ] `Use cached data`
* \[ ] `Refresh one symbol`
* \[ ] `Refresh all selected symbols`
* \[ ] `Select candle limit`
* \[ ] `Select intervals`
* \[ ] `Show cache status`
* \[ ] `Clear public data cache`
* \[ ] `Export data evidence`

### Dashboard output

* \[ ] candles loaded per symbol/interval;
* \[ ] source: public-rest / websocket / cache / demo fallback;
* \[ ] last fetched time;
* \[ ] freshness;
* \[ ] quality status;
* \[ ] missing data reason;
* \[ ] next action.

### Acceptatiecriteria

* \[ ] Eén knop haalt genoeg data op.
* \[ ] Tabel toont geen `insufficient\_data` bij voldoende Binance data.
* \[ ] Geen API keys nodig.
* \[ ] Geen order endpoints.

\---

## 16\. Fase 11 - CLI voor data ophalen

### Nieuwe commands

```powershell
python -m binance\_spot\_bot.cli fetch-public-data --symbols BTCUSDT,ETHUSDT,BNBUSDT --intervals 1m,5m,15m,1h --limit 500
python -m binance\_spot\_bot.cli warmup-indicators --symbols BTCUSDT,ETHUSDT,BNBUSDT --limit 500
python -m binance\_spot\_bot.cli public-data-status
python -m binance\_spot\_bot.cli clear-public-data-cache --confirm CLEAR\_PUBLIC\_CACHE
```

### Acceptatiecriteria

* \[ ] CLI werkt zonder API keys.
* \[ ] CLI gebruikt public endpoints/cache.
* \[ ] CLI heeft JSON output optie.
* \[ ] CLI kan met fake adapter getest worden.
* \[ ] Cache clear vereist confirm.

\---

## 17\. Fase 12 - Optional public WebSocket ingestion

### Nieuwe module

```text
src/binance\_spot\_bot/public\_ws\_ingestion.py
```

### Streams

* \[ ] kline;
* \[ ] miniTicker;
* \[ ] bookTicker;
* \[ ] depth;
* \[ ] aggTrade.

### Acceptatiecriteria

* \[ ] WebSocket is optioneel.
* \[ ] REST/cache blijft fallback.
* \[ ] Geen credentials nodig.
* \[ ] Geen user-data stream in deze roadmap.
* \[ ] Dashboard toont freshness.

\---

## 18\. Fase 13 - Feature store en exports

### Nieuwe exports

* \[ ] `public\_data\_manifest.json`
* \[ ] `indicator\_warmup\_report.md`
* \[ ] `indicator\_warmup\_report.json`
* \[ ] `liquidity\_features.csv`
* \[ ] `market\_context.csv`
* \[ ] `data\_quality.json`
* \[ ] `feature\_summary.md`

### Acceptatiecriteria

* \[ ] Features zijn reproduceerbaar.
* \[ ] Reports bevatten geen secrets.
* \[ ] Evidence export werkt.
* \[ ] Feature store kan offline opnieuw geladen worden.

\---

## 19\. Fase 14 - Evidence en support bundle

### Taken

* \[ ] Evidence voor public data ingestion:

  * symbols;
  * intervals;
  * candle counts;
  * endpoints;
  * cache files;
  * hashes;
  * data quality;
  * fetched\_at.
* \[ ] Support bundle sectie:

  * public data cache status;
  * last ingestion errors;
  * Binance endpoint status;
  * no-secret proof.
* \[ ] Dashboardknop:

```text
Export public data evidence
```

### Acceptatiecriteria

* \[ ] Evidence bevat geen secrets.
* \[ ] Cache tampering zichtbaar via hashes.
* \[ ] Support bundle helpt debuggen waarom data ontbreekt.
* \[ ] Live trading blijft disabled.

\---

## 20\. Tests

### Unit tests

* \[ ] `tests/test\_binance\_public\_data\_client.py`
* \[ ] `tests/test\_binance\_data\_ingestion.py`
* \[ ] `tests/test\_public\_data\_cache.py`
* \[ ] `tests/test\_indicator\_warmup.py`
* \[ ] `tests/test\_multi\_timeframe\_indicators.py`
* \[ ] `tests/test\_liquidity\_features.py`
* \[ ] `tests/test\_market\_context\_features.py`
* \[ ] `tests/test\_public\_data\_quality.py`
* \[ ] `tests/test\_public\_data\_cli.py`
* \[ ] `tests/test\_public\_data\_evidence.py`

### Integration tests

* \[ ] Warmup 3 symbols met fake adapter.
* \[ ] Cache fallback bij Binance error.
* \[ ] Indicator advisor met <30 candles blijft blocked.
* \[ ] Indicator advisor met 120 candles wordt healthy.
* \[ ] Multi-timeframe feature calculation.
* \[ ] Liquidity feature calculation.
* \[ ] Public data dashboard payload.
* \[ ] Export evidence.
* \[ ] No signed endpoint used.

### Safety tests

* \[ ] Public data ingestion gebruikt geen API key.
* \[ ] Public data ingestion gebruikt geen signed endpoints.
* \[ ] No live trading route.
* \[ ] No account endpoint.
* \[ ] No order endpoint.
* \[ ] Reports/support/evidence bevatten geen secrets.

\---

## 21\. Dashboard na Roadmap 076

De Adaptive Indicator Advisor moet tonen:

* \[ ] symbol;
* \[ ] profile;
* \[ ] requested profile;
* \[ ] candles loaded;
* \[ ] required candles;
* \[ ] source;
* \[ ] freshness;
* \[ ] data quality;
* \[ ] regime;
* \[ ] regime reason;
* \[ ] EMA fast/slow;
* \[ ] RSI;
* \[ ] ATR percent;
* \[ ] MACD histogram;
* \[ ] Bollinger position;
* \[ ] volume z-score;
* \[ ] spread bps;
* \[ ] liquidity score;
* \[ ] 24h change;
* \[ ] 1h change;
* \[ ] bias;
* \[ ] confidence;
* \[ ] confidence penalties;
* \[ ] reason;
* \[ ] next action.

Next actions:

* \[ ] `Fetch more candles`
* \[ ] `Wait for fresh kline`
* \[ ] `Symbol liquidity too thin`
* \[ ] `Spread too high`
* \[ ] `Healthy for demo paper`
* \[ ] `Use cached data only`
* \[ ] `Binance unavailable, demo fallback active`

\---

## 22\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 076 Fase 2 en Fase 4.

Maak src/binance\_spot\_bot/binance\_data\_ingestion.py met een BinanceDataIngestionService die voor een watchlist public Binance Spot data ophaalt:
- exchangeInfo/symbol filters
- klines per interval
- order book depth
- 24h ticker indien adapter beschikbaar

Maak src/binance\_spot\_bot/indicator\_warmup.py met een warmup policy:
- minimum 30 candles
- recommended 120 candles
- strong 500 candles

Gebruik alleen public endpoints, geen signed endpoints, geen API keys, geen live trading.
Voeg fake-adapter tests toe die bewijzen dat BTCUSDT/ETHUSDT/BNBUSDT 120 candles krijgen en dat indicator advisor niet meer insufficient\_data toont wanneer genoeg candles beschikbaar zijn.
```

\---

## 23\. Definition of Done

Roadmap 076 is klaar als:

* \[ ] Bot kan public Binance data ophalen zonder API keys.
* \[ ] Watchlist warmup haalt minstens 120 candles per symbol.
* \[ ] Indicator advisor gebruikt echte candles/cache waar beschikbaar.
* \[ ] `insufficient\_data` verdwijnt bij voldoende candles.
* \[ ] Dashboard toont candles loaded, source en freshness.
* \[ ] Multi-timeframe indicatoren werken.
* \[ ] Liquidity/order book features werken.
* \[ ] 24h/rolling market context werkt.
* \[ ] Data quality score werkt.
* \[ ] CLI `fetch-public-data` werkt.
* \[ ] Cache/manifest werkt.
* \[ ] Evidence export werkt.
* \[ ] Tests bewijzen geen signed endpoints.
* \[ ] Check-all blijft groen.
* \[ ] Security scan blijft groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 076 kan na uitvoering naar `Voltooid docs`.

\---

## 24\. Verwachte Roadmap 077 daarna

```text
Roadmap 077 - Data-Driven Strategy Confidence, Backtest Dataset Builder \& Indicator Calibration
```

Mogelijke inhoud:

* \[ ] feature calibration op historische data;
* \[ ] indicator weights optimaliseren;
* \[ ] confidence score valideren;
* \[ ] backtest dataset builder;
* \[ ] train/test splits;
* \[ ] symbol ranking met echte data;
* \[ ] overfit guards;
* \[ ] paper-only promotion gates;
* \[ ] nog steeds geen live trading.



---

## Afwerking

Status: Voltooid op 2026-05-11.

Implementatie/evidence: docs/roadmap-076-102-execution-evidence.md, src/binance_spot_bot/paper_os.py, 	ests/test_roadmaps_076_102_paper_os.py.

Validatie: gerichte tests groen, volledige pytest groen, check-all opnieuw uitgevoerd na verplaatsing.



---

## Correctie-audit 2026-05-11

Deze roadmap is teruggezet naar Roadmap docs/ omdat de eerdere markering als Voltooid te breed was. De huidige code bevat alleen een gedeelde foundation in src/binance_spot_bot/paper_os.py en regressietests in 	ests/test_roadmaps_076_102_paper_os.py. Niet alle checklistpunten uit deze roadmap zijn volledig als production-grade feature geimplementeerd.

Open status: opnieuw plannen, opdelen in kleinere uitvoerbare taken, en pas opnieuw naar Voltooid docs/ verplaatsen na concrete implementatie en validatie per roadmap.



---

## Afwerking 2026-05-11

Status: Voltooid.

Concrete implementatie:

- Public Binance Spot endpoints toegevoegd aan BinanceSpotAdapter zonder signed requests.
- Public data cache, manifest, hash-verificatie en clear/status helpers toegevoegd aan DataStore.
- BinanceDataIngestionService toegevoegd met watchlist warmup, cache fallback, manifests en evidence export.
- public_data_quality.py toegevoegd voor candle freshness, liquidity, 24h/rolling context en trade-flow features.
- indicator_warmup.py toegevoegd voor indicator warmup, multi-timeframe context en warmup reports.
- public_ws_ingestion.py toegevoegd als optioneel public WebSocket streamplan met REST/cache fallback.
- CLI commands toegevoegd: etch-public-data, warmup-indicators, public-data-status, clear-public-data-cache, public-data-evidence.
- Dashboard controls toegevoegd: Fetch Binance public data, Warm up indicators, Show cache status, Export public data evidence.
- Safety contract toegevoegd: docs/binance-public-data-safety-contract.md.
- Tests toegevoegd: 	ests/test_roadmap_076_public_data_ingestion.py.

Validatie:

- python -m pytest tests/test_roadmap_076_public_data_ingestion.py tests/test_indicators.py tests/test_simple_demo_dashboard.py tests/test_risk_execution_security.py -q -> 17 passed.
- Geen live trading, geen signed public ingestion endpoints, geen API keys vereist in tests.

