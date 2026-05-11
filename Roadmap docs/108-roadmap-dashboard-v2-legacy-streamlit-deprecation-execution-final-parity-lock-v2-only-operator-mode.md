# Roadmap 108 - Dashboard V2 Legacy Streamlit Deprecation Execution, Final Parity Lock \& V2-Only Operator Mode

Status: Nieuw / Gepland  
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

* \[x] Streamlit app met veel operatorfunctionaliteit in één grote flow.
* \[x] 36 dashboard pages in `page\_registry.py`.
* \[x] `validate\_page\_registry()` die duplicate keys/titles en live trading pages blokkeert.
* \[x] CLI commands voor `launch-dashboard`, `dashboard`, `dashboard-smoke`, `dashboard-browser-smoke`, `check-all`, support/evidence, paper sessions, demo pilot en operator reports.
* \[x] `check\_all.py` forceert `LIVE\_TRADING\_ENABLED=false`, `KILL\_SWITCH=true` en `PYTHONPATH=src`.
* \[x] `runtime.py` beperkt UI modes tot `demo`, `paper` en `testnet-readiness`.
* \[x] Runtime snapshots bevatten genoeg data om Dashboard V2 volledig te voeden: candles, signals, fills, equity, sessions, model, readiness, alerts, orders, demo pilot en reconciliation.
* \[x] Roadmap 104-107 plannen het nieuwe Dashboard V2 fundament, feature parity, performance/cutover readiness en UX workflow simplification.

### Belangrijkste gat na Roadmap 107

Na Roadmap 107 is Dashboard V2 waarschijnlijk de betere operatorflow, maar er blijven nog overgangsrisico’s:

* \[ ] Is elke Streamlit page/action volledig gemapt naar V2?
* \[ ] Welke Streamlit-only functies bestaan nog?
* \[ ] Is V2 veilig genoeg als standaard `dashboard` command?
* \[ ] Zijn alle docs V2-first?
* \[ ] Zijn alle UAT-scenario’s V2-first?
* \[ ] Is Streamlit fallback nog bereikbaar als V2 faalt?
* \[ ] Is er een rollbackplan voor de cutover?
* \[ ] Zijn browser smoke, API smoke, check-all en support/evidence V2-first?
* \[ ] Is er een harde gate die Streamlit removal voorkomt zolang V2 niet veilig is?
* \[ ] Kunnen operators zonder Streamlit werken in dagelijkse demo/paper flows?

Roadmap 108 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 108

Maak Dashboard V2 de primaire lokale operator UI en zet Streamlit gecontroleerd in legacy/fallback:

```text
Dashboard V2 UX readiness
→ final parity lock
→ V2-first CLI/docs/UAT
→ Streamlit legacy mode
→ V2-only operator mode
→ fallback/rollback proof
→ deprecation execution evidence
```

Na Roadmap 108 moet het project kunnen:

* \[ ] Dashboard V2 als standaard aanbevolen UI gebruiken.
* \[ ] V2-only operator mode starten zonder Streamlit.
* \[ ] Alle 36 page-registry items mappen naar V2 routes of bewust legacy/fallback markeren.
* \[ ] Alle kritieke operator workflows in V2 uitvoeren.
* \[ ] Streamlit duidelijk als legacy/fallback tonen.
* \[ ] Streamlit niet verwijderen zolang hard blockers bestaan.
* \[ ] Dashboard command V2-first maken met veilige fallback.
* \[ ] UAT, docs, check-all, release en support bundles V2-first maken.
* \[ ] Evidence leveren dat V2 geen live/signed/account/order endpoints toevoegt.
* \[ ] Een aparte toekomstige cleanup-roadmap voorbereiden voor mogelijke Streamlit removal.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen Dashboard V2 foundation opnieuw bouwen.
* \[ ] Geen feature parity opnieuw plannen.
* \[ ] Geen performance/cutover systeem opnieuw bouwen.
* \[ ] Geen UX feedback engine opnieuw bouwen.
* \[ ] Geen trading runtime opnieuw bouwen.
* \[ ] Geen model/data/portfolio pipeline opnieuw bouwen.
* \[ ] Geen Streamlit blind verwijderen.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte account workflows.
* \[ ] Geen remote telemetry.
* \[ ] Geen cloud dashboard.
* \[ ] Geen deletion van fallback zonder rollback evidence.

