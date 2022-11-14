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
	

.PHONY:
populate:
	python3  scripts/upload_demo_data.py 

	
.PHONY:
down:
	docker compose down;