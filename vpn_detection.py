"""
vpn_detection.py

Best-effort VPN/proxy detection for consent logging.
Uses ProxyCheck.io (free tier) with graceful failure behavior.
"""

from __future__ import annotations

import ipaddress
import os
from typing import Optional, Tuple

import requests


def detect_vpn_proxy(ip_address: str) -> Tuple[Optional[bool], Optional[str]]:
    """
    Returns (is_vpn, provider_name).

    Graceful failure contract:
    - If service is unavailable/rate-limited/invalid response, returns (None, None).
    - If IP is private/loopback/invalid, returns (None, None).
    """
    try:
        ip_obj = ipaddress.ip_address(ip_address)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
            return None, None
    except Exception:
        return None, None

    api_key = os.getenv("PROXYCHECK_API_KEY", "").strip()
    params = {
        "vpn": 1,
        "asn": 1,
        "risk": 1,
        "seen": 1,
        "tag": "scoop52-consent",
    }
    if api_key:
        params["key"] = api_key

    url = f"https://proxycheck.io/v2/{ip_address}"
    try:
        resp = requests.get(url, params=params, timeout=2.5)
        if not resp.ok:
            return None, None
        payload = resp.json()
        ip_data = payload.get(ip_address, {})
        if not isinstance(ip_data, dict):
            return None, None

        proxy_flag = str(ip_data.get("proxy", "")).lower()
        is_vpn = True if proxy_flag == "yes" else False if proxy_flag == "no" else None

        provider = (
            ip_data.get("provider")
            or ip_data.get("organisation")
            or ip_data.get("asn")
            or None
        )
        provider_name = str(provider)[:255] if provider else None
        return is_vpn, provider_name
    except Exception:
        return None, None

