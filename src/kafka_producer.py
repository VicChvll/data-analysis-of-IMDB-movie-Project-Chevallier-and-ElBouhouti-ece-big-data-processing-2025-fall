import json
import requests
import sseclient
from confluent_kafka import Producer
import config

def create_producer():
    return Producer({'bootstrap.servers': config.KAFKA_BOOTSTRAP_SERVERS})

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
    
    producer.produce(
        config.KAFKA_TOPIC,
        value=json.dumps(structured_event).encode('utf-8')
    )
    producer.poll(0)
    print(f"Event produced: {entity_name} - {structured_event['event_type']}")
    return True

def main():
    print("Starting Kafka producer...")
    producer = create_producer()
    
    response = requests.get(config.WIKIMEDIA_STREAM_URL, stream=True, timeout=None)
    client = sseclient.SSEClient(response)
    
    print("Connected to Wikimedia EventStreams")
    print("Monitoring events...")
    
    event_count = 0
    total_processed = 0
    
    try:
        for event in client.events():
            total_processed += 1
            
            if total_processed % 1000 == 0:
                print(f"Scanned {total_processed} events, found {event_count} matching")
            
            try:
                if event.data:
                    event_data = json.loads(event.data)
                    if process_event(event_data, producer):
                        event_count += 1
                        if event_count % 10 == 0:
                            producer.flush()
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"Error processing event: {e}")
                continue
                
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        producer.flush()
        print(f"Total matched events: {event_count}")
        print(f"Total events scanned: {total_processed}")

if __name__ == '__main__':
    main()