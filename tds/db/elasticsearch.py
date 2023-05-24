"""
The configured ElasticSearch DB engine
"""
import logging
import time

from elastic_transport import ConnectionError as EsConnectionError
from elasticsearch import Elasticsearch

from tds.settings import settings

logger = logging.Logger(__name__)


def es_client():
    """
    Factory Function that provides an ElasticSearch connection.
    """
    return Elasticsearch(
        [settings.ES_URL], basic_auth=(settings.ES_USERNAME, settings.ES_PASSWORD)
    )


def wait_for_es_up(
    client=None, timeout=120, sleep=5, healthy_statuses=("yellow", "green")
):
    """
    Function provides a healthcheck for ElasticSearch.
    """
    # Use default client if not provided
    if client is None:
        client = es_client()

    # Wait for cluster to become healthy enough to create indexes
    healthy = False
    start = time.time()
    logger.debug("ES wait for up started at %s", start)
    es_logger = logging.getLogger("elastic_transport")
    original_es_logging_level = es_logger.level
    es_logger.setLevel(logging.ERROR)
    while not (healthy or (time.time() - start) > timeout):
        try:
            health = client.health_report()
            healthy = health["status"] in healthy_statuses
        except EsConnectionError:
            logger.warning("ElasticSearch is not ready. Sleeping %s seconds", sleep)
            time.sleep(sleep)
    es_logger.setLevel(original_es_logging_level)
    logger.debug("ES wait finished at %s", time.time())
