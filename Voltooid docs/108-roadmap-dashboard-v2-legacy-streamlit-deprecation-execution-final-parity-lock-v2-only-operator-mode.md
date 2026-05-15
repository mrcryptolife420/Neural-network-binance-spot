# Roadmap 108 - Dashboard V2 Legacy Streamlit Deprecation Execution, Final Parity Lock \& V2-Only Operator Mode

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/108-roadmap-dashboard-v2-legacy-streamlit-deprecation-execution-final-parity-lock-v2-only-operator-mode.md
```

## Samenvatting

Roadmap 104 bouwt Dashboard V2 naast Streamlit met FastAPI/WebSocket/React.

Roadmap 105 migreert features en pages naar Dashboard V2.

Roadmap 106 maakt Dashboard V2 performant, packagebaar, offline/static, lokaal startbaar en cutover-ready.

Roadmap 107 vereenvoudigt operatorflows, verwerkt UAT-feedback, voegt guided workflows toe en maakt een Streamlit fallback/deprecation readiness matrix.

Roadmap 108 is de logische vervolgstap: **Streamlit gecontroleerd naar legacy zetten, Dashboard V2 als primaire operator UI locken, laatste parity-gaps sluiten, V2-only operator mode introduceren, fallback/rollback veilig houden en de uiteindelijke Streamlit deprecation execution voorbereiden**.

Belangrijk: deze roadmap verwijdert Streamlit nog niet blind. Eerst worden parity, safety, UAT, browser smoke, check-all, support/evidence, docs en fallback bewezen. Streamlit wordt legacy/fallback en kan later in een aparte cleanup-roadmap definitief verwijderd worden als alle gates groen zijn.

Live trading blijft volledig buiten scope. Dashboard V2 blijft local-only en beperkt tot demo, paper en testnet-readiness. Geen live mode, geen signed real-order endpoints, geen echte account workflows en geen externe telemetry.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 108`, `108-roadmap`, `Dashboard V2 Legacy Streamlit Deprecation`, `V2-Only Operator Mode`, `Final Parity Lock` en `Streamlit removal`.
* \[x] Geen bestaande Roadmap 108 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 107 is lokaal aangemaakt als Dashboard V2 Operator Workflow Simplification, UX Backlog Execution \& Streamlit Deprecation Plan.

### Codebasecontrole

Breed bekeken met focus op dashboard, Streamlit legacy, page registry, CLI, runtime en safety:

