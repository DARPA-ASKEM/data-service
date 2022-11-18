SHELL = /bin/bash
LANG = en_US.utf-8
PYTHON = $(shell which python3 || which python)
export LANG


.PHONY:init
init:
	poetry install;
	poetry run pre-commit install
	
.PHONY:
tidy: 
	poetry run pre-commit run;
	poetry run pylint ./tds
	poetry run pylint ./tests
	poetry run pytest

.PHONY:
up:
	docker-compose up --build -d;
	

.PHONY:
populate:
	python3 scripts/upload_demo_data.py;

	
.PHONY:
down:
	docker-compose down;
