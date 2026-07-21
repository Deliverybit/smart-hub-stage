#!/usr/bin/env python3
"""Smoke test for DATABASE_URL normalization."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app_config import get_database_url  # noqa: E402


def main() -> int:
    os.environ["DATABASE_URL"] = '"postgresql://user:pass@host:5432/db?sslmode=require"'
    url = get_database_url(required=True)
    assert url == "postgresql://user:pass@host:5432/db?sslmode=require", url
    print("PASS: quote stripping")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
