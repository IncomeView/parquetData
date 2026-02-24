import psycopg2
import pandas as pd
from scripts.config import POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

def get_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

def create_schema(schema: str):
    sql = f"CREATE SCHEMA IF NOT EXISTS {schema};"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def create_table_if_not_exists(df: pd.DataFrame, table_name: str, schema: str):
    cols = ", ".join([f'"{c}" TEXT' for c in df.columns])
    sql = f"""
    CREATE TABLE IF NOT EXISTS {schema}.{table_name} (
        {cols}
    );
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def insert_dataframe(df: pd.DataFrame, table_name: str, schema: str):
    conn = get_connection()
    cur = conn.cursor()

    cols = ",".join([f'"{c}"' for c in df.columns])
    values = ",".join(["%s"] * len(df.columns))

    sql = f"""
    INSERT INTO {schema}.{table_name} ({cols})
    VALUES ({values})
    """

    for _, row in df.iterrows():
        cur.execute(sql, tuple(row.astype(str)))

    conn.commit()
    cur.close()
    conn.close()

def run_sql(sql: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
