# Roadmap 001 - Neural Network Binance Spot AI Trading Bot

Status: Voltooid  
Project: Neural network Binance spot  
Doelomgeving: Binance.com Spot + Spot Testnet  
Aanpak: paper/testnet-first, supervised neural network als signaalgenerator, deterministische risk engine voor alle handelsbeslissingen  
Belangrijk: dit document is technische planning en geen financieel advies of winstgarantie.

## 1. Doel en succescriteria

Het doel is een production-minded AI spot trading bot te bouwen die Binance.com spot market data gebruikt, eerst volledig offline en in paper/testnet draait, en pas later onder strikte gates echte orders mag plaatsen.

De bot moet niet vertrouwen op een LLM of neural network als autonome beslisser. Het neural network voorspelt alleen een signaal, confidence en horizon. Een deterministische risk engine beslist daarna of een trade toegestaan is, hoe groot die mag zijn, en wanneer trading volledig geblokkeerd wordt.

Succes betekent:

- Historische data kan betrouwbaar verzameld, opgeslagen en herhaald verwerkt worden.
- Features worden zonder look-ahead leakage gebouwd.
- Een baseline model en neural network kunnen reproduceerbaar getraind en geevalueerd worden.
- Backtests verwerken fees, slippage, spread, orderfilters en positieboekhouding.
- Paper trading draait stabiel met order reconciliation, kill switch, rate-limit handling en audit logs.
- Spot Testnet wordt gebruikt voor technische orderflow-validatie voordat live trading zelfs overwogen wordt.
- Live trading blijft geblokkeerd totdat expliciete live-readiness criteria zijn gehaald.

## 2. Onderzoeksconclusies

### Binance Spot API

Belangrijke officiele bronnen:

- Binance Spot API documentatie: https://github.com/binance/binance-spot-api-docs
- Spot REST API: https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/rest-api.md
- Spot Testnet: https://testnet.binance.vision/
- Spot filters: https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/filters.md
- Spot WebSocket streams: https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/web-socket-streams.md

Belangrijke API-conclusies:

- Gebruik `/api/v3/exchangeInfo` als bron voor trading rules, filters, symbol status, tick size, step size, min notional en orderlimieten.
- Iedere order moet vooraf lokaal gevalideerd worden tegen Binance filters, niet pas na een API rejection.
- Signed endpoints vereisen timestamp, signature en geldige API key permissions.
- `recvWindow` moet klein blijven, standaard maximaal 5000 ms tenzij er een concrete reden is.
- HTTP 429 betekent backoff; herhaald negeren kan leiden tot IP-ban via HTTP 418.
- HTTP 5xx of timeout bij orders mag niet blind als "failed" behandeld worden. Orderstatus moet via user data stream of query endpoint gereconcilieerd worden.
- Spot Testnet is geschikt voor technische orderflow, maar niet voor realistische liquiditeit, marktimpact of winstverwachting.

### OpenAI en AI-gebruik

Belangrijke bronnen:

- OpenAI models: https://developers.openai.com/api/docs/models
- Responses API: https://developers.openai.com/api/reference/responses
- Function calling: https://developers.openai.com/api/docs/guides/function-calling
- Structured outputs: https://developers.openai.com/api/docs/guides/structured-outputs
- Evals: https://developers.openai.com/api/docs/guides/evals

OpenAI kan later nuttig zijn voor analyse, rapportage, anomalie-uitleg, experimentnotities of structured decision reviews. OpenAI mag in deze roadmap niet de live orderbeslisser worden.

Voor eventuele LLM-onderdelen gelden harde regels:

- Gebruik structured outputs of strict function schemas.
- Laat LLM-output nooit direct orders plaatsen.
- Log model, promptversie, inputcontext, output en validatieresultaat.
- Gebruik evals voordat prompts of modellen in operationele flows worden gewijzigd.

### Security

Belangrijke bronnen:

- OWASP API Security Top 10: https://owasp.org/API-Security/editions/2023/en/0x10-api-security-risks/
- OWASP Secrets Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

Security-conclusies:

