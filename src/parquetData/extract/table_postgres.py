from pathlib import Path
from typing import Optional

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


def _load_env() -> None:
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(env_path)


def get_postgres_engine():
    _load_env()

    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")
    host = os.getenv("PG_HOST")
    port = os.getenv("PG_PORT", "5432")
    database = os.getenv("PG_DATABASE")

    if not all([user, password, host, database]):
        raise ValueError("Variáveis de ambiente do PostgreSQL não estão completas.")

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    return create_engine(url)


def read_table(table_name: str, schema: Optional[str] = None) -> pd.DataFrame:
    engine = get_postgres_engine()

    if schema:
        full_name = f"{schema}.{table_name}"
    else:
        full_name = table_name

    query = f"SELECT * FROM {full_name}"
    df = pd.read_sql(query, engine)
    return df


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
