HEAD
# 🚗 Autonomous Fleet Monitoring

A smart simulation of autonomous vehicle fleet monitoring in urban environments using synthetic data and NoSQL storage.

This project generates fake telemetry and urban event data for a fleet of autonomous vehicles, stores the data in MongoDB Atlas, and performs analytical queries to support decision-making related to performance, safety, and system diagnostics.

---

## 📁 Project Structure

```bash
.
├── generate_data.py         # Generates and inserts fake data into MongoDB
├── query.py                 # Executes analytics queries and outputs insights
├── .env                     # MongoDB URI and configuration
├── relatorio_consultas.txt  # Output of the analytics queries
└── README.md
```

---

## ⚙️ Technologies Used

- Python 3.10+
- MongoDB Atlas (NoSQL database)
- PyMongo
- Faker (synthetic data generation)
- dotenv

---

## 📊 Database Schema

### `vehicle_data` Collection

| Field                | Type       | Description                                        |
|----------------------|------------|----------------------------------------------------|
| `vehicle_id`         | `string`   | Unique ID of the vehicle (e.g., `V-2025-007`)      |
| `timestamp`          | `datetime` | Date and time of the data record                   |
| `location.lat`       | `float`    | Latitude of the vehicle's position                 |
| `location.lng`       | `float`    | Longitude of the vehicle's position                |
| `speed_kmh`          | `float`    | Current speed in kilometers per hour              |
| `battery_level`      | `float`    | Battery level in percentage                        |
| `temperature_celsius`| `float`    | System temperature in degrees Celsius              |
| `system_status`      | `string`   | System status (`OK`, `WARNING`, or `ERROR`)        |

---

### `urban_events` Collection

| Field                | Type         | Description                                        |
|----------------------|--------------|----------------------------------------------------|
| `event_id`           | `UUID string`| Unique identifier for the event                    |
| `vehicle_id`         | `string`     | ID of the vehicle involved                         |
| `timestamp`          | `datetime`   | Date and time of the event                         |
| `event_type`         | `string`     | Type of event (`accident`, `roadwork`, etc.)       |
| `description`        | `string`     | Short description of the event                     |
| `location.lat`       | `float`      | Latitude of the event                              |
| `location.lng`       | `float`      | Longitude of the event                             |
| `severity`           | `string`     | Severity level (`low`, `medium`, or `high`)        |

---

## ❓ Example Analytical Queries

The `query.py` script answers key business questions such as:



1. **Which vehicles had critical failures in the last 24 hours?**  
   → Enables prompt preventive maintenance.

2. **Which urban areas had the highest number of severe events?**  
   → Supports urban infrastructure and safety planning.

3. **What was the average battery level between 6AM and 10AM?**  
   → Helps evaluate route efficiency and power usage.

4. **What was the average speed per vehicle in the last 7 days?**  
   → Enables performance auditing and optimization.

5. **Which events occurred while the vehicle system was in "ERROR"?**  
   → Assists in cross-analyzing vehicle system errors and external factors.

---

## 🧪 How to Run

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Configure environment variables**

Create a `.env` file with:

```env
MONGO_URI=your_mongodb_uri
DB_NAME=fleet_monitoring
```

3. **Generate and upload data**

```bash
python generate_data.py
```

4. **Run analytics and export report**

```bash
python query.py
```

---

## 📄 Output

Analytics results are saved to:

```
relatorio_consultas.txt
```

---

## 📬 License

MIT License. Feel free to fork, use, and contribute!

---

Created by [Lucas Arneiro](https://github.com/lucasarneiro5)
