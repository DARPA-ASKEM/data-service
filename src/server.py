#!/usr/bin/env python3

from click import command, option
from fastapi import FastAPI
from importlib import import_module
from uvicorn import run as uvicorn_run


def attach_router(api : FastAPI, router_name : str) -> None:
    router_package = import_module(f'routers.{router_name}')
    api.include_router(router_package.router, prefix=f'/{router_name}', tags=[router_name])


def build_api(*args : str) -> FastAPI:
    app = FastAPI(docs_url='/') 
    for router_name in args:
        attach_router(app, router_name)
    return app


@command()
@option('--host', default='0.0.0.0', type=str, help='Address for the API')
@option('--port', default=8000, type=int, help='Port to expose API')
@option('--endpoint', multiple=True, type=str, help='Set of endpoints to include in API')
def main(host: str, port: int, endpoint: str) -> None:
    """
    Execute data store API using uvicorn
    """
    api = build_api(*endpoint) 
    uvicorn_run(
      api,
      host=host,
      port=port,
    )


if __name__ == "__main__":
    main()


