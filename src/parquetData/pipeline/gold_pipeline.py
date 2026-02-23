from pathlib import Path
import pandas as pd

from parquetData.transform.silver_to_gold import silver_to_gold


def run_gold_pipeline(
    local_silver_file: Path,
    local_gold_dir: Path | None = None,
) -> Path:
    if local_gold_dir is None:
        local_gold_dir = Path("data/gold")

    local_gold_dir.mkdir(parents=True, exist_ok=True)

    df_silver = pd.read_parquet(local_silver_file)
    df_gold = silver_to_gold(df_silver)

    gold_file = local_gold_dir / local_silver_file.name
    df_gold.to_parquet(gold_file, index=False)

    return gold_file
