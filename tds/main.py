#!/usr/bin/env python3
"""
The module hosts the API using a command line interface.
"""

from sys import exit as sys_exit

from click import command, echo, option
from dbml_builder import verify
from sqlalchemy.exc import OperationalError
from uvicorn import run as uvicorn_run

from tds.db import init_dev_content, rdb
from tds.settings import settings


@command()
@option("--host", default="0.0.0.0", type=str, help="Address for the API")
@option("--port", default=8000, type=int, help="Port to expose API")
@option("--dev", default=True, type=bool, help="Set development flag")
@option(
    "--server-config",
    default="full",
    type=str,
    help="Name of server config to use from `tds.server.configs`",
)
def cli(host: str, port: int, dev: bool, server_config: str) -> None:
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
            connection = rdb.connect()
        except OperationalError:
            echo("FAILED: DB NOT CONNECTED")
        else:
            echo("SUCCESS")
            init_dev_content(connection)
    uvicorn_run(f"tds.server.configs:{server_config}", host=host, port=port, reload=dev)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
