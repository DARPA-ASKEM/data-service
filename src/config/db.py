from config.settings import settings
from sqlalchemy import create_engine

url = f'postgresql://{settings.sql_user}:{settings.sql_password}@{settings.sql_url}:{settings.sql_port}/askem'

engine = create_engine(url)
 
