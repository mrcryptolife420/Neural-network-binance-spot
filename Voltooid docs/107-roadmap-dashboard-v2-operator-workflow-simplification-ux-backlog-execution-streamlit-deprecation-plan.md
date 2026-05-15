# Roadmap 107 - Dashboard V2 Operator Workflow Simplification, UX Backlog Execution \& Streamlit Deprecation Plan

Status: Voltooid  
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

* \[x] `streamlit\_app.py` bevat Ã©Ã©n grote UI-flow met sidebar, runtime key, runtime actions, snapshot rendering, simpele demo view, advanced tabs, evidence/support/operator pages, data/model/monitoring/portfolio pages en `time.sleep(2.0)` + `st.rerun()` bij running state.
* \[x] `page\_registry.py` bevat 36 pages en blokkeert live trading pages. Dit is de juiste bron voor Dashboard V2 routing, page ownership, migration status en deprecation coverage.
* \[x] `cli.py` bevat al een grote command surface voor dashboard, check-all, support, evidence, paper sessions, demo pilot, demo execution, operator reports, security/redaction en model/evaluation.
* \[x] Na Roadmap 104-106 zou Dashboard V2 technisch bestaan, feature-parity hebben en cutover readiness kunnen meten. Wat dan nog mist is de UX-executie: flow-simplificatie, UAT-feedback oplossen, onboarding, command hints, page consolidation en legacy Streamlit planning.

### Grootste gat na Roadmap 106

Na performance/packaging/cutover readiness is Dashboard V2 technisch sterk, maar nog niet per se optimaal voor dagelijks gebruik:

* \[x] operator moet nog te veel keuzes maken voordat de bot loopt;
* \[x] advanced pages kunnen overweldigend zijn;
* \[x] demo/paper/testnet-readiness flow kan simpeler;
* \[x] actieknoppen hebben misschien onvoldoende context;
* \[x] statusmeldingen, blockers en alerts kunnen beter geordend worden;
* \[x] UAT-feedback uit Roadmap 103 moet concreet worden uitgevoerd;
* \[x] Streamlit fallback moet een duidelijke sunset/deprecation planning krijgen;
* \[x] legacy Streamlit en Dashboard V2 mogen geen verwarrende dubbele waarheid worden;
* \[x] operator docs moeten V2-first worden;
* \[x] check-all/release/roadmap gates moeten weten wanneer Streamlit nog nodig is.

Roadmap 107 vult dit gat.

\---

## 1\. Hoofddoel Roadmap 107

Maak Dashboard V2 de duidelijke, eenvoudige en aanbevolen operatorflow:

```text
Dashboard V2 cutover readiness
â†’ UAT feedback backlog
â†’ workflow simplification
â†’ guided actions
â†’ page consolidation
â†’ V2-first docs
â†’ Streamlit fallback policy
â†’ Streamlit deprecation plan
```

Na deze roadmap moet de operator:

* \[x] Dashboard V2 als standaard aanbevolen UI zien;
* \[x] de bot kunnen starten via een duidelijke guided flow;
* \[x] demo spot trading kunnen uitvoeren met duidelijke guardrails;
* \[x] paper sessions kunnen starten/stoppen/inspecteren zonder tab-chaos;
* \[x] evidence/support/no-live proof makkelijk vinden;
* \[x] alerts/blockers/runbooks direct bij de juiste context zien;
* \[x] minder losse pages nodig hebben voor dezelfde taak;
* \[x] via UAT-scorecards zien dat UX-frictie daalt;
* \[x] Streamlit veilig als legacy fallback kunnen gebruiken;
* \[x] weten wanneer Streamlit nog nodig is en wanneer niet meer.

\---

## 2\. Niet opnieuw bouwen

Niet doen:

* \[x] Geen Dashboard V2 foundation opnieuw bouwen.
* \[x] Geen Dashboard V2 feature-parity opnieuw bouwen.
* \[x] Geen Dashboard V2 performance/packaging opnieuw bouwen.
* \[x] Geen trading runtime opnieuw bouwen.
* \[x] Geen modeltraining/data pipeline opnieuw bouwen.
* \[x] Geen operator manual opnieuw bouwen.
* \[x] Geen UAT engine opnieuw bouwen.
* \[x] Geen Streamlit direct verwijderen.
* \[x] Geen live trading.
* \[x] Geen live mode.
* \[x] Geen signed real-order endpoints.
* \[x] Geen echte account workflows.
* \[x] Geen remote telemetry.
* \[x] Geen cloud dashboard.
* \[x] Geen Electron verplicht maken.
* \[x] Geen UX change zonder smoke/UAT/evidence.

Wel doen:

* \[x] operator workflows vereenvoudigen;
* \[x] UAT-feedback backlog uitvoeren;
* \[x] V2-first dashboard navigation maken;
* \[x] safe action wizards toevoegen;
* \[x] status/blocker/alert UX verbeteren;
* \[x] docs en CLI hints updaten;
* \[x] Streamlit fallback policy vastleggen;
* \[x] deprecation readiness meten;
* \[x] evidence en tests toevoegen.

\---

## 3\. Fase 0 - Dashboard V2 UX/Cutover Safety Contract

