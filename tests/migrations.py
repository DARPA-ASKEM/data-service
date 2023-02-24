"""
Ensure migrations are up to date and upgrades and downgrades work
"""
from pytest import fixture

# Use preconfigured tests provided by `pytest_alembic`
# pylint: disable=unused-import
from pytest_alembic.tests import (  # test_model_definitions_match_ddl,
    test_single_head_revision,
    test_up_down_consistency,
    test_upgrade,
)
from pytest_mock_resources import PostgresConfig, create_postgres_fixture


@fixture(scope="session")
def pmr_postgres_config():
    """
    Match postgres to image used in the docker compose and the
    expectations in `alembic.ini`
    """
    return PostgresConfig(
        image="postgres:15.1",
        port=8032,
        ci_port=8032,
        username="dev",
        password="dev",
        root_database="askem",
    )


@fixture
def alembic_config():
    """Override this fixture to configure the exact alembic context setup required."""
    return {"file": "migrate/alembic.ini"}


alembic_engine = create_postgres_fixture()
