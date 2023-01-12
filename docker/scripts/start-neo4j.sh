#!/bin/bash

# TODO: Run the script dynamically when Postgres is available instead of sleeping
sleep 2

psql --command="\COPY provenance TO '/var/lib/neo4j/import/provenance.csv' WITH (FORMAT CSV, HEADER);" postgresql://dev:dev@rdb:5432/askem

set -m
/startup/docker-entrypoint.sh neo4j &

# TODO: run this using apoc.initialize
sleep 8
cypher-shell -u neo4j -p password -f /tmp/populate-cache.cypher --non-interactive
echo "Loaded all data"

fg %1