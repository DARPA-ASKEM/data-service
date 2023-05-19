"""
The configured ElasticSearch DB engine
"""
import logging
import time

from elastic_transport import ConnectionError
from elasticsearch import Elasticsearch

from tds.settings import settings

logger = logging.Logger(__name__)

url = f"http://{settings.ES_HOST}:{settings.ES_PORT}"

es = Elasticsearch([url])


def wait_for_es_up(timeout=120, sleep=5, healthy_statuses=("yellow", "green")):
    # Wait for cluster to become healthy enough to create indexes
    healthy = False
    start = time.time()
    logger.debug(f"ES wait for up started at %s", start)
    es_logger = logging.getLogger("elastic_transport")
    original_es_logging_level = es_logger.level
    es_logger.setLevel(logging.ERROR)
    while not (healthy or (time.time() - start) > timeout):
        try:
            health = es.health_report()
            healthy = health["status"] in healthy_statuses
        except ConnectionError:
            logger.warn("ElasticSearch is not ready. Sleeping %s seconds", sleep)
            time.sleep(sleep)
    es_logger.setLevel(original_es_logging_level)
    logger.debug("ES wait finished at %s", time.time())
