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


def upload_to_adls(local_file: Path, remote_path: str, overwrite: bool = True):
    service_client = get_adls_client()
    file_system = service_client.get_file_system_client(AZURE_STORAGE_FILESYSTEM)
    file_client = file_system.get_file_client(remote_path)

    if overwrite:
        file_client.create_file()

    chunk_size = 4 * 1024 * 1024  # 4 MB
    offset = 0

    with open(local_file, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break

            file_client.append_data(data, offset=offset, length=len(data))
            offset += len(data)

    file_client.flush_data(offset)
    print(f"✔️ Upload concluído: {remote_path}")

