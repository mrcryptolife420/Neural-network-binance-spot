# Roadmap 015 - Operational Hardening, Dashboard Polish en Long-Running Paper Ops

Status: Voltooid  
Project: Neural network Binance spot  
Datum: 2026-05-09  
Bestandsdoel:

```text
Roadmap docs/015-roadmap-operational-hardening-dashboard-polish-long-paper-ops.md
```

## 1. Context uit vorige roadmaps

`Roadmap docs/` is leeg op startmoment van deze roadmap. `Voltooid docs/` bevat Roadmaps 001 t/m 014 plus `codex-build-priority-plan-roadmaps-005-014.md`.

Belangrijkste afgeronde basis:

- Roadmap 001-004: veilige Binance Spot bot-architectuur, lokaal dashboard, realtime data/modelops, Windows one-click control center.
- Roadmap 005-014: check-all/CI, control-center, demo trading, preflight, alerts, session reports, paper accounting, workspaces, backup/restore, diagnostics, strategy lab, copilot guardrails, experiment DB, scanner history, portfolio paper, evidence, shadow, chaos en readiness.
- `check-all` was groen met 67 tests.
- Live trading blijft uitgeschakeld; Roadmap 008 is alleen design/audit.

Conclusie: de volgende stap is geen nieuwe feature-explosie. De code heeft veel veilige MVP-bouwstenen. Roadmap 015 moet die bouwstenen productwaardig integreren, langdurige paper-runs betrouwbaarder maken en het dashboard minder JSON/MVP en meer operator-control-center maken.

## 2. Hoofddoel

Maak van de huidige veilige MVP een robuuste lokale paper/testnet-readiness operatoromgeving:

- één duidelijke operator-flow van start tot rapport;
- lange demo/paper sessies met watchdog, accounting en session report;
- dashboard-tabs die bestaande modules echt gebruiken;
- minder ruwe JSON als hoofdweergave;
- consistente UI-status, badges, tabellen en acties;
- betere testdekking rond langdurige sessies en regressies;
- geen live trading, geen secrets, geen signed orderpad buiten expliciet testnet-readiness ontwerp.

## 3. Niet opnieuw bouwen

Niet dubbel bouwen:

- geen tweede `RiskEngine`;
- geen tweede `ExecutionEngine`;
- geen tweede credential store;
- geen tweede dashboard-app;
- geen nieuwe scanner als `scanner_history.py` kan worden uitgebreid;
- geen nieuwe portfolio-accounting als `portfolio.py`, `portfolio_risk.py` en `paper_accounting.py` kunnen worden geïntegreerd;
- geen live-trading route;
- geen autonomous LLM trader.

Gebruik en versterk bestaande modules:

- `runtime.py`
- `alerts.py`
- `paper_accounting.py`
- `session_report.py`
- `workspaces.py`
- `diagnostics.py`
- `support_bundle.py`
- `risk_debugger.py`
- `signal_explainer.py`
- `replay_sandbox.py`
- `scanner_history.py`
- `portfolio.py`
- `evidence.py`
- `readiness.py`
- `ui/streamlit_app.py`

## 4. Fase A - Runtime integratie van alerts, paper accounting en reports

Doel: runtime gebruikt de Roadmap 005/006/007 bouwstenen echt tijdens demo/paper runs.

Taken:

- [x] Integreer `AlertManager` in `BotRuntime`.
- [x] Runtime emit alerts bij:
  - stale data;
  - spread boven limiet;
  - max-loss bereikt;
  - order lifecycle mismatch;
  - write failure;
  - connectivity fallback.
- [x] Gebruik `PaperAccount` of een equivalent uit `paper_accounting.py` als bron voor:
  - quote balance;
  - base balance;
  - realized PnL;
  - fees;
  - slippage;
  - exposure.
- [x] Schrijf alerts naar `alerts.jsonl` in de huidige sessie.
- [x] Schrijf order lifecycle events naar `orders.jsonl` waar mogelijk.
- [x] Laat `session_report.py` bij session finish automatisch exporteerbare artifacts maken.
- [x] Voeg runtime summary veld toe:
  - alerts count;
  - critical alerts count;
  - realized PnL;
  - fees paid;
  - slippage estimate;
  - readiness blockers.

Acceptatie:

- [x] `run-local --mode demo --steps 200` schrijft session summary, fills, alerts en report bundle.
- [x] Paper PnL in dashboard en report komt uit dezelfde accountingbron.
- [x] Critical alert stopt of pauzeert paper/demo runtime volgens watchdog policy.
- [x] Geen signed Binance endpoint wordt aangeroepen.
- [x] `check-all` blijft groen.

## 5. Fase B - Dashboard operator polish

Doel: dashboard minder MVP/JSON en meer bruikbaar control center.

Taken:

- [x] Maak compacte status-header component:
  - live disabled;
  - mode;
  - workspace;
  - profile;
  - kill switch;
  - session status;
  - readiness level.
