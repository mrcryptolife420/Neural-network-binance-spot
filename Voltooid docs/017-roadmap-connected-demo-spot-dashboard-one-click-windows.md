# Roadmap 017: Connected Demo Spot Dashboard en One-click Windows Start

## Status

Voltooid.

Validatie:

- `python -m unittest discover -s tests` groen: 89 tests.
- `python -m binance_spot_bot.cli check-all --json` groen.
- Security scan groen: geen secret artifacts gevonden.
- `git diff --check` zonder whitespace errors.
- Live trading blijft disabled.

Geimplementeerd:

- Demo Spot connection state en demo trading gate.
- Binance Demo Spot signed adapter allowlist op `https://demo-api.binance.com`.
- Adapterfuncties voor account, test order, place order, query order, cancel order en open orders.
- ExecutionEngine demo-arm flow: test order voor place order, max orders gate en structured reject payloads.
- Runtime snapshotvelden voor demo connection, demo account en demo open orders.
- Dashboard arm/disarm controls, connection badges, demo gate status, demo account en open orders.
- One-click Windows startscript met foutmelding/logpad en veilige env.
- Launcher gebruikt de actieve Python executable en control center schrijft vaste logs.
- CLI `run-local --demo-trading-armed` summary bevat demo armed status.
- Tests voor demo gate, adapter allowlist, execution flow en connection state.

Deze roadmap bouwt voort op roadmaps 001 t/m 016. De bestaande bot heeft al een veilige paper/testnet/demo basis, Streamlit-dashboard, credentials flow, exchange profiles, risk engine, execution engine, order lifecycle, paper accounting, readiness checks, session reports, model governance en een Windows startscript. Roadmap 017 maakt hiervan één verbonden lokale operatorervaring:

**1 klik op Windows 11 -> dashboard opent -> Binance Demo Spot profiel kiezen -> keys invoeren/testen -> bot armeren -> demo spot orders kunnen plaatsen, volgen en stoppen vanuit het dashboard.**

Live trading blijft buiten scope en moet disabled blijven.

## Bronnen en actuele uitgangspunten

- Binance Spot API docs: `https://github.com/binance/binance-spot-api-docs`
- Binance Spot API reference noemt Demo als base URL: `https://demo-api.binance.com`
- Authenticated Spot endpoints zijn relevant voor demo execution: `/api/v3/order/test`, `/api/v3/order`, `/api/v3/openOrders`, `/api/v3/account`, `/api/v3/time`
- Alleen Binance Demo Spot en bestaande paper/testnet-readiness flows worden verbonden. Geen mainnet live trading.

## Hoofddoel

Maak het dashboard de centrale control room voor de bot:

- lokaal starten met één klik;
- verbinden met Binance Demo Spot;
- credentials veilig invoeren voor de sessie;
- verbinding en accountstatus testen;
- bot armeren voor demo trading;
- signalen, risk decisions, intents, orders, fills, balances en PnL live volgen;
- demo orders plaatsen via bestaande risk/execution route;
- altijd kunnen pauzeren, disarmen en kill switch activeren.

## Niet dubbel bouwen

Roadmap 017 mag geen tweede dashboard, tweede credential store, tweede execution engine, tweede order lifecycle of tweede runtime bouwen.

Hergebruik en breid uit:

- `Start Bot Dashboard.cmd`
- `control_center.py`
- `launcher.py`
- `ui/streamlit_app.py`
- `ui/state.py`
- `credentials.py`
- `exchange_profiles.py`
- `binance.py`
- `execution.py`
- `runtime.py`
- `order_lifecycle.py`
- `paper_accounting.py`
- `risk.py`
- `readiness.py`
- `session_store.py`
- `session_report.py`
- `check_all.py`

## Scope

In scope:

