IMDB Data Analysis & Stream Processing
Group Members:

CHEVALLIER Victor
ELBOUHOUTI Adeline

Structure du Projet

imdb-project/
├── data/                    # Datasets IMDB
├── src/                     # Code source
│   ├── config.py           # Configuration
│   ├── database.py         # Operations base de données
│   ├── kafka_producer.py   # Producteur Kafka
│   └── kafka_consumer.py   # Consommateur Kafka
├── sql/
│   └── init.sql            # Schema base de données
├── outputs/                # Logs et résultats
├── imdb_analysis.ipynb     # Analyse IMDB
├── ANSWERS.md              # Réponses aux questions
├── docker-compose.yml      # Configuration Docker
└── requirements.txt        # Dépendances Python


Installation
Prérequis

Docker Desktop
Python 3.9+
pip

Étapes

Installer les dépendances Python:

bashpip install -r requirements.txt

Démarrer les services Docker:

bashdocker-compose up -d

Vérifier que les services sont démarrés:

bashdocker-compose ps
Utilisation
Partie 1: Analyse IMDB
Ouvrir et exécuter le notebook Jupyter:
bashjupyter notebook imdb_analysis.ipynb
Le notebook va:

Télécharger les datasets IMDB
Répondre aux 12 questions
Générer ANSWERS.md

Partie 2: Stream Processing
Dans 2 terminaux séparés:
Terminal 1 - Producer:
bashpython src/kafka_producer.py
Terminal 2 - Consumer:
bashpython src/kafka_consumer.py
Le système va:

Monitorer les événements Wikipedia en temps réel
Traquer 5 entités IMDB
Stocker les métriques dans PostgreSQL
Générer des alertes

Entités Trackées

The Shawshank Redemption (film)
The Godfather (film)
Christopher Nolan (réalisateur)
Morgan Freeman (acteur)
Film noir (genre)

Base de Données
Tables

wiki_events: Événements Wikipedia bruts
entity_metrics: Métriques agrégées par entité
alerts: Alertes générées

Connexion
bashdocker exec -it postgres psql -U imdb_user -d imdb_db
Requêtes utiles:
sqlSELECT * FROM wiki_events LIMIT 10;
SELECT entity_name, COUNT(*) FROM wiki_events GROUP BY entity_name;
SELECT * FROM alerts ORDER BY triggered_at DESC;
Système d'Alertes
Le consumer génère des alertes pour:

Activité élevée (>10 éditions par heure)
Éditions rapides (>3 par minute)
Activité de bots élevée (>80%)

Arrêt
bash# Arrêter producer et consumer: Ctrl+C

# Arrêter Docker
docker-compose down
Notes

Les datasets IMDB peuvent prendre plusieurs minutes à télécharger
Le stream processing nécessite une connexion internet active
Les événements Wikipedia peuvent être rares selon les entités