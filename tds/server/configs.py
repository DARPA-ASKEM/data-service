"""
tds.server.configs - Configured ASGI apps to be launched by Uvicorn
"""
from tds.server.build import build_api

full = build_api()