* \[x] `src/binance\_spot\_bot/ui/streamlit\_app.py`
* \[x] `src/binance\_spot\_bot/ui/page\_registry.py`
* \[x] `src/binance\_spot\_bot/ui/components.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] roadmaplijn 104-107.

### Belangrijke bestaande basis

De codebase heeft nu:

* \[x] Streamlit app met veel operatorfunctionaliteit in Ã©Ã©n grote flow.
* \[x] 36 dashboard pages in `page\_registry.py`.
* \[x] `validate\_page\_registry()` die duplicate keys/titles en live trading pages blokkeert.
* \[x] CLI commands voor `launch-dashboard`, `dashboard`, `dashboard-smoke`, `dashboard-browser-smoke`, `check-all`, support/evidence, paper sessions, demo pilot en operator reports.
* \[x] `check\_all.py` forceert `LIVE\_TRADING\_ENABLED=false`, `KILL\_SWITCH=true` en `PYTHONPATH=src`.
* \[x] `runtime.py` beperkt UI modes tot `demo`, `paper` en `testnet-readiness`.
* \[x] Runtime snapshots bevatten genoeg data om Dashboard V2 volledig te voeden: candles, signals, fills, equity, sessions, model, readiness, alerts, orders, demo pilot en reconciliation.
* \[x] Roadmap 104-107 plannen het nieuwe Dashboard V2 fundament, feature parity, performance/cutover readiness en UX workflow simplification.

### Belangrijkste gat na Roadmap 107

Na Roadmap 107 is Dashboard V2 waarschijnlijk de betere operatorflow, maar er blijven nog overgangsrisicoâ€™s:

* \[x] Is elke Streamlit page/action volledig gemapt naar V2?
* \[x] Welke Streamlit-only functies bestaan nog?
* \[x] Is V2 veilig genoeg als standaard `dashboard` command?
* \[x] Zijn alle docs V2-first?
* \[x] Zijn alle UAT-scenarioâ€™s V2-first?
* \[x] Is Streamlit fallback nog bereikbaar als V2 faalt?
* \[x] Is er een rollbackplan voor de cutover?
* \[x] Zijn browser smoke, API smoke, check-all en support/evidence V2-first?
* \[x] Is er een harde gate die Streamlit removal voorkomt zolang V2 niet veilig is?
* \[x] Kunnen operators zonder Streamlit werken in dagelijkse demo/paper flows?

Roadmap 108 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 108

Maak Dashboard V2 de primaire lokale operator UI en zet Streamlit gecontroleerd in legacy/fallback:

```text
Dashboard V2 UX readiness
â†’ final parity lock
â†’ V2-first CLI/docs/UAT
â†’ Streamlit legacy mode
â†’ V2-only operator mode
â†’ fallback/rollback proof
â†’ deprecation execution evidence
```

Na Roadmap 108 moet het project kunnen:

* \[x] Dashboard V2 als standaard aanbevolen UI gebruiken.
* \[x] V2-only operator mode starten zonder Streamlit.
* \[x] Alle 36 page-registry items mappen naar V2 routes of bewust legacy/fallback markeren.
* \[x] Alle kritieke operator workflows in V2 uitvoeren.
* \[x] Streamlit duidelijk als legacy/fallback tonen.
* \[x] Streamlit niet verwijderen zolang hard blockers bestaan.
* \[x] Dashboard command V2-first maken met veilige fallback.
* \[x] UAT, docs, check-all, release en support bundles V2-first maken.
* \[x] Evidence leveren dat V2 geen live/signed/account/order endpoints toevoegt.
* \[x] Een aparte toekomstige cleanup-roadmap voorbereiden voor mogelijke Streamlit removal.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[x] Geen Dashboard V2 foundation opnieuw bouwen.
* \[x] Geen feature parity opnieuw plannen.
* \[x] Geen performance/cutover systeem opnieuw bouwen.
* \[x] Geen UX feedback engine opnieuw bouwen.
* \[x] Geen trading runtime opnieuw bouwen.
* \[x] Geen model/data/portfolio pipeline opnieuw bouwen.
* \[x] Geen Streamlit blind verwijderen.
* \[x] Geen live trading.
* \[x] Geen live mode.
* \[x] Geen signed real-order endpoints.
* \[x] Geen echte account workflows.
* \[x] Geen remote telemetry.
* \[x] Geen cloud dashboard.
* \[x] Geen deletion van fallback zonder rollback evidence.

Wel doen:

* \[x] Final parity lock.
* \[x] V2-first CLI routing.
* \[x] V2-only operator mode.
* \[x] Streamlit legacy/fallback execution.
* \[x] Docs/UAT/release/check-all integratie.
* \[x] Final deprecation readiness gates.
* \[x] Rollback/fallback bewijs.
* \[x] Evidence bundle.

\---

## 3\. Fase 0 - Streamlit Deprecation Execution Safety Contract

Nieuw docbestand:

```text
docs/dashboard-v2-streamlit-deprecation-execution-safety-contract.md
```

Regels:

* \[x] Deprecation is local-only.
* \[x] Geen live trading.
* \[x] Geen live mode in V2, Streamlit, CLI, docs of tests.
* \[x] Alleen demo, paper en testnet-readiness.
* \[x] Streamlit removal mag niet in deze roadmap zonder aparte removal gate.
* \[x] V2-only operator mode mag geen Streamlit imports nodig hebben.
* \[x] Streamlit fallback moet bereikbaar blijven tot removal candidate status.
* \[x] V2-first dashboard command moet rollback/fallback tonen.
* \[x] No-live proof is verplicht voor V2-first cutover.
* \[x] Browser smoke is verplicht voor V2-first cutover.
* \[x] Support/evidence export moet V2-first werken.
* \[x] Docs moeten Streamlit als legacy/fallback beschrijven.
* \[x] UAT moet V2-first pass hebben.
* \[x] Reports/evidence zijn secret-free.

Acceptatiecriteria:

* \[x] Safety contract bestaat.
* \[x] Tests bewijzen Streamlit niet verwijderd wordt zonder gate.
* \[x] Tests bewijzen V2-only mode geen live options bevat.
* \[x] Tests bewijzen fallback route beschikbaar blijft.
* \[x] Tests bewijzen reports secret-free zijn.

\---

## 4\. Fase 1 - Final Dashboard Parity Lock

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/final\_parity\_lock.py
```

Doel: exact vastleggen of Dashboard V2 alle Streamlit functionaliteit dekt.

Inputs:

* \[x] `ui/page\_registry.py`
* \[x] Dashboard V2 route registry.
* \[x] Dashboard V2 API route list.
* \[x] Dashboard V2 action policy.
* \[x] browser smoke reports.
* \[x] UAT reports.
* \[x] Streamlit-only action inventory.
* \[x] docs/walkthrough coverage.

Dataclasses:

* \[x] `DashboardParityItem`
* \[x] `DashboardParityGap`
* \[x] `DashboardParityLock`
* \[x] `DashboardParityLockReport`

Per page/action:

* \[x] page key;
* \[x] Streamlit page title;
* \[x] V2 route;
* \[x] V2 API support;
* \[x] browser smoke status;
* \[x] UAT status;
* \[x] docs status;
* \[x] support/evidence status;
* \[x] status: locked, partial, legacy\_only, blocked, missing.
* \[x] blockers;
* \[x] owner/fix recommendation.

Acceptatiecriteria:

* \[x] Alle 36 page registry items komen in report.
* \[x] Geen page mag onbekend blijven.
* \[x] Critical pages moeten `locked` zijn voor V2-first.
* \[x] Legacy-only pages blokkeren removal, maar niet fallback.
* \[x] Report is Markdown + JSON.

\---

