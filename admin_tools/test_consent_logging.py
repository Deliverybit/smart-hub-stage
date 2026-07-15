#!/usr/bin/env python3
"""
Step 5 — Test legal consent logging to Supabase (or SQLite fallback).

Simulates Terms acceptance via log_terms_acceptance(), then verifies the row exists.

Usage:
    python admin_tools/test_consent_logging.py
"""

from __future__ import annotations

import sys
import uuid
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app_config import get_app_env, get_database_url  # noqa: E402
from legal_consent_logger import log_terms_acceptance  # noqa: E402


class _SessionState(dict):
    def get(self, key, default=None):  # noqa: ANN001
        return super().get(key, default)


def _mock_streamlit(consent_key: str) -> SimpleNamespace:
    headers = {
        "user-agent": "SmartHubConsentTest/1.0",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua-platform": '"Windows"',
        "cookie": "scoop_tz=America%2FChicago; scoop_tz_offset=-300",
    }
    context = SimpleNamespace(headers=headers)
    return SimpleNamespace(
        session_state=_SessionState(),
        context=context,
    )


def _count_rows(source: str, database_url: str | None, user_agent: str) -> int:
    if source == "PostgreSQL":
        import psycopg

        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(*) FROM legal_consents WHERE user_agent = %s",
                    (user_agent,),
                )
                return int(cur.fetchone()[0])

    import sqlite3

    db_path = ROOT / "legal_consents.db"
    with sqlite3.connect(db_path) as conn:
        cur = conn.execute(
            "SELECT COUNT(*) FROM legal_consents WHERE user_agent = ?",
            (user_agent,),
        )
        return int(cur.fetchone()[0])


def _fetch_latest_by_user_agent(source: str, database_url: str | None, user_agent: str) -> dict | None:
    if source == "PostgreSQL":
        import psycopg

        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id::text, consent_action, tos_version, user_agent
                    FROM legal_consents
                    WHERE user_agent = %s
                    ORDER BY timestamp_utc DESC
                    LIMIT 1
                    """,
                    (user_agent,),
                )
                row = cur.fetchone()
                if not row:
                    return None
                return {
                    "id": row[0],
                    "consent_action": row[1],
                    "tos_version": row[2],
                    "user_agent": row[3],
                }

    import sqlite3

    db_path = ROOT / "legal_consents.db"
    with sqlite3.connect(db_path) as conn:
        cur = conn.execute(
            """
            SELECT id, consent_action, tos_version, user_agent
            FROM legal_consents
            WHERE user_agent = ?
            ORDER BY timestamp_utc DESC
            LIMIT 1
            """,
            (user_agent,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "consent_action": row[1],
            "tos_version": row[2],
            "user_agent": row[3],
        }


def main() -> int:
    database_url = get_database_url()
    source = "PostgreSQL" if database_url else "SQLite"
    app_env = get_app_env()
    consent_key = f"agree_terms_test_{uuid.uuid4().hex[:8]}"

    print("Consent logging test")
    print(f"APP_ENV={app_env}  Source={source}")
    print("-" * 60)

    if source == "PostgreSQL":
        print("DATABASE_URL configured — expecting Supabase staging/prod.")
    else:
        print("DATABASE_URL not set — will use local legal_consents.db.")

    st = _mock_streamlit(consent_key)
    log_terms_acceptance(st, consent_key=consent_key)

    logged_marker = st.session_state.get(f"_legal_consent_logged::{consent_key}")
    session_marked = logged_marker is True
    print(f"1) log_terms_acceptance session marker: {'PASS' if session_marked else 'FAIL'}")

    before_count = _count_rows(source, database_url, "SmartHubConsentTest/1.0")
    log_terms_acceptance(st, consent_key=consent_key)
    after_count = _count_rows(source, database_url, "SmartHubConsentTest/1.0")
    dedupe_ok = after_count == before_count
    print(f"2) Duplicate log suppressed in session: {'PASS' if dedupe_ok else 'FAIL'}")

    row = _fetch_latest_by_user_agent(source, database_url, "SmartHubConsentTest/1.0")
    row_found = row is not None
    action_ok = row and row["consent_action"] == "click_wrap_accept"
    print(f"3) Row persisted ({source}): {'PASS' if row_found else 'FAIL'}")
    if row:
        print(f"   id={row['id']}")
        print(f"   consent_action={row['consent_action']}  tos_version={row['tos_version']}")
    print(f"4) consent_action click_wrap_accept: {'PASS' if action_ok else 'FAIL'}")

    passed = session_marked and dedupe_ok and row_found and action_ok
    print("-" * 60)
    print(f"Overall: {'PASS' if passed else 'FAIL'}")
    if passed and source == "PostgreSQL":
        print("Verify in Supabase Table Editor -> legal_consents (latest row).")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
