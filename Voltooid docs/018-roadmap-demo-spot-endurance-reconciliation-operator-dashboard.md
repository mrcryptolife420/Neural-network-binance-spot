# Roadmap 018: Demo Spot Endurance, Reconciliation en Operator Dashboard

## Status

Voltooid.

Validatie:

- `python -m unittest discover -s tests` groen: 94 tests.
- `python -m binance_spot_bot.cli check-all --json` groen.
- Security scan groen: geen secret artifacts gevonden.
- `git diff --check` zonder whitespace errors.
- Live trading blijft disabled.

Geimplementeerd:

- Demo pilot presets: smoke, operator en endurance.
- Demo pilot counters en pause-limits.
- REST order reconciliation voor known, failed en orphan orders.
- Clean-start check die open/orphan demo orders blokkeert.
- Demo account sync met non-zero balance filtering.
- User data stream status uitgebreid met listenKey/fallback-rest state.
- Binance adapter listenKey lifecycle helpers.
- Runtime snapshotvelden voor demo pilot, reconciliation, resume-required, order errors en cancel-on-stop status.
- Cancel-open-orders-on-stop policy.
- Demo Pilot dashboardtab met pilot status, counters, pipeline, reconciliation, balances, open orders en report export.
- Demo pilot report artifact `demo-pilot.json`.
- Tests voor pilot config, reconciler, account sync, clean start, cancel-on-stop en report metadata.

Deze roadmap bouwt direct voort op roadmaps 001 t/m 017. Roadmap 017 heeft de lokale Windows one-click dashboardflow, Binance Demo Spot connection state, demo trading gate, armed execution route, adapter allowlist en dashboardstatussen verbonden. Roadmap 018 maakt deze Demo Spot flow betrouwbaar voor langere lokale operatorpilots.

Doel:

**Bot lokaal starten, verbinden met Binance Demo Spot, armeren, onder strikte limieten laten handelen, orderstatussen reconciliëren, balances syncen, veilig stoppen, open orders cancellen en een volledig demo pilot rapport krijgen.**

Live trading blijft buiten scope en disabled.

## Waarom deze roadmap nu nodig is

De Demo Spot route kan nu expliciet worden geactiveerd, maar een trading bot is pas bruikbaar als de operator ook kan vertrouwen op wat er na orderplaatsing gebeurt:

- Is de order echt geaccepteerd?
- Is hij gevuld, gedeeltelijk gevuld, geannuleerd of onbekend?
- Zijn er open orders blijven hangen?
- Komt de lokale orderstatus overeen met Binance Demo Spot?
- Zijn balances consistent?
- Kan de bot veilig hervatten na crash of restart?
- Is er een rapport dat laat zien wat er tijdens de demo pilot is gebeurd?

Roadmap 018 lost deze operationele gaten op zonder live trading te openen.

## Scope

In scope:

- Demo Spot endurance/pilot sessies.
- Order reconciliation via REST.
- Open-order detectie bij start en stop.
- Cancel-open-orders-on-stop.
- Demo account/balance sync.
- User data stream voorbereiding en event parsing integratie.
- Dashboard Demo Pilot pagina.
- Crash/resume safety.
- Pilot rapportage.
- Tests en `check-all`.

Niet in scope:

- Binance mainnet live trading.
- Withdrawal endpoints.
- Margin/futures.
- Nieuwe exchange-integraties.
- Autonome LLM-trading.
- Strategie-optimalisatie of winstbelofte.

## Bestaande infrastructuur die moet worden hergebruikt

Niet opnieuw bouwen:

- `demo_spot.py`
- `binance.py`
- `execution.py`
- `runtime.py`
- `order_lifecycle.py`
- `user_data_stream.py`
- `session_store.py`
- `session_report.py`
- `paper_accounting.py`
- `alerts.py`
- `readiness.py`
- `ui/streamlit_app.py`
- `control_center.py`
- `check_all.py`

Nieuwe code moet deze modules uitbreiden of hierop aansluiten.

## Gewenste operatorflow

1. Gebruiker start dashboard via Windows one-click.
2. Dashboard detecteert actieve/unfinished Demo Spot sessie.
3. Dashboard controleert Binance Demo Spot connection.
4. Dashboard haalt open orders op.
5. Als er open/unknown orders zijn, moet operator kiezen:
   - reconciliëren;
   - open demo orders cancellen;
   - nieuwe sessie starten na bevestiging.
6. Gebruiker kiest een demo pilot mode:
   - 15 minuten smoke pilot;
   - 60 minuten operator pilot;
   - 240 minuten endurance pilot.
