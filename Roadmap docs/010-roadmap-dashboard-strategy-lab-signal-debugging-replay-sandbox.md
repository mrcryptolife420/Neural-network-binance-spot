# Roadmap 010 - Dashboard Strategy Lab, Signal Debugging \& Replay Sandbox

Status: Concept / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-09  
Voorgestelde bestandsnaam:

```text
Roadmap docs/010-roadmap-dashboard-strategy-lab-signal-debugging-replay-sandbox.md
```

Volgt op:

* `Voltooid docs/001-roadmap-binance-spot-ai-trading-bot.md`
* `Voltooid docs/002-roadmap-local-visual-paper-bot-dashboard.md`
* `Voltooid docs/003-roadmap-realtime-market-data-modelops-dashboard.md`
* `Voltooid docs/004-roadmap-windows-one-click-secure-control-center.md`
* `Roadmap docs/005-roadmap-long-paper-testnet-alerts-scanner-packaging.md`
* `006-roadmap-multi-symbol-portfolio-testnet-endurance-mlops.md`
* `007-roadmap-live-readiness-audit-shadow-chaos-release-governance.md`
* `008-roadmap-strict-live-readiness-pilot-design.md`
* `009-roadmap-unified-dashboard-launcher-binance-spot-demo-trading-control-center.md`

Doel: nadat Roadmap 009 dashboard/startflow en demo spot trading veel beter maakt, voegt Roadmap 010 een echte **Strategy Lab** laag toe. De gebruiker moet in het dashboard kunnen begrijpen waarom de bot BUY/SELL/HOLD doet, strategieën vergelijken, signalen debuggen, sessies replayen, instellingen veilig aanpassen en demo-resultaten visueel vergelijken.

Live trading blijft volledig buiten scope.

\---

## 0\. Waarom deze Roadmap 010

Roadmap 009 maakt het dashboard bruikbaar als control center:

* \[ ] bot/dashboard samen starten;
* \[ ] first-run wizard;
* \[ ] demo spot trading tab;
* \[ ] manual demo trade ticket;
* \[ ] betere orders/fills/lifecycle UI.

Daarna is de volgende beste verbetering:

* \[ ] niet méér knoppen;
* \[ ] maar méér inzicht.

De gebruiker moet kunnen zien:

* \[ ] waarom een signaal ontstaat;
* \[ ] waarom RiskEngine blokkeert;
* \[ ] waarom een demo trade uitgevoerd wordt;
* \[ ] welke parameters het resultaat veranderen;
* \[ ] welke strategie beter/slechter werkt;
* \[ ] welke sessies vergelijkbaar zijn;
* \[ ] hoe een oude markt opnieuw afgespeeld kan worden.

\---

## 1\. Onderzoek en basis

### Bestaande repo-basis

Gecontroleerd:

* \[x] Dashboard heeft al tabs, start/pause/step/reset/emergency stop.
* \[x] CLI heeft al `run-local`, `stream-paper`, `dashboard`, `launch-dashboard`, session en evaluation commands.
* \[x] Windows startscript start dashboard veilig met live disabled.
* \[x] Runtime heeft snapshots met candles, signals, fills, equity, data quality, model, account en lifecycle.
* \[x] Sessions slaan summaries, snapshots en fills op.
* \[x] Binance Spot public market data is bruikbaar voor BTCUSDT/ETHUSDT/BNBUSDT preview en demo/paper analysis.

### Gaten die Roadmap 010 oplost

* \[ ] De gebruiker ziet nog onvoldoende waarom een botbeslissing gebeurde.
* \[ ] Strategy parameters zijn nog niet visueel vergelijkbaar.
* \[ ] Evaluation is nog beperkt en niet als labervaring gebouwd.
* \[ ] Er is geen replay sandbox vanuit oude sessies.
* \[ ] Er is geen session compare dashboard.
* \[ ] Er is geen visual “decision timeline”.
* \[ ] Er is geen parameter sweep UI.
* \[ ] Er is geen duidelijke explainability voor features/signals/risk blocks.
* \[ ] Er is geen “wat als ik deze risk settings wijzig?” preview.

\---

## 2\. Scope

### In scope

* \[ ] Strategy Lab tab.
* \[ ] Signal explanation panel.
* \[ ] Risk decision debugger.
* \[ ] Replay sandbox.
* \[ ] Session comparison dashboard.
* \[ ] Parameter sweep UI.
* \[ ] Feature inspector.
* \[ ] Model-vs-baseline comparison UI.
* \[ ] What-if simulator.
* \[ ] Better charts and overlays.
* \[ ] Exportable strategy experiment reports.

