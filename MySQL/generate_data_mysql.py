import mysql.connector
from faker import Faker
import uuid
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import time
import sys

# --- Setup ---
load_dotenv()
fake = Faker()

# MySQL config
conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST", "localhost"),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD", "root")
)
cursor = conn.cursor()

# --- Redirecionar saída para arquivo ---
log_filename = "log_insercao_mysql.txt"
original_stdout = sys.stdout

try:
    with open(log_filename, "w", encoding="utf-8") as f:
        sys.stdout = f

        print(f"📅 Execution started at: {datetime.now().isoformat()}\n")

        # --- Criar banco e tabelas ---
        cursor.execute("CREATE DATABASE IF NOT EXISTS fleet_monitoring")
        conn.commit()
        cursor.execute("USE fleet_monitoring")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vehicle_id VARCHAR(20),
            timestamp DATETIME,
            lat DOUBLE,
            lng DOUBLE,
            speed_kmh DOUBLE,
            battery_level DOUBLE,
            temperature_celsius DOUBLE,
            system_status ENUM('OK', 'WARNING', 'ERROR')
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS urban_events (
            id INT AUTO_INCREMENT PRIMARY KEY,
            event_id VARCHAR(36),
            vehicle_id VARCHAR(20),
            timestamp DATETIME,
            event_type VARCHAR(50),
            description TEXT,
            lat DOUBLE,
            lng DOUBLE,
            severity ENUM('low', 'medium', 'high')
        )
        """)

        # --- Parâmetros ---
        NUM_VEHICLES = 50
        NUM_VEHICLE_DOCS = 1000
        NUM_EVENT_DOCS = 1000
        VEHICLE_IDS = [f"V-2025-{str(i).zfill(3)}" for i in range(NUM_VEHICLES)]
        EVENT_TYPES = ["obstacle", "traffic_jam", "roadwork", "accident", "pedestrian_crossing"]
        STATUS_TYPES = ["OK", "WARNING", "ERROR"]
        SEVERITY_LEVELS = ["low", "medium", "high"]

        # --- Funções ---
        def generate_vehicle_data():
            vehicle_id = random.choice(VEHICLE_IDS)
            location = fake.local_latlng(country_code="BR", coords_only=True)
            timestamp = datetime.now() - timedelta(days=random.randint(0, 6), hours=random.randint(6, 10))
            return (
                vehicle_id,
                timestamp,
                float(location[0]),
                float(location[1]),
                round(random.uniform(0, 120), 2),
                round(random.uniform(10, 100), 2),
                round(random.uniform(20, 90), 2),
                random.choices(STATUS_TYPES, weights=[0.6, 0.3, 0.1])[0]
            )

        def generate_urban_event():
            vehicle_id = random.choice(VEHICLE_IDS)
            location = fake.local_latlng(country_code="BR", coords_only=True)
            timestamp = datetime.now() - timedelta(days=random.randint(0, 6))
            return (
                str(uuid.uuid4()),
                vehicle_id,
                timestamp,
                random.choice(EVENT_TYPES),
                fake.sentence(nb_words=6),
                float(location[0]),
                float(location[1]),
                random.choices(SEVERITY_LEVELS, weights=[0.2, 0.3, 0.5])[0]
            )

        # --- Delete old data ---
        print("🧹 Deleting old data...")
        start_delete = time.time()
        cursor.execute("DELETE FROM vehicle_data")
        cursor.execute("DELETE FROM urban_events")
        conn.commit()
        end_delete = time.time()
        print(f"\n🗑️ Data deletion completed in {end_delete - start_delete:.2f} seconds.\n")

        # --- Insert new data ---
        print(f"Generating {NUM_VEHICLE_DOCS} vehicle telemetry records...")
        vehicle_data = [generate_vehicle_data() for _ in range(NUM_VEHICLE_DOCS)]

        print(f"Generating {NUM_EVENT_DOCS} urban event records...")
        event_data = [generate_urban_event() for _ in range(NUM_EVENT_DOCS)]

        print("🚗 Inserting vehicle data...")
        start_insert = time.time()
        cursor.executemany("""
            INSERT INTO vehicle_data (vehicle_id, timestamp, lat, lng, speed_kmh, battery_level, temperature_celsius, system_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, vehicle_data)

        print("🌆 Inserting urban event data...")
        cursor.executemany("""
            INSERT INTO urban_events (event_id, vehicle_id, timestamp, event_type, description, lat, lng, severity)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, event_data)
        conn.commit()
        end_insert = time.time()
        print(f"\n📥 Data insertion completed in {end_insert - start_insert:.2f} seconds.\n")

        # --- Update example ---
        print("🔧 Updating 5 random vehicle records...\n")
        start_update = time.time()
        cursor.execute("SELECT id, battery_level, speed_kmh, system_status FROM vehicle_data ORDER BY RAND() LIMIT 5")
        rows = cursor.fetchall()

        for row in rows:
            vid, old_battery, old_speed, old_status = row
            new_battery = round(random.uniform(10, 100), 2)
            new_speed = round(random.uniform(0, 120), 2)
            new_status = random.choice(STATUS_TYPES)
            print(f"ID {vid}: Battery {old_battery} → {new_battery}, Speed {old_speed} → {new_speed}, Status {old_status} → {new_status}")
            cursor.execute("""
                UPDATE vehicle_data
                SET battery_level=%s, speed_kmh=%s, system_status=%s
                WHERE id=%s
            """, (new_battery, new_speed, new_status, vid))

        conn.commit()
        end_update = time.time()
        print(f"\n✅ Update completed in {end_update - start_update:.2f} seconds.")
        print("📌 All operations finished.")

finally:
    conn.close()
    sys.stdout = original_stdout
    print(f"📄 Logs saved to '{log_filename}'")
