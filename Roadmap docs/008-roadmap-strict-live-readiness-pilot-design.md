# Roadmap 008 - Strict Live-Readiness Pilot Design

Status: Concept / Alleen ontwerp, geen live activatie  
Project: Neural network Binance spot  
Datum: 2026-05-09  
Voorgestelde bestandsnaam:

```text
Roadmap docs/008-roadmap-strict-live-readiness-pilot-design.md
```

Volgt op:

* `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
* `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
* `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
* `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
* `Roadmap docs/005-roadmap-long-paper-testnet-alerts-scanner-packaging.md`
* `006-roadmap-multi-symbol-portfolio-testnet-endurance-mlops.md`
* `007-roadmap-live-readiness-audit-shadow-chaos-release-governance.md`

Belangrijk: Roadmap 008 mag **geen live trading activeren**. Deze roadmap ontwerpt alleen een extreem strenge live-readiness pilot voor een latere aparte implementatiebeslissing. Als bewijs ontbreekt, blijft alles paper/testnet/shadow.

\---

## 0\. Waarom Roadmap 008

Roadmap 005 focust op lange paper/testnet sessies, alerts, scanner, modeltraining, reports en Windows packaging. Roadmap 006 focust op multi-symbol portfolio paper trading en testnet endurance. Roadmap 007 focust op evidence vault, shadow mode, chaos testing, drills, readiness score en release governance.

Daarna is de volgende logische stap niet “live aanzetten”, maar:

* \[ ] ontwerp van een strict live-readiness pilot;
* \[ ] exact bepalen welke bewijsstukken verplicht zijn;
* \[ ] exposure en risico extreem laag houden;
* \[ ] manual approvals verplicht maken;
* \[ ] automatische stop/rollback verplicht maken;
* \[ ] live codepad nog steeds standaard uit houden;
* \[ ] pilot pas toestaan als alle scorecards groen zijn.

\---

## 1\. Kernbeslissing

Ik zou nu Roadmap 008 doen als:

```text
Strict Live-Readiness Pilot Design
```

Doel:

* \[ ] Een toekomstige live-pilot ontwerpen zonder live trading nu te activeren.
* \[ ] Alle harde voorwaarden vastleggen.
* \[ ] Alle stopcondities vastleggen.
* \[ ] Alle bewijseisen vastleggen.
* \[ ] Alle operatorstappen vastleggen.
* \[ ] Alle juridische/financiële waarschuwingen zichtbaar maken.
* \[ ] Technische implementatie nog achter aparte latere roadmap houden.

\---

## 2\. Niet opnieuw bouwen

Niet opnieuw bouwen:

* \[ ] Geen nieuwe RiskEngine.
* \[ ] Geen nieuwe ExecutionEngine.
* \[ ] Geen tweede dashboard.
* \[ ] Geen tweede Binance adapter.
* \[ ] Geen nieuwe ModelRegistry.
* \[ ] Geen live auto-trader.
* \[ ] Geen LLM orderbeslisser.
* \[ ] Geen futures/margin/leverage.
* \[ ] Geen withdrawals.

Wel hergebruiken:

* \[ ] `BotSettings.validate\_live\_readiness()`
* \[ ] `RiskEngine`
* \[ ] `ExecutionEngine`
* \[ ] `OrderLifecycleStore`
* \[ ] `SessionStore`
* \[ ] `EvidenceVault`
* \[ ] `ReadinessScorecard`
* \[ ] `AlertManager`
* \[ ] `WatchdogPolicy`
* \[ ] `ShadowLedger`
* \[ ] `ModelRegistry`
* \[ ] `Dashboard Control Center`

\---

## 3\. Strikte startvoorwaarde

Roadmap 008 mag alleen definitief gemaakt worden als deze outputs bestaan:

