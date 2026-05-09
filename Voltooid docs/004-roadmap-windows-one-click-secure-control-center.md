# Roadmap 004: Windows One-Click Secure Bot Control Center

Status: Voltooid  
Volgt op:
- `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
- `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
- `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`

Doel: de bestaande veilige Binance Spot bot uitbreiden tot een Windows 11 control center dat met 1 klik start, automatisch het lokale dashboard opent, veilig credentials kan invoeren voor demo/testnet, duidelijk toont welke Binance-modus actief is, en meer bot-instellingen vanuit de frontend laat aanpassen. Live trading blijft buiten scope.

Belangrijk: niets dubbel bouwen. Hergebruik `BotRuntime`, `BotSettings`, `BinanceSpotAdapter`, `MarketDataSource`, `RiskEngine`, `ExecutionEngine`, `SessionStore`, `ModelRegistry`, `DataQualityReport`, Streamlit dashboard, CLI en bestaande PowerShell-helper.

Voltooiingsnotitie:
- Windows one-click launcher toegevoegd: `Start Bot Dashboard.cmd`, `Stop Bot Dashboard.cmd`, `scripts/start-dashboard.ps1`, `scripts/stop-dashboard.ps1`, `scripts/check-local-env.ps1`.
- Exchange profiles, session-only credential handling, Windows SecretManagement adapter, connectivity checks, settings persistence, user-data parsers en order lifecycle store toegevoegd.
- Dashboard is omgebouwd naar een control center met profile/mode badges, credential entry, bot controls, risk controls, model/evaluation, market data, orders/account, sessions en security tabs.
- `BINANCE_API_BASE_URL` alias en profile-aware active base URL toegevoegd.
- Secret redaction en security scan uitgebreid voor scripts/docs/settings/logs.
- Verificatie uitgevoerd: unit tests, security scan, config validation en browsercheck.

## Researchbronnen

- Binance Spot REST API docs: https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/rest-api.md
- Binance Spot WebSocket Streams: https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/web-socket-streams.md
- Binance User Data Streams: https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/user-data-stream.md
- Binance Spot Testnet: https://testnet.binance.vision/
- Streamlit `st.secrets`: https://docs.streamlit.io/develop/api-reference/connections/st.secrets
- Streamlit `st.dialog`: https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog
- Streamlit `st.form`: https://docs.streamlit.io/develop/concepts/architecture/forms
- Microsoft PowerShell `Start-Process`: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process
- Windows URI launch behavior: https://learn.microsoft.com/en-us/windows/apps/develop/launch/launch-default-app
- Microsoft PowerShell SecretManagement: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.secretmanagement/
- OWASP Key Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html
- OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- OpenAI Responses / Structured Outputs / Evals docs:
  - https://platform.openai.com/docs/api-reference/responses
  - https://platform.openai.com/docs/guides/structured-outputs
  - https://platform.openai.com/docs/api-reference/evals

## Onderzoeksconclusies

- Binance REST responses zijn chronologisch voor tijdreeksen en signed endpoints vereisen HMAC signing, timestamp en `recvWindow`. De bot heeft dit al deels in `BinanceSpotAdapter`; Roadmap 004 moet dit zichtbaar maken in de UI via connectivity checks, niet door keys in logs of bestanden te schrijven.
- Binance REST timeouts kunnen een onbekende execution status betekenen. Voor testnet-orderflow moet de bot orderstatus altijd reconciliëren via user-data `executionReport` of REST query voordat de UI een definitieve lifecycle toont.
- Binance WebSocket market streams gebruiken lowercase symbols, 24h reconnect, ping/pong en message-rate limits. Roadmap 003 heeft market-stream parsing; Roadmap 004 moet signed user-data events toevoegen voor testnet-readiness en account/order reconciliation.
- Binance User Data Streams geven `outboundAccountPosition`, `balanceUpdate` en `executionReport`. Die events zijn nodig om in testnet exact te zien wat met orders gebeurt.
- Streamlit ondersteunt `st.form` voor gebundelde instellingen en `st.dialog` voor modale flows. Dit past bij key-entry, profile selection en risky confirmations.
- Streamlit `st.secrets` bestaat, maar voor deze lokale app is session-only input veiliger als default. Optionele persistence moet via Windows user-scoped secret storage gebeuren, niet via plaintext TOML in de repo.
- Windows kan via PowerShell `Start-Process` processen starten en met `http://`/`https://` de default browser openen. Dit is genoeg voor een 1-klik `.cmd`/`.ps1` launcher.
- Microsoft SecretManagement/SecretStore is een logische optionele Windows-vault laag. Voor MVP mag het ontbreken; de app moet dan session-only blijven werken.
- OWASP benadrukt dat keys niet plaintext opgeslagen moeten worden, key storage bewust gekozen moet zijn, en API flows met gevoelige acties rate limits, logging en fail-closed gedrag nodig hebben.
- OpenAI kan later nuttig zijn voor verklarende rapporten of structured incident summaries, maar mag geen autonome trader worden en mag geen secrets of orderbeslissingen krijgen. Als toegevoegd, alleen read-only summaries met Structured Outputs en evals.