- One-click Windows start verbeteren.
- Dashboard connect/arm/trade flow.
- Binance Demo Spot authenticated adapter pad.
- Demo order test/place/query/cancel flow.
- Demo balances en account status.
- Reconciliation van demo orders in order lifecycle.
- Dashboard trading control center UX.
- Safety gates en audit logs.
- Tests en `check-all`.

Niet in scope:

- Binance mainnet live trading.
- Withdrawal endpoints.
- Margin/futures.
- DCA/grid/algo trading endpoints.
- Mobile app.
- VPS deployment.
- Automatische winstoptimalisatie.
- Autonome LLM-trading.

## Gebruikerservaring

### Gewenste operatorflow

1. Gebruiker dubbelklikt op Windows: `Start Bot Dashboard.cmd`.
2. Script controleert Python/dependencies en start Streamlit.
3. Browser opent automatisch op het lokale dashboard.
4. Dashboard toont bovenaan:
   - actieve mode;
   - exchange profile;
   - connection status;
   - bot status;
   - armed/disarmed;
   - kill switch;
   - live trading disabled.
5. Gebruiker kiest `Binance Demo Spot`.
6. Gebruiker voert API key en secret in.
7. Gebruiker klikt `Test connection`.
8. Dashboard toont:
   - server time ok/fail;
   - account accessible ok/fail;
   - trading permission ok/fail;
   - base URL `https://demo-api.binance.com`;
   - key fingerprint, nooit plaintext secret.
9. Gebruiker klikt `Arm demo trading`.
10. Bot mag alleen demo orders sturen wanneer:
    - demo profile actief is;
    - live disabled is;
    - kill switch niet actief is voor demo;
    - risk limits geldig zijn;
    - connection health ok is;
    - operator expliciet armed heeft.
11. Dashboard toont realtime:
    - candle chart;
    - model signal;
    - risk decision;
    - trade intent;
    - order request;
    - order response;
    - order lifecycle;
    - open orders;
    - demo balances;
    - PnL/equity;
    - alerts.
12. Gebruiker kan altijd:
    - pause;
    - disarm;
    - cancel open orders;
    - emergency stop;
    - export session report.

## Architectuur

### DemoSpotConnectionState

Nieuwe of uitgebreide statusstructuur voor dashboard/runtime.

Velden:

- `profile`
- `base_url`
- `connected`
- `authenticated`
- `server_time_ok`
- `account_ok`
- `trading_permission_ok`
- `armed`
- `kill_switch`
- `last_error`
- `api_key_fingerprint`
- `checked_at_ms`

Acceptatie:

- Dashboard kan deze status als badges tonen.
- Secret of volledige key komt nooit in status, logs of reports.

### Binance Demo Spot Adapter

Breid bestaande `binance.py`/adapterlaag uit waar nodig.

Minimale functies:

- `ping`
- `server_time`
- `exchange_info`
- `account`
- `test_order`
- `place_order`
- `query_order`
- `cancel_order`
- `open_orders`

Regels:

- Demo trading alleen toegestaan op `https://demo-api.binance.com`.
- Testnet trading alleen op `https://testnet.binance.vision`.
- Mainnet live blijft disabled.
- Signed requests gebruiken bestaande HMAC-flow.
- `recvWindow` en timestamp worden gecontroleerd.
- Binance errors worden gestructureerd teruggegeven.

Acceptatie:

- Unit tests mocken signed demo requests.
- Base URL allowlist blokkeert mainnet order routes.
- `/api/v3/order/test` werkt als dry-run stap voor place-order.

### Demo Trading Gate

Nieuwe gate tussen dashboard/runtime en execution.

Voorwaarden:

- profile is `binance_demo_spot`;
- base URL is `https://demo-api.binance.com`;
- credentials aanwezig;
- connection check recent groen;
- dashboard is armed;
- live trading disabled;
- risk engine geeft ALLOW;
- symbol filters zijn geladen;
- order size voldoet aan Binance filters;
- max orders per sessie niet overschreden;
- kill switch niet actief.

