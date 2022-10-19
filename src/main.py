#!/usr/bin/env python3
"""
main - The script builds and hosts the API using a command line interface.
"""


from importlib import import_module
from click import argument, echo, group, option
from dbml_builder import verify
from fastapi import FastAPI
from uvicorn import run as uvicorn_run

DBML_PATH = '../askem.dbml'
DBML_VERSION = 'v0.11.1'
GENERATED_PATH = './generated'


def attach_router(api : FastAPI, router_name : str) -> None:
    """
    Import router module dynamically and attach it to the API

    At runtime, the routes to be used can be specified instead of
    being hardcoded.
    """
    router_package = import_module(f'routers.{router_name}')
    api.include_router(router_package.router, prefix=f'/{router_name}', tags=[router_name])


def build_api(*args : str) -> FastAPI:
    """
    Build an API using a group of specified router modules
    """
    app = FastAPI(docs_url='/') 
    for router_name in args:
        attach_router(app, router_name)
    return app


@group()
def main() -> None:
    """
    Manage the data store API service
    """
    pass


@main.command()
@option('--host', default='0.0.0.0', type=str, help='Address for the API')
@option('--port', default=8000, type=int, help='Port to expose API')
@argument('endpoint', nargs=-1)
def start(host: str, port: int, endpoint: str) -> None:
    """
    Execute data store API using uvicorn
    """
    try:
        assert verify(DBML_VERSION, GENERATED_PATH)
    except AssertionError:
        echo('Failed to start: version mismatch. DBML has either been updated or generated schemas have been modified by users')
        exit()
        
    api = build_api(*endpoint)
    uvicorn_run(
      api,
      host=host,
      port=port,
    )


if __name__ == "__main__":
    main()
