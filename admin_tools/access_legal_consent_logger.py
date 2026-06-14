"""
Locate and optionally import legal_consent_logger from the repo root.

Works from any current working directory (uses this file's location).

Usage (PowerShell):
    python admin_tools/access_legal_consent_logger.py
    python admin_tools/access_legal_consent_logger.py --import-check

After running, copy the printed logger path and open it in your editor, or from
PowerShell:  start <path-to-legal_consent_logger.py>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGGER_PATH = ROOT / "legal_consent_logger.py"
# Same path rule as legal_consent_logger._SQLITE_PATH
DB_PATH = LOGGER_PATH.parent / "legal_consents.db"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print absolute paths to legal_consent_logger.py and legal_consents.db.",
    )
    parser.add_argument(
        "--import-check",
        action="store_true",
        help="Add repo root to sys.path and import legal_consent_logger (needs app dependencies).",
    )
    args = parser.parse_args()

    print(f"Repo root:        {ROOT}")
    print(f"Logger module:    {LOGGER_PATH}  (exists: {LOGGER_PATH.is_file()})")
    print(f"SQLite database:  {DB_PATH}  (exists: {DB_PATH.is_file()})")

    if args.import_check:
        sys.path.insert(0, str(ROOT))
        import legal_consent_logger as lcl  # noqa: PLC0415

        print("\nImport OK.")
        print(f"Module __file__:  {Path(lcl.__file__).resolve()}")
        for name in ("ensure_timezone_cookie", "log_terms_acceptance"):
            print(f"  {name!r}: {getattr(lcl, name, None)}")


if __name__ == "__main__":
    main()
