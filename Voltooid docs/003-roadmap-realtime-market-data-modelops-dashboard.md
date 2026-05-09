# Roadmap 003 - Realtime market data, modelops en dashboard verdieping

Status: Voltooid  
Volgt op:

- `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
- `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`

Doel: de bestaande veilige bot en lokale dashboard uitbreiden met realtime market data, robuuste orderbook/spread-informatie, betere paper-session persistence, model registry, drift/quality checks en frontend verbeteringen.  
Belangrijk: niets dubbel bouwen. Gebruik de bestaande `BotRuntime`, `RiskEngine`, `ExecutionEngine`, `AuditLog`, `DataStore`, Streamlit dashboard en CLI als basis. Live trading blijft buiten scope.

Voltooiingsnotitie:
- Realtime stream parsers, URL builders en reconnect-policy toegevoegd in `market_stream.py`.
- Top-of-book/orderbook skeleton, spread/staleness handling en risk-input-integratie toegevoegd.
- `BotRuntime` gebruikt nu een data-source abstraction voor demo, REST polling en WebSocket-degraded paper mode.
- Paper sessions, fills, snapshots en exports worden lokaal opgeslagen in `data/sessions/`.
- Lichte lokale model registry met aliases en CLI-registratie toegevoegd.
- Chronologische evaluation workflow en data-quality checks toegevoegd.
- Streamlit dashboard toont microstructure, data quality, sessions, ModelOps en blijft live trading uitsluiten.
- Verificatie uitgevoerd: unit tests, security scan, config validation en browsercheck.

## 1. Research samenvatting

### Binance realtime market data

Bronnen:

- Binance Spot WebSocket Streams: https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/web-socket-streams.md
- Binance User Data Streams: https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/user-data-stream.md

Belangrijke punten:

- Binance Spot market streams gebruiken `wss://stream.binance.com:9443` of `wss://stream.binance.com:443`.
- Symbolen in streamnamen zijn lowercase.
- Een WebSocket-connection is maximaal 24 uur geldig; reconnect moet dus expliciet onderdeel van het ontwerp zijn.
- Binance stuurt ping frames; de client moet pong responses correct afhandelen.
- Er geldt een limiet van 5 inkomende berichten per seconde per WebSocket-connection en maximaal 1024 streams per connection.
- Kline streams (`<symbol>@kline_<interval>`) geven candle updates; bij 1s elke 1000 ms, bij andere intervals elke 2000 ms.
- `@bookTicker` geeft realtime best bid/ask en is nuttig voor spread/slippage checks.
- Diff depth streams vereisen snapshot + buffered events + update-id validatie; bij gemiste sequence moet het lokale orderbook opnieuw opgebouwd worden.
- User Data Streams leveren account/order events zoals `outboundAccountPosition`, `balanceUpdate` en `executionReport`, maar vereisen API-key/auth flow. Voor Roadmap 003 alleen testnet-readiness/design of optionele testnet-only support, geen live.

### Frontend/dashboard

Bronnen:

- Streamlit fragments: https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment
- Streamlit fragment concepts: https://docs.streamlit.io/develop/concepts/architecture/fragments
- Plotly candlestick docs: https://plotly.com/python-api-reference/generated/plotly.graph_objects.Candlestick.html

Belangrijke punten:

- `st.fragment(run_every=...)` kan delen van het dashboard automatisch verversen zonder de volledige app te rerunnen.
- Dit past bij live metrics, chart updates en audit-tail streaming.
- Plotly candlestick blijft geschikt, maar de dashboardlaag moet minder vaak volledige figuren herbouwen en meer expliciet omgaan met lege/partial data.
- De huidige dashboardflow werkt, maar is nog een eenvoudige replay/full-rerun loop. Roadmap 003 moet dit verbeteren zonder een aparte frontend stack te introduceren.

### Modelops en training

Bronnen:

- scikit-learn `TimeSeriesSplit`: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
- PyTorch saving/loading models: https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html
- MLflow Model Registry workflows: https://www.mlflow.org/docs/latest/ml/model-registry/workflow/
- Evidently data drift docs: https://docs.evidentlyai.com/metrics/explainer_drift

Belangrijke punten:

- Time-series validatie moet chronologisch blijven; gewone shuffled cross-validation is ongeschikt omdat training op toekomstige data kan lekken.
- PyTorch adviseert modelparameters via `state_dict` te bewaren voor flexibele inference en restore.
- MLflow registry gebruikt modelversies, aliases en tags; voor dit project kan een lichte lokale registry eerst genoeg zijn voordat MLflow als dependency wordt toegevoegd.
- Drift detection vergelijkt reference/current distributies en is nuttig om te detecteren of live/paper inputfeatures afwijken van trainingdata.

