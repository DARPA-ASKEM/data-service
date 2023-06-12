#!/usr/bin/env python
import json
import os
import sys

print(sys.path)

from pathlib import Path

from alembic import config
from sqlalchemy import create_engine, text
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


def seed_postgres_data(conn):
    print("Seeding Postgres Data.")
    session = Session(bind=conn)

    projects = json.load(open(f"{seed_dir}/projects.json"))

    for project in projects:
        session.add(orm.Project(**project))

    publications = json.load(open(f"{seed_dir}/publications.json"))

    for publication in publications:
        session.add(orm.Publication(**publication))

    assets = json.load(open(f"{seed_dir}/project_assets.json"))

    for asset in assets:
        session.add(orm.ProjectAsset(**asset))

    provenance = json.load(open(f"{seed_dir}/provenance.json"))

    for record in provenance:
        session.add(orm.Provenance(**record))

    frameworks = json.load(open(f"{seed_dir}/model_framework.json"))

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
