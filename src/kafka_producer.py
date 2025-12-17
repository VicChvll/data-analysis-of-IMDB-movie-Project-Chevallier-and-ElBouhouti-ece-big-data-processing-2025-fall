import json
import requests
import sseclient
from kafka import KafkaProducer
import config

def create_producer():
    return KafkaProducer(
        bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def process_event(event_data, producer):
    title = event_data.get('title', '')
    entity_name = config.is_tracked_entity(title)
    
    if not entity_name:
        return False
    
    structured_event = {
        'entity_name': entity_name,
        'wiki_title': title,
        'event_type': event_data.get('type', ''),
        'user': event_data.get('user', ''),
        'bot': event_data.get('bot', False),
        'revision_id': event_data.get('revision', {}).get('new'),
        'timestamp': event_data.get('timestamp'),
        'comment': event_data.get('comment', ''),
        'raw_event': event_data
    }
    
    producer.send(config.KAFKA_TOPIC, value=structured_event)
    print(f"Event produced: {entity_name} - {structured_event['event_type']}")
    return True

def main():
    print("Starting Kafka producer...")
    print(f"Tracking {len(config.TRACKED_ENTITIES)} entities")
    
    producer = create_producer()
    
    response = requests.get(config.WIKIMEDIA_STREAM_URL, stream=True)
    client = sseclient.SSEClient(response)
    
    print("Connected to Wikimedia EventStreams")
    print("Monitoring events...")
    
    event_count = 0
    try:
        for event in client.events():
            try:
                event_data = json.loads(event.data)
                if process_event(event_data, producer):
                    event_count += 1
                    if event_count % 10 == 0:
                        print(f"Total events produced: {event_count}")
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"Error: {e}")
                continue
    except KeyboardInterrupt:
        print("\nShutting down producer...")
    finally:
        producer.close()
        print(f"Total events produced: {event_count}")

if __name__ == '__main__':
    main()