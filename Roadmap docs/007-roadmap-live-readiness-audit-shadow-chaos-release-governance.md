# Roadmap 007 - Live-Readiness Audit, Shadow Mode, Chaos Testing \& Release Governance

Status: Concept / Vervolgroadmap  
Project: Neural network Binance spot  
Datum: 2026-05-09  
Voorgestelde bestandsnaam:

```text
Roadmap docs/007-roadmap-live-readiness-audit-shadow-chaos-release-governance.md
```

Volgt op:

* `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
* `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
* `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
* `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
* `Roadmap docs/005-roadmap-long-paper-testnet-alerts-scanner-packaging.md`
* `006-roadmap-multi-symbol-portfolio-testnet-endurance-mlops.md`

Belangrijk: Roadmap 007 is **geen live-trading roadmap**. Deze roadmap is bedoeld om bewijs, safety, auditability, chaos testing, shadow mode en release governance op te bouwen zodat later objectief beslist kan worden of een aparte live-readiness roadmap überhaupt verantwoord is.

Live trading blijft volledig uitgeschakeld.

\---

## 0\. Waarom deze Roadmap 007

Na Roadmap 005 en Roadmap 006 heeft het project naar verwachting:

* \[ ] lange paper-session reports;
* \[ ] alert/watchdog events;
* \[ ] gated testnet orderflow;
* \[ ] durable order lifecycle;
* \[ ] realistischer paper accounting;
* \[ ] multi-symbol portfolio paper trading;
* \[ ] testnet endurance reports;
* \[ ] model promotion/rejection history;
* \[ ] external alerts;
* \[ ] live-readiness audit prep.

De logische volgende stap is dan niet meteen live trading. De logische volgende stap is:

* \[ ] bewijzen verzamelen;
* \[ ] failure modes testen;
* \[ ] shadow trading zonder orders draaien;
* \[ ] release/CI/security volwassen maken;
* \[ ] operator drills uitvoeren;
* \[ ] readiness objectief scoren;
* \[ ] alle resterende risico’s zichtbaar maken.

\---

## 1\. Belangrijkste conclusie

Ik zou als volgende roadmap doen:

```text
Roadmap 007 - Live-Readiness Audit, Shadow Mode, Chaos Testing \& Release Governance
```

Niet omdat live trading al klaar is, maar omdat dit de veiligste brug is tussen:

```text
paper/testnet/portfolio-validatie
```

en een eventuele latere:

```text
Roadmap 008 - Strict Live-Readiness Pilot Design
```

Roadmap 007 moet expliciet bewijzen of het project **nog niet klaar** is voor live. Dat is net zo waardevol als bewijzen dat sommige onderdelen wel klaar zijn.

\---

## 2\. Onderzoeksbasis binnen deze repo

### Gecontroleerde roadmap-lijn

* \[x] Roadmap 001: veilige Binance Spot bot basis, paper/testnet-first, NN alleen signaalgenerator.
* \[x] Roadmap 002: lokaal visueel dashboard.
* \[x] Roadmap 003: realtime market data, top-of-book, sessions, model registry, evaluation, data quality.
* \[x] Roadmap 004: Windows one-click control center, credentials, connectivity, settings, user-data parsers, lifecycle store.
* \[x] Roadmap 005: long paper/testnet sessions, alerts, scanner, modeltraining, reports, packaging.
* \[x] Roadmap 006: multi-symbol portfolio paper trading, testnet endurance, research maturity, MLOps, external alerts.

### Gecontroleerde codebase-richting

De huidige codebase heeft al belangrijke bouwstenen:

* \[x] `BotRuntime` met modes `demo`, `paper`, `testnet-readiness`.
* \[x] `DATA\_SOURCES` met `auto`, `demo`, `rest`, `websocket`.
* \[x] `SessionStore` met session summaries, snapshots en fills.
* \[x] `OrderLifecycleStore` met intent, unknown status en execution report updates.
* \[x] `BotSettings.validate\_live\_readiness()` blokkeert live als gates ontbreken.
* \[x] Dependency groups voor `research`, `dev`, `ui`, `realtime`, `mlops`.

