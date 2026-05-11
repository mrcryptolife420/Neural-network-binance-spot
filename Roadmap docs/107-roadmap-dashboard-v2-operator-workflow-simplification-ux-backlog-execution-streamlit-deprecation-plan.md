# Roadmap 107 - Dashboard V2 Operator Workflow Simplification, UX Backlog Execution \& Streamlit Deprecation Plan

Status: Nieuw / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-11  
Voorgestelde locatie:

```text
Roadmap docs/107-roadmap-dashboard-v2-operator-workflow-simplification-ux-backlog-execution-streamlit-deprecation-plan.md
```

## Samenvatting

Roadmap 104 bouwt het fundament van Dashboard V2 zonder Streamlit: FastAPI/Uvicorn, WebSocket events, React/Vite frontend, action policy, runtime bridge, API/browser smoke en local-only no-live guardrails.

Roadmap 105 maakt Dashboard V2 feature-parity met het huidige Streamlit dashboard.

Roadmap 106 maakt Dashboard V2 performant, packagebaar, lokaal startbaar, evidence-ready en cutover-ready, met Streamlit nog als fallback.

Roadmap 107 is de logische volgende stap: **operator workflows vereenvoudigen, UAT-feedback uitvoeren, dashboardfrictie verminderen en een veilige Streamlit-deprecation planning maken**. Niet meteen Streamlit verwijderen, maar eerst aantoonbaar maken dat Dashboard V2 makkelijker, sneller en veiliger is voor de dagelijkse operatorflows.

Live trading blijft volledig buiten scope. Dashboard V2 blijft local-only en beperkt tot demo, paper en testnet-readiness. Geen live mode, geen signed real-order endpoints, geen echte account workflows en geen externe telemetry.

\---

## 0\. Controle vooraf

### Repo- en roadmapcontrole

* \[x] Gezocht naar bestaande `Roadmap 107`, `107-roadmap`, `Dashboard V2 Operator Workflow Simplification`, `Streamlit Deprecation Plan`, `UX Backlog Execution` en `Dashboard V2 Performance Regression`.
* \[x] Geen bestaande Roadmap 107 gevonden.
* \[x] Gezocht in `Voltooid docs`, `Roadmap docs` en `docs`.
* \[x] Roadmap 106 is lokaal aangemaakt als Dashboard V2 Performance, Desktop Packaging \& Streamlit Cutover Readiness.

### Codebasecontrole

Breed bekeken met focus op dashboard, workflow, CLI, page registry, safety en cutover:

* \[x] `src/binance\_spot\_bot/ui/streamlit\_app.py`
* \[x] `src/binance\_spot\_bot/ui/page\_registry.py`
* \[x] `src/binance\_spot\_bot/ui/components.py`
* \[x] `src/binance\_spot\_bot/cli.py`
* \[x] `src/binance\_spot\_bot/check\_all.py`
* \[x] `src/binance\_spot\_bot/runtime.py`
* \[x] `src/binance\_spot\_bot/operator\_ops.py`
* \[x] roadmaplijn 100-106: milestone audit, stabilization, operator training, UAT, Dashboard V2 foundation/parity/performance.

### Belangrijke conclusies

De bestaande Streamlit app is functioneel maar zwaar:

* \[x] `streamlit\_app.py` bevat één grote UI-flow met sidebar, runtime key, runtime actions, snapshot rendering, simpele demo view, advanced tabs, evidence/support/operator pages, data/model/monitoring/portfolio pages en `time.sleep(2.0)` + `st.rerun()` bij running state.
* \[x] `page\_registry.py` bevat 36 pages en blokkeert live trading pages. Dit is de juiste bron voor Dashboard V2 routing, page ownership, migration status en deprecation coverage.
* \[x] `cli.py` bevat al een grote command surface voor dashboard, check-all, support, evidence, paper sessions, demo pilot, demo execution, operator reports, security/redaction en model/evaluation.
* \[x] Na Roadmap 104-106 zou Dashboard V2 technisch bestaan, feature-parity hebben en cutover readiness kunnen meten. Wat dan nog mist is de UX-executie: flow-simplificatie, UAT-feedback oplossen, onboarding, command hints, page consolidation en legacy Streamlit planning.

### Grootste gat na Roadmap 106

Na performance/packaging/cutover readiness is Dashboard V2 technisch sterk, maar nog niet per se optimaal voor dagelijks gebruik:

* \[ ] operator moet nog te veel keuzes maken voordat de bot loopt;
* \[ ] advanced pages kunnen overweldigend zijn;
* \[ ] demo/paper/testnet-readiness flow kan simpeler;
* \[ ] actieknoppen hebben misschien onvoldoende context;
* \[ ] statusmeldingen, blockers en alerts kunnen beter geordend worden;
* \[ ] UAT-feedback uit Roadmap 103 moet concreet worden uitgevoerd;
* \[ ] Streamlit fallback moet een duidelijke sunset/deprecation planning krijgen;
* \[ ] legacy Streamlit en Dashboard V2 mogen geen verwarrende dubbele waarheid worden;
* \[ ] operator docs moeten V2-first worden;
* \[ ] check-all/release/roadmap gates moeten weten wanneer Streamlit nog nodig is.

Roadmap 107 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 107

Maak Dashboard V2 de duidelijke, eenvoudige en aanbevolen operatorflow:

```text
Dashboard V2 cutover readiness
→ UAT feedback backlog
→ workflow simplification
→ guided actions
→ page consolidation
→ V2-first docs
→ Streamlit fallback policy
→ Streamlit deprecation plan
```

Na deze roadmap moet de operator:

* \[ ] Dashboard V2 als standaard aanbevolen UI zien;
* \[ ] de bot kunnen starten via een duidelijke guided flow;
* \[ ] demo spot trading kunnen uitvoeren met duidelijke guardrails;
* \[ ] paper sessions kunnen starten/stoppen/inspecteren zonder tab-chaos;
* \[ ] evidence/support/no-live proof makkelijk vinden;
* \[ ] alerts/blockers/runbooks direct bij de juiste context zien;
* \[ ] minder losse pages nodig hebben voor dezelfde taak;
* \[ ] via UAT-scorecards zien dat UX-frictie daalt;
* \[ ] Streamlit veilig als legacy fallback kunnen gebruiken;
* \[ ] weten wanneer Streamlit nog nodig is en wanneer niet meer.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[ ] Geen Dashboard V2 foundation opnieuw bouwen.
* \[ ] Geen Dashboard V2 feature-parity opnieuw bouwen.
* \[ ] Geen Dashboard V2 performance/packaging opnieuw bouwen.
* \[ ] Geen trading runtime opnieuw bouwen.
* \[ ] Geen modeltraining/data pipeline opnieuw bouwen.
* \[ ] Geen operator manual opnieuw bouwen.
* \[ ] Geen UAT engine opnieuw bouwen.
* \[ ] Geen Streamlit direct verwijderen.
* \[ ] Geen live trading.
* \[ ] Geen live mode.
* \[ ] Geen signed real-order endpoints.
* \[ ] Geen echte account workflows.
* \[ ] Geen remote telemetry.
* \[ ] Geen cloud dashboard.
* \[ ] Geen Electron verplicht maken.
* \[ ] Geen UX change zonder smoke/UAT/evidence.

Wel doen:

* \[ ] operator workflows vereenvoudigen;
* \[ ] UAT-feedback backlog uitvoeren;
* \[ ] V2-first dashboard navigation maken;
* \[ ] safe action wizards toevoegen;
* \[ ] status/blocker/alert UX verbeteren;
* \[ ] docs en CLI hints updaten;
* \[ ] Streamlit fallback policy vastleggen;
* \[ ] deprecation readiness meten;
* \[ ] evidence en tests toevoegen.

\---

## 3\. Fase 0 - Dashboard V2 UX/Cutover Safety Contract

Nieuw docbestand:

```text
docs/dashboard-v2-ux-cutover-safety-contract.md
```

Regels:

* \[ ] Dashboard V2 UX changes zijn local-only.
* \[ ] Geen live trading.
* \[ ] Geen live mode in navigation, forms, actions, CLI of docs.
* \[ ] Alleen demo/paper/testnet-readiness.
* \[ ] Streamlit blijft fallback tot deprecation gate pass.
* \[ ] Geen UX-flow mag no-live proof verbergen.
* \[ ] Geen action wizard mag safety guards omzeilen.
* \[ ] Demo trading blijft expliciet demo en guarded.
* \[ ] Paper sessions blijven paper-only.
* \[ ] Testnet-readiness blijft readiness-only.
* \[ ] UAT feedback mag geen secrets opslaan.
* \[ ] UX reports en evidence zijn secret-free.
* \[ ] Operator moet rollback/fallback naar Streamlit kunnen vinden.
* \[ ] Deprecation betekent niet deletion zonder aparte roadmap/gate.

Acceptatiecriteria:

* \[ ] Safety contract bestaat.
* \[ ] Tests bewijzen live wording/controls niet verschijnen.
* \[ ] Tests bewijzen no-live banner in V2-first layout blijft.
* \[ ] Tests bewijzen Streamlit fallback link aanwezig blijft.
* \[ ] Tests bewijzen UX feedback redacted blijft.

\---

## 4\. Fase 1 - UX Backlog Ingestor

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/ux\_backlog\_ingest.py
```

Inputs:

* \[ ] Roadmap 103 UAT feedback backlog;
* \[ ] Roadmap 106 cutover readiness report;
* \[ ] browser smoke matrix failures;
* \[ ] Dashboard V2 performance warnings;
* \[ ] operator support bundle findings;
* \[ ] docs consistency findings;
* \[ ] Streamlit parity gaps;
* \[ ] manual operator notes.

Dataclasses:

* \[ ] `DashboardV2UxFinding`
* \[ ] `DashboardV2UxBacklog`
* \[ ] `DashboardV2UxBacklogItem`
* \[ ] `DashboardV2UxIngestReport`

Categories:

* \[ ] onboarding;
* \[ ] navigation;
* \[ ] runtime\_controls;
* \[ ] demo\_spot\_trading;
* \[ ] paper\_sessions;
* \[ ] charts;
* \[ ] evidence\_support;
* \[ ] alerts\_blockers;
* \[ ] settings\_profiles;
* \[ ] docs\_help;
* \[ ] performance;
* \[ ] accessibility;
* \[ ] no\_live\_safety;
* \[ ] streamlit\_fallback.

Priorities:

* \[ ] UX-P0 safety/no-live confusion;
* \[ ] UX-P1 critical workflow blocked;
* \[ ] UX-P2 high-friction common workflow;
* \[ ] UX-P3 clarity/polish;
* \[ ] UX-P4 nice-to-have.

Acceptatiecriteria:

* \[ ] UAT feedback kan worden ingelezen.
* \[ ] Cutover readiness warnings worden backlog items.
* \[ ] Duplicates worden gegroepeerd.
* \[ ] No-live confusion wordt P0.
* \[ ] Report is Markdown + JSON en secret-free.

\---

## 5\. Fase 2 - Operator Journey Map

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/operator\_journey\_map.py
```

Belangrijkste journeys:

### Beginner

* \[ ] open dashboard;
* \[ ] verify no-live;
* \[ ] choose demo mode;
* \[ ] inspect status;
* \[ ] run demo paper smoke;
* \[ ] export support/evidence.

### Paper operator

* \[ ] choose symbol/source;
* \[ ] configure risk;
* \[ ] start paper session;
* \[ ] monitor chart/equity/orders;
* \[ ] stop session;
* \[ ] review session report.

### Demo spot operator

* \[ ] choose demo profile;
* \[ ] verify credentials status;
* \[ ] arm demo;
* \[ ] preview order;
* \[ ] test order;
* \[ ] guarded place if allowed;
* \[ ] reconcile/cancel/report.

### Maintainer