## Scope

In scope:
- Windows 11 one-click start voor dashboard.
- Dashboard profile selector voor:
  - local demo replay, zonder keys;
  - Binance Demo Spot API profile;
  - Binance Spot Testnet profile.
- Dashboard credential entry met masked inputs.
- Session-only credentials als default.
- Optionele Windows SecretManagement persistence.
- Connectivity checks: public API, signed account check, server time, active base URL.
- Testnet user-data stream parsing en order lifecycle display.
- Meer frontend controls voor risk, model, symbol, source, session, evaluation en paper/testnet readiness.
- Security hardening rond secrets, audit redaction en UI exposure.

Out of scope:
- Live trading.
- Margin/futures.
- Withdrawals.
- Cloud deployment.
- Autonome LLM trading decisions.
- Keys hardcoden in repo, roadmap of geheugen.

## Architectuurkeuze

Nieuwe laag boven bestaande config:

```text
CredentialProfile
- name: local-demo | binance-demo-spot | binance-spot-testnet
- trading_mode: disabled | testnet
- rest_base_url
- websocket_base_url
- user_data_stream_enabled
- has_api_key
- api_key_fingerprint
- storage: session | windows-secretstore | env
```

Nieuwe componenten:

```text
DashboardLauncher
- kiest vrije poort
- start Streamlit met juiste PYTHONPATH
- schrijft logs naar data/logs/
- opent default browser
- toont duidelijke foutmelding als Python/deps ontbreken

CredentialManager
- session-only keys in memory
- optioneel Windows SecretManagement vault
- masked fingerprints, nooit plaintext teruggeven
- exporteert veilige BotSettings voor runtime

ExchangeProfileManager
- local demo, Binance demo spot, Binance spot testnet
- profile metadata en base URLs
- voorkomt live profile in dashboard

ConnectivityService
- public ping/server time
- signed account check
- exchangeInfo filters
- user-data stream readiness
- redacted failure payloads

UserDataStreamAdapter
- testnet/demo signed-only
- subscribe/connect lifecycle
- parse account/order events
- reconnect/keepalive policy

OrderLifecycleStore
- order intents, test orders, accepted/rejected/canceled/filled
- reconciliation status
- maps executionReport + REST query order

DashboardSettingsStore
- non-secret preferences only
- selected profile, symbol list, risk presets, chart layout
- stored as JSON under data/settings/
```

Hergebruiken:
- `BinanceSpotAdapter` voor REST en signed requests.
- `MarketDataSource` en `WebSocketMarketDataSource` voor market-data mode.
- `RiskEngine` voor deterministic trade gating.
- `ExecutionEngine` voor disabled/paper/testnet boundaries.
- `SessionStore` voor sessions/fills/equity.
- `ModelRegistry` voor model alias/metadata.
- `AuditLog` voor immutable decision logs.

## Fase 1: Windows 11 one-click start

Toevoegen:

```text
Start Bot Dashboard.cmd
scripts/start-dashboard.ps1
scripts/stop-dashboard.ps1
scripts/check-local-env.ps1
```

