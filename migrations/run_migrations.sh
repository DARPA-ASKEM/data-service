#!/usr/bin/env bash

echo "Running migrations."
alembic -c migrations/alembic.ini upgrade head 2>/dev/stdout
echo "Migrations complete."

# echo "Checking storage bucket."
# python migrations/scripts/file_storage.py create_bucket

# echo "Running Elasticsearch index build"
# python migrations/scripts/start_elasticsearch.py

# if [[ "$SEED_DATA" == "true" ]] ; then
#   echo "Seeding Data"
#   python migrations/scripts/start_elasticsearch.py "seed"
#   python migrations/scripts/seed_data.py
#   python migrations/scripts/file_storage.py upload_file datasets
# fi
# To Troubleshoot the migration container, uncomment the following lines:
#touch /logger.log
#tail -f /logger.log
echo "Completed running migrations."
exit 0
