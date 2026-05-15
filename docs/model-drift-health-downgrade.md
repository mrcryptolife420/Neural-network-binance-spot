# Model Drift, Health And Downgrade

Roadmap: 098

Monitoring signals:
- feature drift
- prediction drift
- confidence drift
- paper PnL/drawdown performance
- model health score

Downgrade action:
- allowed only for paper/shadow/demo aliases;
- requires `DOWNGRADE_PAPER_MODEL`;
- writes alias history evidence;
- never touches live aliases.
