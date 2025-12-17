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
├── docker-compose.yml      # Docker configuration
└── requirements.txt        # Python dependencies
```

## Installation

### Prerequisites
- Docker Desktop
- Python 3.9+ (i had python 3.13 and it caused problem with panda and numpy had to downgrade)
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

3. Verify services are running:
```bash
docker-compose ps
```

## Usage

### Part 1: IMDB Analysis

Run the Jupyter notebook:
```bash
jupyter notebook imdb_analysis.ipynb
```

The notebook will:
- Download IMDB datasets
- Answer all questions
- Generate ANSWERS.md

### Part 2: Stream Processing

Open 2 separate terminals:

**Terminal 1 - Producer:**
```bash
python src/kafka_producer.py
```

**Terminal 2 - Consumer:**
```bash
python src/kafka_consumer.py
```

The system will:
- Monitor Wikipedia events in real-time
- Track 5 IMDB entities
- Store metrics in PostgreSQL
- Generate alerts

## Tracked Entities

1. The Shawshank Redemption (movie)
2. The Godfather (movie)
3. Christopher Nolan (director)
4. Morgan Freeman (actor)
5. Film noir (genre)

## Database

### Tables
- **wiki_events**: Raw Wikipedia events
- **entity_metrics**: Aggregated metrics per entity
- **alerts**: Generated alerts

### Connection
```bash
docker exec -it postgres psql -U imdb_user -d imdb_db
```

### Useful queries
```sql
SELECT * FROM wiki_events LIMIT 10;
SELECT entity_name, COUNT(*) FROM wiki_events GROUP BY entity_name;
SELECT * FROM alerts ORDER BY triggered_at DESC;
```

## Alert System

The consumer generates alerts for:
- High activity (>10 edits per hour)
- Rapid edits (>3 per minute)
- High bot activity (>80%)

## Shutdown
```bash
# Stop producer and consumer: Ctrl+C

# Stop Docker
docker-compose down
```

## Notes

- IMDB datasets may take several minutes to download
- Stream processing requires active internet connection
- Wikipedia events may be rare depending on entities

