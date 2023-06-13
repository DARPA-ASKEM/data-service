#!/usr/bin/env python
"""
TDS Data seed for postgres.
"""
import json
import os
from pathlib import Path

from alembic import config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tds.autogen import orm

migrate_dir = Path(os.path.dirname(__file__))
alembic_cfg = config.Config(f"{migrate_dir.parent}/alembic.ini")
seed_dir = f"{migrate_dir.parent}/seeds/postgres"
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
SQL_URL = os.getenv("SQL_URL")
SQL_PORT = str(os.getenv("SQL_PORT"))
SQL_DB = os.getenv("SQL_DB")


# pylint: disable-next=(too-many-locals
def seed_postgres_data(conn):
    """
    Function seeds postgres data.
    """
    print("Seeding Postgres Data.")
    session = Session(bind=conn)

    with open(f"{seed_dir}/projects.json", encoding="utf-8") as project_json:
        projects = json.load(project_json)
        for project in projects:
            session.add(orm.Project(**project))

    with open(f"{seed_dir}/publications.json", encoding="utf-8") as publications_json:
        publications = json.load(publications_json)
        for publication in publications:
            session.add(orm.Publication(**publication))

    with open(f"{seed_dir}/project_assets.json", encoding="utf-8") as assets_json:
        assets = json.load(assets_json)
        for asset in assets:
            session.add(orm.ProjectAsset(**asset))

    with open(f"{seed_dir}/provenance.json", encoding="utf-8") as provenance_json:
        provenance = json.load(provenance_json)
        for record in provenance:
            session.add(orm.Provenance(**record))

    with open(
        f"{seed_dir}/model_framework.json", encoding="utf-8"
    ) as model_framework_json:
        frameworks = json.load(model_framework_json)
        for framework in frameworks:
            session.add(orm.ModelFramework(**framework))
    session.commit()


if __name__ == "__main__":
    url = (
        f"postgresql+psycopg2://{SQL_USER}:{SQL_PASSWORD}@{SQL_URL}:{SQL_PORT}/{SQL_DB}"
    )
    engine = create_engine(
        url, pool_size=25, max_overflow=10, connect_args={"connect_timeout": 8}
    )
    with engine.connect() as connection:
        seed_postgres_data(connection)
