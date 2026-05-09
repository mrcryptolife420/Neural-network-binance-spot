# Roadmap 002 - Lokale visuele paper bot dashboard

Status: Voltooid  
Volgt op: `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`  
Doel: de bestaande veilige bot-infrastructuur lokaal startbaar en visueel observeerbaar maken, zonder bestaande modules dubbel te bouwen.  
Belangrijk: live trading blijft buiten scope en blijft geblokkeerd.

## 1. Samenvatting

Roadmap 001 leverde de veilige kern op: config guardrails, Binance adapter, datastore, feature pipeline, signal models, risk engine, execution engine, backtester, paper trader, auditlog, monitoring en tests.

Roadmap 002 bouwt hierop verder met een lokale operator-ervaring:

- een enkele lokale startflow waarmee de gebruiker de bot direct kan starten;
- een visueel dashboard in de browser;
- demo replay zonder API keys;
- paper mode met bestaande paper/risk/execution modules;
- optionele read-only Binance market data;
- zichtbare candles, signalen, risk decisions, paper fills, PnL, auditlog en health status.

De kernkeuze is: gebruik Streamlit + Plotly voor de eerste lokale UI. Dit voorkomt een dubbele backend/frontend-architectuur en past bij de bestaande Python-codebase. FastAPI/WebSockets blijven een latere optie als multi-client of production API nodig wordt.

## 2. Research en ontwerpkeuzes

### Bronnen

- Streamlit lokale start: https://docs.streamlit.io/develop/concepts/architecture/run-your-app
- Streamlit CLI: https://docs.streamlit.io/develop/api-reference/cli/run
- Plotly candlestick charts: https://plotly.com/python-api-reference/generated/plotly.graph_objects.Candlestick.html
- FastAPI WebSockets: https://fastapi.tiangolo.com/advanced/websockets/
- Binance Spot WebSocket Streams: https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/web-socket-streams.md

### Conclusies

- Streamlit is geschikt voor een eerste lokale operator UI omdat `streamlit run` direct een lokale server start en de app in een browser opent.
- Plotly ondersteunt candlestick charts met open/high/low/close en is geschikt om signal markers en paper fills op dezelfde grafiek te tonen.
- Binance WebSocket streams zijn nuttig voor latere realtime market data; voor Roadmap 002 is een replay-loop plus optionele REST-refresh genoeg om snel visueel resultaat te leveren.
- FastAPI WebSockets zijn nuttig voor latere scheiding tussen bot runtime en UI, maar zouden nu extra backend/frontend-complexiteit toevoegen. Niet bouwen in deze roadmap tenzij Streamlit de acceptatiecriteria niet kan halen.

## 3. Niet dubbel bouwen

Gebruik bestaande onderdelen:

- `BotSettings` voor alle mode- en safety-config.
- `DataStore` voor demo datasets en lokale output.
- `build_feature_rows` en `build_label_rows` voor feature/label generatie.
- `RuleBasedSignalModel` en `TinyNeuralSignalModel` voor eerste signalen.
- `RiskEngine` en `RiskLimits` voor alle trade decisions.
- `ExecutionEngine` voor paper fills.
- `PaperTrader` voor step-based runtime.
- `AuditLog` voor alle events.
- `RuntimeMetrics` voor health en status.
- `BinanceSpotAdapter` alleen voor read-only market data of explicit testnet checks.

Nieuwe code mag alleen orchestration, UI en kleine adapterlagen toevoegen. Bestaande businesslogica niet kopieren naar de UI.

## 4. Gewenste lokale startflow

Na implementatie moet de gebruiker vanuit de projectroot kunnen draaien:

```powershell
$env:PYTHONPATH="src"
python -m binance_spot_bot.local_run --mode demo --symbol BTCUSDT --interval 1m
```

Voor visuele modus:

```powershell
$env:PYTHONPATH="src"
python -m streamlit run src/binance_spot_bot/ui/streamlit_app.py -- --mode demo --symbol BTCUSDT --interval 1m
```

De dashboardflow moet zonder API keys werken in `demo` mode.

Optionele paper market-data mode:

```powershell
$env:PYTHONPATH="src"
python -m streamlit run src/binance_spot_bot/ui/streamlit_app.py -- --mode paper --symbol BTCUSDT --interval 1m
```

Regels:

- `demo` gebruikt lokale of synthetische candles en plaatst nooit externe requests.
- `paper` mag read-only market data ophalen, maar plaatst geen echte orders.
- `testnet` mag alleen testnet-safe acties tonen en gebruikt bestaande `ExecutionEngine` test-order guardrails.
- `live` wordt niet beschikbaar gemaakt in de UI.

