KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'wiki-events'

POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5432
POSTGRES_DB = 'imdb_db'
POSTGRES_USER = 'imdb_user'
POSTGRES_PASSWORD = 'imdb_password'

WIKIMEDIA_STREAM_URL = 'https://stream.wikimedia.org/v2/stream/recentchange'

TRACKED_ENTITIES = {
    'The Shawshank Redemption': {
        'type': 'movie',
        'wiki_page': 'The_Shawshank_Redemption'
    },
    'The Godfather': {
        'type': 'movie',
        'wiki_page': 'The_Godfather'
    },
    'Christopher Nolan': {
        'type': 'director',
        'wiki_page': 'Christopher_Nolan'
    },
    'Morgan Freeman': {
        'type': 'actor',
        'wiki_page': 'Morgan_Freeman'
    },
    'Film noir': {
        'type': 'genre',
        'wiki_page': 'Film_noir'
    }
}

def is_tracked_entity(title):
    title_lower = title.lower().replace('_', ' ')
    for entity_name, config in TRACKED_ENTITIES.items():
        wiki_page = config['wiki_page'].lower().replace('_', ' ')
        if wiki_page in title_lower or title_lower in wiki_page:
            return entity_name
    return None