Wel doen:

* \[ ] Final parity lock.
* \[ ] V2-first CLI routing.
* \[ ] V2-only operator mode.
* \[ ] Streamlit legacy/fallback execution.
* \[ ] Docs/UAT/release/check-all integratie.
* \[ ] Final deprecation readiness gates.
* \[ ] Rollback/fallback bewijs.
* \[ ] Evidence bundle.

\---

## 3\. Fase 0 - Streamlit Deprecation Execution Safety Contract

Nieuw docbestand:

```text
docs/dashboard-v2-streamlit-deprecation-execution-safety-contract.md
```

Regels:

* \[ ] Deprecation is local-only.
* \[ ] Geen live trading.
* \[ ] Geen live mode in V2, Streamlit, CLI, docs of tests.
* \[ ] Alleen demo, paper en testnet-readiness.
* \[ ] Streamlit removal mag niet in deze roadmap zonder aparte removal gate.
* \[ ] V2-only operator mode mag geen Streamlit imports nodig hebben.
* \[ ] Streamlit fallback moet bereikbaar blijven tot removal candidate status.
* \[ ] V2-first dashboard command moet rollback/fallback tonen.
* \[ ] No-live proof is verplicht voor V2-first cutover.
* \[ ] Browser smoke is verplicht voor V2-first cutover.
* \[ ] Support/evidence export moet V2-first werken.
* \[ ] Docs moeten Streamlit als legacy/fallback beschrijven.
* \[ ] UAT moet V2-first pass hebben.
* \[ ] Reports/evidence zijn secret-free.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen Streamlit niet verwijderd wordt zonder gate.
* \[ ] Tests bewijzen V2-only mode geen live options bevat.
* \[ ] Tests bewijzen fallback route beschikbaar blijft.
* \[ ] Tests bewijzen reports secret-free zijn.

\---

## 4\. Fase 1 - Final Dashboard Parity Lock

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/final\_parity\_lock.py
```

Doel: exact vastleggen of Dashboard V2 alle Streamlit functionaliteit dekt.

Inputs:

* \[ ] `ui/page\_registry.py`
* \[ ] Dashboard V2 route registry.
* \[ ] Dashboard V2 API route list.
* \[ ] Dashboard V2 action policy.
* \[ ] browser smoke reports.
* \[ ] UAT reports.
* \[ ] Streamlit-only action inventory.
* \[ ] docs/walkthrough coverage.

Dataclasses:

* \[ ] `DashboardParityItem`
* \[ ] `DashboardParityGap`
* \[ ] `DashboardParityLock`
* \[ ] `DashboardParityLockReport`

Per page/action:

* \[ ] page key;
* \[ ] Streamlit page title;
* \[ ] V2 route;
* \[ ] V2 API support;
* \[ ] browser smoke status;
* \[ ] UAT status;
* \[ ] docs status;
* \[ ] support/evidence status;
* \[ ] status: locked, partial, legacy\_only, blocked, missing.
* \[ ] blockers;
* \[ ] owner/fix recommendation.

Acceptatiecriteria:

* \[ ] Alle 36 page registry items komen in report.
* \[ ] Geen page mag onbekend blijven.
* \[ ] Critical pages moeten `locked` zijn voor V2-first.
* \[ ] Legacy-only pages blokkeren removal, maar niet fallback.
* \[ ] Report is Markdown + JSON.

\---

## 5\. Fase 2 - Streamlit-Only Inventory

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/streamlit\_only\_inventory.py
```

Te detecteren:

* \[ ] Streamlit-only pages.
* \[ ] Streamlit-only forms.
* \[ ] Streamlit-only buttons.
* \[ ] Streamlit-only charts.
* \[ ] Streamlit-only support/evidence actions.
* \[ ] Streamlit-only demo trading actions.
* \[ ] Streamlit-only operator reports.
* \[ ] Streamlit-only advanced docs.
* \[ ] Streamlit-only imports/dependencies.
* \[ ] Streamlit-only tests/smokes.

Output:

```text
data/dashboard-v2/deprecation/streamlit\_only\_inventory.json
data/dashboard-v2/deprecation/streamlit\_only\_inventory.md
```

