"""
consent_api.py

FastAPI endpoint for legal click-wrap consent logging.
Run:
    uvicorn consent_api:app --host 0.0.0.0 --port 8000

Security (recommended on any network reachable from the internet):

- CONSENT_API_KEY: shared secret. By default, POST /api/v1/consent requires the
  same value in either header ``X-API-Key`` or ``Authorization: Bearer <key>``.
- CONSENT_API_ALLOW_ANON: set to "1"/"true" to allow unauthenticated requests
  (intended only for local/private-network development).
- CONSENT_API_RPM: max successful auth checks per client key per rolling minute
  (default 120). Set to 0 to disable rate limiting. Client key is derived from
  the TCP client host unless CONSENT_TRUST_PROXY is enabled.
- CONSENT_TRUST_PROXY: set to "1"/"true" only when running behind a trusted
  reverse proxy that overwrites forwarding headers. When enabled, the service
  will use the first hop in Forwarded/X-Forwarded-For/X-Real-IP to identify
  clients (for logging and rate limiting).

For TLS client certificates (mTLS), terminate at a reverse proxy and keep the
API bound to localhost or a private interface only.
"""

from __future__ import annotations

import ipaddress
import os
import secrets
import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from typing import Optional

import psycopg
from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, field_validator
from app_config import get_database_url
from vpn_detection import detect_vpn_proxy

DEFAULT_TIMEZONE = os.getenv("CONSENT_DEFAULT_TIMEZONE", "America/Chicago").strip() or "UTC"


class ConsentPayload(BaseModel):
    tos_version: str = Field(..., min_length=1, max_length=64)
    fingerprint_hash: str = Field(..., min_length=64, max_length=64)
    consent_action: str = Field(default="click_wrap_accept", min_length=1, max_length=64)
    user_agent: Optional[str] = Field(default=None, max_length=2048)
    timezone_name: Optional[str] = Field(default=None, max_length=128)
    timezone_offset: Optional[int] = Field(default=None, ge=-840, le=840)
    manual_opt_out: Optional[bool] = Field(default=None)

    @field_validator("fingerprint_hash")
    @classmethod
    def validate_fingerprint_hash(cls, value: str) -> str:
        lowered = value.lower()
        if len(lowered) != 64 or any(ch not in "0123456789abcdef" for ch in lowered):
            raise ValueError("fingerprint_hash must be a 64-char SHA-256 hex string.")
        return lowered


app = FastAPI(title="The Scoop 52 Legal Consent API", version="1.0.0")

_RL_LOCK = threading.Lock()
_RL_BUCKETS: dict[str, deque[float]] = defaultdict(deque)
_RL_LAST_SEEN: dict[str, float] = {}
_RL_MAX_CLIENTS = 10_000


def _env_truthy(name: str, default: str = "") -> bool:
    raw = os.getenv(name, default)
    return str(raw).strip().lower() in ("1", "true", "t", "yes", "y", "on")


def _trust_proxy_headers() -> bool:
    return _env_truthy("CONSENT_TRUST_PROXY", "0")


def _rate_limit_client_key(request: Request) -> str:
    """Best-effort client key for rate limits (does not raise on bad IP strings)."""
    if _trust_proxy_headers():
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            cand = _extract_ip_candidate(forwarded_for.split(",")[0])
            if cand:
                try:
                    return str(ipaddress.ip_address(cand))
                except Exception:
                    pass
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            cand = _extract_ip_candidate(real_ip)
            if cand:
                try:
                    return str(ipaddress.ip_address(cand))
                except Exception:
                    pass
    if request.client and request.client.host:
        try:
            return str(ipaddress.ip_address(request.client.host.strip()))
        except Exception:
            return request.client.host.strip() or "unknown"
    return "unknown"


