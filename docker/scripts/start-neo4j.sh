#!/bin/bash

echo Waiting for rdb to be available
while ! nc -z rdb 5432; do
    sleep 0.2
done
echo rdb is now available. Continuing.
psql --command="\COPY provenance TO '/var/lib/neo4j/import/provenance.csv' WITH (FORMAT CSV, HEADER);" postgresql://dev:dev@rdb:5432/askem

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
