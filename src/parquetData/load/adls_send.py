from pathlib import Path
from typing import Optional

import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient


def _load_env() -> None:
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(env_path)


def get_adls_client() -> DataLakeServiceClient:
    _load_env()

    tenant_id = os.getenv("TENANT_ID")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    storage_account = os.getenv("STORAGE_ACCOUNT")

    if not all([tenant_id, client_id, client_secret, storage_account]):
        raise ValueError("Variáveis de ambiente do ADLS não estão completas.")

    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret,
    )

    account_url = f"https://{storage_account}.dfs.core.windows.net"
    return DataLakeServiceClient(account_url=account_url, credential=credential)


def upload_parquet_to_adls(
    local_file: Path,
    container: Optional[str] = None,
    remote_path: Optional[str] = None,
    overwrite: bool = True,
) -> None:
    _load_env()

    if container is None:
        container = os.getenv("CONTAINER")
    if container is None:
        raise ValueError("Container não informado e CONTAINER não definido no .env.")

    if remote_path is None:
        remote_path = local_file.name

    service_client = get_adls_client()
    file_system = service_client.get_file_system_client(container)

    file_client = file_system.get_file_client(remote_path)

    with open(local_file, "rb") as f:
        file_client.upload_data(f, overwrite=overwrite)
