-- 002_add_timezone_columns_to_legal_consents.sql
-- Adds per-user timezone fields for legal consent records.

ALTER TABLE legal_consents
    ADD COLUMN IF NOT EXISTS timezone_name VARCHAR(128);

ALTER TABLE legal_consents
    ADD COLUMN IF NOT EXISTS timestamp_local TIMESTAMPTZ;

