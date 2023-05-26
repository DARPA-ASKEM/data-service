#!/usr/bin/env python3
"""
The module hosts the API using a command line interface.
"""

import logging
from sys import exit as sys_exit

from click import command, echo, option
from sqlalchemy.exc import OperationalError
from uvicorn import run as uvicorn_run

from tds.db import init_dev_content, rdb, stamp, upgrade
from tds.db.elasticsearch import es_client, wait_for_es_up
from tds.settings import settings

logger = logging.Logger("main.py")


def setup_elasticsearch_indexes() -> None:
    """
    Function creates indexes in ElasticSearch.
    """
    # Config should match keyword args on
    # https://elasticsearch-py.readthedocs.io/en/v8.3.2/api.html#elasticsearch.client.IndicesClient.create
    indices = {
        "model": {
            "properties": {
                "model": {
                    "type": "object",
                    "enabled": False,
                },
                "semantics": {
                    "type": "object",
                    "enabled": False,
                },
            },
        },
        "dataset": {},
        "model_configuration": {
            "properties": {
                "model.model": {
                    "type": "object",
                    "enabled": False,
                },
                "model.semantics": {
                    "type": "object",
                    "enabled": False,
                },
            },
        },
    }

    # Wait for elasticsearch to be online and healthy enough to proceed
    es = es_client()
    wait_for_es_up(es)

    # Create indexes
    for idx, config in indices.items():
        index_name = f"{settings.ES_INDEX_PREFIX}{idx}"
        if not es.indices.exists(index=index_name):
            logger.debug("Creating index %s", index_name)
            es.indices.create(index=index_name, mappings=config)


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
