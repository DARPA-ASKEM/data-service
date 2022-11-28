#!/bin/bash
set -e

echo "Restoring dev data..."
pg_restore --format=tar --username=dev -v -d askem /var/lib/postgresql/backup/data-service-dev-db.sql
echo "dev data restored!"