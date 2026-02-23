import os
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient

env_path = Path(__file__).resolve().parents[1] / ".env" 
load_dotenv(env_path)

tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
account_name = os.getenv("STORAGE_ACCOUNT")
container_name = os.getenv("CONTAINER")

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

service = DataLakeServiceClient(
    account_url=f"https://{account_name}.dfs.core.windows.net",
    credential=credential
)

file_system = service.get_file_system_client(container_name)
paths = list(file_system.get_paths())

print("Conexão OK. Objetos encontrados:", paths)