* \[ ] check-all status;
* \[ ] support bundle;
* \[ ] evidence chain;
* \[ ] dashboard smoke;
* \[ ] release/milestone status;
* \[ ] troubleshooting.

Dataclasses:

* \[ ] `OperatorJourney`
* \[ ] `OperatorJourneyStep`
* \[ ] `OperatorJourneyFriction`
* \[ ] `OperatorJourneyMetric`

Acceptatiecriteria:

* \[ ] Journeys zijn JSON-serializable.
* \[ ] Elke journey heeft primary route en fallback route.
* \[ ] Elke journey heeft no-live proof step.
* \[ ] Missing pages/actions worden gerapporteerd.
* \[ ] Dashboard toont journey progress.

\---

## 6\. Fase 3 - Dashboard V2 Home Simplification

Doel: de homepagina wordt een operator cockpit, geen losse technische pagina.

Nieuwe V2 home layout:

* \[ ] top safety banner;
* \[ ] connection/runtime status;
* \[ ] “Start demo bot” guided card;
* \[ ] “Start paper session” guided card;
* \[ ] “Review evidence/support” guided card;
* \[ ] “Fix blockers” guided card;
* \[ ] latest alerts;
* \[ ] latest session summary;
* \[ ] no-live proof status;
* \[ ] WebSocket status;
* \[ ] Streamlit fallback link.

Verwijder/verminder op home:

* \[ ] onnodige debug JSON;
* \[ ] te veel advanced panels;
* \[ ] duplicate metrics;
* \[ ] deep advanced links zonder context.

Acceptatiecriteria:

* \[ ] Beginner ziet 3-5 duidelijke acties.
* \[ ] No-live proof zichtbaar boven de fold.
* \[ ] Live option nergens zichtbaar.
* \[ ] Home route laadt snel.
* \[ ] UAT scenario home-first-launch pass.

\---

## 7\. Fase 4 - Guided Action Cards

Nieuwe frontend componenten:

```text
dashboard-v2/src/components/guided/
  GuidedActionCard.tsx
  GuidedChecklist.tsx
  SafetyPrecheck.tsx
  ActionPreview.tsx
  ActionResultPanel.tsx
```

Action cards:

* \[ ] Start demo bot;
* \[ ] Start paper session;
* \[ ] Connect demo profile;
* \[ ] Preview demo order;
* \[ ] Export support bundle;
* \[ ] Export operator evidence;
* \[ ] Run dashboard smoke;
* \[ ] Review no-live proof;
* \[ ] Open troubleshooting playbook.

Elke card heeft:

* \[ ] purpose;
* \[ ] safety label;
* \[ ] prerequisites;
* \[ ] expected result;
* \[ ] primary action;
* \[ ] fallback action;
* \[ ] related CLI command;
* \[ ] related doc/playbook;
* \[ ] evidence output.

Acceptatiecriteria:

* \[ ] Cards gebruiken backend action policy.
* \[ ] Cards tonen disabled reason.
* \[ ] Cards tonen no-live safety.
* \[ ] Action result is zichtbaar en downloadbaar.
* \[ ] Tests dekken card states.

\---

## 8\. Fase 5 - Runtime Start Wizard V2

Nieuwe wizard:

```text
dashboard-v2/src/pages/StartBotWizardPage.tsx
```

Stappen:

* \[ ] choose mode: demo/paper/testnet-readiness;
* \[ ] choose source: auto/demo/rest/websocket;
* \[ ] choose symbol/interval;
* \[ ] choose scenario/model alias;
* \[ ] risk preset;
* \[ ] safety precheck;
* \[ ] no-live confirmation;
* \[ ] start/paper smoke;
* \[ ] monitor page redirect.

Backend support:

```text
src/binance\_spot\_bot/dashboard\_v2/start\_wizard.py
```

Acceptatiecriteria:

* \[ ] Wizard bevat geen live mode.
* \[ ] Wizard kan demo runtime starten.
* \[ ] Wizard kan paper session starten.
* \[ ] Precheck failures zijn duidelijk.
* \[ ] Browser smoke dekt wizard happy path.

\---

## 9\. Fase 6 - Demo Spot Guided Flow

Doel: demo spot trading niet meer als technisch paneel, maar als veilige flow.

Stappen:

* \[ ] profile check;
* \[ ] credentials status/fingerprint;
* \[ ] connectivity check;
* \[ ] demo armed state;
* \[ ] order preview;
* \[ ] test order;
* \[ ] guarded demo place;
* \[ ] reconciliation;
* \[ ] cancel/open order management;
* \[ ] evidence/report.

Frontend:

```text
dashboard-v2/src/pages/DemoSpotWizardPage.tsx
```

Backend:

```text
src/binance\_spot\_bot/dashboard\_v2/demo\_spot\_flow.py
```

Acceptatiecriteria:

* \[ ] Flow blokkeert zonder demo profile.
* \[ ] Flow blokkeert zonder confirm waar nodig.
* \[ ] Flow toont duidelijk “demo only”.
* \[ ] Flow geeft evidence output.
* \[ ] UAT demo scenario pass.

\---

## 10\. Fase 7 - Paper Session Workflow Simplification

Nieuwe workflow page:

```text
dashboard-v2/src/pages/PaperSessionWorkflowPage.tsx
```

Operator acties:

* \[ ] start paper session;
* \[ ] monitor status/equity/position/risk;
* \[ ] pause/stop;
* \[ ] review fills/orders;
* \[ ] export session report;
* \[ ] compare with previous session;
* \[ ] create support/evidence if failed.

UX improvements:

* \[ ] one visible primary action at a time;
* \[ ] risk blockers shown next to action;
* \[ ] stop button always visible;
* \[ ] alerts summarized by severity;
* \[ ] report export after stop.

Acceptatiecriteria:

* \[ ] Paper session can complete guided flow.
* \[ ] Stop always accessible.
* \[ ] Risk block explanation available.
* \[ ] Session report link visible.
* \[ ] Browser smoke covers flow.

\---

## 11\. Fase 8 - Alerts, Blockers \& Runbook UX

