"""
Update DB to latest version
"""

from alembic.config import Config

alembic_cfg = Config()
alembic_cfg.set_main_option("script_location", "myapp:migrations")
alembic_cfg.set_main_option("sqlalchemy.url", "postgresql://foo/bar")
alembic_cfg.set_section_option("mysection", "foo", "bar")
