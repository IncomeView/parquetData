import time
from scripts.parquet_loader import list_parquet_files, load_parquet, get_table_name
from scripts.db_utils import create_schema, create_table_if_not_exists, insert_dataframe

def run_bronze_pipeline():
    print("🔶 Iniciando pipeline Bronze...")

    # Tempo total do pipeline
    start_total = time.time()

    # Garante que o schema existe
    create_schema("bronze")

    files = list_parquet_files()
    print(f"📦 Encontrados {len(files)} arquivos Parquet para ingestão.")

    for file in files:
        start_file = time.time()  # tempo por arquivo

        try:
            print(f"\n➡️  Processando arquivo: {file}")

            df = load_parquet(file)
            table_name = get_table_name(file)

            print(f"   • Tabela destino: bronze.{table_name}")
            print(f"   • Linhas: {len(df)}")

            create_table_if_not_exists(df, table_name, schema="bronze")
            insert_dataframe(df, table_name, schema="bronze")

            elapsed_file = time.time() - start_file
            print(f"✔ Arquivo {file} carregado com sucesso em {elapsed_file:.2f} segundos.")

        except Exception as e:
            elapsed_file = time.time() - start_file
            print(f"❌ Erro ao processar {file} após {elapsed_file:.2f} segundos.")
            print(f"   • Detalhes do erro: {e}")
            # Continua para o próximo arquivo sem interromper o pipeline
            continue

    # Tempo total
    elapsed_total = time.time() - start_total
    print(f"\n🏁 Pipeline Bronze finalizado em {elapsed_total:.2f} segundos.")

if __name__ == "__main__":
    run_bronze_pipeline()
