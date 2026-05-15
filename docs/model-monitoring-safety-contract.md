# Model Monitoring Safety Contract

Roadmap: 098

Model monitoring is local-only and may only propose or apply paper/shadow/demo alias downgrades.

Rules:
- No live trading.
- No signed order endpoints.
- No account endpoints.
- Monitoring never places orders.
- Downgrades require evidence and confirmation.
- Forbidden aliases: `champion_live`, `live_approved`, `auto_live`.
- Allowed aliases are paper/shadow/demo candidate aliases only.
- Reports and alias history are redacted.

Validation:
- `validate_model_monitoring_config` blocks live aliases.
- `model_downgrade_executor` blocks forbidden aliases and missing confirmation.
- `run_model_monitoring` computes drift, paper performance, health score and downgrade policy without execution side effects.