### Out of scope

* \[ ] Live trading.
* \[ ] Autonome LLM trade execution.
* \[ ] Margin/futures/leverage.
* \[ ] Cloud deployment.
* \[ ] Strategy marketplace.
* \[ ] Winstgaranties.

\---

## 3\. Fase 0 - Strategy Lab safety contract

Doel: alle Strategy Lab functies read-only of demo/paper houden.

### Taken

* \[ ] Maak `docs/strategy-lab-safety-contract.md`.
* \[ ] Definieer Strategy Lab als:

  * read-only analysis;
  * demo/paper simulation;
  * no live orders;
  * no signed endpoints required.
* \[ ] Voeg dashboard badge toe:

  * `Strategy Lab = analysis only`.
* \[ ] Tests:

  * Strategy Lab kan geen live mode laden.
  * Strategy Lab kan geen `place\_order()` triggeren.
  * Strategy Lab gebruikt alleen session data, demo data of public market data.

### Acceptatiecriteria

* \[ ] Elke Strategy Lab actie is veilig.
* \[ ] Geen Strategy Lab knop kan echte orders sturen.
* \[ ] Live blijft disabled.
* \[ ] Safety contract is zichtbaar in dashboard.

\---

## 4\. Fase 1 - Strategy Lab tab

Doel: één centrale dashboardplek voor strategie-analyse.

### Nieuwe tab

```text
Strategy Lab
```

### Layout

* \[ ] Strategy selector.
* \[ ] Model selector.
* \[ ] Symbol selector.
* \[ ] Timeframe selector.
* \[ ] Data source selector:

  * current session;
  * historical session;
  * demo replay;
  * Binance public data cache.
* \[ ] Run analysis button.
* \[ ] Results summary:

  * PnL;
  * max drawdown;
  * trades;
  * win rate;
  * fees;
  * slippage;
  * block reasons.
* \[ ] Compare to baseline:

  * no-trade;
  * buy-and-hold;
  * rule-based;
  * tiny neural model.

### Acceptatiecriteria

* \[ ] Strategy Lab werkt zonder API keys.
* \[ ] Strategy Lab kan huidige sessie analyseren.
* \[ ] Strategy Lab kan oude sessie analyseren.
* \[ ] Resultaten zijn exporteerbaar.
* \[ ] Geen live execution.

\---

## 5\. Fase 2 - Signal Explanation Panel

Doel: uitleggen waarom BUY/SELL/HOLD ontstond.

### Nieuwe module

```text
src/binance\_spot\_bot/signal\_explainer.py
```

### Uitlegvelden

* \[ ] Signal side.
* \[ ] Confidence.
* \[ ] Model version.
* \[ ] Feature values.
* \[ ] Belangrijkste feature drivers.
* \[ ] Candle context.
* \[ ] Trend context.
* \[ ] Volume context.
* \[ ] Volatility context.
* \[ ] Previous signal comparison.

### Dashboard UI

* \[ ] Klik op chart signal marker.
* \[ ] Side panel opent.
* \[ ] Toon:

  * raw signal;
  * human explanation;
  * feature table;
  * confidence gauge;
  * model metadata.

### Acceptatiecriteria

* \[ ] Elk signal point is klikbaar.
* \[ ] Gebruiker ziet waarom signaal ontstond.
* \[ ] Untrained model/HOLD wordt duidelijk uitgelegd.
* \[ ] Explanation is deterministic, geen hallucinerende AI nodig.
* \[ ] Export bevat explanation.

\---

## 6\. Fase 3 - Risk Decision Debugger

Doel: duidelijk maken waarom RiskEngine toestaat of blokkeert.

### Nieuwe module

```text
src/binance\_spot\_bot/risk\_debugger.py
```

### Debug output

* \[ ] Kill switch status.
* \[ ] Signal confidence vs minimum.
* \[ ] Max trades status.
* \[ ] Daily loss status.
* \[ ] Position exposure status.
* \[ ] Spread status.
* \[ ] Data age status.
* \[ ] Balance status.
* \[ ] Final decision.
* \[ ] Human-readable reason.

### Dashboard UI

* \[ ] Risk decision timeline.
* \[ ] Block reason badges.
* \[ ] Expand details per block.
* \[ ] What would fix this?

  * lower quote size;
  * wait for fresh data;
  * reduce spread threshold;
  * disable kill switch only in safe paper flow;
  * choose safer symbol.

