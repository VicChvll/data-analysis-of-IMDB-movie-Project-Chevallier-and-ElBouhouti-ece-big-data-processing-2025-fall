CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS wiki_events (
    event_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_name VARCHAR(255) NOT NULL,
    wiki_title VARCHAR(500) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    user_name VARCHAR(255),
    user_is_bot BOOLEAN DEFAULT FALSE,
    revision_id BIGINT,
    timestamp TIMESTAMP NOT NULL,
    comment TEXT,
    raw_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_entity_name ON wiki_events(entity_name);
CREATE INDEX idx_timestamp ON wiki_events(timestamp);

CREATE TABLE IF NOT EXISTS entity_metrics (
    metric_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_name VARCHAR(255) NOT NULL,
    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL,
    total_edits INT DEFAULT 0,
    unique_editors INT DEFAULT 0,
    bot_edits INT DEFAULT 0,
    human_edits INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(entity_name, window_start)
);

CREATE TABLE IF NOT EXISTS alerts (
    alert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_name VARCHAR(255) NOT NULL,
    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    details JSONB,
    triggered_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO tracked_entities (entity_name, entity_type, wiki_page)
VALUES 
    ('The Shawshank Redemption', 'movie', 'The_Shawshank_Redemption'),
    ('The Godfather', 'movie', 'The_Godfather'),
    ('Christopher Nolan', 'director', 'Christopher_Nolan'),
    ('Morgan Freeman', 'actor', 'Morgan_Freeman'),
    ('Film noir', 'genre', 'Film_noir')
ON CONFLICT DO NOTHING;