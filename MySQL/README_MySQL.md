# 🚗 Fleet Monitoring System - MySQL Version

Este projeto simula o monitoramento de uma frota de veículos autônomos urbanos, com dados gerados artificialmente e armazenados em um banco de dados MySQL. Ele realiza:

- Criação e popularização de tabelas com dados de veículos e eventos urbanos;
- Atualização de dados;
- Consultas analíticas úteis;
- Geração de logs e relatórios de desempenho.

---

## ⚙️ Etapas do Projeto

### 1. Geração e Inserção de Dados

Arquivo principal: `mysql_data_generator.py`

- Gera 1000 documentos de telemetria de veículos;
- Gera 1000 eventos urbanos com severidades variadas;
- Armazena os dados no banco MySQL local;
- Atualiza aleatoriamente 5 registros como exemplo.

### 2. Consultas SQL Analíticas

Arquivo: `mysql_queries.py`

Executa as seguintes análises:

1. **Veículos com falhas críticas nas últimas 24h**;
2. **Regiões com mais eventos com severidade alta**;
3. **Nível médio de bateria entre 06h e 10h**;
4. **Velocidade média por veículo nos últimos 7 dias**;
5. **Eventos ocorridos enquanto o sistema interno estava em "ERROR"**.

Os resultados são salvos no arquivo `relatorio_consultas_mysql.txt`, junto com os tempos de execução de cada query.

---

## ⏱️ Comparativo de Performance: MongoDB x MySQL (localmente)

| Etapa                                         | MongoDB (s) | MySQL (s) | Observações                                                                 |
|----------------------------------------------|-------------|-----------|------------------------------------------------------------------------------|
| Exclusão de dados antigos                    | 0.16        | 0.03      | MySQL geralmente é mais eficiente para deletes diretos em tabelas indexadas |
| Inserção de dados                            | 0.04        | 0.10      | MongoDB tem inserção em lote mais rápida, especialmente sem schema fixo     |
| Atualização de 5 registros                   | 0.04        | 0.01      | UPDATE no MySQL pode ser mais rápido com índices                            |
| Falhas críticas nas últimas 24h              | 0.0106      | 0.0013    | MySQL performou melhor nesta busca com filtro por data                      |
| Regiões com mais eventos severos             | 0.0031      | 0.0024    | Ambos eficientes, mas MySQL teve leve vantagem                              |
| Nível médio de bateria (06h–10h)             | 0.0027      | 0.0008    | MySQL mais eficiente para agregações com filtro por hora                    |
| Velocidade média por veículo (7 dias)        | 0.0034      | 0.0017    | MySQL novamente mais rápido                                                 |
| Eventos com sistema interno em “ERROR”       | 0.0041      | 0.0071    | MongoDB foi mais eficiente em junção por relação implícita                  |

### ✅ Conclusão

- **MongoDB** é mais ágil na **inserção em lote** e em **consultas com estrutura flexível** (como eventos com condição cruzada).
- **MySQL** mostra desempenho superior em **queries com filtros, agregações e índices**, e também em operações CRUD básicas.
- Ambos funcionaram localmente, e a escolha ideal depende do tipo de análise e volume de dados.

---

## 📁 Arquivos gerados

- `mysql_data_generator.py` → Geração e inserção de dados;
- `mysql_queries.py` → Execução das queries com log de performance;
- `relatorio_consultas_mysql.txt` → Relatório com resultados e tempos;
- `log_insercao.txt` → Log completo do processo de inserção e atualização;
- `README.md` → Documentação atual do projeto.

---

## 🧪 Pré-requisitos

- Python 3.9+
- MySQL Server local rodando
- Biblioteca `mysql-connector-python`, `python-dotenv`, `faker`

Instale com:

```bash
pip install mysql-connector-python faker python-dotenv
