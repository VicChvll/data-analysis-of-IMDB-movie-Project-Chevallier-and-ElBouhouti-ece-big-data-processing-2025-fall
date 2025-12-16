import psycopg2
from psycopg2.extras import Json
import config

def get_connection():
    return psycopg2.connect(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        database=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD
    )

def insert_event(event_data):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO wiki_events 
                (entity_name, wiki_title, event_type, user_name, user_is_bot, 
                 revision_id, timestamp, comment, raw_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                event_data['entity_name'],
                event_data['wiki_title'],
                event_data['event_type'],
                event_data['user_name'],
                event_data['user_is_bot'],
                event_data['revision_id'],
                event_data['timestamp'],
                event_data['comment'],
                Json(event_data['raw_data'])
            ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def insert_metric(metric_data):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO entity_metrics 
                (entity_name, window_start, window_end, total_edits, 
                 unique_editors, bot_edits, human_edits)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (entity_name, window_start) 
                DO UPDATE SET
                    total_edits = EXCLUDED.total_edits,
                    unique_editors = EXCLUDED.unique_editors,
                    bot_edits = EXCLUDED.bot_edits,
                    human_edits = EXCLUDED.human_edits
            """, (
                metric_data['entity_name'],
                metric_data['window_start'],
                metric_data['window_end'],
                metric_data['total_edits'],
                metric_data['unique_editors'],
                metric_data['bot_edits'],
                metric_data['human_edits']
            ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def insert_alert(alert_data):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO alerts 
                (entity_name, alert_type, severity, message, details, triggered_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                alert_data['entity_name'],
                alert_data['alert_type'],
                alert_data['severity'],
                alert_data['message'],
                Json(alert_data['details']),
                alert_data['triggered_at']
            ))
        conn.commit()
        print(f"ALERT: {alert_data['severity']} - {alert_data['message']}")
        return True
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()