"""
Constructs API given specified router
"""

from importlib import import_module, metadata
from pkgutil import iter_modules

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

API_DESCRIPTION = "TDS handles data between TERArium and other ASKEM components."


def load_module_routers(api):
    """
    Function loads the module router objects and registers them with FastAPI.
    """
    modules = import_module("tds.modules")
    for mod in iter_modules(modules.__path__):
        module = import_module(f"tds.modules.{mod.name}")
        api.include_router(
            module.router, tags=module.TAGS, prefix="/" + module.ROUTE_PREFIX
        )


def build_api() -> FastAPI:
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

    return api
