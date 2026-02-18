import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

# Testa DataFrames vazios

def test_empty_dataframe_parquet(tmp_path: Path):
    df = pd.DataFrame()
    file_path = tmp_path / "empty.parquet"
    # Escreve
    table = pa.Table.from_pandas(df)
    pq.write_table(table, file_path)
    # Lê
    df_lido = pq.read_table(file_path).to_pandas()
    # Compara
    pd.testing.assert_frame_equal(df, df_lido)
