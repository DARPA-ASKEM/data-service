"""
The configured DB engine
"""

from sqlalchemy import create_engine

from tds.settings import settings

# pylint: disable-next=line-too-long
sql_url = f"{settings.SQL_PROTOCOL}://{settings.SQL_USER}:{settings.SQL_PASSWORD}@{settings.SQL_URL}:{settings.SQL_PORT}/{settings.SQL_DB}"
sql_args = {"pool_size": 25, "max_overflow": 10, "connect_args": {"connect_timeout": 8}}
if settings.SQL_CONN_STR:
    sql_url = settings.SQL_CONN_STR
    sql_args = {}
engine = create_engine(sql_url, **sql_args)


async def request_engine():
    """
    Provides postgres engine that can be used by FastAPI Dependencies
    """
    return engine