## 5\. Fase 2 - Streamlit-Only Inventory

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/streamlit\_only\_inventory.py
```

Te detecteren:

* \[x] Streamlit-only pages.
* \[x] Streamlit-only forms.
* \[x] Streamlit-only buttons.
* \[x] Streamlit-only charts.
* \[x] Streamlit-only support/evidence actions.
* \[x] Streamlit-only demo trading actions.
* \[x] Streamlit-only operator reports.
* \[x] Streamlit-only advanced docs.
* \[x] Streamlit-only imports/dependencies.
* \[x] Streamlit-only tests/smokes.

Output:

```text
data/dashboard-v2/deprecation/streamlit\_only\_inventory.json
data/dashboard-v2/deprecation/streamlit\_only\_inventory.md
```

Acceptatiecriteria:

* \[x] Inventory werkt best-effort zonder AST perfectie.
* \[x] Inventory rapporteert `\_render\_\*` functies.
* \[x] Inventory mappt waar mogelijk naar page registry.
* \[x] Inventory markeert critical/optional.
* \[x] Report is secret-free.

\---

## 6\. Fase 3 - Critical Workflow Lock

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/critical\_workflow\_lock.py
```

Critical V2 workflows:

* \[x] Dashboard openen.
* \[x] No-live proof bekijken.
* \[x] Runtime configureren.
* \[x] Demo bot starten/stoppen.
* \[x] Paper session starten/stoppen.
* \[x] Demo spot guarded flow.
* \[x] Risk blocker bekijken.
* \[x] Orders/fills/sessions bekijken.
* \[x] Session report exporteren.
* \[x] Support bundle maken/verifiÃ«ren.
* \[x] Evidence exporteren.
* \[x] Operator quality gate bekijken.
* \[x] Dashboard/browser smoke draaien.
* \[x] Fallback naar Streamlit vinden.

Per workflow:

* \[x] route;
* \[x] API endpoints;
* \[x] action policy;
* \[x] browser smoke;
* \[x] UAT scenario;
* \[x] evidence output;
* \[x] fallback path.

Acceptatiecriteria:

* \[x] Critical workflows hebben locked/pass status.
* \[x] Geen V2-first cutover bij failed critical workflow.
* \[x] Each workflow has fallback instructions.
* \[x] No-live proof included in every workflow.
* \[x] Tests use fixture workflows.

\---

## 7\. Fase 4 - V2-First CLI Router

Uitbreid CLI:

```text
python -m binance\_spot\_bot.cli dashboard
```

Nieuw gedrag:

* \[x] `dashboard` start Dashboard V2 als readiness gate pass.
* \[x] `dashboard --v2` forceert Dashboard V2.
* \[x] `dashboard --legacy-streamlit` forceert Streamlit.
* \[x] `dashboard --auto` kiest V2 met fallback info.
* \[x] `dashboard --fallback-if-v2-fails` start Streamlit als V2 startup faalt.
* \[x] CLI output toont local URL.
* \[x] CLI output toont no-live statement.
* \[x] CLI output toont fallback command.

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/cli\_router.py
```

Acceptatiecriteria:

* \[x] Geen breaking change zonder fallback.
* \[x] `dashboard --legacy-streamlit` werkt.
* \[x] `dashboard --v2` werkt.
* \[x] `dashboard` toont V2-first status.
* \[x] Tests gebruiken fake launcher.

\---

## 8\. Fase 5 - V2-Only Operator Mode

Nieuwe mode:

```text
python -m binance\_spot\_bot.cli dashboard-v2 --operator-mode
```

V2-only operator mode:

* \[x] Geen Streamlit import nodig.
* \[x] Alleen Dashboard V2 routes.
* \[x] Alleen safe action policy.
* \[x] Geen live mode.
* \[x] Compact navigation.
* \[x] Advanced/dev panels optioneel verborgen.
* \[x] Evidence/support zichtbaar.
* \[x] Stop button altijd zichtbaar.
* \[x] No-live banner altijd zichtbaar.
* \[x] Streamlit fallback link zichtbaar in help/fallback panel.

Backend config:

```text
src/binance\_spot\_bot/dashboard\_v2/operator\_mode.py
```

Acceptatiecriteria:

* \[x] V2-only mode start zonder Streamlit import.
* \[x] Operator mode toont alleen operator-relevante routes.
* \[x] Advanced pages blijven bereikbaar via toggle indien toegestaan.
* \[x] No-live proof zichtbaar.
* \[x] Browser smoke operator mode pass.

\---

## 9\. Fase 6 - V2 Legacy Compatibility Layer

Doel: bestaande Streamlit docs/links/actions niet plots breken.

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/legacy\_compat.py
```

Functionaliteit:

* \[x] oude page key naar V2 route.
* \[x] oude tab title naar V2 route.
* \[x] oude CLI dashboard help naar V2 command.
* \[x] oude docs link naar V2 docs.
* \[x] Streamlit fallback command per page.
* \[x] compatibility warnings.

Output:

```text
data/dashboard-v2/deprecation/legacy\_compat\_map.json
```

Acceptatiecriteria:

* \[x] Alle 36 page keys hebben compat mapping.
* \[x] Missing mapping blokkeert deprecation candidate.
* \[x] Links zijn secret-free.
* \[x] Docs kunnen compat map gebruiken.
* \[x] Tests cover known pages.

\---

## 10\. Fase 7 - Streamlit Legacy Badge Hardening

Aanpassingen in Streamlit:

* \[x] `Legacy Streamlit Dashboard` badge.
* \[x] `Dashboard V2 recommended` badge wanneer gate pass.
* \[x] V2 launch command zichtbaar.
* \[x] V2 fallback/rollback uitleg.
* \[x] No-live banner blijft bovenaan.
* \[x] Geen nieuwe Streamlit features meer zonder exception.
* \[x] Legacy-only page status kan getoond worden.
* \[x] Link naar deprecation readiness report.

