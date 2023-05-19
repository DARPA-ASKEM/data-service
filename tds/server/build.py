"""
Constructs API given specified router
"""

from importlib import import_module, metadata
from pkgutil import iter_modules
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

API_DESCRIPTION = "TDS handles data between TERArium and other ASKEM components."


def find_valid_routers() -> List[str]:
    """
    Generate list of module names that are possible to import
    """
    router = import_module("tds.routers")
    return [module.name for module in iter_modules(router.__path__)]


def attach_router(api: FastAPI, router_name: str) -> None:
    """
    Import router module dynamically and attach it to the API

    At runtime, the routes to be used can be specified instead of
    being hardcoded.
    """
    router_package = import_module(f"tds.routers.{router_name}")
    api.include_router(
        router_package.router, tags=[router_name], prefix="/" + router_name
    )

    if api.openapi_tags is None:
        api.openapi_tags = []
    api.openapi_tags.append(
        {"name": router_name, "description": router_package.__doc__}
    )


def load_module_routers(api):
    modules = import_module("tds.modules")
    for mod in iter_modules(modules.__path__):
        module = import_module(f"tds.modules.{mod.name}")
        api.include_router(
            module.router, tags=module.TAGS, prefix="/" + module.ROUTE_PREFIX
        )


def build_api(*args: str) -> FastAPI:
    """
    Build an API using a group of specified router modules
    """
    api = FastAPI(
        title="TERArium Data Service",
        version=metadata.version("tds"),
        description=API_DESCRIPTION,
        docs_url="/",
    )
    origins = [
        "http://localhost",
        "http://localhost:8080",
    ]
    api.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Load routers from the modules package.
    load_module_routers(api)

    for router_name in args if len(args) != 0 else find_valid_routers():
        attach_router(api, router_name)

    return api
