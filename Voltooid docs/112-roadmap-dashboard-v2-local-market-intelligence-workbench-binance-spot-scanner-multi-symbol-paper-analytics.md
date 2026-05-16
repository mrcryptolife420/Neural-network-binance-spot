# Roadmap 112 - Dashboard V2 Local Market Intelligence Workbench, Binance Spot Scanner \& Multi-Symbol Paper Analytics

Status: Voltooid / Gevalideerd
Project: Neural network Binance spot  
Datum: 2026-05-11
Afgerond: 2026-05-15
Validatie: gerichte pytest 112, CLI-smokes, security-scan, Dashboard V2 smoke, check-all --skip-tests, Playwright browser-smoke op /market-intelligence, volledige pytest-suite.
Voorgestelde locatie:

```text
Roadmap docs/112-roadmap-dashboard-v2-local-market-intelligence-workbench-binance-spot-scanner-multi-symbol-paper-analytics.md
```

## Samenvatting

Roadmap 104 bouwt Dashboard V2 naast Streamlit met FastAPI/WebSocket/React.

Roadmap 105 migreert feature parity van Streamlit naar Dashboard V2.

Roadmap 106 maakt Dashboard V2 performant, lokaal packagebaar, offline/static, browser-smoke-ready en cutover-ready.

Roadmap 107 vereenvoudigt operatorflows, verwerkt UAT-feedback en maakt Streamlit deprecation planning concreet.

Roadmap 108 zet Dashboard V2 als primaire UI neer, maakt V2-only operator mode en houdt Streamlit als legacy/fallback.

Roadmap 109 maakt Streamlit removal-candidate, dependency isolation, V2-only release hardening, legacy archive en removal readiness gate.

Roadmap 110 maakt Dashboard V2 een echte operator workspace met custom layouts, widgets, watchlists, preferences, synchronized charts en workspace evidence.

Roadmap 111 bouwt veilige local-only plugin-less extension packs, workspace templates, analytics presets, watchlists en operator workflow packs.

Roadmap 112 is de logische volgende stap: **een lokale Market Intelligence Workbench voor Binance Spot public data**, gebouwd op Dashboard V2 workspaces en packs. Het doel is multi-symbol scanning, watchlist snapshots, symbol ranking, spread/volume/volatility/momentum analytics, market-data freshness, data-quality scoring en multi-symbol paper analytics — allemaal local-only, paper-only en zonder live trading.

Deze roadmap maakt van Dashboard V2 niet alleen een bot-monitor, maar ook een lokale research/scanner-omgeving:

```text
Binance public spot endpoints
→ local market cache
→ watchlist scanner
→ symbol metrics
→ ranking/scoring
→ Dashboard V2 market intelligence workspace
→ paper-only strategy comparison
→ evidence/reporting
```

Live trading blijft volledig buiten scope. De scanner gebruikt alleen public/unsigned market data endpoints. Geen live mode, geen signed order endpoints, geen echte account endpoints, geen financiële aanbevelingen, geen auto-trading vanuit scanner rankings en geen externe telemetry.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 112`, `112-roadmap`, `Market Intelligence Workbench`, `Binance Spot Scanner`, `Multi-Symbol Paper Analytics` en `market scanner`.
* \[x] Geen bestaande Roadmap 112 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 111 is lokaal aangemaakt als Dashboard V2 Local Plugin-Less Extension Packs, Analytics Presets \& Operator Workspace Templates.

### Codebasecontrole

Breed bekeken met focus op Binance spot public data, market data, runtime snapshots, Dashboard V2/workspaces, CLI en check-all:

* \[x] `src/binance\_spot\_bot/binance.py`
* \[x] `src/binance\_spot\_bot/market\_data\_source.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/ui/page\_registry.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] roadmaplijn 104-111.

### Belangrijke bestaande basis

De codebase heeft nu of krijgt via Roadmap 104-111:

* \[x] `BinanceSpotAdapter` heeft public market endpoints:

  * `get\_exchange\_info`;
  * `get\_klines`;
  * `get\_order\_book`;
  * `get\_24hr\_ticker`;
  * `get\_rolling\_ticker`;
  * `get\_avg\_price`;
  * `get\_recent\_trades`;
  * `get\_agg\_trades`;
  * `get\_book\_ticker`;
  * `get\_ui\_klines`.
* \[x] Dezelfde adapter heeft signed/account/order routes, maar Roadmap 112 moet scanner code hard beperken tot public/unsigned endpoints.
* \[x] `market\_data\_source.py` heeft `StaticMarketDataSource`, `DemoMarketReplaySource`, `RestPollingMarketDataSource` en `WebSocketMarketDataSource` met veilige fallback naar REST/demo data.
* \[x] `runtime.py` beperkt UI modes tot `demo`, `paper` en `testnet-readiness`.
* \[x] `RuntimeSnapshot` bevat al candles, signals, fills, equity, market\_data, top\_of\_book, data\_quality, sessions, model info, alerts, paper account, readiness, demo orders en reconciliation.
* \[x] `page\_registry.py` bevat 36 dashboard pages en blokkeert live trading pages.
* \[x] `check\_all.py` forceert `LIVE\_TRADING\_ENABLED=false`, `KILL\_SWITCH=true` en `PYTHONPATH=src`.
* \[x] Roadmap 110/111 maken workspaces, widgets, watchlists, analytics presets en pack catalog mogelijk.

### Belangrijkste gat na Roadmap 111

Na Roadmap 111 zijn workspaces en packs veilig herbruikbaar. Wat nog mist is een echte market intelligence laag:

