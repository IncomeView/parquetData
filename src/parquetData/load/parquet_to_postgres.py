from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from parquetData.config import (POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)


def get_engine():
    url = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    return create_engine(url)


def load_parquet_to_postgres(parquet_path: Path, table_name: str, schema: str = "public"):
    df = pd.read_parquet(parquet_path)
    engine = get_engine()

    df.to_sql(
        table_name,
        engine,
        schema=schema,
        if_exists="replace",
        index=False
    )

    print(f"✔ Tabela {schema}.{table_name} carregada no Postgres a partir de {parquet_path}")
