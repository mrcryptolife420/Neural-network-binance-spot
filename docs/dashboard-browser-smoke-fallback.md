# Dashboard Browser Smoke Fallback

Roadmap: 094

On Windows, Playwright can be blocked by subprocess pipe permissions. The browser smoke now probes asyncio subprocess support first. If the probe fails, it uses HTTP fallback.

HTTP fallback validates:
- dashboard URL is reachable;
- common Streamlit exception markers are absent;
- Playwright is reported as skipped, not failed.

This keeps local validation useful while preserving full Playwright coverage on machines where browser subprocesses are allowed.
