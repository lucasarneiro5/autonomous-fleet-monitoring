# Autonomous Fleet Monitoring in Urban Environments

This project simulates an IoT environment where autonomous vehicles operating in urban areas send sensor data and detect environmental events. The data is stored in a **remote NoSQL database (MongoDB)** using at least **two collections**: one for vehicle telemetry and another for detected urban events.

---

## 🚀 Project Goals

- Simulate autonomous vehicle telemetry and environmental event detection.
- Generate **fake but realistic data** using Python libraries.
- Store the data in a **remote MongoDB database**.
- Enable analysis and monitoring of the fleet in urban contexts.

---

## 🧠 Features

- Generation of at least **1,000+ documents per collection**.
- Two MongoDB collections:
  - `vehicle_data`: Vehicle telemetry (location, speed, battery, etc.)
  - `urban_events`: Events like obstacles, traffic jams, etc.
- Data generated with randomized yet consistent structure.
- Modular code structure for extensibility.

---

## 🧰 Technologies Used

- Python 3.x
- [Faker](https://faker.readthedocs.io/en/master/) — Data generation
- `random`, `uuid`, `datetime` — Native Python libs
- `pymongo` — MongoDB integration
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) — Remote NoSQL database

---

## 🗃️ Example Document Structures

### `vehicle_data`:
```json
{
  "vehicle_id": "V-2025-038",
  "timestamp": "2025-05-26T14:33:12Z",
  "location": {
    "lat": -23.5489,
    "lng": -46.6388
  },
  "speed_kmh": 42.5,
  "battery_level": 78.2,
  "temperature_celsius": 45.3,
  "system_status": "OK"
}


## Details generate_data.py:

1. ✅ Imports e setup

Faker: biblioteca que gera dados falsos realistas (nomes, coordenadas, frases...).
random, uuid, datetime: geram números, IDs únicos e datas.
pymongo: biblioteca oficial do Python para trabalhar com MongoDB.
dotenv/os: para ler variáveis do .env.

2. 🌐 Conectando com o banco

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
vehicle_collection = db["vehicle_data"]
events_collection = db["urban_events"]

Pega a URI e nome do banco do .env.
Conecta no cluster MongoDB.
Cria duas referências às collections onde os dados serão inseridos.

3. ⚙️ Parâmetros configuráveis

NUM_VEHICLES = 50
NUM_VEHICLE_DOCS = 1000
NUM_EVENT_DOCS = 1000
Quantos veículos fictícios teremos.
Quantos documentos em cada collection serão gerados.

VEHICLE_IDS = [f"V-{2025}-{str(i).zfill(3)}" for i in range(NUM_VEHICLES)]
Cria IDs no estilo V-2025-000, V-2025-001, ..., V-2025-049.

4. 🧠 Funções geradoras de dados

🚗 generate_vehicle_data():
{
  "vehicle_id": ...,               # ID do veículo
  "timestamp": ...,                # Data/hora ISO
  "location": {"lat": ..., "lng": ...},
  "speed_kmh": ...,                # Velocidade
  "battery_level": ...,            # Nível de bateria
  "temperature_celsius": ...,      # Temperatura interna
  "system_status": ...             # OK/WARNING/ERROR
}
Simula um "ping" do veículo com dados de sensores embarcados.

🚧 generate_urban_event():
{
  "event_id": ...,                 # UUID do evento
  "vehicle_id": ...,               # Veículo que detectou
  "timestamp": ...,
  "event_type": ...,               # obstacle, traffic_jam...
  "description": ...,              # Frase aleatória
  "location": {"lat": ..., "lng": ...},
  "severity": ...                  # low/medium/high
}
Simula eventos no ambiente urbano, como obstáculos, detectados pelos veículos

5. 📤 Inserção no MongoDB

vehicle_docs = [generate_vehicle_data() for _ in range(NUM_VEHICLE_DOCS)]
vehicle_collection.insert_many(vehicle_docs)
Gera uma lista com 1.000 documentos e envia para o MongoDB.
Repete o mesmo processo para a collection urban_events.