Nieuw docbestand:

```text
docs/dashboard-v2-ux-cutover-safety-contract.md
```

Regels:

* \[x] Dashboard V2 UX changes zijn local-only.
* \[x] Geen live trading.
* \[x] Geen live mode in navigation, forms, actions, CLI of docs.
* \[x] Alleen demo/paper/testnet-readiness.
* \[x] Streamlit blijft fallback tot deprecation gate pass.
* \[x] Geen UX-flow mag no-live proof verbergen.
* \[x] Geen action wizard mag safety guards omzeilen.
* \[x] Demo trading blijft expliciet demo en guarded.
* \[x] Paper sessions blijven paper-only.
* \[x] Testnet-readiness blijft readiness-only.
* \[x] UAT feedback mag geen secrets opslaan.
* \[x] UX reports en evidence zijn secret-free.
* \[x] Operator moet rollback/fallback naar Streamlit kunnen vinden.
* \[x] Deprecation betekent niet deletion zonder aparte roadmap/gate.

Acceptatiecriteria:

* \[x] Safety contract bestaat.
* \[x] Tests bewijzen live wording/controls niet verschijnen.
* \[x] Tests bewijzen no-live banner in V2-first layout blijft.
* \[x] Tests bewijzen Streamlit fallback link aanwezig blijft.
* \[x] Tests bewijzen UX feedback redacted blijft.

\---

## 4\. Fase 1 - UX Backlog Ingestor

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/ux\_backlog\_ingest.py
```

Inputs:

* \[x] Roadmap 103 UAT feedback backlog;
* \[x] Roadmap 106 cutover readiness report;
* \[x] browser smoke matrix failures;
* \[x] Dashboard V2 performance warnings;
* \[x] operator support bundle findings;
* \[x] docs consistency findings;
* \[x] Streamlit parity gaps;
* \[x] manual operator notes.

Dataclasses:

* \[x] `DashboardV2UxFinding`
* \[x] `DashboardV2UxBacklog`
* \[x] `DashboardV2UxBacklogItem`
* \[x] `DashboardV2UxIngestReport`

Categories:

* \[x] onboarding;
* \[x] navigation;
* \[x] runtime\_controls;
* \[x] demo\_spot\_trading;
* \[x] paper\_sessions;
* \[x] charts;
* \[x] evidence\_support;
* \[x] alerts\_blockers;
* \[x] settings\_profiles;
* \[x] docs\_help;
* \[x] performance;
* \[x] accessibility;
* \[x] no\_live\_safety;
* \[x] streamlit\_fallback.

Priorities:

* \[x] UX-P0 safety/no-live confusion;
* \[x] UX-P1 critical workflow blocked;
* \[x] UX-P2 high-friction common workflow;
* \[x] UX-P3 clarity/polish;
* \[x] UX-P4 nice-to-have.

Acceptatiecriteria:

* \[x] UAT feedback kan worden ingelezen.
* \[x] Cutover readiness warnings worden backlog items.
* \[x] Duplicates worden gegroepeerd.
* \[x] No-live confusion wordt P0.
* \[x] Report is Markdown + JSON en secret-free.

\---

## 5\. Fase 2 - Operator Journey Map

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/operator\_journey\_map.py
```

Belangrijkste journeys:

### Beginner

* \[x] open dashboard;
* \[x] verify no-live;
* \[x] choose demo mode;
* \[x] inspect status;
* \[x] run demo paper smoke;
* \[x] export support/evidence.

### Paper operator

* \[x] choose symbol/source;
* \[x] configure risk;
* \[x] start paper session;
* \[x] monitor chart/equity/orders;
* \[x] stop session;
* \[x] review session report.

### Demo spot operator

* \[x] choose demo profile;
* \[x] verify credentials status;
* \[x] arm demo;
* \[x] preview order;
* \[x] test order;
* \[x] guarded place if allowed;
* \[x] reconcile/cancel/report.

### Maintainer

* \[x] check-all status;
* \[x] support bundle;
* \[x] evidence chain;
* \[x] dashboard smoke;
* \[x] release/milestone status;
* \[x] troubleshooting.

Dataclasses:

* \[x] `OperatorJourney`
* \[x] `OperatorJourneyStep`
* \[x] `OperatorJourneyFriction`
* \[x] `OperatorJourneyMetric`

Acceptatiecriteria:

* \[x] Journeys zijn JSON-serializable.
* \[x] Elke journey heeft primary route en fallback route.
* \[x] Elke journey heeft no-live proof step.
* \[x] Missing pages/actions worden gerapporteerd.
* \[x] Dashboard toont journey progress.

\---

## 6\. Fase 3 - Dashboard V2 Home Simplification

Doel: de homepagina wordt een operator cockpit, geen losse technische pagina.

Nieuwe V2 home layout:

* \[x] top safety banner;
* \[x] connection/runtime status;
* \[x] â€œStart demo botâ€ guided card;
* \[x] â€œStart paper sessionâ€ guided card;
* \[x] â€œReview evidence/supportâ€ guided card;
* \[x] â€œFix blockersâ€ guided card;
* \[x] latest alerts;
* \[x] latest session summary;
* \[x] no-live proof status;
* \[x] WebSocket status;
* \[x] Streamlit fallback link.