## 5. Implementatieplan

### Fase 0 - Dependency en projectintegratie

Doel: UI-dependencies toevoegen zonder bestaande kern onnodig zwaar te maken.

Taken:

- Voeg optionele dependency group `ui` toe aan `pyproject.toml`:
  - `streamlit`
  - `plotly`
- Houd kernpackage zonder verplichte UI-dependencies bruikbaar.
- Update README met exacte lokale startcommando's.
- Voeg `docs/local-dashboard.md` toe met setup, modes, controls en troubleshooting.

Acceptatiecriteria:

- Unit tests blijven draaien zonder UI-dependencies.
- UI-installatie is expliciet: `pip install -e ".[ui]"`.
- README noemt demo mode als veiligste eerste start.

### Fase 1 - Bot runtime supervisor

Doel: een herbruikbare runtime-laag maken die CLI en UI kunnen gebruiken.

Nieuwe module:

```text
src/binance_spot_bot/runtime.py
```

Nieuwe verantwoordelijkheden:

- Runtime state beheren.
- Candles als stream/replay aanbieden.
- Per tick bestaande feature/model/risk/execution flow aanroepen.
- Metrics en audit events bijwerken.
- Stop/start/pause state beheren.

Minimale interfaces:

```text
BotRuntime
- start()
- stop()
- step()
- run_steps(count)
- snapshot()

RuntimeSnapshot
- mode
- symbol
- interval
- current_candle
- latest_signal
- latest_risk_decision
- latest_execution_result
- equity
- paper_position
- metrics
- audit_tail
```

Belangrijk:

- `BotRuntime` mag geen risk rules dupliceren.
- Iedere tick gebruikt bestaande `PaperTrader` of dezelfde componentketen.
- Bij ontbrekende candles of features moet runtime duidelijk `waiting_for_data` tonen.

Acceptatiecriteria:

- Runtime kan 50 demo ticks draaien zonder API keys.
- Runtime snapshot bevat genoeg data voor UI-rendering.
- Runtime stopt netjes zonder halfgeschreven audit events.

### Fase 2 - Demo data en replay engine

Doel: de gebruiker kan de bot meteen visueel zien werken zonder Binance credentials.

Taken:

- Voeg `DemoMarketReplay` toe die synthetische maar realistische candles maakt of bestaande demo candles uit `data/` gebruikt.
- Maak replay-snelheid instelbaar: 1x, 5x, 10x, step-by-step.
- Voeg trend/regime scenario's toe:
  - sideways
  - uptrend
  - downtrend
  - volatile
- Bewaar demo-output in `data/audit/` en `data/features/`, maar voorkom dat grote generated data in Git belandt.

Acceptatiecriteria:

- Dashboard toont binnen 10 seconden bewegende candles/signalen in demo mode.
- Geen API keys of internetverbinding nodig.
- Replay is reproduceerbaar met seed.

### Fase 3 - Streamlit dashboard

Doel: visuele lokale operator UI.

Nieuwe files:

```text
src/binance_spot_bot/ui/streamlit_app.py
src/binance_spot_bot/ui/charts.py
src/binance_spot_bot/ui/state.py
```

Dashboard layout:

- Bovenbalk:
  - mode
  - symbol
  - interval
  - kill switch status
  - runtime status
  - last update timestamp
- Linker sidebar:
  - mode selector: demo, paper, testnet-readiness
  - symbol selector
  - interval selector
  - replay speed
  - risk limit inputs
  - start/pause/step/reset controls
- Hoofdscherm:
  - candlestick chart
  - signal markers
  - paper buy/sell/fill markers
  - equity/PnL chart
  - exposure chart
- Onderste panels:
  - latest signal
  - latest risk decision
  - block reason counts
  - audit tail
  - health metrics

Visuele regels:

- Geen decoratieve landing page.
- Dashboard is direct de eerste view.
- Gebruik compacte operationele layout, geen marketing hero.
- UI moet duidelijk tonen dat `live` niet actief is.
- Risk blocks moeten zichtbaar zijn, niet verborgen in logs.

Acceptatiecriteria:

- `python -m streamlit run ... -- --mode demo` opent lokaal en toont bewegende botstatus.
- Candles, signalen, decisions en paper fills zijn zichtbaar.
- UI kan pauzeren, single-step uitvoeren en resetten.
- Live mode is niet selecteerbaar.

### Fase 4 - CLI startcommand en lokale scripts

Doel: naast Streamlit ook een simpele terminal-startflow.

Taken:

- Voeg CLI command toe:

```powershell
python -m binance_spot_bot.cli run-local --mode demo --symbol BTCUSDT --steps 100
```

- Voeg CLI command toe:

