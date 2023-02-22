SHELL = /bin/bash
LANG = en_US.utf-8
PYTHON = $(shell which python3 || which python)
export LANG

SQL_HASH_FILE = data/.version
SCHEMA_SQL_FILE = data/001_schema.sql
DATA_SQL_FILE = data/002_data.sql

SCHEMA_FILES = $(shell find tds/schema/ tds/autogen/ -type f -name '*.py')
DATA_PY_FILES = $(shell find scripts/ -type f -name '*.py') 
DATA_FILES = $(DATA_PY_FILES) $(SCHEMA_SQL_FILE)
SQL_HASH = $(shell md5sum $(SCHEMA_FILES) $(DATA_PY_FILES) | md5sum | cut -c -32)


.PHONY:init
init:
	cp api.env.sample api.env
	poetry install;
	poetry run pre-commit install
	
.PHONY:tidy
tidy: 
	poetry run pre-commit run;
	poetry run pylint ./tds
	poetry run pylint ./migrate
	poetry run pylint ./migrate/versions
	poetry run pylint ./tests
	poetry run pytest

.PHONY:up
up:
	docker compose up --build -d;
	
.PHONY: gen-migration
gen-migration:
	poetry run alembic -c migrate/alembic.ini revision --autogenerate -m "$(message)"

.PHONY:populate
populate:up
	poetry run python3 scripts/upload_demo_data.py || (sleep 3; docker compose logs api; false);

.PHONY:fake
fake:up
	poetry run python3 scripts/upload_demo_data.py --fake
	
.PHONY:down
down:
	docker compose down;

.PHONY:db-clean
db-clean:
	rm -f ./data/*.sql; \
	rm -f ./data/datasets/*/*; \
	rmdir ./data/datasets/*;

$(SCHEMA_SQL_FILE):$(SCHEMA_FILES)
	if [ -n "$$(docker compose ps | grep rdb)" ]; then \
		echo "Writing out file $(SCHEMA_SQL_FILE)"; \
		docker compose exec -u postgres rdb /bin/bash -c 'pg_dump -s -h "localhost" -U "$$POSTGRES_USER" "$$POSTGRES_DB" > /tmp/001_schema.sql' && \
		docker compose cp rdb:/tmp/001_schema.sql ./data; \
	fi

$(DATA_SQL_FILE):$(DATA_FILES)
	if [ -n "$$(docker compose ps | grep rdb)" ]; then \
		echo "Writing out file $(DATA_SQL_FILE)"; \
		docker compose exec -u postgres rdb /bin/bash -c 'pg_dump -a -h "localhost" -U "$$POSTGRES_USER" "$$POSTGRES_DB" > /tmp/002_data.sql' && \
		docker compose cp rdb:/tmp/002_data.sql ./data; \
	fi

.PHONY:db-full
db-full: | $(SCHEMA_SQL_FILE) $(DATA_SQL_FILE)


.PHONY:repopulate-db
repopulate-db:
	# Check if we need to rebuild the .sql files by checking if any prerequisite files are newer than the .sql files
	if [ "$(SQL_HASH)" != "$$(cat $(SQL_HASH_FILE))" ]; then \
		make down; \
		make db-clean; \
		NEO4J_ENABLED=False make up && \
		sleep 1 && \
		NEO4J_ENABLED=False make populate && \
		make db-full && \
		echo '$(SQL_HASH)' > $(SQL_HASH_FILE); \
	fi
