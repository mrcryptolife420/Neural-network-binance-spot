# Experiment Stopping Rules

Stopping rules protect the current champion during paper rollout. The evaluator can stop or continue a challenger from local experiment metrics.

Stop triggers:

- challenger max drawdown breach
- material underperformance versus champion
- too few samples
- policy violations
- watchdog alerts
- data-quality warnings
- blocked-rate or conflict-rate breach
- turnover breach
- signed endpoint usage

The output contains the action, reasons, evidence references, and `live_trading_enabled: false`.
