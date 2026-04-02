
## 📦 parquetData
#### Pipeline moderno para ingestão, transformação e publicação de dados em Parquet, PostgreSQL e Microsoft Fabric Lakehouse.

![CI](https://github.com/IncomeView/parquetData/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/IncomeView/parquetData/actions/workflows/release.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12+-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

O **parquetData** é um pipeline de dados modular, escalável e orientado a ambientes modernos de engenharia de dados. Ele integra:
- extração de dados de bancos relacionais (PostgreSQL)
- geração de arquivos Parquet
- envio estruturado para Azure Data Lake Storage Gen2
- compatibilidade nativa com Microsoft Fabric Lakehouse (pasta Files/)
- transformações Bronze → Silver → Gold
- execução padronizada via CLI e Docker
- versionamento automático via Git tags
- CI/CD completo com GitHub Actions

O projeto foi desenvolvido para atender pipelines corporativos que exigem rastreabilidade, padronização, automação e integração com plataformas analíticas modernas.

---

## 🏢 Contexto Corporativo
O parquetData faz parte da arquitetura de dados da **IncomeView**, atuando como o componente responsável por:
- padronizar ingestão e transformação de dados
- integrar fontes locais (PostgreSQL/WSL) com o ecossistema Azure
- alimentar o **Microsoft Fabric** com dados estruturados
- garantir versionamento, reprodutibilidade e governança

Ele é utilizado em pipelines financeiros, contábeis e operacionais, onde consistência e auditabilidade são essenciais.

---

## 🚀 Objetivo do Projeto
Criar um pipeline completo e modular que:
- extrai dados de bancos relacionais
- gera arquivos Parquet padronizados
- envia para o ADLS no formato compatível com o Fabric
- organiza dados em camadas Bronze → Silver → Gold
- suporta execução local, em WSL, Docker ou CI/CD
- permite versionamento semântico baseado em tags
- integra com dashboards corporativos

---

## 🔄 Arquitetura do Pipeline

```text
                ┌──────────────────────────────┐
                │     PostgreSQL (WSL)         │
                │   • Tabelas de origem        │
                └──────────────┬───────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │        Bronze Pipeline       │
                │  • Extração                  │
                │  • Parquet local             │
                │  • Upload para ADLS          │
                │    (Files/bronze/)           │
                └──────────────┬───────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │        Silver Pipeline       │
                │  • Limpeza                   │
                │  • Normalização              │
                │  • Tipagem                   │
                │  • Envio para ADLS           │
                │    (Files/silver/)           │
                └──────────────┬───────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │         Gold Pipeline        │
                │  • Modelagem analítica       │
                │  • Métricas e agregações     │
                │  • Publicação no Fabric      │
                │    (Files/gold/)             │
                └──────────────────────────────┘
```

---

## 🧩 Funcionalidades Principais
- 📥 Extração de tabelas PostgreSQL
- 🪵 Geração de Parquet local (Bronze)
- ☁️ Upload automático para ADLS (pasta Files/ compatível com Fabric)
- 🧹 Transformações Bronze → Silver → Gold
- 🧪 Testes automatizados (PyTest)
- 🐳 Execução via Docker
- 🔄 CI/CD completo com GitHub Actions
- 🏷️ Versionamento automático baseado em tags
- 🧰 CLI integrada (parquetdata <comando>)

---

## 🛠️ Tecnologias Utilizadas
- Python 3.12+
- PyArrow / Pandas
- PostgreSQL (WSL)
- Azure Storage (ADLS Gen2)
- Microsoft Fabric Lakehouse
- Docker
- GitHub Actions (CI/CD)

---

## 📂 Estrutura do Projeto

```text
parquetData/
│
├── src/parquetData/
│   ├── extract/
│   │   ├── table_postgres.py
│   │   └── db_utils.py
│   ├── load/
│   │   ├── adls_send.py
│   │   ├── parquet_loader.py
│   │   └── parquet_to_postgres.py
│   ├── transform/
│   │   ├── bronze_to_silver.py
│   │   └── silver_to_gold.py
│   ├── pipeline/
│   │   ├── bronze_pipeline.py
│   │   ├── silver_pipeline.py
│   │   └── gold_pipeline.py
│   ├── cli.py
│   ├── settings.py
│   └── __main__.py
│
├── tests/
├── .github/workflows/
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## 🐳 Execução via Docker

```bash
docker build -t parquetdata:latest .
docker run --rm parquetdata:latest
```

---

## 🔄 Versionamento e Releases
O projeto usa **versionamento semântico baseado em tags**:

```bash
git tag v0.7.0
git push origin v0.7.0
```

A pipeline de release:
- lê a tag
- atualiza a versão do pacote
- gera wheel + sdist
- publica a Release no GitHub

---

## 🧭 Roadmap
### ✔ Concluído
- [x] Ambiente WSL real configurado
- [x] .venv estável e integrado ao VS Code
- [x] Bronze Pipeline funcional
- [x] Upload para ADLS com caminho correto (Files/bronze/)
- [x] CI/CD funcionando
- [x] Docker funcional
- [x] Versionamento automático por tags
### 🔜 em andamento
- [ ] Silver Pipeline (limpeza e normalização)
- [ ] Gold Pipeline (modelagem analítica)
- [ ] Integração com Warehouse Gen2
- [ ] Publicação automática no Fabric
- [ ] Documentação avançada
### 🛣️ Futuro
- [ ] Carga incremental
- [ ] Orquestração (Fabric Data Pipelines / Airflow)
- [ ] Monitoramento e alertas
- [ ] Benchmarks de performance

---

## 🤝 Contribuições
Contribuições são bem-vindas via Issues e Pull Requests.

---

## 📄 Licença
MIT License.

---

## 👤 Autor
Moacir Magalhães Faria  
IncomeView — Data & Financial Engineering
GitHub: https://github.com/MmsFaria  
LinkedIn: https://www.linkedin.com/in/moacirfaria
