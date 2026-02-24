import os
import pandas as pd
import pyarrow.parquet as pq

BRONZE_PATH = "data/bronze"

def list_parquet_files():
    return [
        os.path.join(BRONZE_PATH, f)
        for f in os.listdir(BRONZE_PATH)
        if f.endswith(".parquet")
    ]

def load_parquet(file_path):
    table = pq.read_table(file_path)
    df = table.to_pandas()
    return df

def get_table_name(file_path):
    file = os.path.basename(file_path)
    name = file.replace(".parquet", "")
    return name.lower()