* \[ ] Roadmap 005 long paper reports.
* \[ ] Roadmap 005 alert/watchdog reports.
* \[ ] Roadmap 005 gated testnet reports.
* \[ ] Roadmap 006 portfolio paper reports.
* \[ ] Roadmap 006 testnet endurance reports.
* \[ ] Roadmap 006 model comparison reports.
* \[ ] Roadmap 007 evidence vault.
* \[ ] Roadmap 007 chaos suite reports.
* \[ ] Roadmap 007 operator drill reports.
* \[ ] Roadmap 007 readiness scorecard.
* \[ ] Roadmap 007 release governance report.
* \[ ] Roadmap 007 security audit pack.
* \[ ] Roadmap 007 shadow vs paper vs testnet comparison.

Als één kritisch bewijsstuk ontbreekt:

* \[ ] geen live pilot;
* \[ ] alleen paper/testnet/shadow verder verbeteren.

\---

## 4\. Fase 0 - Live-readiness evidence gate

Doel: objectief bepalen of een live-pilot ontwerp überhaupt verder mag.

### Taken

* \[ ] Verzamel alle evidence uit Roadmap 005, 006 en 007.
* \[ ] Controleer hashes van alle evidence records.
* \[ ] Controleer of session reports secrets bevatten.
* \[ ] Controleer of testnet endurance succesvol was.
* \[ ] Controleer of unknown order reconciliation betrouwbaar is.
* \[ ] Controleer of alerts buiten dashboard aankomen.
* \[ ] Controleer of operator drills geslaagd zijn.
* \[ ] Controleer of model promotion/rejection traceerbaar is.
* \[ ] Controleer of release governance groen is.
* \[ ] Maak `docs/live-pilot-evidence-gate.md`.

### Acceptatiecriteria

* \[ ] Evidence gate kan rood/geel/groen zijn.
* \[ ] Rood blokkeert live pilot volledig.
* \[ ] Geel vereist meer paper/testnet bewijs.
* \[ ] Groen betekent alleen: pilotontwerp mag verder.
* \[ ] Groen betekent niet: live trading mag aan.

\---

## 5\. Fase 1 - Live Pilot Policy ontwerp

Doel: exact specificeren onder welke voorwaarden een minimale live pilot later ooit mag starten.

### Nieuwe doc

```text
docs/live-pilot-policy.md
```

### Policy velden

* \[ ] Allowed symbols.
* \[ ] Allowed quote assets.
* \[ ] Max order quote.
* \[ ] Max total daily quote exposure.
* \[ ] Max total portfolio exposure.
* \[ ] Max daily realized loss.
* \[ ] Max daily unrealized drawdown.
* \[ ] Max trades per day.
* \[ ] Max open positions.
* \[ ] Max spread bps.
* \[ ] Max data age.
* \[ ] Min model status.
* \[ ] Required release approval.
* \[ ] Required evidence score.
* \[ ] Required operator presence.
* \[ ] Required emergency stop availability.

### Mijn voorgestelde pilotlimieten

Start extreem klein:

* \[ ] 1 symbol.
* \[ ] 1 quote asset.
* \[ ] 1 model: champion only.
* \[ ] Max 1 open position.
* \[ ] Max 1-3 trades per dag.
* \[ ] Max order quote zeer laag.
* \[ ] Geen unattended live.
* \[ ] Geen overnight live.
* \[ ] Geen compounding.
* \[ ] Geen auto-resume na crash.
* \[ ] Geen live als dashboard niet bereikbaar is.
* \[ ] Geen live als alerts niet werken.

### Acceptatiecriteria

* \[ ] Policy is machine-readable en human-readable.
* \[ ] Policy heeft geen default permissive values.
* \[ ] Elke ontbrekende waarde blokkeert pilot.
* \[ ] Policy wordt opgenomen in Evidence Vault.

\---

## 6\. Fase 2 - Account \& Exchange Safety Checklist

Doel: voorkomen dat keys of accountrechten onveilig zijn.

### Checklist

