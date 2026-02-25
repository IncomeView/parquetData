from pathlib import Path
from typing import Optional
import pandas as pd
from sqlalchemy import create_engine
from parquetData.config import (POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)


def get_postgres_engine():
    if not all([POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD]):
        raise ValueError("Variáveis de ambiente do PostgreSQL não estão completas.")

    url = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    return create_engine(url)


def read_table(table_name: str, schema: Optional[str] = None) -> pd.DataFrame:
    engine = get_postgres_engine()

    full_name = f"{schema}.{table_name}" if schema else table_name
    query = f"SELECT * FROM {full_name}"

    return pd.read_sql(query, engine)


def read_table_to_parquet(
    table_name: str,
    output_path: Path,
    schema: Optional[str] = None,
    index: bool = False,
) -> Path:
    df = read_table(table_name=table_name, schema=schema)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=index)
    return output_path
