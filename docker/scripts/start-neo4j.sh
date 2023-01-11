#!/bin/bash

# TODO: Run the script dynamically when Postgres is available instead of sleeping
sleep 5

psql --command="\COPY provenance TO '/var/lib/neo4j/import/provenance.csv' WITH (FORMAT CSV, HEADER);" postgresql://dev:dev@rdb:5432/askem

/startup/docker-entrypoint.sh neo4j