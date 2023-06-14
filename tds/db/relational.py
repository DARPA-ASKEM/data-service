"""
The configured DB engine
"""

from sqlalchemy import create_engine

from tds.settings import settings

# pylint: disable-next=line-too-long
url = f"postgresql+psycopg2://{settings.SQL_USER}:{settings.SQL_PASSWORD}@{settings.SQL_URL}:{settings.SQL_PORT}/{settings.SQL_DB}"
engine = create_engine(
    url, pool_size=25, max_overflow=10, connect_args={"connect_timeout": 8}
)


async def request_engine():
    """
    Provides postgres engine that can be used by FastAPI Dependencies
    """
    return engine
