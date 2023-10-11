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

COPY .git/HEAD .git/HEAD
COPY .git/refs .git/refs
RUN grep '^ref:' .git/HEAD && cp .git/`cat .git/HEAD | awk '/^ref: / {print $2}'` /.version || cp .git/HEAD /.version
RUN rm -fr .git

# Poetry complains if the README doesn't exist
COPY README.md README.md
COPY migrations migrations
RUN poetry install --only-root
EXPOSE 8000
CMD ["poetry", "run", "tds"]