* \[ ] Geen multi-symbol Binance public data scanner.
* \[ ] Geen lokale cache voor exchangeInfo/ticker/bookTicker/klines per watchlist.
* \[ ] Geen watchlist market snapshot.
* \[ ] Geen spread/volume/volatility/liquidity ranking.
* \[ ] Geen symbol universe filtering.
* \[ ] Geen scanner presets voor majors, high volume, low spread, volatile, trending.
* \[ ] Geen multi-symbol paper analytics.
* \[ ] Geen symbol comparison workspace.
* \[ ] Geen market data freshness dashboard.
* \[ ] Geen scanner evidence bundle.
* \[ ] Geen scanner no-live proof.
* \[ ] Geen rate-limit budget en public endpoint guard.
* \[ ] Geen “scanner output is not trading advice” safety layer.

Roadmap 112 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 112

Maak een lokale Binance Spot Market Intelligence Workbench:

```text
Public market data adapter
→ local symbol universe
→ watchlist scanner
→ market snapshot cache
→ scanner metrics
→ ranking/scoring
→ multi-symbol paper analytics
→ Dashboard V2 scanner workspace
→ evidence bundle
```

Na Roadmap 112 moet de operator:

* \[ ] Binance spot symbol universe lokaal kunnen ophalen via public data.
* \[ ] Watchlists kunnen scannen zonder API keys.
* \[ ] Symbolen kunnen filteren op quote asset, status, volume, spread, volatility en data quality.
* \[ ] Rankings kunnen bekijken voor volume, spread, momentum, volatility, freshness en liquidity.
* \[ ] Klines, bookTicker, 24hr ticker en avg price kunnen combineren in scanner metrics.
* \[ ] Multi-symbol paper analytics kunnen draaien op demo/rest cached data.
* \[ ] Scanner presets kunnen laden in Dashboard V2 workspaces.
* \[ ] Scanner output kunnen exporteren als evidence/report.
* \[ ] Zeker weten dat scanner geen live trading of signed routes gebruikt.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen trading engine opnieuw bouwen.
* \[ ] Geen runtime refactor opnieuw bouwen.
* \[ ] Geen Dashboard V2 workspace systeem opnieuw bouwen.
* \[ ] Geen plugin runtime.
* \[ ] Geen remote marketplace.
* \[ ] Geen cloud scanner.
* \[ ] Geen externe telemetry.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed order endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen scanner die automatisch orders plaatst.
* \[ ] Geen financial advice labels zoals “koop nu”.
* \[ ] Geen API key vereisen voor market scanner.
* \[ ] Geen request storm zonder rate-limit budget.
* \[ ] Geen scanner cache met secrets.

Wel doen:

* \[ ] public-data-only scanner;
* \[ ] symbol universe cache;
* \[ ] watchlist scanner;
* \[ ] market metrics;
* \[ ] ranking/scoring;
* \[ ] multi-symbol paper analytics;
* \[ ] Dashboard V2 scanner widgets;
* \[ ] scanner workspace templates/packs;
* \[ ] evidence/reports/tests;
* \[ ] no-live/public-only guard.

\---

## 3\. Fase 0 - Market Intelligence Safety Contract

Nieuw docbestand:

```text
docs/market-intelligence-safety-contract.md
```

Regels:

* \[ ] Market intelligence is local-only.
* \[ ] Market scanner gebruikt alleen public/unsigned Binance spot market data endpoints.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed order endpoints.
* \[ ] Geen account endpoints.
* \[ ] Geen API keys nodig voor scanner.
* \[ ] Geen auto-ordering op basis van rankings.
* \[ ] Rankings zijn research/scanner-signalen, geen financieel advies.
* \[ ] Scanner actions zijn read-only behalve lokale cache/report writes.
* \[ ] Rate-limit budget verplicht.
* \[ ] Scanner evidence is secret-free.
* \[ ] Scanner output bevat `live\_trading\_enabled=False`.
* \[ ] Dashboard toont `MARKET INTELLIGENCE - NO LIVE TRADING`.
* \[ ] Public endpoint allowlist is machine-testbaar.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen signed/account/order endpoints geblokkeerd zijn.
* \[ ] Tests bewijzen scanner zonder API keys werkt.
* \[ ] Tests bewijzen ranking output geen “buy/sell advice” claim bevat.
* \[ ] Tests bewijzen reports secret-free zijn.

\---

## 4\. Fase 1 - Public Market Endpoint Policy

Nieuwe module:

```text
src/binance\_spot\_bot/market\_intelligence/public\_endpoint\_policy.py
```

Allowlist endpoints/methods:

* \[ ] `get\_exchange\_info`
* \[ ] `get\_klines`
* \[ ] `get\_ui\_klines`
* \[ ] `get\_24hr\_ticker`
* \[ ] `get\_rolling\_ticker`
* \[ ] `get\_avg\_price`
* \[ ] `get\_book\_ticker`
* \[ ] `get\_order\_book`
* \[ ] `get\_recent\_trades`
* \[ ] `get\_agg\_trades`

Forbidden:

* \[ ] `get\_account\_state`
* \[ ] `test\_order`
* \[ ] `place\_order`
* \[ ] `cancel\_order`
* \[ ] `get\_order`
* \[ ] `open\_orders`
* \[ ] `query\_order`
* \[ ] user data stream listen-key endpoints unless explicitly needed outside scanner.

Dataclasses:

* \[ ] `PublicEndpointPolicy`
* \[ ] `PublicEndpointCheck`
* \[ ] `PublicEndpointPolicyReport`

Acceptatiecriteria:

* \[ ] Policy blocks signed/account/order methods.
* \[ ] Policy can wrap/check adapter calls.
* \[ ] Policy report is JSON + Markdown.
* \[ ] Tests cover allowlist and blocklist.
* \[ ] No-live statement included.

\---

## 5\. Fase 2 - Symbol Universe Cache

Nieuwe module:

```text
src/binance\_spot\_bot/market\_intelligence/symbol\_universe.py
```

Doel: Binance spot symbol metadata lokaal cachen en filteren.

Dataclasses:

* \[ ] `SymbolUniverseEntry`
* \[ ] `SymbolUniverseSnapshot`
* \[ ] `SymbolUniverseFilter`
* \[ ] `SymbolUniverseReport`

Fields per symbol:

* \[ ] symbol;
* \[ ] base\_asset;
* \[ ] quote\_asset;
* \[ ] status;
* \[ ] is\_spot\_trading\_allowed;
* \[ ] order\_types;
* \[ ] tick\_size;
* \[ ] step\_size;
* \[ ] min\_qty;
* \[ ] max\_qty;
* \[ ] min\_notional;
* \[ ] permissions if available;
* \[ ] updated\_at\_ms.

Filters:

* \[ ] quote asset:

  * USDT;
  * FDUSD;
  * USDC;
  * BTC;
  * ETH.
* \[ ] status `TRADING`.
* \[ ] exclude leveraged tokens optional.
* \[ ] include/exclude symbols.
* \[ ] max symbols.
* \[ ] asset allow/deny list.

Storage:

```text
data/market-intelligence/symbol-universe/
  exchange\_info\_latest.json
  symbol\_universe\_latest.json
  symbol\_universe\_report.md
```

Acceptatiecriteria:

* \[ ] Symbol universe can be built from cached fixture.
* \[ ] Symbol universe can be built from public `exchangeInfo`.
* \[ ] Filters work offline.
* \[ ] No API keys required.
* \[ ] Tests use fixture exchangeInfo.

\---

## 6\. Fase 3 - Market Snapshot Cache

Nieuwe module:

```text
src/binance\_spot\_bot/market\_intelligence/market\_snapshot\_cache.py
```

Caches:

* \[ ] 24hr ticker snapshots.
* \[ ] bookTicker snapshots.
* \[ ] avgPrice snapshots.
* \[ ] rolling ticker snapshots.
* \[ ] klines tail.
* \[ ] uiKlines tail.
* \[ ] order book depth optional.
* \[ ] recent/agg trades optional.

Storage:

```text
data/market-intelligence/snapshots/
  tickers/
  book\_tickers/
  avg\_price/
  klines/
  rolling/
  depth/
  trades/
```

Cache metadata:

* \[ ] endpoint;
* \[ ] symbol;
* \[ ] interval/window;
* \[ ] fetched\_at\_ms;
* \[ ] age\_ms;
* \[ ] status:

  * fresh;
  * stale;
  * missing;
  * failed;
  * fallback.
* \[ ] payload\_hash;
* \[ ] source:

  * public\_rest;
  * cache;
  * fixture;
  * demo\_fallback.

Acceptatiecriteria:

* \[ ] Cache writes/loads JSON safely.
* \[ ] Staleness detection works.
* \[ ] Corrupt cache handled.
* \[ ] Secret scan passes.
* \[ ] Tests use temp dirs.

\---

## 7\. Fase 4 - Scanner Rate-Limit Budget

Nieuwe module:

```text
src/binance\_spot\_bot/market\_intelligence/rate\_limit\_budget.py
```

Features:

* \[ ] endpoint request budget.
* \[ ] symbols per scan limit.
* \[ ] concurrency limit.
* \[ ] scan interval limit.
* \[ ] backoff on 429/418.
* \[ ] cache-first mode.
* \[ ] dry-run request plan.
* \[ ] estimated request count.
* \[ ] public endpoint policy integration.

Dataclasses:

* \[ ] `ScannerRateLimitBudget`
* \[ ] `ScannerRequestPlan`
* \[ ] `ScannerRequestDecision`
* \[ ] `ScannerRateLimitReport`

Acceptatiecriteria:

* \[ ] Dry-run shows request plan.
* \[ ] Oversized watchlist gets warning/block.
* \[ ] 429/418 produces backoff status.
* \[ ] Cache-first mode reduces request count.
* \[ ] Tests cover budgets.

\---

## 8\. Fase 5 - Watchlist Scanner

Nieuwe module:

```text
src/binance\_spot\_bot/market\_intelligence/watchlist\_scanner.py
```

Input:

* \[ ] symbol universe;
* \[ ] watchlist;
* \[ ] scanner preset;
* \[ ] cache policy;
* \[ ] rate-limit budget;
* \[ ] interval/window settings.

Output:

* \[ ] `WatchlistScanRun`
* \[ ] `WatchlistSymbolSnapshot`
* \[ ] `WatchlistScanReport`

Per symbol:

* \[ ] symbol;
* \[ ] status;
* \[ ] last\_price;
* \[ ] bid;
* \[ ] ask;
* \[ ] spread\_bps;
* \[ ] volume\_24h;
* \[ ] quote\_volume\_24h;
* \[ ] price\_change\_percent\_24h;
* \[ ] avg\_price;
* \[ ] candle\_count;
* \[ ] last\_kline\_close\_time\_ms;
* \[ ] data\_age\_ms;
* \[ ] data\_quality\_status;
* \[ ] source\_status;
* \[ ] warnings.

Acceptatiecriteria:

* \[ ] Scanner runs from fixture cache.
* \[ ] Scanner can use public endpoints when available.
* \[ ] Scanner works without API keys.
* \[ ] Oversized watchlist respects budget.
* \[ ] Report is JSON + Markdown.

\---

## 9\. Fase 6 - Market Metrics Engine

Nieuwe module:

```text
src/binance\_spot\_bot/market\_intelligence/market\_metrics.py
```

Metrics:

* \[ ] spread\_bps;
* \[ ] quote\_volume\_24h;
* \[ ] base\_volume\_24h;
* \[ ] price\_change\_24h;
* \[ ] high\_low\_range\_24h;
* \[ ] intraday volatility from klines;
* \[ ] candle momentum;
* \[ ] moving average distance;
* \[ ] simple trend slope;
* \[ ] top-of-book freshness;
* \[ ] data freshness;
* \[ ] liquidity proxy;
* \[ ] volatility bucket;
* \[ ] momentum bucket;
* \[ ] data quality score.

Dataclasses:

* \[ ] `MarketMetricSet`
* \[ ] `MarketMetricConfig`
* \[ ] `MarketMetricReport`

Acceptatiecriteria:

* \[ ] Metrics deterministic from fixture data.
* \[ ] Missing data creates warning, not crash.
* \[ ] Decimal serialization safe.
* \[ ] No advice labels.
* \[ ] Tests cover edge cases.

\---

## 10\. Fase 7 - Symbol Ranking \& Scanner Scores

Nieuwe module:

```text
src/binance\_spot\_bot/market\_intelligence/symbol\_ranking.py
```

Ranking dimensions:

* \[ ] highest quote volume;
* \[ ] lowest spread;
* \[ ] highest volatility;
* \[ ] lowest volatility;
* \[ ] strongest positive momentum;
* \[ ] strongest negative momentum;
* \[ ] freshest data;
* \[ ] best liquidity proxy;
* \[ ] data quality score;
* \[ ] paper strategy suitability score.

Important wording:

* \[ ] Use “ranked by metric”.
* \[ ] Do not say “buy/sell”.
* \[ ] Do not say “best coin to trade”.
* \[ ] Do not produce financial advice.

Dataclasses:

* \[ ] `SymbolRank`
* \[ ] `SymbolRankingConfig`
* \[ ] `SymbolRankingReport`

Acceptatiecriteria:

* \[ ] Rankings deterministic.
* \[ ] Ties handled.
* \[ ] Missing metrics handled.
* \[ ] Advice wording scan passes.
* \[ ] Tests cover ranking configs.

\---

## 11\. Fase 8 - Scanner Presets

Nieuwe module:

```text
src/binance\_spot\_bot/market\_intelligence/scanner\_presets.py
```

Presets:

### `majors\_overview`

* \[ ] BTCUSDT;
* \[ ] ETHUSDT;
* \[ ] BNBUSDT;
* \[ ] SOLUSDT;
* \[ ] XRPUSDT.
* \[ ] metrics: spread, volume, volatility, momentum.

### `high\_volume\_usdt`

* \[ ] quote asset USDT;
* \[ ] status TRADING;
* \[ ] rank by quote volume;
* \[ ] max 50 symbols.

### `low\_spread\_liquidity`

* \[ ] quote asset USDT;
* \[ ] min quote volume;
* \[ ] rank by spread/liquidity.

### `volatile\_watch`

* \[ ] quote asset USDT;
* \[ ] rank by volatility/high-low range;
* \[ ] warnings for high risk.

### `data\_quality\_watch`

* \[ ] rank by freshness/staleness/data-quality warnings.

### `paper\_strategy\_candidates`

* \[ ] no advice;
* \[ ] rank by paper suitability metrics;
* \[ ] requires paper-only validation.

Acceptatiecriteria:

* \[ ] Presets validate.
* \[ ] Presets include budget.
* \[ ] Presets include no-live statement.
* \[ ] Presets produce scan config.
* \[ ] Tests cover all presets.

\---

## 12\. Fase 9 - Multi-Symbol Paper Analytics

Nieuwe module:

```text
src/binance\_spot\_bot/market\_intelligence/multi\_symbol\_paper\_analytics.py
```

Doel: paper-only strategy comparison across symbols.

Input:

* \[ ] watchlist scan report;
* \[ ] cached klines;
* \[ ] strategy/model alias optional;
* \[ ] risk settings;
* \[ ] time window;
* \[ ] max symbols.

Output per symbol:

* \[ ] paper session simulation status;
* \[ ] candle count;
* \[ ] signal count;
* \[ ] block count;
* \[ ] fill count;
* \[ ] paper PnL;
* \[ ] max drawdown;
* \[ ] fees estimate;
* \[ ] data quality warnings;
* \[ ] model used;
* \[ ] runtime/paper-only proof.

Strict rules:

* \[ ] No real orders.
* \[ ] No signed endpoints.
* \[ ] No account endpoints.
* \[ ] No live mode.
* \[ ] No financial advice.

Acceptatiecriteria:

* \[ ] Works on fixture candles.
* \[ ] Can run small watchlist.
* \[ ] Uses safe paper runtime or pure simulation helper.
* \[ ] Produces JSON + Markdown report.
* \[ ] Tests cover paper-only proof.

\---

## 13\. Fase 10 - Scanner API Endpoints

Nieuwe Dashboard V2 API routes:

