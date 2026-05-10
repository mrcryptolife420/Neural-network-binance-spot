# Roadmap 019: Dashboard UX, Demo Pilot Operator Flow en Live Ops Polish

## Status

Voltooid.

Deze roadmap bouwt direct voort op roadmaps 001 t/m 018. De backend heeft nu een veilige lokale botbasis, model governance, one-click Windows start, Binance Demo Spot connect/arm flow, order reconciliation, clean-start checks, account sync, cancel-on-stop en demo pilot rapportage. Roadmap 019 richt zich daarom niet op nieuwe tradinglogica, maar op de operatorervaring:

**Maak het dashboard voelen als één professionele lokale trading control app in plaats van losse technische tabs.**

Live trading blijft buiten scope en disabled.

## Waarom deze roadmap nu de beste volgende stap is

De technische fundamenten zijn aanwezig:

- Demo Spot connectie en credentials flow.
- Armed demo execution.
- Risk engine blijft deterministisch.
- Order lifecycle en reconciliation.
- Demo account sync.
- Demo pilot presets en counters.
- Pilot reports.
- One-click Windows start.

De grootste resterende zwakte is bruikbaarheid. De gebruiker moet in één oogopslag kunnen zien:

- Ben ik verbonden?
- Welke mode/profile/base URL is actief?
- Is de bot armed?
- Mag hij demo orders plaatsen?
- Waarom is trading geblokkeerd?
- Welke order is in welke lifecycle stap?
- Zijn er open/orphan/unknown orders?
- Wat moet ik nu doen?

## Hoofddoel

Maak één duidelijke operatorflow:

1. Start dashboard.
2. Connect Binance Demo Spot.
3. Check account en clean start.
4. Kies pilot preset.
5. Arm demo trading.
6. Start pilot.
7. Monitor signal -> risk -> order -> reconciliation -> fill/cancel.
8. Stop/disarm/cancel open orders.
9. Export pilot report.

## Scope

In scope:

- Dashboard herstructureren rond Demo Pilot.
- Minder technische ruis op primaire schermen.
- Statusbalk en action bar.
- Operator checklist.
- Visual trading pipeline.
- Chart polish met signal/order/fill/reconciliation markers.
- Demo Pilot control panel.
- Betere HTML/Markdown pilot reports.
- Windows one-click start polish.
- Dashboard render/import tests.
- Report tests en no-secret checks.

Niet in scope:

- Binance live trading.
- Nieuwe exchange-integraties.
- Nieuwe ML-strategie.
- RL.
- Autonome LLM-orders.
- Futures/margin.

## Bestaande infrastructuur die moet worden hergebruikt

Niet opnieuw bouwen:

- `ui/streamlit_app.py`
- `ui/components.py`
- `ui/charts.py`
- `demo_pilot.py`
- `demo_spot.py`
- `runtime.py`
- `order_lifecycle.py`
- `session_report.py`
- `html_reports.py`
- `control_center.py`
- `settings_store.py`
- `readiness.py`
- `check_all.py`

Nieuwe code moet bestaande componenten uitbreiden of helpen renderen.

## UX-principes

- Primary UI toont badges, tabellen en duidelijke acties.
- Raw JSON alleen in expanders/debug.
- Live disabled altijd zichtbaar.
- Demo Spot base URL altijd zichtbaar.
- Blocks moeten exacte reden tonen.
- Operator moet weten wat de volgende veilige actie is.
- Buttons voor gevaarlijke acties moeten expliciet zijn:
  - disarm;
  - cancel open demo orders;
  - stop pilot.
- Dashboard moet lokaal op Windows bruikbaar blijven.

## Fase 1: Dashboard informatiearchitectuur

Taken:

- Herstructureer tabs zodat `Demo Pilot` centraal staat.
- Maak top-level status header altijd scanbaar.
- Voeg action bar toe met:
  - Connect;
  - Test connection;
  - Reconcile now;
  - Arm;
  - Disarm;
  - Stop;
  - Cancel open demo orders;
  - Export report.
- Verplaats minder belangrijke technische details naar expanders.

Acceptatiecriteria:

- Operator ziet binnen 5 seconden status en volgende actie.
- Live disabled is zichtbaar.
- Demo Spot base URL is zichtbaar.
- Geen raw JSON als primaire content.

## Fase 2: Operator checklist

Taken:

- Voeg checklistcomponent toe:
  - profile is Binance Demo Spot;
  - credentials loaded;
  - connection ok;
  - server time ok;
  - account canTrade;
  - clean start ok;
  - no orphan orders;
  - risk limits set;
  - pilot preset selected;
  - armed.
- Toon pass/fail/warning per item.
- Toon exacte blocker reason.

Acceptatiecriteria:

- Arm/start is visueel verklaarbaar.
- Als iets blokkeert, toont dashboard waarom.
- Checklist gebruikt bestaande runtime/connectivity/reconciliation payloads.

## Fase 3: Visual trading pipeline

Taken:

- Maak pipelinecomponent:
  - Signal;
  - Risk;
  - Intent;
  - Test order;
  - Demo order;
  - Reconciliation;
  - Fill/Cancel/Reject.
- Toon per stap:
  - status;
  - timestamp;
  - korte reden;
  - model/order id waar relevant.