Nieuwe componenten:

```text
AlertInbox.tsx
BlockerPanel.tsx
RunbookLink.tsx
ActionableIssue.tsx
```

Functionaliteit:

* \[ ] group alerts by severity;
* \[ ] group blockers by subsystem;
* \[ ] link blocker to playbook;
* \[ ] link blocker to CLI command;
* \[ ] show “what to do next”;
* \[ ] mark as reviewed locally;
* \[ ] export issue evidence;
* \[ ] no-live P0 always top.

Backend:

```text
src/binance\_spot\_bot/dashboard\_v2/actionable\_issues.py
```

Acceptatiecriteria:

* \[ ] Alerts zijn niet alleen losse JSON.
* \[ ] P0 no-live issue is impossible to hide.
* \[ ] Runbook links valid.
* \[ ] Reviewed state local-only.
* \[ ] Tests dekken grouping/priorities.

\---

## 12\. Fase 9 - Navigation \& Page Consolidation

Doel: van 36 technische pages naar duidelijke operatorgroepen.

Nieuwe navigatiegroepen:

* \[ ] Home
* \[ ] Start \& Monitor
* \[ ] Demo Spot
* \[ ] Paper Sessions
* \[ ] Market \& Strategy
* \[ ] Data/Model Ops
* \[ ] Portfolio
* \[ ] Evidence \& Support
* \[ ] System \& Safety
* \[ ] Training \& UAT
* \[ ] Advanced

Page consolidation matrix:

* \[ ] Overview + Bot Controls → Start \& Monitor
* \[ ] Demo Spot Trading + Demo Pilot → Demo Spot
* \[ ] Sessions + Orders/Account → Paper Sessions
* \[ ] Logs/Security + Readiness + Permissions → System \& Safety
* \[ ] Evidence + Support + Operator → Evidence \& Support
* \[ ] Roadmap/Stabilization/UAT/Training → Training \& UAT or Advanced
* \[ ] Research/Strategy Lab remains Advanced until simplified.

Acceptatiecriteria:

* \[ ] All 36 page registry items mapped to group.
* \[ ] No page orphaned.
* \[ ] Search/jump-to-page exists.
* \[ ] Advanced pages collapsed by default.
* \[ ] Browser smoke validates main groups.

\---

## 13\. Fase 10 - Global Command Palette

Frontend:

```text
dashboard-v2/src/components/CommandPalette.tsx
```

Features:

* \[ ] keyboard shortcut;
* \[ ] search pages;
* \[ ] search actions;
* \[ ] search CLI commands;
* \[ ] search docs/playbooks;
* \[ ] show safety level;
* \[ ] copy command;
* \[ ] navigate to page;
* \[ ] blocked action reason;
* \[ ] no live actions.

Backend:

```text
src/binance\_spot\_bot/dashboard\_v2/command\_palette.py
```

Acceptatiecriteria:

* \[ ] Command palette contains no live actions.
* \[ ] CLI commands copied are safe variants.
* \[ ] Search works locally.
* \[ ] Playbook links valid.
* \[ ] Tests dekken forbidden actions.

\---

## 14\. Fase 11 - UX Copy, Status Language \& Help Text Pass

Doel: verwarrende technische statusmeldingen duidelijk maken.

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/status\_language.py
```

Voorbeelden:

* \[ ] `waiting\_for\_data` → “Wachten op genoeg candle data”
* \[ ] `blocked` → “Geblokkeerd door safety/risk check”
* \[ ] `testnet-readiness` → “Readiness-check, geen orders”
* \[ ] `demo armed` → “Demo-acties toegestaan na guardrails”
* \[ ] `kill switch` → “Trading-acties geblokkeerd/veilig”

Checks:

* \[ ] status dictionary;
* \[ ] tooltip dictionary;
* \[ ] i18n-ready labels optional;
* \[ ] forbidden live approval wording scan;
* \[ ] consistency with operator glossary.

Acceptatiecriteria:

* \[ ] Common statuses hebben operatorvriendelijke uitleg.
* \[ ] Tooltips zichtbaar in critical actions.
* \[ ] No-live wording consistent.
* \[ ] Docs/glossary links werken.
* \[ ] Tests controleren forbidden phrases.

\---

## 15\. Fase 12 - Onboarding Wizard

Nieuwe page:

```text
dashboard-v2/src/pages/OnboardingWizardPage.tsx
```

Stappen:

* \[ ] local environment check;
* \[ ] no-live explanation;
* \[ ] data dir check;
* \[ ] dashboard health;
* \[ ] first demo source check;
* \[ ] first paper session smoke;
* \[ ] support bundle creation;
* \[ ] evidence export;
* \[ ] optional operator certification link.

Backend:

```text
src/binance\_spot\_bot/dashboard\_v2/onboarding.py
```

Acceptatiecriteria:

* \[ ] Onboarding works without API keys.
* \[ ] No-live proof is required step.
* \[ ] Optional steps clearly marked.
* \[ ] Progress saved locally.
* \[ ] UAT onboarding scenario pass.

\---

## 16\. Fase 13 - Dashboard V2 UX Metrics

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/ux\_metrics.py
```

Local-only metrics:

* \[ ] page load count;
* \[ ] action start count;
* \[ ] action success/fail;
* \[ ] blocked action count;
* \[ ] wizard completion rate;
* \[ ] time to start demo bot;
* \[ ] time to start paper session;
* \[ ] support bundle creation success;
* \[ ] evidence export success;
* \[ ] no-live proof views;
* \[ ] Streamlit fallback launches;
* \[ ] UAT feedback links.

Privacy:

* \[ ] local-only;
* \[ ] no remote telemetry;
* \[ ] no raw secrets;
* \[ ] can disable collection;
* \[ ] aggregate-only reports.

Acceptatiecriteria:

* \[ ] Metrics are local-only.
* \[ ] Metrics have opt-out.
* \[ ] Metrics are secret-free.
* \[ ] UX report uses aggregates.
* \[ ] Tests cover redaction.

\---