def _enforce_rate_limit(request: Request) -> None:
    raw = os.getenv("CONSENT_API_RPM", "120").strip()
    try:
        rpm = int(raw)
    except ValueError:
        rpm = 120
    if rpm <= 0:
        return
    key = _rate_limit_client_key(request)
    now = time.monotonic()
    window = 60.0
    with _RL_LOCK:
        bucket = _RL_BUCKETS[key]
        cutoff = now - window
        while bucket and bucket[0] <= cutoff:
            bucket.popleft()

        _RL_LAST_SEEN[key] = now

        # Bound memory usage: cap number of unique client keys.
        if len(_RL_LAST_SEEN) > _RL_MAX_CLIENTS:
            # Evict least-recently-seen keys.
            overflow = len(_RL_LAST_SEEN) - _RL_MAX_CLIENTS
            for victim, _ in sorted(_RL_LAST_SEEN.items(), key=lambda kv: kv[1])[:overflow]:
                _RL_LAST_SEEN.pop(victim, None)
                _RL_BUCKETS.pop(victim, None)

        if len(bucket) >= rpm:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again later.",
            )
        bucket.append(now)


def _require_consent_api_key(request: Request) -> None:
    expected = os.getenv("CONSENT_API_KEY", "").strip()
    allow_anon = _env_truthy("CONSENT_API_ALLOW_ANON", "0")
    if not expected:
        if allow_anon:
            return
        raise HTTPException(
            status_code=503,
            detail="Consent API is not configured. Set CONSENT_API_KEY (or set CONSENT_API_ALLOW_ANON=1 for local dev).",
        )
    header_key = (request.headers.get("x-api-key") or "").strip()
    auth = (request.headers.get("authorization") or "").strip()
    bearer = ""
    if auth.lower().startswith("bearer "):
        bearer = auth[7:].strip()
    if secrets.compare_digest(header_key, expected) or (
        bearer and secrets.compare_digest(bearer, expected)
    ):
        return
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API key. Send X-API-Key or Authorization: Bearer.",
    )


def consent_api_guard(request: Request) -> None:
    """Rate limit first, then optional shared-secret auth."""
    _enforce_rate_limit(request)
    _require_consent_api_key(request)


def _normalize_ip(value: str) -> str:
    try:
        return str(ipaddress.ip_address(value.strip()))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid client IP.") from exc


def _extract_ip_candidate(raw_value: str) -> str:
    value = (raw_value or "").strip().strip('"').strip("'")
    if not value:
        return ""
    if value.startswith("for="):
        value = value[4:].strip()
    if value.startswith("[") and "]" in value:
        value = value[1:value.index("]")]
    if value.count(":") == 1 and "." in value:
        host_part, port_part = value.rsplit(":", 1)
        if port_part.isdigit():
            value = host_part
    return value


def _get_client_ip(request: Request) -> str:
    if _trust_proxy_headers():
        forwarded = request.headers.get("forwarded")
        if forwarded:
            first_part = forwarded.split(",")[0]
            for token in first_part.split(";"):
                token = token.strip()
                if token.lower().startswith("for="):
                    return _normalize_ip(_extract_ip_candidate(token))

        # In proxied deployments, trust the first hop in X-Forwarded-For.
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return _normalize_ip(_extract_ip_candidate(forwarded_for.split(",")[0]))

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return _normalize_ip(_extract_ip_candidate(real_ip))

        cf_ip = request.headers.get("cf-connecting-ip")
        if cf_ip:
            return _normalize_ip(_extract_ip_candidate(cf_ip))

        for key in ("true-client-ip", "x-client-ip", "x-original-forwarded-for", "x-envoy-external-address"):
            value = request.headers.get(key)
            if value:
                return _normalize_ip(_extract_ip_candidate(value))

    if request.client and request.client.host:
        return _normalize_ip(request.client.host)

    raise HTTPException(status_code=400, detail="Unable to determine client IP.")


