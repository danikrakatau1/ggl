"""Persistent Chrome context. One profile dir per account, never shared."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from playwright.async_api import BrowserContext, Playwright

ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-first-run",
    "--no-default-browser-check",
    "--webrtc-ip-handling-policy=disable_non_proxied_udp",
]


async def launch(
    p: Playwright,
    profile_dir: Path,
    *,
    headless: bool = False,
    proxy: dict[str, Any] | None = None,
) -> BrowserContext:
    profile_dir.mkdir(parents=True, exist_ok=True)
    launch_kwargs = {
        "user_data_dir": str(profile_dir),
        "headless": headless,
        "locale": "en-US",
        "timezone_id": "America/Los_Angeles",
        "viewport": {"width": 1440, "height": 900},
        "proxy": proxy,
        "args": ARGS,
    }
    try:
        if sys.platform == "darwin":
            return await p.chromium.launch_persistent_context(channel="chrome", **launch_kwargs)
        else:
            return await p.chromium.launch_persistent_context(channel="chrome", **launch_kwargs)
    except Exception:
        return await p.chromium.launch_persistent_context(**launch_kwargs)