```text
GET  /api/market-intelligence/health
GET  /api/market-intelligence/symbol-universe
POST /api/market-intelligence/symbol-universe/refresh
GET  /api/market-intelligence/scanner-presets
POST /api/market-intelligence/scan/preview
POST /api/market-intelligence/scan/run
GET  /api/market-intelligence/scan-runs
GET  /api/market-intelligence/scan-runs/{run\_id}
GET  /api/market-intelligence/rankings/{run\_id}
POST /api/market-intelligence/paper-analytics/preview
POST /api/market-intelligence/paper-analytics/run
GET  /api/market-intelligence/evidence
WS   /ws/market-intelligence
```

API rules:

* \[ ] All responses include `live\_trading\_enabled=False`.
* \[ ] Mutation routes only write local cache/reports.
* \[ ] Refresh/scan uses public endpoint policy.
* \[ ] Scan preview required before large scan.
* \[ ] Large scan confirm required.
* \[ ] No signed/account/order routes.
* \[ ] Payload limits enforced.
* \[ ] Reports redacted.

Acceptatiecriteria:

* \[ ] TestClient covers routes.
* \[ ] Public-only route proof passes.
* \[ ] Oversized scan blocked/warned.
* \[ ] No-live proof in every response.
* \[ ] Tests cover error paths.

\---

## 14\. Fase 11 - Dashboard V2 Market Intelligence Workspace

Nieuwe routes/pages:

```text
/market-intelligence
/market-intelligence/scanner
/market-intelligence/rankings
/market-intelligence/symbols
/market-intelligence/watchlists
/market-intelligence/paper-analytics
/market-intelligence/reports
```

Core panels:

* \[ ] scanner health;
* \[ ] endpoint policy status;
* \[ ] rate-limit budget;
* \[ ] symbol universe;
* \[ ] watchlist selector;
* \[ ] scanner preset selector;
* \[ ] scan preview;
* \[ ] scan progress;
* \[ ] ranking table;
* \[ ] symbol detail drawer;
* \[ ] metric explanation;
* \[ ] paper analytics runner;
* \[ ] evidence export;
* \[ ] no-live banner.

Acceptatiecriteria:

* \[ ] Scanner page loads in Dashboard V2.
* \[ ] Scan preview works from cache fixtures.
* \[ ] Rankings table works.
* \[ ] Symbol detail drawer works.
* \[ ] Browser smoke covers scanner happy path.

\---

## 15\. Fase 12 - Market Intelligence Widgets

Nieuwe Dashboard V2 widgets:

* \[ ] `MarketScannerHealthWidget`
* \[ ] `PublicEndpointPolicyWidget`
* \[ ] `RateLimitBudgetWidget`
* \[ ] `SymbolUniverseWidget`
* \[ ] `WatchlistSnapshotWidget`
* \[ ] `MarketRankingTableWidget`
* \[ ] `SpreadVolumeMatrixWidget`
* \[ ] `VolatilityMomentumWidget`
* \[ ] `DataFreshnessWidget`
* \[ ] `MarketDataQualityWidget`
* \[ ] `SymbolDetailWidget`
* \[ ] `MultiSymbolPaperAnalyticsWidget`
* \[ ] `ScannerEvidenceWidget`

Widget registry updates:

* \[ ] Add market\_intelligence category.
* \[ ] All widgets safe/read-only except local scan/cache actions.
* \[ ] No live actions.
* \[ ] No signed/account/order capabilities.

Acceptatiecriteria:

* \[ ] Widgets validate in widget registry.
* \[ ] Widgets render empty/loading/error states.
* \[ ] Widgets enforce no-live proof.
* \[ ] Frontend tests cover core widgets.
* \[ ] Workspace presets can use widgets.

\---

## 16\. Fase 13 - Market Intelligence Workspace/Pack Templates

Extends Roadmap 111 extension packs:

Built-in packs:

### `market-intelligence-overview`

* \[ ] scanner health;
* \[ ] watchlist snapshot;
* \[ ] rankings;
* \[ ] data freshness;
* \[ ] no-live proof.

### `binance-spot-scanner-desk`

* \[ ] symbol universe;
* \[ ] scanner presets;
* \[ ] scan preview;
* \[ ] ranking table;
* \[ ] symbol detail.

### `volume-spread-monitor`

* \[ ] high volume ranking;
* \[ ] low spread ranking;
* \[ ] spread-volume matrix;
* \[ ] data quality.

### `volatility-momentum-monitor`

* \[ ] volatility ranking;
* \[ ] momentum ranking;
* \[ ] candle chart;
* \[ ] risk warning panel.

### `multi-symbol-paper-lab`

* \[ ] watchlist;
* \[ ] paper analytics run;
* \[ ] compare PnL/drawdown/blocks;
* \[ ] export report.

Acceptatiecriteria:

* \[ ] Packs validate through Roadmap 111 schema.
* \[ ] Packs include no-live widgets.
* \[ ] Packs instantiate workspace.
* \[ ] Browser smoke covers at least one pack.
* \[ ] Pack evidence generated.

\---

## 17\. Fase 14 - Scanner Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/market\_intelligence/scanner\_evidence\_bundle.py
```

Bundle bevat:

* \[ ] safety contract;
* \[ ] public endpoint policy report;
* \[ ] symbol universe report;
* \[ ] market snapshot cache report;
* \[ ] rate-limit budget report;
* \[ ] watchlist scan report;
* \[ ] market metrics report;
* \[ ] ranking report;
* \[ ] scanner preset report;
* \[ ] multi-symbol paper analytics report;
* \[ ] Dashboard V2 API smoke;
* \[ ] browser smoke;
* \[ ] pack/template validation;
* \[ ] no-live proof;
* \[ ] redaction proof;
* \[ ] hashes.

Output:

```text
data/market-intelligence/evidence/<run\_id>/
  market\_intelligence\_evidence\_manifest.json
  market\_intelligence\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle clearly says rankings are not financial advice.