Acceptatiecriteria:

* \[ ] Inventory werkt best-effort zonder AST perfectie.
* \[ ] Inventory rapporteert `\_render\_\*` functies.
* \[ ] Inventory mappt waar mogelijk naar page registry.
* \[ ] Inventory markeert critical/optional.
* \[ ] Report is secret-free.

\---

## 6\. Fase 3 - Critical Workflow Lock

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/critical\_workflow\_lock.py
```

Critical V2 workflows:

* \[ ] Dashboard openen.
* \[ ] No-live proof bekijken.
* \[ ] Runtime configureren.
* \[ ] Demo bot starten/stoppen.
* \[ ] Paper session starten/stoppen.
* \[ ] Demo spot guarded flow.
* \[ ] Risk blocker bekijken.
* \[ ] Orders/fills/sessions bekijken.
* \[ ] Session report exporteren.
* \[ ] Support bundle maken/verifiëren.
* \[ ] Evidence exporteren.
* \[ ] Operator quality gate bekijken.
* \[ ] Dashboard/browser smoke draaien.
* \[ ] Fallback naar Streamlit vinden.

Per workflow:

* \[ ] route;
* \[ ] API endpoints;
* \[ ] action policy;
* \[ ] browser smoke;
* \[ ] UAT scenario;
* \[ ] evidence output;
* \[ ] fallback path.

Acceptatiecriteria:

* \[ ] Critical workflows hebben locked/pass status.
* \[ ] Geen V2-first cutover bij failed critical workflow.
* \[ ] Each workflow has fallback instructions.
* \[ ] No-live proof included in every workflow.
* \[ ] Tests use fixture workflows.

\---

## 7\. Fase 4 - V2-First CLI Router

Uitbreid CLI:

```text
python -m binance\_spot\_bot.cli dashboard
```

Nieuw gedrag:

* \[ ] `dashboard` start Dashboard V2 als readiness gate pass.
* \[ ] `dashboard --v2` forceert Dashboard V2.
* \[ ] `dashboard --legacy-streamlit` forceert Streamlit.
* \[ ] `dashboard --auto` kiest V2 met fallback info.
* \[ ] `dashboard --fallback-if-v2-fails` start Streamlit als V2 startup faalt.
* \[ ] CLI output toont local URL.
* \[ ] CLI output toont no-live statement.
* \[ ] CLI output toont fallback command.

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/cli\_router.py
```

Acceptatiecriteria:

* \[ ] Geen breaking change zonder fallback.
* \[ ] `dashboard --legacy-streamlit` werkt.
* \[ ] `dashboard --v2` werkt.
* \[ ] `dashboard` toont V2-first status.
* \[ ] Tests gebruiken fake launcher.

\---

## 8\. Fase 5 - V2-Only Operator Mode

Nieuwe mode:

```text
python -m binance\_spot\_bot.cli dashboard-v2 --operator-mode
```

V2-only operator mode:

* \[ ] Geen Streamlit import nodig.
* \[ ] Alleen Dashboard V2 routes.
* \[ ] Alleen safe action policy.
* \[ ] Geen live mode.
* \[ ] Compact navigation.
* \[ ] Advanced/dev panels optioneel verborgen.
* \[ ] Evidence/support zichtbaar.
* \[ ] Stop button altijd zichtbaar.
* \[ ] No-live banner altijd zichtbaar.
* \[ ] Streamlit fallback link zichtbaar in help/fallback panel.

Backend config:

```text
src/binance\_spot\_bot/dashboard\_v2/operator\_mode.py
```

Acceptatiecriteria:

* \[ ] V2-only mode start zonder Streamlit import.
* \[ ] Operator mode toont alleen operator-relevante routes.
* \[ ] Advanced pages blijven bereikbaar via toggle indien toegestaan.
* \[ ] No-live proof zichtbaar.
* \[ ] Browser smoke operator mode pass.

\---

## 9\. Fase 6 - V2 Legacy Compatibility Layer

