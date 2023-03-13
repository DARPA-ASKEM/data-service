"""
Handles migrations
"""

from alembic import command
from alembic.config import Config

from tds.settings import settings

# pylint: disable-next=line-too-long
url = f"postgresql://{settings.SQL_USER}:{settings.SQL_PASSWORD}@{settings.SQL_URL}:{settings.SQL_PORT}/askem"
config = Config("./migrate/alembic.ini")
config.set_main_option("sqlalchemy.url", str(url))
config.set_main_option("script_location", "./migrate")


def stamp():
    """
    Apply most recent version to DB
    """
    command.stamp(config, "head")


def upgrade():
    """
    Upgrade DB to latest version
    """
    command.upgrade(config, "head")