- API keys en secrets mogen nooit in Git, logs, screenshots of roadmapdocs staan.
- Gebruik aparte keys per doel: market/user-data/trade. Gebruik de laagste permissies die praktisch werken.
- Withdrawal-permissies moeten uitgeschakeld blijven.
- IP-restricties moeten aan staan waar Binance dit ondersteunt.
- Alle externe API-responses worden als onbetrouwbaar behandeld tot parsing, schema-checks en range-checks zijn uitgevoerd.
- Rate limiting, retry policy en circuit breakers zijn security- en reliability-eisen, geen optimalisaties.

### Financial ML en backtesting

Belangrijke researchthema's:

- Backtest overfitting is een primaire faalmodus bij trading ML.
- Look-ahead bias ontstaat snel bij indicators, labels, rolling windows, resampling en train/test splits.
- Crypto returns hebben veel noise, regime shifts, fat tails en exchange-specifieke microstructure.
- Een winstgevende backtest zonder fees, slippage en spread is niet bruikbaar.
- Reinforcement learning is niet geschikt voor MVP door extra complexiteit in simulator, reward design en overfittingcontrole.

MVP-keuze:

- Start met supervised learning voor korte horizon directional/return/risk labels.
- Vergelijk NN altijd tegen simpele baselines, zoals buy-and-hold, moving average, momentum, mean reversion en no-trade.
- Model-output is alleen een input voor de risk engine.

## 3. Kernarchitectuur

De eerste echte codebase moet modulair worden opgezet rond duidelijke grenzen.

### 3.1 ExchangeAdapter

Verantwoordelijkheid:

- Binance.com Spot REST en WebSocket integratie.
- Spot Testnet support via config.
- Market data ophalen.
- Account state lezen.
- Test orders uitvoeren.
- Orders plaatsen, annuleren en queryen, later pas voor live.
- Exchange filters ophalen en cachen.
- Server time sync en signed request signing.

Minimale interface:

```text
ExchangeAdapter
- get_exchange_info(symbols)
- get_klines(symbol, interval, start_time, end_time, limit)
- get_order_book(symbol, depth)
- get_account_state()
- test_order(order_request)
- place_order(order_request)
- cancel_order(symbol, order_id)
- get_order(symbol, order_id)
- stream_market_data(symbols, streams)
- stream_user_data()
```

Niet toegestaan in MVP:

- Margin trading.
- Futures trading.
- Withdrawals.
- Cross-exchange routing.
- Autonomous live trading.

### 3.2 DataStore

Verantwoordelijkheid:

- Raw Binance responses onveranderd bewaren.
- Genormaliseerde OHLCV, trades en orderbook snapshots opslaan.
- Feature datasets versioneren.
- Modeltraining reproduceerbaar maken.

Aanbevolen start:

- Lokale file-based opslag voor MVP: `data/raw`, `data/processed`, `data/features`.
- Parquet voor tijdreeksen zodra Python stack aanwezig is.
- SQLite of DuckDB voor metadata, runs, datasets en audit queries.

Minimale datasets:

- Raw klines per symbol/interval.
- Processed candles met UTC timestamps.
- Feature matrix met datasetversie.
- Label dataset met horizon en labeldefinitie.
- Backtest result sets.
- Paper trading audit events.

### 3.3 Feature Pipeline

Verantwoordelijkheid:

- Deterministische features maken uit historische data.
- Feature definitions versioneren.
- Geen toekomstige informatie lekken.
- Alle rolling features alleen berekenen met informatie tot en met het beslismoment.

Startfeatures:

- Returns over meerdere horizons.
- Rolling volatility.
- Volume z-score.
- Spread proxy uit best bid/ask waar beschikbaar.
- Candle body/wick ratios.
- Trend indicators met alleen historische windows.
- Time features in UTC.

Verboden zonder expliciete validatie:

- Features die toekomstige candles gebruiken.
- Normalisatie over de volledige dataset voor train/test split.
- Labels of target returns die per ongeluk in features belanden.
- Survivorship-style selectie van alleen winnaars of recente populaire symbols.

### 3.4 SignalModel