Roadmap 007 moet deze componenten dus **auditen, stress-testen en governance toevoegen**, niet opnieuw bouwen.

\---

## 3\. Wat ik extra zou toevoegen bovenop Roadmap 005/006

### Extra featurepakket A - Shadow Trading Mode

Doel: live marktdata lezen en would-be orders/logica draaien, maar **geen echte orders sturen**.

* \[ ] `shadow` mode toevoegen als aparte runtime mode.
* \[ ] Live market data toegestaan.
* \[ ] Signed order endpoints verboden.
* \[ ] Bot genereert alleen `ShadowIntent`.
* \[ ] RiskEngine draait volledig.
* \[ ] ExecutionEngine wordt niet aangeroepen voor echte orderplaatsing.
* \[ ] Alle would-be trades worden opgeslagen.
* \[ ] Shadow performance wordt vergeleken met paper/testnet.

### Extra featurepakket B - Chaos Testing

Doel: bot bewust kapotmaken in veilige omgeving.

* \[ ] Simuleer Binance 429.
* \[ ] Simuleer Binance 418.
* \[ ] Simuleer 5xx.
* \[ ] Simuleer order timeout.
* \[ ] Simuleer WebSocket disconnect.
* \[ ] Simuleer stale candles.
* \[ ] Simuleer extreme spread.
* \[ ] Simuleer corrupted exchangeInfo filters.
* \[ ] Simuleer partial fills.
* \[ ] Simuleer duplicate execution reports.
* \[ ] Simuleer missing user-data event.
* \[ ] Simuleer system clock drift.
* \[ ] Simuleer full disk / write failure.

### Extra featurepakket C - Evidence Vault

Doel: alle proof-of-safety reports bundelen.

* \[ ] Paper reports.
* \[ ] Testnet reports.
* \[ ] Portfolio reports.
* \[ ] Model promotion history.
* \[ ] Drift reports.
* \[ ] Alerts.
* \[ ] Incidents.
* \[ ] Security scans.
* \[ ] Config snapshots.
* \[ ] Release hashes.
* \[ ] Dependency audit.
* \[ ] Operator drills.

### Extra featurepakket D - Release Governance

Doel: voorkomen dat een willekeurige codeversie testnet/live-readiness claims krijgt.

* \[ ] Versioned releases.
* \[ ] Changelog.
* \[ ] Release checklist.
* \[ ] Reproducible build.
* \[ ] Dependency lock.
* \[ ] SBOM optioneel.
* \[ ] Signed/hash-verified release zip.
* \[ ] Test evidence per release.
* \[ ] “Approved for demo/paper/testnet-readiness” badge.

### Extra featurepakket E - Operator Safety Drills

Doel: bewijzen dat de gebruiker gevaarlijke situaties kan stoppen.

* \[ ] Kill switch drill.
* \[ ] Emergency stop drill.
* \[ ] Network disconnect drill.
* \[ ] Testnet order cancel drill.
* \[ ] Secret rotation drill.
* \[ ] Incident bundle export drill.
* \[ ] Restart/resume drill.
* \[ ] Dashboard recovery drill.

\---

## 4\. Fase 0 - Roadmap 005/006 completion gate

Doel: Roadmap 007 pas echt starten wanneer genoeg bewijs bestaat uit 005 en 006.

### Taken

* \[ ] Controleer of Roadmap 005 is voltooid of gedeeltelijk bruikbaar.
* \[ ] Controleer of Roadmap 006 is voltooid of gedeeltelijk bruikbaar.
* \[ ] Verzamel minimaal:

  * \[ ] 10 demo/paper long-session reports;
  * \[ ] 3 portfolio paper-session reports;
  * \[ ] 1 testnet endurance report indien testnet credentials beschikbaar zijn;
  * \[ ] 1 incident drill report;
  * \[ ] 1 model promotion/rejection report;
  * \[ ] 1 security scan report;
  * \[ ] 1 package/preflight report.
* \[ ] Maak `docs/roadmap-005-006-results-summary.md`.
* \[ ] Label ontbrekende bewijsstukken als blockers.

