"""
The environment file provides the necessary context for the migrations

> This is a Python script that is run whenever the alembic migration tool is invoked.
> At the very least, it contains instructions to configure and generate a
> SQLAlchemy engine, procure a connection from that engine along with a transaction,
> and then invoke the migration engine, using the connection as a source of database
> connectivity.

Source: 'https://alembic.sqlalchemy.org/en/latest/tutorial.html'
"""
import os
import re
from logging.config import fileConfig

# pylint: disable=no-member
# NOTE: context doesn't exist until runtime
from alembic import context
from sqlalchemy import create_engine, engine_from_config, pool

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def setup_context():
    tokens = {
        "SQL_USER": os.getenv("SQL_USER"),
        "SQL_PASSWORD": os.getenv("SQL_PASSWORD"),
        "SQL_URL": os.getenv("SQL_URL"),
        "SQL_PORT": str(os.getenv("SQL_PORT")),
        "SQL_DB": os.getenv("SQL_DB"),
    }
    url = config.get_main_option("sqlalchemy.url")
    url = re.sub(r"\${(.+?)}", lambda m: tokens[m.group(1)], url)

    context.configure(
        url=url,
        dialect_opts={"paramstyle": "named"},
    )

    return url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = setup_context()

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = setup_context()
    connectable = context.config.attributes.get("connection", None)

    if connectable is None:
        connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