Verantwoordelijkheid:

- Feature vector naar gestructureerd trading signal.
- Modelversies vastleggen.
- Confidence kalibreren.

Minimale output:

```json
{
  "signal": "BUY|SELL|HOLD",
  "confidence": 0.0,
  "horizon": "string",
  "model_version": "string"
}
```

MVP-modellen:

1. No-trade baseline.
2. Simple rules baseline.
3. Logistic regression of gradient boosting baseline.
4. Kleine neural network classifier/regressor.

Eerste neural network:

- Compact MLP of 1D temporal model.
- Geen grote transformer in MVP.
- Early stopping.
- Chronologische splits.
- Reproduceerbare seed.
- Model registry metadata.

### 3.5 RiskEngine

Verantwoordelijkheid:

- Alle trade-intenties toestaan of blokkeren.
- Positiegrootte bepalen.
- Max loss, max exposure, max trades en cooldowns afdwingen.
- Kill switch afdwingen.

Input:

- SignalModel output.
- Account state.
- Current exposure.
- Exchange filters.
- Market state.
- Configured risk limits.

Output:

```json
{
  "decision": "ALLOW|BLOCK",
  "reason": "string",
  "intent": {
    "symbol": "BTCUSDT",
    "side": "BUY|SELL",
    "quote_size": "decimal",
    "order_type": "MARKET|LIMIT",
    "max_slippage_bps": "decimal"
  }
}
```

MVP risk rules:

- Default mode is no-trade.
- Per-symbol max quote exposure.
- Daily max loss.
- Max number of trades per day.
- Min confidence threshold.
- Cooldown after loss streak.
- Block trading on stale data.
- Block trading on missing exchange filters.
- Block trading when spread/slippage proxy exceeds threshold.
- Emergency kill switch via local config/env flag.

### 3.6 ExecutionEngine

Verantwoordelijkheid:

- Risk-approved trade intent omzetten naar Binance-compliant order requests.
- Decimal rounding correct uitvoeren op tick size en step size.
- Idempotency/client order IDs beheren.
- Order lifecycle volgen.

MVP-volgorde:

1. Dry run execution.
2. Paper execution met gesimuleerde fills.
3. Spot Testnet test order.
4. Spot Testnet echte testnet order.
5. Live order pas na live-readiness gate.

Belangrijke orderregels:

- Valideer `PRICE_FILTER`, `LOT_SIZE`, `MARKET_LOT_SIZE`, `NOTIONAL` en ordercount-limieten.
- Gebruik Decimal, geen floating point voor order quantities/prices.
- Bij timeout of 5xx: status unknown, dus query/reconcile voordat opnieuw geplaatst wordt.
- Geen retry die dubbele orders kan veroorzaken.

### 3.7 AuditLog

Verantwoordelijkheid:

- Iedere beslissing en order lifecycle immutable vastleggen.
- Debugging, compliance en post-mortem analyse mogelijk maken.

Minimale events:

- Data fetch started/completed/failed.
- Feature dataset built.
- Model trained.
- Backtest run completed.
- Signal generated.
- Risk decision made.
- Order intent created.
- Test order accepted/rejected.
- Order placed/canceled/filled/reconciled.
- Kill switch changed.
- Config changed.

Audit event moet bevatten:

- Timestamp UTC.
- Component.
- Correlation ID.
- Symbol.
- Model version.
- Dataset version.
- Risk config version.
- Decision.
- Reason.
- Sanitized payload zonder secrets.

### 3.8 Monitoring

Verantwoordelijkheid:

- Runtime health zichtbaar maken.
- Paper/live afwijkingen detecteren.
- Bot stilleggen bij gevaarlijke condities.

MVP-metrics:

- Data freshness.
- API request count en rate-limit usage.
- Error rate per endpoint.
- Signal distribution.
- Block reasons.
- Paper PnL.
- Drawdown.
- Exposure.
- Open orders.
- Reconciliation failures.

Alerts:

- Stale market data.
- API 429/418.
- Order status unknown te lang.
- Daily max loss bereikt.
- Kill switch actief.
- Unexpected live trading mode.