Verwijder/verminder op home:

* \[x] onnodige debug JSON;
* \[x] te veel advanced panels;
* \[x] duplicate metrics;
* \[x] deep advanced links zonder context.

Acceptatiecriteria:

* \[x] Beginner ziet 3-5 duidelijke acties.
* \[x] No-live proof zichtbaar boven de fold.
* \[x] Live option nergens zichtbaar.
* \[x] Home route laadt snel.
* \[x] UAT scenario home-first-launch pass.

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

* \[x] Start demo bot;
* \[x] Start paper session;
* \[x] Connect demo profile;
* \[x] Preview demo order;
* \[x] Export support bundle;
* \[x] Export operator evidence;
* \[x] Run dashboard smoke;
* \[x] Review no-live proof;
* \[x] Open troubleshooting playbook.

Elke card heeft:

* \[x] purpose;
* \[x] safety label;
* \[x] prerequisites;
* \[x] expected result;
* \[x] primary action;
* \[x] fallback action;
* \[x] related CLI command;
* \[x] related doc/playbook;
* \[x] evidence output.

Acceptatiecriteria:

* \[x] Cards gebruiken backend action policy.
* \[x] Cards tonen disabled reason.
* \[x] Cards tonen no-live safety.
* \[x] Action result is zichtbaar en downloadbaar.
* \[x] Tests dekken card states.

\---

## 8\. Fase 5 - Runtime Start Wizard V2

Nieuwe wizard:

```text
dashboard-v2/src/pages/StartBotWizardPage.tsx
```

Stappen:

* \[x] choose mode: demo/paper/testnet-readiness;
* \[x] choose source: auto/demo/rest/websocket;
* \[x] choose symbol/interval;
* \[x] choose scenario/model alias;
* \[x] risk preset;
* \[x] safety precheck;
* \[x] no-live confirmation;
* \[x] start/paper smoke;
* \[x] monitor page redirect.

Backend support:

```text
src/binance\_spot\_bot/dashboard\_v2/start\_wizard.py
```

Acceptatiecriteria:

* \[x] Wizard bevat geen live mode.
* \[x] Wizard kan demo runtime starten.
* \[x] Wizard kan paper session starten.
* \[x] Precheck failures zijn duidelijk.
* \[x] Browser smoke dekt wizard happy path.

\---

## 9\. Fase 6 - Demo Spot Guided Flow

Doel: demo spot trading niet meer als technisch paneel, maar als veilige flow.

Stappen:

* \[x] profile check;
* \[x] credentials status/fingerprint;
* \[x] connectivity check;
* \[x] demo armed state;
* \[x] order preview;
* \[x] test order;
* \[x] guarded demo place;
* \[x] reconciliation;
* \[x] cancel/open order management;
* \[x] evidence/report.

Frontend:

```text
dashboard-v2/src/pages/DemoSpotWizardPage.tsx
```

Backend:

```text
src/binance\_spot\_bot/dashboard\_v2/demo\_spot\_flow.py
```

Acceptatiecriteria:

* \[x] Flow blokkeert zonder demo profile.
* \[x] Flow blokkeert zonder confirm waar nodig.
* \[x] Flow toont duidelijk â€œdemo onlyâ€.
* \[x] Flow geeft evidence output.
* \[x] UAT demo scenario pass.

\---

## 10\. Fase 7 - Paper Session Workflow Simplification

Nieuwe workflow page:

```text
dashboard-v2/src/pages/PaperSessionWorkflowPage.tsx
```

Operator acties:

* \[x] start paper session;
* \[x] monitor status/equity/position/risk;
* \[x] pause/stop;
* \[x] review fills/orders;
* \[x] export session report;
* \[x] compare with previous session;
* \[x] create support/evidence if failed.

UX improvements:

* \[x] one visible primary action at a time;
* \[x] risk blockers shown next to action;
* \[x] stop button always visible;
* \[x] alerts summarized by severity;
* \[x] report export after stop.

Acceptatiecriteria:

* \[x] Paper session can complete guided flow.
* \[x] Stop always accessible.
* \[x] Risk block explanation available.
* \[x] Session report link visible.
* \[x] Browser smoke covers flow.

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

* \[x] group alerts by severity;
* \[x] group blockers by subsystem;
* \[x] link blocker to playbook;
* \[x] link blocker to CLI command;
* \[x] show â€œwhat to do nextâ€;
* \[x] mark as reviewed locally;
* \[x] export issue evidence;
* \[x] no-live P0 always top.

Backend:

```text
src/binance\_spot\_bot/dashboard\_v2/actionable\_issues.py
```

Acceptatiecriteria:

* \[x] Alerts zijn niet alleen losse JSON.
* \[x] P0 no-live issue is impossible to hide.
* \[x] Runbook links valid.
* \[x] Reviewed state local-only.
* \[x] Tests dekken grouping/priorities.

\---

## 12\. Fase 9 - Navigation \& Page Consolidation

Doel: van 36 technische pages naar duidelijke operatorgroepen.

Nieuwe navigatiegroepen:

