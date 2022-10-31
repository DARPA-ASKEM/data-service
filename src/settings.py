"""
config.settings - Configures data store using environment variables
"""
from pydantic import BaseSettings


class Settings(BaseSettings):  # pylint: disable=too-few-public-methods
    """
    Data store configuration
    """

    dbml_version: str = "v0.11.5"
    generated_path: str = "./src/generated"
    dbml_path: str = "./askem.dbml"
    sql_url: str = "db"
    sql_port: int = 8032
    sql_user: str = "dev"
    sql_password: str = "dev"


settings = Settings()