## 4. Gefaseerde roadmap

### Fase 0 - Projectbasis en guardrails

Doel: repo klaarzetten zonder tradingrisico.

Taken:

- Kies Python als primaire taal voor data, ML en Binance integratie.
- Maak basisstructuur voor `src`, `tests`, `docs`, `data`, `configs`.
- Voeg `.env.example` toe zonder echte secrets.
- Voeg `.gitignore` toe voor `.env`, data dumps, model artifacts en logs.
- Definieer configprofielen: `local`, `paper`, `testnet`, `live-disabled`.
- Zet live trading standaard hard uit.
- Voeg secret scanning en basis lint/test commands toe.

Acceptatiecriteria:

- Repo bevat geen echte API keys.
- Live trading kan niet per ongeluk aan staan.
- Config laadt zonder secrets.
- Tests draaien minimaal voor config-validatie.

### Fase 1 - Binance market data collector

Doel: betrouwbare historische en actuele market data verzamelen.

Taken:

- Implementeer `ExchangeAdapter` read-only endpoints.
- Haal `/api/v3/exchangeInfo` op en parse symbol filters.
- Download klines voor geselecteerde symbols en intervals.
- Sla raw responses en processed candles op.
- Voeg rate-limit aware request wrapper toe.
- Voeg retry met exponential backoff toe voor read-only requests.

Startsymbolen:

- `BTCUSDT`
- `ETHUSDT`
- Eventueel later top-volume USDT spot pairs, pas na validatie.

Acceptatiecriteria:

- Kline data kan herhaald worden opgehaald zonder duplicaten.
- Timestamps zijn UTC en chronologisch.
- Exchange filters worden opgeslagen met versie/timestamp.
- 429 leidt tot backoff, niet tot spam.

### Fase 2 - Dataset en feature pipeline

Doel: reproduceerbare ML dataset zonder leakage.

Taken:

- Bouw candle normalization.
- Bouw feature generator met rolling windows.
- Bouw label generator voor vaste horizons.
- Maak chronologische train/validation/test split.
- Log datasetversie en featureconfig.
- Voeg leakage checks toe.

Acceptatiecriteria:

- Iedere feature gebruikt alleen data die op dat moment beschikbaar was.
- Normalisatie wordt alleen op train fit en daarna op validation/test toegepast.
- Dataset rebuild met dezelfde inputs geeft dezelfde output.
- Testset blijft volledig out-of-sample.

### Fase 3 - Baselines en modeltraining

Doel: aantonen of het neural network iets toevoegt boven simpele strategieen.

Taken:

- Implementeer no-trade baseline.
- Implementeer buy-and-hold benchmark.
- Implementeer eenvoudige rule-based baseline.
- Train een klassieke ML baseline.
- Train eerste compacte neural network.
- Leg alle modelruns vast met datasetversie, parameters en metrics.

Acceptatiecriteria:

- NN wordt alleen geaccepteerd als het out-of-sample beter is dan relevante baselines.
- Metrics bevatten niet alleen accuracy, maar ook precision/recall per action, calibration, expected value en turnover.
- Slechte of onzekere modellen leiden tot HOLD/no-trade default.

### Fase 4 - Backtest engine

Doel: strategie realistisch toetsen voordat er paper/testnet wordt gedraaid.

Taken:

- Bouw event-driven backtester.
- Verwerk fees, slippage, spread en min notional.
- Simuleer position accounting.
- Simuleer order rejection door filters.
- Voeg walk-forward evaluation toe.
- Voeg rapportage toe voor PnL, Sharpe-like metrics, max drawdown, hit rate, turnover en exposure.

Acceptatiecriteria:

- Fees en slippage staan standaard aan.
- Geen trade kan exchange filters negeren.
- Backtest faalt hard bij ontbrekende data of niet-monotone timestamps.
- Rapport toont baselinevergelijking en drawdowns.
- Overfit-indicatoren en out-of-sample resultaten staan apart van trainresultaten.

### Fase 5 - Paper trader

Doel: live market data gebruiken zonder echte orders.