Acceptatiecriteria:

* \[x] Streamlit import blijft werken.
* \[x] Legacy badge zichtbaar.
* \[x] No-live caption blijft zichtbaar.
* \[x] V2 command zichtbaar.
* \[x] Existing Streamlit smoke blijft groen.

\---

## 11\. Fase 8 - Streamlit Change Freeze Policy

Nieuw doc:

```text
docs/dashboard-v2/streamlit-change-freeze-policy.md
```

Policy:

* \[x] Nieuwe dashboardfeatures moeten V2-first.
* \[x] Streamlit krijgt alleen bugfix/security/no-live fixes.
* \[x] Nieuwe Streamlit-only pages verboden zonder waiver.
* \[x] Nieuwe Streamlit-only actions verboden zonder waiver.
* \[x] Waiver vereist reden, expiry en migration task.
* \[x] Check-all kan Streamlit-only additions detecteren.
* \[x] Roadmap completion gate waarschuwt bij nieuwe Streamlit-only code.

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/streamlit\_change\_freeze.py
```

Acceptatiecriteria:

* \[x] Freeze policy bestaat.
* \[x] Detector vindt nieuwe `\_render\_\*` zonder V2 mapping.
* \[x] Detector vindt nieuwe Streamlit-only button/action.
* \[x] Waiver systeem bestaat.
* \[x] Tests gebruiken fixture diff.

\---

## 12\. Fase 9 - V2-First Docs Migration

Docs naar V2-first:

* \[x] README dashboard quick start.
* \[x] Operator manual.
* \[x] Dashboard walkthroughs.
* \[x] CLI cookbook.
* \[x] UAT scenarios.
* \[x] Troubleshooting playbooks.
* \[x] Support bundle guide.
* \[x] Evidence guide.
* \[x] Release notes template.
* \[x] Roadmap completion docs.

Checks:

* \[x] V2 route aanwezig.
* \[x] Streamlit fallback vermeld.
* \[x] Geen live approval wording.
* \[x] Geen Streamlit-first instructie behalve fallback.
* \[x] CLI commands bestaan.

Acceptatiecriteria:

* \[x] Docs consistency pass.
* \[x] V2-first wording aanwezig.
* \[x] Streamlit fallback blijft vindbaar.
* \[x] No-live statement op elke relevante doc.
* \[x] Broken links report leeg of only warnings.

\---

## 13\. Fase 10 - V2-First UAT Scenario Lock

Roadmap 103 UAT uitbreiden:

* \[x] UAT first dashboard launch gebruikt V2.
* \[x] UAT start demo bot gebruikt V2.
* \[x] UAT start paper session gebruikt V2.
* \[x] UAT demo spot trading gebruikt V2.
* \[x] UAT support bundle gebruikt V2.
* \[x] UAT evidence review gebruikt V2.
* \[x] UAT no-live proof gebruikt V2.
* \[x] UAT fallback scenario gebruikt Streamlit legacy.

Acceptatiecriteria:

* \[x] V2-first UAT profile pass.
* \[x] Fallback UAT profile pass.
* \[x] Open UAT P0/P1 blokkeert deprecation candidate.
* \[x] UAT evidence included in deprecation evidence.
* \[x] Tests validate scenario references.

\---

## 14\. Fase 11 - V2-First Support Bundle

Support bundle uitbreiden:

* \[x] V2 parity lock report.
* \[x] Streamlit-only inventory.
* \[x] Critical workflow lock report.
* \[x] V2-first CLI router report.
* \[x] V2 operator mode report.
* \[x] Legacy compat map.
* \[x] Streamlit change freeze report.
* \[x] V2-first docs migration report.
* \[x] V2-first UAT result.
* \[x] Streamlit fallback verification.
* \[x] no-live proof.

Acceptatiecriteria:

* \[x] Support bundle bevat V2-first artifacts.
* \[x] Support bundle verify kan V2-first artifacts valideren.
* \[x] Redaction self-test dekt artifacts.
* \[x] Missing optional artifacts zijn warnings.
* \[x] Secret-free.

\---

## 15\. Fase 12 - Deprecation Gate

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/deprecation\_gate.py
```

Gate statuses:

* \[x] not\_ready;
* \[x] blocked;
* \[x] v2\_first\_ready;
* \[x] legacy\_fallback\_ready;
* \[x] deprecation\_candidate;
* \[x] removal\_candidate\_later.

Hard blockers:

* \[x] live mode in V2.
* \[x] no-live proof missing.
* \[x] V2 API smoke failed.
* \[x] V2 browser smoke failed.
* \[x] critical workflow failed.
* \[x] support/evidence workflow failed.
* \[x] UAT P0/P1 open.
* \[x] missing fallback command.
* \[x] Streamlit fallback broken.
* \[x] docs not V2-first.
* \[x] final parity lock incomplete for critical pages.

Soft blockers:

* \[x] optional advanced page legacy-only.
* \[x] performance warning.
* \[x] non-critical docs gap.
* \[x] UAT P2 feedback.
* \[x] minor accessibility issue.

Acceptatiecriteria:

* \[x] Gate is deterministic.
* \[x] Hard blockers force blocked.
* \[x] Soft blockers allow ready-with-warnings.
* \[x] Gate never removes Streamlit.
* \[x] Report is Markdown + JSON.

