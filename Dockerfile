FROM python:latest
RUN apt update 2> /dev/null
RUN apt install -y postgresql postgresql-contrib
RUN pip install poetry
WORKDIR /api
ADD poetry.lock poetry.lock
ADD pyproject.toml pyproject.toml
ADD askem.dbml askem.dbml
COPY src src 
EXPOSE 8000
WORKDIR /api/src
CMD ["poetry", "run", "ads"]