* \[ ] Dashboard can download bundle.

\---

## 18\. Fase 15 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli market-intelligence-policy --json
python -m binance\_spot\_bot.cli symbol-universe-refresh --quote USDT --json
python -m binance\_spot\_bot.cli symbol-universe-report --json
python -m binance\_spot\_bot.cli market-snapshot-cache-report --json
python -m binance\_spot\_bot.cli scanner-rate-limit-plan --preset majors\_overview --json
python -m binance\_spot\_bot.cli watchlist-scan-preview --preset majors\_overview --json
python -m binance\_spot\_bot.cli watchlist-scan-run --preset majors\_overview --confirm RUN\_PUBLIC\_MARKET\_SCAN
python -m binance\_spot\_bot.cli market-rankings --run-id <id> --json
python -m binance\_spot\_bot.cli market-scanner-presets --json
python -m binance\_spot\_bot.cli multi-symbol-paper-analytics-preview --watchlist majors --json
python -m binance\_spot\_bot.cli multi-symbol-paper-analytics-run --watchlist majors --confirm RUN\_PAPER\_ANALYTICS\_ONLY
python -m binance\_spot\_bot.cli market-intelligence-evidence-export
python -m binance\_spot\_bot.cli dashboard-v2-market-intelligence-smoke --json
```

Acceptatiecriteria:

* \[ ] Commands werken offline met fixtures/cache waar mogelijk.
* \[ ] Commands ondersteunen JSON.
* \[ ] Public scan confirm vereist.
* \[ ] Paper analytics confirm vereist.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Reports zijn secret-free.

\---

## 19\. Fase 16 - Check-All Integration

Nieuwe checks:

Fast profile:

* \[ ] market intelligence module imports.
* \[ ] public endpoint policy.
* \[ ] scanner preset validation.
* \[ ] symbol universe fixture validation.
* \[ ] no-live proof.

Deep profile:

* \[ ] watchlist scan fixture.
* \[ ] market metrics fixture.
* \[ ] ranking fixture.
* \[ ] multi-symbol paper analytics fixture.
* \[ ] Dashboard V2 scanner API smoke.
* \[ ] browser smoke for scanner page.
* \[ ] scanner evidence bundle verify.

Acceptatiecriteria:

* \[ ] Fast check-all blijft snel.
* \[ ] No-live/public-only failure is hard fail.
* \[ ] Deep profile covers scanner end-to-end.
* \[ ] Reports are secret-free.
* \[ ] Existing check-all safety env preserved.

\---

## 20\. Fase 17 - Operator/UAT Integration

Roadmap 102:

* \[ ] Operator manual krijgt Market Intelligence guide.
* \[ ] CLI cookbook krijgt scanner commands.
* \[ ] Troubleshooting krijgt rate-limit/data-stale/scanner-cache playbooks.
* \[ ] Evidence guide krijgt scanner evidence uitleg.

Roadmap 103:

* \[ ] UAT scenario: open Market Intelligence workspace.
* \[ ] UAT scenario: run scan preview.
* \[ ] UAT scenario: inspect rankings.
* \[ ] UAT scenario: run fixture multi-symbol paper analytics.
* \[ ] UAT scenario: verify no-live/public-only proof.
* \[ ] UAT scenario: export scanner evidence.

Acceptatiecriteria:

* \[ ] UAT scenarios pass.
* \[ ] Docs link valid.
* \[ ] UAT confirms no financial advice wording.
* \[ ] No-live proof included.
* \[ ] UAT feedback can create scanner backlog items.

\---

## 21\. Fase 18 - Release/Knowledge/Test/Performance Integration

Roadmap 089:

* \[ ] Release notes include market intelligence workbench.
* \[ ] Version manifest includes scanner schema version.
* \[ ] Migration notes include scanner cache path.

Roadmap 091:

* \[ ] Knowledge graph maps scanner modules to Binance public endpoints, Dashboard V2 routes and widgets.
* \[ ] Impact analysis detects adapter endpoint changes affecting scanner.
* \[ ] Ownership map includes market intelligence modules.

Roadmap 092:

* \[ ] Test selector chooses scanner tests for market\_intelligence changes.
* \[ ] Binance adapter public endpoint changes select endpoint policy tests.
* \[ ] Dashboard scanner UI changes select browser smoke.

Roadmap 093:

* \[ ] Scanner performance budget tracks symbol count, request count, scan duration, payload size.
* \[ ] Heavy scan warnings become findings.

Acceptatiecriteria:

* \[ ] Release evidence includes scanner evidence.
* \[ ] Knowledge graph updated.
* \[ ] Test selection works.
* \[ ] Performance reports include scanner budgets.
* \[ ] No-live proof preserved.

\---

## 22\. Fase 19 - Scheduled Scanner Reports

Uitbreiding op local scheduled reports:

Scheduled jobs:

* \[ ] daily symbol universe freshness check.
* \[ ] daily majors scan from cache/public budget.
* \[ ] weekly high-volume USDT scan.
* \[ ] weekly data quality watch.
* \[ ] weekly scanner evidence export.
* \[ ] post-release scanner smoke.
* \[ ] post-adapter-change endpoint policy check.

Metrics:

* \[ ] symbol universe age.
* \[ ] scan success/failure count.
* \[ ] stale symbol count.
* \[ ] rate-limit warnings.
* \[ ] cache hit ratio.
* \[ ] top volume symbols.
* \[ ] lowest spread symbols.
* \[ ] data quality warning count.
* \[ ] no-live/public-only proof status.

Acceptatiecriteria:

* \[ ] Jobs are local-only.
* \[ ] Jobs use public endpoint policy.
* \[ ] Jobs respect rate-limit budget.
* \[ ] Reports are secret-free.
* \[ ] No live trading.

\---

## 23\. Fase 20 - Tests

### Unit tests

* \[ ] `tests/test\_market\_intelligence\_safety\_contract.py`
* \[ ] `tests/test\_public\_endpoint\_policy.py`
* \[ ] `tests/test\_symbol\_universe.py`
* \[ ] `tests/test\_market\_snapshot\_cache.py`
* \[ ] `tests/test\_scanner\_rate\_limit\_budget.py`
* \[ ] `tests/test\_watchlist\_scanner.py`
* \[ ] `tests/test\_market\_metrics.py`
* \[ ] `tests/test\_symbol\_ranking.py`
* \[ ] `tests/test\_scanner\_presets.py`
* \[ ] `tests/test\_multi\_symbol\_paper\_analytics.py`
* \[ ] `tests/test\_market\_intelligence\_api.py`
* \[ ] `tests/test\_market\_intelligence\_widgets.py`
* \[ ] `tests/test\_market\_intelligence\_packs.py`
* \[ ] `tests/test\_scanner\_evidence\_bundle.py`

### Integration tests

* \[ ] Build symbol universe from fixture exchangeInfo.
* \[ ] Build ticker/bookTicker cache from fixtures.
* \[ ] Run watchlist scan from fixtures.
* \[ ] Compute metrics and rankings.
* \[ ] Run scanner preset.
* \[ ] Run multi-symbol paper analytics fixture.
* \[ ] Export evidence bundle.
* \[ ] Verify public endpoint policy.
* \[ ] Dashboard V2 scanner API TestClient smoke.

### Browser smoke

* \[ ] `/market-intelligence` loads.
* \[ ] scanner page loads.
* \[ ] preset selector visible.
* \[ ] scan preview works with fixture/cache.
* \[ ] rankings visible.
* \[ ] symbol detail opens.
* \[ ] paper analytics preview visible.
* \[ ] no-live banner visible.
* \[ ] no live controls visible.

### Safety tests

* \[ ] Signed endpoint call blocked.
* \[ ] Account endpoint call blocked.
* \[ ] Order endpoint call blocked.
* \[ ] Scanner works without API keys.
* \[ ] Live mode blocked.
* \[ ] Advice wording blocked.
* \[ ] Public scan obeys rate budget.
* \[ ] Evidence secret-free.
* \[ ] Check-all safe env preserved.

\---

## 24\. Docs

Nieuwe docs:

```text
docs/market-intelligence-safety-contract.md
docs/market-intelligence/public-endpoint-policy.md
docs/market-intelligence/symbol-universe.md
docs/market-intelligence/market-snapshot-cache.md
docs/market-intelligence/rate-limit-budget.md
docs/market-intelligence/watchlist-scanner.md
docs/market-intelligence/market-metrics.md
docs/market-intelligence/symbol-ranking.md
docs/market-intelligence/scanner-presets.md
docs/market-intelligence/multi-symbol-paper-analytics.md
docs/market-intelligence/dashboard-v2-workbench.md
docs/market-intelligence/scanner-widgets.md
docs/market-intelligence/scanner-evidence-bundle.md
docs/market-intelligence/troubleshooting.md
```

README updates:

* \[ ] Market Intelligence Workbench overview.
* \[ ] Public-data-only statement.
* \[ ] No financial advice statement.
* \[ ] Scanner commands.
* \[ ] Dashboard V2 scanner route.
* \[ ] Evidence export.
* \[ ] No-live statement.

Operator docs updates:

* \[ ] Scanner quick start.
* \[ ] Watchlist scan guide.
* \[ ] Ranking interpretation guide.
* \[ ] Paper analytics guide.
* \[ ] Rate-limit troubleshooting.
* \[ ] Public-only safety proof.

\---

## 25\. Codex bouwvolgorde

### PR 1 - Safety Contract + Public Endpoint Policy

* \[ ] `docs/market-intelligence-safety-contract.md`
* \[ ] `market\_intelligence/public\_endpoint\_policy.py`
* \[ ] endpoint allow/block tests.
* \[ ] no-live tests.

### PR 2 - Symbol Universe + Snapshot Cache

* \[ ] `symbol\_universe.py`
* \[ ] `market\_snapshot\_cache.py`
* \[ ] fixture exchangeInfo/ticker tests.

### PR 3 - Rate-Limit Budget + Watchlist Scanner

* \[ ] `rate\_limit\_budget.py`
* \[ ] `watchlist\_scanner.py`
* \[ ] dry-run/request-plan tests.

### PR 4 - Market Metrics + Rankings

* \[ ] `market\_metrics.py`
* \[ ] `symbol\_ranking.py`
* \[ ] deterministic ranking tests.

### PR 5 - Scanner Presets

* \[ ] `scanner\_presets.py`
* \[ ] presets for majors/high-volume/low-spread/volatile/data-quality/paper-candidates.
* \[ ] validation tests.

### PR 6 - Multi-Symbol Paper Analytics

* \[ ] `multi\_symbol\_paper\_analytics.py`
* \[ ] paper-only fixture tests.
* \[ ] no signed/order/account tests.

### PR 7 - Dashboard V2 API + Widgets

* \[ ] scanner API routes.
* \[ ] scanner widgets.
* \[ ] TestClient/frontend tests.

### PR 8 - Dashboard Workbench + Packs

* \[ ] Dashboard V2 market intelligence pages.
* \[ ] workspace/template packs.
* \[ ] browser smoke.

### PR 9 - Evidence + CLI + Check-All

* \[ ] `scanner\_evidence\_bundle.py`
* \[ ] CLI commands.
* \[ ] check-all integration.

### PR 10 - Docs, UAT, Release/Knowledge/Test/Performance Integration

* \[ ] docs.
* \[ ] UAT scenarios.
* \[ ] release notes.
* \[ ] knowledge/test/performance integration.
* \[ ] scheduled reports.

\---

## 26\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 112 PR 1: Market Intelligence Safety Contract + Public Market Endpoint Policy.

Maak docs/market-intelligence-safety-contract.md.

Maak src/binance\_spot\_bot/market\_intelligence/\_\_init\_\_.py.
Maak src/binance\_spot\_bot/market\_intelligence/public\_endpoint\_policy.py met:
- PublicEndpointPolicy
- PublicEndpointCheck
- PublicEndpointPolicyReport
- allowed\_public\_market\_methods()
- forbidden\_signed\_or\_account\_methods()
- check\_market\_intelligence\_endpoint(method\_name: str)
- assert\_public\_market\_endpoint(method\_name: str)
- public\_endpoint\_policy\_report\_to\_dict(...)
- write\_public\_endpoint\_policy\_report(...)

Allowlist minimaal:
- get\_exchange\_info
- get\_klines
- get\_ui\_klines
- get\_order\_book
- get\_24hr\_ticker
- get\_rolling\_ticker
- get\_avg\_price
- get\_recent\_trades
- get\_agg\_trades
- get\_book\_ticker

Blocklist minimaal:
- get\_account\_state
- test\_order
- place\_order
- cancel\_order
- get\_order
- open\_orders
- query\_order
- create\_listen\_key
- keepalive\_listen\_key
- close\_listen\_key

Gedrag:
- allowlisted methods krijgen status allowed
- blocklisted methods krijgen status blocked
- unknown methods krijgen status unknown/blocked by default
- report bevat live\_trading\_enabled=False
- report bevat no\_live\_statement
- report bevat public\_data\_only\_statement
- report bevat no\_financial\_advice\_statement
- secret-like values worden geredact
- geen command execution
- geen API calls
- geen signed endpoints
- geen account/order endpoints
- geen live trading

Voeg tests toe voor:
- all allowlisted methods allowed
- all blocklisted methods blocked
- unknown method blocked by default
- report JSON serialization
- live\_trading\_enabled=False
- no\_live\_statement aanwezig
- public\_data\_only\_statement aanwezig
- no\_financial\_advice\_statement aanwezig
- secret-like values worden geredact
```

