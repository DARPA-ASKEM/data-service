#!/usr/bin/env python3
"""
src.main - The script hosts the API using a command line interface.
"""

from sys import exit as sys_exit

from click import command, echo, option
from dbml_builder import verify
from sqlalchemy.exc import OperationalError
from src.db import engine, init_dev_content
from src.settings import settings
from uvicorn import run as uvicorn_run


@command()
@option("--host", default="0.0.0.0", type=str, help="Address for the API")
@option("--port", default=8000, type=int, help="Port to expose API")
@option("--dev", default=True, type=bool, help="Set development flag")
@option("--name", default="full", type=str, help="Name of configured API to use")
def cli(host: str, port: int, dev: bool, name: str) -> None:
    """
    Execute data store API using uvicorn
    """
    is_success, message = verify(settings.DBML_VERSION, settings.GENERATED_PATH)
    if not is_success:
        echo(f"Failed to start: {message}.")
        sys_exit()
    if dev:
        try:
            echo("Connecting to DB... ", nl=False)
            connection = engine.connect()
        except OperationalError:
            echo("FAILED: DB NOT CONNECTED")
        else:
            echo("SUCCESS")
            init_dev_content(connection)
    uvicorn_run(f"src.server.configs:{name}", host=host, port=port, reload=dev)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
