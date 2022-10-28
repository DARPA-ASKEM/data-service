FROM python:latest
RUN apt update 2> /dev/null
RUN apt install -y postgresql postgresql-contrib
RUN pip install poetry
WORKDIR /api
ADD poetry.lock poetry.lock
ADD pyproject.toml pyproject.toml
ADD askem.dbml askem.dbml
RUN poetry config virtualenvs.create false
COPY src src 
# Poetry complains if the README doesn't exist
COPY README.md README.md
# Optimally, the install would BEFORE copying `src`
RUN poetry install
EXPOSE 8000
CMD ["poetry", "run", "ads"]
