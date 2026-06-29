-- 005_supabase_lockdown_legal_consents.sql
-- Staging/production hardening for Supabase: keep legal_consents server-side only.
-- The Streamlit app and consent_api connect with the postgres role (DATABASE_URL),
-- which bypasses RLS. anon/authenticated must not read consent PII via the Data API.

ALTER TABLE legal_consents ENABLE ROW LEVEL SECURITY;

REVOKE ALL ON TABLE legal_consents FROM anon, authenticated;
REVOKE ALL ON TABLE legal_consents FROM PUBLIC;

GRANT SELECT, INSERT ON TABLE legal_consents TO postgres;
