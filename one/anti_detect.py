"""
Advanced Anti-Detection Module for SheerID API Requests.

Features:
- Dynamic & Randomized Browser Impersonation (Chrome, Edge, Safari).
- Perfectly matched User-Agent and sec-ch-ua headers.
- Advanced "human-like" delays using Gamma distribution.
- Enhanced, more unique device fingerprinting.
- Robust proxy support for IP rotation.
- NewRelic tracking headers to mimic JS agent.
"""

import os
import random
import hashlib
import time
import uuid
import base64
import json
import logging

logger = logging.getLogger(__name__)

# ===================== PROXY CONFIG =====================
# To use, set PROXY_URL in your .env file.
# Format: host:port:user:pass or http://user:pass@host:port
# For multiple, separate with |: proxy1|proxy2
PROXY_URL = os.environ.get("PROXY_URL", "" )

def get_random_proxy() -> str | None:
    """Picks a random proxy from the PROXY_URL environment variable."""
    if not PROXY_URL:
        return None
    proxies = [p.strip() for p in PROXY_URL.split("|") if p.strip()]
    return random.choice(proxies) if proxies else None

# ===================== DYNAMIC BROWSER PROFILES =====================
# SOLUTION: Instead of a static profile, we create a list of complete, consistent browser profiles.
# The bot will randomly pick one of these for each verification attempt.
BROWSER_PROFILES = [
    {
        "impersonate": "chrome131",
        "platform": '"Windows"',
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec_ch_ua": '"Chromium";v="131", "Google Chrome";v="131", "Not_A Brand";v="24"',
    },
    {
        "impersonate": "chrome131",
        "platform": '"macOS"',
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec_ch_ua": '"Chromium";v="131", "Google Chrome";v="131", "Not_A Brand";v="24"',
    },
    {
        "impersonate": "edge131",
        "platform": '"Windows"',
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.2259.170",
        "sec_ch_ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    },
    {
        "impersonate": "chrome124",
        "platform": '"Windows"',
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "sec_ch_ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    },
    {
        "impersonate": "safari17_2",
        "platform": '"macOS"',
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
        "sec_ch_ua": None, # Safari doesn't send sec-ch-ua
    },
]

LANGUAGES = ["en-US,en;q=0.9", "en-GB,en;q=0.9,en-US;q=0.8", "en-CA,en;q=0.9,en;q=0.8"]
RESOLUTIONS = ["1920x1080", "1536x864", "1440x900", "2560x1440", "1600x900"]

# ===================== FINGERPRINTING =====================
def generate_fingerprint() -> str:
    """Generates a more realistic and randomized browser fingerprint hash."""
    components = [
        str(int(time.time() * 1000)), str(random.random()),
        random.choice(RESOLUTIONS), str(random.choice([-8, -7, -6, -5, -4])),
        random.choice(LANGUAGES).split(",")[0],
        random.choice(["Win32", "MacIntel", "Linux x86_64"]),
        random.choice(["Google Inc.", "Apple Computer, Inc.", ""]), # vendor
        str(2**random.randint(1, 5)),  # CPU cores (2, 4, 8, 16, 32)
        str(2**random.randint(2, 6)),  # device memory (4, 8, 16, 32, 64)
        str(random.randint(0, 1)), str(uuid.uuid4()),
    ]
    return hashlib.md5("|".join(components).encode()).hexdigest()

# ===================== NEWRELIC HEADERS =====================
def _newrelic_headers() -> dict:
    """Generates NewRelic tracking headers required by SheerID."""
    trace_id = uuid.uuid4().hex
    span_id = uuid.uuid4().hex[:16]
    ts = int(time.time() * 1000)
    payload = {
        "v": [0, 1],
        "d": {"ty": "Browser", "ac": "364029", "ap": "134291347", "id": span_id, "tr": trace_id, "ti": ts},
    }
    return {
        "newrelic": base64.b64encode(json.dumps(payload).encode()).decode(),
        "traceparent": f"00-{trace_id}-{span_id}-01",
        "tracestate": f"364029@nr=0-1-364029-134291347-{span_id}----{ts}",
    }

# ===================== HEADERS =====================
def get_sheerid_headers(profile: dict) -> dict:
    """Generates full, consistent browser-like headers for a given profile."""
    lang = random.choice(LANGUAGES)
    nr = _newrelic_headers()
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": lang,
        "cache-control": "no-cache", "pragma": "no-cache",
        "content-type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin",
        "user-agent": profile["user_agent"],
        "clientversion": "2.158.0", "clientname": "jslib",
        "origin": "https://services.sheerid.com",
        "referer": "https://services.sheerid.com/",
        **nr,
    }
    if profile["sec_ch_ua"]:
        headers["sec-ch-ua"] = profile["sec_ch_ua"]
        headers["sec-ch-ua-platform"] = profile["platform"]
    return headers

# ===================== DELAYS =====================
def human_delay(min_ms: int = 400, max_ms: int = 1500 ):
    """Sleeps with a more human-like timing distribution."""
    try:
        import numpy as np
        # Use a gamma distribution for more realistic, non-uniform delays
        shape, scale = 2.0, (max_ms - min_ms) / 4000.0
        delay = min_ms / 1000.0 + np.random.gamma(shape, scale)
        time.sleep(min(delay, max_ms / 1000.0))
    except ImportError:
        time.sleep(random.uniform(min_ms / 1000.0, max_ms / 1000.0))

# ===================== SESSION CREATION =====================
def _format_proxy(proxy: str) -> str | None:
    """Normalizes various proxy formats to a standard http://... URL."""
    if not proxy: return None
    proxy = proxy.strip( )
    if "://" in proxy: return proxy
    parts = proxy.split(":")
    if len(parts) == 2: return f"http://{parts[0]}:{parts[1]}"
    if len(parts ) == 4: return f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
    return f"http://{proxy}" if "@" in proxy else None

def create_session(proxy: str = None ):
    """Creates an HTTP session with the best available library and a random browser profile."""
    proxy_url = _format_proxy(proxy or get_random_proxy())
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    if proxy_url: logger.info(f"🔒 Proxy configured: {proxy_url[:35]}..." )

    profile = random.choice(BROWSER_PROFILES)
    impersonate_version = profile["impersonate"]

    try:
        from curl_cffi.requests import Session
        sess = Session(proxies=proxies, impersonate=impersonate_version, timeout=30)
        logger.info(f"✅ Anti-detect: curl_cffi + {impersonate_version} TLS impersonation")
        return sess, "curl_cffi", profile
    except (ImportError, Exception) as e:
        if isinstance(e, ImportError):
            logger.warning("❌ curl_cffi not installed — TLS fingerprint is detectable! Install: pip install curl_cffi")
        else:
            logger.warning(f"curl_cffi impersonation failed for {impersonate_version}, falling back. Error: {e}")

    try:
        import httpx
        client_proxies = proxies.get("http" ) if proxies else None
        sess = httpx.Client(timeout=30, proxies=client_proxies )
        logger.warning("⚠️ Anti-detect: httpx (no TLS spoofing, higher detection risk )")
        return sess, "httpx", profile
    except ImportError:
        import requests
        sess = requests.Session( )
        if proxies: sess.proxies = proxies
        logger.error("❌ Anti-detect: requests (VERY HIGH detection risk)")
        return sess, "requests", profile

# ===================== SESSION WARMUP =====================
def warm_session(session, profile: dict, program_id: str = None):
    """Performs pre-requests to simulate a real browser loading the page."""
    base = "https://services.sheerid.com"
    hdrs = get_sheerid_headers(profile )
    try:
        session.get(f"{base}/rest/v2/config", headers=hdrs, timeout=10)
        human_delay(500, 1000)
        if program_id:
            session.get(f"{base}/rest/v2/program/{program_id}", headers=hdrs, timeout=10)
            human_delay(300, 700)
        session.get(f"{base}/rest/v2/organization/search", params={"country": "US", "term": ""}, headers=hdrs, timeout=10)
    except Exception as e:
        logger.warning(f"Session warmup failed: {e}")

