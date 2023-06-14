#!/usr/bin/env python
"""
TDS Data seed for postgres.
"""
import json
import os
from pathlib import Path

from alembic import config
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
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

pg_data_load = {
    "model_framework": orm.ModelFramework,
    "persons": orm.Person,
    "projects": orm.Project,
    "project_assets": orm.ProjectAsset,
    "provenance": orm.Provenance,
    "publications": orm.Publication,
}


# pylint: disable-next=(too-many-locals
def seed_postgres_data(conn):
    """
    Function seeds postgres data.
    """
    print("Seeding Postgres Data.")
    for key in pg_data_load.keys():
        seed_data_into_db(conn=conn, json_file=key, model_class=pg_data_load[key])


def seed_data_into_db(conn, json_file: str, model_class):
    # sqlalchemy.exc.
    session = Session(bind=conn)
    print(f"Seeding {json_file.capitalize()}")
    with open(f"{seed_dir}/{json_file}.json", encoding="utf-8") as data_json:
        data = json.load(data_json)
        for row in data:
            session.add(model_class(**row))
        try:
            session.commit()
        except IntegrityError as in_e:
            print(in_e.orig)


if __name__ == "__main__":
    url = (
        f"postgresql+psycopg2://{SQL_USER}:{SQL_PASSWORD}@{SQL_URL}:{SQL_PORT}/{SQL_DB}"
    )
    engine = create_engine(
        url, pool_size=25, max_overflow=10, connect_args={"connect_timeout": 8}
    )
    with engine.connect() as connection:
        seed_postgres_data(connection)