7. Gebruiker armt Demo Spot trading.
8. Bot handelt alleen binnen ingestelde limieten.
9. Dashboard toont live:
   - connection status;
   - runtime status;
   - armed/disarmed;
   - signal -> risk -> intent -> test order -> demo order -> fill pipeline;
   - open orders;
   - reconciliatie status;
   - balances;
   - fills;
   - alerts;
   - Binance errors/rejects.
10. Bij stop/pause/kill switch:
    - trading disarmed;
    - open orders worden optioneel of verplicht gecancelled volgens policy;
    - order reconciliation wordt gedraaid;
    - rapport wordt geëxporteerd.

## Architectuur

### DemoPilotConfig

Nieuwe configuratiestructuur voor pilot/endurance sessies.

Velden:

- `pilot_name`
- `duration_minutes`
- `max_demo_orders`
- `max_rejects`
- `max_api_errors`
- `max_reconciliation_failures`
- `cancel_open_orders_on_stop`
- `reconciliation_interval_seconds`
- `account_sync_interval_seconds`
- `pause_on_connection_degraded`
- `require_clean_start`

Acceptatie:

- Dashboard kan pilot mode kiezen.
- Runtime kan limieten lezen.
- Tests kunnen korte pilotconfig gebruiken.

### DemoOrderReconciler

Nieuwe of uitgebreide component rond bestaande `OrderLifecycleStore`.

Taken:

- `/api/v3/openOrders` ophalen.
- `/api/v3/order` query uitvoeren voor bekende orders.
- Unknown/orphan orders detecteren.
- Lifecycle statussen normaliseren.
- Reconciliation result opslaan in session events.

Statussen:

- `INTENT`
- `TESTED`
- `SUBMITTED`
- `NEW`
- `PARTIALLY_FILLED`
- `FILLED`
- `CANCELED`
- `REJECTED`
- `EXPIRED`
- `UNKNOWN`
- `ORPHAN_OPEN`
- `RECONCILIATION_FAILED`

Acceptatie:

- Na elke submitted demo order wordt query-order aangeroepen.
- Open orders worden zichtbaar in dashboard.
- Unknown/orphan orders blokkeren nieuwe orderplaatsing tot operatoractie.
- Reconciliation events worden in audit en session log geschreven.

### DemoAccountSync

Component voor Demo Spot account en balances.

Taken:

- `/api/v3/account` ophalen.
- Non-zero balances tonen.
- Account flags tonen: `canTrade`, `accountType`.
- Last sync timestamp tonen.
- Verschil tonen tussen lokale paper/equity indicatie en Binance Demo balances waar zinvol.

Acceptatie:

- Dashboard toont balances zonder secrets.
- Account sync errors stoppen runtime niet direct, maar verhogen alert/reject counters.
- Bij degraded account sync kan demo trading automatisch pauzeren volgens pilot config.

### UserDataStream voorbereiding

Gebruik bestaande `user_data_stream.py`.

Taken:

- ListenKey lifecycle ontwerpen/implementeren waar haalbaar:
  - create listenKey;
  - keepalive;
  - close.
- Execution reports verwerken via bestaande parser.
- REST reconciliation blijft fallback.
- Dashboard toont streamstatus:
  - disconnected;
  - connected;
  - reconnecting;
  - fallback-rest.

Acceptatie:

- Parser tests blijven groen.
- Stream events kunnen lifecycle updaten.
- Als stream ontbreekt, blijft REST reconciliation werken.

### Runtime Demo Pilot State

Breid runtime snapshot uit met:

- `demo_pilot`
- `reconciliation`
- `demo_account`
- `demo_open_orders`
- `demo_order_errors`
- `resume_required`
- `cancel_on_stop_status`

Acceptatie:

- Dashboard kan alle velden renderen zonder extra API calls waar mogelijk.
- Session report bevat dezelfde kerninformatie.

### Dashboard Demo Pilot pagina

Maak één duidelijke operatorpagina of tab die alles samenbrengt.

Panelen:

- Pilot mode selector.
- Connection/armed status.
- Clean start/resume warning.
- Pipeline:
  - Signal
  - Risk
  - Intent
  - Test order
  - Demo order
  - Reconciliation
  - Fill/cancel/reject
- Open orders.
- Known orders lifecycle.
- Balances.
- Reject/API error counters.
- Pilot timer.
- Stop/disarm/cancel controls.
- Export pilot report.

UX-regels:

- Geen raw JSON als primaire UI.
- Raw payloads alleen in expander.
- Statussen moeten met badges/tabellen zichtbaar zijn.
- Live disabled altijd zichtbaar.
- Demo Spot base URL altijd zichtbaar.

## Fases

### Fase 1: Pilot config en clean-start checks

Taken:

- Voeg `DemoPilotConfig` toe.
- Voeg preset modes toe: smoke, operator, endurance.
- Voeg clean-start check toe op open orders.
- Voeg resume-required state toe.
- Dashboard toont clean-start waarschuwing.

