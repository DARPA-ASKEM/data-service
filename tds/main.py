#!/usr/bin/env python3
"""
The module hosts the API using a command line interface.
"""

import logging
import os
from sys import exit as sys_exit

from click import command, echo, option
from uvicorn import run as uvicorn_run

logger = logging.Logger("main.py")


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
    # @TODO: This is a temporary bypass so we can remove the DBML
    # without having to fully decouple from the system now. -- Todd Roper, 5/26/23
    is_success, message = (True, "success")
    if not is_success:
        echo(f"Failed to start: {message}.")
        sys_exit()

    uvicorn_run(f"tds.server.configs:{server_config}", host=host, port=port, reload=dev)


if __name__ == "__main__":
    opts = {
        "host": os.getenv("TDS_HOST", "0.0.0.0"),
        "port": os.getenv("TDS_LISTEN_PORT"),
        "dev": os.getenv("DEV_MODE", True),
    }
    cli(**opts)  # pylint: disable=no-value-for-parameter
