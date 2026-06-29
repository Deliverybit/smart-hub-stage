"""
Backend-only consent log export tool.

Usage (PowerShell):
    python admin_tools/export_consent_logs.py --limit 5000 --out consent_logs.csv
    python admin_tools/export_consent_logs.py --start "2026-03-15" --end "2026-03-15 23:59:59"

If DATABASE_URL is set, exports from PostgreSQL.
Otherwise exports from local SQLite file legal_consents.db.
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
SQLITE_PATH = ROOT / "legal_consents.db"


def parse_datetime_arg(
    raw: str | None,
    tz_name: str,
    is_end: bool = False,
) -> str | None:
    if not raw:
        return None
    value = raw.strip()
    local_tz = ZoneInfo(tz_name)
    dt: datetime | None = None

    # First attempt flexible ISO parsing.
    try:
        if len(value) == 10:
            dt = datetime.fromisoformat(value)
            if is_end:
                dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
            else:
                dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        dt = None

    # Fallback formats for typed CLI input.
    if dt is None:
        fmts = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y %H:%M",
            "%m/%d/%Y",
        ]
        for fmt in fmts:
            try:
                dt = datetime.strptime(value, fmt)
                if fmt in ("%m/%d/%Y",) and is_end:
                    dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
                elif fmt in ("%m/%d/%Y",) and not is_end:
                    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
                break
            except Exception:
                continue

    if dt is None:
        raise ValueError(
            f"Invalid datetime '{raw}'. Use YYYY-MM-DD, MM/DD/YYYY, or ISO/24h datetime."
        )

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=local_tz)
    return dt.astimezone(timezone.utc).isoformat()


def load_from_postgres(
    database_url: str,
    limit: int,
    start_utc: str | None = None,
    end_utc: str | None = None,
) -> pd.DataFrame:
    import psycopg

    filters: list[str] = []
    params: list[object] = []
    if start_utc:
        filters.append("timestamp_utc >= %s::timestamptz")
        params.append(start_utc)
    if end_utc:
        filters.append("timestamp_utc <= %s::timestamptz")
        params.append(end_utc)
    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

    with psycopg.connect(database_url) as conn:
        try:
            query = """
                SELECT
                    id,
                    timestamp_utc,
                    timestamp_local,
                    timezone_name,
                    timezone_offset,
                    ip_address::text AS ip_address,
                    user_agent,
                    tos_version,
                    fingerprint_hash,
                    consent_action,
                    is_vpn,
                    vpn_service_provider
                FROM legal_consents
                {where_clause}
                ORDER BY timestamp_utc DESC
                LIMIT %s
            """.format(where_clause=where_clause)
            return pd.read_sql(query, conn, params=tuple(params + [limit]))
        except Exception:
            legacy = """
                SELECT
                    id,
                    timestamp_utc,
                    ip_address::text AS ip_address,
                    user_agent,
                    tos_version,
                    fingerprint_hash,
                    consent_action
                FROM legal_consents
                {where_clause}
                ORDER BY timestamp_utc DESC
                LIMIT %s
            """.format(where_clause=where_clause)
            return pd.read_sql(legacy, conn, params=tuple(params + [limit]))


def load_from_sqlite(
    limit: int,
    start_utc: str | None = None,
    end_utc: str | None = None,
) -> pd.DataFrame:
    if not SQLITE_PATH.exists():
        raise FileNotFoundError(f"SQLite file not found: {SQLITE_PATH}")
    with sqlite3.connect(SQLITE_PATH) as conn:
        cols = {row[1] for row in conn.execute("PRAGMA table_info(legal_consents)").fetchall()}
        sqlite_filters: list[str] = []
        sqlite_params: list[object] = []
        if start_utc:
            sqlite_filters.append("datetime(timestamp_utc) >= datetime(?)")
            sqlite_params.append(start_utc)
        if end_utc:
            sqlite_filters.append("datetime(timestamp_utc) <= datetime(?)")
            sqlite_params.append(end_utc)
        where_clause = f"WHERE {' AND '.join(sqlite_filters)}" if sqlite_filters else ""
        if "timestamp_local" in cols and "timezone_name" in cols:
            query = """
                SELECT
                    id,
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
                    vpn_service_provider
                FROM legal_consents
                {where_clause}
                ORDER BY timestamp_utc DESC
                LIMIT ?
            """.format(where_clause=where_clause)
        else:
            query = """
                SELECT
                    id,
                    timestamp_utc,
                    ip_address,
                    user_agent,
                    tos_version,
                    fingerprint_hash,
                    consent_action
                FROM legal_consents
                {where_clause}
                ORDER BY timestamp_utc DESC
                LIMIT ?
            """.format(where_clause=where_clause)
        return pd.read_sql_query(query, conn, params=tuple(sqlite_params + [limit]))


def main() -> None:
    parser = argparse.ArgumentParser(description="Export legal consent logs to CSV.")
    parser.add_argument("--limit", type=int, default=5000, help="Max rows to export.")
    parser.add_argument("--out", type=str, default="consent_logs_export.csv", help="Output CSV filename.")
    parser.add_argument(
        "--start",
        type=str,
        default=None,
        help='Start datetime (inclusive). Example: "2026-03-15" or "2026-03-15 00:00:00".',
    )
    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help='End datetime (inclusive). Example: "2026-03-15" or "2026-03-15 23:59:59".',
    )
    parser.add_argument(
        "--timezone",
        type=str,
        default=os.getenv("CONSENT_DEFAULT_TIMEZONE", "America/Chicago"),
        help='Timezone for naive --start/--end input. Example: "America/Chicago".',
    )
    args = parser.parse_args()
    try:
        ZoneInfo(args.timezone)
    except Exception:
        print(
            f"ERROR: Invalid timezone '{args.timezone}'. Example: --timezone \"America/Chicago\"",
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        start_utc = parse_datetime_arg(args.start, args.timezone, is_end=False)
        end_utc = parse_datetime_arg(args.end, args.timezone, is_end=True)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print(
            "Examples:\n"
            "  --start \"2026-03-15\" --end \"2026-03-15\"\n"
            "  --start \"03/15/2026 18:00\" --end \"03/15/2026 23:59\"",
            file=sys.stderr,
        )
        sys.exit(2)

    from app_config import get_database_url

    db_url = get_database_url()
    if db_url:
        df = load_from_postgres(
            db_url,
            args.limit,
            start_utc=start_utc,
            end_utc=end_utc,
        )
        source = "PostgreSQL"
    else:
        df = load_from_sqlite(
            args.limit,
            start_utc=start_utc,
            end_utc=end_utc,
        )
        source = "SQLite"

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

    date_range_note = ""
    if start_utc or end_utc:
        date_range_note = (
            f" | input_tz: {args.timezone}"
            f" | range_utc: {start_utc or '-'} -> {end_utc or '-'}"
        )
    print(f"Exported {len(df)} consent rows from {source} to: {out_path}{date_range_note}")


if __name__ == "__main__":
    main()

