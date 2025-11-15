-- Initialize database schema for Intelligent Development Platform

-- Table for storing code commits
CREATE TABLE IF NOT EXISTS commits (
    id SERIAL PRIMARY KEY,
    commit_hash VARCHAR(255) UNIQUE NOT NULL,
    repository VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    message TEXT,
    timestamp TIMESTAMP NOT NULL,
    files_changed JSONB,
    lines_added INTEGER,
    lines_deleted INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_commits_timestamp ON commits(timestamp);
CREATE INDEX idx_commits_repository ON commits(repository);

-- Table for storing breaking change predictions
CREATE TABLE IF NOT EXISTS breaking_changes (
    id SERIAL PRIMARY KEY,
    commit_hash VARCHAR(255) REFERENCES commits(commit_hash),
    prediction_confidence FLOAT,
    predicted_impact TEXT,
    reason TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- Table for storing performance metrics
CREATE TABLE IF NOT EXISTS performance_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(255) NOT NULL,
    metric_value FLOAT NOT NULL,
    labels JSONB,
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_performance_metrics_timestamp ON performance_metrics(timestamp);
CREATE INDEX idx_performance_metrics_name ON performance_metrics(metric_name);

-- Table for storing log patterns
CREATE TABLE IF NOT EXISTS log_patterns (
    id SERIAL PRIMARY KEY,
    pattern TEXT NOT NULL,
    severity VARCHAR(50),
    frequency INTEGER DEFAULT 1,
    first_seen TIMESTAMP NOT NULL,
    last_seen TIMESTAMP NOT NULL,
    is_anomaly BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing traces
CREATE TABLE IF NOT EXISTS traces_analysis (
    id SERIAL PRIMARY KEY,
    trace_id VARCHAR(255) UNIQUE NOT NULL,
    service_name VARCHAR(255),
    operation_name VARCHAR(255),
    duration_ms BIGINT,
    error BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_traces_timestamp ON traces_analysis(timestamp);
CREATE INDEX idx_traces_service ON traces_analysis(service_name);

-- Table for storing AI model predictions
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    prediction_type VARCHAR(100) NOT NULL,
    input_data JSONB,
    prediction_result JSONB,
    confidence_score FLOAT,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing optimization recommendations
CREATE TABLE IF NOT EXISTS optimization_recommendations (
    id SERIAL PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    severity VARCHAR(50),
    estimated_impact FLOAT,
    auto_fixable BOOLEAN DEFAULT FALSE,
    fix_applied BOOLEAN DEFAULT FALSE,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    applied_at TIMESTAMP
);

-- Table for storing self-healing actions
CREATE TABLE IF NOT EXISTS healing_actions (
    id SERIAL PRIMARY KEY,
    trigger_event JSONB,
    action_type VARCHAR(100) NOT NULL,
    action_details JSONB,
    status VARCHAR(50) DEFAULT 'pending',
    result JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    executed_at TIMESTAMP
);

-- Table for storing training data
CREATE TABLE IF NOT EXISTS training_data (
    id SERIAL PRIMARY KEY,
    data_type VARCHAR(100) NOT NULL,
    features JSONB,
    labels JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing model versions
CREATE TABLE IF NOT EXISTS model_versions (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    accuracy FLOAT,
    metrics JSONB,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create views for common queries
CREATE OR REPLACE VIEW recent_breaking_changes AS
SELECT bc.*, c.message, c.author, c.repository
FROM breaking_changes bc
JOIN commits c ON bc.commit_hash = c.commit_hash
WHERE bc.created_at > NOW() - INTERVAL '7 days'
ORDER BY bc.created_at DESC;

CREATE OR REPLACE VIEW active_recommendations AS
SELECT *
FROM optimization_recommendations
WHERE status = 'active' AND fix_applied = FALSE
ORDER BY severity DESC, estimated_impact DESC;

-- Insert initial data
INSERT INTO model_versions (model_name, version, is_active, accuracy)
VALUES
    ('breaking_change_detector', '1.0.0', true, 0.85),
    ('anomaly_detector', '1.0.0', true, 0.90),
    ('performance_predictor', '1.0.0', true, 0.82);

