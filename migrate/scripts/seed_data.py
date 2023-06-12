#!/usr/bin/env python
import os
from pathlib import Path

migrate_dir = Path(os.path.dirname(__file__))
seed_dir = f"{migrate_dir.parent}/seeds"


def seed_postgres_data():
    print("Seeding Postgres Data.")


if __name__ == "__main__":
    # Seed ES first so we have the IDs for provenance.
    seed_postgres_data()
