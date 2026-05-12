# Roadmap Execution CLI

Core commands:

```powershell
python -m binance_spot_bot.cli roadmap-index --json
python -m binance_spot_bot.cli roadmap-next-number --json
python -m binance_spot_bot.cli roadmap-duplicate-guard --number 090 --json
python -m binance_spot_bot.cli roadmap-validate --file "Roadmap docs/090-roadmap-developer-experience-codex-task-packs-roadmap-execution-automation.md" --json
python -m binance_spot_bot.cli roadmap-graph --json
python -m binance_spot_bot.cli codex-task-packs --roadmap 090 --json
python -m binance_spot_bot.cli pr-template --roadmap 090 --phase foundation --json
python -m binance_spot_bot.cli roadmap-completion-gate --roadmap 090 --tests-passed --check-all-passed --json
python -m binance_spot_bot.cli roadmap-evidence-export --roadmap 090 --json
```

Live trading enabled: false.