* \[ ] API key is nieuw aangemaakt voor pilot.
* \[ ] Withdrawals zijn disabled.
* \[ ] IP allowlist is ingesteld indien mogelijk.
* \[ ] Alleen spot trading permissie indien nodig.
* \[ ] Geen margin/futures permissies.
* \[ ] Geen universal transfer permissies.
* \[ ] Geen master account key.
* \[ ] Key fingerprint is opgeslagen.
* \[ ] Key rotation procedure bestaat.
* \[ ] Secret is niet in `.env`, logs, docs, reports of screenshots zichtbaar.
* \[ ] Emergency key revoke procedure bestaat.

### Nieuwe doc

```text
docs/live-account-safety-checklist.md
```

### Acceptatiecriteria

* \[ ] Checklist vereist handmatige afvink.
* \[ ] Checklist wordt evidence record.
* \[ ] Missing/unsafe permission blokkeert pilot.
* \[ ] Bot kan geen withdrawal-gerelateerde endpoints gebruiken.

\---

## 7\. Fase 3 - Manual Approval Flow ontwerp

Doel: geen live pilot zonder bewuste menselijke actie.

### Vereiste approvals

* \[ ] Exacte approval phrase.
* \[ ] Release hash bevestiging.
* \[ ] Evidence bundle hash bevestiging.
* \[ ] Policy hash bevestiging.
* \[ ] Symbol bevestiging.
* \[ ] Max exposure bevestiging.
* \[ ] Emergency stop test bevestiging.
* \[ ] Operator aanwezig bevestiging.

### Voorbeeld phrases

```text
I\_ACCEPT\_STRICT\_SPOT\_LIVE\_PILOT\_RISK
I\_CONFIRM\_NO\_WITHDRAWAL\_KEYS
I\_CONFIRM\_MAX\_EXPOSURE\_LIMITS
I\_CONFIRM\_EMERGENCY\_STOP\_TESTED
```

### Acceptatiecriteria

* \[ ] Geen enkele approval mag standaard ingevuld zijn.
* \[ ] Dashboard moet risky dialog gebruiken.
* \[ ] CLI vereist `--confirm` met exacte phrase.
* \[ ] Approval verloopt na korte tijd.
* \[ ] Approval is gekoppeld aan release hash en policy hash.

\---

## 8\. Fase 4 - Live Dry-Run Mode

Doel: exact live codepad voorbereiden, maar zonder order submit.

### Nieuwe mode

```text
live-dry-run
```

### Regels

* \[ ] Mag live public market data lezen.
* \[ ] Mag account read-only check uitvoeren.
* \[ ] Mag exchange filters lezen.
* \[ ] Mag model/risk/execution order request bouwen.
* \[ ] Mag geen `/api/v3/order` POST doen.
* \[ ] Mag geen order submitten.
* \[ ] Mag alleen `DryRunOrderIntent` opslaan.

### Verschil met shadow mode

* Shadow mode gebruikt would-be trades voor observatie.
* Live dry-run valideert exact live readiness policy en order-build pipeline zonder submit.

### Acceptatiecriteria

* \[ ] Tests bewijzen dat `place\_order()` niet wordt aangeroepen.
* \[ ] Dry-run report lijkt op live report, maar met `submitted=false`.
* \[ ] Dry-run kan readiness blockers tonen.
* \[ ] Dry-run draait alleen als policy/evidence aanwezig is.

\---

## 9\. Fase 5 - Two-Person Rule ontwerp

Doel: live pilot niet door één impulsieve klik laten starten.

### Taken

* \[ ] Ontwerp optionele two-person approval.
* \[ ] Approver 1: operator.
* \[ ] Approver 2: reviewer.
* \[ ] Beide approvals krijgen timestamp.
* \[ ] Beide approvals krijgen local signature/hash.
* \[ ] Approval verloopt automatisch.
* \[ ] Geen secrets in approval file.

### Acceptatiecriteria