@app.post("/api/v1/consent")
def log_legal_consent(
    payload: ConsentPayload,
    request: Request,
    _: None = Depends(consent_api_guard),
) -> dict:
    ip_address = _get_client_ip(request)
    user_agent = payload.user_agent or request.headers.get("user-agent", "unknown")
    now_utc = datetime.now(timezone.utc)
    timezone_name = (payload.timezone_name or DEFAULT_TIMEZONE).strip()
    try:
        tz = ZoneInfo(timezone_name)
    except Exception:
        timezone_name = "UTC"
        tz = ZoneInfo("UTC")
    now_local = now_utc.astimezone(tz)
    timezone_offset = payload.timezone_offset

    # Best-effort opt-out signals.
    gpc_header = (request.headers.get("sec-gpc") or "").strip()
    gpc_signal: Optional[bool] = None
    if gpc_header:
        gpc_signal = True if gpc_header == "1" else False
    dnt_header = (request.headers.get("dnt") or "").strip()
    dnt_signal: Optional[bool] = None
    if dnt_header:
        dnt_signal = True if dnt_header == "1" else False
    manual_opt_out = payload.manual_opt_out

    sources: list[str] = []
    if gpc_signal is True:
        sources.append("gpc")
    if dnt_signal is True:
        sources.append("dnt")
    if manual_opt_out is True:
        sources.append("manual")
    opt_out_effective = bool(sources)
    opt_out_source = ",".join(sources) if sources else "none"
    tracking_mode = "essential_only" if opt_out_effective else "standard"

    # Mind Bright Technologies LLC forensic note:
    # timezone_offset/timezone_name from browser can be compared with IP geography.
    # A major mismatch (e.g., Texas IP with London timezone) can indicate VPN/proxy usage.
    is_vpn, vpn_service_provider = detect_vpn_proxy(ip_address)

    sql_with_vpn = """
        INSERT INTO legal_consents (
            timestamp_utc,
            timestamp_local,
            timezone_name,
            timezone_offset,
            ip_address,
            user_agent,
            tos_version,
            fingerprint_hash,
            consent_action,
            is_vpn,
            vpn_service_provider,
            gpc_signal,
            manual_opt_out,
            opt_out_effective,
            opt_out_source,
            tracking_mode
        )
        VALUES (%s, %s, %s, %s, %s::inet, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, timestamp_utc
    """
    sql_with_timezone = """
        INSERT INTO legal_consents (
            timestamp_utc,
            timestamp_local,
            timezone_name,
            ip_address,
            user_agent,
            tos_version,
            fingerprint_hash,
            consent_action,
            gpc_signal,
            manual_opt_out,
            opt_out_effective,
            opt_out_source,
            tracking_mode
        )
        VALUES (%s, %s, %s, %s::inet, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, timestamp_utc
    """
    sql_legacy = """
        INSERT INTO legal_consents (
            timestamp_utc,
            ip_address,
            user_agent,
            tos_version,
            fingerprint_hash,
            consent_action,
            gpc_signal,
            manual_opt_out,
            opt_out_effective,
            opt_out_source,
            tracking_mode
        )
        VALUES (%s, %s::inet, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, timestamp_utc
    """

    try:
        database_url = get_database_url(required=True)
        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        sql_with_vpn,
                        (
                            now_utc,
                            now_local,
                            timezone_name,
                            timezone_offset,
                            ip_address,
                            user_agent,
                            payload.tos_version,
                            payload.fingerprint_hash,
                            payload.consent_action,
                            is_vpn,
                            vpn_service_provider,
                            gpc_signal,
                            manual_opt_out,
                            opt_out_effective,
                            opt_out_source,
                            tracking_mode,
                        ),
                    )
                except Exception:
                    try:
                        cur.execute(
                            sql_with_timezone,
                            (
                                now_utc,
                                now_local,
                                timezone_name,
                                ip_address,
                                user_agent,
                                payload.tos_version,
                                payload.fingerprint_hash,
                                payload.consent_action,
                                gpc_signal,
                                manual_opt_out,
                                opt_out_effective,
                                opt_out_source,
                                tracking_mode,
                            ),
                        )
                    except Exception:
                        cur.execute(
                            sql_legacy,
                            (
                                now_utc,
                                ip_address,
                                user_agent,
                                payload.tos_version,
                                payload.fingerprint_hash,
                                payload.consent_action,
                                gpc_signal,
                                manual_opt_out,
                                opt_out_effective,
                                opt_out_source,
                                tracking_mode,
                            ),
                        )
                created_id, created_ts = cur.fetchone()
            conn.commit()
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to persist legal consent.") from exc

    return {
        "status": "ok",
        "id": str(created_id),
        "timestamp_utc": created_ts.isoformat(),
    }