### Acceptatiecriteria

* \[ ] Roadmap 007 start niet op aannames.
* \[ ] Ontbrekend bewijs wordt zichtbaar als blocker.
* \[ ] Live trading blijft disabled.
* \[ ] Geen roadmapfase claimt live-readiness zonder bewijs.

\---

## 5\. Fase 1 - Evidence Vault

Doel: één lokale bewijsmap waar alle readiness-data samenkomt.

### Nieuwe module

```text
src/binance\_spot\_bot/evidence.py
```

### Nieuwe mapstructuur

```text
data/evidence/
  releases/
  sessions/
  testnet/
  portfolio/
  models/
  alerts/
  incidents/
  security/
  chaos/
  drills/
  readiness/
```

### Taken

* \[ ] Voeg `EvidenceRecord` toe:

  * \[ ] record\_id;
  * \[ ] type;
  * \[ ] source file;
  * \[ ] hash;
  * \[ ] created\_at;
  * \[ ] status;
  * \[ ] summary;
  * \[ ] linked session/model/release.
* \[ ] Voeg `EvidenceVault` toe:

  * \[ ] add record;
  * \[ ] list records;
  * \[ ] verify hash;
  * \[ ] export bundle.
* \[ ] Voeg CLI toe:

```powershell
python -m binance\_spot\_bot.cli evidence-list
python -m binance\_spot\_bot.cli evidence-add --type paper-session --path data/sessions/<id>/summary.json
python -m binance\_spot\_bot.cli evidence-export --output data/evidence/readiness-bundle.zip
```

* \[ ] Dashboard Evidence tab:

  * \[ ] proof list;
  * \[ ] missing proof;
  * \[ ] readiness blockers;
  * \[ ] export button.

### Acceptatiecriteria

* \[ ] Elk belangrijk report kan als evidence record worden geregistreerd.
* \[ ] Hash-verificatie detecteert gewijzigde bestanden.
* \[ ] Evidence bundle bevat geen secrets.
* \[ ] Readiness kan niet “groen” worden zonder bewijs.

\---

## 6\. Fase 2 - Shadow Trading Mode

Doel: live market data en volledige decision chain testen zonder echte orders.

### Nieuwe runtime mode

```text
shadow
```

### Regels

* \[ ] Mag live public market data lezen.
* \[ ] Mag geen signed order endpoints aanroepen.
* \[ ] Mag geen echte orders plaatsen.
* \[ ] Mag geen testnet orders plaatsen.
* \[ ] Genereert alleen `ShadowIntent`.
* \[ ] Alle intents krijgen:

  * \[ ] timestamp;
  * \[ ] symbol;
  * \[ ] model signal;
  * \[ ] risk decision;
  * \[ ] would-be order;
  * \[ ] block reason;
  * \[ ] estimated fill;
  * \[ ] estimated fees/slippage;
  * \[ ] model version;
  * \[ ] config hash.

### Nieuwe modules

```text
src/binance\_spot\_bot/shadow.py
src/binance\_spot\_bot/shadow\_ledger.py
```

### CLI

```powershell
python -m binance\_spot\_bot.cli shadow-session --symbols BTCUSDT,ETHUSDT --duration-minutes 120 --source websocket
```

### Dashboard

* \[ ] Shadow tab.
* \[ ] Would-be trades table.
* \[ ] Would-be equity curve.
* \[ ] Difference vs paper/testnet.
* \[ ] Block reason analysis.
* \[ ] “NO ORDERS SENT” badge.

### Acceptatiecriteria

* \[ ] Shadow mode kan niet naar live/testnet execution.
* \[ ] Alle would-be orders zijn auditbaar.
* \[ ] Shadow mode gebruikt dezelfde SignalModel/RiskEngine.
* \[ ] Geen codepad kan signed order endpoints triggeren.
* \[ ] Tests bewijzen dat adapter `place\_order()` nooit wordt aangeroepen.

\---

## 7\. Fase 3 - Chaos Testing Harness

Doel: failure modes automatisch testen.

### Nieuwe module

```text
src/binance\_spot\_bot/chaos.py
```

