import pyarrow.parquet as pq
import pytest

# Testa erros esperados

def test_read_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        pq.read_table("arquivo_inexistente.parquet")