* \[ ] Two-person rule is optioneel maar aanbevolen.
* \[ ] Als enabled, kan pilot niet starten met één approval.
* \[ ] Approval evidence wordt opgeslagen.
* \[ ] Dashboard toont approval status.

\---

## 10\. Fase 6 - Micro Pilot Execution Design

Doel: ontwerp van de kleinste mogelijke live pilot, nog niet implementeren als actieve live execution.

### Micro-pilot regels

* \[ ] Eén symbol.
* \[ ] Eén tiny order size.
* \[ ] Eén order tegelijk.
* \[ ] Geen market order tenzij policy dit expliciet toestaat.
* \[ ] Prefer limit/post-only indien Binance Spot API en strategy dit veilig ondersteunen.
* \[ ] Geen averaging down.
* \[ ] Geen pyramiding.
* \[ ] Geen auto-reentry na stop.
* \[ ] Geen trading tijdens degraded market data.
* \[ ] Geen trading tijdens high spread.
* \[ ] Geen trading na alert severity error/critical.
* \[ ] Geen trading als dashboard/alerts onbereikbaar zijn.
* \[ ] Geen trading als session report write faalt.

### Exit policy

* \[ ] Take-profit/stop rules alleen als vooraf policy-defined.
* \[ ] Manual close procedure.
* \[ ] Emergency cancel procedure.
* \[ ] Max holding time.
* \[ ] Forced exit alleen als safe and policy-defined.
* \[ ] If reconciliation unknown: no new orders.

### Acceptatiecriteria

* \[ ] Pilot is beperkt genoeg om technisch gedrag te testen, niet winst te maximaliseren.
* \[ ] Pilot heeft harde stopvoorwaarden.
* \[ ] Pilot heeft geen compounding.
* \[ ] Pilot heeft geen autonomous scaling.

\---

## 11\. Fase 7 - Hard Stop \& Rollback Design

Doel: live pilot veilig kunnen stoppen.

### Stop triggers

* \[ ] Manual emergency stop.
* \[ ] Kill switch.
* \[ ] Max daily loss hit.
* \[ ] Max drawdown hit.
* \[ ] Unknown order status.
* \[ ] Reconciliation failure.
* \[ ] WebSocket disconnected.
* \[ ] REST circuit breaker open.
* \[ ] Alert sink failure.
* \[ ] Session report write failure.
* \[ ] Evidence write failure.
* \[ ] Model drift critical.
* \[ ] Release hash mismatch.
* \[ ] Policy hash mismatch.
* \[ ] Operator heartbeat missing.

### Rollback actions

* \[ ] Disable live pilot flag.
* \[ ] Cancel open orders if safe.
* \[ ] Stop new intents.
* \[ ] Export incident bundle.
* \[ ] Mark release blocked.
* \[ ] Require new evidence gate before retry.

### Acceptatiecriteria

* \[ ] Stop design is documented.
* \[ ] Every stop trigger has action.
* \[ ] Incident bundle is mandatory.
* \[ ] New pilot cannot restart without fresh approval.

\---

## 12\. Fase 8 - Operator Heartbeat

Doel: live pilot alleen onder actieve observatie.

### Taken

* \[ ] Ontwerp operator heartbeat:

  * \[ ] dashboard button;
  * \[ ] CLI input;
  * \[ ] periodic confirmation.
* \[ ] Missing heartbeat:

  * \[ ] pause new orders;
  * \[ ] optional cancel open orders;
  * \[ ] alert critical.
* \[ ] Heartbeat interval policy.
* \[ ] Heartbeat logged in audit.

### Acceptatiecriteria

* \[ ] Geen unattended live pilot.
* \[ ] Missing heartbeat blocks new orders.
* \[ ] Heartbeat evidence wordt opgeslagen.
* \[ ] Tests kunnen heartbeat timeout simuleren.

\---

## 13\. Fase 9 - Financial \& Legal Risk Notice

Doel: gebruiker expliciet laten zien dat trading risico heeft.

### Taken

* \[ ] Voeg risk notice doc toe:

```text
docs/live-pilot-risk-notice.md
```

* \[ ] Dashboard dialog toont:

  * \[ ] je kunt geld verliezen;
  * \[ ] paper/testnet garandeert niets;
  * \[ ] slippage/liquidity kan verschillen;
  * \[ ] API/network failures kunnen optreden;
  * \[ ] model kan fout zijn;
  * \[ ] eigen verantwoordelijkheid.
* \[ ] CLI toont risk notice bij pilot design commands.
* \[ ] Approval vereist risk notice hash.

### Acceptatiecriteria

* \[ ] Risk notice is zichtbaar.
* \[ ] Risk notice wordt niet verstopt.
* \[ ] Pilot approval vereist bevestiging.
* \[ ] Geen winstclaims.

\---

## 14\. Fase 10 - Live Pilot Simulation Report

Doel: vóór echte implementatie simuleren hoe pilot zou verlopen.

### Taken

* \[ ] Gebruik historical paper/testnet/shadow data.
* \[ ] Replay micro-pilot policy.
* \[ ] Meet:

  * \[ ] would-be trades;
  * \[ ] expected fees;
  * \[ ] expected drawdown;
  * \[ ] stop trigger frequency;
  * \[ ] alert frequency;
  * \[ ] blocked trade rate;
  * \[ ] operator heartbeat requirements.
* \[ ] Maak `live-pilot-simulation.md`.

### Acceptatiecriteria

* \[ ] Simulation report is verplicht.
* \[ ] Als stop triggers te vaak voorkomen, pilot blijft blocked.
* \[ ] Als model underperforms, pilot blijft blocked.
* \[ ] Simulation is evidence record.

\---

## 15\. Fase 11 - Pilot Dashboard Design

Doel: dashboard ontwerpen voor live-pilot observatie, zonder activatie.

### UI elementen

* \[ ] Big red `LIVE PILOT NOT ACTIVE` badge.
* \[ ] Policy summary.
* \[ ] Evidence status.
* \[ ] Readiness score.
* \[ ] Approval status.
* \[ ] Operator heartbeat.
* \[ ] Emergency stop.
* \[ ] Open orders.
* \[ ] Reconciliation status.
* \[ ] Alerts.
* \[ ] Exposure.
* \[ ] PnL.
* \[ ] Session report writer status.

### Acceptatiecriteria

* \[ ] Dashboard kan pilot status tonen zonder live execution.
* \[ ] Geen verborgen live toggle.
* \[ ] Risky actions zitten achter dialogs.
* \[ ] UI maakt duidelijk wat blocked is.

\---

## 16\. Fase 12 - No-Go Criteria

Doel: expliciet maken wanneer live pilot niet mag.

### No-go voorbeelden

* \[ ] Minder dan vereiste paper sessions.
* \[ ] Minder dan vereiste testnet endurance.
* \[ ] Unknown order unresolved.
* \[ ] Reconciliation success onder threshold.
* \[ ] Critical alert in laatste N sessies.
* \[ ] Security scan finding.
* \[ ] Secret exposure finding.
* \[ ] Model drift critical.
* \[ ] Model status niet champion/paper-approved.
* \[ ] Release niet verified.
* \[ ] Evidence hash mismatch.
* \[ ] Operator drill failed.
* \[ ] Emergency stop failed.
* \[ ] Testnet cancel failed.
* \[ ] Missing account safety checklist.
* \[ ] Missing risk notice approval.

### Acceptatiecriteria

* \[ ] No-go criteria zijn machine-readable.
* \[ ] Dashboard toont exact waarom pilot blocked is.
* \[ ] CLI geeft non-zero exit bij no-go.
* \[ ] No-go kan niet genegeerd worden door standaard config.

\---

## 17\. Fase 13 - Roadmap 009 Decision Gate

Doel: na Roadmap 008 beslissen of er ooit een echte pilot-implementatie komt.

### Mogelijke uitkomsten