## 2. Huidige staat na Roadmap 002

Bestaand en hergebruiken:

- `BinanceSpotAdapter`: REST market/account/order/test-order adapter.
- `DataStore`: raw/processed/features/model directories.
- `build_feature_rows`, `build_label_rows`: feature/label pipeline.
- `RuleBasedSignalModel`, `TinyNeuralSignalModel`: eerste modelinterfaces.
- `RiskEngine`, `RiskLimits`: deterministic trade gating.
- `ExecutionEngine`: disabled/paper/testnet execution boundary.
- `BotRuntime`: demo/paper/testnet-readiness runtime.
- `DemoMarketReplay`: synthetic replay.
- Streamlit dashboard: local visual dashboard.
- `AuditLog` en `RuntimeMetrics`.
- Tests en security scan.

Niet opnieuw bouwen:

- Geen tweede risk engine.
- Geen tweede execution path.
- Geen aparte dashboard backend tenzij Streamlit onmogelijk blijkt.
- Geen live trading UI.
- Geen duplicated Binance REST wrapper.

## 3. Roadmap 003 scope

Roadmap 003 bouwt vijf lagen:

1. Realtime market data client.
2. Local orderbook en spread/slippage feed.
3. Persistente paper sessions en replay/export.
4. Model registry en training/evaluation workflow.
5. Dashboard verbeteringen voor realtime observability.

Live trading, margin, futures en withdrawals blijven buiten scope.

## 4. Backend uitbreidingen

### Fase 0 - Dependencies en boundaries

Doel: realtime support toevoegen zonder de core onnodig te breken.

Toevoegen aan optionele dependency group:

```toml
realtime = [
  "websockets>=12",
]
mlops = [
  "scikit-learn>=1.5",
]
```

MLflow en Evidently blijven voorlopig research/optioneel. Eerst wordt een lichte lokale registry en drift summary gebouwd met bestaande dataformaten.

Acceptatiecriteria:

- Bestaande tests blijven werken zonder `realtime` of `mlops` dependencies.
- Nieuwe realtime tests mogen websockets mocken en mogen niet afhankelijk zijn van Binance netwerk.
- Geen nieuwe dependency wordt verplicht voor demo mode.

### Fase 1 - Realtime market data client

Nieuwe module:

```text
src/binance_spot_bot/market_stream.py
```

Verantwoordelijkheid:

- Binance Spot WebSocket stream URL's bouwen.
- Lowercase stream symbols afdwingen.
- Subscribe/unsubscribe payloads valideren.
- Kline, trade, miniTicker en bookTicker events parsen naar interne dataclasses.
- Reconnect policy modelleren.
- Heartbeat/ping-pong gedrag documenteren en waar mogelijk via library support afhandelen.

Nieuwe types:

```text
KlineStreamEvent
BookTickerEvent
TradeStreamEvent
StreamStatus
```

Minimale streams voor Roadmap 003:

- `<symbol>@kline_<interval>`
- `<symbol>@bookTicker`
- optioneel `<symbol>@trade`

Acceptatiecriteria:

- Unit tests voor URL-builders, parser en lowercase symbol handling.
- Parser accepteert Binance payloadvormen uit de officiële docs.
- Runtime kan stream events via een interface ontvangen zonder direct aan websockets gekoppeld te zijn.
- Reconnect policy heeft backoff en 24h reconnect awareness.

### Fase 2 - Local orderbook en spread feed

Nieuwe module:

```text
src/binance_spot_bot/orderbook.py
```

Verantwoordelijkheid:

- Top-of-book uit `bookTicker` bijhouden.
- Later uitbreidbaar naar full local orderbook via depth snapshot + diff updates.
- Spread bps, mid price, bid/ask quantity en staleness berekenen.
- RiskEngine input verbeteren met echte bid/ask in `MarketState`.

Roadmap 003 implementatievolgorde:

1. Start met `bookTicker` top-of-book, omdat dit direct nuttig is voor spread/slippage en eenvoudiger is.
2. Voeg een `DepthBookBuilder` skeleton toe met sequence-check tests voor later.
3. Full diff-depth orderbook alleen implementeren als tests de officiële update-id regels afdekken.

Acceptatiecriteria:

- `MarketState.spread_bps` gebruikt echte bid/ask wanneer beschikbaar.
- RiskEngine blokkeert paper trades bij stale top-of-book of te brede spread.
- Dashboard toont bid, ask, mid en spread bps.
- Depth sequence gaps leiden tot `resync_required`, niet tot stille corrupte orderbook state.

