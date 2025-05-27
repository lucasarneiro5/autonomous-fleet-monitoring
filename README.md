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




