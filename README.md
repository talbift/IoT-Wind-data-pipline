\# Pipeline de Données IoT - Parc Éolien 



Ce projet implémente une architecture distribuée à 3 nœuds pour la collecte, le nettoyage et l'analyse de données de capteurs éoliens en temps réel.



\## 📁 Structure du Projet

\- \*\*src/\*\* : Contient les scripts Python d'ingestion (Node 1) et d'archivage (Node 2).

\- \*\*data/\*\* : Scripts de simulation et génération de données brutes.

\- \*\*docs/\*\* : Rapport technique détaillé et schéma de l'architecture.

\- \*\*requirements.txt\*\* : Dépendances nécessaires (Paho-MQTT, PyMongo, Redis).



\## 🏗 Architecture de la Solution

Le pipeline repose sur un découplage des responsabilités :

1\. \*\*MQTT (Mosquitto)\*\* : Transport des messages des turbines.

2\. \*\*Node 1 (Ingestion)\*\* : Nettoyage des données (imputation des `NaN` par la moyenne).

3\. \*\*Redis Streams\*\* : Système de buffer à haute performance.

4\. \*\*Node 2 (Archivage)\*\* : Transfert persistant vers la base NoSQL.

5\. \*\*MongoDB\*\* : Stockage long terme et calcul des KPIs via moteur d'agrégation.



\## 🛠 Installation et Utilisation

```bash

\# Installer les dépendances

pip install -r requirements.txt



\# Lancer les services Docker

docker run -d -p 6379:6379 redis

docker run -d -p 27017:27017 mongo



\# Lancer les composants

python src/node1\_ingestion.py #python3  src/node1\_ingestion.py

python src/node2\_archiver.py  #python3  src/node2\_archiver.py



\#Lancer les générateurs

python data/Turibne\_101\_Data\_Generator.py #python3 data/Turibne\_101\_Data\_Generator.py

python data/Turibne\_102\_Data\_Generator.py #python3 data/Turibne\_102\_Data\_Generator.py

python data/Turibne\_103\_Data\_Generator.py #python3 data/Turibne\_103\_Data\_Generator.py



