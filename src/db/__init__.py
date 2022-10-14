from os import getenv
from sqlalchemy import create_engine

URL=getenv('SQL_URL', 'localhost')
PORT=int(getenv('SQL_PORT','8001'))
USER=getenv('SQL_USER', 'dev')
PASSWORD=getenv('SQL_password', 'dev')

ENGINE = create_engine(
    f'postgresql://{USER}:{PASSWORD}@{URL}:{PORT}/askem'
)
