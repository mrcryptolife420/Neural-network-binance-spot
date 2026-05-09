# Roadmap 013 - Testing, CI/CD Hardening, Release Signing, Plugin Sandboxing \& Installer UX

Status: Concept / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-09  
Voorgestelde bestandsnaam:

```text
Roadmap docs/013-roadmap-testing-cicd-release-signing-plugin-sandboxing-installer-ux.md
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
* `010-roadmap-dashboard-strategy-lab-signal-debugging-replay-sandbox.md`
* `011-roadmap-safe-dashboard-copilot-strategy-templates-dataset-builder-ui.md`
* `012-roadmap-advanced-scanner-experiment-database-notebook-exports-dashboard-performance.md`

Doel: het project technisch betrouwbaar maken voordat er nóg meer features bovenop komen. Roadmap 013 focust op automatische tests, CI/CD, type checking, coverage, mutation testing, release signing, installer UX, plugin sandboxing, dependency/security audit en build verification. Dit is de kwaliteitslaag die nodig is om toekomstige roadmaps veilig te blijven bouwen.

Live trading blijft buiten scope.

\---

## 0\. Waarom deze Roadmap 013

Roadmap 009 t/m 012 voegen veel dashboard-, research-, copilot-, scanner- en exportfunctionaliteit toe. Dat maakt het project krachtiger, maar ook complexer.

Daarom is de volgende beste stap niet opnieuw een grote featurelaag, maar:

* \[ ] betrouwbaarheid;
* \[ ] testbaarheid;
* \[ ] releasekwaliteit;
* \[ ] installatiestabiliteit;
* \[ ] pluginveiligheid;
* \[ ] CI/CD;
* \[ ] type checks;
* \[ ] security audits;
* \[ ] build verification.

Zonder deze laag wordt het risico groter dat nieuwe dashboard- of tradinglogica iets breekt dat eerder veilig was.

\---

## 1\. Onderzoek en huidige basis

### Repo-check

* \[x] Geen Roadmap 013 gevonden in repo-zoekresultaten.
* \[x] `pyproject.toml` bestaat en gebruikt Python `>=3.12`.
* \[x] `pyproject.toml` heeft optional dependencies:

  * `research`;
  * `dev`;
  * `ui`;
  * `realtime`;
  * `mlops`.
* \[x] `dev` bevat momenteel:

  * `pytest`;
  * `ruff`.
* \[x] `ruff` is geconfigureerd.
* \[x] `pytest` testpaths zijn geconfigureerd.
* \[x] `spot-bot` CLI entrypoint bestaat.
* \[x] `scripts/check-local-env.ps1` controleert Python en UI dependencies.
* \[x] Bestaande tests dekken onder andere config fail-closed en live readiness.
* \[x] Binance Spot public exchangeInfo bevat rate limits, order types en filters die in tests gesimuleerd moeten blijven.

### Gaten

* \[ ] Geen duidelijke `.github/workflows` CI gevonden.
* \[ ] Geen coverage config.
* \[ ] Geen mypy/pyright.
* \[ ] Geen mutation testing.
* \[ ] Geen benchmark suite.
* \[ ] Geen release build verification.
* \[ ] Geen signed/hash release manifest.
* \[ ] Geen installer test.
* \[ ] Geen plugin sandbox policy.
* \[ ] Geen dependency vulnerability audit.
* \[ ] Geen complete “all checks” command dat CI en lokaal exact hetzelfde draait.
* \[ ] Geen testmatrix voor Windows/Linux/Python versions.
* \[ ] Geen performance regression checks.

\---

## 2\. Scope

### In scope

* \[ ] CI/CD workflow.
* \[ ] Local all-checks runner.
* \[ ] Coverage reporting.
* \[ ] Type checking.
* \[ ] Ruff lint/format.
* \[ ] Security/dependency audit.
* \[ ] Mutation testing.
* \[ ] Benchmark suite.
* \[ ] Contract tests voor Binance adapter/parsers.
* \[ ] Dashboard smoke tests.
* \[ ] Plugin sandboxing.
* \[ ] Release build script.
* \[ ] Release verification script.
* \[ ] Release hashes/signing.
* \[ ] Installer/portable package UX.
* \[ ] Documentation portal.
* \[ ] Contribution/development guide.

### Out of scope

* \[ ] Live trading.
* \[ ] New trading strategy logic.
* \[ ] New model architecture.
* \[ ] Cloud deployment as requirement.
* \[ ] Remote plugin marketplace.
* \[ ] Real-money pilot implementation.

\---

## 3\. Fase 0 - Quality contract

Doel: exact vastleggen welke checks elke commit/release moet halen.

### Nieuwe doc

```text
docs/quality-contract.md
```

### Required checks

* \[ ] Unit tests.
* \[ ] Integration tests.
* \[ ] No-live safety tests.
* \[ ] Ruff lint.
* \[ ] Ruff format check.
* \[ ] Type check.
* \[ ] Coverage threshold.
* \[ ] Security scan.
* \[ ] Dependency audit.
* \[ ] Dashboard import smoke.
* \[ ] CLI smoke.
* \[ ] Package build smoke.
* \[ ] Release verification.
* \[ ] No secrets in artifacts.

### Acceptatiecriteria

* \[ ] Quality contract is zichtbaar in repo.
* \[ ] CI gebruikt dezelfde checks als lokaal.
* \[ ] Roadmap mag niet naar `Voltooid docs` zonder quality contract groen.
* \[ ] Live trading blijft disabled.

\---

## 4\. Fase 1 - Unified local all-checks runner

Doel: één command lokaal alles laten controleren.

### Nieuwe scripts

```text
scripts/check-all.ps1
scripts/check-all.py
```

### Checks

* \[ ] Python version.
* \[ ] Project import.
* \[ ] CLI import.
* \[ ] Dashboard import.
* \[ ] Unit tests.
* \[ ] Ruff check.
* \[ ] Ruff format check.
* \[ ] Type check.
* \[ ] Security scan.
* \[ ] No-live UI check.
* \[ ] No-secret generated artifact check.
* \[ ] Optional coverage.
* \[ ] Optional dependency audit.

### CLI

```powershell
python -m binance\_spot\_bot.cli check-all
```

### Acceptatiecriteria

* \[ ] `scripts/check-all.ps1` werkt op Windows.
* \[ ] `scripts/check-all.py` werkt cross-platform.
* \[ ] CI en lokaal gebruiken dezelfde checklijst.
* \[ ] Output is duidelijk groen/geel/rood.
* \[ ] Geen secrets worden geprint.

\---

## 5\. Fase 2 - GitHub Actions CI

Doel: elke push en pull request automatisch valideren.

### Nieuwe workflow

```text
.github/workflows/ci.yml
```

### Matrix

* \[ ] Windows latest, Python 3.12.
* \[ ] Ubuntu latest, Python 3.12.
* \[ ] Optional Python 3.13 allowed-failure later.
* \[ ] Minimal install.
* \[ ] `\[dev]` install.
* \[ ] `\[ui]` import smoke.
* \[ ] `\[realtime]` parser smoke.
* \[ ] `\[mlops]` optional smoke.

### Jobs

* \[ ] lint.
* \[ ] tests.
* \[ ] type-check.
* \[ ] security-scan.
* \[ ] dashboard-smoke.
* \[ ] build-package.
* \[ ] artifact-secret-scan.

### Acceptatiecriteria

* \[ ] CI draait zonder Binance credentials.
* \[ ] CI gebruikt geen live endpoints.
* \[ ] Tests mocken externe calls.
* \[ ] Failing safety test blokkeert merge.
* \[ ] CI artifacts bevatten geen secrets.

\---

## 6\. Fase 3 - Coverage and test strategy

Doel: testdekking meetbaar maken.

### Tools

* \[ ] `pytest-cov`.
* \[ ] Coverage config in `pyproject.toml`.
* \[ ] Coverage HTML report.
* \[ ] Coverage XML for CI.

### Thresholds

Start realistisch:

* \[ ] Minimum total coverage: 60%.
* \[ ] Critical modules: 80%.
* \[ ] No-live safety modules: 90%.

Critical modules:

* \[ ] config;
* \[ ] risk;
* \[ ] execution;
* \[ ] order lifecycle;
* \[ ] redaction;
* \[ ] credentials;
* \[ ] settings store;
* \[ ] dashboard mode selectors;
* \[ ] testnet policy modules;
* \[ ] plugin permissions.

### Acceptatiecriteria

* \[ ] Coverage report wordt gegenereerd.
* \[ ] Critical modules krijgen hogere eis.
* \[ ] Coverage threshold groeit per roadmap.
* \[ ] Coverage mag niet dalen zonder expliciete reden.

\---

## 7\. Fase 4 - Type checking

Doel: runtimefouten eerder vinden.

### Tools

Kies één hoofdpad:

* \[ ] `mypy`

of:

* \[ ] `pyright`

Aanbevolen start:

* \[ ] `mypy` voor core modules.
* \[ ] Later strenger maken.

### Taken

* \[ ] Voeg type-check dependency toe.
* \[ ] Voeg config toe in `pyproject.toml`.
* \[ ] Start met core:

  * config;
  * types;
  * risk;
  * execution;
  * data;
  * features;
  * session\_store;
  * order\_lifecycle.
* \[ ] Dashboard mag eerst soepeler zijn.
* \[ ] Voeg `typing\_extensions` alleen toe indien nodig.

### Acceptatiecriteria

* \[ ] Core modules type-checken.
* \[ ] Geen massale `ignore` zonder comment.
* \[ ] CI draait type-check.
* \[ ] Type-check errors blokkeren core changes.

\---

## 8\. Fase 5 - Safety regression test suite

Doel: elke roadmap moet bewijzen dat safety niet stuk is.

### Nieuwe testgroep

```text
tests/safety/
```

### Tests

* \[ ] Live mode not selectable in dashboard.
* \[ ] Live mode not selectable in CLI user-facing safe commands.
* \[ ] `LIVE\_TRADING\_ENABLED=false` in launcher.
* \[ ] `KILL\_SWITCH=true` default.
* \[ ] `validate\_live\_readiness()` fail-closed.
* \[ ] Copilot cannot call execution.
* \[ ] Strategy Lab cannot place orders.
* \[ ] Scanner cannot place orders.
* \[ ] Demo trade cannot call signed endpoint.
* \[ ] Plugins cannot request forbidden permissions.
* \[ ] Reports contain no secrets.
* \[ ] Dashboard generated diagnostics are redacted.

### Acceptatiecriteria

* \[ ] Safety suite draait apart en in CI.
* \[ ] Safety suite moet altijd groen zijn.
* \[ ] Geen feature mag safety suite overslaan.
* \[ ] Nieuwe features krijgen safety tests.

\---

## 9\. Fase 6 - Binance contract tests

Doel: Binance API assumptions lokaal testen zonder echte calls.

### Waarom

Public Binance Spot `exchangeInfo` bevat filters en rate limits. De bot moet die correct blijven parsen en toepassen.

### Fixtures

* \[ ] BTCUSDT exchangeInfo fixture.
* \[ ] ETHUSDT exchangeInfo fixture.
* \[ ] Symbol halted fixture.
* \[ ] Missing filter fixture.
* \[ ] Changed NOTIONAL filter fixture.
* \[ ] Order book ticker fixture.
* \[ ] Kline fixture.
* \[ ] 429 response fixture.
* \[ ] 418 response fixture.
* \[ ] 5xx response fixture.

### Tests

* \[ ] tick size parsing.
* \[ ] lot size parsing.
* \[ ] min notional parsing.
* \[ ] market lot size parsing.
* \[ ] symbol status handling.
* \[ ] rate limit headers.
* \[ ] retry policy.
* \[ ] circuit breaker.
* \[ ] stale data detection.

### Acceptatiecriteria

* \[ ] Contract tests gebruiken geen internet.
* \[ ] Fixtures zijn versie/hash-gelabeld.
* \[ ] Parser changes breken tests als API-shape assumptions wijzigen.
* \[ ] Testdata bevat geen secrets.

\---

## 10\. Fase 7 - Dashboard smoke/browser tests

Doel: dashboard niet breken door refactors.

### Opties

* \[ ] Streamlit import smoke.
* \[ ] Component-level render tests waar mogelijk.
* \[ ] Playwright optional.
* \[ ] Screenshot smoke optional.

### Testflows

* \[ ] Dashboard imports.
* \[ ] Local demo loads.
* \[ ] Live badge visible.
* \[ ] First-run wizard opens.
* \[ ] Demo Spot Trading tab visible.
* \[ ] Strategy Lab tab visible.
* \[ ] Copilot panel visible.
* \[ ] Emergency stop visible.
* \[ ] No live button visible.
* \[ ] Dashboard can render snapshot fixture.

### Acceptatiecriteria

* \[ ] Dashboard smoke draait in CI.
* \[ ] Browser tests mogen optioneel maar niet flaky zijn.
* \[ ] No-live UI tests zijn verplicht.
* \[ ] UI refactor moet tests updaten.

\---

## 11\. Fase 8 - Mutation testing

Doel: testen of tests echt bugs vangen.

### Toolopties

* \[ ] `mutmut`
* \[ ] `cosmic-ray`

Start klein:

* \[ ] risk module.
* \[ ] execution module.
* \[ ] config live-readiness.
* \[ ] redaction.
* \[ ] plugin permissions.
* \[ ] copilot permissions.

### Acceptatiecriteria

* \[ ] Mutation score baseline bestaat.
* \[ ] Critical modules krijgen mutation target.
* \[ ] Mutations rond live guards moeten gedood worden.
* \[ ] Mutation tests hoeven niet elke PR volledig te draaien, maar wel nightly/manual.

\---

## 12\. Fase 9 - Benchmark suite

Doel: performance regressions vinden.

### Nieuwe module

```text
benchmarks/
```

### Benchmarks

* \[ ] feature building.
* \[ ] data quality checks.
* \[ ] session loading.
* \[ ] dashboard chart building.
* \[ ] scanner ranking.
* \[ ] strategy lab replay.
* \[ ] experiment database queries.
* \[ ] notebook export.
* \[ ] report generation.

### Acceptatiecriteria

* \[ ] Benchmarks zijn lokaal te draaien.
* \[ ] CI kan smoke benchmark draaien.
* \[ ] Full benchmark is optioneel/manual.
* \[ ] Results worden opgeslagen als artifact.
* \[ ] Grote regressies krijgen waarschuwing.

\---

## 13\. Fase 10 - Plugin sandboxing

Doel: Roadmap 011/012 plugin architecture veilig maken.

### Nieuwe module

```text
src/binance\_spot\_bot/plugin\_sandbox.py
```

### Policies

* \[ ] Plugin permissions explicit.
* \[ ] No direct execution access.
* \[ ] No direct credentials access.
* \[ ] No raw filesystem write buiten plugin data dir.
* \[ ] No network access tenzij expliciet allowed.
* \[ ] No live mode access.
* \[ ] Plugin errors isolated.
* \[ ] Plugin manifest required.
* \[ ] Plugin signature/hash optional.

### Acceptatiecriteria

* \[ ] Plugin zonder manifest laadt niet.
* \[ ] Plugin met forbidden permission laadt niet.
* \[ ] Plugin crash breekt dashboard niet.
* \[ ] Plugin kan geen order plaatsen.
* \[ ] Tests dekken malicious plugin fixtures.

\---

## 14\. Fase 11 - Security and dependency audit

Doel: dependency/security problemen zichtbaar maken.

### Tools

* \[ ] `pip-audit` optional.
* \[ ] `bandit` optional.
* \[ ] internal secret scan.
* \[ ] artifact secret scan.
* \[ ] dependency freeze.

### Tasks

* \[ ] Voeg `security-audit` command toe.
* \[ ] Voeg dependency vulnerability report toe.
* \[ ] Scan:

  * source;
  * docs;
  * reports;
  * sessions;
  * releases;
  * experiment bundles.
* \[ ] Dashboard Security tab toont laatste audit.

### Acceptatiecriteria

* \[ ] Security audit kan lokaal draaien.
* \[ ] CI draait lightweight audit.
* \[ ] Findings zijn duidelijk.
* \[ ] False positives kunnen met comment worden onderdrukt.
* \[ ] Geen secrets in artifacts.

\---

## 15\. Fase 12 - Release build system

Doel: reproduceerbare lokale releases maken.

### Scripts

```text
scripts/build-release.ps1
scripts/build-release.py
scripts/verify-release.ps1
scripts/verify-release.py
```

### Release inhoud

* \[ ] source snapshot.
* \[ ] pyproject.
* \[ ] lock/dependency snapshot.
* \[ ] docs.
* \[ ] scripts.
* \[ ] dashboard start/stop.
* \[ ] tests summary.
* \[ ] coverage summary.
* \[ ] security summary.
* \[ ] release manifest.
* \[ ] hashes.
* \[ ] no secrets.

### Acceptatiecriteria

* \[ ] Release zip wordt gemaakt.
* \[ ] Release manifest bevat hashes.
* \[ ] Verify script controleert hashes.
* \[ ] Release bevat geen secrets.
* \[ ] Release is gekoppeld aan commit/version.

\---

## 16\. Fase 13 - Release signing / hash verification

Doel: gebruiker kan zien of release is gewijzigd.

### Taken

* \[ ] SHA256 manifest.
* \[ ] Optional minisign/GPG signing.
* \[ ] Local verify command.
* \[ ] Dashboard about panel toont:

  * version;
  * commit;
  * release hash;
  * build time;
  * approved modes.
* \[ ] Docs voor verificatie.

### Acceptatiecriteria

* \[ ] Elke release heeft hash manifest.
* \[ ] Verify faalt bij wijziging.
* \[ ] Signature is optioneel maar voorbereid.
* \[ ] Dashboard toont release metadata.

\---

## 17\. Fase 14 - Installer / portable package UX

Doel: Windows-gebruiker kan makkelijk installeren/starten.

### Richtingen

* \[ ] Portable folder.
* \[ ] `.cmd` shortcuts.
* \[ ] PowerShell installer.
* \[ ] Optional Start Menu shortcut.
* \[ ] Optional desktop shortcut.
* \[ ] Uninstall script.
* \[ ] Update script.

### Taken

* \[ ] `Install Bot Dashboard.cmd`.
* \[ ] `Update Bot Dashboard.cmd`.
* \[ ] `Uninstall Bot Dashboard.cmd`.
* \[ ] `Open Data Folder.cmd`.
* \[ ] `Open Logs Folder.cmd`.
* \[ ] `Run Diagnostics.cmd`.
* \[ ] Preflight vóór start.
* \[ ] Friendly errors.

### Acceptatiecriteria

* \[ ] Install werkt op Windows zonder handmatige PYTHONPATH.
* \[ ] Update overschrijft geen data/secrets.
* \[ ] Uninstall verwijdert geen data zonder confirm.
* \[ ] Paths met spaties werken.
* \[ ] Logs zijn makkelijk vindbaar.

\---

## 18\. Fase 15 - Documentation portal

Doel: documentatie beter vindbaar maken.

### Docs structuur

```text
docs/
  getting-started/
  dashboard/
  demo-trading/
  strategy-lab/
  copilot/
  scanner/
  model-training/
  testing/
  release/
  security/
  runbooks/
