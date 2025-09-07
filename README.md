## 🚀 Guia de Instalação e Execução do Projeto

Este documento descreve os passos necessários para configurar, instalar e executar o projeto **Monitor de Transações em Tempo Real**.

#### 📦 Pré-requisitos

Antes de iniciar, certifique-se de ter os seguintes componentes instalados:

- [Python 3.11+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/)

#### 📥 Clonando o Repositório

```bash
git clone https://github.com/leonardo-lima-98/cloudwalk-challenge.git
cd cloudwalk-challenge
```

#### 🛠️ Configuração do Ambiente

Crie um ambiente virtual (recomendado):

```bash
python -m venv venv
source venv/bin/activate   # Linux/MacOS
venv\Scripts\activate    # Windows (PowerShell)
```

Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```  

<details>
  <summary>📂 Ver estrutura do projeto</summary>

  ```
  📦 projeto-monitor-transacoes
  ┣ 📂 data/                           # Dados simulados
  ┃ ┣ 📂 checkout/                     # Arquivos de checkout simulados
  ┃ ┃ ┣ 📜 checkout_1.csv
  ┃ ┃ ┗ 📜 checkout_2.csv
  ┃ ┣ 📂 transactions/
  ┃ ┃ ┣ 📜 seed_checkout.py
  ┃ ┃ ┗ 📜 seed_transactions.py
  ┣ 📂 docs/                           # Documentação
  ┃ ┣ 📜 anomaly_monitor.md
  ┃ ┗ 📜 transacoes_monitor.md
  ┣ 📂 pages/                          # Páginas extras do Streamlit
  ┃ ┣ 📜 Monitor_de_Anomalias.py
  ┃ ┗ 📜 Monitor_de_Transacoes.py
  ┣ 📂 src/                            # Código-fonte principal
  ┃ ┣ 📂 db/                           # Banco e utilitários
  ┃ ┃ ┣ 📜 db_utils.py
  ┃ ┃ ┣ 📜 monitor.db                  # Banco de dados SQLite
  ┃ ┃ ┣ 📜 query.sql                   # Query principal de agregação
  ┃ ┃ ┗ 📜 schema.sql                  # Script de criação de schema
  ┃ ┣ 📜 monitor_anomalies.py
  ┃ ┣ 📜 monitor_transactions.py
  ┃ ┗ 📜 utils.py
  ┣ 📜 Home.py                         # Página inicial do Streamlit
  ┣ 📜 README.md                       # Guia do projeto
  ┗ 📜 requirements.txt                # Dependências do Python
  ```
</details>  

---

#### ▶️ Executando o Projeto

Para iniciar a aplicação Streamlit, execute:

```bash
streamlit run Home.py
```

A aplicação ficará disponível em:  
👉 http://localhost:8501

- A página inicial é `Home.py` podendo consultar toda documentação do projeto  
- As principais páginas (como `Monitor_de_Transacoes.py` e `Monitor_de_Anomalias.py`) ficam acessíveis no menu lateral do Streamlit.

#### Monitor_de_Anomalias.py
```
Nessa sessão podemos analisar os arquivos .csv de checkout. Considerando a numeração final como sendo os meses do ano podendo importar mais arquivos e analisa-los.
```
##### Funcionalidades:
###### ⬆️ Importe de Arquivos

A biblioteca Streamlit forneçe nativamente a sessão de carregamento dos arquivos podendo ser salvo no lake de dados.

###### 📈 Graficos de Exibição

Com o gráfico de linhas podemos ter uma visão do dados díarios com a referencia de média e o grafico de tabela sinaliza qual horario foi detectado uma anomalia.  

#### Monitor_de_Transacoes.py
```
Nessa sessão podemos analisar os arquivos .csv de transactions. A simulação de analise em tempo real consultando dos dados populados em um banco de dados.
```
##### Funcionalidades:
###### 🔄 Atualização Automática

O sistema utiliza a extensão do Streamlit `streamlit-autorefresh` para atualizar os dados a cada **5 segundos**, simulando um fluxo contínuo de transações.

###### ⚙️ Sidebar Customizavel

Você pode modificar a visão dos dados apartir da legenda escolhida e o intervalo de tempo para uma analise mais especifica ou abrangente.
