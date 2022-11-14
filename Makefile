SHELL = /bin/bash
LANG = en_US.utf-8
PYTHON = $(shell which python3 || which python)
export LANG


.PHONY:init
init:
	poetry install;
	

.PHONY:
up:
	docker compose up --build -d;
	python3  upload_bio_models.py ${PARAMS} 

.PHONY:
down:
	docker compose down;