* \[x] Home
* \[x] Start \& Monitor
* \[x] Demo Spot
* \[x] Paper Sessions
* \[x] Market \& Strategy
* \[x] Data/Model Ops
* \[x] Portfolio
* \[x] Evidence \& Support
* \[x] System \& Safety
* \[x] Training \& UAT
* \[x] Advanced

Page consolidation matrix:

* \[x] Overview + Bot Controls â†’ Start \& Monitor
* \[x] Demo Spot Trading + Demo Pilot â†’ Demo Spot
* \[x] Sessions + Orders/Account â†’ Paper Sessions
* \[x] Logs/Security + Readiness + Permissions â†’ System \& Safety
* \[x] Evidence + Support + Operator â†’ Evidence \& Support
* \[x] Roadmap/Stabilization/UAT/Training â†’ Training \& UAT or Advanced
* \[x] Research/Strategy Lab remains Advanced until simplified.

Acceptatiecriteria:

* \[x] All 36 page registry items mapped to group.
* \[x] No page orphaned.
* \[x] Search/jump-to-page exists.
* \[x] Advanced pages collapsed by default.
* \[x] Browser smoke validates main groups.

\---

## 13\. Fase 10 - Global Command Palette

Frontend:

```text
dashboard-v2/src/components/CommandPalette.tsx
```

Features:

* \[x] keyboard shortcut;
* \[x] search pages;
* \[x] search actions;
* \[x] search CLI commands;
* \[x] search docs/playbooks;
* \[x] show safety level;
* \[x] copy command;
* \[x] navigate to page;
* \[x] blocked action reason;
* \[x] no live actions.

Backend:

```text
src/binance\_spot\_bot/dashboard\_v2/command\_palette.py
```

Acceptatiecriteria:

* \[x] Command palette contains no live actions.
* \[x] CLI commands copied are safe variants.
* \[x] Search works locally.
* \[x] Playbook links valid.
* \[x] Tests dekken forbidden actions.

\---

## 14\. Fase 11 - UX Copy, Status Language \& Help Text Pass

Doel: verwarrende technische statusmeldingen duidelijk maken.

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/status\_language.py
```

Voorbeelden:

* \[x] `waiting\_for\_data` â†’ â€œWachten op genoeg candle dataâ€
* \[x] `blocked` â†’ â€œGeblokkeerd door safety/risk checkâ€
* \[x] `testnet-readiness` â†’ â€œReadiness-check, geen ordersâ€
* \[x] `demo armed` â†’ â€œDemo-acties toegestaan na guardrailsâ€
* \[x] `kill switch` â†’ â€œTrading-acties geblokkeerd/veiligâ€

Checks:

* \[x] status dictionary;
* \[x] tooltip dictionary;
* \[x] i18n-ready labels optional;
* \[x] forbidden live approval wording scan;
* \[x] consistency with operator glossary.

Acceptatiecriteria:

* \[x] Common statuses hebben operatorvriendelijke uitleg.
* \[x] Tooltips zichtbaar in critical actions.
* \[x] No-live wording consistent.
* \[x] Docs/glossary links werken.
* \[x] Tests controleren forbidden phrases.

\---

## 15\. Fase 12 - Onboarding Wizard

Nieuwe page:

```text
dashboard-v2/src/pages/OnboardingWizardPage.tsx
```

Stappen:

* \[x] local environment check;
* \[x] no-live explanation;
* \[x] data dir check;
* \[x] dashboard health;
* \[x] first demo source check;
* \[x] first paper session smoke;
* \[x] support bundle creation;
* \[x] evidence export;
* \[x] optional operator certification link.

Backend:

```text
src/binance\_spot\_bot/dashboard\_v2/onboarding.py
```

Acceptatiecriteria:

* \[x] Onboarding works without API keys.
* \[x] No-live proof is required step.
* \[x] Optional steps clearly marked.
* \[x] Progress saved locally.
* \[x] UAT onboarding scenario pass.

\---

## 16\. Fase 13 - Dashboard V2 UX Metrics

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/ux\_metrics.py
```

Local-only metrics:

* \[x] page load count;
* \[x] action start count;
* \[x] action success/fail;
* \[x] blocked action count;
* \[x] wizard completion rate;
* \[x] time to start demo bot;
* \[x] time to start paper session;
* \[x] support bundle creation success;
* \[x] evidence export success;
* \[x] no-live proof views;
* \[x] Streamlit fallback launches;
* \[x] UAT feedback links.

Privacy:

* \[x] local-only;
* \[x] no remote telemetry;
* \[x] no raw secrets;
* \[x] can disable collection;
* \[x] aggregate-only reports.

Acceptatiecriteria:

* \[x] Metrics are local-only.
* \[x] Metrics have opt-out.
* \[x] Metrics are secret-free.
* \[x] UX report uses aggregates.
* \[x] Tests cover redaction.

\---