Gedrag:
- Dubbelklik op `Start Bot Dashboard.cmd`.
- Script opent een PowerShell-venster met duidelijke statusregels.
- Controleert Python versie en projectpad.
- Zet `PYTHONPATH=src`.
- Installeert optioneel ontbrekende UI dependencies alleen na duidelijke melding.
- Kiest vrije poort vanaf `8503`.
- Start Streamlit.
- Wacht tot poort bereikbaar is.
- Opent `http://127.0.0.1:<port>` in de default browser.
- Schrijft logs naar `data/logs/dashboard-<timestamp>.log`.
- Laat live trading disabled.

Acceptatiecriteria:
- Werkt met een projectpad dat spaties bevat.
- Geen adminrechten nodig.
- Dubbelklikken opent dashboard automatisch.
- Bij ontbrekende dependency verschijnt een begrijpelijke instructie.
- Als poort bezet is, wordt automatisch een volgende poort gebruikt.
- `Stop Bot Dashboard.cmd` of `scripts/stop-dashboard.ps1` stopt alleen de eigen dashboardprocessen.
- Browsercheck bevestigt dat het dashboard lokaal opent en `LIVE TRADING DISABLED` toont.

## Fase 2: Exchange profiles en zichtbare modus

Dashboard moet bovenaan altijd tonen:
- actieve profile naam;
- mode badge: `LOCAL DEMO`, `BINANCE DEMO SPOT`, `BINANCE SPOT TESTNET`;
- REST base URL;
- WebSocket base URL;
- signed trading capability: `not configured`, `read-only/account ok`, `test-order capable`;
- live status: altijd `disabled`.

Aanpassingen:
- `BotSettings` uitbreiden met `exchange_profile`.
- `BINANCE_API_BASE_URL` als compatibele alias ondersteunen naast `BINANCE_BASE_URL`/`BINANCE_TESTNET_BASE_URL`, omdat gebruikers vaak die naam verwachten.
- `TradingMode.TESTNET` gebruiken voor Binance demo/testnet signed flows, maar profile metadata bepaalt welke base URL actief is.
- Dashboard mode selector mag geen `live` bevatten.

Acceptatiecriteria:
- Gebruiker ziet direct of hij demo keys of testnet keys moet invoeren.
- Base URL is zichtbaar en wordt nooit impliciet live.
- Als `binance-demo-spot` geselecteerd is, gebruikt runtime de demo base URL.
- Als `binance-spot-testnet` geselecteerd is, gebruikt runtime testnet base URL.
- Geen profile kan withdrawals of live activeren.

## Fase 3: Credentials invoeren in dashboard

Nieuwe UI:
- `Credentials` tab of dialog.
- API key input met masked text.
- API secret input met password field.
- Profile selector boven de inputs.
- Buttons:
  - `Use for this session`;
  - `Test connection`;
  - `Clear session credentials`;
  - optioneel `Save to Windows SecretStore`.

Securityregels:
- Default is session-only.
- Plaintext keys worden nooit naar `data/`, `logs/`, `audit/`, sessions of roadmap docs geschreven.
- UI toont alleen fingerprint: eerste 4 en laatste 4 tekens, of hash-prefix.
- Errors worden geredact.
- Clipboard buttons voor secrets worden niet toegevoegd.
- `st.secrets` mag alleen als read-only fallback worden gebruikt, niet als dashboard-write target.
- Windows SecretManagement is optioneel en user-scoped.

Acceptatiecriteria:
- Credentials werken zonder `.env` te maken.
- Refresh van dashboard bewaart session-only credentials zolang Streamlit session leeft.
- Herstart wist session-only credentials.
- Secret scan vindt geen keys.
- Logs bevatten geen API key, secret of signed query signature.
- Tests valideren redaction.

## Fase 4: Connectivity en readiness panel

Nieuwe backend:

```text
connectivity.py
- check_public_market_data(profile)
- check_server_time(profile)
- check_exchange_info(symbol)
- check_signed_account(settings)
- check_test_order_capability(settings, symbol)
```