```

### Taken

* \[ ] `docs/index.md`.
* \[ ] Quick start.
* \[ ] Troubleshooting.
* \[ ] Dashboard guide.
* \[ ] Development guide.
* \[ ] Release guide.
* \[ ] Testing guide.
* \[ ] Security guide.
* \[ ] Glossary.

### Acceptatiecriteria

* \[ ] Nieuwe gebruiker vindt startinstructies snel.
* \[ ] Ontwikkelaar vindt test/release flow snel.
* \[ ] Docs bevatten geen live trading claims.
* \[ ] Docs zijn onderdeel van release.

\---

## 19\. Fase 16 - Roadmap completion governance

Doel: voorkomen dat roadmaps “voltooid” worden zonder bewijs.

### Taken

* \[ ] Voeg `docs/roadmap-completion-policy.md` toe.
* \[ ] Roadmap mag naar `Voltooid docs` als:

  * checks groen;
  * tests groen;
  * security scan groen;
  * docs bijgewerkt;
  * acceptance criteria afgevinkt;
  * known issues genoteerd.
* \[ ] Voeg completion template toe.
* \[ ] Voeg CLI helper toe:

```powershell
python -m binance\_spot\_bot.cli roadmap-check --roadmap Roadmap docs/013...
```

### Acceptatiecriteria

* \[ ] Roadmap completion is evidence-based.
* \[ ] Geen roadmap wordt voltooid zonder testresultaten.
* \[ ] Voltooid docs blijven betrouwbaar.

\---

## 20\. Nieuwe bestanden

### Source

* \[ ] `src/binance\_spot\_bot/checks.py`
* \[ ] `src/binance\_spot\_bot/ci\_report.py`
* \[ ] `src/binance\_spot\_bot/plugin\_sandbox.py`
* \[ ] `src/binance\_spot\_bot/release\_build.py`
* \[ ] `src/binance\_spot\_bot/release\_verify.py`
* \[ ] `src/binance\_spot\_bot/security\_audit.py`
* \[ ] `src/binance\_spot\_bot/roadmap\_check.py`

### Tests

* \[ ] `tests/safety/test\_no\_live\_ui.py`
* \[ ] `tests/safety/test\_no\_live\_cli.py`
* \[ ] `tests/safety/test\_no\_signed\_demo.py`
* \[ ] `tests/contract/test\_binance\_exchange\_info.py`
* \[ ] `tests/contract/test\_binance\_rate\_limits.py`
* \[ ] `tests/test\_plugin\_sandbox.py`
* \[ ] `tests/test\_release\_build.py`
* \[ ] `tests/test\_release\_verify.py`
* \[ ] `tests/test\_roadmap\_check.py`

### Scripts

* \[ ] `scripts/check-all.ps1`
* \[ ] `scripts/check-all.py`
* \[ ] `scripts/build-release.ps1`
* \[ ] `scripts/build-release.py`
* \[ ] `scripts/verify-release.ps1`
* \[ ] `scripts/verify-release.py`
* \[ ] `scripts/install-dashboard.ps1`
* \[ ] `scripts/update-dashboard.ps1`
* \[ ] `scripts/uninstall-dashboard.ps1`

### CI

* \[ ] `.github/workflows/ci.yml`
* \[ ] `.github/workflows/security.yml`
* \[ ] `.github/workflows/release-smoke.yml`

### Docs

* \[ ] `docs/quality-contract.md`
* \[ ] `docs/testing-guide.md`
* \[ ] `docs/ci-cd.md`
* \[ ] `docs/release-guide.md`
* \[ ] `docs/plugin-sandboxing.md`
* \[ ] `docs/installer-ux.md`
* \[ ] `docs/roadmap-completion-policy.md`

\---

## 21\. Prioriteiten

### Eerst

1. \[ ] Quality contract.
2. \[ ] Local check-all runner.
3. \[ ] CI workflow.
4. \[ ] Safety regression suite.
5. \[ ] Coverage.

### Daarna

6. \[ ] Type checking.
7. \[ ] Binance contract tests.
8. \[ ] Dashboard smoke tests.
9. \[ ] Security/dependency audit.
10. \[ ] Plugin sandboxing.

### Als laatste

11. \[ ] Mutation testing.
12. \[ ] Benchmarks.
13. \[ ] Release build/verify.
14. \[ ] Release signing/hash verification.
15. \[ ] Installer UX.
16. \[ ] Documentation portal.
17. \[ ] Roadmap completion governance.

\---

## 22\. Definition of Done

Roadmap 013 is klaar als:

* \[ ] `check-all` lokaal werkt.
* \[ ] GitHub Actions CI draait.
* \[ ] Ruff lint/format draait.
* \[ ] Pytest suite draait.
* \[ ] Coverage report bestaat.
* \[ ] Type checking draait voor core modules.
* \[ ] Safety regression suite bestaat.
* \[ ] Binance contract tests bestaan.
* \[ ] Dashboard smoke tests bestaan.
* \[ ] Security/dependency audit bestaat.
* \[ ] Plugin sandboxing werkt.
* \[ ] Release build script werkt.
* \[ ] Release verify script werkt.
* \[ ] Release hash manifest bestaat.
* \[ ] Installer/portable UX werkt.
* \[ ] Documentation portal bestaat.
* \[ ] Roadmap completion policy bestaat.
* \[ ] Alle generated artifacts zijn secret-free.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 013 kan na uitvoering naar `Voltooid docs`.

\---

## 23\. Verwachte Roadmap 014 daarna

Na Roadmap 013 zou Roadmap 014 logisch focussen op:

* \[ ] UX polish op basis van echte gebruikersfeedback;
* \[ ] volledige Windows packaged app;
* \[ ] accessibility;
* \[ ] mobile/tablet dashboard layout;
* \[ ] theme system;
* \[ ] guided tutorials;
* \[ ] onboarding videos/scripts;
* \[ ] local backup/restore;
* \[ ] workspace profiles.

