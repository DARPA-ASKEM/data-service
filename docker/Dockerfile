FROM python:3.10
RUN apt update 2> /dev/null
RUN apt install -y postgresql postgresql-contrib
RUN pip install poetry
WORKDIR /api
ADD poetry.lock poetry.lock
ADD pyproject.toml pyproject.toml
RUN poetry config virtualenvs.create false
COPY tds tds
COPY graph_relations.json graph_relations.json
RUN mkdir /api/tests && touch /api/tests/test.py
RUN poetry install --no-dev

EXPOSE 8000
CMD ["poetry", "run", "tds"]
