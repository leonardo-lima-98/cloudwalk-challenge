## 📊 Monitor de Transações em Tempo Real

Este módulo implementa uma aplicação **Streamlit** para monitoramento de transações financeiras em tempo real.  
Ele integra consultas SQL, processamento com Pandas e visualização de gráficos/tabelas, permitindo acompanhar métricas como **aprovadas, negadas, revertidas, falhas e taxa de falhas**.

#### ⚙️ Estrutura Geral

1. **Configuração inicial**

- Banco de dados: `src/db/monitor.db`
- Schema SQL: `src/db/schema.sql`
- Dados simulados: `data/transactions/transactions.csv`
- Query: `src/db/query.sql`

Funções utilitárias importadas:
- `init_db(db_path, schema_path)` → cria o banco e aplica o schema.
- `populate_db_from_csv(db_path, csv_path)` → popula o banco com dados de exemplo.
- `load_df(db_path, query_path)` → executa a query SQL e retorna um `DataFrame` com intervalo de tempo (`start_time`, `end_time`).

2. **Configuração da página Streamlit**

```python
autorefresh = st_autorefresh(interval=5000, limit=None, key="refresh")
```

- Atualização automática a cada **5 segundos** via `st_autorefresh`.

3. **Controle de estado (Session State)**

- `columns` → estados selecionados pelo usuário (`approved`,`failed`,`denied`,`reversed`,`failure_rate`).  
- `current_time` → posição atual no tempo da simulação.  

Isso permite navegação **temporal** pelos dados.

4. **Sidebar (Parâmetros do usuário)**

- **Janela baseline (minutos):** controla quantos minutos recentes são exibidos.  
- **Seleção de estados:** usuário escolhe quais colunas (métricas) visualizar.  
- Garantia de pelo menos **uma seleção** (senão, mantém todas).  

5. **Conteúdo principal**

- **Gráfico de linha** (`st.line_chart`) → evolução temporal dos estados selecionados.  
- **Tabela** (`st.dataframe`) → registros da janela atual, ordenados de forma decrescente por `timestamp`.  

6. **Avanço temporal**

A simulação avança automaticamente:  
- Incrementa `current_time` em passos de **500 segundos**.  
- Ao chegar no `end_time`, retorna ao `start_time` (loop).  
