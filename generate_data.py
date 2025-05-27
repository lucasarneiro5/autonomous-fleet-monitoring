import random
import uuid
from datetime import datetime
from faker import Faker
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import time

# --- Setup ---
load_dotenv()
fake = Faker()

# MongoDB config
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
vehicle_collection = db["vehicle_data"]
events_collection = db["urban_events"]

# --- Configurable parameters ---
NUM_VEHICLES = 50
NUM_VEHICLE_DOCS = 1000
NUM_EVENT_DOCS = 1000
VEHICLE_IDS = [f"V-{2025}-{str(i).zfill(3)}" for i in range(NUM_VEHICLES)]

EVENT_TYPES = ["obstacle", "traffic_jam", "roadwork", "accident", "pedestrian_crossing"]
STATUS_TYPES = ["OK", "WARNING", "ERROR"]
SEVERITY_LEVELS = ["low", "medium", "high"]

# --- Helper functions ---
def generate_vehicle_data():
    vehicle_id = random.choice(VEHICLE_IDS)
    location = fake.local_latlng(country_code="BR", coords_only=True)
    return {
        "vehicle_id": vehicle_id,
        "timestamp": datetime.utcnow().isoformat(),
        "location": {
            "lat": float(location[0]),
            "lng": float(location[1])
        },
        "speed_kmh": round(random.uniform(0, 120), 2),
        "battery_level": round(random.uniform(10, 100), 2),
        "temperature_celsius": round(random.uniform(20, 90), 2),
        "system_status": random.choice(STATUS_TYPES)
    }

def generate_urban_event():
    vehicle_id = random.choice(VEHICLE_IDS)
    location = fake.local_latlng(country_code="BR", coords_only=True)
    return {
        "event_id": str(uuid.uuid4()),
        "vehicle_id": vehicle_id,
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": random.choice(EVENT_TYPES),
        "description": fake.sentence(nb_words=6),
        "location": {
            "lat": float(location[0]),
            "lng": float(location[1])
        },
        "severity": random.choice(SEVERITY_LEVELS)
    }

# --- Delete old data if exists ---
print("Checking for existing data...")
vehicle_collection.delete_many({
    "timestamp": {"$gte": start_of_today.isoformat()}
})

deleted_events = events_collection.delete_many({})
print(f"Deleted {deleted_vehicles.deleted_count} old vehicle records.")
print(f"Deleted {deleted_events.deleted_count} old urban event records.")

# --- Generate and insert new data ---
print(f"Generating {NUM_VEHICLE_DOCS} vehicle telemetry documents...")
vehicle_docs = [generate_vehicle_data() for _ in range(NUM_VEHICLE_DOCS)]

print(f"Generating {NUM_EVENT_DOCS} urban event documents...")
event_docs = [generate_urban_event() for _ in range(NUM_EVENT_DOCS)]

# Insert with timing
print("Inserting vehicle data...")
start_vehicles = time.time()
vehicle_collection.insert_many(vehicle_docs)
end_vehicles = time.time()
print(f"Vehicle data inserted in {end_vehicles - start_vehicles:.2f} seconds.")

print("Inserting urban events...")
start_events = time.time()
events_collection.insert_many(event_docs)
end_events = time.time()
print(f"Urban event data inserted in {end_events - start_events:.2f} seconds.")

print("Data generation and insertion completed.")