## 17\. Fase 14 - UAT Feedback Execution Tracker

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/uat\_feedback\_execution.py
```

Tracks:

* \[ ] feedback item id;
* \[ ] issue category;
* \[ ] chosen fix;
* \[ ] files changed;
* \[ ] validation command;
* \[ ] before score;
* \[ ] after score;
* \[ ] operator acceptance;
* \[ ] evidence path;
* \[ ] status.

Statuses:

* \[ ] planned;
* \[ ] in\_progress;
* \[ ] implemented;
* \[ ] validated;
* \[ ] rejected;
* \[ ] deferred;
* \[ ] closed.

Acceptatiecriteria:

* \[ ] UAT feedback items can be linked to fixes.
* \[ ] Closed item requires validation evidence.
* \[ ] No-live P0 cannot be deferred without fail status.
* \[ ] Report is Markdown + JSON.
* \[ ] Tests use fixture UAT backlog.

\---

## 18\. Fase 15 - Streamlit Fallback Policy

Nieuw doc:

```text
docs/dashboard-v2/streamlit-fallback-policy.md
```

Policy:

* \[ ] Streamlit remains fallback in Roadmap 107.
* \[ ] Streamlit can be used if V2 smoke fails.
* \[ ] Streamlit can be used for pages not yet stable in V2.
* \[ ] Streamlit should show legacy badge.
* \[ ] V2 should show fallback link.
* \[ ] Operator docs recommend V2 where gate passes.
* \[ ] Fallback usage should be measured locally.
* \[ ] Streamlit removal requires separate deprecation gate and roadmap.

Acceptatiecriteria:

* \[ ] Policy exists.
* \[ ] CLI help references policy.
* \[ ] Dashboard V2 fallback link exists.
* \[ ] Streamlit legacy badge exists or task created.
* \[ ] Tests validate docs/link presence.

\---

## 19\. Fase 16 - Streamlit Deprecation Readiness Matrix

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/streamlit\_deprecation\_readiness.py
```

Criteria:

* \[ ] V2 feature parity score;
* \[ ] V2 cutover readiness score;
* \[ ] V2 UAT pass score;
* \[ ] V2 browser smoke pass;
* \[ ] V2 API smoke pass;
* \[ ] V2 performance budgets pass;
* \[ ] V2 support/evidence pass;
* \[ ] operator docs V2-first;
* \[ ] Streamlit fallback still works;
* \[ ] remaining Streamlit-only pages;
* \[ ] remaining Streamlit-only actions;
* \[ ] fallback launch count.

Grades:

* \[ ] not\_ready;
* \[ ] preview\_ready;
* \[ ] recommended\_ready;
* \[ ] deprecation\_candidate;
* \[ ] removal\_candidate\_later.

Hard blockers:

* \[ ] no-live proof missing in V2;
* \[ ] V2 browser smoke failing;
* \[ ] critical route missing;
* \[ ] support/evidence export missing;
* \[ ] operator cannot start paper session in V2;
* \[ ] Streamlit fallback broken before deprecation.

Acceptatiecriteria:

* \[ ] Matrix is explainable.
* \[ ] Does not remove Streamlit.
* \[ ] Lists exact remaining blockers.
* \[ ] Report is Markdown + JSON.
* \[ ] Tests cover pass/fail cases.

\---

## 20\. Fase 17 - Streamlit Legacy Badge \& Exit Ramp

Changes to Streamlit UI:

* \[ ] Add clear `Legacy Streamlit Dashboard` badge.
* \[ ] Explain Dashboard V2 recommendation if ready.
* \[ ] Add link/command to launch Dashboard V2.
* \[ ] Keep no-live banner.
* \[ ] Keep all current safety guards.
* \[ ] Do not remove Streamlit features yet.
* \[ ] Optional: show “this page is migrated to V2” notes.

Acceptatiecriteria:

* \[ ] Streamlit still imports.
* \[ ] Streamlit no-live banner remains.
* \[ ] Legacy badge visible.
* \[ ] Dashboard V2 launch guidance visible.
* \[ ] Existing Streamlit tests pass.

\---

## 21\. Fase 18 - V2-First Docs \& CLI Help

Docs updates:

* \[ ] README recommends Dashboard V2 if readiness A/B.
* \[ ] Streamlit documented as fallback.
* \[ ] Operator manual uses V2 screenshots/routes.
* \[ ] CLI cookbook uses V2 commands first.
* \[ ] Troubleshooting includes V2 fallback steps.
* \[ ] UAT scenarios target V2 first.
* \[ ] Roadmap/milestone docs know V2-first status.

CLI help:

* \[ ] `dashboard` shows V2 recommendation.
* \[ ] `dashboard --v2` route.
* \[ ] `dashboard --legacy-streamlit` route.
* \[ ] `dashboard-v2-status`.
* \[ ] `dashboard-v2-fallback-info`.

Acceptatiecriteria:

* \[ ] Docs consistency passes.
* \[ ] No forbidden live wording.
* \[ ] Commands exist and are safe.
* \[ ] Operator can find fallback instructions.
* \[ ] Tests validate CLI help text.

\---

## 22\. Fase 19 - Accessibility \& Keyboard UX Pass

Dashboard V2 improvements:

* \[ ] keyboard navigation for core actions;
* \[ ] command palette shortcut;
* \[ ] visible focus states;
* \[ ] button labels clear;
* \[ ] color not only status indicator;
* \[ ] ARIA labels for critical controls;
* \[ ] chart alternative summary;
* \[ ] table captions;
* \[ ] reduced motion option;
* \[ ] readable font sizes.

Acceptatiecriteria:

* \[ ] Critical actions keyboard reachable.
* \[ ] No-live banner screen-reader friendly.
* \[ ] Buttons have labels.
* \[ ] Chart summary text exists.
* \[ ] Browser smoke/a11y smoke covers basics.

\---

## 23\. Fase 20 - Mobile/Small-Screen Local UX

Not full mobile app, but local browser layout should not break.

Tasks:

