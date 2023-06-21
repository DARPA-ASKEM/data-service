#!/bin/bash

PG_HOST=${PG_HOST:-rdb}
PG_USER=${PG_USER:-dev}
PG_PASSWORD=${PG_PASSWORD:-dev}
PG_PORT=${PG_PORT:-5432}
PG_DB=${PG_DB:-askem}
PG_HOST=${SQL_URL:-rdb}
PG_USER=${SQL_USER:-dev}
PG_PASSWORD=${SQL_PASSWORD:-dev}
PG_PORT=${SQL_PORT:-5432}
PG_DB=${SQL_DB:-askem}

echo Waiting for ${PG_HOST} to be available
while ! nc -z ${PG_HOST} ${PG_PORT}; do
    sleep 0.2
done
echo ${PG_HOST} is now available. Continuing.
psql --command="\COPY provenance TO '/var/lib/neo4j/import/provenance.csv' WITH (FORMAT CSV, HEADER);" postgresql://${PG_USER}:${PG_PASSWORD}@${PG_HOST}:${PG_PORT}/${PG_DB}

set -m
/startup/docker-entrypoint.sh neo4j &

# TODO: run this using apoc.initialize
echo Waiting for neo4j service to be available
while ! nc -z localhost 7474; do
    sleep 0.2
done
echo neo4j is now available. Continuing.
cypher-shell -u neo4j -p password -f /tmp/populate-cache.cypher --non-interactive
echo "Loaded all data"

fg %1
