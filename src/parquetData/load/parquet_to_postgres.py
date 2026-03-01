from pathlib import Path
import time
from sqlalchemy import create_engine
from parquetData.config import (
    POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB,
    POSTGRES_USER, POSTGRES_PASSWORD
)
from parquetData.load.parquet_loader import (
    load_parquet_in_batches,
    list_parquet_files,
    get_table_name
)


def get_engine():
    url = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    return create_engine(url, pool_pre_ping=True)


def load_parquet_to_postgres(parquet_path: Path, table_name: str, schema: str = "public"):
    print(f"\n=== Iniciando carga do arquivo: {parquet_path} ===")
    start_total = time.perf_counter()

    engine = get_engine()
    first_batch = True
    batch_num = 1

    for df in load_parquet_in_batches(parquet_path):
        start_batch = time.perf_counter()

        df.to_sql(
            table_name,
            engine,
            schema=schema,
            if_exists="replace" if first_batch else "append",
            index=False,
            method="multi",
            chunksize=5000
        )

        end_batch = time.perf_counter()
        print(f"  → Batch {batch_num} carregado em {end_batch - start_batch:.2f} segundos")

        first_batch = False
        batch_num += 1

    end_total = time.perf_counter()
    print(f"✔ Tabela {schema}.{table_name} carregada com sucesso")
    print(f"⏱ Tempo total do arquivo: {end_total - start_total:.2f} segundos")
    print("============================================\n")


def load_all_parquet_to_postgres(schema: str = "public"):
    print("\n=== INICIANDO CARGA COMPLETA PARA O POSTGRES ===\n")

    start_global = time.perf_counter()

    files = list_parquet_files()
    print(f"Encontrados {len(files)} arquivos parquet.\n")

    for file in files:
        table = get_table_name(file)
        print(f">>> Carregando arquivo: {file}")
        print(f"    Tabela destino: {table}")

        start_file = time.perf_counter()
        load_parquet_to_postgres(file, table, schema=schema)
        end_file = time.perf_counter()

        print(f"⏱ Tempo total do arquivo {table}: {end_file - start_file:.2f} segundos\n")

    end_global = time.perf_counter()

    print("=== CARGA COMPLETA FINALIZADA ===")
    print(f"⏱ Tempo total da carga completa: {end_global - start_global:.2f} segundos\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Carrega arquivos Parquet para o PostgreSQL.")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Carrega todos os arquivos da camada Bronze (data/fonte)."
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Carrega apenas um arquivo Parquet específico."
    )
    parser.add_argument(
        "--table",
        type=str,
        help="Nome da tabela destino (obrigatório se usar --file)."
    )

    args = parser.parse_args()

    if args.all:
        load_all_parquet_to_postgres()
    elif args.file and args.table:
        load_parquet_to_postgres(args.file, args.table)
    else:
        print("Uso inválido. Exemplos:")
        print("  python3 -m parquetData.load.parquet_to_postgres --all")
        print("  python3 -m parquetData.load.parquet_to_postgres --file data/fonte/creditors.parquet --table creditors")
