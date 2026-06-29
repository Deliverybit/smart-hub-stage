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

- **Table Editor** → `legal_consents`, `schema_migrations`
- Accept Terms in the app → new row in `legal_consents`
- `python admin_tools/export_consent_logs.py --limit 5` → source **PostgreSQL**

## Production (later)

Create a **separate** Supabase project (`smart-hub-prod`), separate Streamlit deploy, and set `APP_ENV = "production"` there. Never share `DATABASE_URL` between staging and production.

## What is stored

Only **legal consent audit events**. Market/screener data stays in Alpha Vantage + Streamlit cache — not in Supabase.
