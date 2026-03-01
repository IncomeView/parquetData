import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

# Testa leitura/escrita de Parquet (round‑trip)

def test_parquet_roundtrip(tmp_path: Path):
    df_original = pd.DataFrame({
        "id": [1, 2, 3],
        "valor": [10.5, 20.0, 30.7],
        "ativo": [True, False, True],
    })
    file_path = tmp_path / "roundtrip.parquet"
    # Escreve
    table = pa.Table.from_pandas(df_original)
    pq.write_table(table, file_path)
    # Lê
    df_lido = pq.read_table(file_path).to_pandas()
    # Compara
    pd.testing.assert_frame_equal(df_original, df_lido)