* \[ ] responsive header;
* \[ ] collapsible sidebar;
* \[ ] cards stack cleanly;
* \[ ] tables scroll horizontally;
* \[ ] charts resize;
* \[ ] action buttons remain visible;
* \[ ] stop button remains accessible;
* \[ ] no-live banner remains visible;
* \[ ] small-screen browser smoke.

Acceptatiecriteria:

* \[ ] 1366px desktop works.
* \[ ] 1024px tablet width works.
* \[ ] 390px mobile width not broken for read-only monitoring.
* \[ ] Stop button accessible.
* \[ ] No-live banner visible.

\---

## 24\. Fase 21 - Operator Workflow Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/workflow\_evidence\_bundle.py
```

Bundle bevat:

* \[ ] UX backlog report;
* \[ ] journey map;
* \[ ] guided action card report;
* \[ ] wizard validation report;
* \[ ] demo spot flow report;
* \[ ] paper session workflow report;
* \[ ] alerts/blockers UX report;
* \[ ] navigation consolidation report;
* \[ ] command palette safety report;
* \[ ] UX copy/status language report;
* \[ ] onboarding report;
* \[ ] UX metrics report;
* \[ ] UAT feedback execution report;
* \[ ] Streamlit fallback policy;
* \[ ] Streamlit deprecation readiness matrix;
* \[ ] no-live proof;
* \[ ] hashes.

Output:

```text
data/dashboard-v2/workflow-evidence/<run\_id>/
  dashboard\_v2\_workflow\_evidence\_manifest.json
  dashboard\_v2\_workflow\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[ ] Bundle is secret-free.
* \[ ] Bundle has manifest/hash.
* \[ ] Bundle links to Roadmap 103 UAT evidence.
* \[ ] Bundle links to Roadmap 106 cutover evidence.
* \[ ] Dashboard can download bundle.

\---

## 25\. Fase 22 - Check-All / Browser Smoke / UAT Gate Integration

Check-all additions:

* \[ ] Dashboard V2 UX route smoke.
* \[ ] Start wizard smoke.
* \[ ] Demo spot wizard smoke.
* \[ ] Paper session workflow smoke.
* \[ ] command palette safety smoke.
* \[ ] Streamlit fallback availability.
* \[ ] no-live banner on all main UX routes.
* \[ ] deprecation readiness report in deep profile.

UAT additions:

* \[ ] V2 home simplified scenario.
* \[ ] V2 start wizard scenario.
* \[ ] V2 paper session scenario.
* \[ ] V2 demo spot guided scenario.
* \[ ] V2 support/evidence scenario.
* \[ ] V2 fallback scenario.

Acceptatiecriteria:

* \[ ] Fast check-all stays reasonable.
* \[ ] Deep profile covers UX flows.
* \[ ] No-live missing hard fails.
* \[ ] Streamlit fallback missing warns/fails depending gate.
* \[ ] UAT evidence generated.

\---

## 26\. Fase 23 - Release/Knowledge/Test Integration

Roadmap 089:

* \[ ] Release notes mention Dashboard V2 UX changes.
* \[ ] Release candidate requires V2 UX evidence if V2-first.
* \[ ] Streamlit fallback policy included.

Roadmap 090:

* \[ ] Codex task packs can be generated from UX backlog.
* \[ ] Completion gate requires UX smoke/evidence.

Roadmap 091:

* \[ ] Knowledge graph maps operator journeys to frontend routes/backend APIs.
* \[ ] Impact analysis flags affected journeys.

Roadmap 092:

* \[ ] Test selector chooses UX smoke for route/action changes.
* \[ ] Test selector chooses Streamlit fallback test when fallback files change.

Roadmap 100/101/103:

* \[ ] Paper OS milestone includes V2 UX readiness.
* \[ ] Stabilization backlog imports V2 UX P0/P1.
* \[ ] UAT scorecards include V2 flow improvements.

Acceptatiecriteria:

* \[ ] Integration reports exist.
* \[ ] Test selection works.
* \[ ] Release evidence includes UX evidence.
* \[ ] UAT feedback closure visible.
* \[ ] No-live proof preserved.

\---

## 27\. CLI Commands

Nieuwe commands:

```powershell
python -m binance\_spot\_bot.cli dashboard-v2-ux-backlog --json
python -m binance\_spot\_bot.cli dashboard-v2-journey-map --json
python -m binance\_spot\_bot.cli dashboard-v2-guided-actions --json
python -m binance\_spot\_bot.cli dashboard-v2-start-wizard-smoke --json
python -m binance\_spot\_bot.cli dashboard-v2-demo-spot-flow-smoke --json
python -m binance\_spot\_bot.cli dashboard-v2-paper-session-flow-smoke --json
python -m binance\_spot\_bot.cli dashboard-v2-actionable-issues --json
python -m binance\_spot\_bot.cli dashboard-v2-navigation-map --json
python -m binance\_spot\_bot.cli dashboard-v2-command-palette-smoke --json
python -m binance\_spot\_bot.cli dashboard-v2-ux-metrics --json
python -m binance\_spot\_bot.cli dashboard-v2-uat-feedback-execution --json
python -m binance\_spot\_bot.cli dashboard-v2-streamlit-fallback-info --json
python -m binance\_spot\_bot.cli dashboard-v2-streamlit-deprecation-readiness --json
python -m binance\_spot\_bot.cli dashboard-v2-workflow-evidence-export
python -m binance\_spot\_bot.cli dashboard --v2
python -m binance\_spot\_bot.cli dashboard --legacy-streamlit
```

Acceptatiecriteria:

* \[ ] Commands werken offline.
* \[ ] Commands ondersteunen JSON waar relevant.
* \[ ] Commands gebruiken geen API keys.
* \[ ] Commands gebruiken geen signed/order/account endpoints.
* \[ ] Commands bevatten no-live statement.
* \[ ] Reports zijn secret-free.

\---

## 28\. Tests

### Backend/unit tests

