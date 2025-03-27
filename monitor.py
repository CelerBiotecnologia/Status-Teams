# monitor.py
import time
import os
import csv
from datetime import datetime
from dotenv import load_dotenv
import json
from utils.graph_api import get_token, get_presence

# Carrega variáveis do .env
load_dotenv()
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
INTERVAL = int(os.getenv("INTERVAL", 60))
USERS = json.loads(os.getenv("USERS"))

# Garante que o diretório de dados existe
if not os.path.exists("data"):
    os.makedirs("data")

def log_status(user_name, availability, activity):
    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%H:%M:%S")
    file_path = f"data/{user_name.replace(' ', '_')}.csv"

    write_header = not os.path.exists(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["Data", "Hora", "Disponibilidade", "Atividade"])
        writer.writerow([date_str, time_str, availability, activity])

if __name__ == "__main__":
    print("Iniciando monitoramento de status do Teams...")
    token = get_token(TENANT_ID, CLIENT_ID, CLIENT_SECRET)

    while True:
        for name, user_id in USERS.items():
            try:
                presence = get_presence(user_id, token)
                availability = presence.get("availability", "Desconhecido")
                activity = presence.get("activity", "Desconhecido")
                log_status(name, availability, activity)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {name}: {availability} - {activity}")
            except Exception as e:
                print(f"Erro ao consultar {name}: {e}")

        time.sleep(INTERVAL)