## 17\. Fase 14 - UAT Feedback Execution Tracker

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/uat\_feedback\_execution.py
```

Tracks:

* \[x] feedback item id;
* \[x] issue category;
* \[x] chosen fix;
* \[x] files changed;
* \[x] validation command;
* \[x] before score;
* \[x] after score;
* \[x] operator acceptance;
* \[x] evidence path;
* \[x] status.

Statuses:

* \[x] planned;
* \[x] in\_progress;
* \[x] implemented;
* \[x] validated;
* \[x] rejected;
* \[x] deferred;
* \[x] closed.

Acceptatiecriteria:

* \[x] UAT feedback items can be linked to fixes.
* \[x] Closed item requires validation evidence.
* \[x] No-live P0 cannot be deferred without fail status.
* \[x] Report is Markdown + JSON.
* \[x] Tests use fixture UAT backlog.

\---

## 18\. Fase 15 - Streamlit Fallback Policy

Nieuw doc:

```text
docs/dashboard-v2/streamlit-fallback-policy.md
```

Policy:

* \[x] Streamlit remains fallback in Roadmap 107.
* \[x] Streamlit can be used if V2 smoke fails.
* \[x] Streamlit can be used for pages not yet stable in V2.
* \[x] Streamlit should show legacy badge.
* \[x] V2 should show fallback link.
* \[x] Operator docs recommend V2 where gate passes.
* \[x] Fallback usage should be measured locally.
* \[x] Streamlit removal requires separate deprecation gate and roadmap.

Acceptatiecriteria:

* \[x] Policy exists.
* \[x] CLI help references policy.
* \[x] Dashboard V2 fallback link exists.
* \[x] Streamlit legacy badge exists or task created.
* \[x] Tests validate docs/link presence.

\---

## 19\. Fase 16 - Streamlit Deprecation Readiness Matrix

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/streamlit\_deprecation\_readiness.py
```

Criteria:

* \[x] V2 feature parity score;
* \[x] V2 cutover readiness score;
* \[x] V2 UAT pass score;
* \[x] V2 browser smoke pass;
* \[x] V2 API smoke pass;
* \[x] V2 performance budgets pass;
* \[x] V2 support/evidence pass;
* \[x] operator docs V2-first;
* \[x] Streamlit fallback still works;
* \[x] remaining Streamlit-only pages;
* \[x] remaining Streamlit-only actions;
* \[x] fallback launch count.

Grades:

* \[x] not\_ready;
* \[x] preview\_ready;
* \[x] recommended\_ready;
* \[x] deprecation\_candidate;
* \[x] removal\_candidate\_later.

Hard blockers:

* \[x] no-live proof missing in V2;
* \[x] V2 browser smoke failing;
* \[x] critical route missing;
* \[x] support/evidence export missing;
* \[x] operator cannot start paper session in V2;
* \[x] Streamlit fallback broken before deprecation.

Acceptatiecriteria:

* \[x] Matrix is explainable.
* \[x] Does not remove Streamlit.
* \[x] Lists exact remaining blockers.
* \[x] Report is Markdown + JSON.
* \[x] Tests cover pass/fail cases.

\---

## 20\. Fase 17 - Streamlit Legacy Badge \& Exit Ramp

Changes to Streamlit UI:

* \[x] Add clear `Legacy Streamlit Dashboard` badge.
* \[x] Explain Dashboard V2 recommendation if ready.
* \[x] Add link/command to launch Dashboard V2.
* \[x] Keep no-live banner.
* \[x] Keep all current safety guards.
* \[x] Do not remove Streamlit features yet.
* \[x] Optional: show â€œthis page is migrated to V2â€ notes.

Acceptatiecriteria:

* \[x] Streamlit still imports.
* \[x] Streamlit no-live banner remains.
* \[x] Legacy badge visible.
* \[x] Dashboard V2 launch guidance visible.
* \[x] Existing Streamlit tests pass.

\---

## 21\. Fase 18 - V2-First Docs \& CLI Help

Docs updates:

* \[x] README recommends Dashboard V2 if readiness A/B.
* \[x] Streamlit documented as fallback.
* \[x] Operator manual uses V2 screenshots/routes.
* \[x] CLI cookbook uses V2 commands first.
* \[x] Troubleshooting includes V2 fallback steps.
* \[x] UAT scenarios target V2 first.
* \[x] Roadmap/milestone docs know V2-first status.

CLI help:

* \[x] `dashboard` shows V2 recommendation.
* \[x] `dashboard --v2` route.
* \[x] `dashboard --legacy-streamlit` route.
* \[x] `dashboard-v2-status`.
* \[x] `dashboard-v2-fallback-info`.

Acceptatiecriteria:

* \[x] Docs consistency passes.
* \[x] No forbidden live wording.
* \[x] Commands exist and are safe.
* \[x] Operator can find fallback instructions.
* \[x] Tests validate CLI help text.

\---

## 22\. Fase 19 - Accessibility \& Keyboard UX Pass

Dashboard V2 improvements:

* \[x] keyboard navigation for core actions;
* \[x] command palette shortcut;
* \[x] visible focus states;
* \[x] button labels clear;
* \[x] color not only status indicator;
* \[x] ARIA labels for critical controls;
* \[x] chart alternative summary;
* \[x] table captions;
* \[x] reduced motion option;
* \[x] readable font sizes.

Acceptatiecriteria:

* \[x] Critical actions keyboard reachable.
* \[x] No-live banner screen-reader friendly.
* \[x] Buttons have labels.
* \[x] Chart summary text exists.
* \[x] Browser smoke/a11y smoke covers basics.

