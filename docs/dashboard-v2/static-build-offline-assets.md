# Static Build And Offline Assets

Run `python -m binance_spot_bot.cli dashboard-v2-static-verify --json`.

The verifier accepts a missing build as a warning during development, but blocks external CDN or remote font references. Release packaging can require the static build.