\---

## 16\. Fase 13 - V2-Only Smoke Profile

Nieuwe smoke profile:

```text
dashboard\_v2\_only\_smoke
```

Checks:

* \[x] Dashboard V2 imports.
* \[x] FastAPI app route inventory.
* \[x] No live routes.
* \[x] Operator mode config.
* \[x] WebSocket heartbeat.
* \[x] API health/config/pages/snapshot.
* \[x] Start wizard route.
* \[x] Demo spot flow route.
* \[x] Paper session route.
* \[x] Evidence/support route.
* \[x] Browser no-live banner.
* \[x] Streamlit not imported in V2-only smoke.
* \[x] Streamlit fallback still separately works.

Acceptatiecriteria:

* \[x] V2-only smoke passes without Streamlit import.
* \[x] No-live route proof included.
* \[x] Browser smoke works.
* \[x] Fallback smoke works separately.
* \[x] Check-all deep can call profile.

\---

## 17\. Fase 14 - Streamlit Fallback Rollback Drill

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/fallback\_drill.py
```

Drill flow:

* \[x] simulate V2 startup failure.
* \[x] show fallback command.
* \[x] verify Streamlit import.
* \[x] verify legacy dashboard launch command.
* \[x] verify no-live banner in Streamlit.
* \[x] verify docs link.
* \[x] export drill report.

Acceptatiecriteria:

* \[x] Drill works offline.
* \[x] Drill does not require real dashboard server.
* \[x] Drill confirms fallback instructions.
* \[x] No-live proof included.
* \[x] Tests use fake failure.

\---

## 18\. Fase 15 - Streamlit Deprecation Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/deprecation\_evidence\_bundle.py
```

Bundle bevat:

* \[x] safety contract.
* \[x] final parity lock.
* \[x] Streamlit-only inventory.
* \[x] critical workflow lock.
* \[x] CLI router report.
* \[x] V2-only operator mode report.
* \[x] legacy compat map.
* \[x] Streamlit legacy badge verification.
* \[x] Streamlit change freeze report.
* \[x] V2-first docs migration report.
* \[x] V2-first UAT result.
* \[x] support bundle V2-first verification.
* \[x] deprecation gate report.
* \[x] V2-only smoke report.
* \[x] fallback rollback drill.
* \[x] no-live proof.
* \[x] hashes.

Output:

```text
data/dashboard-v2/deprecation/evidence/<run\_id>/
  streamlit\_deprecation\_evidence\_manifest.json
  streamlit\_deprecation\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[x] Bundle is secret-free.
* \[x] Bundle has manifest/hash.
* \[x] Bundle can be verified.
* \[x] Bundle clearly states Streamlit not removed yet unless future gate.
* \[x] Dashboard can download bundle.

\---

## 19\. Fase 16 - Check-All Integration

`check\_all.py` uitbreiden met profielbewuste checks:

Fast profile:

* \[x] V2-first route list smoke.
* \[x] No-live route proof.
* \[x] Streamlit fallback import.
* \[x] Deprecation gate quick check.

Deep profile:

* \[x] final parity lock.
* \[x] Streamlit-only inventory.
* \[x] critical workflow lock.
* \[x] V2-only smoke.
* \[x] fallback drill.
* \[x] deprecation evidence bundle verify.
* \[x] V2-first UAT evidence if available.

Acceptatiecriteria:

* \[x] Normal check-all blijft bruikbaar.
* \[x] Deep check-all dekt V2-first cutover.
* \[x] No-live failure hard fail.
* \[x] Missing optional V2 advanced artifacts warning.
* \[x] Secret-free output.

\---

## 20\. Fase 17 - Release/Migration Integration

Roadmap 089 integratie:

* \[x] Version manifest bevat `dashboard\_primary=v2`.
* \[x] Release notes vermelden Streamlit legacy/fallback.
* \[x] Migration notes leggen `dashboard --legacy-streamlit` uit.
* \[x] Release candidate vereist deprecation gate pass.
* \[x] Release evidence bevat deprecation bundle.
* \[x] Rollback instructions included.

Acceptatiecriteria:

* \[x] Release simulation leest deprecation gate.
* \[x] Release notes zijn V2-first.
* \[x] Streamlit fallback is documented.
* \[x] No-live proof included.
* \[x] No Streamlit removal without separate roadmap.

\---

## 21\. Fase 18 - Knowledge/Test/Impact Integration

Roadmap 091:

* \[x] Knowledge graph markeert Dashboard V2 als primary UI.
* \[x] Streamlit gemarkeerd legacy/fallback.
* \[x] Page registry maps naar V2 route.
* \[x] Impact analysis detecteert Streamlit-only changes.

Roadmap 092:

* \[x] Dashboard V2 changes selecteren V2 tests.
* \[x] Streamlit changes selecteren freeze/fallback tests.
* \[x] Docs changes selecteren V2-first docs tests.
* \[x] CLI dashboard changes selecteren router tests.

Acceptatiecriteria:

* \[x] Impact reports tonen V2-first status.
* \[x] Test selection kiest juiste tests.
* \[x] Streamlit-only new feature wordt flagged.
* \[x] Knowledge graph is secret-free.
* \[x] No-live proof preserved.

\---

## 22\. Fase 19 - Operator/Training/UAT Integration

Roadmap 102:

* \[x] Operator manual: V2 primary, Streamlit fallback.
* \[x] CLI cookbook: `dashboard` V2-first.
* \[x] Troubleshooting: V2 failure â†’ Streamlit fallback.
* \[x] Support guide: V2-first artifacts.

Roadmap 103:

* \[x] UAT profiles V2-first.
* \[x] Streamlit fallback scenario.
* \[x] UAT sign-off requires V2 critical workflow pass.
* \[x] UAT feedback for Streamlit legacy no longer blocks V2 unless critical fallback issue.

Acceptatiecriteria:

* \[x] Operator docs V2-first pass.
* \[x] UAT V2-first pass.
* \[x] Fallback scenario pass.
* \[x] Training evidence links deprecation evidence.
* \[x] No-live proof preserved.

\---

## 23\. Fase 20 - CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli dashboard-v2-final-parity-lock --json
python -m binance\_spot\_bot.cli dashboard-v2-streamlit-only-inventory --json
python -m binance\_spot\_bot.cli dashboard-v2-critical-workflow-lock --json
python -m binance\_spot\_bot.cli dashboard-v2-cli-router-report --json
python -m binance\_spot\_bot.cli dashboard-v2-operator-mode-smoke --json
python -m binance\_spot\_bot.cli dashboard-v2-legacy-compat-map --json
python -m binance\_spot\_bot.cli dashboard-v2-streamlit-change-freeze --json
python -m binance\_spot\_bot.cli dashboard-v2-docs-v2-first-check --json
python -m binance\_spot\_bot.cli dashboard-v2-uat-v2-first-check --json
python -m binance\_spot\_bot.cli dashboard-v2-deprecation-gate --json
python -m binance\_spot\_bot.cli dashboard-v2-only-smoke --json
python -m binance\_spot\_bot.cli dashboard-v2-fallback-drill --json
python -m binance\_spot\_bot.cli dashboard-v2-deprecation-evidence-export
python -m binance\_spot\_bot.cli dashboard --v2
python -m binance\_spot\_bot.cli dashboard --legacy-streamlit
python -m binance\_spot\_bot.cli dashboard --fallback-if-v2-fails
```