- Voeg reject/error panel toe.

Acceptatiecriteria:

- Laatste tick/orderflow is begrijpelijk zonder logs.
- Rejects en reconciliation failures zijn direct zichtbaar.
- Pipeline blijft werken zonder actieve order.

## Fase 4: Chart polish

Taken:

- Breid `ui/charts.py` uit:
  - signal markers;
  - fill markers;
  - open order markers;
  - reconciliation markers;
  - equity/PnL panel.
- Zorg dat chart niet crasht bij lege data.
- Houd kleuren rustig en functioneel.

Acceptatiecriteria:

- Candles, signals en fills zijn visueel onderscheidbaar.
- Open orders/reconciliation events kunnen worden weergegeven.
- Dashboard import test blijft groen.

## Fase 5: Demo Pilot control panel

Taken:

- Toon pilot preset details:
  - duration;
  - max orders;
  - max rejects;
  - max API errors;
  - max reconciliation failures;
  - cancel-on-stop policy.
- Toon timer/counters.
- Toon stop reason.
- Toon resume-required status.
- Voeg buttons toe:
  - reconcile now;
  - cancel open demo orders;
  - export pilot report;
  - reset local runtime.

Acceptatiecriteria:

- Operator kan pilot bedienen vanuit één panel.
- Counters en limieten zijn naast elkaar zichtbaar.
- Resume-required status is duidelijk.

## Fase 6: Betere pilot reports

Taken:

- Breid HTML/Markdown reports uit met:
  - executive summary;
  - connection/account summary;
  - pilot config;
  - counters;
  - order lifecycle;
  - reconciliation issues;
  - balances before/after;
  - alerts;
  - operator checklist snapshot.
- Voeg links/paths toe in dashboard.
- Houd reports redacted.

Acceptatiecriteria:

- Pilot report is leesbaar zonder JSON te openen.
- Geen secrets in report.
- Report bevat order/reconciliation/cancel events.

## Fase 7: Windows one-click polish

Taken:

- Zorg dat startscript duidelijke output geeft:
  - dashboard URL;
  - log pad;
  - live disabled;
  - how to close.
- Voeg eventueel shortcut generator toe voor desktop.
- Zorg dat dashboard opent op de centrale Demo Pilot view waar haalbaar.

Acceptatiecriteria:

- Dubbelklikervaring is duidelijk.
- Foutmelding verwijst naar logbestand.
- Geen extra terminalkennis nodig.

## Fase 8: Tests en afronding

Taken:

- Tests voor checklist payload.
- Tests voor pipeline payload.
- Tests voor chart helpers met lege data.
- Tests voor report artifact.
- Dashboard import test.
- `check-all`.
- Secret scan.

Acceptatiecriteria:

- `python -m unittest discover -s tests` groen.
- `python -m binance_spot_bot.cli check-all --json` groen.
- Geen secret artifacts.
- Live trading blijft disabled.
- Roadmap wordt pas daarna naar `Voltooid docs/` verplaatst.

## Safety regels

- Geen secrets in dashboard, logs, reports of artifacts.
- Geen live trading UI.
- Demo trading blijft achter explicit arm.
- Unknown/orphan orders blijven blockers.
- Risk engine mag niet worden omzeild.
- LLM mag geen autonome tradingacties uitvoeren.

## Definition of Done

Roadmap 019 is volledig afgewerkt wanneer:

- Dashboard heeft centrale Demo Pilot operatorflow.
- Status header/action bar/checklist/pipeline zijn duidelijk.
- Demo Pilot control panel toont preset, timer, counters en limieten.
- Charts tonen signalen/fills/orders/reconciliation zonder crashes.
- Pilot reports zijn leesbaar en redacted.
- Windows one-click output is duidelijker.
- Tests en `check-all` groen zijn.
- Roadmapbestand wordt verplaatst naar `Voltooid docs/`.

## Aanbevolen eerste implementatiestap

Start met:

1. Checklist payload helper.
2. Pipeline payload helper.
3. Dashboard Demo Pilot tab herwerken.
4. Report summary uitbreiden.

Daarna pas chart polish en Windows shortcut polish.

## Uitvoering

Afgewerkt op 2026-05-10.

- Gedeelde operator-checklist en signal-to-order pipeline helpers toegevoegd.
- Demo Pilot dashboard herwerkt rond status, actiebar, checklist, presetlimieten, counters, blockers en technische payloads in expanders.
- Candlestick chart uitgebreid met open demo order markers en reconciliation markers, inclusief lege-data pad.
- Demo pilot rapportage uitgebreid met `demo-pilot.md`, operator checklist, pipeline, orders, alerts en redacted JSON.
- Gerichte roadmap 019 tests toegevoegd voor payloads, charts, rapporten en dashboard import.

## Validatie

- `python -m unittest tests.test_roadmap_019_dashboard_ux tests.test_roadmap_018_demo_pilot_reconciliation` groen: 9 tests.
- `python -m unittest discover -s tests` groen: 98 tests.
- `python -m binance_spot_bot.cli check-all --json` groen.
- `git diff --check` zonder whitespace errors; alleen bestaande Windows line-ending waarschuwingen.