### Failure scenarios

* \[ ] REST 429 rate limit.
* \[ ] REST 418 ban response.
* \[ ] REST 500.
* \[ ] REST timeout.
* \[ ] Signed order timeout.
* \[ ] Unknown order status.
* \[ ] WebSocket disconnect.
* \[ ] WebSocket duplicate event.
* \[ ] WebSocket stale event.
* \[ ] Missing kline close event.
* \[ ] Corrupt candle data.
* \[ ] Extreme spread.
* \[ ] ExchangeInfo missing filters.
* \[ ] Clock drift.
* \[ ] Data directory not writable.
* \[ ] Audit log write failure.
* \[ ] Session store write failure.
* \[ ] Model artifact missing.
* \[ ] Secret scan finding.
* \[ ] Alert sink failure.

### CLI

```powershell
python -m binance\_spot\_bot.cli chaos-run --scenario websocket-disconnect
python -m binance\_spot\_bot.cli chaos-suite --safe
```

### Acceptatiecriteria

* \[ ] Chaos tests draaien zonder echte Binance calls.
* \[ ] Critical failures stoppen runtime of blokkeren execution.
* \[ ] Unknown order status leidt tot reconciliation.
* \[ ] Write failure geeft alert en stopt veilig.
* \[ ] Chaos report wordt evidence record.

\---

## 8\. Fase 4 - Operational Safety Drills

Doel: bewijzen dat operator en systeem veilig reageren.

### Drills

* \[ ] Kill switch drill.
* \[ ] Emergency stop drill.
* \[ ] Testnet cancel drill.
* \[ ] Secret rotation drill.
* \[ ] Reconnect drill.
* \[ ] Resume-after-crash drill.
* \[ ] Evidence export drill.
* \[ ] Incident bundle drill.
* \[ ] Alert delivery drill.
* \[ ] Model rollback drill.

### Nieuwe module

```text
src/binance\_spot\_bot/drills.py
```

### CLI

```powershell
python -m binance\_spot\_bot.cli drill-run --name kill-switch
python -m binance\_spot\_bot.cli drill-suite
```

### Acceptatiecriteria

* \[ ] Elke drill heeft pass/fail.
* \[ ] Elke drill schrijft report.
* \[ ] Drill report gaat naar Evidence Vault.
* \[ ] Failing drill blokkeert readiness score.
* \[ ] Geen drill gebruikt live orders.

\---

## 9\. Fase 5 - Readiness Scorecard

Doel: objectief meten hoe ver het project is.

### Nieuwe module

```text
src/binance\_spot\_bot/readiness.py
```

### Readiness levels

```text
R0 - Development only
R1 - Demo stable
R2 - Paper stable
R3 - Testnet technical stable
R4 - Portfolio/testnet endurance stable
R5 - Live-readiness audit candidate
```

### Score categories

* \[ ] Safety.
* \[ ] Security.
* \[ ] Data quality.
* \[ ] Model quality.
* \[ ] Risk controls.
* \[ ] Execution/reconciliation.
* \[ ] Observability.
* \[ ] Operator controls.
* \[ ] Incident response.
* \[ ] Release quality.
* \[ ] Documentation.
* \[ ] Evidence completeness.

### CLI

```powershell
python -m binance\_spot\_bot.cli readiness-score
python -m binance\_spot\_bot.cli readiness-report --output data/evidence/readiness/readiness.md
```

### Acceptatiecriteria

* \[ ] Score is evidence-based.
* \[ ] Missing evidence lowers score.
* \[ ] Critical blocker prevents R5.
* \[ ] Readiness report zegt expliciet dat live nog niet geactiveerd wordt.
* \[ ] Dashboard toont readiness level en blockers.

\---

## 10\. Fase 6 - Release Governance

Doel: alleen gecontroleerde versies krijgen readiness/evidence status.

### Taken

* \[ ] Voeg release metadata toe:

  * \[ ] version;
  * \[ ] git commit;
  * \[ ] build time;
  * \[ ] dependency snapshot;
  * \[ ] test results;
  * \[ ] security results;
  * \[ ] evidence bundle hash.
