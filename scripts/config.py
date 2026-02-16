import  os
from    dotenv import load_dotenv

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
env_path = os.path.join(base_dir, ".env")
load_dotenv(env_path)

#   Banco
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA")
