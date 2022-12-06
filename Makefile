SHELL = /bin/bash
LANG = en_US.utf-8
PYTHON = $(shell which python3 || which python)
export LANG

SCHEMA_SQL_FILE = data/001_schema.sql
DATA_SQL_FILE = data/002_data.sql

SCHEMA_FILES = $(shell find tds/schema/ tds/autogen/ -type f -name '*.py')
DATA_FILES = $(shell find scripts/ -type f -name '*.py') $(SCHEMA_SQL_FILE)


.PHONY:init
init:
	cp api.env.sample api.env
	poetry install;
	poetry run pre-commit install
	
.PHONY:tidy
tidy: 
	poetry run pre-commit run;
	poetry run pylint ./tds
	poetry run pylint ./tests
	poetry run pytest

.PHONY:up
up:
	docker compose up --build -d;
	
.PHONY:populate
populate:up
	poetry run python3 scripts/upload_demo_data.py;

	
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
		docker compose exec -u postgres rdb /bin/bash -c 'pg_dump -s -h "localhost" -U "$$POSTGRES_USER" "$$POSTGRES_DB" > /tmp/001_schema.sql'; \
		docker compose cp rdb:/tmp/001_schema.sql ./data; \
	fi

$(DATA_SQL_FILE):$(DATA_FILES)
	if [ -n "$$(docker compose ps | grep rdb)" ]; then \
		echo "Writing out file $(DATA_SQL_FILE)"; \
		docker compose exec -u postgres rdb /bin/bash -c 'pg_dump -a -h "localhost" -U "$$POSTGRES_USER" "$$POSTGRES_DB" > /tmp/002_data.sql'; \
		docker compose cp rdb:/tmp/002_data.sql ./data; \
	fi

.PHONY:db-full
db-full: | $(SCHEMA_SQL_FILE) $(DATA_SQL_FILE)


repopulate-db:
	# Check if we need to rebuild the .sql files by checking if any prerequisite files are newer than the .sql files
	[ -e "$(SCHEMA_SQL_FILE)" ] \
		&& modified_files="$$(find $(SCHEMA_FILES) -newer $(SCHEMA_SQL_FILE))"  \
		|| modified_files="missing"; \
	[ -e "$(DATA_SQL_FILE)" ] \
		&& modified_files="$$modified_files $$(find $(DATA_FILES) -newer $(DATA_SQL_FILE))" \
		|| modified_files="$$modified_files missing"; \
	echo $${modified_files}; \
	if [ "$${modified_files}" != " " ]; then \
		make down; \
		make db-clean; \
		make up; \
		make populate; \
		make db-full; \
	fi
