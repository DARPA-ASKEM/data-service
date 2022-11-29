"""
Configures data store using environment variables
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Data store configuration
    """

    DBML_VERSION: str = "v4"
    GENERATED_PATH: str = "./tds/autogen"
    DBML_PATH: str = "./askem.dbml"
    SQL_URL: str = "rdb"
    SQL_PORT: int = 8032
    SQL_USER: str = "dev"
    SQL_PASSWORD: str = "dev"
    DKG_URL = "http://34.230.33.149"
    DKG_API_PORT = 8771
    DKG_DESC_PORT = 8772


settings = Settings()
