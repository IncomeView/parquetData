# PROJECT KNOWLEDGE BASE

Gerado em: 2026-11-03 17:15:55

Projeto: parquetData

---

## Resumo Executivo

- Projeto: parquetData
- Arquivos Python: 24
- Arquivos Markdown: 2
- Notebooks: 0

- Total de arquivos: 34
- Scripts Python: 24
- Arquivos Markdown: 2
- Notebooks: 0
- Extensões encontradas: 6

---

## Estrutura do Projeto

```text
parquetData
├── .github
│   └── workflows
│       ├── ci.yml
│       └── release.yml
├── .vscode
├── data
├── docs
│   └── _PROJECT_KNOWLEDGE_BASE.md
├── notebooks
├── scripts
│   └── generate_project_knowledge_base.py
├── src
│   ├── parquetData
│   │   ├── extract
│   │   │   ├── __init__.py
│   │   │   ├── db_utils.py
│   │   │   └── table_postgres.py
│   │   ├── load
│   │   │   ├── __init__.py
│   │   │   ├── adls_send.py
│   │   │   ├── parquet_loader.py
│   │   │   └── parquet_to_postgres.py
│   │   ├── pipeline
│   │   │   ├── __init__.py
│   │   │   ├── bronze_pipeline.py
│   │   │   ├── gold_pipeline.py
│   │   │   └── silver_pipeline.py
│   │   ├── transform
│   │   │   ├── __init__.py
│   │   │   ├── bronze_to_silver.py
│   │   │   └── silver_to_gold.py
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── cli.py
│   │   ├── config.py
│   │   └── settings.py
│   └── parquetData.egg-info
├── tests
│   ├── test_basic.py
│   ├── test_empty.py
│   ├── test_errors.py
│   ├── test_roundtrip.py
│   └── test_schema.py
├── .gitignore
├── docker-compose.yml
├── dockerfile
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## PyProject

- name: parquetData
- version: 0.3.3
- python: >=3.10

---

## Dependências

- azure-identity
- azure-storage-file-datalake
- click
- openpyxl
- pandas
- psycopg2-binary
- pyarrow
- pytest
- python-dotenv
- requests
- sqlalchemy

---

## Estatísticas de Arquivos

- .md: 2
- .py: 25
- .toml: 1
- .txt: 1
- .yml: 3
- [sem extensão]: 2

---

## Docker

- docker-compose.yml
- dockerfile

---

## GitHub Actions

- .github/workflows/ci.yml
- .github/workflows/release.yml

---

## Azure Detection

### Fabric

- README.md
- docs/_PROJECT_KNOWLEDGE_BASE.md
- scripts/generate_project_knowledge_base.py
- src/parquetData/settings.py

### ADLS

- ClientSecretCredential
- DataLakeServiceClient
- dfs.core.windows.net

---

## Pipeline Flow

### src/parquetData/cli.py

- bronze
- load

### src/parquetData/config.py

- load

### src/parquetData/extract/table_postgres.py

- read_table_to_parquet

### src/parquetData/load/adls_send.py

- upload_to_adls
- load

### src/parquetData/load/parquet_loader.py

- load

### src/parquetData/load/parquet_to_postgres.py

- load

### src/parquetData/pipeline/bronze_pipeline.py

- read_table_to_parquet
- upload_to_adls
- bronze
- load
- extract

### src/parquetData/pipeline/gold_pipeline.py

- silver
- gold
- transform

### src/parquetData/pipeline/silver_pipeline.py

- bronze
- silver
- transform

### src/parquetData/settings.py

- bronze
- silver
- gold

### src/parquetData/transform/bronze_to_silver.py

- bronze
- silver

### src/parquetData/transform/silver_to_gold.py

- silver
- gold

---

## Arquitetura Reconstruída


            PostgreSQL
                │
                ▼
            read_table_to_parquet()
                │
                ▼
            Arquivos Parquet
                │
                ▼
            upload_to_adls()
                │
                ▼
            Azure Data Lake Storage Gen2
                │
                ▼
            bronze/
                │
                ▼
            silver/
                │
                ▼
            gold/
                │
                ▼
            Microsoft Fabric Lakehouse
        

      Fluxo reconstruído automaticamente a partir das dependências, imports e pipelines detectados no projeto.

---

## Arquitetura Detectada

- Azure Data Lake Storage Gen2
- PostgreSQL
- Parquet Storage
- Medallion Architecture
- Microsoft Fabric
- Containerization

---

## Stack Tecnológica

- azure-identity
- azure-storage-file-datalake
- click
- openpyxl
- pandas
- psycopg2-binary
- pyarrow
- pytest
- python-dotenv
- requests
- sqlalchemy

---

## Entrypoints

- src/parquetData/__main__.py
- src/parquetData/cli.py
- src/parquetData/load/parquet_to_postgres.py

---

## Arquivos de Configuração

- .gitignore
- docker-compose.yml
- dockerfile
- pyproject.toml
- requirements.txt

---

## Entidades de Negócio

- bankmovement
- bankmovementbuldingcosts
- bankmovementfinancialcategories
- creditors
- customers
- income
- incomebankmovements
- incomecategoriesreceipts
- incomefinancialcategories
- incomereceipts
- incomereceiptsbankmovements
- incomereceiptsbankmovementsfinancialcategories
- incomereceiptscategories
- outcome
- outcomeauthorizations
- outcomebuildingscosts
- outcomecategoriespayments
- outcomepayments
- outcomepaymentsbankmovements
- outcomepaymentsbankmovementspaymentscategories

---

## Riscos Detectados


---

## Recomendações

- Avaliar migração para DefaultAzureCredential
- Adicionar observabilidade estruturada com logging
- Adicionar documentação de arquitetura
- Adicionar data lineage
- Adicionar monitoramento de pipelines

### Arquivos Relacionados

- src/parquetData/config.py
- src/parquetData/load/adls_send.py
- src/parquetData/settings.py

### Keywords Detectadas

- ClientSecretCredential
- DataLakeServiceClient
- azure.identity
- azure.storage
- dfs.core.windows.net
- lakehouse

### Variáveis de Ambiente

- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET
- AZURE_STORAGE_ACCOUNT_NAME
- AZURE_STORAGE_FILESYSTEM
- AZURE_TENANT_ID

---

## Roadmap Sugerido

- Observabilidade com logging estruturado
- Data Lineage
- Carga incremental
- Arquitetura Bronze/Silver/Gold completa
- Integração avançada com Fabric
- Monitoramento de pipelines
- Testes de integração

---

## Mapa de Dependências

---

## Catálogo de Scripts Python

### src/parquetData/__init__.py

### src/parquetData/__main__.py

#### Imports

- parquetData.cli

### src/parquetData/cli.py

#### Funções

- cli()
- bronze()
- bronze_all()
- load_parquet_all()

#### Imports

- click
- parquetData.load.parquet_to_postgres
- parquetData.pipeline.bronze_pipeline
- parquetData.settings
- pathlib

### src/parquetData/config.py

#### Imports

- dotenv
- os
- pathlib

### src/parquetData/extract/__init__.py

### src/parquetData/extract/db_utils.py

#### Funções

- get_connection()
- create_schema()
- create_table_if_not_exists()
- insert_dataframe()
- run_sql()

#### Imports

- pandas
- parquetData.config
- psycopg2

### src/parquetData/extract/table_postgres.py

#### Funções

- get_postgres_engine()
- read_table()
- read_table_to_parquet()

#### Imports

- pandas
- parquetData.config
- pathlib
- sqlalchemy
- typing

### src/parquetData/load/__init__.py

### src/parquetData/load/adls_send.py

#### Funções

- get_adls_client()
- upload_to_adls()

#### Imports

- azure.identity
- azure.storage.filedatalake
- parquetData.config
- pathlib

### src/parquetData/load/parquet_loader.py

#### Funções

- list_parquet_files()
- load_parquet_in_batches()
- get_table_name()

#### Imports

- os
- pyarrow.dataset

### src/parquetData/load/parquet_to_postgres.py

#### Funções

- get_engine()
- load_parquet_to_postgres()
- load_all_parquet_to_postgres()

#### Imports

- argparse
- parquetData.config
- parquetData.load.parquet_loader
- pathlib
- sqlalchemy
- time

### src/parquetData/pipeline/__init__.py

### src/parquetData/pipeline/bronze_pipeline.py

#### Funções

- run_bronze_pipeline()

#### Imports

- parquetData.extract.table_postgres
- parquetData.load.adls_send
- parquetData.settings
- pathlib

### src/parquetData/pipeline/gold_pipeline.py

#### Funções

- run_gold_pipeline()

#### Imports

- pandas
- parquetData.transform.silver_to_gold
- pathlib

### src/parquetData/pipeline/silver_pipeline.py

#### Funções

- run_silver_pipeline()

#### Imports

- pandas
- parquetData.transform.bronze_to_silver
- pathlib

### src/parquetData/settings.py

### src/parquetData/transform/__init__.py

### src/parquetData/transform/bronze_to_silver.py

#### Funções

- bronze_to_silver()

#### Imports

- pandas

### src/parquetData/transform/silver_to_gold.py

#### Funções

- silver_to_gold()

#### Imports

- pandas

### tests/test_basic.py

#### Funções

- test_basic_environment()

#### Imports

- pandas
- pathlib
- pyarrow
- pyarrow.parquet

### tests/test_empty.py

#### Funções

- test_empty_dataframe_parquet()

#### Imports

- pandas
- pathlib
- pyarrow
- pyarrow.parquet

### tests/test_errors.py

#### Funções

- test_read_nonexistent_file()

#### Imports

- pyarrow.parquet
- pytest

### tests/test_roundtrip.py

#### Funções

- test_parquet_roundtrip()

#### Imports

- pandas
- pathlib
- pyarrow
- pyarrow.parquet

### tests/test_schema.py

#### Funções

- test_dataframe_schema()

#### Imports

- pandas

