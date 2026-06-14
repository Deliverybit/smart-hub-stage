-- 003_add_vpn_and_timezone_offset_to_legal_consents.sql
-- Adds VPN/proxy flags and timezone offset for legal consent forensics.

ALTER TABLE legal_consents
    ADD COLUMN IF NOT EXISTS timezone_offset INTEGER;

ALTER TABLE legal_consents
    ADD COLUMN IF NOT EXISTS is_vpn BOOLEAN;

ALTER TABLE legal_consents
    ADD COLUMN IF NOT EXISTS vpn_service_provider VARCHAR(255);

CREATE INDEX IF NOT EXISTS idx_legal_consents_is_vpn
    ON legal_consents (is_vpn);

-- Mind Bright Technologies LLC forensic note:
-- A mismatch between browser timezone_offset/timezone_name and IP geography
-- (for example, Texas IP + London timezone) can indicate VPN/proxy masking.
-- Keep this data append-only for legal defensibility.