* \[ ] `tests/test\_dashboard\_v2\_ux\_cutover\_safety\_contract.py`
* \[ ] `tests/test\_dashboard\_v2\_ux\_backlog\_ingest.py`
* \[ ] `tests/test\_dashboard\_v2\_operator\_journey\_map.py`
* \[ ] `tests/test\_dashboard\_v2\_start\_wizard.py`
* \[ ] `tests/test\_dashboard\_v2\_demo\_spot\_flow.py`
* \[ ] `tests/test\_dashboard\_v2\_actionable\_issues.py`
* \[ ] `tests/test\_dashboard\_v2\_command\_palette.py`
* \[ ] `tests/test\_dashboard\_v2\_status\_language.py`
* \[ ] `tests/test\_dashboard\_v2\_onboarding.py`
* \[ ] `tests/test\_dashboard\_v2\_ux\_metrics.py`
* \[ ] `tests/test\_dashboard\_v2\_uat\_feedback\_execution.py`
* \[ ] `tests/test\_dashboard\_v2\_streamlit\_deprecation\_readiness.py`
* \[ ] `tests/test\_dashboard\_v2\_workflow\_evidence\_bundle.py`

### Frontend tests

* \[ ] home action cards render;
* \[ ] guided card disabled reasons;
* \[ ] start wizard steps;
* \[ ] demo spot wizard guardrails;
* \[ ] paper session workflow;
* \[ ] alert/blocker grouping;
* \[ ] navigation groups;
* \[ ] command palette search;
* \[ ] no-live banner;
* \[ ] Streamlit fallback link;
* \[ ] responsive layout.

### Browser smoke

* \[ ] V2 home simplified;
* \[ ] start wizard happy path;
* \[ ] demo spot guarded flow blocked without confirm;
* \[ ] paper session flow;
* \[ ] evidence/support access;
* \[ ] command palette no live action;
* \[ ] no-live banner on all main routes;
* \[ ] Streamlit fallback link visible.

### Safety tests

* \[ ] live mode absent.
* \[ ] live actions absent.
* \[ ] signed/order/account commands absent.
* \[ ] no-live proof cannot be hidden.
* \[ ] UX feedback redacted.
* \[ ] Streamlit fallback not removed.
* \[ ] deprecation readiness cannot pass if V2 unsafe.
* \[ ] docs have no live approval wording.
* \[ ] check-all safe env preserved.

\---

## 29\. Docs

Nieuwe docs:

```text
docs/dashboard-v2/ux-cutover-safety-contract.md
docs/dashboard-v2/operator-journey-map.md
docs/dashboard-v2/guided-action-cards.md
docs/dashboard-v2/start-bot-wizard.md
docs/dashboard-v2/demo-spot-guided-flow.md
docs/dashboard-v2/paper-session-workflow.md
docs/dashboard-v2/alerts-blockers-runbook-ux.md
docs/dashboard-v2/navigation-consolidation.md
docs/dashboard-v2/command-palette.md
docs/dashboard-v2/status-language.md
docs/dashboard-v2/onboarding-wizard.md
docs/dashboard-v2/ux-metrics.md
docs/dashboard-v2/uat-feedback-execution.md
docs/dashboard-v2/streamlit-fallback-policy.md
docs/dashboard-v2/streamlit-deprecation-readiness.md
docs/dashboard-v2/workflow-evidence-bundle.md
```

README updates:

* \[ ] Dashboard V2 is recommended when readiness gate passes.
* \[ ] Streamlit is fallback/legacy.
* \[ ] V2 quick start.
* \[ ] V2 guided workflows.
* \[ ] V2 troubleshooting.
* \[ ] Streamlit fallback command.
* \[ ] No-live statement.

Operator manual updates:

* \[ ] V2-first screenshots/routes.
* \[ ] Start wizard.
* \[ ] Paper session workflow.
* \[ ] Demo spot guided flow.
* \[ ] Evidence/support flow.
* \[ ] Streamlit fallback guide.

\---

## 30\. Codex bouwvolgorde

### PR 1 - UX Cutover Safety Contract + UX Backlog Ingestor

* \[ ] `docs/dashboard-v2-ux-cutover-safety-contract.md`
* \[ ] `dashboard\_v2/ux\_backlog\_ingest.py`
* \[ ] tests for UAT/cutover report ingestion.
* \[ ] no-live P0 mapping tests.

### PR 2 - Operator Journey Map + Navigation Consolidation

* \[ ] `operator\_journey\_map.py`
* \[ ] navigation group mapping.
* \[ ] page registry coverage tests.

### PR 3 - Home Simplification + Guided Action Cards

* \[ ] simplified home layout.
* \[ ] guided action cards.
* \[ ] frontend card tests.

### PR 4 - Start Bot Wizard

* \[ ] `start\_wizard.py`
* \[ ] StartBotWizardPage.
* \[ ] API/action policy integration.
* \[ ] browser smoke.

### PR 5 - Demo Spot + Paper Session Guided Workflows

* \[ ] `demo\_spot\_flow.py`
* \[ ] PaperSessionWorkflowPage.
* \[ ] guided flow tests.

### PR 6 - Alerts/Blockers UX + Status Language

* \[ ] `actionable\_issues.py`
* \[ ] `status\_language.py`
* \[ ] runbook/status tests.

### PR 7 - Command Palette + Onboarding Wizard

* \[ ] `command\_palette.py`
* \[ ] `onboarding.py`
* \[ ] frontend command palette/onboarding tests.

### PR 8 - UX Metrics + UAT Feedback Execution

* \[ ] `ux\_metrics.py`
* \[ ] `uat\_feedback\_execution.py`
* \[ ] local-only metrics tests.

### PR 9 - Streamlit Fallback Policy + Deprecation Readiness

* \[ ] fallback docs.
* \[ ] `streamlit\_deprecation\_readiness.py`
* \[ ] Streamlit legacy badge.
* \[ ] CLI fallback commands.

### PR 10 - Evidence, Check-All, UAT, Release \& Docs

* \[ ] `workflow\_evidence\_bundle.py`
* \[ ] check-all integration.
* \[ ] UAT scenario updates.
* \[ ] release/knowledge/test integration.
* \[ ] README/operator docs.

