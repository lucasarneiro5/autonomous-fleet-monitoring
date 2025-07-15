import mysql.connector
from datetime import datetime, timedelta
import sys
import time

# Conectar ao banco de dados
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="fleet_monitoring"
)
cursor = conn.cursor(dictionary=True)

def run_query(title, query, formatter):
    print(f"\n🔍 {title}")
    start_time = time.time()
    cursor.execute(query)
    results = cursor.fetchall()
    end_time = time.time()
    formatter(results)
    print(f"⏱ Tempo de execução: {end_time - start_time:.4f} segundos")

# 1. Veículos com falhas críticas nas últimas 24 horas
def critical_failures_last_24h(results):
    if results:
        for row in results:
            print(f"Vehicle: {row['vehicle_id']} | Timestamp: {row['timestamp']}")
    else:
        print("Nenhum veículo com falha crítica nas últimas 24h.")

# 2. Regiões com mais eventos severos
def most_severe_event_areas(results):
    for row in results:
        print(f"Location: ({row['lat']}, {row['lng']}) | Total High Severity Events: {row['total']}")

# 3. Nível médio de bateria entre 6h e 10h
def average_battery_morning(results):
    if results and results[0]['avg_battery'] is not None:
        print(f"Nível médio de bateria entre 06h e 10h: {results[0]['avg_battery']:.2f}%")
    else:
        print("Nenhum dado de bateria encontrado entre 06h e 10h.")

# 4. Velocidade média por veículo nos últimos 7 dias
def avg_speed_last_7_days(results):
    for row in results:
        print(f"Vehicle: {row['vehicle_id']} | Velocidade média: {row['avg_speed']:.2f} km/h")

# 5. Eventos enquanto veículo estava com sistema em 'ERROR'
def events_while_system_error(results):
    for row in results:
        print(f"Vehicle: {row['vehicle_id']} | Event: {row['event_type']} | Timestamp: {row['timestamp']} | Severity: {row['severity']}")

# Consultas SQL
query_1 = """
SELECT vehicle_id, timestamp
FROM vehicle_data
WHERE system_status = 'ERROR'
  AND timestamp >= NOW() - INTERVAL 1 DAY;
"""

query_2 = """
SELECT lat, lng, COUNT(*) AS total
FROM urban_events
WHERE severity = 'high'
GROUP BY lat, lng
ORDER BY total DESC
LIMIT 5;
"""

query_3 = """
SELECT AVG(battery_level) AS avg_battery
FROM vehicle_data
WHERE HOUR(timestamp) BETWEEN 6 AND 10;
"""

query_4 = """
SELECT vehicle_id, AVG(speed_kmh) AS avg_speed
FROM vehicle_data
WHERE timestamp >= NOW() - INTERVAL 7 DAY
GROUP BY vehicle_id
ORDER BY avg_speed DESC;
"""

query_5 = """
SELECT ue.vehicle_id, ue.event_type, ue.timestamp, ue.severity
FROM urban_events ue
JOIN (
    SELECT DISTINCT vehicle_id
    FROM vehicle_data
    WHERE system_status = 'ERROR'
) err_vehicles
ON ue.vehicle_id = err_vehicles.vehicle_id;
"""

# --- Salvar resultados no arquivo ---
if __name__ == "__main__":
    with open("relatorio_consultas_mysql.txt", "w", encoding="utf-8") as f:
        original_stdout = sys.stdout
        sys.stdout = f

        print(f"📅 Relatório gerado em: {datetime.now().isoformat()}")

        run_query("1. Veículos com falhas críticas nas últimas 24h", query_1, critical_failures_last_24h)
        run_query("2. Regiões com mais eventos severos", query_2, most_severe_event_areas)
        run_query("3. Nível médio de bateria entre 6h e 10h", query_3, average_battery_morning)
        run_query("4. Velocidade média por veículo nos últimos 7 dias", query_4, avg_speed_last_7_days)
        run_query("5. Eventos ocorridos enquanto o sistema estava em 'ERROR'", query_5, events_while_system_error)

        sys.stdout = original_stdout
    print("📄 Relatório salvo em 'relatorio_consultas_mysql.txt'")