Acceptatie:

- Zonder open orders kan pilot starten.
- Met open orders wordt arm/trade geblokkeerd tot reconciliatie/cancel.
- Tests dekken clean en dirty start.

### Fase 2: REST order reconciliation

Taken:

- Bouw `DemoOrderReconciler`.
- Query known orders.
- Haal open orders op.
- Detecteer orphan open orders.
- Update `OrderLifecycleStore`.
- Log reconciliation events.

Acceptatie:

- Submitted order wordt na plaatsing queried.
- Open order zonder bekende client id wordt `ORPHAN_OPEN`.
- Failed query wordt `RECONCILIATION_FAILED`.
- Dashboard toont reconciliation summary.

### Fase 3: Demo account sync

Taken:

- Bouw `DemoAccountSync`.
- Haal account/balances op.
- Filter non-zero balances.
- Houd last sync en errors bij.
- Voeg dashboard balance panel toe.

Acceptatie:

- Balances zichtbaar in dashboard.
- Secret scan blijft groen.
- Account errors verhogen alert counter.

### Fase 4: Runtime endurance guard

Taken:

- Voeg pilot runtime counters toe:
  - orders;
  - rejects;
  - api errors;
  - reconciliation failures;
  - elapsed time.
- Auto-pause bij overschrijding.
- Cancel-open-orders-on-stop policy.
- Session events voor pilot heartbeat.

Acceptatie:

- Runtime stopt/pauzeert bij limieten.
- Stop voert cancel/reconcile policy uit.
- Heartbeats worden vastgelegd.

### Fase 5: Dashboard Demo Pilot UX

Taken:

- Voeg Demo Pilot tab of sectie toe.
- Toon pilot presets.
- Toon timer en counters.
- Toon pipeline.
- Toon lifecycle/reconciliation.
- Toon balances.
- Voeg buttons toe:
  - reconcile now;
  - cancel open demo orders;
  - export pilot report.

Acceptatie:

- Operator kan Demo Spot pilot vanaf dashboard volgen.
- Unknown/orphan orders zijn duidelijk zichtbaar.
- Disarm/stop/cancel controls zijn altijd bereikbaar.

### Fase 6: User data stream fallback design/implementation

Taken:

- Voeg listenKey functies toe als adapterlaag.
- Parse execution reports naar lifecycle.
- Keepalive status zichtbaar maken.
- REST fallback behouden.

Acceptatie:

- Stream parser tests dekken lifecycle update.
- REST fallback werkt zonder stream.
- Dashboard toont fallback status.

### Fase 7: Pilot reports en support bundle

Taken:

- Breid session report uit met demo pilot summary.
- Voeg reconciliation issues toe.
- Voeg balances before/after toe.
- Voeg reject/error counters toe.
- Voeg support bundle metadata toe zonder secrets.

Acceptatie:

- Pilot report is lokaal exporteerbaar.
- Rapport bevat geen keys/secrets.
- Open orders/cancel events staan in report.

### Fase 8: Tests en afronding

Taken:

- Unit tests voor pilot config.
- Unit tests voor reconciler.
- Unit tests voor account sync.
- Runtime smoke test met fake Demo Spot adapter.
- Dashboard import test.
- Cancel-on-stop test.
- Resume-with-open-orders test.
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
- Geen secrets in logs, reports, session events, screenshots of support bundles.
- Demo trading vereist expliciete arm-actie.
- Unknown/orphan open orders blokkeren nieuwe demo orders.
- Cancel-on-stop moet auditbaar zijn.
- Risk engine mag niet worden omzeild.
- Live trading blijft disabled.
- LLM mag geen autonome orders plaatsen.

## Definition of Done

Roadmap 018 is volledig afgewerkt wanneer:

- Demo pilot presets bestaan.
- Clean-start checks open orders detecteren.
- Order reconciliation known, unknown en orphan orders verwerkt.
- Demo account sync balances toont.
- Runtime counters en endurance guards werken.
- Stop/disarm/cancel policy werkt.
- Dashboard Demo Pilot pagina de volledige flow zichtbaar maakt.
- Pilot reports reconciliation, balances, orders en errors bevatten.
- User data stream fallback of minimaal REST fallback helder werkt.
- Tests en `check-all` groen zijn.
- Roadmapbestand wordt verplaatst naar `Voltooid docs/`.

## Aanbevolen eerste implementatiestap

Start met:

1. `DemoPilotConfig`.
2. `DemoOrderReconciler`.
3. Tests met fake Demo Spot adapter.
4. Dashboard clean-start/reconciliation summary.

Daarna pas endurance timers en user data stream integratie toevoegen.