Doel: bestaande Streamlit docs/links/actions niet plots breken.

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/legacy\_compat.py
```

Functionaliteit:

* \[ ] oude page key naar V2 route.
* \[ ] oude tab title naar V2 route.
* \[ ] oude CLI dashboard help naar V2 command.
* \[ ] oude docs link naar V2 docs.
* \[ ] Streamlit fallback command per page.
* \[ ] compatibility warnings.

Output:

```text
data/dashboard-v2/deprecation/legacy\_compat\_map.json
```

Acceptatiecriteria:

* \[ ] Alle 36 page keys hebben compat mapping.
* \[ ] Missing mapping blokkeert deprecation candidate.
* \[ ] Links zijn secret-free.
* \[ ] Docs kunnen compat map gebruiken.
* \[ ] Tests cover known pages.

\---

## 10\. Fase 7 - Streamlit Legacy Badge Hardening

Aanpassingen in Streamlit:

* \[ ] `Legacy Streamlit Dashboard` badge.
* \[ ] `Dashboard V2 recommended` badge wanneer gate pass.
* \[ ] V2 launch command zichtbaar.
* \[ ] V2 fallback/rollback uitleg.
* \[ ] No-live banner blijft bovenaan.
* \[ ] Geen nieuwe Streamlit features meer zonder exception.
* \[ ] Legacy-only page status kan getoond worden.
* \[ ] Link naar deprecation readiness report.

Acceptatiecriteria:

* \[ ] Streamlit import blijft werken.
* \[ ] Legacy badge zichtbaar.
* \[ ] No-live caption blijft zichtbaar.
* \[ ] V2 command zichtbaar.
* \[ ] Existing Streamlit smoke blijft groen.

\---

## 11\. Fase 8 - Streamlit Change Freeze Policy

Nieuw doc:

```text
docs/dashboard-v2/streamlit-change-freeze-policy.md
```

Policy:

* \[ ] Nieuwe dashboardfeatures moeten V2-first.
* \[ ] Streamlit krijgt alleen bugfix/security/no-live fixes.
* \[ ] Nieuwe Streamlit-only pages verboden zonder waiver.
* \[ ] Nieuwe Streamlit-only actions verboden zonder waiver.
* \[ ] Waiver vereist reden, expiry en migration task.
* \[ ] Check-all kan Streamlit-only additions detecteren.
* \[ ] Roadmap completion gate waarschuwt bij nieuwe Streamlit-only code.

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/streamlit\_change\_freeze.py
```

Acceptatiecriteria:

* \[ ] Freeze policy bestaat.
* \[ ] Detector vindt nieuwe `\_render\_\*` zonder V2 mapping.
* \[ ] Detector vindt nieuwe Streamlit-only button/action.
* \[ ] Waiver systeem bestaat.
* \[ ] Tests gebruiken fixture diff.

\---

## 12\. Fase 9 - V2-First Docs Migration

Docs naar V2-first:

* \[ ] README dashboard quick start.
* \[ ] Operator manual.
* \[ ] Dashboard walkthroughs.
* \[ ] CLI cookbook.
* \[ ] UAT scenarios.
* \[ ] Troubleshooting playbooks.
* \[ ] Support bundle guide.
* \[ ] Evidence guide.
* \[ ] Release notes template.
* \[ ] Roadmap completion docs.

Checks:

* \[ ] V2 route aanwezig.
* \[ ] Streamlit fallback vermeld.
* \[ ] Geen live approval wording.
* \[ ] Geen Streamlit-first instructie behalve fallback.
* \[ ] CLI commands bestaan.

Acceptatiecriteria:

* \[ ] Docs consistency pass.
* \[ ] V2-first wording aanwezig.
* \[ ] Streamlit fallback blijft vindbaar.
* \[ ] No-live statement op elke relevante doc.
* \[ ] Broken links report leeg of only warnings.

\---

## 13\. Fase 10 - V2-First UAT Scenario Lock

Roadmap 103 UAT uitbreiden:

* \[ ] UAT first dashboard launch gebruikt V2.
* \[ ] UAT start demo bot gebruikt V2.
* \[ ] UAT start paper session gebruikt V2.
* \[ ] UAT demo spot trading gebruikt V2.
* \[ ] UAT support bundle gebruikt V2.
* \[ ] UAT evidence review gebruikt V2.
* \[ ] UAT no-live proof gebruikt V2.
* \[ ] UAT fallback scenario gebruikt Streamlit legacy.

Acceptatiecriteria:

* \[ ] V2-first UAT profile pass.
* \[ ] Fallback UAT profile pass.
* \[ ] Open UAT P0/P1 blokkeert deprecation candidate.
* \[ ] UAT evidence included in deprecation evidence.
* \[ ] Tests validate scenario references.

\---

## 14\. Fase 11 - V2-First Support Bundle

Support bundle uitbreiden:

* \[ ] V2 parity lock report.
* \[ ] Streamlit-only inventory.
* \[ ] Critical workflow lock report.
* \[ ] V2-first CLI router report.
* \[ ] V2 operator mode report.
* \[ ] Legacy compat map.
* \[ ] Streamlit change freeze report.
* \[ ] V2-first docs migration report.
* \[ ] V2-first UAT result.
* \[ ] Streamlit fallback verification.
* \[ ] no-live proof.

Acceptatiecriteria:

* \[ ] Support bundle bevat V2-first artifacts.
* \[ ] Support bundle verify kan V2-first artifacts valideren.
* \[ ] Redaction self-test dekt artifacts.
* \[ ] Missing optional artifacts zijn warnings.
* \[ ] Secret-free.

\---

## 15\. Fase 12 - Deprecation Gate

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/deprecation\_gate.py
```

Gate statuses:

* \[ ] not\_ready;
* \[ ] blocked;
* \[ ] v2\_first\_ready;
* \[ ] legacy\_fallback\_ready;
* \[ ] deprecation\_candidate;
* \[ ] removal\_candidate\_later.

Hard blockers:

* \[ ] live mode in V2.
* \[ ] no-live proof missing.
* \[ ] V2 API smoke failed.
* \[ ] V2 browser smoke failed.
* \[ ] critical workflow failed.
* \[ ] support/evidence workflow failed.
* \[ ] UAT P0/P1 open.
* \[ ] missing fallback command.
* \[ ] Streamlit fallback broken.
* \[ ] docs not V2-first.
* \[ ] final parity lock incomplete for critical pages.

Soft blockers:

* \[ ] optional advanced page legacy-only.
* \[ ] performance warning.
* \[ ] non-critical docs gap.
* \[ ] UAT P2 feedback.
* \[ ] minor accessibility issue.

Acceptatiecriteria:

* \[ ] Gate is deterministic.
* \[ ] Hard blockers force blocked.
* \[ ] Soft blockers allow ready-with-warnings.
* \[ ] Gate never removes Streamlit.
* \[ ] Report is Markdown + JSON.

\---

## 16\. Fase 13 - V2-Only Smoke Profile

Nieuwe smoke profile:

```text
dashboard\_v2\_only\_smoke
```

Checks:

* \[ ] Dashboard V2 imports.
* \[ ] FastAPI app route inventory.
* \[ ] No live routes.
* \[ ] Operator mode config.
* \[ ] WebSocket heartbeat.
* \[ ] API health/config/pages/snapshot.
* \[ ] Start wizard route.
* \[ ] Demo spot flow route.
* \[ ] Paper session route.
* \[ ] Evidence/support route.
* \[ ] Browser no-live banner.
* \[ ] Streamlit not imported in V2-only smoke.
* \[ ] Streamlit fallback still separately works.

Acceptatiecriteria:

* \[ ] V2-only smoke passes without Streamlit import.
* \[ ] No-live route proof included.
* \[ ] Browser smoke works.
* \[ ] Fallback smoke works separately.
* \[ ] Check-all deep can call profile.

\---

## 17\. Fase 14 - Streamlit Fallback Rollback Drill

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/fallback\_drill.py
```

Drill flow:

* \[ ] simulate V2 startup failure.
* \[ ] show fallback command.
* \[ ] verify Streamlit import.
* \[ ] verify legacy dashboard launch command.
* \[ ] verify no-live banner in Streamlit.
* \[ ] verify docs link.
* \[ ] export drill report.

Acceptatiecriteria:

* \[ ] Drill works offline.
* \[ ] Drill does not require real dashboard server.
* \[ ] Drill confirms fallback instructions.
* \[ ] No-live proof included.
* \[ ] Tests use fake failure.

\---

