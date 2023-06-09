#!/usr/bin/env bash
is_up_to_date=$(alembic -c migrate/alembic.ini check)

if [[ $is_up_to_date == *"Target database is not up to date."* ]] ; then
  echo "Running migrations."
  alembic -c migrate/alembic.ini upgrade head
fi
echo "Completed Postgres migrations."


echo "Running Elasticsearch index build"

python migrate/start_elasticsearch.py


if [[ "$SEED_DATA" == "true" ]] ; then
  echo "Seeding Data"
fi
touch /logger.log
tail -f /logger.log
echo "Booting TDS API."
exit 0
