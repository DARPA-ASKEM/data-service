FROM python:3.10
RUN apt update 2> /dev/null
RUN apt install -y postgresql postgresql-contrib
RUN pip install poetry
WORKDIR /api
ADD poetry.lock poetry.lock
ADD pyproject.toml pyproject.toml
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
COPY tests tests
COPY tds tds 
COPY graph_relations.json graph_relations.json

# Poetry complains if the README doesn't exist
COPY README.md README.md
COPY data/datasets /datasets
COPY migrate migrate
RUN poetry install --only-root
EXPOSE 8000
CMD ["poetry", "run", "tds"]
