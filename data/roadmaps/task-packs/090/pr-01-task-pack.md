# Developer Experience, Codex Task Packs \& Roadmap Execution Automation - foundation

Roadmap: 090 - Developer Experience, Codex Task Packs \& Roadmap Execution Automation
Goal: Implement and validate the foundation slice without rebuilding existing infrastructure.

Allowed files:
- src/binance_spot_bot/roadmap_index.py
- src/binance_spot_bot/roadmap_duplicate_guard.py

Forbidden files:
- .env
- *.pem
- data/secrets/*
- live_trading/*

Validation:
- `python -m pytest -q`
- `python -m binance_spot_bot.cli dashboard-smoke --seconds 1`

Safety:
- local-only roadmap execution
- live_trading_enabled must remain false
- no signed Binance endpoints
- no order or account endpoints
- no API keys in files, logs, reports, or task packs
- Live trading enabled: false