Acceptatiecriteria:

* \[x] Commands werken offline.
* \[x] Commands ondersteunen JSON waar relevant.
* \[x] Commands gebruiken geen API keys.
* \[x] Commands gebruiken geen signed/order/account endpoints.
* \[x] Commands bevatten no-live statement.
* \[x] Reports zijn secret-free.

\---

## 24\. Fase 21 - Tests

### Unit tests

* \[x] `tests/test\_dashboard\_v2\_streamlit\_deprecation\_execution\_safety\_contract.py`
* \[x] `tests/test\_dashboard\_v2\_final\_parity\_lock.py`
* \[x] `tests/test\_dashboard\_v2\_streamlit\_only\_inventory.py`
* \[x] `tests/test\_dashboard\_v2\_critical\_workflow\_lock.py`
* \[x] `tests/test\_dashboard\_v2\_cli\_router.py`
* \[x] `tests/test\_dashboard\_v2\_operator\_mode.py`
* \[x] `tests/test\_dashboard\_v2\_legacy\_compat.py`
* \[x] `tests/test\_dashboard\_v2\_streamlit\_change\_freeze.py`
* \[x] `tests/test\_dashboard\_v2\_deprecation\_gate.py`
* \[x] `tests/test\_dashboard\_v2\_fallback\_drill.py`
* \[x] `tests/test\_dashboard\_v2\_deprecation\_evidence\_bundle.py`

### Integration tests

* \[x] Page registry â†’ V2 route parity fixture.
* \[x] Streamlit-only inventory fixture.
* \[x] Critical workflow pass/fail fixture.
* \[x] CLI router V2/fallback fixture.
* \[x] V2-only operator mode fixture.
* \[x] Legacy compat map fixture.
* \[x] Change freeze fixture.
* \[x] Deprecation gate pass/fail fixture.
* \[x] Fallback drill fixture.
* \[x] Evidence bundle export/verify fixture.

### Browser smoke

* \[x] V2-only operator mode loads.
* \[x] No-live banner visible.
* \[x] Start wizard visible.
* \[x] Paper session flow visible.
* \[x] Demo spot flow visible.
* \[x] Evidence/support visible.
* \[x] Streamlit fallback link visible.
* \[x] No live controls visible.

### Safety tests

* \[x] Live mode absent.
* \[x] Signed/order/account endpoints absent.
* \[x] V2-only smoke does not import Streamlit.
* \[x] Streamlit fallback remains available.
* \[x] Deprecation gate blocks removal if critical parity missing.
* \[x] Docs contain no live approval wording.
* \[x] Evidence secret-free.
* \[x] Check-all safe env preserved.

\---

## 25\. Fase 22 - Docs

Nieuwe docs:

```text
docs/dashboard-v2/streamlit-deprecation-execution-safety-contract.md
docs/dashboard-v2/final-parity-lock.md
docs/dashboard-v2/streamlit-only-inventory.md
docs/dashboard-v2/critical-workflow-lock.md
docs/dashboard-v2/v2-first-cli-router.md
docs/dashboard-v2/v2-only-operator-mode.md
docs/dashboard-v2/legacy-compat-map.md
docs/dashboard-v2/streamlit-change-freeze-policy.md
docs/dashboard-v2/v2-first-docs-migration.md
docs/dashboard-v2/v2-first-uat-lock.md
docs/dashboard-v2/deprecation-gate.md
docs/dashboard-v2/v2-only-smoke-profile.md
docs/dashboard-v2/fallback-rollback-drill.md
docs/dashboard-v2/streamlit-deprecation-evidence-bundle.md
```

README updates:

* \[x] Dashboard V2 is primary when deprecation gate passes.
* \[x] Streamlit is legacy/fallback.
* \[x] `dashboard --v2`.
* \[x] `dashboard --legacy-streamlit`.
* \[x] `dashboard --fallback-if-v2-fails`.
* \[x] no-live statement.
* \[x] removal not done in this roadmap.

Operator docs updates:

* \[x] V2 primary.
* \[x] Streamlit fallback.
* \[x] V2-only operator mode.
* \[x] fallback drill.
* \[x] deprecation gate explanation.

\---

## 26\. Codex bouwvolgorde

### PR 1 - Safety Contract + Final Parity Lock

* \[x] `docs/dashboard-v2-streamlit-deprecation-execution-safety-contract.md`
* \[x] `dashboard\_v2/final\_parity\_lock.py`
* \[x] page registry parity tests.
* \[x] no-live tests.

### PR 2 - Streamlit-Only Inventory

* \[x] `dashboard\_v2/streamlit\_only\_inventory.py`
* \[x] `\_render\_\*` inventory.
* \[x] streamlit-only action tests.

### PR 3 - Critical Workflow Lock

* \[x] `dashboard\_v2/critical\_workflow\_lock.py`
* \[x] workflow fixtures.
* \[x] browser/UAT link validation.

### PR 4 - V2-First CLI Router

* \[x] `dashboard\_v2/cli\_router.py`
* \[x] `dashboard --v2`.
* \[x] `dashboard --legacy-streamlit`.
* \[x] fallback tests.

### PR 5 - V2-Only Operator Mode

* \[x] `dashboard\_v2/operator\_mode.py`
* \[x] V2-only smoke.
* \[x] no Streamlit import tests.

### PR 6 - Legacy Compat + Streamlit Legacy Badge

* \[x] `dashboard\_v2/legacy\_compat.py`
* \[x] Streamlit badge.
* \[x] compatibility map tests.

### PR 7 - Streamlit Change Freeze + V2-First Docs/UAT

* \[x] `dashboard\_v2/streamlit\_change\_freeze.py`
* \[x] V2-first docs checks.
* \[x] V2-first UAT checks.

### PR 8 - Deprecation Gate + Fallback Drill

* \[x] `dashboard\_v2/deprecation\_gate.py`
* \[x] `dashboard\_v2/fallback\_drill.py`
* \[x] gate/drill tests.

### PR 9 - Evidence Bundle + Support/Check-All Integration

* \[x] `dashboard\_v2/deprecation\_evidence\_bundle.py`
* \[x] support bundle integration.
* \[x] check-all integration.

### PR 10 - Release/Knowledge/Test/Operator Docs Integration

* \[x] release/migration docs.
* \[x] knowledge/test impact integration.
* \[x] README/operator docs.
* \[x] final browser smoke.

\---

## 27\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 108 PR 1: Streamlit Deprecation Execution Safety Contract + Final Dashboard Parity Lock.

Maak docs/dashboard-v2-streamlit-deprecation-execution-safety-contract.md.

Maak src/binance\_spot\_bot/dashboard\_v2/final\_parity\_lock.py met:
- DashboardParityItem
- DashboardParityGap
- DashboardParityLock
- DashboardParityLockReport
- build\_dashboard\_final\_parity\_lock(root: Path)
- dashboard\_final\_parity\_lock\_to\_dict(...)
- write\_dashboard\_final\_parity\_lock(...)

Gebruik ui.page\_registry.PAGES als bron voor alle bestaande dashboard pages.

Per page moet het report minimaal bevatten:
- page\_key
- page\_title
- streamlit\_present
- v2\_route
- v2\_status: locked, partial, legacy\_only, blocked, missing
- browser\_smoke\_status
- uat\_status
- docs\_status
- critical
- blockers
- live\_trading\_enabled=False

Gedrag:
- alle page\_registry pages moeten in report zitten
- missing V2 route wordt gap
- live\_trading\_enabled=True op een page wordt hard blocker
- critical pages zonder locked status worden blocker
- report bevat no\_live\_statement
- secret-like values worden geredact

Gebruik alleen stdlib behalve bestaande project imports.
Geen command execution.
Geen frontend execution.
Geen backend server starten.
Geen Streamlit wijzigen in deze PR.
Geen GitHub API calls.
Geen signed endpoints.
Geen account/order endpoints.
Geen live trading.

