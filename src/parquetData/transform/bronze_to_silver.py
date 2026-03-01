import pandas as pd


def bronze_to_silver(df: pd.DataFrame) -> pd.DataFrame:
    # Placeholder: aqui entram regras de limpeza, tipos, normalização etc.
    # Exemplo simples: remover linhas totalmente vazias
    df = df.dropna(how="all")
    return df
