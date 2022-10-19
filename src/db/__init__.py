"""
db - A universal configuration for the database.
"""

from os import getenv
from sqlalchemy import create_engine

HOST=getenv('SQL_URL', 'db')
PORT=getenv('SQL_PORT','5432')
USER=getenv('SQL_USER', 'dev')
PASSWORD=getenv('SQL_PASSWORD', 'dev')
URL = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/askem'

ENGINE = create_engine(URL)
    
