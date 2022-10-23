"""
config.settings - Configures data store using environment variables
"""
from pydantic import BaseSettings


class Settings(BaseSettings): #pylint: disable=too-few-public-methods
    """
    Data store configuration
    """
    sql_url: str = 'db'
    sql_port: int = 5432
    sql_user: str =  'dev'
    sql_password: str =  'dev'


settings = Settings()