* \[ ] Voeg `RELEASE\_NOTES.md` flow toe.
* \[ ] Voeg `CHANGELOG.md` toe.
* \[ ] Voeg `scripts/build-release.ps1` toe.
* \[ ] Voeg `scripts/verify-release.ps1` toe.
* \[ ] Voeg release zip hash toe.
* \[ ] Voeg optional SBOM toe.
* \[ ] Voeg dependency vulnerability report toe.
* \[ ] Voeg “approved modes” toe:

  * \[ ] demo-approved;
  * \[ ] paper-approved;
  * \[ ] testnet-readiness-approved;
  * \[ ] shadow-approved;
  * \[ ] not-live-approved.

### Acceptatiecriteria

* \[ ] Release kan gereproduceerd worden.
* \[ ] Release bevat geen secrets.
* \[ ] Release is gekoppeld aan evidence.
* \[ ] Dashboard toont build/release version.
* \[ ] Live-approved status bestaat niet in Roadmap 007.

\---

## 11\. Fase 7 - Security Audit Pack

Doel: security bewijs verzamelen voor toekomstige audit.

### Taken

* \[ ] Voeg dependency audit toe:

  * \[ ] `pip-audit` optioneel;
  * \[ ] fallback report als tool ontbreekt.
* \[ ] Voeg secret audit toe:

  * \[ ] repo;
  * \[ ] docs;
  * \[ ] reports;
  * \[ ] data/settings;
  * \[ ] data/sessions;
  * \[ ] evidence bundles.
* \[ ] Voeg credential permission checklist toe:

  * \[ ] withdrawal disabled;
  * \[ ] IP restrictions;
  * \[ ] testnet/demo only;
  * \[ ] key rotation date;
  * \[ ] least privilege.
* \[ ] Voeg local machine hardening checklist toe:

  * \[ ] Windows user permissions;
  * \[ ] folder permissions;
  * \[ ] antivirus exclusions niet vereist;
  * \[ ] secrets niet in screenshots.
* \[ ] Voeg `docs/security-audit-pack.md`.

### Acceptatiecriteria

* \[ ] Security audit report is downloadbaar.
* \[ ] Geen secrets in reports.
* \[ ] Security blocker verlaagt readiness score.
* \[ ] Dependency findings worden zichtbaar.

\---

## 12\. Fase 8 - Model Risk Governance

Doel: modellen behandelen als risicobron, niet als magie.

### Taken

* \[ ] Voeg `ModelCard` toe per model:

  * \[ ] purpose;
  * \[ ] training data;
  * \[ ] validation data;
  * \[ ] known limitations;
  * \[ ] allowed modes;
  * \[ ] metrics;
  * \[ ] drift status;
  * \[ ] promotion history;
  * \[ ] rejection reasons.
* \[ ] Voeg model rollback command toe:

```powershell
python -m binance\_spot\_bot.cli model-rollback --alias champion --to <model\_id>
```

* \[ ] Voeg model freeze toe:

  * \[ ] no new model promotion during incidents;
  * \[ ] no promotion without evidence.
* \[ ] Voeg drift response:

  * \[ ] warn;
  * \[ ] block model;
  * \[ ] fallback baseline.
* \[ ] Voeg dashboard Model Risk tab toe.

### Acceptatiecriteria

* \[ ] Elk actief model heeft model card.
* \[ ] Model kan worden teruggerold.
* \[ ] Drift kan model blokkeren.
* \[ ] Model card wordt toegevoegd aan evidence bundle.
* \[ ] Geen model mag direct live-ready claimen.

\---

## 13\. Fase 9 - Observability \& SLOs

Doel: meten of de bot operationeel stabiel is.

### SLO voorbeelden

* \[ ] Market data freshness.
* \[ ] WebSocket reconnect rate.
* \[ ] REST error rate.
* \[ ] Reconciliation success rate.
* \[ ] Unknown order duration.
* \[ ] Alert response time.
* \[ ] Session report completion.
* \[ ] Audit write success.
* \[ ] Dashboard availability.
* \[ ] Data-quality healthy ratio.

