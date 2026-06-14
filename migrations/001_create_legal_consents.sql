-- 001_create_legal_consents.sql
-- Legal consent log table for click-wrap acceptance events.
-- Target DB: PostgreSQL

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS legal_consents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp_utc TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ip_address INET NOT NULL,
    user_agent TEXT NOT NULL,
    tos_version VARCHAR(64) NOT NULL,
    fingerprint_hash CHAR(64) NOT NULL,
    consent_action VARCHAR(64) NOT NULL CHECK (consent_action IN ('click_wrap_accept'))
);

CREATE INDEX IF NOT EXISTS idx_legal_consents_timestamp_utc
    ON legal_consents (timestamp_utc DESC);

CREATE INDEX IF NOT EXISTS idx_legal_consents_tos_version
    ON legal_consents (tos_version);

CREATE INDEX IF NOT EXISTS idx_legal_consents_fingerprint_hash
    ON legal_consents (fingerprint_hash);

-- Security / legal integrity note for Mind Bright Technologies LLC:
-- Make this table append-only by prohibiting UPDATE/DELETE.
-- This preserves an immutable audit trail of recorded consents.
CREATE OR REPLACE FUNCTION prevent_legal_consents_mutation()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE EXCEPTION
        'legal_consents is append-only for legal audit integrity (Mind Bright Technologies LLC).';
END;
$$;

DROP TRIGGER IF EXISTS trg_prevent_legal_consents_update_delete ON legal_consents;
CREATE TRIGGER trg_prevent_legal_consents_update_delete
    BEFORE UPDATE OR DELETE ON legal_consents
    FOR EACH ROW
    EXECUTE FUNCTION prevent_legal_consents_mutation();