Taken:

- Bouw paper execution engine.
- Gebruik actuele market data en gesimuleerde fills.
- Koppel SignalModel, RiskEngine en AuditLog.
- Voeg runtime loop toe met duidelijke intervallen.
- Voeg kill switch toe.
- Voeg daily max loss en max exposure toe.
- Voeg dashboard/lograpport toe.

Acceptatiecriteria:

- Paper trader draait minimaal meerdere sessies zonder crash.
- Alle beslissingen zijn traceerbaar in AuditLog.
- RiskEngine blokkeert trades bij stale data, lage confidence, max loss en kill switch.
- Paper PnL en exposure worden correct bijgehouden.

### Fase 6 - Spot Testnet orderflow

Doel: Binance signed endpoints technisch valideren zonder echt kapitaal.

Taken:

- Voeg signed request signing toe.
- Voeg server time sync toe.
- Voeg test order support toe.
- Voeg Spot Testnet config toe.
- Plaats alleen testnet orders met kleine testnet sizes.
- Implementeer order query en reconciliation.

Acceptatiecriteria:

- API keys komen alleen uit environment of secret manager.
- Withdrawal permissions blijven uit.
- Test order endpoint werkt.
- Testnet order lifecycle wordt volledig gelogd.
- Timeout/status unknown wordt gereconcilieerd voordat nieuwe orderpoging volgt.

### Fase 7 - Security hardening

Doel: voorkomen dat bugs of leaks financieel schadelijk worden.

Taken:

- Secret scan in lokale checks.
- Logging scrubber voor API keys, signatures en headers.
- Config validation voor live mode.
- Trade permission checks bij startup.
- IP allowlist documenteren.
- Incident runbook schrijven.
- Dependency vulnerability scan toevoegen.

Acceptatiecriteria:

- Geen secretachtige waarden in logs of repo.
- Live mode vereist expliciete meerstapsconfig en blijft standaard disabled.
- Bot stopt bij ontbrekende security controls.
- Incident runbook beschrijft kill switch, key revocation en order cancellation.

### Fase 8 - Observability en operations

Doel: botgedrag operationeel begrijpelijk maken.

Taken:

- Structured logs.
- Metrics export.
- Health checks.
- Dagelijks performance report.
- Model drift checks.
- Data quality checks.
- Alerting voor kritieke failures.

Acceptatiecriteria:

- Operator kan zien waarom trades wel/niet genomen zijn.
- Reconciliation failures zijn zichtbaar.
- Stale data en API-ban risico's geven alerts.
- Modelversie en configversie zijn zichtbaar in rapporten.

### Fase 9 - Live-readiness gate

Doel: bepalen of een kleine live pilot verantwoord is.

Live trading mag pas gepland worden als alle onderstaande punten waar zijn:

- Backtests zijn out-of-sample positief na fees/slippage.
- Paper trading is stabiel over een vooraf afgesproken periode.
- Testnet orderflow is betrouwbaar.
- Kill switch is getest.
- Daily max loss werkt.
- Order reconciliation werkt.
- Secret handling is gevalideerd.
- Withdrawal permissions zijn uit.
- API key permissions zijn minimaal.
- Position sizing is klein en begrensd.
- Er is handmatige goedkeuring voor live mode.

Live pilot defaultlimieten:

- Een symbol tegelijk.
- Kleine quote exposure.
- Max aantal trades per dag.
- Max daily loss.
- Alleen spot.
- Geen leverage.
- Geen margin.
- Geen withdrawals.

## 5. Belangrijke risico's en mitigaties

### Financieel risico

Risico:

- Model lijkt winstgevend in backtest maar faalt live.

Mitigatie:

- Paper/testnet-first.
- Out-of-sample en walk-forward testing.
- Fees/slippage/spread verplicht.
- No-trade default.
- Kleine positiegrenzen.

### Look-ahead leakage

Risico:

- Features bevatten toekomstige informatie.

Mitigatie:

- Chronologische splits.
- Rolling features alleen op historische windows.
- Tests voor feature timestamps.
- Label/feature scheiding.

### Overfitting

