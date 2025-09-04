# 📦 Estrutura do projeto

```
streamlit-incident-monitor/
├─ app.py                    # App Streamlit com 2 abas
├─ server.py                 # FastAPI: endpoint /ingest para monitoramento
├─ model.py                  # Funções de detecção de anomalia (regra + z-score)
├─ schema.sql                # Consultas SQL úteis
├─ requirements.txt          # Dependências
├─ README.md                 # Como rodar e como apresentar
└─ sample_data/
   ├─ pos_hourly.csv         # Exemplo de POS por hora (use o seu CSV real)
   └─ seed_transactions.py   # Script opcional para popular SQLite com eventos
```

---

# README.md

```md
# Incident Monitor – Streamlit + FastAPI

App para analisar comportamento anômalo em POS por hora e monitorar transações em tempo (quase) real com alertas.

## 🚀 Como rodar

```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\\Scripts\\activate)
pip install -r requirements.txt

# 1) subir a API
uvicorn server:app --reload --port 8000

# 2) subir o app Streamlit (em outro terminal)
streamlit run app.py
```

## 🔌 Envio de eventos (exemplos)

```bash
# Aprovada
curl -X POST http://localhost:8000/ingest -H 'Content-Type: application/json' \
  -d '{"ts":"2025-09-03T10:00:00","status":"approved","count":90}'

# Falha
curl -X POST http://localhost:8000/ingest -H 'Content-Type: application/json' \
  -d '{"ts":"2025-09-03T10:00:00","status":"failed","count":30}'
```

A resposta da API inclui `recommend_alert` e os detalhes do cálculo (baseline vs janela recente e z-score).

## 🧪 CSV de exemplo

Colunas esperadas para POS: `hour, sales_today, sales_yesterday, avg_other_days`.
Use seu CSV real, ou comece com `sample_data/pos_hourly.csv`.

## 🧠 Como determinamos anomalias

- **POS por hora**: z-score por hora (|z| ≥ 2) entre hoje e a média histórica.
- **Transações**: taxa de falha por minuto. Comparamos a média da janela recente (ex.: 5 min) contra o baseline (ex.: 60 min) e alertamos se ultrapassar `μ + σ*k` (k configurável).

## 📈 SQL principal

Veja `schema.sql`. A consulta agrega por minuto e calcula `failure_rate = failed / total`.

## 📝 Dicas para a apresentação

- Mostre a aba 1 destacando as horas com `anomaly_flag=True` e explique hipóteses (picos de almoço, quedas por instabilidade no PDV etc.).
- Na aba 2, rode a consulta, exiba o gráfico e clique em **Executar** para mostrar a recomendação de alerta.
- Ajuste as janelas e `sigma` ao vivo para demonstrar sensibilidade do monitor.
```

---