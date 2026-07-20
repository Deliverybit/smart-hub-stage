# Supabase staging database setup

The Scoop 52 uses Postgres for **legal consent logs** (`legal_consents` table). Local dev falls back to SQLite when `DATABASE_URL` is unset; **staging** uses Supabase project `smart-hub-stage`.

## 1. Create the Supabase project

| Field | Recommendation |
|-------|----------------|
| **Organization** | Deliverybit's Org (PRO) |
| **Project name** | `smart-hub-stage` |
| **Database password** | Generate a strong password — save in a password manager |
| **Region** | **Americas** (or closest to your Streamlit host) |
| **Compute** | Micro is fine for staging |
| **Enable Data API** | ✅ OK (app uses direct Postgres, not REST) |
| **Automatically expose new tables** | ❌ **Uncheck** |
| **Enable automatic RLS** | ✅ **Check** |

## 2. Get the connection string

1. **Connect** → **Direct** → **Session pooler** → **URI**
2. Copy the `postgresql://...` string
3. Replace `[YOUR-PASSWORD]` with your database password
4. Append `?sslmode=require` if missing

## 3. Configure secrets

**Windows:** run `.\launch.ps1` once — it copies the example file if `secrets.toml` is missing.

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

```toml
APP_ENV = "staging"
ALPHA_VANTAGE_API_KEY = "..."
SCREENER_SYMBOL_LIMIT = 1000
DATABASE_URL = "postgresql://postgres....?sslmode=require"
```

## 4. Run migrations

```bash
python admin_tools/run_migrations.py
```

## 5. Verify

- **Table Editor** → `legal_consents`, `screener_snapshots`, `schema_migrations`
- Accept Terms in the app → new row in `legal_consents`
- `python admin_tools/export_consent_logs.py --limit 5` → source **PostgreSQL**

## Production (later)

Create a **separate** Supabase project (`smart-hub-prod`), separate Streamlit deploy, and set `APP_ENV = "production"` there. Never share `DATABASE_URL` between staging and production.

## What is stored

- **Legal consent audit events** (`legal_consents`)
- **Precomputed screener snapshots** (`screener_snapshots`) — refreshed every 15 minutes by `admin_tools/screener_worker.py` so Top 10 pages load instantly

Market prices still come from Alpha Vantage; snapshots cache the processed Top 10 rows (including headlines) in Postgres.

## 6. Precomputed screener snapshots

After migrations, refresh snapshots locally:

```bash
python admin_tools/screener_worker.py
```

Or one screener:

```bash
python admin_tools/screener_worker.py --screener NYSE
```

**GitHub Actions:** workflow `.github/workflows/screener-snapshots.yml` runs every 15 minutes when repo secrets `DATABASE_URL` and `ALPHA_VANTAGE_API_KEY` are set.

Verify:

```bash
python admin_tools/test_screener_snapshots.py
```
