"""
tests.main - A basic healthcheck
"""

from dbml_builder import get_dbml_version

from tds.settings import settings


def test_version() -> None:
    """
    Ensure the code is not using an outdated version of the DBML
    """
    assert settings.DBML_VERSION == get_dbml_version(settings.DBML_PATH)