### Fase 3 - Runtime data source abstraction

Nieuwe interface:

```text
MarketDataSource
- next_event()
- snapshot()
- status()
- close()
```

Implementaties:

- `DemoMarketReplaySource`
- `RestPollingMarketDataSource`
- `WebSocketMarketDataSource`

Aanpassing:

- `BotRuntime` gebruikt een data source in plaats van intern candles te laden.
- Bestaande demo/paper commands blijven compatibel.
- UI kan kiezen tussen demo replay, REST polling en WebSocket paper stream.

Acceptatiecriteria:

- Demo mode blijft deterministic.
- Paper REST mode blijft werken zoals Roadmap 002.
- WebSocket paper mode kan lokaal gestart worden en valt veilig terug naar error/degraded state bij netwerkproblemen.
- Geen signed endpoints nodig voor market-data-only mode.

### Fase 4 - Persistente paper sessions

Nieuwe module:

```text
src/binance_spot_bot/session_store.py
```

Verantwoordelijkheid:

- Paper session metadata opslaan.
- Trades/fills/equity curve opslaan.
- Runtime snapshots periodiek persistenter maken.
- Sessies kunnen later opnieuw bekeken worden in dashboard.

Opslag:

- Start met JSONL/CSV in `data/sessions/`.
- Geen database verplicht in deze roadmap.
- Houd DuckDB als latere optimalisatie.

Acceptatiecriteria:

- Elke `run-local` en dashboard-run krijgt een session id.
- Session summary bevat mode, symbol, interval, start/end, PnL, max drawdown, trades, blocks, model version.
- Dashboard kan minimaal de laatste 5 sessies tonen.
- Export naar CSV of JSONL werkt.

### Fase 5 - Model registry light

Nieuwe module:

```text
src/binance_spot_bot/model_registry.py
```

Verantwoordelijkheid:

- Model artifacts registreren.
- Metadata opslaan:
  - model id
  - model type
  - feature set version
  - dataset id
  - train/validation/test range
  - metrics
  - created timestamp
  - alias: `candidate`, `champion`, `archived`
- Bestaande `TinyNeuralSignalModel.save/load` gebruiken.

Waarom light registry eerst:

- MLflow is nuttig, maar een volledige MLflow server/registry is te zwaar voor de huidige lokale botfase.
- De roadmap moet eerst de interne contracts stabiliseren. Daarna kan MLflow als integratie komen.

Acceptatiecriteria:

- CLI kan model registreren:

```powershell
python -m binance_spot_bot.cli register-demo-model --alias candidate
```

- Runtime kan model by alias laden.
- Dashboard toont actieve model alias, model version en metrics.
- Er is nooit ambiguïteit welk model een paper-session gebruikte.

### Fase 6 - Time-series evaluation workflow

Nieuwe module:

```text
src/binance_spot_bot/evaluation.py
```

Verantwoordelijkheid:

- Chronologische train/validation/test evaluatie uitbreiden.
- Time-series split workflow toevoegen.
- Backtest metrics en model metrics samen rapporteren.
- Leakage guardrails expliciet testen.

Gebaseerd op scikit-learn `TimeSeriesSplit` concept:

- latere folds worden niet gebruikt om eerdere folds te trainen;
- optionele gap tussen train en test om leakage rond label horizon te verminderen;
- fold summaries worden opgeslagen.

Acceptatiecriteria:

- Geen shuffled split in evaluation workflow.
- Rapport bevat per fold:
  - dataset range
  - signal distribution
  - PnL
  - max drawdown
  - turnover
  - block reasons
- Dashboard kan laatste evaluation summary tonen.

### Fase 7 - Drift en data quality checks

Nieuwe module:

```text
src/binance_spot_bot/data_quality.py
```

Checks:

- missing candles;
- duplicate timestamps;
- non-monotonic timestamps;
- stale stream events;
- extreme spread;
- zero/negative prices;
- feature distribution shift vs reference;
- signal confidence distribution shift.

Geen zware drift dependency verplicht. Start met:

- mean/std comparison;
- percentile comparison;
- simple PSI-like buckets;
- alert threshold in config.

Acceptatiecriteria:

- Runtime health wordt `degraded` bij stale/missing/shifted data.
- Dashboard toont data quality panel.
- AuditLog krijgt `data_quality_warning` events.

## 5. Frontend uitbreidingen

### Fase 8 - Dashboard realtime refresh verbetering

Aanpassing:

- Gebruik `st.fragment(run_every=...)` voor chart/metrics/audit panels.
- Houd sidebar controls buiten fragments.
- Voorkom element-accumulatie door containers correct te gebruiken.

