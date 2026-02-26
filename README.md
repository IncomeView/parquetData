
# 📦 parquetData
### Pipeline completo para ingestão, transformação e análise de dados baseados em arquivos Parquet.

![CI](https://github.com/IncomeView/parquetData/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/IncomeView/parquetData/actions/workflows/release.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12+-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

O **parquetData** é uma solução projetada para centralizar todo o ciclo de vida de dados provenientes de arquivos Parquet, permitindo que sejam transformados, estruturados, armazenados e disponibilizados para análises corporativas.

Ele funciona como o núcleo de um pipeline moderno de dados, integrando:
- ingestão de arquivos Parquet
- transformações avançadas em Python
- criação de tabelas e views em PostgreSQL (WSL)
- preparação de datasets para dashboards
- automação de CI/CD com versionamento baseado em tags
- execução padronizada via Docker

---

## 🏢 Contexto
O projeto foi idealizado para atender cenários onde:
- há grande volume de dados em formato Parquet
- é necessário padronizar e transformar informações
- existe um banco PostgreSQL para armazenamento e modelagem
- dashboards dependem de dados consistentes e atualizados
- automação e rastreabilidade são essenciais
- execução padronizada via containers facilita o ambiente de desenvolvimento

O parquetData se torna o elo entre **dados brutos** e **informações analíticas**.

---

## 🚀 Objetivo do Projeto
Criar uma base sólida e escalável para:
- padronizar ingestão de arquivos Parquet
- aplicar transformações avançadas
- estruturar dados em PostgreSQL
- gerar views analíticas
- alimentar dashboards corporativos
- automatizar releases e versionamento
- permitir execução consistente via Docker

---

## 🔄 Pipeline de Dados

```text
                ┌───────────────────────┐
                │   Arquivos Parquet    │
                └──────────┬────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │ Transformações        │
                │ Avançadas em Python   │
                └──────────┬────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │   PostgreSQL (WSL)    │
                │  • Tabelas            │
                │  • Views              │
                │  • Materialized Views │
                │  • Functions          │
                └──────────┬────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │   Dashboards / BI     │
                │ Power BI / Metabase   │
                └───────────────────────┘
```

---

## 🧩 Funcionalidades
- 📥 Ingestão de arquivos Parquet
- 🧹 Transformações avançadas em Python
- 🗄️ Criação automática de tabelas no PostgreSQL
- 📊 Geração de views analíticas
- 🔄 Pipeline CI/CD com versionamento automático
- 📦 Empacotamento automático (wheel + sdist)
- 🧪 Testes automatizados (PyTest)
- 🐳 Execução padronizada via Docker

---

## 🛠️ Tecnologias Utilizadas
- Python 3.12+
- Pandas
- PyArrow
- PostgreSQL (WSL)
- GitHub Actions (CI/CD)
- Docker

---

## 🐳 Execução via Docker
O projeto inclui suporte a execução containerizada, garantindo:
- ambiente padronizado
- isolamento de dependências
- facilidade de implantação

```bash
# 1. Build da imagem
docker build -t parquetdata:latest .

# 2. Execução do container
docker run --rm parquetdata:latest
```

---

## 📂 Estrutura do Projeto

```text
parquetData/
│
├── src/
│   └── parquetData/
│       └── __init__.py
│
├── scripts/
│   ├── main.py
│   ├── db_utils.py
│   ├── config.py
│   └── ...
│
├── tests/
│   ├── test_basic.py
│   ├── test_empty.py
│   ├── test_errors.py
│   ├── test_roundtrip.py
│   └── test_schema.py
│
├── .github/workflows/
│   ├── ci.yml
│   └── release.yml
│
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## 🔄 Versionamento e Releases
O versionamento **é automático e baseado em tags.**

```bash
git tag v0.3.6
git push origin v0.3.6
```

O GitHub Actions:
- extrai a versão da tag
- atualiza o pyproject.toml
- gera o wheel e o tar.gz
- cria a Release automaticamente

---

## 📘 Exemplos de Uso
(serão adicionados futuramente)

---

## 🧭 Roadmap
### ✔ Concluído
- [x] Leitura de arquivos Parquet
- [x] Transformações avançadas
- [x] CI com testes
- [x] CD com versionamento automático
- [x] Empacotamento automático
- [x] Suporte a Docker
### 🔜 Próximas etapas sugeridas
- [ ] Conector PostgreSQL completo
- [ ] Geração automática de views
- [ ] Carga incremental
- [ ] Exportação para dashboards
- [ ] Automação total do versionamento (semantic-release)
- [ ] Documentação avançada
- [ ] Benchmarks de performance
- [ ] Scripts de execução via Docker

---

## 🤝 Contribuições
Contribuições são bem-vindas!
Sugestões, melhorias e correções podem ser enviadas via Issues ou Pull Requests.

---

## 📄 Licença
Este projeto é distribuído sob a licença MIT.

---

## 👤 Autor
Moacir Magalhães Faria  
IncomeView — Data & Financial Engineering
GitHub: https://github.com/MmsFaria  
LinkedIn: https://www.linkedin.com/in/moacirfaria