### Acceptatiecriteria

* \[ ] Iedere BLOCK heeft duidelijke uitleg.
* \[ ] Iedere ALLOW toont welke checks groen waren.
* \[ ] Debugger kan geen risk gates omzeilen.
* \[ ] Tests dekken alle belangrijke block reasons.

\---

## 7\. Fase 4 - Replay Sandbox

Doel: oude sessies opnieuw afspelen en zien wat de bot deed.

### Nieuwe module

```text
src/binance\_spot\_bot/replay\_sandbox.py
```

### Features

* \[ ] Load old session.
* \[ ] Replay candles.
* \[ ] Replay signals.
* \[ ] Replay fills.
* \[ ] Replay equity.
* \[ ] Timeline scrubber.
* \[ ] Speed:

  * 1x;
  * 5x;
  * 10x;
  * instant.
* \[ ] Pause at:

  * first trade;
  * first block;
  * max drawdown;
  * critical alert.
* \[ ] Add notes to replay moments.

### Dashboard UI

* \[ ] Replay tab inside Strategy Lab.
* \[ ] Timeline slider.
* \[ ] Chart updates with historical markers.
* \[ ] Decision panel updates per selected timestamp.

### Acceptatiecriteria

* \[ ] Een oude sessie kan visueel opnieuw bekeken worden.
* \[ ] Replay wijzigt de originele sessie niet.
* \[ ] Replay werkt offline.
* \[ ] Replay kan worden geëxporteerd als report.

\---

## 8\. Fase 5 - Session Comparison Dashboard

Doel: meerdere sessies naast elkaar vergelijken.

### Vergelijkingsvelden

* \[ ] Symbol.
* \[ ] Mode.
* \[ ] Source.
* \[ ] Model version.
* \[ ] Risk preset.
* \[ ] PnL.
* \[ ] Max drawdown.
* \[ ] Trade count.
* \[ ] Block count.
* \[ ] Fees.
* \[ ] Slippage.
* \[ ] Alerts.
* \[ ] Data quality status.
* \[ ] Runtime duration.

### Dashboard UI

* \[ ] Selecteer 2-10 sessions.
* \[ ] Summary table.
* \[ ] Equity curves overlay.
* \[ ] PnL distribution.
* \[ ] Block reason comparison.
* \[ ] Model comparison.
* \[ ] Export comparison report.

### Acceptatiecriteria

* \[ ] Gebruiker kan snel zien welke sessie beter was.
* \[ ] Resultaten zijn niet alleen PnL-gebaseerd.
* \[ ] Slechte data quality wordt meegewogen.
* \[ ] Export bevat alle gekozen sessies.

\---

## 9\. Fase 6 - Parameter Sweep UI

Doel: veilig testen hoe instellingen effect hebben.

### Parameters

* \[ ] Min signal confidence.
* \[ ] Max spread bps.
* \[ ] Max position quote.
* \[ ] Default quote size.
* \[ ] Feature window.
* \[ ] Risk preset.
* \[ ] Strategy variant.

### Backend

```text
src/binance\_spot\_bot/parameter\_sweep.py
```

### Taken

* \[ ] Run parameter grid op demo/replay data.
* \[ ] Beperk combinaties voor performance.
* \[ ] Toon top resultaten.
* \[ ] Toon robustness score.
* \[ ] Penaliseer:

  * hoge drawdown;
  * te veel trades;
  * te veel fees;
  * lage data quality;
  * overfit-signalen.

### Acceptatiecriteria

* \[ ] Sweep gebruikt geen live data execution.
* \[ ] Sweep draait op demo/replay/public cached data.
* \[ ] Beste resultaat wordt niet automatisch toegepast.
* \[ ] Gebruiker kan settings handmatig overnemen.
* \[ ] Overfit waarschuwing zichtbaar.

\---

## 10\. Fase 7 - What-if Simulator

Doel: simuleren wat er zou gebeuren met andere instellingen.

### Voorbeelden

* \[ ] Wat als quote size 10 → 25 ging?
* \[ ] Wat als min confidence 0.15 → 0.40 ging?
* \[ ] Wat als max spread strenger was?
* \[ ] Wat als fees/slippage hoger waren?
* \[ ] Wat als bot alleen BUY maar niet SELL deed?
* \[ ] Wat als cooldown na loss streak aan stond?

### UI

