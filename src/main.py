#!/usr/bin/env python3
"""
main - The script builds and hosts the API using a command line interface.
"""

from importlib import import_module
from pkgutil import iter_modules
from sys import exit as sys_exit
from typing import List

from click import argument, command, echo, option
from dbml_builder import verify
from fastapi import FastAPI
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import OperationalError
from uvicorn import run as uvicorn_run

from src.db import engine as live_engine
from src.db import init_dev_content
from src.settings import settings


def find_valid_routers() -> List[str]:
    """
    Generate list of module names that are possible to import
    """
    router = import_module("src.routers")
    return [module.name for module in iter_modules(router.__path__)]


def attach_router(api: FastAPI, engine: Engine, router_name: str) -> None:
    """
    Import router module dynamically and attach it to the API

    At runtime, the routes to be used can be specified instead of
    being hardcoded.
    """
    router_package = import_module(f"src.routers.{router_name}")
    api.include_router(router_package.gen_router(engine), tags=[router_name])


def build_api(engine: Engine, *args: str) -> FastAPI:
    """
    Build an API using a group of specified router modules
    """
    app = FastAPI(docs_url="/")
    for router_name in args if len(args) != 0 else find_valid_routers():
        attach_router(app, engine, router_name)
    return app


@command()
@option("--host", default="0.0.0.0", type=str, help="Address for the API")
@option("--port", default=8000, type=int, help="Port to expose API")
@option("--dev", default=True, type=bool, help="Set development flag")
@argument("endpoint", nargs=-1)
def main(host: str, port: int, dev: bool, endpoint: str) -> None:
    """
    Execute data store API using uvicorn
    """
    is_success, message = verify(settings.DBML_VERSION, settings.GENERATED_PATH)
    if not is_success:
        # pylint: disable-next=line-too-long
        echo(f"Failed to start: {message}.")
        sys_exit()
    if dev:
        try:
            echo("Connecting to DB... ", nl=False)
            connection = live_engine.connect()
        except OperationalError:
            echo("FAILED: DB NOT CONNECTED")
        else:
            echo("SUCCESS")
            init_dev_content(connection)

    api = build_api(live_engine, *endpoint)
    uvicorn_run(
        api,
        host=host,
        port=port,
    )


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
