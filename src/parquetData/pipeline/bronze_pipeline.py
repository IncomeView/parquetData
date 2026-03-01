from pathlib import Path
from parquetData.extract.table_postgres import read_table_to_parquet
from parquetData.settings import ADLS_PATHS
from parquetData.load.adls_send import upload_to_adls

def run_bronze_pipeline(table_name: str, schema: str = "public"):
    try:
        print(f"🔶 Extraindo tabela {schema}.{table_name} do Postgres...")

        local_path = Path(f"data/bronze/{table_name}.parquet")
        local_path.parent.mkdir(parents=True, exist_ok=True)

        read_table_to_parquet(
            table_name=table_name,
            schema=schema,
            output_path=local_path
        )

        print(f"📦 Arquivo Bronze gerado: {local_path}")

        adls_path = f"{ADLS_PATHS['bronze']}{table_name}.parquet"
        upload_to_adls(local_path, adls_path)

        print(f"🚀 Enviado para ADLS: {adls_path}")

    except Exception as e:
        print(f"❌ Erro ao processar {schema}.{table_name}: {e}")
