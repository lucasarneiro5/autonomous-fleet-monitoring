# 🚗📊 Fleet Monitoring - Projeto com MySQL

Este projeto simula a geração, inserção e análise de dados de uma frota de veículos conectados e eventos urbanos, utilizando Python e MySQL.

---

## ⚙️ Tecnologias Utilizadas

- Python 3.11+
- MySQL (local)
- Faker (geração de dados falsos realistas)
- dotenv (leitura de variáveis de ambiente)
- mysql-connector-python

---

## 📦 Estrutura do Projeto

```
.
├── gerar_dados_mysql.py
├── consultar_dados_mysql.py
├── relatorio_consultas_mysql.txt
├── log_insercao.txt
├── .env
└── README.md
```

---

## 📁 1. `gerar_dados_mysql.py`

### ✅ O que faz:

- Cria o banco de dados `fleet_monitoring` (se não existir)
- Cria as tabelas `vehicle_data` e `urban_events`
- Gera 1000 registros de telemetria veicular e 1000 eventos urbanos aleatórios
- Deleta dados antigos
- Insere os novos dados
- Realiza 5 atualizações aleatórias
- Salva um log com tempos de execução no arquivo `log_insercao.txt`

### 🔧 Tabelas Criadas:

```sql
CREATE TABLE IF NOT EXISTS vehicle_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id VARCHAR(20),
    timestamp DATETIME,
    lat DOUBLE,
    lng DOUBLE,
    speed_kmh DOUBLE,
    battery_level DOUBLE,
    temperature_celsius DOUBLE,
    system_status ENUM('OK', 'WARNING', 'ERROR')
);

CREATE TABLE IF NOT EXISTS urban_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id VARCHAR(36),
    vehicle_id VARCHAR(20),
    timestamp DATETIME,
    event_type VARCHAR(50),
    description TEXT,
    lat DOUBLE,
    lng DOUBLE,
    severity ENUM('low', 'medium', 'high')
);
```

---

## 📁 2. `consultar_dados_mysql.py`

### 🔍 Consultas Realizadas:

1. **Veículos com falhas críticas nas últimas 24 horas**
2. **Regiões com maior número de eventos de alta severidade**
3. **Nível médio de bateria entre 06h e 10h**
4. **Velocidade média por veículo nos últimos 7 dias**
5. **Eventos urbanos ocorridos enquanto o sistema do veículo estava em “ERROR”**

### 🕒 Cada consulta registra o tempo de execução em:

```bash
relatorio_consultas_mysql.txt
```

---

## 🧪 Como Executar

1. **Crie um ambiente virtual (opcional)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

   Ou instale manualmente:
   ```bash
   pip install faker mysql-connector-python python-dotenv
   ```

3. **Configure o arquivo `.env`**:

   Crie um arquivo `.env` com o seguinte conteúdo:

   ```env
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=root
   MYSQL_DB=fleet_monitoring
   ```

4. **Execute o script de geração de dados**:
   ```bash
   python gerar_dados_mysql.py
   ```

5. **Execute as consultas**:
   ```bash
   python consultar_dados_mysql.py
   ```

---

## 📄 Arquivos Gerados

- `log_insercao.txt`: Log de inserção e atualização de dados no MySQL com tempo de execução.
- `relatorio_consultas_mysql.txt`: Resultados das queries analíticas com tempo de execução.

---

## 👨‍💻 Autor

**Lucas Arneiro**  
Desenvolvedor de Dados & Educador Técnico  
🇧🇷 Brasil

---

## 📌 Observações

Este projeto é uma simulação para fins de aprendizado e prática de:

- Integração Python + MySQL
- Criação e manipulação de dados sintéticos
- Consultas analíticas otimizadas
