#!/usr/bin/env python3
"""
The module hosts the API using a command line interface.
"""

import logging
from sys import exit as sys_exit

from click import command, echo, option
from dbml_builder import verify
from elasticsearch.client import CatClient
from sqlalchemy.exc import OperationalError
from uvicorn import run as uvicorn_run

from tds.db import init_dev_content, rdb, stamp, upgrade
from tds.db.elasticsearch import es, wait_for_es_up
from tds.settings import settings

logger = logging.Logger("main.py")

def setup_elasticsearch_indexes() -> None:
    # Config should match keyword args on https://elasticsearch-py.readthedocs.io/en/v8.3.2/api.html#elasticsearch.client.IndicesClient.create
    indices = {
        "model": {},
    }

    # Wait for elasticsearch to be online and healthy enough to proceed
    wait_for_es_up()

    # Create indexes
    for idx, config in indices.items():
        if not es.indices.exists(index=idx):
            logger.debug(f"Creating index {idx}")
            es.indices.create(index=idx, body=config)


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
    setup_elasticsearch_indexes()
    if dev:
        try:
            echo("Connecting to DB... ", nl=False)
            connection = rdb.connect()
        except OperationalError:
            echo("FAILED: DB NOT CONNECTED")
        else:
            echo("SUCCESS")
            if len(rdb.table_names()) == 0:
                init_dev_content(connection)
                stamp()
                echo("STAMPED WITH CURRENT DB VERSION")
            else:
                upgrade()
                echo("DB IS UP TO DATE")

    uvicorn_run(f"tds.server.configs:{server_config}", host=host, port=port, reload=dev)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