* \[ ] `NO-GO`: terug naar paper/testnet.
* \[ ] `MORE-EVIDENCE`: meer Roadmap 005/006/007 runs nodig.
* \[ ] `DESIGN-ONLY-COMPLETE`: pilot ontwerp klaar, geen implementatie.
* \[ ] `READY-FOR-ROADMAP-009-DESIGN`: alleen als alle gates groen zijn.

### Acceptatiecriteria

* \[ ] Geen automatische overgang naar live.
* \[ ] Menselijke review blijft verplicht.
* \[ ] Roadmap 009 mag alleen ontstaan met evidence bundle.

\---

## 18\. Nieuwe bestanden

### Docs

* \[ ] `docs/live-pilot-evidence-gate.md`
* \[ ] `docs/live-pilot-policy.md`
* \[ ] `docs/live-account-safety-checklist.md`
* \[ ] `docs/live-pilot-manual-approval.md`
* \[ ] `docs/live-dry-run-mode.md`
* \[ ] `docs/two-person-rule.md`
* \[ ] `docs/micro-pilot-execution-design.md`
* \[ ] `docs/live-pilot-stop-rollback.md`
* \[ ] `docs/operator-heartbeat.md`
* \[ ] `docs/live-pilot-risk-notice.md`
* \[ ] `docs/live-pilot-simulation.md`
* \[ ] `docs/live-pilot-dashboard-design.md`
* \[ ] `docs/live-pilot-no-go-criteria.md`
* \[ ] `docs/roadmap-009-decision-gate.md`

### Source design stubs

* \[ ] `src/binance\_spot\_bot/live\_policy.py`
* \[ ] `src/binance\_spot\_bot/live\_dry\_run.py`
* \[ ] `src/binance\_spot\_bot/operator\_heartbeat.py`
* \[ ] `src/binance\_spot\_bot/no\_go.py`
* \[ ] `src/binance\_spot\_bot/pilot\_simulation.py`

### Tests

* \[ ] `tests/test\_live\_policy.py`
* \[ ] `tests/test\_live\_dry\_run.py`
* \[ ] `tests/test\_operator\_heartbeat.py`
* \[ ] `tests/test\_no\_go.py`
* \[ ] `tests/test\_pilot\_simulation.py`

\---

## 19\. Definition of Done

Roadmap 008 is klaar als:

* \[ ] Live-pilot policy is geschreven.
* \[ ] Evidence gate is geschreven.
* \[ ] Account safety checklist is geschreven.
* \[ ] Manual approval flow is ontworpen.
* \[ ] Live dry-run mode is ontworpen.
* \[ ] Two-person rule is ontworpen.
* \[ ] Micro-pilot rules zijn ontworpen.
* \[ ] Stop/rollback design is compleet.
* \[ ] Operator heartbeat design is compleet.
* \[ ] Risk notice is compleet.
* \[ ] Simulation report bestaat.
* \[ ] Dashboard design bestaat.
* \[ ] No-go criteria zijn machine-readable.
* \[ ] Tests bewijzen dat live execution niet geactiveerd wordt.
* \[ ] Roadmap 009 decision gate bestaat.
* \[ ] Alle docs zijn lokaal beschikbaar.
* \[ ] Live trading blijft disabled.

\---

## 20\. Mijn advies

Ik zou deze roadmap pas uitvoeren nadat Roadmap 005, 006 en 007 minimaal gedeeltelijk bewijs hebben opgeleverd.

De veiligste volgorde blijft:

1. \[ ] Roadmap 005 bouwen.
2. \[ ] Roadmap 006 bouwen.
3. \[ ] Roadmap 007 bouwen.
4. \[ ] Roadmap 008 alleen als design/audit roadmap maken.
5. \[ ] Geen echte live pilot zonder aparte Roadmap 009 en bewijs.

Roadmap 008 is dus geen “meer features”-roadmap, maar een veiligheids- en beslissingsroadmap.

