from __future__ import annotations

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Any
from urllib.request import urlopen

from .dashboard_evidence import dashboard_checks_dir, utc_timestamp
from .redaction import redact_payload

REQUIRED_MARKERS = (
    "Neural Network Binance Spot Bot",
    "LIVE TRADING DISABLED",
    "Overview",
    "Demo Spot Trading",
    "Demo Pilot",
)
ERROR_MARKERS = (
    "StreamlitDuplicateElementId",
    "Traceback",
    "ModuleNotFoundError",
    "StreamlitAPIException",
    "Uncaught app exception",
)
SCREENSHOT_TABS = ("Overview", "Demo Spot Trading", "Demo Pilot", "Logs & Security")


def analyze_dashboard_text(text: str) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    for marker in REQUIRED_MARKERS:
        checks.append(
            {
                "name": f"marker:{marker}",
                "status": "ok" if marker in text else "failed",
                "message": "visible" if marker in text else "missing",
            }
        )
    for marker in ERROR_MARKERS:
        checks.append(
            {
                "name": f"absent:{marker}",
                "status": "failed" if marker in text else "ok",
                "message": "present" if marker in text else "absent",
            }
        )
    return checks


def run_dashboard_browser_smoke(
    url: str,
    data_dir: Path,
    *,
    seconds: int = 15,
    update_baseline: bool = False,
) -> dict[str, Any]:
    subprocess_probe = _asyncio_subprocess_probe()
    if subprocess_probe:
        payload = _run_http_smoke(url, data_dir, seconds=seconds, reason=subprocess_probe)
        out = dashboard_checks_dir(data_dir) / "browser-smoke.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
        return {"path": str(out), **payload}
    try:
        payload = _run_playwright_smoke(url, data_dir, seconds=seconds, update_baseline=update_baseline)
    except (ImportError, PermissionError) as exc:
        payload = _run_http_smoke(url, data_dir, seconds=seconds, reason=str(exc))
    except Exception as exc:
        payload = _payload(
            url,
            "playwright",
            [{"name": "browser:playwright", "status": "failed", "message": str(exc)}],
            {},
            seconds,
        )
    out = dashboard_checks_dir(data_dir) / "browser-smoke.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    return {"path": str(out), **payload}


def _asyncio_subprocess_probe() -> str:
    async def _probe() -> str:
        try:
            process = await asyncio.create_subprocess_exec(
                sys.executable,
                "-c",
                "pass",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await process.communicate()
            return ""
        except PermissionError as exc:
            return str(exc)
        except Exception:
            return ""

    try:
        return asyncio.run(_probe())
    except RuntimeError:
        return ""


def _run_playwright_smoke(url: str, data_dir: Path, *, seconds: int, update_baseline: bool) -> dict[str, Any]:
    from playwright.sync_api import sync_playwright

    screenshot_dir = dashboard_checks_dir(data_dir) / "screenshots"
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    screenshots: dict[str, str] = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1100})
        page.goto(url, wait_until="networkidle", timeout=max(5, seconds) * 1000)
        page.wait_for_timeout(1000)
        text = page.locator("body").inner_text(timeout=max(5, seconds) * 1000)
        title = page.title()
        checks = analyze_dashboard_text(f"{title}\n{text}")
        for tab in SCREENSHOT_TABS:
            try:
                page.get_by_role("tab", name=tab).click(timeout=3000)
                page.wait_for_timeout(700)
            except Exception:
                pass
            path = screenshot_dir / f"{_slug(tab)}.png"
            page.screenshot(path=str(path), full_page=True)
            screenshots[tab] = str(path)
        browser.close()
    if update_baseline:
        baseline_dir = dashboard_checks_dir(data_dir) / "baselines"
        baseline_dir.mkdir(parents=True, exist_ok=True)
        for tab, src in screenshots.items():
            Path(src).replace(baseline_dir / f"{_slug(tab)}.png")
            screenshots[tab] = str(baseline_dir / f"{_slug(tab)}.png")
    return _payload(url, "playwright", checks, screenshots, seconds)


def _run_http_smoke(url: str, data_dir: Path, *, seconds: int, reason: str) -> dict[str, Any]:
    deadline = time.time() + max(1, seconds)
    body = ""
    last_error = ""
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=2) as response:
                body = response.read().decode("utf-8", errors="replace")
            break
        except Exception as exc:
            last_error = str(exc)
            time.sleep(0.5)
    checks = [
        {
            "name": "http:reachable",
            "status": "ok" if body else "failed",
            "message": "response body received" if body else last_error or "empty",
        }
    ]
    for marker in ERROR_MARKERS:
        checks.append(
            {
                "name": f"absent:{marker}",
                "status": "failed" if marker in body else "ok",
                "message": "present" if marker in body else "absent",
            }
        )
    checks.append({"name": "browser:playwright", "status": "skipped", "message": reason})
    if not body:
        checks.append({"name": "http:body", "status": "failed", "message": last_error or "empty"})
    return _payload(url, "http-fallback", checks, {}, seconds)


def _payload(
    url: str,
    mode: str,
    checks: list[dict[str, str]],
    screenshots: dict[str, str],
    seconds: int,
) -> dict[str, Any]:
    status = "ok" if checks and all(check["status"] in {"ok", "skipped"} for check in checks) else "failed"
    return redact_payload(
        {
            "timestamp": utc_timestamp(),
            "status": status,
            "url": url,
            "browser_mode": mode,
            "seconds": seconds,
            "checks": checks,
            "screenshots": screenshots,
            "live_trading_enabled": False,
        }
    )


def _slug(value: str) -> str:
    return value.lower().replace("&", "and").replace(" ", "-")
