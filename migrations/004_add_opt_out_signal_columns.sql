-- 004_add_opt_out_signal_columns.sql
-- Adds GPC/opt-out signals for TDPSA and global GPC compliance tracking.

ALTER TABLE legal_consents
    ADD COLUMN IF NOT EXISTS gpc_signal BOOLEAN;

ALTER TABLE legal_consents
    ADD COLUMN IF NOT EXISTS manual_opt_out BOOLEAN;

ALTER TABLE legal_consents
    ADD COLUMN IF NOT EXISTS opt_out_effective BOOLEAN;

ALTER TABLE legal_consents
    ADD COLUMN IF NOT EXISTS opt_out_source VARCHAR(32);

ALTER TABLE legal_consents
    ADD COLUMN IF NOT EXISTS tracking_mode VARCHAR(32);

CREATE INDEX IF NOT EXISTS idx_legal_consents_opt_out_effective
    ON legal_consents (opt_out_effective);

-- Mind Bright Technologies LLC compliance note (2026):
-- These fields provide evidentiary support for TDPSA "Do Not Sell/Share"
-- and Global Privacy Control handling by recording signal source and
-- effective tracking mode at consent time.