- [x] Maak herbruikbare UI-render helpers voor:
  - badges;
  - metric rows;
  - redacted tables;
  - alert list;
  - fills table;
  - risk block timeline.
- [x] Vervang hoofdweergave-JSON door tabellen/metrics waar nuttig:
  - Demo Spot Trading fills;
  - Risk timeline;
  - Alerts;
  - Portfolio state;
  - Readiness blockers;
  - Scanner ranking.
- [x] JSON blijft beschikbaar als inklapbare debugsectie.
- [x] Zorg dat `DEMO/PAPER ONLY` duidelijk zichtbaar is op alle tradingachtige panels.
- [x] Zorg dat emergency stop en pause zichtbaar blijven.
- [x] Voeg no-overlap/responsive sanity check toe voor brede desktop en laptopbreedte.

Acceptatie:

- [x] Dashboard opent zonder error via `Start Bot Dashboard.cmd`.
- [x] Belangrijkste status is zichtbaar zonder scrollen.
- [x] Demo trading tab toont fills als tabel.
- [x] Strategy Lab toont block reasons en signal uitleg zonder ruwe JSON als primaire UI.
- [x] Live disabled badge blijft zichtbaar.
- [x] Browser/HTTP smoke test slaagt.

## 6. Fase C - Workspace lifecycle afronden

Doel: workspaces worden echte operatorprofielen, niet alleen opgeslagen JSON.

Taken:

- [x] Breid `WorkspaceProfile` uit met:
  - `created_at_ms`;
  - `last_opened_at_ms`;
  - `layout`;
  - `notes`;
  - `schema_version`.
- [x] Workspace create/rename/duplicate/archive.
- [x] Workspace switch reset runtime bewust en schrijft audit event.
- [x] Per-workspace data dir of subdir.
- [x] Workspace selector in dashboard met duidelijke actieve workspace.
- [x] Workspace export/import zonder secrets.
- [x] Workspace archive wist niets zonder confirm.

Acceptatie:

- [x] Nieuwe workspace kan zonder API keys worden gemaakt.
- [x] Workspace switch zet runtime veilig stil of vraagt bevestiging.
- [x] Workspace config bevat geen secrets.
- [x] Export/import is redacted en testbaar.
- [x] Geen bestaande data wordt overschreven zonder confirm.

## 7. Fase D - Long-running paper session mode

Doel: langdurige lokale paper runs worden betrouwbaar meetbaar.

Taken:

- [x] CLI command:

```powershell
python -m binance_spot_bot.cli paper-session --symbol BTCUSDT --minutes 60
```

- [x] Runtime budget:
  - max minutes;
  - max steps;
  - max paper orders;
  - max critical alerts;
  - max report size.
- [x] Graceful shutdown met session report.
- [x] Heartbeat events in session.
- [x] Watchdog pause/stop bij critical alerts.
- [x] Local demo fallback als Binance public data onbereikbaar is.
- [x] Dashboard panel voor actieve/laatste paper session.

Acceptatie:

- [x] 15-minuten demo/paper smoke kan lokaal draaien zonder keys.
- [x] Session eindigt met report bundle.
- [x] Ctrl+C of stop maakt alsnog summary/report waar mogelijk.
- [x] Geen live URL vereist.
- [x] Geen secrets in logs/reports.

## 8. Fase E - Scanner naar research workflow koppelen

Doel: scanner is een read-only research hulpmiddel met geschiedenis en exports.

Taken:

- [x] Dashboard scanner grid met watchlist:
  - symbol;
  - bid/ask/spread;
  - volume;
  - signal;
  - confidence;
  - rank score.
- [x] Scanner run opslaan in `ScannerHistory`.
- [x] Scanner run indexeren in `ExperimentDB`.
- [x] Scanner export naar HTML/notebook via bestaande exporters.
- [x] Scanner mag geen orderintents uitvoeren.
- [x] Per-workspace watchlist.

Acceptatie:

- [x] Scanner werkt zonder credentials op demo/fallback data.
- [x] Scanner plaatst geen orders.
- [x] Scanner history is zichtbaar in dashboard.
- [x] Export bevat geen secrets.

## 9. Fase F - Replay, compare en evidence als operator-flow

Doel: na elke run kan gebruiker terugkijken, vergelijken en bewijs vastleggen.

Taken:

- [x] Dashboard replay selector voor vorige sessies.
- [x] Timeline scrubber op basis van `ReplaySandbox`.
- [x] Session comparison UI voor 2-10 sessies.
- [x] Evidence vault schrijft hashes voor:
  - check-all output;
  - session report;
  - shadow proof;
  - readiness score.
- [x] Readiness panel toont:
  - score;
  - blockers;
  - ontbrekende evidence;
  - next safe step.

Acceptatie:

- [x] Replay wijzigt geen sessiedata.
- [x] Compare export werkt.
- [x] Evidence hash verificatie werkt.
- [x] Readiness kan live nooit groen maken.