Dashboard panel:
- public REST status;
- signed account status;
- server time drift;
- exchangeInfo filters;
- permissions warning;
- rate-limit headers wanneer beschikbaar;
- user-data stream readiness;
- laatste connectivity check tijd.

Acceptatiecriteria:
- `local-demo` vereist geen keys en toont `No signed credentials required`.
- `binance-demo-spot` en `binance-spot-testnet` tonen `needs credentials` tot keys ingevoerd zijn.
- Signed account check faalt veilig zonder stack trace.
- Server time drift boven threshold geeft warning.
- Test order capability gebruikt alleen test-order endpoint of disabled/paper equivalent, geen echte order in deze fase.

## Fase 5: Testnet user-data stream en order lifecycle

Nieuwe module:

```text
src/binance_spot_bot/user_data_stream.py
```

Verantwoordelijkheid:
- user-data subscription/connect lifecycle voor testnet/demo;
- parse `outboundAccountPosition`;
- parse `balanceUpdate`;
- parse `executionReport`;
- parse `listStatus`;
- reconnect en expired stream handling;
- redacted audit events.

Nieuwe module:

```text
src/binance_spot_bot/order_lifecycle.py
```

Verantwoordelijkheid:
- order intent -> submitted -> accepted/rejected -> partially filled -> filled/canceled/expired;
- reconcile via user-data events;
- fallback REST query order bij unknown status;
- dashboard timeline.

Acceptatiecriteria:
- Parser tests met officiële Binance eventvormen.
- Unknown REST timeout status wordt niet als failed of filled gemarkeerd zonder reconciliation.
- Dashboard toont order lifecycle timeline.
- Testnet orderflow blijft gated achter manual `Enable testnet test-order checks` toggle.
- Geen live order path toegevoegd.

## Fase 6: Dashboard control center verbeteringen

Nieuwe/uitgebreide tabs:

```text
Overview
Credentials & Profile
Bot Controls
Risk Controls
Strategy & Model
Market Data
Orders & Account
Sessions
Evaluation
Logs & Security
```

Frontend features:
- Risk presets: conservative, balanced, aggressive-paper-only, custom.
- Editable risk fields:
  - max daily loss;
  - max position quote;
  - max trades per day;
  - min confidence;
  - max spread bps;
  - max data age;
  - default quote size.
- Symbol watchlist.
- Market source selector: demo, REST, WebSocket.
- Model alias selector: baseline, candidate, champion.
- Evaluation trigger button for selected symbol/interval.
- Session compare view: PnL, drawdown, trades, blocks.
- Data quality drilldown.
- Emergency stop button that stops runtime and keeps kill-switch semantics visible.
- Export session/evaluation/model metadata.

Designregels:
- Geen marketing landing page.
- Dense operational layout, geen overgrote hero.
- Status badges en metrics moeten scanbaar zijn.
- Controls in forms zodat wijzigingen pas na `Apply` actief worden.
- Risky actions in dialogs met duidelijke gevolgen.

Acceptatiecriteria:
- Gebruiker kan de bot starten/pauzeren/resetten vanaf dashboard.
- Gebruiker kan risk/model/source/symbol aanpassen zonder terminal.
- UI toont duidelijk welke wijzigingen actief zijn en welke pending zijn.
- Geen live optie zichtbaar.
- Browsercheck desktop en smalle viewport zonder overlappende tekst.

## Fase 7: Settings persistence zonder secrets

Nieuwe module:

```text
src/binance_spot_bot/settings_store.py
```

Opslag:

```text
data/settings/dashboard.json
data/settings/risk-presets.json
data/settings/watchlists.json
```

Niet opslaan:
- API key;
- API secret;
- signatures;
- listen keys;
- Authorization headers;
- raw signed URLs.

Acceptatiecriteria:
- Dashboard onthoudt profile, symbol, interval, risk preset en layout.
- Secret scan op `data/settings/` is schoon.
- Settings kunnen terug naar defaults.
- Invalid JSON faalt veilig met defaults.

## Fase 8: Optionele AI-assistent voor uitleg, niet voor trading

Alleen optioneel als `OPENAI_API_KEY` lokaal aanwezig is.

