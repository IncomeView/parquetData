import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

# Testa se o ambiente está saudável (pytest, pandas, pyarrow funcionando)

def test_basic_environment():
    # Teste simples para garantir que o ambiente está funcionando
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    assert not df.empty
