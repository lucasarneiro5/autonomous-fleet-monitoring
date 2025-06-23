import time
from datetime import datetime, timedelta, UTC
from pymongo import MongoClient
from collections import defaultdict
from dotenv import load_dotenv
import os
import sys

# --- Setup ---
load_dotenv()

# MongoDB config
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Conexão com o MongoDB
client = MongoClient(MONGO_URI)
db = client["fleet_monitoring"]
vehicle_collection = db["vehicle_data"]
event_collection = db["urban_events"]

# Função auxiliar para medir tempo de execução
def run_query(title, func):
    print(f"\n🔍 {title}")
    start = time.perf_counter()
    func()
    end = time.perf_counter()
    print(f"⏱️  Tempo de execução: {end - start:.4f} segundos\n")

# 1. Veículos com falha crítica nas últimas 24h
def critical_failures_last_24h():
    since = datetime.now(UTC) - timedelta(hours=24)
    count = vehicle_collection.count_documents({
        "timestamp": {"$gte": since.isoformat()},
        "system_status": "ERROR"
    })
    print(f"Total de veículos com falhas críticas nas últimas 24h: {count}")

# 2. Regiões com mais eventos severos
def most_severe_event_areas():
    pipeline = [
        {"$match": {"severity": "high"}},
        {"$group": {"_id": "$location", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    results = list(event_collection.aggregate(pipeline))
    print("Top 5 regiões com mais eventos severos:")
    for r in results:
        print(f"Local: {r['_id']} - Eventos severos: {r['count']}")

# 3. Nível médio de bateria entre 6h e 10h
def average_battery_morning():
    today = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = today + timedelta(hours=6)
    end_time = today + timedelta(hours=10)

    pipeline = [
        {"$match": {"timestamp": {"$gte": start_time.isoformat(), "$lte": end_time.isoformat()}}},
        {"$group": {"_id": None, "avg_battery": {"$avg": "$battery_level"}}}
    ]

    result = list(vehicle_collection.aggregate(pipeline))
    if result:
        print(f"Nível médio de bateria entre 6h e 10h: {result[0]['avg_battery']:.2f}%")
    else:
        print("Nenhum dado encontrado nesse intervalo de tempo.")

# 4. Velocidade média por veículo nos últimos 7 dias
def avg_speed_last_7_days():
    since = datetime.now(UTC) - timedelta(days=7)
    pipeline = [
        #{"$match": {"timestamp": {"$gte": since.isoformat()}}},
        {"$match": {"timestamp": {"$gte": since}}},
        {"$group": {"_id": "$vehicle_id", "avg_speed": {"$avg": "$speed_kmh"}}},
        {"$sort": {"avg_speed": -1}}
    ]
    results = list(vehicle_collection.aggregate(pipeline))
    if results:
        total = sum(doc["avg_speed"] for doc in results)
        media_geral = total / len(results)
        print(f"Velocidade média geral nos últimos 7 dias: {media_geral:.2f} km/h")
    else:
        print("Nenhum dado de velocidade encontrado nos últimos 7 dias.")

# 5. Eventos com sistema do veículo em "ERROR"
def events_while_system_error():
    error_vehicle_ids = vehicle_collection.distinct("vehicle_id", {"system_status": "ERROR"})
    if not error_vehicle_ids:
        print("Nenhum veículo com status de erro encontrado.")
        return

    count = event_collection.count_documents({"vehicle_id": {"$in": error_vehicle_ids}})
    print(f"Total de eventos relacionados a veículos com erro: {count}")

# Executar todas as queries
if __name__ == "__main__":
    # Salvar a saída em um arquivo .txt
    with open("relatorio_consultas.txt", "w", encoding="utf-8") as f:
        original_stdout = sys.stdout  
        sys.stdout = f  

        run_query("1. Veículos com falhas críticas nas últimas 24h", critical_failures_last_24h)
        run_query("2. Regiões com mais eventos severos", most_severe_event_areas)
        run_query("3. Nível médio de bateria entre 6h e 10h", average_battery_morning)
        run_query("4. Velocidade média por veículo nos últimos 7 dias", avg_speed_last_7_days)
        run_query("5. Eventos ocorridos enquanto o sistema estava em 'ERROR'", events_while_system_error)

        sys.stdout = original_stdout  
    print("📄 Relatório salvo em 'relatorio_consultas.txt'")