\---

## 31\. Beste eerste Codex-opdracht

```text
Implementeer Roadmap 107 PR 1: Dashboard V2 UX Cutover Safety Contract + UX Backlog Ingestor.

Maak docs/dashboard-v2-ux-cutover-safety-contract.md.

Maak src/binance\_spot\_bot/dashboard\_v2/ux\_backlog\_ingest.py met:
- DashboardV2UxFinding
- DashboardV2UxBacklogItem
- DashboardV2UxBacklog
- DashboardV2UxIngestReport
- ingest\_dashboard\_v2\_ux\_backlog(root: Path)
- dashboard\_v2\_ux\_backlog\_to\_dict(...)
- write\_dashboard\_v2\_ux\_backlog(...)

De ingestor moet best-effort kunnen lezen:
- Roadmap 103 UAT feedback backlog JSON indien aanwezig
- Roadmap 106 cutover readiness JSON indien aanwezig
- Dashboard V2 browser smoke report JSON indien aanwezig
- Dashboard V2 performance budget report JSON indien aanwezig
- docs consistency report JSON indien aanwezig

Gedrag:
- ontbrekende input artifacts worden warnings, geen crash
- no-live/safety confusion wordt UX-P0
- critical workflow blocked wordt UX-P1
- high-friction common workflow wordt UX-P2
- duplicate findings worden gegroepeerd
- alle output bevat live\_trading\_enabled=False
- report bevat no\_live\_statement
- secret-like values worden geredact

Gebruik alleen stdlib.
Geen command execution.
Geen frontend execution.
Geen backend server starten.
Geen Streamlit wijzigen.
Geen GitHub API calls.
Geen signed endpoints.
Geen account/order endpoints.
Geen live trading.

Voeg tests toe voor:
- ingest complete fixture
- ingest missing artifacts
- no-live confusion maps to UX-P0
- critical workflow blocked maps to UX-P1
- duplicate grouping
- JSON serialization
- secret-like values worden geredact
- live\_trading\_enabled=False
- no\_live\_statement aanwezig
```

Waarom eerst:

* Roadmap 107 draait om het uitvoeren van UX/UAT-feedback; daarom moet eerst de backlog betrouwbaar ingelezen en geprioriteerd worden.
* Het is read-only en raakt runtime/trading/frontend niet.
* Het is klein genoeg voor Codex.
* No-live P0 mapping en secret-free output kunnen direct getest worden.
* Daarna kunnen journey maps, guided actions en Streamlit deprecation readiness veilig volgen.

\---

## 32\. Definition of Done

Roadmap 107 is klaar als:

* \[ ] Dashboard V2 UX/Cutover Safety Contract bestaat.
* \[ ] UX Backlog Ingestor werkt.
* \[ ] Operator Journey Map werkt.
* \[ ] Dashboard V2 Home Simplification werkt.
* \[ ] Guided Action Cards werken.
* \[ ] Runtime Start Wizard V2 werkt.
* \[ ] Demo Spot Guided Flow werkt.
* \[ ] Paper Session Workflow Simplification werkt.
* \[ ] Alerts, Blockers \& Runbook UX werkt.
* \[ ] Navigation \& Page Consolidation werkt.
* \[ ] Global Command Palette werkt.
* \[ ] UX Copy, Status Language \& Help Text Pass werkt.
* \[ ] Onboarding Wizard werkt.
* \[ ] Dashboard V2 UX Metrics werkt.
* \[ ] UAT Feedback Execution Tracker werkt.
* \[ ] Streamlit Fallback Policy bestaat.
* \[ ] Streamlit Deprecation Readiness Matrix werkt.
* \[ ] Streamlit Legacy Badge \& Exit Ramp werkt.
* \[ ] V2-first docs en CLI help bestaan.
* \[ ] Accessibility \& Keyboard UX Pass werkt.
* \[ ] Mobile/small-screen UX pass werkt.
* \[ ] Operator Workflow Evidence Bundle werkt.
* \[ ] Check-all/browser smoke/UAT gate integratie werkt.
* \[ ] Release/knowledge/test integratie werkt.
* \[ ] CLI commands werken.
* \[ ] Tests bewijzen geen live/signed/account/order endpoints.
* \[ ] Tests bewijzen no-live proof niet verborgen kan worden.
* \[ ] Tests bewijzen Streamlit fallback beschikbaar blijft.
* \[ ] Tests bewijzen UX evidence secret-free is.
* \[ ] Browser smoke blijft groen.
* \[ ] Check-all blijft groen.
* \[ ] Dashboard V2 is V2-first aanbevolen wanneer gate pass.
* \[ ] Streamlit is legacy/fallback maar niet verwijderd.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 107 kan na uitvoering naar `Voltooid docs`.

\---

## 33\. Verwachte Roadmap 108 daarna

Na Roadmap 107 zijn er twee logische paden.

Als Dashboard V2 goed scoort:

```text
Roadmap 108 - Dashboard V2 Legacy Streamlit Deprecation Execution, Final Parity Lock \& V2-Only Operator Mode
```

Mogelijke inhoud:

* \[ ] laatste Streamlit-only gaps sluiten;
* \[ ] V2-only operator mode;
* \[ ] Streamlit command naar legacy/fallback verplaatsen;
* \[ ] final fallback/rollback gate;
* \[ ] docs volledig V2-first;
* \[ ] still no live trading.

Als UX/performance nog issues heeft:

```text
Roadmap 108 - Dashboard V2 UX Regression Burn-Down, Workflow Polish \& Realtime Reliability Sprint
```

Mogelijke inhoud:

* \[ ] resterende UAT P0/P1/P2 oplossen;
* \[ ] chart/render latency verbeteren;
* \[ ] wizard frictie verminderen;
* \[ ] action copy/hints verbeteren;
* \[ ] browser smoke stabiliseren;
* \[ ] still no live trading.

```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Operator workflow simplification and grouped cockpit flow.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.