## 18\. Fase 15 - Streamlit Deprecation Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/deprecation\_evidence\_bundle.py
```

Bundle bevat:

* \[ ] safety contract.
* \[ ] final parity lock.
* \[ ] Streamlit-only inventory.
* \[ ] critical workflow lock.
* \[ ] CLI router report.
* \[ ] V2-only operator mode report.
* \[ ] legacy compat map.
* \[ ] Streamlit legacy badge verification.
* \[ ] Streamlit change freeze report.
* \[ ] V2-first docs migration report.
* \[ ] V2-first UAT result.
* \[ ] support bundle V2-first verification.
* \[ ] deprecation gate report.
* \[ ] V2-only smoke report.
* \[ ] fallback rollback drill.
* \[ ] no-live proof.
* \[ ] hashes.

Output:

```text
data/dashboard-v2/deprecation/evidence/<run\_id>/
  streamlit\_deprecation\_evidence\_manifest.json
  streamlit\_deprecation\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle can be verified.
* \[ ] Bundle clearly states Streamlit not removed yet unless future gate.
* \[ ] Dashboard can download bundle.

\---

## 19\. Fase 16 - Check-All Integration

`check\_all.py` uitbreiden met profielbewuste checks:

Fast profile:

* \[ ] V2-first route list smoke.
* \[ ] No-live route proof.
* \[ ] Streamlit fallback import.
* \[ ] Deprecation gate quick check.

Deep profile:

* \[ ] final parity lock.
* \[ ] Streamlit-only inventory.
* \[ ] critical workflow lock.
* \[ ] V2-only smoke.
* \[ ] fallback drill.
* \[ ] deprecation evidence bundle verify.
* \[ ] V2-first UAT evidence if available.

Acceptatiecriteria:

* \[ ] Normal check-all blijft bruikbaar.
* \[ ] Deep check-all dekt V2-first cutover.
* \[ ] No-live failure hard fail.
* \[ ] Missing optional V2 advanced artifacts warning.
* \[ ] Secret-free output.

\---

## 20\. Fase 17 - Release/Migration Integration

Roadmap 089 integratie:

* \[ ] Version manifest bevat `dashboard\_primary=v2`.
* \[ ] Release notes vermelden Streamlit legacy/fallback.
* \[ ] Migration notes leggen `dashboard --legacy-streamlit` uit.
* \[ ] Release candidate vereist deprecation gate pass.
* \[ ] Release evidence bevat deprecation bundle.
* \[ ] Rollback instructions included.

Acceptatiecriteria:

* \[ ] Release simulation leest deprecation gate.
* \[ ] Release notes zijn V2-first.
* \[ ] Streamlit fallback is documented.
* \[ ] No-live proof included.
* \[ ] No Streamlit removal without separate roadmap.

\---

## 21\. Fase 18 - Knowledge/Test/Impact Integration

Roadmap 091:

* \[ ] Knowledge graph markeert Dashboard V2 als primary UI.
* \[ ] Streamlit gemarkeerd legacy/fallback.
* \[ ] Page registry maps naar V2 route.
* \[ ] Impact analysis detecteert Streamlit-only changes.

Roadmap 092:

* \[ ] Dashboard V2 changes selecteren V2 tests.
* \[ ] Streamlit changes selecteren freeze/fallback tests.
* \[ ] Docs changes selecteren V2-first docs tests.
* \[ ] CLI dashboard changes selecteren router tests.

Acceptatiecriteria:

* \[ ] Impact reports tonen V2-first status.
* \[ ] Test selection kiest juiste tests.
* \[ ] Streamlit-only new feature wordt flagged.
* \[ ] Knowledge graph is secret-free.
* \[ ] No-live proof preserved.

\---

## 22\. Fase 19 - Operator/Training/UAT Integration

Roadmap 102:

* \[ ] Operator manual: V2 primary, Streamlit fallback.
* \[ ] CLI cookbook: `dashboard` V2-first.
* \[ ] Troubleshooting: V2 failure → Streamlit fallback.
* \[ ] Support guide: V2-first artifacts.

Roadmap 103:

* \[ ] UAT profiles V2-first.
* \[ ] Streamlit fallback scenario.
* \[ ] UAT sign-off requires V2 critical workflow pass.
* \[ ] UAT feedback for Streamlit legacy no longer blocks V2 unless critical fallback issue.

Acceptatiecriteria:

