# Portfolio Policy Registry

Roadmap: 082

`src/binance_spot_bot/portfolio_policy_registry.py` stores local paper policy metadata under `data/portfolio-policies/registry.json`.

Supported operations:

- register candidate/challenger/champion paper policy metadata;
- list and load policies by ID;
- get the current champion;
- promote a paper champion with previous champion preservation;
- suspend or archive policies.

The registry rejects unsupported statuses and policies that set `live_trading_enabled=True`.