Acceptatie:

- Elke geblokkeerde order heeft duidelijke reden.
- Gate output wordt in audit/order lifecycle opgeslagen.
- Tests dekken allowed en blocked situaties.

### Runtime integratie

Breid bestaande `BotRuntime` uit zodat demo execution een expliciete mode krijgt.

Gedrag:

- Paper blijft standaard.
- Demo Spot execution alleen na arm.
- Bij disarm of kill switch stopt orderplaatsing direct.
- Market data kan demo/rest/websocket blijven gebruiken.
- Risk engine blijft altijd deterministisch.
- Model levert alleen signalen, niet directe orders.

Acceptatie:

- Runtime kan in demo armed mode een order-intent naar Demo Spot adapter sturen.
- Runtime schrijft lifecycle events voor request, accepted/rejected, queried, filled/canceled.
- Runtime blijft werken zonder credentials in paper mode.

### Dashboard Control Center

Breid `ui/streamlit_app.py` uit met een duidelijke bovenliggende flow.

Nieuwe of verbeterde panelen:

- Connection banner.
- Profile & keys panel.
- Arm/disarm demo trading.
- Demo account balances.
- Open orders.
- Order lifecycle timeline.
- Signal -> risk -> intent -> order pipeline.
- Cancel open demo orders knop.
- Session report/export knop.
- Error/reject panel.

UX-regels:

- Geen ruwe JSON als primaire UI voor operatorflows.
- Tabellen en badges voor status.
- Raw JSON alleen in expander/debug.
- Live disabled altijd zichtbaar.
- Demo Spot label moet duidelijk zijn.

Acceptatie:

- Gebruiker ziet in één scherm of bot verbonden, armed en trading is.
- Gebruiker ziet welke profile/base URL actief is.
- Gebruiker kan niet per ongeluk live inschakelen.

### Windows one-click start

Verbeter `Start Bot Dashboard.cmd` en waar nodig `control_center.py`.

Gedrag:

- Werkt vanaf Windows 11 dubbelklik.
- Controleert Python.
- Zet/controleert venv of gebruikt lokale Python.
- Installeert ontbrekende UI-dependencies alleen als nodig of toont duidelijke instructie.
- Start dashboard op vrije poort.
- Opent browser automatisch.
- Schrijft logs naar `data/logs/control-center.log`.
- Toont duidelijke foutmelding bij mislukking.

Acceptatie:

- Dry-run test geeft URL terug.
- Geen extra terminalcommando nodig voor normale gebruiker.
- Bestaande CLI blijft werken.

## Fases

### Fase 1: Demo Spot profiel en connection state harden

Taken:

- Controleer en verfijn exchange profile voor Binance Demo Spot.
- Voeg `DemoSpotConnectionState` toe.
- Maak connect-check helper voor ping/server time/account.
- Zorg dat key fingerprint zichtbaar is, secret nooit.
- Dashboard toont connection state bovenaan.

Acceptatie:

- Zonder keys: status `disconnected`.
- Met mock keys: status kan `connected/authenticated` tonen.
- Base URL is zichtbaar.
- Secret scan groen.

### Fase 2: Authenticated Demo Spot adapter

Taken:

- Breid adapter uit met account, test order, place order, query order, cancel order en open orders.
- Voeg structured Binance error payload toe.
- Voeg base URL allowlist toe.
- Voeg recvWindow/timestamp handling toe.
- Voeg tests met mocks toe.

Acceptatie:

- Mainnet order route wordt geblokkeerd.
- Demo base URL wordt toegestaan.
- Test order wordt aangeroepen voor echte demo place.
- Query/cancel/open orders hebben gestandaardiseerde output.

### Fase 3: Demo trading gate en runtime koppeling

Taken:

- Voeg explicit armed state toe.
- Koppel risk decision -> execution intent -> demo adapter.
- Voeg max demo orders per sessie toe.
- Voeg disarm/pause/kill switch blokkades toe.
- Schrijf lifecycle events.

