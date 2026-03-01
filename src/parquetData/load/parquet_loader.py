import os
import pyarrow.dataset as ds

BRONZE_PATH = "data/fonte"

def list_parquet_files():
    return [
        os.path.join(BRONZE_PATH, f)
        for f in os.listdir(BRONZE_PATH)
        if f.endswith(".parquet")
    ]

def load_parquet_in_batches(file_path, batch_size=50000):
    dataset = ds.dataset(file_path, format="parquet")
    for batch in dataset.to_batches(batch_size=batch_size):
        yield batch.to_pandas()

def get_table_name(file_path):
    return os.path.basename(file_path).replace(".parquet", "").lower()
