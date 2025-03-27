# monitor.py
import time
import os
import csv
from datetime import datetime, timedelta
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
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "data")

# Garante que o diretório de dados existe
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

# Controle do token global
token = None
token_expiration_time = None

def get_token_with_renewal():
    global token, token_expiration_time

    if not token or datetime.now() >= token_expiration_time:
        print(f"[{datetime.now().strftime('%H:%M')}] Gerando novo token...")
        token_data, expires_in = get_token(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
        token = token_data
        token_expiration_time = datetime.now() + timedelta(seconds=expires_in)

    return token

def log_status(user_name, availability, activity):
    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%H:%M:%S")
    file_name = f"{user_name.replace(' ', '_')}.csv"
    user_file_path = os.path.join(OUTPUT_PATH, file_name)
    GERAL_PATH = os.getenv("GERAL_PATH", OUTPUT_PATH) #Comentar para salvar em data/geral.csv | Caso não esteja comentado salvará no caminho especificado no .env
    geral_file_path = os.path.join(GERAL_PATH, "geral.csv")


    # Arquivo individual
    write_header = not os.path.exists(user_file_path)
    with open(user_file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["Data", "Hora", "Disponibilidade", "Atividade"])
        writer.writerow([date_str, time_str, availability, activity])

    # Arquivo geral
    write_header_geral = not os.path.exists(geral_file_path)
    with open(geral_file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header_geral:
            writer.writerow(["Data", "Hora", "Nome", "Disponibilidade", "Atividade"])
        writer.writerow([date_str, time_str, user_name, availability, activity])

def is_horario_util():
    agora = datetime.now()
    dia_semana = agora.weekday()  # 0 = segunda, 6 = domingo
    hora = agora.hour
    minuto = agora.minute

    # Se for sábado (5) ou domingo (6), não é horário úil
    if dia_semana >= 5:
        return False

    # Horário úil é entre 08:00 e 18:00 (inclusive até 18:00:00)
    if hora < 8 or (hora >= 18 and minuto > 0):
        return False

    return True

if __name__ == "__main__":
    print("Iniciando monitoramento de status do Teams...")

    em_monitoramento = False

    while True:
        if not is_horario_util():
            if em_monitoramento:
                print(f"[{datetime.now().strftime('%d/%m/%Y - %H:%M')}] Monitoramento pausado")
                em_monitoramento = False
            time.sleep(INTERVAL)
            continue

        if not em_monitoramento:
            print(f"[{datetime.now().strftime('%d/%m/%Y - %H:%M')}] Iniciando monitoramento")
            em_monitoramento = True

        token = get_token_with_renewal()

        for name, user_id in USERS.items():
            try:
                presence = get_presence(user_id, token)
                availability = presence.get("availability", "Desconhecido")
                activity = presence.get("activity", "Desconhecido")
                log_status(name, availability, activity)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {name}: {availability} - {activity}")
            except Exception as e:
                print(f"Erro ao consultar {name}: {e}")

        print('==========================================')
        time.sleep(INTERVAL)
