#!/usr/bin/env bash

echo "Running migrations."
alembic -c migrations/alembic.ini upgrade head 2>/dev/stdout
echo "Migrations complete."
exit 0
