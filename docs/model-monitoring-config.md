# Model Monitoring Config

Roadmap: 098

`model_monitoring_config.py` defines monitoring scope, drift thresholds, performance thresholds, downgrade policy and schedule policy.

The default config monitors local paper/shadow/demo aliases only and sets `live_trading_enabled=false`.
