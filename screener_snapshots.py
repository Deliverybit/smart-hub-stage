"""Persist and load precomputed screener snapshots from Postgres."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from app_config import ALPHAVANTAGE_CACHE_TIMEOUT, get_database_url


def snapshot_max_age_seconds() -> int:
    return ALPHAVANTAGE_CACHE_TIMEOUT


def fetch_snapshot(screener_key: str) -> dict[str, Any] | None:
    """Load a snapshot payload for ``screener_key``, or None if missing."""
    database_url = get_database_url()
    if not database_url:
        return None

    import psycopg

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT payload, updated_at
                FROM screener_snapshots
                WHERE screener_key = %s
                """,
                (screener_key,),
            )
            row = cur.fetchone()
            if not row:
                return None

            payload = row[0]
            updated_at = row[1]
            if isinstance(payload, str):
                payload = json.loads(payload)
            if not isinstance(payload, dict):
                return None

            if updated_at is not None:
                payload.setdefault(
                    "updated_at",
                    updated_at.astimezone(timezone.utc).isoformat(),
                )
            payload.setdefault("screener_key", screener_key)
            return payload


def save_snapshot(screener_key: str, payload: dict[str, Any]) -> None:
    """Upsert a snapshot payload for ``screener_key``."""
    database_url = get_database_url(required=True)
    payload = dict(payload)
    payload["screener_key"] = screener_key
    payload.setdefault("updated_at", datetime.now(timezone.utc).isoformat())

    import psycopg
    from psycopg.types.json import Json

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO screener_snapshots (screener_key, payload, updated_at)
                VALUES (%s, %s, NOW())
                ON CONFLICT (screener_key) DO UPDATE
                SET payload = EXCLUDED.payload,
                    updated_at = NOW()
                """,
                (screener_key, Json(payload)),
            )
        conn.commit()


def snapshot_age_seconds(payload: dict[str, Any]) -> float | None:
    raw = payload.get("updated_at")
    if not raw:
        return None
    try:
        updated = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        return None
    if updated.tzinfo is None:
        updated = updated.replace(tzinfo=timezone.utc)
    return max(0.0, (datetime.now(timezone.utc) - updated.astimezone(timezone.utc)).total_seconds())


def snapshot_is_fresh(payload: dict[str, Any], *, max_age: int | None = None) -> bool:
    age_limit = snapshot_max_age_seconds() if max_age is None else max_age
    age = snapshot_age_seconds(payload)
    return age is not None and age <= age_limit
