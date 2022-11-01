"""
src.server.configs - Configured ASGI apps to be launched by Uvicorn
"""
from src.db import engine
from src.server.build import build_api

full = build_api(engine)
