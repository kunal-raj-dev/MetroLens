-- ==============================================================================
-- NIRIKSHAK DATABASE INITIALIZATION SCHEMA (POSTGRESQL 16)
-- Conforms to rules/schema/evidence.schema.json and canonical shared contracts
-- ==============================================================================

CREATE TABLE IF NOT EXISTS inspections (
    inspection_id VARCHAR(64) PRIMARY KEY,
    status VARCHAR(32) NOT NULL DEFAULT 'RECEIVED',
    image_sha256 CHAR(64) NOT NULL,
    overall_verdict VARCHAR(32) NOT NULL DEFAULT 'INCONCLUSIVE',
    quality_gate_passed BOOLEAN NOT NULL DEFAULT FALSE,
    calibration_status VARCHAR(32) NOT NULL DEFAULT 'UNCALIBRATED',
    commodity_category VARCHAR(64),
    officer_id VARCHAR(64),
    device_id VARCHAR(64),
    dossier_pdf_path TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_inspections_image_sha256 ON inspections(image_sha256);
CREATE INDEX IF NOT EXISTS idx_inspections_created_at ON inspections(created_at);
CREATE INDEX IF NOT EXISTS idx_inspections_status ON inspections(status);

CREATE TABLE IF NOT EXISTS declarations (
    declaration_id BIGSERIAL PRIMARY KEY,
    inspection_id VARCHAR(64) NOT NULL REFERENCES inspections(inspection_id) ON DELETE CASCADE,
    field_name VARCHAR(64) NOT NULL,
    raw_text TEXT NOT NULL,
    normalized_value JSONB,
    confidence NUMERIC(4, 3) NOT NULL,
    is_mandatory BOOLEAN NOT NULL DEFAULT TRUE,
    is_present BOOLEAN NOT NULL DEFAULT TRUE,
    bounding_box JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_declarations_inspection_id ON declarations(inspection_id);
CREATE INDEX IF NOT EXISTS idx_declarations_field_name ON declarations(field_name);

CREATE TABLE IF NOT EXISTS measurements (
    measurement_id BIGSERIAL PRIMARY KEY,
    inspection_id VARCHAR(64) NOT NULL REFERENCES inspections(inspection_id) ON DELETE CASCADE,
    feature_name VARCHAR(64) NOT NULL,
    measured_pixels NUMERIC(10, 3) NOT NULL,
    scale_factor_mm_per_pixel NUMERIC(10, 6),
    measured_mm NUMERIC(10, 3),
    uncertainty_mm NUMERIC(10, 3),
    calibration_status VARCHAR(32) NOT NULL DEFAULT 'UNCALIBRATED',
    bounding_box JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_measurements_inspection_id ON measurements(inspection_id);

CREATE TABLE IF NOT EXISTS rule_evaluations (
    evaluation_id BIGSERIAL PRIMARY KEY,
    inspection_id VARCHAR(64) NOT NULL REFERENCES inspections(inspection_id) ON DELETE CASCADE,
    rule_id VARCHAR(64) NOT NULL,
    rule_title TEXT NOT NULL,
    verdict VARCHAR(32) NOT NULL,
    statutory_reference VARCHAR(128) NOT NULL,
    observed_summary TEXT NOT NULL,
    required_summary TEXT NOT NULL,
    uncertainty_flag BOOLEAN NOT NULL DEFAULT FALSE,
    evaluation_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_rule_evaluations_inspection_id ON rule_evaluations(inspection_id);
CREATE INDEX IF NOT EXISTS idx_rule_evaluations_rule_id ON rule_evaluations(rule_id);
CREATE INDEX IF NOT EXISTS idx_rule_evaluations_verdict ON rule_evaluations(verdict);

CREATE TABLE IF NOT EXISTS evidence_items (
    evidence_id VARCHAR(64) PRIMARY KEY,
    inspection_id VARCHAR(64) NOT NULL REFERENCES inspections(inspection_id) ON DELETE CASCADE,
    image_sha256 CHAR(64) NOT NULL,
    panel_name VARCHAR(64) NOT NULL DEFAULT 'PRINCIPAL_DISPLAY_PANEL',
    bounding_box JSONB NOT NULL,
    calibration_status VARCHAR(32) NOT NULL,
    physical_scale_mm_per_pixel NUMERIC(10, 6),
    observed_value JSONB NOT NULL,
    operator_annotation JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_evidence_items_inspection_id ON evidence_items(inspection_id);
CREATE INDEX IF NOT EXISTS idx_evidence_items_image_sha256 ON evidence_items(image_sha256);

CREATE TABLE IF NOT EXISTS audit_log (
    log_id BIGSERIAL PRIMARY KEY,
    inspection_id VARCHAR(64) REFERENCES inspections(inspection_id) ON DELETE SET NULL,
    event_type VARCHAR(64) NOT NULL,
    actor_id VARCHAR(64) NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_log_inspection_id ON audit_log(inspection_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON audit_log(created_at);
