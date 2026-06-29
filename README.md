# Smart Hub Stage

Staging environment for **The Scoop 52** — Streamlit market screener with legal consent logging to Supabase (`smart-hub-stage`).

## Environments

| Environment | Supabase project | `APP_ENV` |
|-------------|------------------|-----------|
| Local | SQLite (default) or stage DB | `local` / unset |
| **Staging** | `smart-hub-stage` | `staging` |
| Production (future) | `smart-hub-prod` | `production` |

## Run locally

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets: APP_ENV, DATABASE_URL, ALPHA_VANTAGE_API_KEY
streamlit run app.py
```

## Database setup

See [docs/SUPABASE_STAGING.md](docs/SUPABASE_STAGING.md).

```bash
python admin_tools/run_migrations.py
```

## Secrets (never commit)

- `.streamlit/secrets.toml` — local / Streamlit Cloud secrets
- `DATABASE_URL` — Supabase Session pooler URI with `?sslmode=require`
