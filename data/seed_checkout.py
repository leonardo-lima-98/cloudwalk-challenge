import pandas as pd
import datetime as dt
import os
import random

# Definição dos horários
horas = [f"{h:02d}h" for h in range(24)]

# Pasta de saída
os.makedirs("checkout", exist_ok=True)

# Data de referência (hoje)
hoje = dt.date.today()

# Função para gerar um DataFrame com valores aleatórios
def gerar_dataframe():
    linhas = []
    for hora in horas:
        today = random.randint(0, 50)                     # vendas de hoje
        yesterday = random.randint(0, 50)                 # vendas de ontem
        same_day_last_week = random.randint(0, 50)        # vendas do mesmo dia semana passada
        avg_last_week = round(random.uniform(0, 30), 2)   # média da última semana
        avg_last_month = round(random.uniform(0, 30), 2)  # média do último mês
        linhas.append([hora, today, yesterday, same_day_last_week, avg_last_week, avg_last_month])
    
    df = pd.DataFrame(linhas, columns=["time","today","yesterday","same_day_last_week","avg_last_week","avg_last_month"])
    return df

# Gerar 30 dias de arquivos
for i in range(30):
    data_ref = hoje - dt.timedelta(days=i)
    nome_arquivo = f"checkout_{data_ref.strftime('%d%m%Y')}.csv"
    caminho = os.path.join("checkout", nome_arquivo)
    df = gerar_dataframe()
    df.to_csv(caminho, index=False)

print("✅ Arquivos CSV gerados em ./checkout")
