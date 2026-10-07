CREATE TABLE IF NOT EXISTS monitor_users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    display_name VARCHAR(120) NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS request_events (
    id BIGSERIAL PRIMARY KEY,
    service VARCHAR(80) NOT NULL DEFAULT 'general',
    method VARCHAR(16) NOT NULL,
    path TEXT NOT NULL,
    status INTEGER NOT NULL,
    duration_ms DOUBLE PRECISION,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_request_events_path
    ON request_events (path);

CREATE INDEX IF NOT EXISTS idx_request_events_status
    ON request_events (status);

CREATE TABLE IF NOT EXISTS observation_notes (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT '확인 전',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT observation_notes_status_check
        CHECK (status IN ('확인 전', '확인 중', '완료'))
);