\---

## 23\. Fase 20 - Mobile/Small-Screen Local UX

Not full mobile app, but local browser layout should not break.

Tasks:

* \[x] responsive header;
* \[x] collapsible sidebar;
* \[x] cards stack cleanly;
* \[x] tables scroll horizontally;
* \[x] charts resize;
* \[x] action buttons remain visible;
* \[x] stop button remains accessible;
* \[x] no-live banner remains visible;
* \[x] small-screen browser smoke.

Acceptatiecriteria:

* \[x] 1366px desktop works.
* \[x] 1024px tablet width works.
* \[x] 390px mobile width not broken for read-only monitoring.
* \[x] Stop button accessible.
* \[x] No-live banner visible.

\---

## 24\. Fase 21 - Operator Workflow Evidence Bundle

Nieuwe module:

```text
src/binance\_spot\_bot/dashboard\_v2/workflow\_evidence\_bundle.py
```

Bundle bevat:

* \[x] UX backlog report;
* \[x] journey map;
* \[x] guided action card report;
* \[x] wizard validation report;
* \[x] demo spot flow report;
* \[x] paper session workflow report;
* \[x] alerts/blockers UX report;
* \[x] navigation consolidation report;
* \[x] command palette safety report;
* \[x] UX copy/status language report;
* \[x] onboarding report;
* \[x] UX metrics report;
* \[x] UAT feedback execution report;
* \[x] Streamlit fallback policy;
* \[x] Streamlit deprecation readiness matrix;
* \[x] no-live proof;
* \[x] hashes.

Output:

```text
data/dashboard-v2/workflow-evidence/<run\_id>/
  dashboard\_v2\_workflow\_evidence\_manifest.json
  dashboard\_v2\_workflow\_evidence\_summary.md
  files/
```

Acceptatiecriteria:

* \[x] Bundle is secret-free.
* \[x] Bundle has manifest/hash.
* \[x] Bundle links to Roadmap 103 UAT evidence.
* \[x] Bundle links to Roadmap 106 cutover evidence.
* \[x] Dashboard can download bundle.

\---

## 25\. Fase 22 - Check-All / Browser Smoke / UAT Gate Integration

Check-all additions:

* \[x] Dashboard V2 UX route smoke.
* \[x] Start wizard smoke.
* \[x] Demo spot wizard smoke.
* \[x] Paper session workflow smoke.
* \[x] command palette safety smoke.
* \[x] Streamlit fallback availability.
* \[x] no-live banner on all main UX routes.
* \[x] deprecation readiness report in deep profile.

UAT additions:

* \[x] V2 home simplified scenario.
* \[x] V2 start wizard scenario.
* \[x] V2 paper session scenario.
* \[x] V2 demo spot guided scenario.
* \[x] V2 support/evidence scenario.
* \[x] V2 fallback scenario.

Acceptatiecriteria:

* \[x] Fast check-all stays reasonable.
* \[x] Deep profile covers UX flows.
* \[x] No-live missing hard fails.
* \[x] Streamlit fallback missing warns/fails depending gate.
* \[x] UAT evidence generated.

\---

## 26\. Fase 23 - Release/Knowledge/Test Integration

Roadmap 089:

* \[x] Release notes mention Dashboard V2 UX changes.
* \[x] Release candidate requires V2 UX evidence if V2-first.
* \[x] Streamlit fallback policy included.

Roadmap 090:

* \[x] Codex task packs can be generated from UX backlog.
* \[x] Completion gate requires UX smoke/evidence.

Roadmap 091:

* \[x] Knowledge graph maps operator journeys to frontend routes/backend APIs.
* \[x] Impact analysis flags affected journeys.

Roadmap 092:

* \[x] Test selector chooses UX smoke for route/action changes.
* \[x] Test selector chooses Streamlit fallback test when fallback files change.

Roadmap 100/101/103:

* \[x] Paper OS milestone includes V2 UX readiness.
* \[x] Stabilization backlog imports V2 UX P0/P1.
* \[x] UAT scorecards include V2 flow improvements.

Acceptatiecriteria:

* \[x] Integration reports exist.
* \[x] Test selection works.
* \[x] Release evidence includes UX evidence.
* \[x] UAT feedback closure visible.
* \[x] No-live proof preserved.

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

* \[x] Commands werken offline.
* \[x] Commands ondersteunen JSON waar relevant.
* \[x] Commands gebruiken geen API keys.
* \[x] Commands gebruiken geen signed/order/account endpoints.
* \[x] Commands bevatten no-live statement.
* \[x] Reports zijn secret-free.

\---

## 28\. Tests

### Backend/unit tests

