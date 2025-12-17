import json
from datetime import datetime, timedelta
from collections import defaultdict
from confluent_kafka import Consumer, KafkaError
import config
import database as db

class MetricsAggregator:
    def __init__(self):
        self.metrics = defaultdict(lambda: {
            'events': [],
            'editors': set(),
            'bot_count': 0,
            'human_count': 0
        })
        self.last_flush = datetime.now()
    
    def add_event(self, entity_name, event):
        m = self.metrics[entity_name]
        m['events'].append(event)
        m['editors'].add(event.get('user', 'Unknown'))
        if event.get('bot', False):
            m['bot_count'] += 1
        else:
            m['human_count'] += 1
    
    def should_flush(self):
        return (datetime.now() - self.last_flush).total_seconds() >= 300
    
    def flush_all(self):
        print("Flushing metrics to database...")
        for entity_name, m in self.metrics.items():
            if not m['events']:
                continue
            
            window_end = datetime.now()
            window_start = window_end - timedelta(seconds=300)
            
            metric_data = {
                'entity_name': entity_name,
                'window_start': window_start,
                'window_end': window_end,
                'total_edits': len(m['events']),
                'unique_editors': len(m['editors']),
                'bot_edits': m['bot_count'],
                'human_edits': m['human_count']
            }
            
            db.insert_metric(metric_data)
        
        self.metrics.clear()
        self.last_flush = datetime.now()
        print("Metrics flushed")

class AlertSystem:
    def __init__(self):
        self.recent_events = defaultdict(list)
        self.alert_cooldowns = {}
    
    def add_event(self, entity_name, event):
        self.recent_events[entity_name].append(event)
        self.check_alerts(entity_name)
    
    def check_alerts(self, entity_name):
        events = self.recent_events[entity_name]
        if len(events) < 5:
            return
        
        alert_key = f"{entity_name}_high_activity"
        if alert_key in self.alert_cooldowns:
            last_trigger = self.alert_cooldowns[alert_key]
            if (datetime.now() - last_trigger).total_seconds() < 300:
                return
        
        if len(events) >= 10:
            alert_data = {
                'entity_name': entity_name,
                'alert_type': 'high_activity',
                'severity': 'MEDIUM',
                'message': f'High activity detected: {len(events)} edits in last hour',
                'details': {'event_count': len(events)},
                'triggered_at': datetime.now()
            }
            db.insert_alert(alert_data)
            self.alert_cooldowns[alert_key] = datetime.now()

def create_consumer():
    return Consumer({
        'bootstrap.servers': config.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'imdb-consumer-group',
        'auto.offset.reset': 'latest'
    })

def main():
    print("Starting Kafka consumer...")
    
    consumer = create_consumer()
    consumer.subscribe([config.KAFKA_TOPIC])
    
    aggregator = MetricsAggregator()
    alerts = AlertSystem()
    
    print("Consuming events...")
    
    event_count = 0
    try:
        while True:
            msg = consumer.poll(1.0)
            
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Error: {msg.error()}")
                    break
            
            event = json.loads(msg.value().decode('utf-8'))
            entity_name = event.get('entity_name')
            
            event_data = {
                'entity_name': entity_name,
                'wiki_title': event.get('wiki_title'),
                'event_type': event.get('event_type'),
                'user_name': event.get('user'),
                'user_is_bot': event.get('bot', False),
                'revision_id': event.get('revision_id'),
                'timestamp': event.get('timestamp'),
                'comment': event.get('comment'),
                'raw_data': event.get('raw_event', {})
            }
            
            db.insert_event(event_data)
            aggregator.add_event(entity_name, event)
            alerts.add_event(entity_name, event)
            
            event_count += 1
            if event_count % 10 == 0:
                print(f"Processed {event_count} events")
            
            if aggregator.should_flush():
                aggregator.flush_all()
    
    except KeyboardInterrupt:
        print("\nShutting down consumer...")
    finally:
        aggregator.flush_all()
        consumer.close()
        print(f"Total events processed: {event_count}")

if __name__ == '__main__':
    main()