* \[ ] Current session baseline.
* \[ ] What-if settings panel.
* \[ ] Simulated result.
* \[ ] Difference:

  * PnL delta;
  * drawdown delta;
  * trades delta;
  * blocks delta;
  * fees delta.

### Acceptatiecriteria

* \[ ] What-if wijzigt echte runtime niet.
* \[ ] Resultaat is duidelijk als simulatie gemarkeerd.
* \[ ] Export mogelijk.
* \[ ] Geen live execution.

\---

## 11\. Fase 8 - Feature Inspector

Doel: feature pipeline zichtbaar maken.

### UI

* \[ ] Feature table per candle.
* \[ ] Feature charts:

  * returns;
  * volatility;
  * volume z-score;
  * wick/body ratio.
* \[ ] Label preview.
* \[ ] Missing/invalid feature warnings.
* \[ ] Feature version display.

### Backend

```text
src/binance\_spot\_bot/feature\_inspector.py
```

### Acceptatiecriteria

* \[ ] Gebruiker ziet welke features de bot gebruikt.
* \[ ] Feature anomalies zijn zichtbaar.
* \[ ] No-lookahead waarschuwingen zichtbaar.
* \[ ] Export als CSV/JSON.

\---

## 12\. Fase 9 - Model-vs-Baseline Comparison

Doel: modelkwaliteit visueel vergelijken.

### Baselines

* \[ ] No trade.
* \[ ] Buy and hold.
* \[ ] Rule-based.
* \[ ] Tiny neural.
* \[ ] Candidate model.
* \[ ] Champion model.

### UI

* \[ ] Model selector.
* \[ ] Baseline selector.
* \[ ] Metrics:

  * return;
  * drawdown;
  * precision;
  * recall;
  * trade count;
  * exposure time;
  * turnover;
  * fees.
* \[ ] Chart:

  * equity comparison;
  * signal distribution;
  * confusion matrix indien labels beschikbaar.

### Acceptatiecriteria

* \[ ] Geen modelpromotie op train-only resultaat.
* \[ ] Slecht model wordt zichtbaar.
* \[ ] Baseline comparison is verplicht bij export.
* \[ ] ModelRegistry metadata wordt gebruikt.

\---

## 13\. Fase 10 - Dashboard Annotations \& Notes

Doel: gebruiker kan opmerkingen toevoegen tijdens analyse.

### Taken

* \[ ] Voeg notes toe per session.
* \[ ] Voeg notes toe per timestamp.
* \[ ] Voeg notes toe per trade.
* \[ ] Notes worden lokaal opgeslagen.
* \[ ] Notes worden geëxporteerd in reports.
* \[ ] Geen secrets in notes via warning en scan.

### Acceptatiecriteria

* \[ ] Gebruiker kan analyse-notities maken.
* \[ ] Notes blijven gekoppeld aan sessie/trade.
* \[ ] Notes zijn exporteerbaar.
* \[ ] Secret scan checkt notes.

\---

## 14\. Fase 11 - Strategy Experiment Reports

Doel: alle labresultaten exporteerbaar maken.

### Report outputs

* \[ ] `strategy\_lab\_summary.md`
* \[ ] `strategy\_lab\_results.json`
* \[ ] `session\_comparison.csv`
* \[ ] `parameter\_sweep.csv`
* \[ ] `what\_if\_results.json`
* \[ ] `feature\_snapshot.csv`
* \[ ] `risk\_debug\_timeline.jsonl`

### Acceptatiecriteria

* \[ ] Elk experiment krijgt ID.
* \[ ] Elk experiment is reproduceerbaar.
* \[ ] Report bevat settings, model, data source en hash.
* \[ ] Report bevat geen secrets.
* \[ ] Report kan later gebruikt worden voor Roadmap 011.

\---

## 15\. Fase 12 - UI polish en advanced charts

### Chart upgrades

* \[ ] Signal confidence overlay.
* \[ ] Risk block markers.
* \[ ] Spread overlay.
* \[ ] Volume panel.
* \[ ] Drawdown chart.
* \[ ] Trade PnL waterfall.
* \[ ] Equity curve with max drawdown marker.
* \[ ] Session comparison equity overlay.
* \[ ] Tooltip met:

  * candle;
  * signal;
  * risk;
  * fill;
  * note.

### Acceptatiecriteria

* \[ ] Charts blijven snel.
* \[ ] Gebruiker kan overlays aan/uit zetten.
* \[ ] Tooltips zijn begrijpelijk.
* \[ ] Geen chart overload in default view.

\---

## 16\. Fase 13 - Testplan