* \[ ] Operator docs V2-first pass.
* \[ ] UAT V2-first pass.
* \[ ] Fallback scenario pass.
* \[ ] Training evidence links deprecation evidence.
* \[ ] No-live proof preserved.

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

* \[ ] Commands werken offline.
* \[ ] Commands ondersteunen JSON waar relevant.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Commands bevatten no-live statement.
* \[ ] Reports zijn secret-free.

\---

## 24\. Fase 21 - Tests

### Unit tests

* \[ ] `tests/test\_dashboard\_v2\_streamlit\_deprecation\_execution\_safety\_contract.py`
* \[ ] `tests/test\_dashboard\_v2\_final\_parity\_lock.py`
* \[ ] `tests/test\_dashboard\_v2\_streamlit\_only\_inventory.py`
* \[ ] `tests/test\_dashboard\_v2\_critical\_workflow\_lock.py`
* \[ ] `tests/test\_dashboard\_v2\_cli\_router.py`
* \[ ] `tests/test\_dashboard\_v2\_operator\_mode.py`
* \[ ] `tests/test\_dashboard\_v2\_legacy\_compat.py`
* \[ ] `tests/test\_dashboard\_v2\_streamlit\_change\_freeze.py`
* \[ ] `tests/test\_dashboard\_v2\_deprecation\_gate.py`
* \[ ] `tests/test\_dashboard\_v2\_fallback\_drill.py`
* \[ ] `tests/test\_dashboard\_v2\_deprecation\_evidence\_bundle.py`

### Integration tests

* \[ ] Page registry → V2 route parity fixture.
* \[ ] Streamlit-only inventory fixture.
* \[ ] Critical workflow pass/fail fixture.
* \[ ] CLI router V2/fallback fixture.
* \[ ] V2-only operator mode fixture.
* \[ ] Legacy compat map fixture.
* \[ ] Change freeze fixture.
* \[ ] Deprecation gate pass/fail fixture.
* \[ ] Fallback drill fixture.
* \[ ] Evidence bundle export/verify fixture.

### Browser smoke

* \[ ] V2-only operator mode loads.
* \[ ] No-live banner visible.
* \[ ] Start wizard visible.
* \[ ] Paper session flow visible.
* \[ ] Demo spot flow visible.
* \[ ] Evidence/support visible.
* \[ ] Streamlit fallback link visible.
* \[ ] No live controls visible.

### Safety tests

* \[ ] Live mode absent.
* \[ ] Signed/order/account endpoints absent.
* \[ ] V2-only smoke does not import Streamlit.
* \[ ] Streamlit fallback remains available.
* \[ ] Deprecation gate blocks removal if critical parity missing.
* \[ ] Docs contain no live approval wording.
* \[ ] Evidence secret-free.
* \[ ] Check-all safe env preserved.

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

* \[ ] Dashboard V2 is primary when deprecation gate passes.
* \[ ] Streamlit is legacy/fallback.
* \[ ] `dashboard --v2`.
* \[ ] `dashboard --legacy-streamlit`.
* \[ ] `dashboard --fallback-if-v2-fails`.
* \[ ] no-live statement.
* \[ ] removal not done in this roadmap.

Operator docs updates:

* \[ ] V2 primary.
* \[ ] Streamlit fallback.
* \[ ] V2-only operator mode.
* \[ ] fallback drill.
* \[ ] deprecation gate explanation.

\---

## 26\. Codex bouwvolgorde

### PR 1 - Safety Contract + Final Parity Lock

* \[ ] `docs/dashboard-v2-streamlit-deprecation-execution-safety-contract.md`
* \[ ] `dashboard\_v2/final\_parity\_lock.py`
* \[ ] page registry parity tests.
* \[ ] no-live tests.

### PR 2 - Streamlit-Only Inventory

* \[ ] `dashboard\_v2/streamlit\_only\_inventory.py`
* \[ ] `\_render\_\*` inventory.
* \[ ] streamlit-only action tests.

### PR 3 - Critical Workflow Lock

* \[ ] `dashboard\_v2/critical\_workflow\_lock.py`
* \[ ] workflow fixtures.
* \[ ] browser/UAT link validation.

### PR 4 - V2-First CLI Router

