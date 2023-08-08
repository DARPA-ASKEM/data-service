#!/usr/bin/env bash

alembic -c migrate/alembic.ini upgrade head
pytest tests/
#touch /logger.log
#tail -f /logger.log