import click
from pathlib import Path
from parquetData.pipeline.bronze_pipeline import run_bronze_pipeline
from parquetData.settings import BRONZE_TABLES
from parquetData.load.parquet_to_postgres import load_parquet_to_postgres


@click.group()
def cli():
    """CLI do projeto parquetData."""
    pass

@cli.command()
@click.argument("table_name")
@click.option("--schema", default="public")
def bronze(table_name, schema):
    """Executa o pipeline Bronze para uma tabela específica."""
    run_bronze_pipeline(table_name, schema)

@cli.command()
def bronze_all():
    """Executa o pipeline Bronze para todas as tabelas configuradas."""
    for schema, tables in BRONZE_TABLES.items():
        for table in tables:
            run_bronze_pipeline(table, schema)

@cli.command()
@click.option("--schema", default="public")
def load_parquet_all(schema):
    """Carrega todos os arquivos .parquet da pasta data/fonte para o Postgres."""
    fonte_dir = Path(__file__).resolve().parents[2] / "data" / "fonte"

    if not fonte_dir.exists():
        print(f"❌ Pasta não encontrada: {fonte_dir}")
        return

    parquet_files = list(fonte_dir.glob("*.parquet"))

    if not parquet_files:
        print("❌ Nenhum arquivo .parquet encontrado em data/fonte")
        return

    for parquet_file in parquet_files:
        table_name = parquet_file.stem  # nome do arquivo vira nome da tabela
        load_parquet_to_postgres(parquet_file, table_name, schema)

    print("🚀 Todos os arquivos .parquet foram carregados no Postgres.")


if __name__ == "__main__":
    cli()
