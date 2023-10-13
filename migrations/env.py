"""
The environment file provides the necessary context for the migrations

> This is a Python script that is run whenever the alembic migration tool is invoked.
> At the very least, it contains instructions to configure and generate a
> SQLAlchemy engine, procure a connection from that engine along with a transaction,
> and then invoke the migration engine, using the connection as a source of database
> connectivity.

Source: 'https://alembic.sqlalchemy.org/en/latest/tutorial.html'
"""
from logging.config import fileConfig

# pylint: disable=no-member
# NOTE: context doesn't exist until runtime
from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.types import Enum

from tds.db.base import RelationalDatabaseBase
from tds.db.helpers import ensure_models_are_loaded
from tds.settings import settings

ensure_models_are_loaded()

target_metadata = RelationalDatabaseBase.metadata
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_rdb_url() -> str:
    """
    Generates the url for the RDB from the settings
    """
    params = {
        "SQL_USER": settings.SQL_USER,
        "SQL_PASSWORD": settings.SQL_PASSWORD,
        "SQL_URL": settings.SQL_URL,
        "SQL_PORT": settings.SQL_PORT,
        "SQL_DB": settings.SQL_DB,
    }
    url = config.get_main_option("sqlalchemy.url")
    url = url.format(**params)
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
    url = get_rdb_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def custom_type_comparison(context, insp_col, metadata_col, insp_type, metadata_type):
    if isinstance(insp_type, Enum) or isinstance(metadata_type, Enum):
        old_enums = set(insp_type.enums)
        new_enums = set(metadata_type.enums)

        if old_enums != new_enums:
            template_args = context.environment_context.context_opts["template_args"]
            extra_ops = template_args.get("extra_ops", None)
            if extra_ops is None:
                extra_ops = []
                template_args["extra_ops"] = extra_ops

            if old_enums.issubset(new_enums):
                print(f"Adding new values for enum type `{{metadata_type.name}}`.")
                sql = "\n".join(
                    [
                        f"ALTER TYPE {metadata_type.name} ADD VALUE '{value}';"
                        for value in (new_enums - old_enums)
                    ]
                )
                new_op = f'''op.execute(sqltext="""{sql}""")\n'''
                if new_op not in extra_ops:
                    extra_ops.append(new_op)
            else:
                warnings = [
                    f"# ATTENTION: Enum type `{metadata_type.name}` cannot be automatically migrated!.",
                    f"# Current enum values in the database: ({', '.join(old_enums)})",
                    f"# Enum definition in the code:         ({', '.join(new_enums)})",
                ]
                print("\n".join(warnings))
                if warnings[0] not in extra_ops:
                    extra_ops.extend(warnings)
    return None


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = get_rdb_url()
    connectable = context.config.attributes.get("connection", None)

    if connectable is None:
        connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=custom_type_comparison,
            compare_server_default=True,
            include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
