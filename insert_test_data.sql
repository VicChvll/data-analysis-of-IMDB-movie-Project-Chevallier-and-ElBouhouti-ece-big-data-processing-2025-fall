INSERT INTO wiki_events (entity_name, wiki_title, event_type, user_name, user_is_bot, revision_id, timestamp, comment, raw_data)
VALUES 
('The Shawshank Redemption', 'The_Shawshank_Redemption', 'edit', 'MovieFan2024', false, 123456789, NOW(), 'Updated cast information', '{}'),
('The Godfather', 'The_Godfather', 'edit', 'CinemaBot', true, 123456790, NOW(), 'Fixed formatting', '{}'),
('Christopher Nolan', 'Christopher_Nolan', 'edit', 'FilmEditor', false, 123456791, NOW(), 'Added recent filmography', '{}');

INSERT INTO entity_metrics (entity_name, window_start, window_end, total_edits, unique_editors, bot_edits, human_edits)
VALUES 
('The Shawshank Redemption', NOW() - INTERVAL '1 hour', NOW(), 15, 8, 3, 12),
('Morgan Freeman', NOW() - INTERVAL '1 hour', NOW(), 8, 5, 2, 6);

INSERT INTO alerts (entity_name, alert_type, severity, message, details, triggered_at)
VALUES 
('The Godfather', 'high_activity', 'MEDIUM', 'High activity: 12 edits', '{"edit_count": 12}', NOW());