Waarom eerst:

* Een market scanner mag nooit per ongeluk signed/order/account routes gebruiken.
* Deze policy is read-only en raakt runtime/trading/frontend niet.
* Het is klein genoeg voor Codex.
* No-live, public-only en no-financial-advice regels worden meteen machine-testbaar.
* Daarna kunnen symbol universe, cache, scanner en Dashboard V2 widgets veilig op deze policy bouwen.

\---

## 27\. Definition of Done

Roadmap 112 is klaar als:

* \[ ] Market Intelligence Safety Contract bestaat.
* \[ ] Public Market Endpoint Policy werkt.
* \[ ] Symbol Universe Cache werkt.
* \[ ] Market Snapshot Cache werkt.
* \[ ] Scanner Rate-Limit Budget werkt.
* \[ ] Watchlist Scanner werkt.
* \[ ] Market Metrics Engine werkt.
* \[ ] Symbol Ranking \& Scanner Scores werken.
* \[ ] Scanner Presets werken.
* \[ ] Multi-Symbol Paper Analytics werkt.
* \[ ] Scanner API Endpoints werken.
* \[ ] Dashboard V2 Market Intelligence Workspace werkt.
* \[ ] Market Intelligence Widgets werken.
* \[ ] Market Intelligence Workspace/Pack Templates werken.
* \[ ] Scanner Evidence Bundle werkt.
* \[ ] CLI commands werken.
* \[ ] Check-All Integration werkt.
* \[ ] Operator/UAT Integration werkt.
* \[ ] Release/Knowledge/Test/Performance Integration werkt.
* \[ ] Scheduled Scanner Reports werken.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen scanner zonder API keys werkt.
* \[ ] Tests bewijzen no-financial-advice wording.
* \[ ] Tests bewijzen evidence secret-free is.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Dashboard V2 market intelligence is local-only.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 112 kan na uitvoering naar `Voltooid docs`.

\---

## 28\. Verwachte Roadmap 113 daarna

Als Roadmap 112 groen is:

```text
Roadmap 113 - Local Multi-Symbol Strategy Lab, Scanner-to-Paper Experiment Queues \& Portfolio Candidate Research
```

Mogelijke inhoud:

* \[ ] scanner rankings omzetten naar paper-only experiment queues;
* \[ ] multi-symbol strategy comparison;
* \[ ] batch paper backtests;
* \[ ] candidate portfolio research;
* \[ ] no-live experiment governance;
* \[ ] still no live trading.

```

Als Roadmap 112 performanceproblemen vindt:

```text
Roadmap 113 - Market Scanner Performance Burn-Down, Cache Optimization \& Large Watchlist Scaling
```

Mogelijke inhoud:

* \[ ] cache hit ratio verbeteren;
* \[ ] batch public endpoint planning;
* \[ ] payload diffing;
* \[ ] large watchlist virtualization;
* \[ ] scanner scheduling budget;
* \[ ] still no live trading.

```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Market intelligence workbench and multi-symbol paper analytics.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.