```powershell
python -m binance_spot_bot.cli dashboard --mode demo
```

`dashboard` mag intern het juiste Streamlit commando printen of starten, afhankelijk van wat het veiligst werkt op Windows.

Acceptatiecriteria:

- `run-local` schrijft audit events en runtime summary.
- `dashboard` geeft een exact bruikbaar commando als automatisch starten niet betrouwbaar is.
- Bestaande CLI commands blijven werken:
  - `validate-config`
  - `security-scan`
  - `demo-backtest`

### Fase 5 - Read-only Binance market data mode

Doel: de bot visueel op echte marktdata kunnen bekijken zonder orderrisico.

Taken:

- Voeg read-only data refresh toe via bestaande `BinanceSpotAdapter.get_klines`.
- Cache opgehaalde candles via `DataStore`.
- Toon duidelijk verschil tussen:
  - demo replay
  - real market data paper simulation
  - testnet technical orderflow
- Voeg rate-limit backoff en UI-status toe.

Acceptatiecriteria:

- Paper mode kan BTCUSDT candles ophalen en visueel tonen.
- Als Binance niet bereikbaar is, valt UI terug naar duidelijke error state en stopt niet hard.
- Geen signed endpoint nodig voor read-only paper market data.

### Fase 6 - Testnet readiness panel

Doel: veilig zichtbaar maken wat nog ontbreekt voor Spot Testnet zonder echte live exposure.

Taken:

- Toon checklist:
  - API key aanwezig
  - secret aanwezig
  - mode is testnet
  - live disabled
  - kill switch status
  - max limits ingesteld
- Voeg een knop of CLI-pad voor `test_order` toe, maar alleen als alle testnet prechecks slagen.
- Testnet acties moeten bestaande `ExecutionEngine` en `BinanceSpotAdapter.test_order` gebruiken.

Acceptatiecriteria:

- Zonder credentials toont UI duidelijke missing-prechecks.
- Met testnet credentials kan alleen Binance test order endpoint gebruikt worden.
- Geen echte live orderroute in dashboard.

### Fase 7 - Tests en visuele verificatie

Doel: aantonen dat de lokale startflow werkt.

Taken:

- Unit tests voor `BotRuntime`.
- Unit tests voor demo replay determinisme.
- Unit tests dat UI mode list geen `live` bevat.
- CLI tests voor `run-local`.
- Security scan blijft groen.
- Optioneel Playwright/browser-verificatie na dashboardimplementatie:
  - open localhost Streamlit URL;
  - controleer dat status, chart container en audit panel zichtbaar zijn.

Acceptatiecriteria:

- `python -m unittest discover -s tests` blijft groen.
- `python -m binance_spot_bot.cli run-local --mode demo --steps 20` werkt zonder API keys.
- Dashboard start lokaal in demo mode.
- Roadmap 002 wordt pas verplaatst naar `Voltooid docs/` wanneer dit allemaal werkt.

## 6. Belangrijke UX details

Dashboard moet operationeel en scanbaar zijn:

- Statuskleur voor running/paused/error.
- Duidelijke tekst: `LIVE TRADING DISABLED`.
- Laatste signal:
  - side
  - confidence
  - model version
- Laatste risk decision:
  - ALLOW/BLOCK
  - reason
- Paper execution:
  - side
  - quantity
  - paper fill price
- Audit tail:
  - timestamp
  - component
  - event
  - reason

Niet doen:

- Geen winstbeloftes.
- Geen echte live orderknop.
- Geen duplicatie van risk logic in Streamlit.
- Geen API secrets tonen of loggen.

## 7. Definition of done

Roadmap 002 is volledig afgerond:

- UI dependency group bestaat.
- Lokale demo-runtime werkt zonder API keys.
- Streamlit dashboard start lokaal en toont visueel botactiviteit.
- Paper mode kan read-only Binance candles tonen of netjes falen bij netwerk/API-problemen.
- Runtime gebruikt bestaande infrastructuur uit Roadmap 001.
- Tests en security scan slagen.
- README en `docs/local-dashboard.md` bevatten exacte startinstructies.
- `002-roadmap-local-visual-paper-bot-dashboard.md` wordt na deze statusupdate naar `Voltooid docs/` verplaatst.

## 8. Verwachte volgende roadmap

Na Roadmap 002 is de logische volgende roadmap:

- echte Binance WebSocket market data integratie;
- robuust local order book management;
- betere model training pipeline met saved model registry;
- operator alerts;
- langere paper-trading sessies met rapportage.

Die volgende roadmap moet opnieuw voortbouwen op de bestaande runtime en dashboardlaag, zonder modules te dupliceren.
