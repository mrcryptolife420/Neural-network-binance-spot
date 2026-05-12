# Foundation Module PR Prompt

Implement the smallest foundation slice for the selected roadmap.

Allowed files: roadmap-specific `src/binance_spot_bot/*`, focused tests, and docs.

Forbidden files: `.env`, secrets, live trading modules unless explicitly scoped, and unrelated user data.

Run focused tests, `check-all --skip-tests`, and full pytest when scope affects shared behavior.

Live trading enabled: false.
