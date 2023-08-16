#!/usr/bin/env bash

alembic -c migrate/alembic.ini upgrade head
python migrate/scripts/start_elasticsearch.py
pytest tests/
#touch /logger.log
#tail -f /logger.log