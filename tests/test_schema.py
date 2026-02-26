import pandas as pd

# Testa estrutura mínima de DataFrames

def test_dataframe_schema():
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "valor": [10.0, 20.0, 30.0],
    })
    assert list(df.columns) == ["id", "valor"]
    assert df["id"].dtype == "int64"
    assert df["valor"].dtype in ["float64", "float32"]
