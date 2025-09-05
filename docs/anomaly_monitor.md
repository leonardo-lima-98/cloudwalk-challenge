## 🚨 Detecção de Anomalias

A função `flag_pos_anomalies` é responsável por identificar **comportamentos fora da curva** nos dados de checkout.  

#### 📊 Estrutura dos Dados
Cada linha do CSV contém:

- `time` → hora do dia (00h, 01h, …)  
- `today` → valor de hoje  
- `yesterday` → valor de ontem  
- `same_day_last_week` → valor do mesmo dia da semana passada  
- `avg_last_week` → média da semana passada  
- `avg_last_month` → média do último mês  

#### ⚙️ Lógica da Detecção
1. **Delta (diferença bruta)**  
   Calcula a diferença entre o valor de hoje e a média do último mês:


2. **Desvio Padrão Proxy**  
Em vez de usar apenas um desvio padrão global, criamos um **proxy** com base na variância de três séries:
- mesmo dia da semana passada  
- média da última semana  
- média do último mês  

Isso garante que a comparação seja mais realista.  
Caso o desvio seja muito pequeno, fixamos o mínimo em `1` para evitar divisões por zero.

3. **Z-score**  
O delta é padronizado dividindo-se pelo desvio proxy:
O z-score indica **quantos desvios padrão** o valor de hoje está acima/abaixo da média.

4. **Flag de Anomalia**  
Se o `|z-score| ≥ 2`, o ponto é considerado uma **anomalia estatística**.

#### 🧩 Exemplo
| time | today | avg_last_month | delta_vs_mean | std_proxy | zscore_today_vs_mean | anomaly_flag |
|------|-------|----------------|---------------|-----------|-----------------------|---------------|
| 10h  | 15    | 10             | +5            | 1.2       | +4.1                  | ✅ True        |
| 11h  | 50    | 12             | +38           | 8.0       | +4.7                  | ✅ True        |
| 12h  | 8     | 9              | -1            | 1.5       | -0.7                  | ❌ False       |

#### 🚦 Resumindo
- **delta_vs_mean** → quanto hoje está acima/abaixo da média.  
- **std_proxy** → desvio padrão ajustado pelas referências.  
- **zscore_today_vs_mean** → medida estatística padronizada.  
- **anomaly_flag** → indica se houve anomalia.  