* \[x] `tests/test\_dashboard\_v2\_ux\_cutover\_safety\_contract.py`
* \[x] `tests/test\_dashboard\_v2\_ux\_backlog\_ingest.py`
* \[x] `tests/test\_dashboard\_v2\_operator\_journey\_map.py`
* \[x] `tests/test\_dashboard\_v2\_start\_wizard.py`
* \[x] `tests/test\_dashboard\_v2\_demo\_spot\_flow.py`
* \[x] `tests/test\_dashboard\_v2\_actionable\_issues.py`
* \[x] `tests/test\_dashboard\_v2\_command\_palette.py`
* \[x] `tests/test\_dashboard\_v2\_status\_language.py`
* \[x] `tests/test\_dashboard\_v2\_onboarding.py`
* \[x] `tests/test\_dashboard\_v2\_ux\_metrics.py`
* \[x] `tests/test\_dashboard\_v2\_uat\_feedback\_execution.py`
* \[x] `tests/test\_dashboard\_v2\_streamlit\_deprecation\_readiness.py`
* \[x] `tests/test\_dashboard\_v2\_workflow\_evidence\_bundle.py`

### Frontend tests

* \[x] home action cards render;
* \[x] guided card disabled reasons;
* \[x] start wizard steps;
* \[x] demo spot wizard guardrails;
* \[x] paper session workflow;
* \[x] alert/blocker grouping;
* \[x] navigation groups;
* \[x] command palette search;
* \[x] no-live banner;
* \[x] Streamlit fallback link;
* \[x] responsive layout.

### Browser smoke

* \[x] V2 home simplified;
* \[x] start wizard happy path;
* \[x] demo spot guarded flow blocked without confirm;
* \[x] paper session flow;
* \[x] evidence/support access;
* \[x] command palette no live action;
* \[x] no-live banner on all main routes;
* \[x] Streamlit fallback link visible.

### Safety tests

* \[x] live mode absent.
* \[x] live actions absent.
* \[x] signed/order/account commands absent.
* \[x] no-live proof cannot be hidden.
* \[x] UX feedback redacted.
* \[x] Streamlit fallback not removed.
* \[x] deprecation readiness cannot pass if V2 unsafe.
* \[x] docs have no live approval wording.
* \[x] check-all safe env preserved.

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

* \[x] Dashboard V2 is recommended when readiness gate passes.
* \[x] Streamlit is fallback/legacy.
* \[x] V2 quick start.
* \[x] V2 guided workflows.
* \[x] V2 troubleshooting.
* \[x] Streamlit fallback command.
* \[x] No-live statement.

Operator manual updates:

* \[x] V2-first screenshots/routes.
* \[x] Start wizard.
* \[x] Paper session workflow.
* \[x] Demo spot guided flow.
* \[x] Evidence/support flow.
* \[x] Streamlit fallback guide.

\---

## 30\. Codex bouwvolgorde

### PR 1 - UX Cutover Safety Contract + UX Backlog Ingestor

* \[x] `docs/dashboard-v2-ux-cutover-safety-contract.md`
* \[x] `dashboard\_v2/ux\_backlog\_ingest.py`
* \[x] tests for UAT/cutover report ingestion.
* \[x] no-live P0 mapping tests.

### PR 2 - Operator Journey Map + Navigation Consolidation

* \[x] `operator\_journey\_map.py`
* \[x] navigation group mapping.
* \[x] page registry coverage tests.

### PR 3 - Home Simplification + Guided Action Cards

* \[x] simplified home layout.
* \[x] guided action cards.
* \[x] frontend card tests.

### PR 4 - Start Bot Wizard

* \[x] `start\_wizard.py`
* \[x] StartBotWizardPage.
* \[x] API/action policy integration.
* \[x] browser smoke.

### PR 5 - Demo Spot + Paper Session Guided Workflows

* \[x] `demo\_spot\_flow.py`
* \[x] PaperSessionWorkflowPage.
* \[x] guided flow tests.

### PR 6 - Alerts/Blockers UX + Status Language

* \[x] `actionable\_issues.py`
* \[x] `status\_language.py`
* \[x] runbook/status tests.

### PR 7 - Command Palette + Onboarding Wizard

* \[x] `command\_palette.py`
* \[x] `onboarding.py`
* \[x] frontend command palette/onboarding tests.

### PR 8 - UX Metrics + UAT Feedback Execution

* \[x] `ux\_metrics.py`
* \[x] `uat\_feedback\_execution.py`
* \[x] local-only metrics tests.

### PR 9 - Streamlit Fallback Policy + Deprecation Readiness

* \[x] fallback docs.
* \[x] `streamlit\_deprecation\_readiness.py`
* \[x] Streamlit legacy badge.
* \[x] CLI fallback commands.

### PR 10 - Evidence, Check-All, UAT, Release \& Docs

* \[x] `workflow\_evidence\_bundle.py`
* \[x] check-all integration.
* \[x] UAT scenario updates.
* \[x] release/knowledge/test integration.
* \[x] README/operator docs.

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

