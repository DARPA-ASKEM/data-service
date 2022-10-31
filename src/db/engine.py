"""
src.db.engine - The configured DB engine
"""

from sqlalchemy import create_engine

from src.settings import settings

# pylint: disable-next=line-too-long
url = f"postgresql://{settings.sql_user}:{settings.sql_password}@{settings.sql_url}:{settings.sql_port}/askem"
engine = create_engine(url, connect_args={"connect_timeout": 8})