### Unit tests

* \[ ] `tests/test\_signal\_explainer.py`
* \[ ] `tests/test\_risk\_debugger.py`
* \[ ] `tests/test\_replay\_sandbox.py`
* \[ ] `tests/test\_session\_compare.py`
* \[ ] `tests/test\_parameter\_sweep.py`
* \[ ] `tests/test\_what\_if\_simulator.py`
* \[ ] `tests/test\_feature\_inspector.py`
* \[ ] `tests/test\_strategy\_lab\_reports.py`

### Integration tests

* \[ ] Load session into Strategy Lab.
* \[ ] Explain signal.
* \[ ] Explain risk block.
* \[ ] Replay session.
* \[ ] Compare sessions.
* \[ ] Run parameter sweep.
* \[ ] Run what-if simulation.
* \[ ] Export report.

### Safety tests

* \[ ] Strategy Lab cannot call live execution.
* \[ ] Strategy Lab cannot call signed order endpoint.
* \[ ] Reports contain no secrets.
* \[ ] Live mode remains hidden/disabled.

\---

## 17\. Nieuwe bestanden

### Source

* \[ ] `src/binance\_spot\_bot/signal\_explainer.py`
* \[ ] `src/binance\_spot\_bot/risk\_debugger.py`
* \[ ] `src/binance\_spot\_bot/replay\_sandbox.py`
* \[ ] `src/binance\_spot\_bot/session\_compare.py`
* \[ ] `src/binance\_spot\_bot/parameter\_sweep.py`
* \[ ] `src/binance\_spot\_bot/what\_if.py`
* \[ ] `src/binance\_spot\_bot/feature\_inspector.py`
* \[ ] `src/binance\_spot\_bot/strategy\_lab\_reports.py`
* \[ ] `src/binance\_spot\_bot/ui/strategy\_lab.py`
* \[ ] `src/binance\_spot\_bot/ui/replay.py`
* \[ ] `src/binance\_spot\_bot/ui/session\_compare.py`

### Docs

* \[ ] `docs/strategy-lab.md`
* \[ ] `docs/signal-explanation.md`
* \[ ] `docs/risk-decision-debugger.md`
* \[ ] `docs/replay-sandbox.md`
* \[ ] `docs/session-comparison.md`
* \[ ] `docs/parameter-sweep.md`
* \[ ] `docs/what-if-simulator.md`
* \[ ] `docs/feature-inspector.md`

\---

## 18\. Prioriteiten

### Eerst

1. \[ ] Strategy Lab tab.
2. \[ ] Signal Explanation Panel.
3. \[ ] Risk Decision Debugger.
4. \[ ] Replay Sandbox.

### Daarna

5. \[ ] Session Comparison Dashboard.
6. \[ ] Parameter Sweep UI.
7. \[ ] What-if Simulator.
8. \[ ] Feature Inspector.

### Als laatste

9. \[ ] Model-vs-baseline comparison.
10. \[ ] Notes/annotations.
11. \[ ] Experiment reports.
12. \[ ] Advanced charts.

\---

## 19\. Definition of Done

Roadmap 010 is klaar als:

* \[ ] Strategy Lab bestaat in dashboard.
* \[ ] Signalen kunnen verklaard worden.
* \[ ] Risk blocks kunnen verklaard worden.
* \[ ] Oude sessies kunnen worden gereplayed.
* \[ ] Sessies kunnen worden vergeleken.
* \[ ] Parameter sweeps draaien veilig.
* \[ ] What-if simulaties wijzigen runtime niet.
* \[ ] Feature inspector toont inputfeatures.
* \[ ] Model-vs-baseline comparison werkt.
* \[ ] Experiment reports zijn exporteerbaar.
* \[ ] Reports bevatten geen secrets.
* \[ ] Geen enkele Strategy Lab functie kan live orders sturen.
* \[ ] Tests en security scan slagen.
* \[ ] Docs zijn bijgewerkt.
* \[ ] Roadmap 010 kan na uitvoering naar `Voltooid docs`.

\---

## 20\. Verwachte Roadmap 011 daarna

Als Roadmap 010 klaar is, zou Roadmap 011 logisch focussen op:

* \[ ] AI-assisted local explanations zonder orderrechten;
* \[ ] strategy templates;
* \[ ] dashboard plugin architecture;
* \[ ] better model training UX;
* \[ ] dataset builder UI;
* \[ ] automated research notebook exports;
* \[ ] advanced multi-symbol scanner UX.

