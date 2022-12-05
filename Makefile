SHELL = /bin/bash
LANG = en_US.utf-8
PYTHON = $(shell which python3 || which python)
export LANG


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
	rm -r ./data/*.sql;

#$(eval d001 := "BAR")
data/001_schema.sql:$(shell find tds/schema/ tds/autogen/ -type f -name '*.py')
	$(eval d001 := "BAR")
	docker compose exec -u postgres rdb /bin/bash -c 'pg_dump -s -h "localhost" -U "$$POSTGRES_USER" "$$POSTGRES_DB" > /tmp/001_schema.sql'; \
	docker compose cp rdb:/tmp/001_schema.sql ./data;

data/002_data.sql:data/001_schema.sql $(shell find scripts/ -type f -name '*.py')
	$(eval d002 := "FOO")
	docker compose exec -u postgres rdb /bin/bash -c 'pg_dump -a -h "localhost" -U "$$POSTGRES_USER" "$$POSTGRES_DB" > /tmp/002_data.sql'; \
	docker compose cp rdb:/tmp/002_data.sql ./data;


.PHONY:db-full
db-full: | data/001_schema.sql data/002_data.sql


repopulate-db: | data/001_schema.sql data/002_data.sql
	$(eval needed := $(d001)$(d002))
	@if [ "$(d001)" != "" ]; then \
		make down; make db-clean; make up; make populate; make db-full; \
	fi
