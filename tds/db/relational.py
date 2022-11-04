"""
tds.db.relational - The configured DB engine
"""

from sqlalchemy import create_engine

from tds.settings import settings

# pylint: disable-next=line-too-long
url = f"postgresql://{settings.SQL_USER}:{settings.SQL_PASSWORD}@{settings.SQL_URL}:{settings.SQL_PORT}/askem"
engine = create_engine(url, connect_args={"connect_timeout": 8})


async def request_engine():
    """
    Provides engine that can be used by FastAPI Dependencies
    """
    return engine