Toegestane functies:
- session summary uitleggen;
- data-quality warnings samenvatten;
- evaluation report structureren;
- risk-control checklist genereren.

Niet toegestaan:
- autonome buy/sell beslissingen;
- directe orderplaatsing;
- secrets verwerken;
- modelpromotie zonder metrics en menselijke bevestiging.

Techniek:
- OpenAI Responses API met Structured Outputs voor vaste JSON schema's.
- Lokale evals voor assistant-output voordat het in dashboard zichtbaar wordt.
- Geen OpenAI dependency verplicht voor demo/dashboard.

Acceptatiecriteria:
- AI-paneel is disabled als geen OpenAI key aanwezig is.
- Prompts bevatten geen Binance secrets.
- Output schema wordt gevalideerd.
- Tests bewijzen dat order intent nooit door AI-paneel wordt gegenereerd.

## Fase 9: Security hardening

Aanpassingen:
- Centrale redaction helper voor logs, audit, errors en UI payloads.
- Extra secret regexes voor Binance key formats.
- Secret scan ook over `scripts/`, `configs/`, `docs/`, `Roadmap docs/`, `Voltooid docs/`, maar `data/sessions` blijft gecontroleerd op secret patterns.
- Fail-closed defaults voor profile mismatch.
- Dashboard warning als user probeert demo key op testnet profile te gebruiken of andersom.
- Rate-limit backoff zichtbaar in UI.
- `recvWindow` en server time drift monitoren.
- Withdrawal permissions check, indien Binance endpoint dit veilig kan rapporteren; anders expliciet handmatige checklist.

Acceptatiecriteria:
- `python -m binance_spot_bot.cli security-scan` vindt geen findings.
- Browsercheck toont keys nooit in plaintext na submit.
- AuditLog bevat alleen masked profile/fingerprint.
- Geen route of command kan `TradingMode.LIVE` activeren.
- `Start Bot Dashboard.cmd` zet live environment flags expliciet uit.

## Fase 10: Testplan

Verplichte checks:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests
python -m binance_spot_bot.cli security-scan
python -m binance_spot_bot.cli validate-config
```

Nieuwe tests:
- Windows launcher syntax en path-with-spaces handling.
- Free-port selection.
- Dashboard profile list bevat geen live.
- CredentialManager session-only behavior.
- Windows SecretManagement adapter mocked.
- Redaction van keys, secrets, signatures, listen keys.
- `BINANCE_API_BASE_URL` alias parsing.
- Connectivity checks met fake adapter.
- User-data stream parsers voor `executionReport`, `outboundAccountPosition`, `balanceUpdate`.
- Order lifecycle reconciliation.
- SettingsStore read/write/defaults.
- Dashboard smoke test met Browser:
  - one-click start opent browser;
  - mode badge zichtbaar;
  - credentials panel zichtbaar;
  - risk controls zichtbaar;
  - `LIVE TRADING DISABLED` zichtbaar;
  - geen console errors.

## Definitie van volledig afgewerkt

Roadmap 004 is pas voltooid als:
- Windows one-click launcher bestaat en opent dashboard automatisch.
- Dashboard kan session-only Binance demo/testnet keys invoeren.
- Dashboard toont actieve profile/mode/base URL en credential status.
- Credential persistence is optioneel en veilig via Windows SecretManagement of blijft session-only.
- User kan risk/model/source/symbol/session/evaluation controls vanuit frontend bedienen.
- Connectivity/readiness panel werkt zonder echte order te plaatsen.
- Testnet user-data event parsing en order lifecycle reconciliation bestaan.
- Settings persistence slaat geen secrets op.
- Security scan, unit tests en browsercheck slagen.
- Roadmapbestand daarna wordt verplaatst naar `Voltooid docs/`.

## Logische Roadmap 005 daarna

- Langdurige unattended paper/testnet sessies met alerts.
- Testnet order placement achter expliciete gated approval.
- Meer geavanceerde modeltraining met PyTorch checkpoints.
- Watchlist/scanner over meerdere symbols.
- MLflow of DuckDB integratie als lokale JSONL te beperkt wordt.
- Packaging als echte Windows app of tray utility.
