from datetime import datetime
import database as db

print("Inserting test events...")

# Test event 1
event1 = {
    'entity_name': 'The Shawshank Redemption',
    'wiki_title': 'The_Shawshank_Redemption',
    'event_type': 'edit',
    'user_name': 'MovieFan2024',
    'user_is_bot': False,
    'revision_id': 123456789,
    'timestamp': datetime.now(),
    'comment': 'Updated cast information',
    'raw_data': {}
}
db.insert_event(event1)
print("Event 1 inserted")

# Test event 2
event2 = {
    'entity_name': 'The Godfather',
    'wiki_title': 'The_Godfather',
    'event_type': 'edit',
    'user_name': 'CinemaBot',
    'user_is_bot': True,
    'revision_id': 123456790,
    'timestamp': datetime.now(),
    'comment': 'Fixed formatting',
    'raw_data': {}
}
db.insert_event(event2)
print("Event 2 inserted")

# Test event 3
event3 = {
    'entity_name': 'Christopher Nolan',
    'wiki_title': 'Christopher_Nolan',
    'event_type': 'edit',
    'user_name': 'FilmEditor',
    'user_is_bot': False,
    'revision_id': 123456791,
    'timestamp': datetime.now(),
    'comment': 'Added recent filmography',
    'raw_data': {}
}
db.insert_event(event3)
print("Event 3 inserted")

# Insert metrics
metric1 = {
    'entity_name': 'The Shawshank Redemption',
    'window_start': datetime.now(),
    'window_end': datetime.now(),
    'total_edits': 15,
    'unique_editors': 8,
    'bot_edits': 3,
    'human_edits': 12
}
db.insert_metric(metric1)
print("Metric 1 inserted")

metric2 = {
    'entity_name': 'Morgan Freeman',
    'window_start': datetime.now(),
    'window_end': datetime.now(),
    'total_edits': 8,
    'unique_editors': 5,
    'bot_edits': 2,
    'human_edits': 6
}
db.insert_metric(metric2)
print("Metric 2 inserted")

# Insert alert
alert1 = {
    'entity_name': 'The Godfather',
    'alert_type': 'high_activity',
    'severity': 'MEDIUM',
    'message': 'High activity detected: 12 edits in last hour',
    'details': {'edit_count': 12, 'threshold': 10},
    'triggered_at': datetime.now()
}
db.insert_alert(alert1)
print("Alert 1 inserted")

print("\nTest data inserted successfully!")
print("Check database with: docker exec -it postgres psql -U imdb_user -d imdb_db")