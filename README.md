Paper/testnet-first Binance.com spot trading bot scaffold.

Core rule: the neural network is only a signal generator. A deterministic risk engine decides whether any trade intent is allowed. Live trading is disabled by default and requires explicit multi-step configuration.

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests
```

Terminal runtime:
```powershell
$env:PYTHONPATH="src"
python -m binance_spot_bot.cli run-local --mode demo --symbol BTCUSDT --steps 50
```

Visueel dashboard:
```powershell
pip install -e ".[ui]"
$env:PYTHONPATH="src"
python -m streamlit run src/binance_spot_bot/ui/streamlit_app.py -- --mode demo --symbol BTCUSDT --interval 1m
```

Windows 11 one-click start:
```powershell
.\Start Bot Dashboard.cmd
```

This starts Streamlit locally, chooses a free port, opens the default browser, and forces live trading off.

`demo` is de veiligste eerste start: geen API keys, geen internet nodig, alleen synthetische replay-data.

- `disabled`: no execution.
- `paper`: simulated fills only.
- `testnet`: Binance Spot Testnet orderflow only.
- `live`: blocked unless all live-readiness guardrails pass.

Never put real API keys in the repository. Use environment variables or a secret manager.
The dashboard supports session-only demo/testnet key entry. Keys are masked, never stored in repo files, and live mode is not selectable.

Meer details: [docs/local-dashboard.md](docs/local-dashboard.md).
