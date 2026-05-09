# Roadmap 014 - Windows App UX, Workspace Profiles, Backup/Restore, Accessibility \& Onboarding

Status: Concept / Gepland  
Project: Neural network Binance spot  
Datum: 2026-05-09  
Voorgestelde bestandsnaam:

```text
Roadmap docs/014-roadmap-windows-app-ux-workspace-profiles-backup-restore-accessibility-onboarding.md
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
* `013-roadmap-testing-cicd-release-signing-plugin-sandboxing-installer-ux.md`

Doel: het project voelt na Roadmap 014 niet meer als losse scripts + Streamlit, maar als een nette lokale Windows-app/workspace. De focus ligt op gebruiksgemak, onboarding, workspace-profielen, backup/restore, toegankelijkheid, thema’s, diagnostic center en veilige data-migraties. Live trading blijft volledig uitgeschakeld.

\---

## 0\. Waarom deze Roadmap 014

Roadmap 013 maakt het project technisch betrouwbaarder met CI, tests, release verification en installer UX. Daarna zou ik de gebruikerervaring afronden:

* \[ ] makkelijker installeren;
* \[ ] makkelijker openen;
* \[ ] makkelijker weten waar data/logs staan;
* \[ ] meerdere werkruimtes/profielen;
* \[ ] backup/restore;
* \[ ] thema’s;
* \[ ] toegankelijkheid;
* \[ ] onboarding tutorials;
* \[ ] guided diagnostics;
* \[ ] safe reset/migration tools.

Dit is belangrijk omdat het project anders krachtig wordt, maar nog steeds te technisch aanvoelt.

\---

## 1\. Onderzoek en huidige basis

### Repo-status

* \[x] Geen Roadmap 014 gevonden in repo-zoekresultaten.
* \[x] README bevat terminalruntime, dashboardstart en Windows one-click start.
* \[x] `Start Bot Dashboard.cmd` / `scripts/start-dashboard.ps1` starten Streamlit lokaal.
* \[x] Startscript zet `LIVE\_TRADING\_ENABLED=false`.
* \[x] Startscript zet `KILL\_SWITCH=true`.
* \[x] Stopscript gebruikt PID file om dashboardproces te stoppen.
* \[x] `DashboardSettingsStore` bewaart dashboardinstellingen zonder secret keys.
* \[x] Dashboard settings bevatten:

  * selected profile;
  * symbol;
  * interval;
  * scenario;
  * source;
  * model alias;
  * risk preset;
  * watchlist.
* \[x] Er zijn risk presets:

  * conservative;
  * balanced;
  * aggressive-paper-only.

### Huidige beperkingen

* \[ ] Geen echte app shell / control launcher UI.
* \[ ] Geen installer met Start Menu/Desktop shortcut.
* \[ ] Geen workspace profiles.
* \[ ] Geen backup/restore.
* \[ ] Geen data migration manager.
* \[ ] Geen in-app diagnostics center.
* \[ ] Geen accessibility review.
* \[ ] Geen theme system.
* \[ ] Geen mobile/tablet responsive dashboard plan.
* \[ ] Geen guided tutorial/checklist in UI.
* \[ ] Geen support bundle generator voor debugging.
* \[ ] Geen safe factory reset met data-preserve opties.

\---

## 2\. Scope

### In scope

* \[ ] Windows app shell / launcher UI.
* \[ ] Start Menu/Desktop shortcuts.
* \[ ] Workspace profiles.
* \[ ] Backup/restore.
* \[ ] Data migration manager.
* \[ ] Diagnostic center.
* \[ ] Support bundle export.
* \[ ] Theme system.
* \[ ] Accessibility improvements.
* \[ ] Responsive dashboard layout.
* \[ ] Guided tutorials.
* \[ ] User onboarding.
* \[ ] Safe reset tools.
* \[ ] Logs/data folder management.
* \[ ] Settings import/export.

### Out of scope

* \[ ] Live trading.
* \[ ] Live pilot implementation.
* \[ ] Cloud service.
* \[ ] Mobile native app.
* \[ ] Remote account sync.
* \[ ] Trading strategy changes.
* \[ ] Model architecture changes.

\---

## 3\. Fase 0 - App UX safety contract

Doel: de app-ervaring mag nooit safety gates verbergen of verzwakken.

### Taken

* \[ ] Maak `docs/app-ux-safety-contract.md`.
* \[ ] Definieer altijd-zichtbare badges:

  * `LIVE DISABLED`;
  * active mode;
  * active workspace;
  * active profile;
  * kill switch status.
* \[ ] Elke launcher moet hard zetten:

  * `LIVE\_TRADING\_ENABLED=false`;
  * safe dashboard mode;
  * no live shortcuts.
* \[ ] Elke backup/export moet secrets redacteren.
* \[ ] Elke restore moet secrets niet automatisch herstellen.
* \[ ] Elke reset moet bevestiging vragen.
* \[ ] Tests voor no-live shortcuts.

### Acceptatiecriteria

* \[ ] Safety is zichtbaar in launcher en dashboard.
* \[ ] Geen app shortcut start live mode.
* \[ ] Backup/export bevat geen secrets.
* \[ ] Restore activeert geen live mode.

\---

## 4\. Fase 1 - Windows App Shell / Launcher UI

Doel: een eenvoudige lokale launcher bovenop de bestaande scripts.

### Nieuwe module

```text
src/binance\_spot\_bot/app\_shell.py
```

### Launcher functies

* \[ ] Start dashboard.
* \[ ] Stop dashboard.
* \[ ] Restart dashboard.
* \[ ] Open dashboard URL.
* \[ ] Open data folder.
* \[ ] Open logs folder.
* \[ ] Run diagnostics.
* \[ ] Create backup.
* \[ ] Restore backup.
* \[ ] Choose workspace.
* \[ ] Show safety status.
* \[ ] Show last error.

### Implementatie-opties

Start simpel:

* \[ ] PowerShell/CLI shell met menu.

Later optioneel:

* \[ ] Tkinter lightweight GUI.
* \[ ] PySide/Tauri later onderzoeken.

### Acceptatiecriteria

* \[ ] Gebruiker kan alles starten vanuit één menu.
* \[ ] Launcher toont status en URL.
* \[ ] Launcher detecteert bestaand dashboard.
* \[ ] Launcher toont live disabled.
* \[ ] Launcher werkt zonder API keys.

\---

## 5\. Fase 2 - Installer, shortcuts en portable UX

Doel: installatie voelt als een lokale app.

### Scripts

```text
Install Bot Dashboard.cmd
Update Bot Dashboard.cmd
Uninstall Bot Dashboard.cmd
Open Bot Dashboard.cmd
Open Data Folder.cmd
Open Logs Folder.cmd
Run Diagnostics.cmd
```

### Taken

* \[ ] Maak Start Menu shortcut.
* \[ ] Optioneel Desktop shortcut.
* \[ ] Configureer portable data dir.
* \[ ] Update zonder data te overschrijven.
* \[ ] Uninstall met keuze:

  * app verwijderen;
  * data bewaren;
  * data verwijderen met confirm phrase.
* \[ ] Detecteer Python en dependencies.
* \[ ] Geef vriendelijke foutmelding met fix.

### Acceptatiecriteria

* \[ ] Install werkt op Windows 11.
* \[ ] Paths met spaties werken.
* \[ ] Update bewaart workspaces en sessions.
* \[ ] Uninstall verwijdert data niet zonder expliciete confirm.
* \[ ] Shortcuts starten altijd safe mode.

\---

## 6\. Fase 3 - Workspace Profiles

Doel: gebruiker kan meerdere lokale werkruimtes hebben.

### Nieuwe module

```text
src/binance\_spot\_bot/workspaces.py
```

### Workspace bevat

* \[ ] name;
* \[ ] data\_dir;
* \[ ] selected profile;
* \[ ] symbol/watchlist;
* \[ ] risk preset;
* \[ ] dashboard layout;
* \[ ] theme;
* \[ ] language;
* \[ ] enabled plugins;
* \[ ] notes;
* \[ ] created\_at;
* \[ ] last\_opened\_at.

### Voorbeelden

* \[ ] `Demo Learning`
* \[ ] `BTCUSDT Paper`
* \[ ] `Scanner Research`
* \[ ] `Model Training`
* \[ ] `Testnet Readiness`

### Taken

* \[ ] Workspace selector in launcher.
* \[ ] Workspace selector in dashboard.
* \[ ] Create/rename/duplicate/archive workspace.
* \[ ] Per-workspace settings.
* \[ ] Per-workspace data folders.
* \[ ] No secrets in workspace config.
* \[ ] Workspace export/import.

### Acceptatiecriteria

* \[ ] Gebruiker kan veilig wisselen tussen workspaces.
* \[ ] Workspace switch reset runtime bewust en duidelijk.
* \[ ] Workspace archive wist niets zonder confirm.
* \[ ] Geen secrets in workspace files.

\---

## 7\. Fase 4 - Backup \& Restore

Doel: lokale data veilig kunnen bewaren en terugzetten.

### Nieuwe module

```text
src/binance\_spot\_bot/backup\_restore.py
```

### Backup inhoud

* \[ ] dashboard settings;
* \[ ] workspaces;
* \[ ] sessions;
* \[ ] reports;
* \[ ] experiment database;
* \[ ] strategy templates;
* \[ ] model metadata;
* \[ ] docs/user notes;
* \[ ] cache manifest optioneel.

Niet automatisch meenemen:

* \[ ] API secrets;
* \[ ] listen keys;
* \[ ] raw credentials;
* \[ ] sensitive logs.

### Restore opties

* \[ ] Restore into new workspace.
* \[ ] Merge into current workspace.
* \[ ] Preview backup before restore.
* \[ ] Conflict resolution.
* \[ ] Verify hashes.
* \[ ] Secret scan after restore.

### Acceptatiecriteria

* \[ ] Backup zip bevat manifest.
* \[ ] Backup bevat geen secrets.
* \[ ] Restore overschrijft niets zonder confirm.
* \[ ] Restore kan naar nieuwe workspace.
* \[ ] Backup/restore werkt offline.

\---

## 8\. Fase 5 - Data Migration Manager

Doel: settings/sessions/data veilig upgraden als schema’s veranderen.

### Nieuwe module

```text
src/binance\_spot\_bot/migrations.py
```

### Taken

* \[ ] Voeg schema version toe aan:

  * dashboard settings;
  * workspace config;
  * session summary;
  * experiment database;
  * model metadata.
* \[ ] Migration registry.
* \[ ] Dry-run migration.
* \[ ] Migration backup.
* \[ ] Migration report.
* \[ ] Rollback indien mogelijk.
* \[ ] Dashboard migration warning.

### Acceptatiecriteria

* \[ ] Oude settings kunnen worden gelezen.
* \[ ] Migratie maakt backup.
* \[ ] Migratie faalt veilig.
* \[ ] Geen secrets in migration reports.
* \[ ] Tests dekken oude fixture-bestanden.

\---

## 9\. Fase 6 - Diagnostic Center

Doel: problemen oplossen zonder handmatig logs te zoeken.

### Nieuwe dashboard tab

```text
Diagnostics
```

### Checks

* \[ ] Python version.
* \[ ] Package version.
* \[ ] Current workspace.
* \[ ] Data dir writable.
* \[ ] Logs dir writable.
* \[ ] Dashboard process status.
* \[ ] Streamlit status.
* \[ ] Dependencies installed.
* \[ ] Public Binance connectivity.
* \[ ] Credentials status without exposing secrets.
* \[ ] Last error.
* \[ ] Last security scan.
* \[ ] Disk usage.
* \[ ] Port status.
* \[ ] PID status.

### Acceptatiecriteria

* \[ ] Diagnostics werkt zonder keys.
* \[ ] Output is user-friendly.
* \[ ] Technical details zijn inklapbaar.
* \[ ] Copy diagnostics redacted.

\---

## 10\. Fase 7 - Support Bundle Export

Doel: gebruiker kan één zip maken voor debugging.

### Bundle inhoud

* \[ ] diagnostics report;
* \[ ] redacted settings;
* \[ ] recent logs;
* \[ ] recent session summaries;
* \[ ] system info;
* \[ ] dependency list;
* \[ ] security scan result;
* \[ ] app version;
* \[ ] workspace manifest.

Niet meenemen:

* \[ ] API secrets;
* \[ ] raw credentials;
* \[ ] large caches tenzij gevraagd;
* \[ ] model artifacts tenzij gevraagd.

### Acceptatiecriteria

* \[ ] Support bundle is redacted.
* \[ ] Secret scan draait vóór zip.
* \[ ] Bundle bevat manifest.
* \[ ] Dashboard kan bundle downloaden.
* \[ ] CLI kan bundle maken.

\---

## 11\. Fase 8 - Theme System

Doel: dashboard prettiger en consistenter maken.

### Themes

* \[ ] System default.
* \[ ] Dark.
* \[ ] Light.
* \[ ] High contrast.
* \[ ] Compact.
* \[ ] Large text.

### Taken

* \[ ] Theme settings per workspace.
* \[ ] Chart theme consistent maken.
* \[ ] Status colors consistent maken.
* \[ ] Badges consistent maken.
* \[ ] Avoid color-only status communication.

### Acceptatiecriteria

* \[ ] Theme wisselen reset runtime niet.
* \[ ] High contrast is bruikbaar.
* \[ ] Status is ook via tekst zichtbaar.
* \[ ] Theme config bevat geen secrets.

\---

## 12\. Fase 9 - Accessibility Pass

Doel: dashboard toegankelijker maken.

### Taken

* \[ ] Keyboard navigatie verbeteren.
* \[ ] Button labels duidelijker.
* \[ ] Icon-only acties vermijden.
* \[ ] Contrast check.
* \[ ] Font size opties.
* \[ ] Tables met duidelijke kolomnamen.
* \[ ] Error messages duidelijk.
* \[ ] Screen-reader friendly labels waar mogelijk.
* \[ ] Geen status alleen via kleur.
* \[ ] Emergency stop duidelijk maar niet verwarrend.

### Acceptatiecriteria

* \[ ] Belangrijkste flows werken met toetsenbord.
* \[ ] High-contrast mode werkt.
* \[ ] Kritieke status heeft tekstlabel.
* \[ ] Accessibility checklist is gedocumenteerd.

\---

## 13\. Fase 10 - Responsive dashboard layout

Doel: dashboard werkt beter op kleinere schermen/tablet.

### Breakpoints

* \[ ] Desktop wide.
* \[ ] Laptop.
* \[ ] Tablet.
* \[ ] Narrow browser.

### Taken

* \[ ] Compact overview cards.
* \[ ] Collapsible sidebar.
* \[ ] Tab grouping.
* \[ ] Charts responsive maken.
* \[ ] Tables met pagination.
* \[ ] Mobile-friendly read-only mode.
* \[ ] Emergency stop blijft bereikbaar.

### Acceptatiecriteria

* \[ ] Dashboard blijft bruikbaar op laptop.
* \[ ] Small screens tonen geen kapotte layout.
* \[ ] Trading/demo actions blijven duidelijk gemarkeerd.
* \[ ] Live disabled badge blijft zichtbaar.

\---

## 14\. Fase 11 - Guided onboarding tutorials

Doel: nieuwe gebruiker stap voor stap leren.

### Tutorials

* \[ ] Eerste start.
* \[ ] Local demo draaien.
* \[ ] Binance public Spot data bekijken.
* \[ ] Demo trade uitvoeren.
* \[ ] Risk block begrijpen.
* \[ ] Session export maken.
* \[ ] Strategy Lab openen.
* \[ ] Backup maken.
* \[ ] Diagnostics uitvoeren.

### UI

* \[ ] Checklist.
* \[ ] Progress per workspace.
* \[ ] “Next recommended step”.
* \[ ] Reset tutorial progress.
* \[ ] Links naar docs.

### Acceptatiecriteria

* \[ ] Nieuwe gebruiker kan veilig starten.
* \[ ] Tutorial vereist geen API keys.
* \[ ] Tutorial plaatst geen echte orders.
* \[ ] Progress wordt per workspace opgeslagen.

\---

## 15\. Fase 12 - Settings import/export

Doel: dashboardconfiguratie makkelijk delen zonder secrets.

### Taken

* \[ ] Export selected settings.
* \[ ] Export risk presets.
* \[ ] Export watchlists.
* \[ ] Export layout/theme.
* \[ ] Import with preview.
* \[ ] Secret strip vóór export.
* \[ ] Conflict handling.

### Acceptatiecriteria

* \[ ] Settings export bevat geen secrets.
* \[ ] Import toont wat wijzigt.
* \[ ] Import kan worden geannuleerd.
* \[ ] Invalid settings worden geweigerd.

\---

## 16\. Fase 13 - Safe Factory Reset

Doel: problemen oplossen zonder per ongeluk data te verliezen.

### Reset opties

* \[ ] Reset dashboard layout only.
* \[ ] Reset settings only.
* \[ ] Reset cache only.
* \[ ] Reset current workspace.
* \[ ] Full app reset, data bewaren.
* \[ ] Full app reset, data verwijderen met confirm phrase.

### Acceptatiecriteria

* \[ ] Reset vereist duidelijke keuze.
* \[ ] Destructieve reset vereist exact confirm.
* \[ ] Backup wordt aangeboden vóór reset.
* \[ ] Live blijft disabled na reset.

\---

## 17\. Fase 14 - Logs and Data Folder Manager

Doel: lokale bestanden begrijpelijk maken.

### UI

* \[ ] Open data folder.
* \[ ] Open logs folder.
* \[ ] Show disk usage.
* \[ ] Show largest folders.
* \[ ] Archive logs.
* \[ ] Clear old logs with confirm.
* \[ ] View latest error log.
* \[ ] Copy log path.

### Acceptatiecriteria

* \[ ] Gebruiker vindt logs makkelijk.
* \[ ] Logs kunnen veilig worden opgeschoond.
* \[ ] Geen secrets in log preview.
* \[ ] Active logs worden niet verwijderd.

\---

## 18\. Fase 15 - User feedback loop

Doel: dashboard verbeteren op basis van echte gebruikspunten.

### Taken

* \[ ] In-app feedback note.
* \[ ] Local-only feedback log.
* \[ ] User pain-point tags.
* \[ ] Export feedback notes.
* \[ ] Link feedback aan workspace/session.
* \[ ] Geen externe upload.

### Acceptatiecriteria

* \[ ] Feedback blijft lokaal.
* \[ ] Feedback kan worden geëxporteerd.
* \[ ] Feedback bevat geen secrets via scan.
* \[ ] Roadmap 015 kan feedback gebruiken.

\---

## 19\. Testplan

### Unit tests

* \[ ] `tests/test\_app\_shell.py`
* \[ ] `tests/test\_workspaces.py`
* \[ ] `tests/test\_backup\_restore.py`
* \[ ] `tests/test\_migrations.py`
* \[ ] `tests/test\_diagnostics.py`
* \[ ] `tests/test\_support\_bundle.py`
* \[ ] `tests/test\_theme\_settings.py`
* \[ ] `tests/test\_settings\_import\_export.py`
* \[ ] `tests/test\_factory\_reset.py`
* \[ ] `tests/test\_logs\_data\_manager.py`

### Integration tests

* \[ ] Launcher starts safe mode.
* \[ ] Workspace create/switch/archive.
* \[ ] Backup and restore into new workspace.
* \[ ] Migration dry-run.
* \[ ] Diagnostics report.
* \[ ] Support bundle export.
* \[ ] Settings export/import.
* \[ ] Factory reset safe path.
* \[ ] Logs cleanup safe path.

### Safety tests

* \[ ] No live shortcuts.
* \[ ] Backup has no secrets.
* \[ ] Support bundle has no secrets.
* \[ ] Restore does not enable live.
* \[ ] Reset does not enable live.
* \[ ] Workspace config has no secrets.
* \[ ] Diagnostics redacts credentials.

\---

## 20\. Nieuwe bestanden

### Source

* \[ ] `src/binance\_spot\_bot/app\_shell.py`
* \[ ] `src/binance\_spot\_bot/workspaces.py`
* \[ ] `src/binance\_spot\_bot/backup\_restore.py`
* \[ ] `src/binance\_spot\_bot/migrations.py`
* \[ ] `src/binance\_spot\_bot/diagnostics.py`
* \[ ] `src/binance\_spot\_bot/support\_bundle.py`
* \[ ] `src/binance\_spot\_bot/theme.py`
* \[ ] `src/binance\_spot\_bot/settings\_import\_export.py`
* \[ ] `src/binance\_spot\_bot/factory\_reset.py`
* \[ ] `src/binance\_spot\_bot/logs\_manager.py`
* \[ ] `src/binance\_spot\_bot/ui/diagnostics.py`
* \[ ] `src/binance\_spot\_bot/ui/onboarding.py`
* \[ ] `src/binance\_spot\_bot/ui/workspace\_settings.py`

### Scripts

* \[ ] `Install Bot Dashboard.cmd`
* \[ ] `Update Bot Dashboard.cmd`
* \[ ] `Uninstall Bot Dashboard.cmd`
* \[ ] `Open Bot Dashboard.cmd`
* \[ ] `Open Data Folder.cmd`
* \[ ] `Open Logs Folder.cmd`
* \[ ] `Run Diagnostics.cmd`
* \[ ] `scripts/install-dashboard.ps1`
* \[ ] `scripts/update-dashboard.ps1`
* \[ ] `scripts/uninstall-dashboard.ps1`

### Docs

* \[ ] `docs/app-ux-safety-contract.md`
* \[ ] `docs/windows-app-shell.md`
* \[ ] `docs/workspace-profiles.md`
* \[ ] `docs/backup-restore.md`
* \[ ] `docs/data-migrations.md`
* \[ ] `docs/diagnostics.md`
* \[ ] `docs/support-bundles.md`
* \[ ] `docs/themes-accessibility.md`
* \[ ] `docs/onboarding-tutorials.md`
* \[ ] `docs/settings-import-export.md`
* \[ ] `docs/factory-reset.md`

\---

## 21\. Prioriteiten

### Eerst

1. \[ ] App UX safety contract.
2. \[ ] Workspace profiles.
3. \[ ] Backup/restore.
4. \[ ] Diagnostic center.
5. \[ ] Support bundle export.

### Daarna

6. \[ ] Windows app shell / launcher UI.
7. \[ ] Installer/shortcuts/portable UX.
8. \[ ] Data migration manager.
9. \[ ] Settings import/export.
10. \[ ] Safe factory reset.

### Als laatste

11. \[ ] Theme system.
12. \[ ] Accessibility pass.
13. \[ ] Responsive layout.
14. \[ ] Guided onboarding tutorials.
15. \[ ] Logs/data folder manager.
16. \[ ] User feedback loop.

\---

## 22\. Definition of Done

Roadmap 014 is klaar als:

* \[ ] Windows app shell bestaat.
* \[ ] Installer/shortcuts werken.
* \[ ] Workspaces kunnen worden gemaakt, gewisseld en gearchiveerd.
* \[ ] Backup/restore werkt zonder secrets.
* \[ ] Data migrations zijn versieerbaar en veilig.
* \[ ] Diagnostic center werkt.
* \[ ] Support bundle export werkt en is redacted.
* \[ ] Theme system werkt.
* \[ ] Accessibility checklist is uitgevoerd.
* \[ ] Responsive layout is verbeterd.
* \[ ] Guided onboarding werkt.
* \[ ] Settings import/export werkt.
* \[ ] Safe factory reset werkt.
* \[ ] Logs/data folder manager werkt.
* \[ ] Alle tests slagen.
* \[ ] Security scan is groen.
* \[ ] Live trading blijft disabled.
* \[ ] Roadmap 014 kan na uitvoering naar `Voltooid docs`.

\---

## 23\. Verwachte Roadmap 015 daarna

Na Roadmap 014 zou ik Roadmap 015 richten op:

* \[ ] real user feedback verwerking;
* \[ ] UI/UX polish sprint;
* \[ ] dashboard component library;
* \[ ] advanced tutorials;
* \[ ] workspace marketplace lokaal zonder remote code;
* \[ ] full help center;
* \[ ] telemetry-free local usage analytics;
* \[ ] stability polish voor lange sessies.

