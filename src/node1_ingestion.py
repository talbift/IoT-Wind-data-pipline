import json
import paho.mqtt.client as mqtt
import redis

# 1. Connexion à Redis (Le réservoir)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 2. Fonction qui nettoie les données
def nettoyer_donnees(data_json):
    valeurs = data_json["data"]
    
    # Si le vent est vide (NaN), on met la moyenne (5.98)
    if valeurs["Wind speed (m/s)"] is None or valeurs["Wind speed (m/s)"] == "NaN":
        valeurs["Wind speed (m/s)"] = 5.98
        print("Opération : Correction Vent (NaN -> 5.98)")

    # Si la puissance est vide, on met la moyenne (504.87)
    if valeurs["Power (kW)"] is None or valeurs["Power (kW)"] == "NaN":
        valeurs["Power (kW)"] = 504.87
        print("Opération : Correction Puissance")
        
    return data_json

# 3. Fonction déclenchée quand un message arrive
def on_message(client, userdata, msg):
    message_recu = str(msg.payload.decode("utf-8"))
    donnees = json.loads(message_recu)
    
    # On nettoie
    donnees_propres = nettoyer_donnees(donnees)
    
    # On envoie dans Redis (Stream s'appelle 'flux_turbines')
    # On applatit un peu les données pour Redis
    r.xadd("flux_turbines", {
        "turbine": donnees_propres["turbine_id"],
        "vent": str(donnees_propres["data"]["Wind speed (m/s)"]),
        "puissance": str(donnees_propres["data"]["Power (kW)"]),
        "energie": str(donnees_propres["data"]["Energy Export (kWh)"])
    })
    print(f"-> Envoyé à Redis : {donnees_propres['turbine_id']}")

# 4. Connexion à Mosquitto
client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.subscribe("wind/turbine/data/#")
client.on_message = on_message

print("Nœud 1 (Ingestion) prêt. En attente...")
client.loop_forever()
