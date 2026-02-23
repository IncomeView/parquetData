from pathlib import Path
import pandas as pd

from parquetData.transform.bronze_to_silver import bronze_to_silver


def run_silver_pipeline(
    local_bronze_file: Path,
    local_silver_dir: Path | None = None,
) -> Path:
    if local_silver_dir is None:
        local_silver_dir = Path("data/silver")

    local_silver_dir.mkdir(parents=True, exist_ok=True)

    df_bronze = pd.read_parquet(local_bronze_file)
    df_silver = bronze_to_silver(df_bronze)

    silver_file = local_silver_dir / local_bronze_file.name
    df_silver.to_parquet(silver_file, index=False)

    return silver_file
