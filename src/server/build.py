"""
src.server.build - Constructs API given specified router
"""

from importlib import import_module
from pkgutil import iter_modules
from typing import List

from fastapi import FastAPI
from sqlalchemy.engine.base import Engine


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