Acceptatiecriteria:

- Start/pause/step/reset blijven werken.
- Bij running mode refreshen chart en metrics zonder volledige app-jank.
- Dashboard blijft bruikbaar bij 1s refresh.
- Geen browser-console errors.

### Fase 9 - Market microstructure panel

Nieuwe UI-panelen:

- bid/ask/mid;
- spread bps;
- bid/ask quantity;
- stream status;
- last event age;
- reconnect count;
- data source mode: demo/rest/websocket.

Acceptatiecriteria:

- Spread blocks zijn visueel verklaarbaar.
- Bij stale stream toont dashboard duidelijke warning.
- Top-of-book panel is zichtbaar naast latest signal/risk decision.

### Fase 10 - Session browser

Nieuwe UI:

- lijst laatste paper sessions;
- selecteer session;
- toon equity curve, fills, block reasons en audit tail;
- export button voor session summary.

Acceptatiecriteria:

- Dashboard kan een afgeronde sessie tonen zonder runtime opnieuw te starten.
- Export bevat geen secrets.
- UI maakt verschil duidelijk tussen live stream en historische session replay.

### Fase 11 - Modelops panel

Nieuwe UI:

- actieve model alias;
- model metrics;
- dataset id;
- feature version;
- train/test range;
- laatst geregistreerde models;
- knop/CLI-instructie om candidate/champion te wisselen.

Acceptatiecriteria:

- Gebruiker kan zien welk model actief is.
- Paper fills/audit events blijven naar model version verwijzen.
- Geen modelpromotie zonder zichtbare metrics.

## 6. CLI uitbreidingen

Nieuwe commands:

```powershell
python -m binance_spot_bot.cli stream-paper --symbol BTCUSDT --interval 1m --source websocket
python -m binance_spot_bot.cli list-sessions
python -m binance_spot_bot.cli show-session --session-id <id>
python -m binance_spot_bot.cli register-demo-model --alias candidate
python -m binance_spot_bot.cli evaluate-model --symbol BTCUSDT --interval 1m
python -m binance_spot_bot.cli data-quality --symbol BTCUSDT --interval 1m
```

Regels:

- `stream-paper` mag alleen disabled/paper execution gebruiken.
- Geen CLI command mag live mode activeren.
- Testnet user-data/order event support mag pas na explicit testnet prechecks.

## 7. Testplan

Nieuwe tests:

- Stream payload parsers met officiële voorbeeldvormen.
- WebSocket URL builder.
- Reconnect policy state transitions.
- `BookTickerEvent` naar `MarketState`.
- Spread/staleness risk blocks.
- Demo/REST/WebSocket data source contract tests.
- SessionStore write/read/export.
- ModelRegistry register/load alias.
- Evaluation chronological split en gap behavior.
- Data quality warnings.
- Dashboard mode list bevat geen `live`.
- CLI smoke tests.

Bestaande checks blijven verplicht:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests
python -m binance_spot_bot.cli security-scan
python -m binance_spot_bot.cli validate-config
```

Browserverificatie:

- start dashboard;
- controleer realtime panel, orderbook panel, data quality panel, session browser en modelops panel;
- controleer geen console errors;
- controleer dat `LIVE TRADING DISABLED` zichtbaar blijft.

## 8. Acceptatiecriteria voor voltooiing

Roadmap 003 is pas volledig afgewerkt als:

- WebSocket market data parser/client bestaat en is getest.
- Runtime kan data source wisselen tussen demo, REST polling en WebSocket paper.
- Top-of-book/spread feed is zichtbaar in RiskEngine input en dashboard.
- Paper sessions worden opgeslagen en kunnen teruggekeken/exported worden.
- Model registry light werkt met aliases en actieve model metadata.
- Evaluation workflow gebruikt chronologische splits en rapporteert fold/backtest metrics.
- Data quality/drift summary bestaat en beïnvloedt runtime health.
- Dashboard gebruikt verbeterde refresh en toont microstructure, sessions en modelops.
- Alle tests, security scan en browsercheck slagen.
- Roadmap 003 daarna naar `Voltooid docs/` wordt verplaatst.

## 9. Verwachte volgende roadmap na Roadmap 003

Roadmap 004 zou daarna logisch focussen op:

- testnet user-data stream en execution reconciliation;
- langdurige paper trading sessions;
- alerting/notificaties;
- uitgebreidere modeltraining met PyTorch state_dict checkpoints;
- eventueel MLflow-integratie wanneer de lichte model registry niet meer genoeg is.