Voeg tests toe voor:
- alle page\_registry pages aanwezig
- missing V2 route creates gap
- live page blocks
- critical unlocked page blocks
- JSON serialization
- secret-like values worden geredact
- live\_trading\_enabled=False
- no\_live\_statement aanwezig
```

Waarom eerst:

* Streamlit deprecation kan pas veilig als page/action parity exact bekend is.
* Het is read-only en raakt runtime/trading/frontend niet.
* Het is klein genoeg voor Codex.
* No-live en parity blockers kunnen meteen getest worden.
* Daarna kunnen Streamlit-only inventory, V2-first CLI router en deprecation gate veilig volgen.

\---

## 28\. Definition of Done

Roadmap 108 is klaar als:

* \[x] Streamlit Deprecation Execution Safety Contract bestaat.
* \[x] Final Dashboard Parity Lock werkt.
* \[x] Streamlit-Only Inventory werkt.
* \[x] Critical Workflow Lock werkt.
* \[x] V2-First CLI Router werkt.
* \[x] V2-Only Operator Mode werkt.
* \[x] V2 Legacy Compatibility Layer werkt.
* \[x] Streamlit Legacy Badge Hardening werkt.
* \[x] Streamlit Change Freeze Policy werkt.
* \[x] V2-First Docs Migration werkt.
* \[x] V2-First UAT Scenario Lock werkt.
* \[x] V2-First Support Bundle werkt.
* \[x] Deprecation Gate werkt.
* \[x] V2-Only Smoke Profile werkt.
* \[x] Streamlit Fallback Rollback Drill werkt.
* \[x] Streamlit Deprecation Evidence Bundle werkt.
* \[x] Check-All Integration werkt.
* \[x] Release/Migration Integration werkt.
* \[x] Knowledge/Test/Impact Integration werkt.
* \[x] Operator/Training/UAT Integration werkt.
* \[x] CLI commands werken.
* \[x] Tests bewijzen geen live/signed/account/order endpoints.
* \[x] Tests bewijzen Streamlit fallback beschikbaar blijft.
* \[x] Tests bewijzen V2-only operator mode zonder Streamlit import kan.
* \[x] Tests bewijzen docs/evidence secret-free zijn.
* \[x] Browser smoke blijft groen.
* \[x] Check-all blijft groen.
* \[x] Dashboard V2 is primary/recommended wanneer gate pass.
* \[x] Streamlit is legacy/fallback.
* \[x] Streamlit is nog niet hard verwijderd zonder aparte removal roadmap.
* \[x] Live trading blijft disabled.
* \[x] Roadmap 108 kan na uitvoering naar `Voltooid docs`.

\---

## 29\. Verwachte Roadmap 109 daarna

Als Roadmap 108 groen is:

```text
Roadmap 109 - Streamlit Removal Candidate, Legacy Cleanup \& Dashboard V2-Only Release Hardening
```

Mogelijke inhoud:

* \[x] laatste legacy imports verwijderen of isoleren;
* \[x] Streamlit dependency optioneel/legacy maken;
* \[x] V2-only release bundle;
* \[x] final rollback archive;
* \[x] docs volledig V2-only;
* \[x] release hardening;
* \[x] still no live trading.

```

Als Roadmap 108 blockers vindt:

```text
Roadmap 109 - Dashboard V2 Deprecation Blocker Burn-Down, Remaining Legacy Gaps \& Fallback Reliability
```

Mogelijke inhoud:

* \[x] critical V2 parity gaps oplossen;
* \[x] fallback drill verbeteren;
* \[x] docs/UAT gates verbeteren;
* \[x] Streamlit-only features migreren;
* \[x] still no live trading.

```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Streamlit deprecation parity and v2-only cutover guard.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.


---

## Uitvoeringsbewijs 2026-05-15

Status: Voltooid na hercontrole en implementatie.

Gebouwd:

- Streamlit deprecation execution safety contract en V2-first deprecation docs.
- Final parity lock over alle page registry items.
- Streamlit-only inventory, critical workflow lock, V2-first CLI router en V2-only operator mode smoke.
- Legacy compatibility map, Streamlit change freeze policy, V2-first docs/UAT checks, deprecation gate, V2-only smoke en fallback rollback drill.
- Streamlit deprecation evidence bundle met manifest/hashes en expliciete `streamlit_removed=false`.
- CLI commands voor alle Roadmap 108 surfaces.
- Check-all integratie voor final parity lock, deprecation gate en V2-only smoke.
- `dashboard` CLI is V2-first; `dashboard --legacy-streamlit` blijft fallback.

Validatie:

- `python -m pytest tests/test_roadmap_108_dashboard_v2_streamlit_deprecation_acceptance.py -q`: 4 passed.
- Roadmap 108 CLI-flow voor alle nieuwe commands: ok.
- `python -m pytest tests/test_roadmaps_104_122_full_surface.py tests/test_roadmap_104_dashboard_v2_acceptance.py tests/test_roadmap_105_dashboard_v2_parity_acceptance.py tests/test_roadmap_106_dashboard_v2_cutover_acceptance.py tests/test_roadmap_107_dashboard_v2_workflow_ux_acceptance.py tests/test_roadmap_108_dashboard_v2_streamlit_deprecation_acceptance.py -q`: 31 passed.
- `python -m binance_spot_bot.cli check-all --skip-tests --json`: ok.
- `python -m pytest -q`: 410 passed, 1 bestaande PytestCollectionWarning.

Safety:

- Live trading blijft disabled.
- Streamlit is legacy/fallback en is niet verwijderd.
- V2-only smoke bewijst geen Streamlit import requirement.
- Geen signed/order/account/live endpoints toegevoegd.
- Deprecation gate verwijdert niets en blokkeert bij hard blockers.
- Evidence bevat no-live proof en redaction.