Acceptatie:

- Demo order kan alleen na arm.
- Paper mode blijft zonder credentials werken.
- Kill switch blokkeert direct.
- Lifecycle toont blocked/accepted/rejected/query/cancel events.

### Fase 4: Dashboard trading control center

Taken:

- Bouw connection banner.
- Bouw arm/disarm controls.
- Toon signal -> risk -> intent -> order pipeline.
- Toon balances, open orders en order lifecycle.
- Voeg cancel open orders knop toe.
- Voeg reject/error panel toe.

Acceptatie:

- Operator kan de volledige demo trading flow visueel volgen.
- Geen secrets zichtbaar.
- Live disabled zichtbaar.
- Raw JSON alleen optioneel.

### Fase 5: Windows one-click polish

Taken:

- Verbeter startscript.
- Voeg dry-run en logging toe.
- Open browser automatisch.
- Gebruik vrije poort.
- Documenteer één klik flow kort in dashboard/docs.

Acceptatie:

- Dubbelklik start dashboard.
- Foutmeldingen zijn begrijpelijk.
- Logbestand wordt aangemaakt.
- `control-center --dry-run` blijft testbaar.

### Fase 6: Reports, readiness en operator audit

Taken:

- Voeg demo connection/trading status toe aan session report.
- Voeg readiness blocker toe wanneer demo trading armed is zonder checks.
- Voeg audit events toe voor connect, arm, disarm, place, cancel en reject.
- Voeg support bundle info toe zonder secrets.

Acceptatie:

- Report toont demo trading mode en order lifecycle.
- Audit log bevat beslisreden.
- Support bundle redacted.

### Fase 7: Tests en afronding

Taken:

- Unit tests voor connection state.
- Unit tests voor adapter allowlist.
- Unit tests voor demo gate.
- Runtime smoke test voor armed demo mock.
- Dashboard import test.
- One-click dry-run test.
- Secret scan.
- `check-all`.

Acceptatie:

- `python -m unittest discover -s tests` groen.
- `python -m binance_spot_bot.cli check-all --json` groen.
- Geen secret artifacts.
- Live trading blijft disabled.
- Roadmap wordt pas daarna naar `Voltooid docs/` verplaatst.

## Safety regels

- Geen echte API keys in repo.
- Geen secrets in logs, reports, screenshots, support bundles of audit payloads.
- Withdrawal permissions blijven buiten scope.
- Mainnet live trading blijft disabled.
- Demo trading vereist expliciete arm-actie.
- Risk engine mag niet worden omzeild.
- Model mag niet direct orders plaatsen.
- LLM mag geen autonome orderbeslissingen nemen.

## Definition of Done

Roadmap 017 is volledig afgewerkt wanneer:

- One-click Windows dashboard start betrouwbaar werkt.
- Dashboard heeft een duidelijke connect/arm/trade flow.
- Binance Demo Spot credentials kunnen veilig sessie-lokaal worden gebruikt.
- Demo connection check toont server/account/trading status.
- Demo Spot order test/place/query/cancel/open-orders flow werkt via bestaande execution route.
- Runtime kan demo orders alleen in armed demo mode plaatsen.
- Order lifecycle en account/balance status zijn zichtbaar in dashboard.
- Cancel/disarm/kill switch werken.
- Reports en audit bevatten demo trading events zonder secrets.
- Tests en `check-all` groen zijn.
- Live trading disabled blijft.
- Roadmapbestand wordt verplaatst naar `Voltooid docs/`.

## Aanbevolen eerste implementatiestap

Start met Fase 1 en Fase 2:

1. Demo Spot profile en connection state harden.
2. Authenticated adapterfuncties toevoegen met mocked tests.
3. Dashboard connection banner tonen.

Daarna pas runtime armed trading koppelen, zodat de veilige verbinding eerst aantoonbaar klopt.
