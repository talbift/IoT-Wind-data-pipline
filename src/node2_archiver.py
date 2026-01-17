import redis
import pymongo

# 1. Connexions
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
client_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
db = client_mongo["projet_eolien"]
collection = db["mesures"]

print("Nœud 2 (Archivage) prêt. J'attends Redis...")

# Variable pour savoir où on s'est arrêté de lire ('$' = maintenant)
dernier_id = "$"

while True:
    # On lit Redis en bloquant (attente infinie qu'une donnée arrive)
    lecture = r.xread({"flux_turbines": dernier_id}, count=1, block=0)
    
    for stream, messages in lecture:
        for message_id, data in messages:
            # On prépare le document pour MongoDB
            document = {
                "turbine": data["turbine"],
                "vent": float(data["vent"]),         # On convertit en nombre !
                "puissance": float(data["puissance"]),
                "energie": float(data["energie"])
            }
            
            # On insère dans MongoDB
            collection.insert_one(document)
            print(f"Stocké en Base de Données : {document}")
            
            # On met à jour pour lire le suivant la prochaine fois
            dernier_id = message_id
