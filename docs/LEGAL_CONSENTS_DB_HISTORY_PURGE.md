# Legal consents SQLite database — Git history purge

**Date:** 2026-05-01  

## What was done

All Git history was rewritten with [`git-filter-repo`](https://github.com/newren/git-filter-repo) to **remove every revision of `legal_consents.db`** from the repository. The file was never appropriate to version-control: it is a **runtime append-only log** created by `legal_consent_logger.py` and may contain **PII** (for example IP addresses and user agents).

Application code was **not** changed for this purge. In particular, `legal_consent_logger.py` and SQL migrations under `migrations/` remain as-is. The database file continues to be created on disk next to that module when the app runs; it is listed in `.gitignore` so it is not committed again.

## Why it was done

- `legal_consents.db` had been committed by mistake before ignore rules and `git rm --cached` were applied.
- Storing that history would keep **recoverable copies of log data** in every clone and fork.

## Scope of exposed data (this repo)

This project was used as a **testing environment only**. The consent log that had entered Git history contained **only the maintainer’s laptop / local test traffic**—not production users or third-party data. The purge was done as **good hygiene** and to align the repo with how the consent store is meant to be handled (local or managed datastore, backups outside Git).

## Aftermath for collaborators

Commit hashes **changed** for the entire history. Anyone with an old clone must **re-clone** or reset hard to the rewritten `main` after the maintainer **force-pushes** (prefer `git push --force-with-lease`).

## Remote note

`git-filter-repo` removes the `origin` remote by default to avoid an accidental push before verifying the rewrite. The remote was re-added locally after verification; confirm with `git remote -v` before pushing.
