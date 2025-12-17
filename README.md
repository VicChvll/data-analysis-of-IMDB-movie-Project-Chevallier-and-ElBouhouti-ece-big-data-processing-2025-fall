# IMDB Data Analysis & Stream Processing

## Group Members
- CHEVALLIER Victor
- ELBOUHOUTI Adeline

## Project Structure
```
data-analysis-of-IMDB-movie-Project-Chevallier-ElBouhouti/
├── data/                    # IMDB Datasets
├── src/                     # Source code
│   ├── config.py           # Configuration
│   ├── database.py         # Database operations
│   ├── kafka_producer.py   # Kafka Producer
│   └── kafka_consumer.py   # Kafka Consumer
├── sql/
│   └── init.sql            # Database schema
├── outputs/                # Logs and results
├── imdb_analysis.ipynb     # IMDB Analysis
├── ANSWERS.md              # Answers to questions
├── insert_test_data.sql    # Test data
├── docker-compose.yml      # Docker configuration
└── requirements.txt        # Python dependencies
```

## Installation

### Prerequisites
- Docker Desktop
- Python 3.9+ (problems with kafka on 3.13 so i had to downgrade..)
- pip

### Steps

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start Docker services:
```bash
docker-compose up -d
```

3. Verify services:
```bash
docker-compose ps
```

## Part 1: IMDB Analysis

Run the Jupyter notebook:
```bash
jupyter notebook imdb_analysis.ipynb
```

The notebook downloads IMDB datasets automatically and answers all 14 questions and the results are exported to ANSWERS.md.

## Part 2: Stream Processing

### Architecture

Producer monitors Wikimedia EventStreams for edits on 5 IMDB entities, publishes to Kafka, Consumer processes events and stores metrics/alerts in PostgreSQL.

### Running

Open 2 terminals:

**Terminal 1:**
```bash
python src/kafka_producer.py
```

**Terminal 2:**
```bash
python src/kafka_consumer.py
```

### Tracked Entities

1. The Shawshank Redemption (movie)
2. The Godfather (movie)
3. Christopher Nolan (director)
4. Morgan Freeman (actor)
5. Film noir (genre)

### Note on Wikipedia Events

Wikipedia edits for IMDB entities are extremely rare. The system works but capturing live events requires hours of runtime. Test data is provided in our project to demonstrate functionality.

### Loading Test Data
```bash
docker cp insert_test_data.sql postgres:/tmp/insert_test_data.sql
docker exec -it postgres psql -U imdb_user -d imdb_db -f /tmp/insert_test_data.sql
```

## Database

### Tables

- **wiki_events**: Raw Wikipedia events
- **entity_metrics**: Aggregated statistics (5-minute windows)
- **alerts**: Alert notifications

### Connection
```bash
docker exec -it postgres psql -U imdb_user -d imdb_db
```

### Queries
```sql
SELECT * FROM wiki_events ORDER BY timestamp DESC;
SELECT entity_name, COUNT(*) FROM wiki_events GROUP BY entity_name;
SELECT * FROM entity_metrics ORDER BY window_start DESC;
SELECT * FROM alerts ORDER BY triggered_at DESC;
```

## Alert System

Alerts trigger on:
- High activity: more than 10 edits per hour (MEDIUM)
- Rapid edits: more than 3 edits per minute (HIGH)
- Bot activity: more than 80% bot edits (LOW)

Each alert type has a 5 minutes cooldown.

## Verification
```bash
docker exec -it postgres psql -U imdb_user -d imdb_db -c "SELECT COUNT(*) FROM wiki_events;"
docker exec -it postgres psql -U imdb_user -d imdb_db -c "SELECT * FROM entity_metrics;"
docker exec -it postgres psql -U imdb_user -d imdb_db -c "SELECT * FROM alerts;"
```