### Taken

* \[ ] Voeg `SLOReport` toe.
* \[ ] Voeg metrics history toe.
* \[ ] Voeg dashboard SLO tab toe.
* \[ ] Voeg CLI toe:

```powershell
python -m binance\_spot\_bot.cli slo-report --days 7
```

### Acceptatiecriteria

* \[ ] SLO report gebruikt echte session/testnet/shadow data.
* \[ ] SLO violations worden alerts.
* \[ ] SLO evidence beïnvloedt readiness score.
* \[ ] Dashboard toont trend, niet alleen laatste status.

\---

## 14\. Fase 10 - Shadow vs Paper vs Testnet Comparison

Doel: verschillen tussen simulatie en testnet zichtbaar maken.

### Taken

* \[ ] Vergelijk:

  * \[ ] shadow intents;
  * \[ ] paper fills;
  * \[ ] testnet fills;
  * \[ ] slippage assumptions;
  * \[ ] spread at decision time;
  * \[ ] rejected/blocked reasons.
* \[ ] Maak comparison report:

  * \[ ] expected vs observed;
  * \[ ] missed fills;
  * \[ ] order latency;
  * \[ ] model signal consistency;
  * \[ ] risk decision consistency.
* \[ ] Dashboard comparison tab.

### Acceptatiecriteria

* \[ ] Verschillen tussen paper en testnet worden meetbaar.
* \[ ] Paper assumptions kunnen worden aangepast op testnet-observaties.
* \[ ] Grote mismatch blokkeert readiness.
* \[ ] Report wordt evidence record.

\---

## 15\. Fase 11 - Documentation \& Runbooks

### Nieuwe docs

* \[ ] `docs/evidence-vault.md`
* \[ ] `docs/shadow-mode.md`
* \[ ] `docs/chaos-testing.md`
* \[ ] `docs/operator-drills.md`
* \[ ] `docs/readiness-scorecard.md`
* \[ ] `docs/release-governance.md`
* \[ ] `docs/security-audit-pack.md`
* \[ ] `docs/model-risk-governance.md`
* \[ ] `docs/observability-slo.md`
* \[ ] `docs/shadow-paper-testnet-comparison.md`

### Runbooks

* \[ ] `docs/runbooks/kill-switch.md`
* \[ ] `docs/runbooks/testnet-cancel.md`
* \[ ] `docs/runbooks/secret-rotation.md`
* \[ ] `docs/runbooks/model-rollback.md`
* \[ ] `docs/runbooks/release-verify.md`
* \[ ] `docs/runbooks/incident-export.md`

### Acceptatiecriteria

* \[ ] Alle runbooks zijn uitvoerbaar op Windows PowerShell.
* \[ ] Runbooks bevatten geen live trading instructie.
* \[ ] Runbooks verwijzen naar CLI commands.
* \[ ] Docs worden opgenomen in release package.

\---

## 16\. Testplan Roadmap 007

### Unit tests

* \[ ] `tests/test\_evidence\_vault.py`
* \[ ] `tests/test\_shadow\_mode.py`
* \[ ] `tests/test\_shadow\_ledger.py`
* \[ ] `tests/test\_chaos.py`
* \[ ] `tests/test\_drills.py`
* \[ ] `tests/test\_readiness.py`
* \[ ] `tests/test\_release\_governance.py`
* \[ ] `tests/test\_security\_audit\_pack.py`
* \[ ] `tests/test\_model\_card.py`
* \[ ] `tests/test\_slo\_report.py`
* \[ ] `tests/test\_shadow\_paper\_testnet\_comparison.py`

### Integration tests

* \[ ] Shadow session without orders.
* \[ ] Chaos suite safe.
* \[ ] Drill suite safe.
* \[ ] Evidence export bundle.
* \[ ] Readiness score blocks missing evidence.
* \[ ] Release build verify.
* \[ ] Secret scan evidence bundle.
* \[ ] Model rollback.
* \[ ] SLO report from sample sessions.

### Safety tests