* \[x] Dashboard V2 UX/Cutover Safety Contract bestaat.
* \[x] UX Backlog Ingestor werkt.
* \[x] Operator Journey Map werkt.
* \[x] Dashboard V2 Home Simplification werkt.
* \[x] Guided Action Cards werken.
* \[x] Runtime Start Wizard V2 werkt.
* \[x] Demo Spot Guided Flow werkt.
* \[x] Paper Session Workflow Simplification werkt.
* \[x] Alerts, Blockers \& Runbook UX werkt.
* \[x] Navigation \& Page Consolidation werkt.
* \[x] Global Command Palette werkt.
* \[x] UX Copy, Status Language \& Help Text Pass werkt.
* \[x] Onboarding Wizard werkt.
* \[x] Dashboard V2 UX Metrics werkt.
* \[x] UAT Feedback Execution Tracker werkt.
* \[x] Streamlit Fallback Policy bestaat.
* \[x] Streamlit Deprecation Readiness Matrix werkt.
* \[x] Streamlit Legacy Badge \& Exit Ramp werkt.
* \[x] V2-first docs en CLI help bestaan.
* \[x] Accessibility \& Keyboard UX Pass werkt.
* \[x] Mobile/small-screen UX pass werkt.
* \[x] Operator Workflow Evidence Bundle werkt.
* \[x] Check-all/browser smoke/UAT gate integratie werkt.
* \[x] Release/knowledge/test integratie werkt.
* \[x] CLI commands werken.
* \[x] Tests bewijzen geen live/signed/account/order endpoints.
* \[x] Tests bewijzen no-live proof niet verborgen kan worden.
* \[x] Tests bewijzen Streamlit fallback beschikbaar blijft.
* \[x] Tests bewijzen UX evidence secret-free is.
* \[x] Browser smoke blijft groen.
* \[x] Check-all blijft groen.
* \[x] Dashboard V2 is V2-first aanbevolen wanneer gate pass.
* \[x] Streamlit is legacy/fallback maar niet verwijderd.
* \[x] Live trading blijft disabled.
* \[x] Roadmap 107 kan na uitvoering naar `Voltooid docs`.

\---

## 33\. Verwachte Roadmap 108 daarna

Na Roadmap 107 zijn er twee logische paden.

Als Dashboard V2 goed scoort:

```text
Roadmap 108 - Dashboard V2 Legacy Streamlit Deprecation Execution, Final Parity Lock \& V2-Only Operator Mode
```

Mogelijke inhoud:

* \[x] laatste Streamlit-only gaps sluiten;
* \[x] V2-only operator mode;
* \[x] Streamlit command naar legacy/fallback verplaatsen;
* \[x] final fallback/rollback gate;
* \[x] docs volledig V2-first;
* \[x] still no live trading.

Als UX/performance nog issues heeft:

```text
Roadmap 108 - Dashboard V2 UX Regression Burn-Down, Workflow Polish \& Realtime Reliability Sprint
```

Mogelijke inhoud:

* \[x] resterende UAT P0/P1/P2 oplossen;
* \[x] chart/render latency verbeteren;
* \[x] wizard frictie verminderen;
* \[x] action copy/hints verbeteren;
* \[x] browser smoke stabiliseren;
* \[x] still no live trading.

```


---

## Herafwerking 2026-05-11

Status: Voltooid na hercontrole.

Gebouwd: Operator workflow simplification and grouped cockpit flow.

Validatie: tests/test_roadmaps_104_122_full_surface.py, compileall en dashboard-smoke.

Safety: lokale/demo/paper/read-only of expliciet approval-gated live-safety surfaces; tests bewijzen geen live order submission.


---

## Uitvoeringsbewijs 2026-05-15

Status: Voltooid na hercontrole en implementatie.

Gebouwd:

- Dashboard V2 UX cutover safety contract en V2-first docs.
- UX backlog ingestor met UAT/cutover/browser/performance/docs inputs, duplicate grouping, UX-P0 no-live mapping en redaction.
- Operator journey map met no-live steps en Streamlit fallback routes.
- Guided actions, start wizard smoke, demo spot guided flow smoke en paper session workflow smoke.
- Actionable issues, navigation consolidation, command palette safety smoke, status language report, onboarding report en local-only UX metrics.
- UAT feedback execution tracker, Streamlit fallback info, Streamlit deprecation readiness matrix en workflow evidence bundle.
- CLI commands voor alle Roadmap 107 surfaces.
- Check-all integratie voor UX backlog en Streamlit deprecation readiness.
- Frontend guided action components, start bot wizard, demo spot wizard, paper session workflow, command palette component en V2 route wiring.

Validatie:

- `python -m pytest tests/test_roadmap_107_dashboard_v2_workflow_ux_acceptance.py -q`: 4 passed.
- Roadmap 107 CLI-flow voor alle nieuwe commands: ok.
- `npm install` en `npm run build` in `dashboard-v2`: ok; `node_modules` daarna verwijderd.
- `python -m pytest tests/test_roadmaps_104_122_full_surface.py tests/test_roadmap_104_dashboard_v2_acceptance.py tests/test_roadmap_105_dashboard_v2_parity_acceptance.py tests/test_roadmap_106_dashboard_v2_cutover_acceptance.py tests/test_roadmap_107_dashboard_v2_workflow_ux_acceptance.py -q`: 27 passed.
- `python -m binance_spot_bot.cli check-all --skip-tests --json`: ok.
- `python -m pytest -q`: 406 passed, 1 bestaande PytestCollectionWarning.

Safety:

- Live trading blijft disabled.
- Streamlit blijft fallback; niet verwijderd.
- Geen signed/order/account/live endpoints toegevoegd.
- UX feedback, metrics en workflow evidence zijn local-only en redacted.
- No-live proof blijft verplicht in flows, reports en evidence.
