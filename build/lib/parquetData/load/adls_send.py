from pathlib import Path
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient

from parquetData.config import (
    AZURE_TENANT_ID,
    AZURE_CLIENT_ID,
    AZURE_CLIENT_SECRET,
    AZURE_STORAGE_ACCOUNT_NAME,
    AZURE_STORAGE_FILESYSTEM,
)


def get_adls_client() -> DataLakeServiceClient:
    if not all([
        AZURE_TENANT_ID,
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET,
        AZURE_STORAGE_ACCOUNT_NAME
    ]):
        raise ValueError("Variáveis de ambiente do ADLS não estão completas.")

    credential = ClientSecretCredential(
        tenant_id=AZURE_TENANT_ID,
        client_id=AZURE_CLIENT_ID,
        client_secret=AZURE_CLIENT_SECRET,
    )

    account_url = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net"
    return DataLakeServiceClient(account_url=account_url, credential=credential)


def upload_to_adls(local_file: Path, remote_path: str, overwrite: bool = True) -> None:
    if not AZURE_STORAGE_FILESYSTEM:
        raise ValueError("AZURE_STORAGE_FILESYSTEM não definido no .env")

    service_client = get_adls_client()
    file_system = service_client.get_file_system_client(AZURE_STORAGE_FILESYSTEM)
    file_client = file_system.get_file_client(remote_path)

    with open(local_file, "rb") as f:
        file_client.upload_data(f, overwrite=overwrite)