## 10. Fase G - Testnet-readiness hardening zonder live trading

Doel: testnet/demo Binance readiness betrouwbaarder maken zonder live trading te activeren.

Taken:

- [x] Profile-specific readiness:
  - Local Demo;
  - Binance public Spot paper;
  - Binance Demo Spot API;
  - Binance Spot Testnet.
- [x] Credential status per profiel zonder plaintext.
- [x] Connectivity panel toont REST/WebSocket/user-data readiness.
- [x] Testnet endurance guard zichtbaar in dashboard.
- [x] Unresolved order lifecycle panel.
- [x] Cancel-open ontwerp blijft gated en testnet-only.
- [x] No-live regression tests uitbreiden voor alle nieuwe UI routes.

Acceptatie:

- [x] Readiness werkt zonder credentials en toont duidelijke blockers.
- [x] Demo/testnet profiel kan niet per ongeluk live URL gebruiken.
- [x] Geen live mode in CLI/dashboard.
- [x] Safety tests falen bij live route.

## 11. Fase H - Documentation en onboarding bijwerken

Doel: gebruiker kan lokaal starten, sessie draaien, rapport vinden en volgende veilige stap begrijpen.

Taken:

- [x] Update `docs/local-dashboard.md`.
- [x] Maak `docs/operator-workflow.md`.
- [x] Maak `docs/long-running-paper-sessions.md`.
- [x] Maak `docs/scanner-research-workflow.md`.
- [x] Maak `docs/replay-compare-evidence.md`.
- [x] Update `docs/live-readiness-pilot-design.md` met Roadmap 015 evidence.
- [x] Dashboard onboarding checklist:
  - start local demo;
  - run paper session;
  - inspect alerts;
  - export report;
  - compare sessions;
  - backup workspace.

Acceptatie:

- [x] Docs noemen geen echte API keys.
- [x] Docs blijven paper/testnet-readiness-first.
- [x] Live trading blijft expliciet disabled.
- [x] Nieuwe gebruiker kan de lokale operator-flow volgen.

## 12. Fase I - Testing, visual checks en CI uitbreiding

Taken:

- [x] Tests voor runtime alerts/accounting/report integration.
- [x] Tests voor workspace lifecycle.
- [x] Tests voor paper-session CLI.
- [x] Tests voor scanner history + experiment DB.
- [x] Tests voor replay/compare/evidence dashboard helpers.
- [x] Tests voor testnet-readiness no-live routes.
- [x] Browser smoke test documenteren of automatiseren waar haalbaar.
- [x] `check-all` uitbreiden met:
  - preflight;
  - optional ruff;
  - roadmap/docs no-secret scan;
  - dashboard import;
  - no-live UI/CLI.

Acceptatie:

- [x] `python -m binance_spot_bot.cli check-all --json` is groen.
- [x] Minimaal 80 unit tests of aantoonbaar meer dekking op nieuwe integraties.
- [x] Security scan heeft nul findings.
- [x] Dashboard import smoke blijft groen.
- [x] Geen live route is toegevoegd.

## 13. Voorgestelde bouwvolgorde

1. Runtime alerts/accounting/report integration.
2. Dashboard operator header en UI helpers.
3. Workspace lifecycle.
4. Long-running paper-session CLI.
5. Scanner research workflow.
6. Replay/compare/evidence flow.
7. Testnet-readiness hardening.
8. Docs/onboarding.
9. CI/check-all uitbreiding.

## 14. Beste eerste Codex-opdracht

```text
Implementeer alleen Roadmap 015 Fase A.
Integreer AlertManager, PaperAccount en session_report met BotRuntime zonder live trading.
Schrijf alerts/fills/orders naar de bestaande SessionStore artifacts.
Voeg tests toe voor demo run, critical alert stop/pause, report bundle en no signed endpoint.
Laat check-all groen blijven.
```

Waarom eerst:

- runtime-integratie is de basis voor dashboard, reports, replay, readiness en lange sessies;
- dit bouwt voort op bestaande modules in plaats van nieuwe modules te stapelen;
- de impact is groot maar de scope blijft duidelijk testbaar.

## 15. Definition of Done

Roadmap 015 is klaar als:

- [x] runtime gebruikt alerts, accounting en reports geïntegreerd;
- [x] dashboard is bruikbaarder en minder JSON-first;
- [x] workspaces hebben lifecycle-acties;
- [x] long-running paper sessions zijn mogelijk en rapporteren netjes;
- [x] scanner is read-only, historisch en exporteerbaar;
- [x] replay/compare/evidence flow werkt;
- [x] testnet-readiness is duidelijker en blijft no-live;
- [x] docs en onboarding zijn bijgewerkt;
- [x] `check-all` is groen;
- [x] security scan is groen;
- [x] live trading blijft disabled;
- [x] roadmap kan na uitvoering naar `Voltooid docs/`.
