import random
import uuid
from datetime import datetime, timedelta, UTC
from faker import Faker
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import time
import sys

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
    random_hour = random.randint(6, 10)
    timestamp = datetime.now(UTC) - timedelta(days=random.randint(0, 6))
    timestamp = timestamp.replace(hour=random_hour, minute=random.randint(0, 59), microsecond=0)
    return {
        "vehicle_id": vehicle_id,
        "timestamp": timestamp,
        "location": {
            "lat": float(location[0]),
            "lng": float(location[1])
        },
        "speed_kmh": round(random.uniform(0, 120), 2),
        "battery_level": round(random.uniform(10, 100), 2),
        "temperature_celsius": round(random.uniform(20, 90), 2),
        "system_status": random.choices(STATUS_TYPES, weights=[0.5, 0.3, 0.2])[0]
    }

def generate_urban_event():
    vehicle_id = random.choice(VEHICLE_IDS)
    location = fake.local_latlng(country_code="BR", coords_only=True)
    timestamp = datetime.now(UTC) - timedelta(days=random.randint(0, 6))
    timestamp = timestamp.replace(microsecond=0)
    return {
        "event_id": str(uuid.uuid4()),
        "vehicle_id": vehicle_id,
        "timestamp": timestamp.isoformat(),
        "event_type": random.choice(EVENT_TYPES),
        "description": fake.sentence(nb_words=6),
        "location": {
            "lat": float(location[0]),
            "lng": float(location[1])
        },
        "severity": random.choices(SEVERITY_LEVELS, weights=[0.2, 0.3, 0.5])[0]
    }

# --- Update Example ---
def update_example_data(n_updates=5):
    print(f"\n🔧 Updating {n_updates} random vehicle documents...\n")
    start_update = time.time()

    sample_vehicles = list(vehicle_collection.aggregate([{"$sample": {"size": n_updates}}]))

    for doc in sample_vehicles:
        vehicle_id = doc["vehicle_id"]
        old_battery = doc["battery_level"]
        old_speed = doc["speed_kmh"]
        old_status = doc["system_status"]

        new_battery = round(random.uniform(10, 100), 2)
        new_speed = round(random.uniform(0, 120), 2)
        new_status = random.choices(STATUS_TYPES, weights=[0.6, 0.3, 0.1])[0]

        vehicle_collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {
                "battery_level": new_battery,
                "speed_kmh": new_speed,
                "system_status": new_status
            }}
        )

        print(f"Vehicle: {vehicle_id}")
        print(f"  🔸 Battery: {old_battery} → {new_battery}")
        print(f"  🔸 Speed:   {old_speed} km/h → {new_speed} km/h")
        print(f"  🔸 Status:  {old_status} → {new_status}\n")

    end_update = time.time()
    print(f"✅ Update completed in {end_update - start_update:.2f} seconds.\n")

# --- Redirecionar saída para arquivo ---
log_filename = f"log_insercao_localhost.txt"
original_stdout = sys.stdout

try:
    with open(log_filename, "w", encoding="utf-8") as f:
        sys.stdout = f

        print(f"📅 Execution started at: {datetime.now(UTC).isoformat()}\n")

        # --- Delete old data ---
        start_delete = time.time()
        deleted_vehicles = vehicle_collection.delete_many({})
        deleted_events = events_collection.delete_many({})
        end_delete = time.time()

        print(f"Deleted {deleted_vehicles.deleted_count} vehicle records.")
        print(f"Deleted {deleted_events.deleted_count} urban event records.")
        print(f"🧹 Data deletion completed in {end_delete - start_delete:.2f} seconds.\n")

        # --- Generate data ---
        print(f"Generating {NUM_VEHICLE_DOCS} vehicle telemetry documents...")
        vehicle_docs = [generate_vehicle_data() for _ in range(NUM_VEHICLE_DOCS)]

        print(f"Generating {NUM_EVENT_DOCS} urban event documents...")
        event_docs = [generate_urban_event() for _ in range(NUM_EVENT_DOCS)]

        # --- Insert data with timing ---
        print("Inserting vehicle data...")
        start_vehicles = time.time()
        vehicle_collection.insert_many(vehicle_docs)
        end_vehicles = time.time()
        print(f"Vehicle data inserted in {end_vehicles - start_vehicles:.2f} seconds.\n")

        print("Inserting urban events...")
        start_events = time.time()
        events_collection.insert_many(event_docs)
        end_events = time.time()
        print(f"Urban event data inserted in {end_events - start_events:.2f} seconds.\n")

        update_example_data(n_updates=5)

        print("✅ Data generation and insertion completed.")

finally:
    sys.stdout = original_stdout
    print(f"📄 Logs saved to '{log_filename}'")