* \[ ] Shadow mode cannot call `place\_order`.
* \[ ] Readiness score cannot mark live-ready.
* \[ ] Release cannot include secrets.
* \[ ] Live mode remains blocked.
* \[ ] UI still excludes live.
* \[ ] Signed order endpoints are mocked/blocked in tests.

\---

## 17\. Nieuwe bestanden

### Source

* \[ ] `src/binance\_spot\_bot/evidence.py`
* \[ ] `src/binance\_spot\_bot/shadow.py`
* \[ ] `src/binance\_spot\_bot/shadow\_ledger.py`
* \[ ] `src/binance\_spot\_bot/chaos.py`
* \[ ] `src/binance\_spot\_bot/drills.py`
* \[ ] `src/binance\_spot\_bot/readiness.py`
* \[ ] `src/binance\_spot\_bot/release\_governance.py`
* \[ ] `src/binance\_spot\_bot/security\_audit.py`
* \[ ] `src/binance\_spot\_bot/model\_card.py`
* \[ ] `src/binance\_spot\_bot/slo.py`
* \[ ] `src/binance\_spot\_bot/comparison.py`

### Scripts

* \[ ] `scripts/build-release.ps1`
* \[ ] `scripts/verify-release.ps1`
* \[ ] `scripts/run-chaos-suite.ps1`
* \[ ] `scripts/run-drill-suite.ps1`

### Docs

* \[ ] `docs/evidence-vault.md`
* \[ ] `docs/shadow-mode.md`
* \[ ] `docs/chaos-testing.md`
* \[ ] `docs/operator-drills.md`
* \[ ] `docs/readiness-scorecard.md`
* \[ ] `docs/release-governance.md`
* \[ ] `docs/security-audit-pack.md`
* \[ ] `docs/model-risk-governance.md`
* \[ ] `docs/observability-slo.md`
* \[ ] `docs/shadow-paper-testnet-comparison.md`

\---

## 18\. Prioriteiten

### Eerst

1. \[ ] Evidence Vault.
2. \[ ] Shadow Trading Mode.
3. \[ ] Chaos Testing Harness.
4. \[ ] Operator Drills.
5. \[ ] Readiness Scorecard.

### Daarna

6. \[ ] Release Governance.
7. \[ ] Security Audit Pack.
8. \[ ] Model Risk Governance.
9. \[ ] Observability \& SLOs.
10. \[ ] Shadow/Paper/Testnet comparison.

### Als laatste

11. \[ ] Documentation and runbooks.
12. \[ ] Evidence export and release packaging.
13. \[ ] Readiness report.

\---

## 19\. Definition of Done

Roadmap 007 is klaar als:

* \[ ] Evidence Vault werkt.
* \[ ] Shadow mode draait zonder orders.
* \[ ] Chaos suite test failure modes veilig.
* \[ ] Operator drills hebben pass/fail reports.
* \[ ] Readiness score is evidence-based.
* \[ ] Release governance koppelt build aan evidence.
* \[ ] Security audit pack is downloadbaar.
* \[ ] Model cards en rollback werken.
* \[ ] SLO reports werken.
* \[ ] Shadow/paper/testnet comparison werkt.
* \[ ] Alle reports bevatten geen secrets.
* \[ ] Live trading blijft disabled.
* \[ ] Alle tests en security scans slagen.
* \[ ] Docs en runbooks zijn bijgewerkt.
* \[ ] Roadmap 007 kan na uitvoering naar `Voltooid docs`.

\---

## 20\. Verwachte Roadmap 008 daarna

Alleen na Roadmap 007 en alleen als readiness score voldoende bewijs heeft:

```text
Roadmap 008 - Strict Live-Readiness Pilot Design
```

Roadmap 008 zou nog steeds niet automatisch live trading activeren. Die roadmap zou alleen ontwerpen:

* \[ ] mini live pilot policy;
* \[ ] handmatige approval;
* \[ ] tiny exposure limits;
* \[ ] withdrawal-disabled verification;
* \[ ] IP allowlist;
* \[ ] kill switch drill;
* \[ ] manual stop procedure;
* \[ ] legal/financial risk notice;
* \[ ] rollback plan.

Geen live default. Geen autonome live trading.

