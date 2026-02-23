from pathlib import Path

from parquetData.extract.table_postgres import read_table_to_parquet
from parquetData.load.adls_send import upload_parquet_to_adls
from parquetData.transform.bronze_to_silver import bronze_to_silver


def run_bronze_pipeline(
    table_name: str,
    schema: str | None = None,
    local_bronze_dir: Path | None = None,
    adls_prefix: str | None = None,
) -> None:
    if local_bronze_dir is None:
        local_bronze_dir = Path("data/bronze")

    local_bronze_dir.mkdir(parents=True, exist_ok=True)

    local_parquet = local_bronze_dir / f"{table_name}.parquet"

    # 1) Extrair do PostgreSQL e salvar Bronze local
    read_table_to_parquet(
        table_name=table_name,
        schema=schema,
        output_path=local_parquet,
        index=False,
    )

    # 2) (Opcional) aplicar transformações leves Bronze → Silver em memória
    #    Se quiser salvar Silver local depois, podemos evoluir isso.
    #    Exemplo: ler de volta e aplicar bronze_to_silver
    #    df = pd.read_parquet(local_parquet)
    #    df_silver = bronze_to_silver(df)
    #    ...

    # 3) Enviar Bronze para ADLS
    remote_path = f"bronze/{table_name}.parquet"
    if adls_prefix:
        remote_path = f"{adls_prefix.rstrip('/')}/bronze/{table_name}.parquet"

    upload_parquet_to_adls(
        local_file=local_parquet,
        remote_path=remote_path,
    )