Risico:

- NN leert ruis of specifieke marktfase.

Mitigatie:

- Baselinevergelijking.
- Simpele modellen eerst.
- Early stopping.
- Walk-forward evaluation.
- Modelacceptatie alleen op out-of-sample gedrag.

### API/rate-limit risico

Risico:

- Bot spamt API, krijgt 429/418, of mist status bij timeout.

Mitigatie:

- Request budget tracking.
- Backoff op 429.
- Circuit breaker.
- Order reconciliation.
- Geen blind retry op unknown order status.

### Secret leakage

Risico:

- API keys lekken via repo, logs of screenshots.

Mitigatie:

- `.env` genegeerd.
- `.env.example` zonder echte waarden.
- Secret scanning.
- Log scrubber.
- Key rotation runbook.

### Autonome AI-beslissingen

Risico:

- AI plaatst of adviseert trades buiten harde regels.

Mitigatie:

- NN geeft alleen signalen.
- RiskEngine is deterministisch.
- ExecutionEngine accepteert alleen risk-approved intents.
- LLM's mogen geen live orders sturen.

## 6. Eerste technische stack

Aanbevolen startstack:

- Python 3.12+
- pandas, numpy, pyarrow
- scikit-learn voor baselines
- PyTorch voor neural network
- pydantic voor config en schemas
- httpx of aiohttp voor REST
- websockets voor streams
- DuckDB of SQLite voor metadata
- pytest voor tests
- ruff voor lint/format checks

Reden:

- Python is sterk voor quant research en ML.
- PyTorch geeft controle zonder te veel framework lock-in.
- DuckDB/Parquet werkt goed voor lokale tijdreeksontwikkeling.
- Pydantic helpt om externe API-data en interne beslisobjecten strikt te valideren.

## 7. Configuratiebeleid

Config moet expliciet en fail-closed zijn.

Voorbeelden van configvelden:

```text
APP_ENV=local|paper|testnet|live
BINANCE_BASE_URL=https://api.binance.com
BINANCE_TESTNET_BASE_URL=https://testnet.binance.vision
TRADING_MODE=disabled|paper|testnet|live
LIVE_TRADING_ENABLED=false
KILL_SWITCH=true
MAX_DAILY_LOSS_QUOTE=0
MAX_POSITION_QUOTE=0
MAX_TRADES_PER_DAY=0
```

Live mode vereist later minimaal:

- `APP_ENV=live`
- `TRADING_MODE=live`
- `LIVE_TRADING_ENABLED=true`
- `KILL_SWITCH=false`
- expliciete risk limits groter dan 0
- expliciete manual approval marker

Tot die tijd moet live mode hard falen.

## 8. Definition of done per roadmap

Een roadmap is pas volledig afgewerkt als:

- Alle geplande taken uitgevoerd zijn.
- Tests en checks uitgevoerd zijn.
- Acceptatiecriteria aantoonbaar gehaald zijn.
- Eventuele afwijkingen gedocumenteerd zijn.
- De volgende roadmap kan voortbouwen op concrete uitkomsten.

Pas daarna wordt het roadmapbestand verplaatst van:

```text
Roadmap docs/
```

naar:

```text
Voltooid docs/
```

Deze roadmap is afgewerkt: de veilige projectbasis, Binance-adapter, dataset/feature pipeline, modelbaseline, tiny neural network, backtester, paper/testnet execution flow, risk controls, auditlog, monitoring, security runbook, live-readiness checklist en lokale tests zijn toegevoegd en gevalideerd.

## 9. Volgende roadmap na afronding

De volgende roadmap moet waarschijnlijk starten met:

- Project scaffold.
- Python dependency setup.
- Config model.
- `.env.example`.
- Binance read-only market data adapter.
- Tests voor config, symbols en exchange filters.

De volgende roadmap moet voortbouwen op de keuzes in dit document:

- Binance.com Spot.
- Spot Testnet voor technische orderflow.
- Paper/testnet-first.
- Supervised NN als signaalgenerator.
- Deterministische RiskEngine.
- Geen live trading in MVP.
