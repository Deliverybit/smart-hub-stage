-- 006_create_screener_snapshots.sql
-- Precomputed screener payloads for instant page loads (written by screener_worker).

CREATE TABLE IF NOT EXISTS screener_snapshots (
    screener_key TEXT PRIMARY KEY,
    payload JSONB NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS screener_snapshots_updated_at_idx
    ON screener_snapshots (updated_at DESC);

ALTER TABLE screener_snapshots ENABLE ROW LEVEL SECURITY;

REVOKE ALL ON TABLE screener_snapshots FROM anon, authenticated;
REVOKE ALL ON TABLE screener_snapshots FROM PUBLIC;

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE screener_snapshots TO postgres;