* \[ ] `dashboard\_v2/cli\_router.py`
* \[ ] `dashboard --v2`.
* \[ ] `dashboard --legacy-streamlit`.
* \[ ] fallback tests.

### PR 5 - V2-Only Operator Mode

* \[ ] `dashboard\_v2/operator\_mode.py`
* \[ ] V2-only smoke.
* \[ ] no Streamlit import tests.

### PR 6 - Legacy Compat + Streamlit Legacy Badge

* \[ ] `dashboard\_v2/legacy\_compat.py`
* \[ ] Streamlit badge.
* \[ ] compatibility map tests.

### PR 7 - Streamlit Change Freeze + V2-First Docs/UAT

* \[ ] `dashboard\_v2/streamlit\_change\_freeze.py`
* \[ ] V2-first docs checks.
* \[ ] V2-first UAT checks.

### PR 8 - Deprecation Gate + Fallback Drill

* \[ ] `dashboard\_v2/deprecation\_gate.py`
* \[ ] `dashboard\_v2/fallback\_drill.py`
* \[ ] gate/drill tests.

### PR 9 - Evidence Bundle + Support/Check-All Integration

* \[ ] `dashboard\_v2/deprecation\_evidence\_bundle.py`
* \[ ] support bundle integration.
* \[ ] check-all integration.

### PR 10 - Release/Knowledge/Test/Operator Docs Integration

* \[ ] release/migration docs.
* \[ ] knowledge/test impact integration.
* \[ ] README/operator docs.
* \[ ] final browser smoke.

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

* \[ ] Streamlit Deprecation Execution Safety Contract bestaat.
* \[ ] Final Dashboard Parity Lock werkt.
* \[ ] Streamlit-Only Inventory werkt.
* \[ ] Critical Workflow Lock werkt.
* \[ ] V2-First CLI Router werkt.
* \[ ] V2-Only Operator Mode werkt.
* \[ ] V2 Legacy Compatibility Layer werkt.
* \[ ] Streamlit Legacy Badge Hardening werkt.
* \[ ] Streamlit Change Freeze Policy werkt.
* \[ ] V2-First Docs Migration werkt.
* \[ ] V2-First UAT Scenario Lock werkt.
* \[ ] V2-First Support Bundle werkt.
* \[ ] Deprecation Gate werkt.
* \[ ] V2-Only Smoke Profile werkt.
* \[ ] Streamlit Fallback Rollback Drill werkt.
* \[ ] Streamlit Deprecation Evidence Bundle werkt.
* \[ ] Check-All Integration werkt.
* \[ ] Release/Migration Integration werkt.
* \[ ] Knowledge/Test/Impact Integration werkt.
* \[ ] Operator/Training/UAT Integration werkt.
* \[ ] CLI commands werken.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen Streamlit fallback beschikbaar blijft.
* \[ ] Tests bewijzen V2-only operator mode zonder Streamlit import kan.
* \[ ] Tests bewijzen docs/evidence secret-free zijn.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Dashboard V2 is primary/recommended wanneer gate pass.
* \[ ] Streamlit is legacy/fallback.
* \[ ] Streamlit is nog niet hard verwijderd zonder aparte removal roadmap.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 108 kan na uitvoering naar `Voltooid docs`.

\---

## 29\. Verwachte Roadmap 109 daarna

Als Roadmap 108 groen is:

```text
Roadmap 109 - Streamlit Removal Candidate, Legacy Cleanup \& Dashboard V2-Only Release Hardening
```

Mogelijke inhoud:

* \[ ] laatste legacy imports verwijderen of isoleren;
* \[ ] Streamlit dependency optioneel/legacy maken;
* \[ ] V2-only release bundle;
* \[ ] final rollback archive;
* \[ ] docs volledig V2-only;
* \[ ] release hardening;
* \[ ] still no live trading.

```

Als Roadmap 108 blockers vindt:

```text
Roadmap 109 - Dashboard V2 Deprecation Blocker Burn-Down, Remaining Legacy Gaps \& Fallback Reliability
```

Mogelijke inhoud:

* \[ ] critical V2 parity gaps oplossen;
* \[ ] fallback drill verbeteren;
* \[ ] docs/UAT gates verbeteren;
* \[ ] Streamlit-only features migreren;
* \[ ] still no live trading.

```

