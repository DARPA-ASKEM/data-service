"""
Configures data store using environment variables
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Data store configuration
    """

<<<<<<< HEAD
    DBML_VERSION: str = "v3"
=======
    DBML_VERSION: str = "v2"
>>>>>>> 219f907 (Bump to `v0.3.0` (#50))
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
